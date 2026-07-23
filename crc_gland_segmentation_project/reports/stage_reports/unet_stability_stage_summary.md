# UNet Stability Stage Summary (A2)

## Gate Status
- complete_runs: `true`
- proto_consistent: `true`
- raw_results_ready: `true`
- aggregated_results_ready: `true`  # compatibility alias: statistical table ready; not per-run aggregate rows
- evidence_mode: `sample_only`
- per_run_aggregate_rows: `false`
- raw_count: `42`
- meanstd_target_count: `14`
- failure_summary_ready: `true`
- blockers_resolved: `true`
- gate_a2: `true`
- stage_pass_a2: `true`
- handoff_ready_for_b1: `true`

## Blocking Reasons

- none

## Conclusion

A2 stage passed: three formal runs are protocol-consistent; sample-only evidence covers seven metrics with raw=42, mean±std target=14, and error patterns explainable. Aggregate values are derived statistics, not per-run CSV rows.
