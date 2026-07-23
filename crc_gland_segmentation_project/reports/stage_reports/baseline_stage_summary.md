# Baseline Stage Summary (B1 ResNet34-U-Net)

## Gate Status
- complete_runs: `true`
- proto_consistent: `true`
- fair_compare: `true`
- standard_identity_ok: `false`
- aggregate_ready: `true`
- main_metrics_not_worse: `true`
- stability_not_weaker: `false`
- qualitative_support_ready: `true`
- baseline_assets_ready: `true`
- freeze_ready: `true`
- gate_b1_compare: `false`
- handoff_ready: `true`
- abnormal_runs_resolved: `true`
- gate_b1: `false`
- stage_pass_b1: `false`
- handoff_ready_for_c1: `false`

## B1 (ResNet34-U-Net) Mean+-Std Summary

### testA
- F1: 0.7602 +/- 0.0331
- Object Dice: 0.8565 +/- 0.0182
- Object Hausdorff: 60.0451 +/- 7.8454
- Dice: 0.9230 +/- 0.0050
- IoU: 0.8631 +/- 0.0070
- HD95: 30.3610 +/- 0.7182
- Boundary F1: 0.7775 +/- 0.0120

### testB
- F1: 0.6532 +/- 0.0563
- Object Dice: 0.8136 +/- 0.0112
- Object Hausdorff: 104.9571 +/- 8.3096
- Dice: 0.9128 +/- 0.0055
- IoU: 0.8468 +/- 0.0092
- HD95: 29.3245 +/- 1.9123
- Boundary F1: 0.6979 +/- 0.0174

## Blocking Reasons

- current_identity_failed fields={config_version=['baseline_stability_v3_encoder_bn_policy'], train_proto_version=['train_proto_v3_encoder_bn_policy'], eval_proto_version=['eval_proto_v1'], bn_policy_version=['bn_policy_v3_encoder_running_stats_frozen', 'bn_policy_v3_noop_identity']}
- stability_not_weaker_failed reasons=['testA:F1:0.033110>0.022197+1.000e-12:fail', 'testA:Object Dice:0.018219>0.006711+1.000e-12:fail', 'testB:F1:0.056251>0.021527+1.000e-12:fail', 'testB:Object Hausdorff:8.309643>7.102623+7.103e-12:fail']

## Conclusion

B1 stage blocked: prerequisites for 05_LKMA are not yet met. Resolve the listed comparison, stability, or asset blockers before handoff.
