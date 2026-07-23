# 04_Baseline 当前状态

- 阶段: `04_Baseline`
- 当前正式结果轮次: `fresh_current_round / current_standard`
- implementation_tracking: `partial`
- 正式训练: `已完成（3 个 seed）`
- 正式测试: `已完成（TestA=60、TestB=20；3 个 seed）`
- 独立 PNG+GT 指标复核: `pass（3/3 seed，TestA/TestB mismatch_count=0）`
- 当前编号阶段 Gate: `blocked`（原始 Gate 保持真实裁决）
- 当前科学解释状态: `valid_with_stability_warning`
- `stability_warning`: `true`（仅 TestB:Object Dice 的三 seed std 略高于 A2）
- 条件性后续研究: `允许，但不等同于 formal handoff；必须沿用当前 B1 三 seed、协议和 raw 结果`
- 当前 workflow gate: `需在新服务器上重新生成，旧报告为 CUDA 不可用时的过期证据`
- 当前可执行结论: `不需要因服务器更换重训；先重跑当前轮 gate/汇总一致性检查`

## 当前正式资产

当前 `experiments/` 下的正式 B1 资产仍然存在，不是 runtime probe 或 smoke：

- `experiments/B1_ResNet34_UNet_GlaS_seed3407/`
- `experiments/B1_ResNet34_UNet_GlaS_seed1234/`
- `experiments/B1_ResNet34_UNet_GlaS_seed2025/`

每个正式 run 已发现 `best.ckpt`、`last.ckpt`、`run_meta.yaml`、`train_log.csv`、`val_metrics.csv`、`testA_metrics.csv` 和 `testB_metrics.csv`。三份独立复核记录分别为：

- `notes/independent_metric_check_B1_ResNet34_UNet_GlaS_seed3407_current_standard.json`
- `notes/independent_metric_check_B1_ResNet34_UNet_GlaS_seed1234_current_standard.json`
- `notes/independent_metric_check_B1_ResNet34_UNet_GlaS_seed2025_current_standard.json`

## 当前科学判定

当前正式结果可以作为 `current_standard` 轮次的真实实验资产继续审查和汇总。独立复核已确认三 seed 的 TestA/TestB 预测与 GT 重新计算结果与正式 CSV 一致；这证明结果在“预测资产—GT—指标 CSV”链上可复核，但不自动等于阶段 Gate 通过。

当前阶段汇总显示：主指标方向不差、协议和资产齐全，但 `TestB:Object Dice` 的三 seed 波动超过 A2 对照，因此 `gate_b1_compare=false`、`stage_pass_b1=false`。该结果应记录为“B1 稳定性门未通过”，不能表述为“B1 结果错误”或“已经证明模型不科学”。

## 轮次边界

旧 `protocol_v3`、B1 v2、A2 历史轮次和 runtime probe 继续保留为历史/辅助证据，不与 `current_standard` 当前正式结果混合。2026-07-14 的 `fresh_reset_20260714` 状态记录反映的是当时的治理重置状态，不再代表当前正式资产不存在；本文件以当前磁盘上的真实资产和当前轮证据为准。

## 后续执行边界

1. 不重训当前 B1；不修改任何 metrics CSV、checkpoint、seed 或历史数字。
2. 保留 `stage_pass_b1=false`、`handoff_ready_for_c1=false`；原始 Gate 仍按冻结规则裁决。
3. 允许开展条件性研究执行、后续阶段协议准备、论文证据整理和探索性下游实验，但必须沿用当前 B1 的三个 seed、split、训练/评估协议、阈值、raw 结果和 `stability_warning=true`。
4. 条件性后续结果只能表述为“相对于当前 B1 对照的变化”，不能表述为“相对于稳定性完全通过的正式 handoff 基座的改进”。
5. 若后续模块增益接近 B1 的 seed 波动，或不同 seed 方向不一致，停止下游主线，回退 04 做单因素稳定性迭代。
6. 若后续要严格满足原始 Gate，必须先归档当前 B1，再建立新契约、标准 run_name 和全新的三 seed 正式运行；不得覆盖当前结果。
