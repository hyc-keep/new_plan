# Active Plan Repair Manifest

- `repair_batch`: `20260719_upstream_active_plan_closeout`
- `active_route`: `journal`
- `active_plan_root`: `/home/featurize/work/Paper/结直肠腺体分割_plan_学报投稿版`
- `active_project_root`: `/home/featurize/work/Paper/crc_gland_segmentation_project_journal`
- `previous_snapshot_unavailable_due_prior_rewrite`: `true`
- `snapshot_truthfulness`: 本轮开始时 00_总览与规范/00-07 与 02_路线与投稿/01-06 已被先前重写覆盖，无法取得本轮重写前原文；不得复制当前稿冒充旧稿。
- `existing_20260719_archive_status`: `repair_round_preservation_copy_not_verified_previous`
- `existing_readonly_manifest`: `_historical_archive/20260719_scientific_plan_repair/archive_manifest.md`
- `nearest_verified_historical_batches`: `_historical_archive/20260718_full_repair_v2/`, `_historical_archive/20260718_governance_rebuild/active_plan/`
- `historical_consumption`: `historical_provenance_only`
- `current_gate_eligible`: `false`

## Target Snapshot Audit

| target group | 20260719 preservation copies | previous snapshot available | audit conclusion |
|---|---:|---:|---|
| `01_实验执行/00_总览与规范/00-04` | exists | false | prior rewrite already applied; copies do not prove pre-rewrite state |
| `01_实验执行/00_总览与规范/05` | exists; byte-identical to current at audit start | false | cannot certify as previous snapshot |
| `01_实验执行/00_总览与规范/06` | absent | false | no 20260719 snapshot |
| `01_实验执行/00_总览与规范/07` | exists; byte-identical to current at audit start | false | cannot certify as previous snapshot |
| `02_路线与投稿/01` | exists; byte-identical to current at audit start | false | cannot certify as previous snapshot |
| `02_路线与投稿/02,05,06` | exists | false | prior rewrite already applied; copies do not prove pre-rewrite state |
| `02_路线与投稿/03,04` | absent | false | no 20260719 snapshot |

## Lineage

- `source_stage`: `upstream_active_plan_repair`
- `source_manifest`: `archive_manifest.md`
- `source_protocol_version`: `standard_md_rewrite_active_repair_v1`
- `source_run_name`: `not_applicable_document_repair`
- `consumer_stage`: `research_alignment_then_stage_lock`
- `consumer_file`: `02_路线与投稿/05_研究定标记录.md`
- `consumption_boundary`: `provenance_only; not_current_gate; no_experiment_result_mutation`

## Prohibitions

- 不得把 20260719 preservation copy 声称为可验证的 pre-rewrite snapshot。
- 不得用本 manifest 或历史归档生成 current Gate、research pass、stage pass 或实验结论。
- 不得修改历史工程、历史结果或 `新计划全面修缮记录.md`。
