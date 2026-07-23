# 04_Baseline 阅读入口

## 当前状态

- 当前阶段: `04_Baseline`
- 当前正式结果轮次: `fresh_current_round / current_standard`
- 正式训练与测试: `已完成，三 seed；TestA=60、TestB=20`
- 独立 PNG+GT 指标复核: `pass，三 seed 的 TestA/TestB mismatch_count=0`
- 当前编号阶段 Gate: `blocked`，原因是 `TestB:Object Dice` 稳定性门未通过
- 当前科学解释状态: `valid_with_stability_warning`
- `stability_warning=true` 仅表示该项三 seed std 略高于 A2，不等于 B1 结果作废或模型不可用
- 条件性后续研究: `允许`，但不等同于正式 handoff；后续必须沿用当前 B1 三 seed、协议、raw 结果和 warning
- 当前 workflow gate: `需在新服务器基于已通过 runtime/code-quality 重新生成；不得沿用 CUDA 不可用时的旧报告`
- 服务器更换处理: `不需要重训；只需重新生成流程证据并继续科学性审查`

上一轮 protocol_v3、B1 v2、A2 历史结果和 2026-07-14 的治理重置记录仍保留为历史/辅助边界，不能与 `current_standard` 当前正式结果混合。

## 历史归档

- `reports/stage_reports/implementation_tracking/_historical_archive/04_Baseline__historical_20260714_protocol_v3_reset/`
- `experiments/_historical_archive/04_Baseline__historical_20260714_protocol_v3_reset/`
- `reports/tables/_historical_archive/04_Baseline__historical_20260714_protocol_v3_reset/`
- `configs/experiment/_historical_archive/04_Baseline__historical_20260714_protocol_v3_reset/`
- `configs/eval/_historical_archive/04_Baseline__historical_20260714_protocol_v3_reset/`
- `b_class_auxiliary/coding_guards/04_Baseline/_historical_archive/04_Baseline__historical_20260714_protocol_v3_reset/`
- `b_class_auxiliary/source_snapshots/04_Baseline/_historical_archive/04_Baseline__historical_20260714_protocol_v3_reset/`

## 当前执行边界

本轮必须重新读取并执行 `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/` 下的原计划文件。原计划命名优先；正式 run、配置、结果和 gate 必须在本轮重新生成。历史归档只用于 lineage 追溯，不得作为当前轮证据。
