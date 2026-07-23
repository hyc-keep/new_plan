# reports/tables/unet_mean_std_summary.csv 怎么看

> 结论先行：这个 CSV 是 `reports/tables/unet_seed_results.csv` 的**聚合版本**，直接回答"UNet 在 GlaS 上的 mean±std 是多少"。
> 你可以把它理解成"实验的摘要报告"——只想快速知道模型表现，就看这张表。

## 当前消费身份与协议

本表当前只消费 `A2_UNet_GlaS_seed3407`、`A2_UNet_GlaS_seed1234`、`A2_UNet_GlaS_seed2025`，协议为 `eval_proto_v1`。`A2_UNet_GlaS_v1_seed*` 仅是配置路径版本说明，`protocol_v3` 仅作历史追溯。任何旧高 F1 或把 F1 等同 Pixel Dice 的数字都是历史错误口径，不得当前消费。

## 这张表是干什么的

这张表从 42 行逐 seed 结果聚合出 14 行 mean±std 数值，由 `scripts/summarize_stage.py` 生成。

它是 A2 阶段的最终输出数字，也是 04_Baseline 阶段的对比基线。

用人话说，想追溯具体哪个 seed 贡献了哪个数字，回去看 `reports/tables/unet_seed_results.csv`；只想要结论，看这张表就够。

## 这张表/这个文件长什么样

这张表有 18 列、14 个数据行（2 split × 7 metrics），外加 1 个表头行。

### 列结构

| 列名 | 含义 | 示例值 |
|------|------|--------|
| model_name | 模型名 | unet |
| dataset | 数据集 | GlaS |
| split_role | 测试 split | testA / testB |
| metric_name | 指标名 | F1 / Object Dice / ... |
| mean | 均值（population mean） | 0.5290508133298323（testA F1） |
| std | 标准差（population std, n=3） | 0.06534870542228736（testA F1） |
| n_runs | 运行次数 | 3 |
| seeds | 参与种子 | "3407,1234,2025" |
| eval_cast_policy | 评估类型转换策略 | float32_before_threshold |
| connected_components_connectivity | 连通方式 | 8 |
| aggregation | 聚合模式 | mean+-std |

## 当前真实结果

### testA

| Metric | Mean | Std |
|--------|------|-----|
| F1 | 0.5290508133298323 | 0.06534870542228736 |
| Object Dice | 0.7081049877960447 | 0.0528843478663972 |
| Object Hausdorff | 128.84087088652046 | 28.70165961765551 |
| Dice | 0.8687005312137156 | 0.014245648618802897 |
| IoU | 0.7802676159056027 | 0.023159000977374777 |

### testB

| Metric | Mean | Std |
|--------|------|-----|
| F1 | 0.5864995222306099 | 0.017711580461373767 |
| Object Dice | 0.7755628763239749 | 0.01214631192503348 |
| Object Hausdorff | 125.01223638001096 | 10.77443214450205 |
| Dice | 0.8785019406751632 | 0.007950925190263055 |
| IoU | 0.7926352354780709 | 0.009535961930616718 |

## 这些列/字段分别是什么意思

逐字段说明：

- `mean`：三 seed 的算术平均，除以 n=3（population mean）
- `std`：population std（除以 n），描述三 run 的内部离散度
- `n_runs`：3，A2 的硬性要求
- `seeds`："3407,1234,2025"，显式列出参与聚合的种子
- `eval_cast_policy` / `connected_components_connectivity`：协议字段，与 raw 表一致

### std 的解读区间

- **< 0.01**：三 run 高度一致
- **0.01~0.03**：有一定波动，仍可接受
- **> 0.03**：差异较大，需结合协议一致性和训练稳定性判断

当前 testA/testB 的 std 以本节表格为准，不将旧版本的稳定性描述作为当前结论。

## 为什么用 population std 而不是 sample std

n=3 时，sample std（除以 n-1=2）会显著放大波动。当前任务是"描述这三个 run 有多一致"，而不是"从三个 run 推断总体分布"，所以用 population std 更诚实。

## 阶段协议回链卡片

