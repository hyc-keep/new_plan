# scripts/test.py 怎么看

> 本文档是 `scripts/test.py` 的学习型说明文，覆盖 03_UNet稳定性 阶段的测试评估脚本。
> 如果你已经读过 02 阶段的同文件说明文，可以直接跳到「A2 阶段新增与变化」看本阶段增量。

## 结构化溯源卡片

- 正式对象: `scripts/test.py`
- 对应阶段: `03_UNet稳定性`

### 论文依据
- 论文: Sirinukunwattana et al., 2017, "Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest"
- 章节: §2.3 (Evaluation Metrics)
- 公式/定义: Dice coefficient, Object-level Dice, Object-level Hausdorff distance

### 代码依据
- 仓库: https://github.com/milesial/Pytorch-UNet
- 文件: `src/models/unet.py`
- commit: 参考 master 分支（推理前向参考，本地已改写落地）
- 许可证: GPL-3.0（上游参考）/ project_internal（本地实现）

### 冻结回链
- 冻结文件: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `threshold_value`, `threshold_source`, `eval_cast_policy`, `boundary_metric_width`, `connected_components_connectivity`

### 当前实现落点
- 文件: `scripts/test.py`
- 符号: `main()` / `_write_metrics_csv()` / `_write_metric_crosscheck_note()` / `_update_run_meta()` / `export_run_visual_assets()`

## 这个脚本的作用

结论先行：这是整个 03 阶段实验链的**评估入口**，负责把 train.py 训出来的 best checkpoint 变成一份可审计的成绩单。

用人话说就是：train.py 造了一个模型，test.py 负责给它出"考试成绩单"。这份成绩单不只是几个数字，而是包含每个样本的 sample-only CSV、crosscheck note（sample 均值与派生重聚合结果的交叉验证）、独立 PNG+GT 复核以及 worst-case 可视化导出；正式测试 CSV 不写 aggregate 行。

它不负责：训练模型（那是 `scripts/train.py` 的事）、聚合多 seed 结果（那是 `scripts/summarize_stage.py` 的事）、定义评估指标（那是 `src/eval/run_eval.py` 的事）。

## 这个脚本在整个阶段中的位置

结论先行：test.py 是三段式实验链的第二段，读上游 checkpoint，产出下游聚合所需的逐样本 CSV 与协议补写。

它的上游依赖有两层：

- 上游依赖 1：`scripts/train.py` 产出的 best checkpoint（每个 seed 一份）
- 上游依赖 2：评估协议配置 `configs/eval/eval_proto_v1.yaml`（定义 threshold 与指标口径）

它的下游消费者也很明确：

- 下游消费者 1：`scripts/summarize_stage.py` 读取本脚本产出的 testA/testB 逐样本 CSV 做 3-seed 聚合
- 下游消费者 2：阶段验收读取本脚本补写的 run_meta 字段核对协议一致性

用一张流程图说明本脚本在链路中的位置：

```text
scripts/train.py
        ↓  产出 best checkpoint + run_meta.yaml
scripts/test.py  (本文件 — 每个 seed 各评估 testA/testB)
        ↓  产出 testA_metrics.csv / testB_metrics.csv / metric_crosscheck_note.md
scripts/summarize_stage.py  →  阶段验收
```

用人话说就是：train.py 造模型 → test.py 检验模型 → summarize_stage.py 汇总结论。

## 当前实现状态

结论先行：正式可用，A2 阶段已用它完整跑过 3 seed 的 testA/testB 评估，非占位壳。

- 状态：正式可用，`experiments/A2_UNet_GlaS_seed3407/testA_metrics.csv` 等评估产物均存在
- 当前真实定位：03_UNet稳定性 阶段正式评估入口
- 测试覆盖：3 seed × 2 split = 6 组评估全部完成，crosscheck 全部 pass

你现在可能会问："test.py 在 02 阶段就写好了，03 阶段有什么变化？"

关键变化不是脚本重写，而是用它跑了 6 组评估，并要求三次协议字段完全一致——这是 A2 稳定性验证的下游证据来源。

## 脚本核心逻辑

### 主要流程

