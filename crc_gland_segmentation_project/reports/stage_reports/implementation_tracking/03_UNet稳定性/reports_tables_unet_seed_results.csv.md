# reports/tables/unet_seed_results.csv 怎么看

> 结论先行：这个 CSV 是 A2 阶段的**逐 seed 原始结果表**，由三个正式 run 的 sample-only 测试 CSV 按 split×metric 重聚合生成，是三层落盘机制中的汇总层 raw 表。
> 你可以把它理解成"实验的原始账本"——任何人想复算 mean±std，都应该从这张表出发。

## 当前消费身份与协议

本表只收录 `A2_UNet_GlaS_seed3407`、`A2_UNet_GlaS_seed1234`、`A2_UNet_GlaS_seed2025` 三个正式身份，当前协议为 `eval_proto_v1`；`protocol_v3` 不参与当前 raw 或聚合消费。旧的 0.887~0.898 等 F1 描述属于历史错误口径。精确聚合结果必须回看 `unet_mean_std_summary.csv`，不能从单 seed 示例替代主结论。

## 这张表是干什么的

这张表把三个 seed（3407、1234、2025）在两个 split（testA、testB）上的七个指标（F1、Object Dice、Object Hausdorff、Dice、IoU、HD95、Boundary F1）汇成一张 42 行的标准化表格。

它由 `scripts/summarize_stage.py` 生成，是 A2 验收的核心物理证据。

用人话说，不管你后来做什么分析、画什么图，原始数据都在这张表里，不用从中间结果文件回推。

## 这张表/这个文件长什么样

这张表有 24 列、42 个数据行（3 seed × 2 split × 7 metrics），外加 1 个表头行。

### 列结构

| 列名 | 含义 | 示例值 |
|------|------|--------|
| run_name | 运行名 | A2_UNet_GlaS_seed3407 |
| stage | 阶段代号 | A2 |
| dataset | 数据集 | GlaS |
| model_name | 模型名 | unet |
| eval_cast_policy | 评估类型转换策略 | float32_before_threshold |
| boundary_metric_width | 边界指标宽度 | 3 |
| connected_components_connectivity | 连通方式 | 8 |
| seed | 随机种子 | 3407 / 1234 / 2025 |
| split_role | 测试 split | testA / testB |
| metric_name | 指标名 | F1 / Object Dice / ... |
| metric_value | 指标值 | 0.5291 |
| checkpoint_path | best 权重路径 | experiments/.../best.ckpt |
| result_tag | 结果标签 | reproduced |
| aggregation | 聚合模式 | single_seed |

## 当前真实结果

当前表内的真实数据（部分示例）：

| run_name | seed | split | metric | value |
|----------|------|-------|--------|-------|
| A2_UNet_GlaS_seed3407 | 3407 | testA | F1 | 0.4877 |
| A2_UNet_GlaS_seed3407 | 3407 | testB | F1 | 0.5760 |
| A2_UNet_GlaS_seed1234 | 1234 | testA | F1 | 0.6213 |
| A2_UNet_GlaS_seed2025 | 2025 | testA | F1 | 0.4782 |

完整 42 行数据见 `reports/tables/unet_seed_results.csv`。当前三 seed 的聚合 F1 以 `unet_mean_std_summary.csv` 为准：testA `0.5291 ± 0.0653`，testB `0.5865 ± 0.0177`。

## 这些列/字段分别是什么意思

前 13 列（run_name 到 connected_components_connectivity）每行重复，这不是冗余——这是三层落盘的核心要求。

- **eval_cast_policy**：三 seed 全部 float32_before_threshold，评估口径一致
- **boundary_metric_width**：三 seed 全部 3，边界定义一致
- **connected_components_connectivity**：三 seed 全部 8，实例划分规则一致
- **checkpoint_path**：追溯"这个结果由哪个模型权重产生"
- **metric_value**：本行指标的真实数值

用人话说：每一行都是一个自包含的实验记录快照，你不需要翻别的文件就能知道这行结果的评估条件。

## 指标含义速查

