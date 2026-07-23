# 04_Baseline 重置状态

- reset_date: `2026-07-14`
- reset_reason: `protocol_v3_archived_and_stage_restarted`
- stage_status: `not_started`
- research_alignment: `not_started`
- stage_definition: `not_started`
- precheck: `not_started`
- runtime: `not_started`
- code_quality: `not_started`
- workflow_gate: `not_started`

上一轮全部 B 类证据位于:
`b_class_auxiliary/coding_guards/04_Baseline/_historical_archive/04_Baseline__historical_20260714_protocol_v3_reset/`

本文件不是 gate report,不能作为任何阶段通过依据。新轮次必须重新生成全部正式门禁文件。

## 当前消费边界

- 允许读取 A2 作为协议/稳定基线来源：`A2_UNet_GlaS_seed3407/1234/2025`、当前 raw=42、mean±std=14 和 A2 限制说明。
- 禁止把 A2 结果、A2 workflow/runtime/code-quality 报告、旧 aggregate、旧 protocol_v3 或共享 `runtime_checks` 文件当作 B1 当前结果或 B1 gate。
- 当前 04 必须建立独立 `source_stage=04_Baseline`、`source_manifest`、`source_protocol_version`、`source_run_name`、`consumer_stage=04_Baseline`、`consumer_file`、`consumption_boundary`。
- 当前唯一允许状态：`stage_status=not_started`；不得由 A2 `handoff_ready_for_b1=true` 推导 04 已通过。
