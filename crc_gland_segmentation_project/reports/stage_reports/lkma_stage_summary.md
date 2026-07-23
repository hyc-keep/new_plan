# LKMA C1 Stage Summary

- current_numbered_stage: `05_LKMA / C1`
- workflow_stage: `post_run_closeout`
- formal_runs_complete: `true`
- independent_metric_check: `pass`
- raw_results_ready: `true`
- meanstd_export_ready: `true`
- lkma_compare_ready: `true`
- lkma_assets_ready: `true`
- decision_level: `drop`
- decision_reason: `Object-level gains are split- and seed-dependent; the formal three-seed evidence does not establish stable cross-split benefit.`
- next_stage_start_model: `baseline`
- visual_support: `available_per_seed_testA_testB_visual_assets; no_manual_quality_score`
- cost_assessment: `params_m_recorded; flops_and_latency_not_measured`
- source_stage: `B1`
- source_manifest: `reports/stage_reports/asset_manifest.json`
- source_protocol_version: `current_standard`
- source_run_name: `B1_ResNet34_UNet_GlaS_seed3407`
- consumer_stage: `C1`
- consumer_file: `reports/tables/lkma_per_seed_summary.csv`
- consumption_boundary: `frozen_baseline_with_warning`
- gate_c1: `blocked`
- handoff_ready: `false`
- gate_blocker: `formal_workflow_gate_and_learning_doc_gate_not_yet_run`

## Raw and Derived Assets

- `reports/tables/lkma_per_seed_summary.csv`
- `reports/tables/baseline_vs_lkma_mean_std.csv`
- `reports/tables/lkma_cost_comparison.csv`
- `reports/tables/lkma_stage_manifest.csv`
- independent PNG/GT checks: three seeds, TestA/TestB, 0 mismatches

## Decision Boundary

The derived comparison records `drop` for C1. This is a model-selection decision, not a claim that the underlying experiment or metrics are invalid. The B1 stability warning remains inherited and unchanged.
