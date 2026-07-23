# Boundary Decision Note

## 1. Decision Identity
- stage: `06_Boundary`
- decision_level: `backup`
- decision_status: `formal_stage_decision`
- current_base_next: `boundary_input_base`
- source_stage: `B1`
- source_manifest: `reports/tables/baseline_stage_manifest.csv`
- source_protocol_version: `eval_proto_v1`
- source_run_name: `B1_ResNet34_UNet_GlaS_seed3407`
- consumer_stage: `07_Distance`
- consumer_file: `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/00_阶段总协议.md`
- consumption_boundary: `Boundary is not admitted as default mainline input; retain as backup candidate only`

## 2. Evidence Completeness
- 三个正式 seed: pass
- TestA60/TestB20 raw CSV: pass
- checkpoint identity: pass
- metric crosscheck: pass
- boundary mean/std: pass
- B1 comparison: pass
- parameter cost: pass (`+2,337` parameters; `+0.009563%`)
- visuals inventory: pass（资产存在，但尚未人工标注成功/失败语义）
- flops/latency: not_measured
- decision evidence sufficient for keep: fail

## 3. Scientific Evidence

### Positive
- TestA mean: F1 `+0.022273`、Object Dice `+0.001867`、Dice `+0.003550`、IoU `+0.004631`、HD95 `-0.322647`、Boundary F1 `+0.004270`。
- TestB mean: F1 `+0.041081`、Object Dice `+0.012829`、Object Hausdorff `-2.766733`、Dice `+0.006922`、IoU `+0.010247`、Boundary F1 `+0.005040`。
- Boundary F1 三 seed mean 均高于 B1，说明固定协议下存在方向性收益信号。

### Conflicts / Risks
- TestA Object Hausdorff 变差 `+2.050143`。
- TestB HD95 变差 `+1.610187`。
- TestA Object Dice 在 seed2025 下降 `-0.008375`。
- TestB F1/Boundary F1 在 seed2025 分别下降 `-0.009185`、`-0.007076`。
- TestA/TestB 的距离指标方向不一致，不能宣称全面形状改善。
- visuals 只有资产清单，尚未形成独立成功/失败案例标签；不能把图片存在本身当成 keep 证据。

## 4. Decision Rule Application
- `keep`: rejected。原因：正式均值存在距离指标冲突，逐 seed 存在材料性退化，案例解释尚未完成。
- `drop`: rejected。原因：Boundary F1、F1、Object Dice 等核心指标存在跨 split 正向均值，且参数增量极小；不能据此宣称无价值。
- `backup`: accepted。原因：存在可复现的方向性收益，但不足以成为 07 的默认主线输入。

## 5. Rollback / Handoff
- 不回退代码、数据、训练 checkpoint 或原始结果。
- 不继续扩展 Boundary width/lambda/loss 搜索。
- 07_Distance 默认起点: `boundary_input_base`。
- Boundary 资产保留为 backup candidate，后续如需比较必须显式引用 D1 三 seed manifest 和本 decision note。
- 下游必须继承：`eval_cast_policy=float32_before_threshold`、`boundary_metric_width=3`、`boundary_metric_impl=binary_erosion_xor_plus_binary_dilation`、`connected_components_impl=scipy.ndimage.label`、`connected_components_connectivity=8`。

## 6. Decision Conclusion
- Formal decision: `backup`
- Scientific wording: BoundaryHead 在固定三 seed、TestA/TestB 和同一评估口径下显示跨 split 的正向平均趋势，但存在 TestA Object Hausdorff、TestB HD95 以及单 seed 退化冲突，故保留为备选模块，不进入默认主线。
- This decision is not a claim that Boundary universally improves segmentation or shape quality.