当用 seed3407 配置启动评估时，脚本按下面顺序执行：

1. 加载 checkpoint（`_resolve_checkpoint_path` → `_load_checkpoint`）：默认加载实验目录下 checkpoints/best.ckpt，通过 model_state_dict 还原权重
2. 构建 test DataLoader：testA/testB 各一个，走 build_eval_transform（无增强），保证与训练 val 阶段一致
3. 逐 split 评估（`evaluate_split`）：forward → sigmoid → threshold(0.5) → 二值预测，计算 pixel/object/boundary 三层指标
4. 写入逐样本 CSV（`_write_metrics_csv`）：每行一个样本，测试 CSV 不写 aggregate 行；同时落盘同空间 eval image、GT 与 prediction PNG
5. 写入 crosscheck note（`_write_metric_crosscheck_note`）：从 sample rows 重算每个 split 的均值，并核对正式 CSV 与独立 PNG+GT 复算结果
6. 更新 run_meta（`_update_run_meta`）：把 testA/testB 的 sample_count、指标摘要、协议字段与 crosscheck 状态写回，作为 run 级审计入口
7. 导出可视化（`export_run_visual_assets`）：每 split 导出最多若干 worst-case 三联图 + error_cases

### 关键函数：`_write_metrics_csv()` — sample-only CSV 与同空间评估资产

这是评估资产落盘层——把每个样本的指标和 source/eval lineage 写进 sample-only CSV，并将 eval image、GT 和 prediction 导出到同一评估空间。字段包含 row_type, sample_id, split_role, objdice, dice, iou, f1, boundary_f1, hd95, object_hausdorff, source_image_path, source_mask_path, eval_image_path, eval_gt_path, pred_path。

> 溯源锚点：
> - 理论依据：阶段总协议 §8.1 要求 raw CSV 含 boundary_metric_* 与 connected_components_*
> - 冻结表对应：参数冻结总表中 threshold_value、boundary_metric_width
> - 当前实现：`scripts/test.py` → `_write_metrics_csv()` 与 `export_run_visual_assets()`

### 关键函数：`_write_metric_crosscheck_note()` — 指标交叉验证与独立资产复核

这个函数做一件非常关键的事：从 sample-only 行重算 split 均值，并与独立 PNG+GT 复核结果对比。

为什么要这样做？因为正式测试 CSV 不写 aggregate 行，split 汇总和 raw/mean±std 表都由 sample 行派生；如果正式 CSV、sample 重聚合和 PNG+GT 独立复核的最大绝对误差超过容忍度（1e-6），说明指标资产链存在问题。

你现在可能会问："这跟稳定性验证有什么关系？"关系很大——如果三个 seed 的 crosscheck 都 pass，你能确信每个 run 内部指标计算没有 bug；如果一个 pass 一个 fail，那 fail 的 run 就不能被纳入 mean±std 聚合。

> 溯源锚点：
> - 理论依据：阶段总协议 §8.1 三层落盘机制中的 crosscheck 要求
> - 冻结表对应：参数冻结总表中 eval_cast_policy、boundary_metric_width、connected_components_connectivity
> - 当前实现：`scripts/test.py` → `_write_metric_crosscheck_note()` L184-236

### 为什么这样设计（候选方案对比）

| 候选方案 | 看起来的好处 | 实际问题 | 最终决策 |
|---|---|---|---|
| 只输出 aggregate 汇总数字 | 文件小、看起来干净 | 无法定位是哪个样本拖低指标，无法做 worst-case 分析 | 为什么不用：否决 |
| aggregate 与逐样本均值各算各的、不做校验 | 省一次遍历 | 指标 bug 无法被发现，稳定性结论不可信 | 为什么不选：否决 |
| sample-only CSV + crosscheck note + 独立 PNG/GT 复核 | 可追溯到样本，并验证重聚合与资产空间一致 | 需要额外复核资产和 note | 最终决策：采用 |

## A2 阶段新增与变化

相比 02 阶段，A2 的 test.py 有这三点关键变化：

