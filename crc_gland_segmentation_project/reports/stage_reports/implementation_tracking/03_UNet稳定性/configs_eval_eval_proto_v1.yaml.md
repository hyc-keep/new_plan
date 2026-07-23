# configs/eval/eval_proto_v1.yaml 怎么看

> 结论先行：这个文件是 A2 阶段的**评估协议配置**，是三个 seed 评估必须共同遵守的口径基准。
> 你可以把它理解成"评估规则的不可变宪章"——`scripts/test.py` 和 `scripts/summarize_stage.py` 都读同一份，保证三次运行的评估口径不漂移。

## 这个文件是干什么的

这个 YAML 规定了评估链的所有关键口径：二值化阈值、阈值来源、类型转换策略、边界指标算法、连通域实现。

它是 `scripts/summarize_stage.py` 里 `_check_proto_consistency` 的比对基准——三个 run 的评估相关字段必须与这份文件一致，否则不能聚合。

用人话说，它把散在代码里的评估参数收成一份显式配置，让评估口径只有一个来源。

## 这张表/这个文件长什么样

这个文件字段集中在四类：best 选择、threshold、cast policy、boundary 与连通域。

第一类 best 选择回答"用哪个 checkpoint 评估"：best_selector、best_metric_name 决定从训练过程里挑哪一版权重。

第二类 threshold 回答"概率图怎么变二值"：threshold_value、threshold_source 决定阈值取多少、依据来自哪里。

第三类 cast policy 回答"什么时候做类型转换"：eval_cast_policy 决定在阈值比较前做 float32 转换，避免精度漂移。

第四类 boundary 与连通域回答"实例怎么切"：boundary_metric_width、boundary_metric_impl、connected_components_impl、connected_components_connectivity 决定边界带与连通方式。

## 当前真实结果

当前文件的真实字段如下：

```yaml
eval_proto_version: eval_proto_v1
best_selector: val_objdice_max
best_metric_name: val_objdice
threshold_value: 0.5
threshold_source: val17
eval_cast_policy: float32_before_threshold
postprocess_version: none_in_v1
boundary_metric_width: 3
boundary_metric_impl: binary_erosion_xor_plus_binary_dilation
connected_components_impl: scipy.ndimage.label
connected_components_connectivity: 8
```

这些字段在三个 run 的 run_meta 里都能核对到，例如 eval_cast_policy 三 seed 均为 float32_before_threshold、connected_components_connectivity 三 seed 均为 8。

需要强调的是：这份文件本身没有"实验结果"可言——它是评估口径，不是评估产出。它的"真实结果"体现在两个方面：一是文件里的字段取值全部是确定值而非占位符，二是这些取值已经被三个 seed 的 run_meta 逐字段回填并核对通过。

换句话说，这份配置的"真实结果"就是它作为协议基准的有效性已被验证：`scripts/summarize_stage.py` 的 `_check_proto_consistency` 用它比对三个 run，结果是 proto_consistent=true。如果任何一个 seed 的评估口径偏离本文件，这个检查会立即失败。所以本文件的正确性不是靠"看起来对"，而是靠三次独立运行的交叉核对来背书。

## 这些列/字段分别是什么意思

逐字段说明，每个字段都能在配置里核对：

- `eval_proto_version`：评估协议版本号，当前 eval_proto_v1
- `best_selector`：选 best checkpoint 的规则，val_objdice_max（选 val_objdice 最高）
- `best_metric_name`：训练/验证主监控指标 val_objdice
- `threshold_value`：二值化阈值 0.5，取值范围 0.0~1.0
- `threshold_source`：阈值来源 val17，表示在 val17 上确定
- `eval_cast_policy`：阈值比较前的类型转换策略，float32_before_threshold
- `boundary_metric_width`：边界带宽度 3 像素
- `boundary_metric_impl`：边界提取实现 binary_erosion_xor_plus_binary_dilation
- `connected_components_impl`：连通域实现 scipy.ndimage.label
- `connected_components_connectivity`：连通方式 8（含对角线）

## 为什么评估协议要单独成文件

你可能会问：这些参数直接写在 `scripts/test.py` 里不就行了？

因为 A2 的 `_check_proto_consistency` 需要跨三个 run 做对比。如果参数硬编码在代码里，每次检查都要翻代码，而且改了代码没改检查逻辑就会出现"代码与检查不一致"的坑。

单独成文件让 `scripts/test.py` 读它、`scripts/summarize_stage.py` 拿它作为比对基准——评估口径来源唯一。

## 为什么 connectivity 是 8 不是 4

