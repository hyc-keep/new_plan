# Historical Baseline Stage Summary (B1 ResNet34-U-Net)

> `historical_archive_only=true`  
> `valid_for_current_gate=false`  
> `protocol_identity=protocol_v3`  
> `gate_b1_compare` 或 `handoff_ready` 单字段不得推断当前 B1 通过；当前 04 只消费专属 current gate、manifest 和 checkpoint identity。

## Gate Status
- complete_runs: `true`
- proto_consistent: `true`
- fair_compare: `true`
- v3_identity_ok: `true`
- aggregate_ready: `true`
- main_metrics_not_worse: `true`
- stability_not_weaker: `true`
- qualitative_support_ready: `true`
- baseline_assets_ready: `true`
- freeze_ready: `false`
- gate_b1_compare: `true`
- handoff_ready: `true`
- abnormal_runs_resolved: `true`
- gate_b1: `false`
- stage_pass_b1: `false`
- handoff_ready_for_c1: `false`

## B1 (ResNet34-U-Net) Mean+-Std Summary

### testA
- F1: 0.7411 +/- 0.0221
- Object Dice: 0.8299 +/- 0.0233
- Object Hausdorff: 72.8044 +/- 10.5360
- Dice: 0.9101 +/- 0.0098
- IoU: 0.8450 +/- 0.0134
- HD95: 33.0119 +/- 2.2982
- Boundary F1: 0.7544 +/- 0.0192

### testB
- F1: 0.7029 +/- 0.0170
- Object Dice: 0.8324 +/- 0.0004
- Object Hausdorff: 95.3279 +/- 3.9155
- Dice: 0.9172 +/- 0.0028
- IoU: 0.8554 +/- 0.0046
- HD95: 27.9321 +/- 0.6348
- Boundary F1: 0.7054 +/- 0.0018

## Blocking Reasons

- checkpoint_identity_failed seeds=[3407, 1234, 2025]
- a2_checkpoint_identity_failed seeds=[3407, 1234, 2025]
- freeze_ready_failed mismatches=[]

## Conclusion

B1 stage blocked: prerequisites for 05_LKMA are not yet met. Resolve the listed comparison, stability, or asset blockers before handoff.