- 当前阶段总协议: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`
- mean±std 汇总规则: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/02_mean_std汇总规则.md`
- 阶段验收: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/03_阶段验收.md`
- 正式规则文件: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 命名与结果记录规范: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`

## 溯源与冻结依据

- 论文依据：mean/std 公式与指标口径对齐 Sirinukunwattana et al., 2017 GlaS Challenge §2.3
- 冻结依据：n_runs=3、seeds 集合、result_tag=reproduced 来自 03 阶段 mean±std 汇总规则
- 生成实现：本表由 `scripts/summarize_stage.py` 的 aggregate_seed_metrics / build_mean_std_summary 产出

## 当前这张表说明了什么

1. 当前主结论必须引用当前汇总 CSV：testA F1=0.5290508133298323±0.06534870542228736，testB F1=0.5864995222306099±0.017711580461373767。
2. 像素级指标为 testA Dice=0.8687005312137156、IoU=0.7802676159056027；testB Dice=0.8785019406751632、IoU=0.7926352354780709。
3. testA Object Dice=0.7081049877960447±0.0528843478663972，testB Object Dice=0.7755628763239749±0.01214631192503348；不能用旧的高 F1 数字替代当前对象级 F1。

## 这张表没说明什么（局限性）

- 不说明这些指标在同类论文中的水平（需自己做文献对比）
- 不说明 CRAG 上的性能（04 阶段目标）
- 不说明 n=3 的 std 是否有统计推断意义

## 如何手工验证这个文件的正确性

下面三个验证步骤按顺序执行，可确认行数正确、mean 可复算、种子列表完整。

### 验证步骤 1：行数检查
- 操作：统计 `reports/tables/unet_mean_std_summary.csv` 的行数
- 期望结果：15 行（1 表头 + 14 数据）
- 实际结果：15 行

### 验证步骤 2：手动复算 testA F1 mean
- 操作：从 `reports/tables/unet_seed_results.csv` 取当前 testA F1 三行（0.48767052693586427、0.6213051506047086、0.4781767624489242），计算三者均值
- 期望结果：0.5290508133298323
- 实际结果：0.5290508133298323

### 验证步骤 3：种子列表完整
- 操作：查看 seeds 列
- 期望结果："3407,1234,2025"
- 实际结果：一致

## 常见问题

### Q：F1 和 Dice 是不是一回事？

A：**不是。** 本项目主表 F1 是 GlaS 官方**对象级检测 F1**（连通域实例化后按 overlap>0.5、GT 面积归一做对象匹配，F1=2TP/(2TP+FP+FN)，逐图后平均），Dice 是**像素级**系数。当前汇总中 testA F1=0.5290508133298323、Dice=0.8687005312137156；testB F1=0.5864995222306099、Dice=0.8785019406751632。
> 历史订正（20260711）：此前版本曾把 F1 误实现成像素 Dice，导致两列逐位相等，并错误解释为"二值分割数学恒等式"。该结论已被推翻，代码与结果均已按官方口径重算，详见 `实现依据记录.md` 第 13 节。

### Q：Object Hausdorff 114 算高还是低？

A：对病理图像分割来说 100+ 偏高，说明部分样本完全漏掉某些腺体。这在 UNet baseline 上是预期的——对象级精确分割需要额外的实例分割头或后处理。这也是容易误解的点：不要因此判定模型崩溃。

## 建议联读

- `reports/stage_reports/implementation_tracking/03_UNet稳定性/reports_tables_unet_seed_results.csv.md` — 本表的原始数据来源
- `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_summarize_stage.py.md` — 生成本表的聚合逻辑说明文

学完后你应该具备的能力：能说清 mean±std 怎么从 42 行 raw 聚合出来，以及为什么用 population std。

## 版本更新记录

| 日期 | 改动内容 | 影响范围 | 是否需要重新验证 |
|------|---------|---------|----------------|
| 2026-07-10 | A2 阶段首次创建学习型说明文 | 本文档 | 是 |
| 2026-07-10 | 按学习型说明文门禁补齐结构/字段解释/误区章节、来源锚点与阶段协议回链，清理无法解析的路径锚点 | 本文档 | 是 |