1. 三层落盘固化：run_meta 补写 eval_cast_policy、connected_components_connectivity、boundary_metric_width 字段，作为 summarize_stage.py 协议一致性校验的输入
2. T-9 保护：每次运行前只清空对应 split 的 predictions 子目录，不误删正式训练目录
3. metric_list 协议对齐：run_meta 中 metric_list 固定为 f1/objdice/object_hausdorff/dice/iou/hd95/boundary_f1，与 summarize_stage.py 中的最小列定义一致

你可能会问："为什么 testA 和 testB 要分开评估？"因为 GlaS 官方划分就是 testA(60) + testB(20) 两个 hold-out 子集，分开评估是为了与论文口径可比，并观察不同难度 split 的表现差异。

## 如何运行这个脚本

环境要求：Python 3.10+，CUDA-capable GPU（CPU fallback 仅用于 preflight/联调，不得作为正式 A2 评估结果），依赖 torch/torchvision/Pillow/PyYAML/numpy/scipy。

完整评估命令：

```bash
cd crc_gland_segmentation_project
python scripts/test.py --config configs/experiment/A2_UNet_GlaS_v1_seed3407.yaml  # 文件名 v1 是配置版本；run_name 为 A2_UNet_GlaS_seed3407
```

参数说明：

- --config：实验配置路径（必填）
- --run-name：可选覆盖 run_name
- --checkpoint：可选指定 checkpoint 路径（默认 best.ckpt）
- --max-samples-per-split：限制评估样本数（仅用于 CPU 连通性检查）
- --max-visual-samples：每个 split 最多导出多少 worst-case 样本（默认 5）
- --skip-visuals：跳过可视化和 error_cases 导出

运行成功后，实验目录下会有 testA_metrics.csv、testB_metrics.csv、metric_crosscheck_note.md、summaries/run_summary.md、predictions/、visuals/。

## 如何验证脚本运行结果

下面三个验证点按顺序执行，可确认逐样本 CSV 行数正确、crosscheck 全部通过、run_meta 评估字段完整。

### 验证点 1：CSV 行数正确
- 操作：查看 testA_metrics.csv 为 1 行表头 + 60 行 sample，testB_metrics.csv 为 1 行表头 + 20 行 sample；两份正式 CSV 均无 aggregate 行
- 通过标准：testA_sample_count=60、testB_sample_count=20
- 实际结果：三 seed 均对齐

### 验证点 2：crosscheck 全部 pass
- 操作：查看三个 seed 的 metric_crosscheck_note.md 中 metric_crosscheck_result 字段
- 通过标准：所有 run 均为 pass
- 实际结果：三 seed 全部 pass

### 验证点 3：run_meta 评估字段完整
- 操作：查看 run_meta.yaml 是否含 eval_cast_policy、boundary_metric_width、connected_components_connectivity
- 通过标准：三字段均存在且与冻结表一致
- 实际结果：一致 — eval_cast_policy=float32_before_threshold、boundary_metric_width=3、connected_components_connectivity=8

## 误区和排错点

### 误区 1：F1 和 Dice 对二值分割永远相等

**错。这正是本阶段曾经踩过的坑。** GlaS 主表的 F1 是**对象级检测 F1**（连通域实例化后按 overlap>0.5、GT 面积归一做对象匹配，F1=2TP/(2TP+FP+FN)），它和像素级 Dice 完全不是一回事，数值也不同（历史旧版本示例：testA F1≈0.61 vs Dice≈0.89；该数字不是当前 A2 结果）。此前代码误把 F1 实现成像素 Dice，导致两列逐位相等，并被错误解释成"二值分割数学恒等式"——该结论已于 20260711 推翻并按官方口径重算，详见 `实现依据记录.md` 第 13 节。只有"像素级 F1"才等于 Dice，但那不是本项目主表要报告的 F1。

### 误区 2：crosscheck pass 就说明指标"正确"

crosscheck 只验证 sample_mean ≈ aggregate 的内部一致性，不验证指标定义是否合理、是否与论文口径一致、threshold 是否最优。那些是协议层面的判断。

### 误区 3：HD95 为 nan 或异常大就是模型崩了