腺体在病理切片里形状不规则，8-connectivity 能更准确地捕获实例；如果腺体内有微小空洞（腺腔常见），8-connectivity 不会把它误判成两个独立实例。

## 阶段协议回链卡片

- 当前阶段总协议: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`
- mean±std 汇总规则: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/02_mean_std汇总规则.md`
- 阶段验收: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/03_阶段验收.md`
- 上一阶段放行文件: `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 正式规则文件: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 评估口径对齐: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`

## 溯源与冻结依据

- 论文依据：Object-level Dice、Hausdorff 等评估指标口径来自 Sirinukunwattana et al., 2017 GlaS Challenge §2.3
- 冻结依据：boundary_metric_width、connected_components_connectivity、eval_cast_policy 均来自参数冻结总表，本文件是它们在 eval 配置链上的落点
- 参考行数与实现：boundary/连通域实现落在 `src/eval/run_eval.py`

## 这个文件没说明什么

- 不规定用哪些指标（metric_list 在 `scripts/test.py` 中定义）
- 不规定可视化导出参数（在 `scripts/test.py` 的 CLI 参数里）
- 不规定训练超参数（那是 `configs/train/unet_flow_v1.yaml` 的职责）
- 局限性：它只冻结口径，不负责指标的具体计算实现

## 如何手工验证这个文件的正确性

下面两个验证步骤按顺序执行，可确认本配置与冻结表、三个 run 的 run_meta 完全一致。

### 验证步骤 1：与冻结表对齐
- 操作：打开 `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`，对照 boundary_metric_width=3、connected_components_connectivity=8、eval_cast_policy=float32_before_threshold
- 期望结果：三字段完全一致
- 实际结果：一致

### 验证步骤 2：与三个 run 的 run_meta 一致
- 操作：查看 `experiments/A2_UNet_GlaS_seed3407/run_meta.yaml` 等三个文件的 eval_cast_policy 字段
- 期望结果：三 seed 均为 float32_before_threshold
- 实际结果：一致

## 常见问题

### Q：threshold_value=0.5 是最优的吗？

A：容易误解。0.5 是二分类默认阈值，且 threshold_source=val17 说明它在 val 集验证过。它是"协议冻结值"，不是"永远最优值"。

### Q：能不能在 04 阶段改这个文件？

A：可以，但必须先更新冻结表、把 eval_proto_version 升到 v2，并承认 04 结果与 03 基线不在同一评估协议下，不可直接对比。

## 建议联读

- `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_test.py.md` — 消费本配置的评估脚本
- `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_summarize_stage.py.md` — 用本配置做协议一致性校验

学完后你应该具备的能力：能说清 A2 评估口径冻结了哪些字段，以及为什么它们必须单独成文件。

## 当前消费边界与审计闭环

当前协议唯一为 `eval_proto_v1`，供 `A2_UNet_GlaS_seed3407`、`A2_UNet_GlaS_seed1234`、`A2_UNet_GlaS_seed2025` 三个正式 run 共用。`protocol_v3` 只作历史追溯，不参与当前汇总或 gate；配置文件名中的旧 v1 仅属路径版本语境。当前 A2 numbered stage gate=true、workflow_gate_status=pass、handoff_ready_for_b1=true，不等于 04 自身通过。

直接依赖：参数冻结表、A2 三次重复设计、GlaS 评估口径与 `scripts/test.py`；代码落点：`scripts/test.py`、`scripts/summarize_stage.py`、`src/eval/run_eval.py`。冲突裁决：任何协议漂移都使当前聚合失效。回退条件：字段不一致时回退 blocked，先恢复 eval_proto_v1 再重评估和聚合。

## 文件质量自检

- [x] 协议字段、正式身份、历史协议边界和下游边界明确。
- [x] 依赖、代码落点、冲突与回退可回查。

## Diagnostics 闭环

已扫描本阶段 Markdown 的协议版本与身份引用；未发现 protocol_v3 被当作当前消费依据。

## 审计对表

冻结规则/文献 → 字段说明；test/summarize → 代码落点；全目录协议扫描 → diagnostics；缺口：无。

## 版本更新记录

| 日期 | 改动内容 | 影响范围 | 是否需要重新验证 |
|------|---------|---------|----------------|
| 2026-07-10 | A2 阶段首次创建学习型说明文 | 本文档 | 是 |
| 2026-07-10 | 按学习型说明文门禁补齐结构/真实结果章节、来源锚点与阶段协议回链，清理无法解析的路径锚点 | 本文档 | 是 |