| 指标 | 层级 | 含义 |
|------|------|------|
| F1 | object-level | GlaS 官方对象级检测 F1：连通域实例化后按 overlap>0.5（GT 面积归一）匹配，F1=2TP/(2TP+FP+FN)，逐图后再平均 |
| Dice | pixel-level | 像素级 Dice 系数 |
| IoU | pixel-level | 像素级交并比 |
| Object Dice | object-level | 基于连通域的实例级 Dice |
| Object Hausdorff | object-level | 对象级 Hausdorff 距离 |

## 阶段协议回链卡片

- 当前阶段总协议: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`
- mean±std 汇总规则: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/02_mean_std汇总规则.md`
- 阶段验收: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/03_阶段验收.md`
- 正式规则文件: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 命名与结果记录规范: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`

## 溯源与冻结依据

- 论文依据：Object Dice / Object Hausdorff 指标口径来自 Sirinukunwattana et al., 2017 GlaS Challenge §2.3
- 冻结依据：eval_cast_policy、boundary_metric_width、connected_components_connectivity 来自参数冻结总表
- 生成实现：本表由 `scripts/summarize_stage.py` 的 collect_unet_seed_results 产出

## 当前这张表说明了什么

1. 当前三 seed 对象级 F1 的聚合结果为：testA `0.5291 ± 0.0653`、testB `0.5865 ± 0.0177`；这些数值来自当前 `unet_mean_std_summary.csv`，旧的 0.887~0.898 描述属于失效历史口径，不得当前消费
2. 协议一致性成立：所有协议字段三 seed 完全相同，无漂移
3. Object Dice 比 pixel Dice 低约 0.10~0.13，反映 pixel 准确但实例分离不够好

## 这张表没说明什么（局限性）

- 不说明哪个样本特别难（需看 error_cases 或可视化导出）
- 不说明模型在 CRAG 上的表现（那是 04 阶段的目标）
- 不说明训练收敛曲线（需看 run 目录下的 train_log/val_metrics）
- 不说明统计显著性（n=3 只描述内部一致度）

## 如何手工验证这个文件的正确性

下面三个验证步骤按顺序执行，可确认行数正确、协议字段一致、与 per-run CSV 对齐。

### 验证步骤 1：行数检查
- 操作：统计 `reports/tables/unet_seed_results.csv` 的行数
- 期望结果：43 行（1 表头 + 42 数据）
- 实际结果：43 行

### 验证步骤 2：协议字段一致性
- 操作：查看 eval_cast_policy 列的取值分布
- 期望结果：42 行全部为 `float32_before_threshold`
- 实际结果：全部一致

### 验证步骤 3：与 per-run CSV 对齐
- 操作：从 `experiments/A2_UNet_GlaS_seed3407/testA_metrics.csv` 的 60 个 sample 行按指标重聚合，对比本表对应行
- 期望结果：数值一致
- 实际结果：一致；当前测试 CSV 为 sample-only，不存在 aggregate 行；raw seed 表由 sample 行按 split×metric 重聚合生成

## 常见问题

### Q：协议字段每行都一样，是不是可以省掉？

A：容易误解。每行自带协议字段是为了防丢失——某个 seed 的 checkpoint 损坏时，你仍能从 CSV 直接看到当时的评估协议。三层落盘不是为了好看，是为了可审计。

### Q：seed=2025 的 testA F1 最高，是不是该只用它？

A：不对。A2 目标是测稳定性，三 seed 差异应视为噪声，不能挑最优 seed。

## 建议联读

- `reports/stage_reports/implementation_tracking/03_UNet稳定性/reports_tables_unet_mean_std_summary.csv.md` — 由本表聚合的 mean±std 表
- `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_summarize_stage.py.md` — 生成本表的脚本说明文

学完后你应该具备的能力：能说清这张表的 42 行怎么来的，以及为什么协议字段要每行重复。

## 版本更新记录

| 日期 | 改动内容 | 影响范围 | 是否需要重新验证 |
|------|---------|---------|----------------|
| 2026-07-10 | A2 阶段首次创建学习型说明文 | 本文档 | 是 |
| 2026-07-10 | 按学习型说明文门禁补齐结构/字段解释/误区章节、来源锚点与阶段协议回链，清理无法解析的路径锚点 | 本文档 | 是 |
