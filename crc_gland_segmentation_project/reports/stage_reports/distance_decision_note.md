# 07_Distance decision note

decision_status=pass
decision_level=drop
seed_support_count=3
mean_table_direction=TestA mixed-to-negative; TestB mixed, with Boundary F1 positive but HD95 positive
split_consistency=not_consistent
material_object_regression=TestA Object Dice and Object F1 both decrease; TestB both increase
main_version_priority_pass=false
cost_assessment=training_cost_increased; inference_time=BLOCKED; gpu_memory=BLOCKED
rollback_target=current_base boundary_input_base
current_mainline=boundary_input_base

本次正式阶段决策已完成：`Distance-aware Loss v1` 裁决为 `drop`。`drop` 不是训练无效，也不是指标或实验结果作废，而是基于固定三 seed、TestA/TestB 分开汇总、有限人工视觉证据和成本证据，判定该增强不进入当前主线。保留 D2 作为历史/补充实验资产；不修改任何 train_log、test metrics CSV、run_meta、checkpoint、predictions、聚合数值或 `run_meta` 的 `result_tag`。本文件不宣称进入 `08_外部对比`，也不更新任何下游阶段为已开始。

## 正式证据顺序与裁决

### 1. Boundary F1

- TestA：mean delta（Distance - current base）=`-0.005218`（原始值 `-0.005217955909691541`），3 个 seed 支持。
- TestB：mean delta（Distance - current base）=`+0.003046`（原始值 `+0.0030463798481454862`），3 个 seed 支持。
- 解释：两个 split 方向相反，不能形成跨 split 的稳定边界收益；`mean_table_direction` 因此不支持主线保留。

### 2. HD95 / Object Hausdorff

- TestA：HD95 delta=`+1.411279`（原始值 `+1.4112785187032415`），Object Hausdorff delta=`+7.863698`（原始值 `+7.863698053157421`）。距离指标上升代表误差变差。
- TestB：HD95 delta=`+2.143711`（原始值 `+2.143711039225259`），Object Hausdorff delta=`-6.942631`（原始值 `-6.942631416413462`）。
- 解释：HD95 在两个 split 均上升；Object Hausdorff 仅 TestB 下降而 TestA 明显上升，几何证据不稳定，不能通过 `main_version_priority_pass`。

### 3. visual

有限人工抽查 4 张真实 overlay，范围不是全量视觉复核，但四张均暴露风险：

- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_13_overlay.png`：边界偏移、前景覆盖、局部边缘残留。
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_12_overlay.png`：多目标/狭窄结构中的局部轮廓不稳定。
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_10_overlay.png`：欠分割或轮廓不匹配。
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_14_overlay.png`：边界偏移与前景覆盖。

这些有限案例不支持 Distance 的稳定视觉改善，并暴露边界偏移、前景覆盖、欠分割和局部不稳定；不将有限抽查外推为全量结论。

### 4. Object Dice / F1

- TestA：Object Dice delta=`-0.009519`（原始值 `-0.0095182296500409`）；Object F1 delta=`-0.004469`（原始值 `-0.004468724394355528`）。两者均下降，构成 material object regression。
- TestB：Object Dice delta=`+0.010059`（原始值 `+0.010058590562398328`）；Object F1 delta=`+0.034746`（原始值 `+0.03474567410598517`）。两者均上升。
- 解释：TestA 与 TestB 直接反向，且 TestA 的对象级主指标同步退化；这不满足 keep 所需的跨 split、一致对象级支持。

### 5. cost

- 训练成本增加：三个 seed 的 `train_time_delta_distance_minus_baseline_sec` 分别为 `534.7412`、`283.7485`、`531.5338`，成本表原始记录保持不变。
- 推理时间：`BLOCKED`。
- GPU 显存：`BLOCKED`。
- 解释：在推理时间和显存仍 BLOCKED 的情况下，已有训练成本增加没有获得稳定的边界、几何或对象级收益，因此 `cost_assessment` 不支持主线保留。

## 正式裁决理由

依据 07_Distance 固定顺序 `Boundary F1 -> HD95/Object Hausdorff -> visual -> Object Dice/F1 -> cost`：

1. Boundary F1 在 TestA 下降、TestB 上升，split 方向不一致。
2. HD95 在两个 split 均上升；Object Hausdorff 一降一升，几何证据不一致。
3. 四张有限人工抽查均暴露边界偏移、前景覆盖、欠分割或局部不稳定，未支持稳定改善。
4. Object Dice/F1 在 TestA 同步下降、TestB 同步上升，存在 TestA material object regression。
5. 训练成本增加，推理时间和显存仍 `BLOCKED`，代价缺少稳定收益支撑。