HD95 对小目标非常敏感。如果 ground truth 里有一个 2px 的微小腺体、模型完全没预测到，HD95 会直接跳到巨大值。这在医学图像分割里很常见，不应直接判为模型崩溃。

### 协议违规风险

- 把 threshold 从 0.5 改成 0.3 但没改 eval config，crosscheck 仍可能 pass 但评估口径与协议不一致
- 删掉 error_cases 导出，`scripts/summarize_stage.py` 的 failure_summary_ready 检查会受影响

## 与项目其他部分的关联

- 上游依赖：`scripts/train.py`（读 checkpoint）与 `configs/eval/eval_proto_v1.yaml`（读评估协议）
- 下游消费者：`scripts/summarize_stage.py`（读逐样本 CSV 做聚合）
- 评估指标实现：`src/eval/run_eval.py`

## 阶段协议回链卡片

- 当前阶段总协议: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`
- 三次重复设计: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md`
- 上一阶段放行文件: `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 正式规则文件: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 路线锁定文件: `结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`

## 建议联读

- `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_train.py.md` — 上游训练入口
- `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_summarize_stage.py.md` — 下游聚合脚本
- `reports/stage_reports/implementation_tracking/03_UNet稳定性/configs_eval_eval_proto_v1.yaml.md` — 评估协议配置

## 学完后你应该具备什么能力

- 知道 test.py 从 checkpoint 加载到 CSV 输出的完整链路
- 理解 crosscheck 机制防止的是什么问题
- 能说出三层落盘的第二层（raw CSV）和第一层补写（run_meta）具体包含什么字段
- 能区分 pixel-level 和 object-level 指标的不同含义

### 5 分钟自检任务

- [x] 确认任意一个 seed 的 testA_metrics.csv 有 61 行
- [x] 确认三个 seed 的 metric_crosscheck_result 都是 pass
- [x] 说出主表 F1（对象级检测 F1）与像素 Dice 的区别，以及为什么二者数值不同
- [x] 说出 testA/testB sample-only CSV 的 lineage、指标字段和 `not_applicable` loss 字段

## 当前消费口径与审计闭环

本评估入口当前只消费 `A2_UNet_GlaS_seed3407`、`A2_UNet_GlaS_seed1234`、`A2_UNet_GlaS_seed2025` 和 `eval_proto_v1`；`protocol_v3` 仅作历史追溯。精确聚合结果由 `reports/tables/unet_mean_std_summary.csv` 给出：Object F1 testA=`0.5290508133298323±0.06534870542228736`、testB=`0.5864995222306099±0.017711580461373767`；Object Dice testA=`0.7081049877960447±0.0528843478663972`、testB=`0.7755628763239749±0.01214631192503348`；Pixel Dice testA=`0.8687005312137156±0.014245648618802897`、testB=`0.8785019406751632±0.007950925190263055`；IoU testA=`0.7802676159056027±0.023159000977374777`、testB=`0.7926352354780709±0.009535961930616718`。stage gate、workflow gate、handoff 的通过均不等于 04 自身通过。

直接依赖为 checkpoint、eval_proto_v1 和数据模块；下游为 summarize_stage.py。冲突裁决：旧 F1/旧协议不可当前消费。回退条件：协议字段或 crosscheck 失败时不得进入聚合，回退重评估。

## 文件质量自检

- [x] 当前身份、协议、结果源和对象/像素指标区分清楚。
- [x] 依赖、下游、冲突与回退边界已写明。

## Diagnostics 闭环

已扫描本阶段 Markdown 的 F1/Dice 口径、协议和身份残留；旧错误数字均有历史更正语境，未发现未标注当前消费项。

## 审计对表

评估协议 → 当前实现落点；聚合表 → 精确结果；历史更正 → 冲突裁决；全目录扫描 → diagnostics；缺口：无。

## 版本更新记录

| 日期 | 改动内容 | 影响范围 | 是否需要重新验证 |
|------|---------|---------|----------------|
| 2026-07-10 | A2 阶段首次创建学习型说明文 | 本文档 | 是 |
| 2026-07-10 | 按门禁补齐设计取舍/衔接章节与阶段协议回链卡片，清理无法解析的路径锚点与内联命令 | 本文档 | 是 |
