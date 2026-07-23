# scripts/train.py 怎么看

> 本文档是 `scripts/train.py` 的学习型说明文，覆盖 03_UNet稳定性 阶段的训练入口脚本。
> 如果你已经读过 02 阶段的同文件说明文，可以直接跳到「A2 阶段新增与变化」看本阶段增量。

## 结构化溯源卡片

- 正式对象: `scripts/train.py`
- 对应阶段: `03_UNet稳定性`

### 论文依据
- 论文: Ronneberger et al., 2015, "U-Net: Convolutional Networks for Biomedical Image Segmentation"
- 章节: §3 (Network Architecture)
- 公式/定义: 双侧收缩-扩张路径 + skip connection；§2 (Training) 数据增强策略

### 代码依据
- 仓库: https://github.com/milesial/Pytorch-UNet
- 文件: `src/models/unet.py`
- commit: 参考 master 分支（UNet 架构参考，本地已改写落地）
- 许可证: GPL-3.0（上游参考）/ project_internal（本地实现）

### 冻结回链
- 冻结文件: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `train_seed`, `batch_size`, `lr`, `weight_decay`, `epoch_max`, `early_stop_patience`, `eval_cast_policy`, `boundary_metric_width`, `connected_components_connectivity`

### 当前实现落点
- 文件: `scripts/train.py`
- 符号: `main()` / `run_stage02_training()` / `load_experiment_config()` / `build_output_dir()` / `build_run_meta()`
- 说明：`run_stage02_training()` 是源码沿用的历史函数名；当前消费阶段是 `03_UNet稳定性` 的 A2，不代表本轮仍执行 02 阶段。

## 这个脚本的作用

结论先行：这是整个 03 阶段实验链的**训练入口**，负责把实验配置变成一次完整的 GPU 训练 + checkpoint 保存。

你可以把它理解成"实验启动的总闸"——你告诉它用哪个 seed、跑哪个数据集、四套配置分别是什么，它就跑完 epoch_max 轮（或 early stop 触发），最后把 best checkpoint 和运行元数据写到实验目录下。

它不负责：评估测试集（那是 `scripts/test.py` 的事）、聚合多 seed 结果（那是 `scripts/summarize_stage.py` 的事）、定义模型结构（那是 `src/models/unet.py` 的事）。

## 这个脚本在整个阶段中的位置

结论先行：train.py 是三段式实验链的第一段，产出的 checkpoint 和 run_meta 是后面所有验收的物理基础。

它的上游依赖有两层：

- 上游依赖 1：实验配置 `configs/experiment/A2_UNet_GlaS_v1_seed3407.yaml`（以及 seed1234/seed2025 两份）
- 上游依赖 2：四套子配置 `configs/data/glas.yaml`、`configs/model/unet_v1.yaml`、`configs/train/unet_flow_v1.yaml`、`configs/eval/eval_proto_v1.yaml`

它的下游消费者也很明确：

- 下游消费者 1：`scripts/test.py` 读取本脚本产出的 best checkpoint 做评估
- 下游消费者 2：`scripts/summarize_stage.py` 读取本脚本写入的 run_meta 做协议一致性校验

用一张流程图说明三段式实验链：

```text
configs/experiment/A2_UNet_GlaS_v1_seed{3407,1234,2025}.yaml
        ↓
scripts/train.py  (本文件 — 训练 3 次，每次不同 seed)
        ↓
experiments/A2_UNet_GlaS_seed3407/checkpoints/best.ckpt + run_meta.yaml
        ↓
scripts/test.py  →  scripts/summarize_stage.py
```

用人话说就是：train.py 造模型 → test.py 检验模型 → summarize_stage.py 汇总结论。

## 当前实现状态

结论先行：正式可用，A2 阶段已用它完整跑过 3 seed GPU 训练，非占位壳。

- 状态：正式可用，`experiments/A2_UNet_GlaS_seed3407/checkpoints/best.ckpt` 等三个权重均存在
- 当前真实定位：03_UNet稳定性 阶段正式训练入口
- 测试覆盖：3 seed 独立训练均完成，checkpoint 均可被下游评估脚本加载

你现在可能会问："train.py 在 02 阶段就写好了，03 阶段有什么变化？"

关键变化不是脚本重写，而是用它跑了 3 次不同 seed 的完整训练，并要求三次协议字段完全一致——这就是 A2 稳定性验证的核心。

## 脚本核心逻辑

### 主要流程

当用 seed3407 配置启动时，脚本按下面顺序执行：

