# LKMA Decision Note

- stage: `C1`
- decision_level: `drop`
- decision_reason: `Object-level gains are split- and seed-dependent; the formal three-seed evidence does not establish stable cross-split benefit.`
- next_stage_start_model: `baseline`
- visual_support: `available_per_seed_testA_testB_visual_assets; no_manual_quality_score`
- cost_assessment: `params_m_recorded; flops_and_latency_not_measured`
- independent_metric_check: `pass`
- baseline_status_consumed: `valid_with_stability_warning`
- original_gate_b1: `false`
- source_manifest: `reports/stage_reports/asset_manifest.json`
- consumption_boundary: `frozen_baseline_with_warning`

## Evidence Order

1. Object Dice
2. Object Hausdorff
3. F1
4. Per-seed and per-split consistency
5. Visual assets
6. Parameter-count cost record

The numerical conclusion is generated from the raw per-sample CSVs and independently checked prediction/GT assets. No raw result file was edited.