因此，`main_version_priority_pass=false`，正式 `decision_level=drop`。这不是“训练无效”结论，而是“不把该增强带入当前主线”的模型选择结论。

## 资产保留与下游边界

- D2 `Distance` 结果保留为历史/补充实验资产，只读使用，不删除、不改写、不重命名真实结果资产。
- `rollback_target=current_base boundary_input_base`。
- `current_mainline=boundary_input_base`；下游如未来具备独立启动条件，只能消费该 current mainline，不得默认继承 Distance。
- 当前仅完成 07_Distance 的正式决策记录；不声称 `08_外部对比` 或任何更下游阶段已开始，不更新下游阶段状态。
- 项目未发现专门的 07_Distance 当前 handoff Markdown 状态文件；现有阶段表/聚合 CSV 属于结果或机器资产，本轮不修改。

## 回退条件

如发现本决策与原始证据、固定字段或阶段交接语义不一致，回退到本文件重新核对：

- 不得把 `drop` 改写成训练无效或结果作废。
- 不得把 D2 结果移入当前主线，不得把 `Distance` 作为 `08` 的默认输入。
- 不得用未记录的推理时间、显存、额外 seed、额外 lambda 或新聚合数值补强或削弱本次结论。
- 不得修改 train_log、test metrics CSV、run_meta、checkpoint、predictions 或聚合数值。
- 若下游消费边界发生变化，必须先更新明确属于 07_Distance 的正式 handoff 文档，并保持 `current_mainline=boundary_input_base`；不得更新下游阶段为已开始。

## 本轮读取与证据回链

- `/home/featurize/work/Paper/crc_gland_segmentation_project/reports/stage_reports/distance_decision_note.md`：本正式裁决文件，保留原始 delta 并补齐状态、量化方向、主版本门、成本、回退和主线字段。
- `/home/featurize/work/Paper/crc_gland_segmentation_project/reports/stage_reports/distance_visual_casebook.md`：四张有限人工抽查的真实视觉风险证据。
- `/home/featurize/work/Paper/crc_gland_segmentation_project/reports/tables/current_base_vs_distance_mean_std.csv`：三 seed、TestA/TestB 的 mean/std 与原始 delta。
- `/home/featurize/work/Paper/crc_gland_segmentation_project/reports/tables/distance_cost_comparison.csv`：训练成本、推理时间和显存状态。
- `/home/featurize/work/Paper/结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/04_保留或降级标准.md`：固定证据顺序、主版本优先门、drop 条件和 `current_mainline` 绑定规则。
- `/home/featurize/work/Paper/crc_gland_segmentation_project/reports/stage_reports/implementation_tracking/07_Distance/实现依据记录.md`、`/home/featurize/work/Paper/crc_gland_segmentation_project/b_class_auxiliary/coding_guards/07_Distance/stage_gate_check.md`、`/home/featurize/work/Paper/crc_gland_segmentation_project/b_class_auxiliary/coding_guards/07_Distance/Post-QC Guard.md`：确认 07_Distance 资产身份、`boundary_input_base` 输入边界和历史结果只读边界。

## 文件质量自检

- [x] 已按要求先读取决策 note、visual casebook、mean/std 表、cost 表和 07_Distance 保留/降级标准。
- [x] 保留了原始 delta，并将展示值四舍五入到用户指定精度，同时在括号中保留完整原始值。
- [x] 已按固定证据顺序解释 Boundary F1、HD95/Object Hausdorff、visual、Object Dice/F1、cost。
- [x] 已明确 TestA/TestB 方向不一致、TestA 对象级回归、四张有限视觉抽查风险和成本阻断。
- [x] 已新增 `seed_support_count`、`mean_table_direction`、`split_consistency`、`material_object_regression`、`main_version_priority_pass`、`cost_assessment`、`rollback_target`、`current_mainline`。
- [x] 已明确 `drop` 是不进入当前主线，不是训练无效；D2 保留为历史/补充实验资产。
- [x] 已明确 `rollback_target=current_base boundary_input_base`、`current_mainline=boundary_input_base`。
- [x] 未声称进入 08，未更新下游阶段为已开始，未修改 `run_meta` 的 `result_tag`。
- [x] 未编辑任何实验结果文件、聚合数值或运行资产；本轮只编辑本正式决策 Markdown。

## Diagnostics 闭环

- 已回读本文件最终落盘内容，确认顶部状态、证据顺序、裁决理由、资产保留、回退条件和下游边界均存在。
- 将运行 IDE diagnostics，并在验证中检查本文件无新增 markdown 诊断问题。