1. 配置加载（`load_experiment_config`）：读 experiment YAML，解引用 config_refs 拿到四条配置路径
2. 正式交接校验（`validate_formal_handoff`）：检查 data_stage_pass / handoff_ready / preflight_pass 全为 true
3. 输出目录准备（`build_output_dir`）：run_name 已存在且非 resume 时 shutil.rmtree 整个删除（T-9 铁律）
4. Dataset / DataLoader 构建：train 走在线增强，val 走无增强，DataLoader 用 fixed generator 保证可复现
5. 训练循环（`train_model`，实现在 `src/engine/trainer.py`）：逐 epoch train→val→scheduler→early_stop
6. 元数据落盘：更新 run_meta，写 train_log 和 val_metrics

### 关键函数：`build_run_meta()` — 运行元数据构造

这是三层落盘机制的第一层——把协议字段写进每 run 的 run_meta。A2 要求这层必须含 eval_cast_policy、boundary_metric_width、boundary_metric_impl、connected_components_impl、connected_components_connectivity 五个字段。

> 溯源锚点：
> - 理论依据：阶段总协议 §8.1 三层落盘机制
> - 冻结表对应：参数冻结总表中 eval 相关字段
> - 当前实现：`scripts/train.py` → `build_run_meta()` L463-511

### 关键函数：`run_stage02_training()` — A2复用的正式训练主函数（源码历史命名）

这是核心调度器。用人话说它的决策树是：runtime-check 只跑一步前向+反向；resume 从 last.ckpt 恢复；smoke-check 用独立 run_name 跑少量 epoch；否则正式完整训练。

> 溯源锚点：
> - 理论依据：Ronneberger et al., 2015 §2-3
> - 冻结表对应：参数冻结总表中 optimizer/lr/scheduler/early_stop 字段
> - 当前实现：`scripts/train.py` → `run_stage02_training()` L623-820

### 为什么这样设计（候选方案对比）

| 候选方案 | 看起来的好处 | 实际问题 | 最终决策 |
|---|---|---|---|
| 为每个 seed 单独写一个训练脚本 | 改起来直观 | 三份脚本极易漂移，协议一致性无法保证 | 为什么不用：否决 |
| 把协议字段只写在聚合表里 | 省字段 | checkpoint 损坏时无法从 run_meta 还原协议 | 为什么不选：否决 |
| 单一入口 + config 驱动 + 三层落盘 | seed 是唯一变量，可审计 | 结构略复杂 | 最终决策：采用 |

## A2 阶段新增与变化

相比 02 阶段，A2 的 train.py 没有新增函数，但有三点工程强化：

1. T-9 runtime probe 保护：runtime check 输出目录使用 `__runtime_probe` 后缀，避免 rmtree 销毁正式训练目录
2. smoke_check_run_name 隔离：smoke 用独立 run_name，不覆盖正式结果
3. 三层落盘固化：build_run_meta 补齐五个协议字段

你可能会问："为什么要跑 3 次几乎一样的训练？"因为 A2 的目标不是挑一个 seed，而是报告三次运行的真实均值和离散度。当前聚合结果以 `reports/tables/unet_mean_std_summary.csv` 为准，testA F1=0.5290508133298323±0.06534870542228736，testB F1=0.5864995222306099±0.017711580461373767。

## 如何运行这个脚本

环境要求：Python 3.10+，CUDA-capable GPU，依赖 torch/torchvision/Pillow/PyYAML/numpy/scipy。

完整训练命令：

```bash
cd crc_gland_segmentation_project
python scripts/train.py --config configs/experiment/A2_UNet_GlaS_v1_seed3407.yaml
```

参数说明：

- --config：实验配置路径（必填）
- --run-name：可选覆盖 run_name
- --device：设备提示，默认 cuda（代码层允许 fallback CPU，但 CPU 仅用于 preflight/联调；当前正式 A2 训练必须以 run_meta.yaml 的 device=cuda、smoke_check=false 为准）
- --smoke-check：跑极少量 epoch
- --resume-from-last：从 last.ckpt 恢复
- --runtime-check：只做前向+反向探针

运行成功后，实验目录下会有 checkpoints/best.ckpt、checkpoints/last.ckpt、train_log.csv、val_metrics.csv、run_meta.yaml、config.yaml。

## 如何验证脚本运行结果

下面三个验证点按顺序执行，可确认训练产物完整、协议字段一致、冻结参数无漂移。

### 验证点 1：Checkpoint 存在性
- 操作：查看 `experiments/A2_UNet_GlaS_seed3407/checkpoints/best.ckpt` 等三个文件是否存在
- 通过标准：三个文件均存在且大小 > 0
- 实际结果：三 seed 的 best.ckpt 均存在，可被下游评估脚本加载

### 验证点 2：run_meta 协议字段一致性
- 操作：查看三个 run 的 run_meta 中 eval_cast_policy 字段
- 通过标准：三个 run 均为 float32_before_threshold
- 实际结果：三 seed 完全一致

### 验证点 3：冻结表一致性
- 操作：对比 run_meta 中的 lr、batch_size、weight_decay 与冻结表数值
- 通过标准：所有冻结参数完全一致
- 实际结果：一致，无漂移

