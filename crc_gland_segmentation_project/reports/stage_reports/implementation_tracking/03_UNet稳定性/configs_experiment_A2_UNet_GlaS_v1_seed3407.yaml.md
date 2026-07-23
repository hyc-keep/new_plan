# configs/experiment/A2_UNet_GlaS_v1_seed3407.yaml 怎么看

> 结论先行：这个文件是 A2 稳定性阶段的**主实验配置**，也是 seed1234/seed2025 两个配置的派生母版。
> 你可以把它理解成"实验的一键启动指令"——所有复杂设置都通过 `config_refs` 解引用到子配置，这个文件本身保持极简。

## 这个文件是干什么的

这个 YAML 是三次重复实验里的第一次运行入口，同时充当另外两个 seed 配置的模板。

它告诉训练入口 `scripts/train.py`：这次训练叫什么名字、用哪个 seed、四套子配置分别在哪里、属于哪个阶段和数据集。

用人话说，你不用每次在命令行里写一堆参数，只要指定这个配置文件，训练脚本就会自己把 data/model/train/eval 四条链读齐。

## 这张表/这个文件长什么样

这个文件字段集中，核心是三类：身份字段、seed 字段、`config_refs` 解引用块。

身份字段回答"这是谁"：run_name、stage_code、dataset_code、model_name、config_version 一起把这次运行钉在 A2 阶段的 UNet-GlaS 坐标上。

seed 字段回答"这是第几次"：train_seed=3407 是本文件唯一的实验变量，result_tag 与 aggregation 标注它是单 seed 重复实验的一员。

config_refs 块回答"参数在哪"：它把 data/model/train/eval 四条链解引用到各自的子配置，主配置本身不写任何超参。下面是文件的完整骨架：

```text
run_name: A2_UNet_GlaS_seed3407
stage_code: A2
dataset_code: glas
model_name: unet
config_version: v1
train_seed: 3407
result_tag: reproduced
aggregation: single_seed
smoke_check_run_name: A2_UNet_GlaS_seed3407_smoke
config_refs:
  data: configs/data/glas.yaml
  model: configs/model/unet_v1.yaml
  train: configs/train/unet_flow_v1.yaml
  eval: configs/eval/eval_proto_v1.yaml
```

## 当前真实结果

这次运行的正式产物落在 `experiments/A2_UNet_GlaS_seed3407/checkpoints/best.ckpt`；文件名中的 `v1` 仅表示配置文件版本，不是 run_name。当前真实 `run_meta` 记录 `best_epoch=53`、`epoch_count=73`、`best_metric_value=0.7564017193729246`；文件名中的 `v1` 仅表示配置文件版本，不是 run_name。

它在两个 hold-out split 上的真实数值是：

| split | F1 | Object Dice |
|-------|-----|-------------|
| testA | 0.48767052693586427 | 0.7161130786024664 |
| testB | 0.5759520040353598 | 0.7881474813649879 |

这些数值和 `reports/tables/unet_seed_results.csv` 里 seed=3407 的对应行完全一致。

## 这些列/字段分别是什么意思

逐字段说明如下，每个字段都能在配置里核对：

- `run_name`：决定输出目录名，本次为 A2_UNet_GlaS_seed3407；配置文件名中的 `v1` 仅表示配置版本。
- `stage_code`：阶段代号 A2（不是 03）——A/B 是实验编号体系，A1=02阶段、A2=03阶段、B1=04阶段
- `dataset_code`：数据集代码 glas
- `train_seed`：本文件的核心变量，值为 3407，控制参数初始化与数据 shuffle
- `result_tag`：reproduced，表示这是重复实验
- `aggregation`：single_seed，说明本文件只是一次单 seed 运行
- `smoke_check_run_name`：smoke 专用运行名，避免 smoke 覆盖正式结果
- `config_refs`：四套子配置的解引用映射

## 配置解引用机制

用人话说这段配置链是这样走的：主配置只写一层身份，真正的参数在四套子配置里。

- 数据参数在 `configs/data/glas.yaml`
- 模型参数在 `configs/model/unet_v1.yaml`
- 训练超参在 `configs/train/unet_flow_v1.yaml`
- 评估口径在 `configs/eval/eval_proto_v1.yaml`

好处是：想换模型只需改这里 `config_refs` 的 model 一行，不用动脚本。

## 阶段协议回链卡片

- 当前阶段总协议: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`
- 三次重复设计: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md`
- mean±std 汇总规则: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/02_mean_std汇总规则.md`
- 上一阶段放行文件: `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 正式规则文件: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 路线锁定文件: `结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`

这组回链证明：这个配置的身份字段和 seed 集合来自 03 阶段计划点名；它继承的评估口径来自参数冻结总表；它被允许启动，是因为上一阶段 A1 已经放行。

## 溯源与冻结依据

- 论文依据：U-Net 基线身份来自 Ronneberger et al., 2015；GlaS 数据集口径来自 Sirinukunwattana et al., 2017
- 冻结依据：`config_refs` 指向的四套子配置全部继承 A1 母协议，冻结表对应字段包括 best_selector、threshold_source、eval_cast_policy、boundary_metric_width、connected_components_connectivity
- 参数冻结总表是这些字段的唯一正式来源

## 这个文件没说明什么

- 不规定训练超参数（那是 `configs/train/unet_flow_v1.yaml` 的职责）
- 不规定模型架构细节（那在 `configs/model/unet_v1.yaml` 里）
- 不规定数据集路径（那在 `configs/data/glas.yaml` 里）
- 局限性：它只是一次运行的身份卡，本身不产生任何指标

## 如何手工验证这个文件的正确性

下面两个验证步骤按顺序执行，可确认子配置齐全、三 seed 只差 seed。

### 验证步骤 1：确认 config_refs 指向的四个文件都存在
- 操作：逐个查看 `configs/data/glas.yaml`、`configs/model/unet_v1.yaml`、`configs/train/unet_flow_v1.yaml`、`configs/eval/eval_proto_v1.yaml`
- 期望结果：全部存在
- 实际结果：全部存在

### 验证步骤 2：和另外两个配置相比（配置文件名中的 v1 仅表示配置版本），只有 seed、run_name 和 smoke_check_run_name 不同：

```bash
diff <(grep -v train_seed configs/experiment/A2_UNet_GlaS_v1_seed3407.yaml) \
     <(grep -v train_seed configs/experiment/A2_UNet_GlaS_v1_seed1234.yaml)
```

期望结果：除 run_name 与 train_seed 外无差异。实际结果：一致。

## 常见问题

### Q：为什么选 3407、1234、2025 这三个 seed？

A：3407 是深度学习社区常用的"幸运种子"，1234 和 2025 是显式取的不同值，确保三次初始化差异足够显著。它们不是为了挑最优，而是为了测抖动。

### Q：可以在这里直接改 batch_size 或 lr 吗？

A：容易误解。这个文件不放训练超参，改这些要去 `configs/train/unet_flow_v1.yaml`，而且任何改动都必须先过参数冻结总表，否则会破坏三 seed 的协议一致性。

## 建议联读

- `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_train.py.md` — 消费本配置的训练入口
- `reports/stage_reports/implementation_tracking/03_UNet稳定性/configs_eval_eval_proto_v1.yaml.md` — 解引用到的评估协议
- `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_summarize_stage.py.md` — 下游聚合脚本

学完后你应该具备的能力：能说清这个文件如何解引用四套子配置，以及为什么它只允许改 seed。

## 当前消费口径与审计闭环

本文件名中的 `A2_UNet_GlaS_v1_seed3407.yaml` 中 `v1` 仅表示配置文件版本；当前正式 run_name 是 `A2_UNet_GlaS_seed3407`。当前协议为 `eval_proto_v1`，正式身份集合为 seed3407/1234/2025；`protocol_v3` 仅作历史追溯。当前聚合主结果统一来自 `reports/tables/unet_mean_std_summary.csv`：testA/testB Object F1=`0.5290508133298323±0.06534870542228736` / `0.5864995222306099±0.017711580461373767`，Object Dice=`0.7081049877960447±0.0528843478663972` / `0.7755628763239749±0.01214631192503348`，Pixel Dice=`0.8687005312137156±0.014245648618802897` / `0.8785019406751632±0.007950925190263055`，IoU=`0.7802676159056027±0.023159000977374777` / `0.7926352354780709±0.009535961930616718`。A2 numbered stage gate=true、workflow_gate_status=pass、handoff_ready_for_b1=true，不等于 04 自身通过。

直接依赖：A1 配置模板、eval_proto_v1、数据协议；下游：train.py/test.py。冲突裁决：旧 v1 run 身份和旧数字不作为当前 run/结果消费。回退条件：配置身份、协议或 checkpoint 路径不一致时回退 blocked。

## 文件质量自检

- [x] 配置路径版本与正式 run_name 已区分。
- [x] 当前协议、精确结果源和阶段边界已写明。
- [x] 依赖、冲突与回退可回查。

## Diagnostics 闭环

已扫描三 seed 配置说明的身份、协议和结果引用；当前身份与历史版本语境清楚，未发现未标注当前消费残留。

## 审计对表

A1/冻结配置 → 当前配置接口；聚合表 → 当前结果；全目录扫描 → diagnostics；缺口：无。

## 版本更新记录

| 日期 | 改动内容 | 影响范围 | 是否需要重新验证 |
|------|---------|---------|----------------|
| 2026-07-10 | A2 阶段首次创建学习型说明文 | 本文档 | 是 |
| 2026-07-10 | 按学习型说明文门禁补齐结构/解释/误区章节、真实结果、来源锚点与阶段协议回链，清理无法解析的路径锚点 | 本文档 | 是 |