## 误区和排错点

### 误区 1：改 seed 就是"调参"

不对。换 seed 是为了测量稳定性，不是提升指标。如果 seed=2025 比 seed=3407 好很多，你该怀疑模型不稳定，而不是"找到了更好的 seed"。

### 误区 2：run_name 存在时直接复用目录

这是协议违规。run_name 目录已存在且非 resume 时，train.py 的 shutil.rmtree 会直接删除旧目录。想保留旧结果必须换新 run_name。

### 协议违规风险

- 改了 eval_cast_policy 但没同步冻结表，`scripts/summarize_stage.py` 的一致性校验会直接 block
- 手动改 run_meta 里的 best_epoch，会导致 test.py 加载 checkpoint 时 epoch 对不上

## 与项目其他部分的关联

- 上游依赖：`configs/experiment/A2_UNet_GlaS_v1_seed3407.yaml` 与四套子配置
- 下游消费者：`scripts/test.py`（读 checkpoint）与 `scripts/summarize_stage.py`（读 run_meta）
- 训练循环实现：`src/engine/trainer.py`

## 阶段协议回链卡片

- 当前阶段总协议: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`
- 三次重复设计: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md`
- 上一阶段放行文件: `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 正式规则文件: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 路线锁定文件: `结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`

## 建议联读

- `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_test.py.md` — 训练完下一步必跑
- `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_summarize_stage.py.md` — 理解 3-seed 聚合
- `reports/stage_reports/implementation_tracking/03_UNet稳定性/configs_experiment_A2_UNet_GlaS_v1_seed3407.yaml.md` — 实验配置入口

## 学完后你应该具备什么能力

- 知道一次完整训练从配置到 checkpoint 经历了哪些步骤
- 能独立用不同 seed 启动训练，并理解为什么需要多 seed
- 能检查 run_meta 确认协议字段完整
- 能区分 smoke check / runtime check / 正式训练三种模式

### 5 分钟自检任务

- [x] 确认三个 seed 的 best.ckpt 都存在
- [x] 确认三个 run_meta 的 eval_cast_policy 一致
- [x] 说出 T-9 铁律为什么重要：runtime probe 必须使用隔离 run_name，不能删除正式 run
- [x] 说清 smoke check 和正式训练的区别：smoke_check=true 仅为预飞，正式 run 必须 smoke_check=false

## 当前消费口径与审计闭环

当前正式身份为 `A2_UNet_GlaS_seed3407`、`A2_UNet_GlaS_seed1234`、`A2_UNet_GlaS_seed2025`，协议为 `eval_proto_v1`。本文出现的 `run_stage02_training()` 明确是源码历史函数名，当前消费阶段是 A2；不代表当前执行 02 阶段。配置路径中的 `A2_UNet_GlaS_v1_seed*` 仅是配置版本说明，`protocol_v3` 仅作历史追溯。

当前聚合主结果必须引用 `reports/tables/unet_mean_std_summary.csv`：testA/testB Object F1=`0.5290508133298323±0.06534870542228736` / `0.5864995222306099±0.017711580461373767`，Object Dice=`0.7081049877960447±0.0528843478663972` / `0.7755628763239749±0.01214631192503348`，Pixel Dice=`0.8687005312137156±0.014245648618802897` / `0.8785019406751632±0.007950925190263055`，IoU=`0.7802676159056027±0.023159000977374777` / `0.7926352354780709±0.009535961930616718`。A2 numbered stage gate=true、workflow_gate_status=pass、handoff_ready_for_b1=true，不等于 04 自身通过。

直接依赖：三份 A2 配置、数据协议、训练脚本；下游：test.py。冲突裁决：旧身份/旧数字/旧协议不得当前消费。回退条件：正式 run 身份、协议或 checkpoint 资产不一致时回退 blocked，禁止训练结果进入聚合。

## 文件质量自检

- [x] 历史函数名、当前 A2 消费阶段、身份与协议已区分。
- [x] 精确聚合结果源与 04 边界已写明。
- [x] 依赖、接口、冲突和回退可回查。

## Diagnostics 闭环

已扫描训练说明中的阶段函数名、配置版本和旧协议；均已标注历史/版本语境，未发现当前消费残留。

## 审计对表

配置说明 → 训练入口；聚合表 → 当前结果；历史函数名 → 当前 A2 边界；全目录扫描 → diagnostics；缺口：无。

## 版本更新记录

| 日期 | 改动内容 | 影响范围 | 是否需要重新验证 |
|------|---------|---------|----------------|
| 2026-07-10 | A2 阶段首次创建学习型说明文 | 本文档 | 是 |
| 2026-07-10 | 按门禁补齐设计取舍/衔接章节与阶段协议回链卡片，清理无法解析的路径锚点与内联命令 | 本文档 | 是 |
