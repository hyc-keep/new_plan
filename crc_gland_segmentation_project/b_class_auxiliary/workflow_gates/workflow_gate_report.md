# Workflow Gate Routing Report (Not Current 04 Gate)

> `report_scope=shared_route_probe`  
> `valid_for_current_04_gate=false`  
> 本文件只报告 04 专属产物是否存在，不是 04 正式 workflow gate。当前 04 必须读取 `b_class_auxiliary/coding_guards/04_Baseline/workflow_gate_report.md`。

## 0. 兜底入口拒绝规则

本文件不是任何阶段的 pass 证据。未显式指定 `coding_guards/<stage>/` 时，兜底入口只返回缺失/拒绝，不读取 A2 或其他阶段的结果文件。

## 1. 固定执行顺序
- `research_alignment_record` -> `stage_definition_gate` -> `precheck_doc_gate` -> `runtime_check` -> `code_quality_gate` -> `workflow_gate`

## 2. 本轮正式产物要求
- required_artifact: `b_class_auxiliary/coding_guards/04_Baseline/研究定标记录.md`
- required_artifact: `b_class_auxiliary/coding_guards/04_Baseline/research_alignment_gate_report.md`
- required_artifact: `b_class_auxiliary/coding_guards/04_Baseline/00_阶段实现卡.md`
- required_artifact: `b_class_auxiliary/coding_guards/04_Baseline/stage_definition_gate_report.md`
- required_artifact: `b_class_auxiliary/coding_guards/04_Baseline/precheck_doc_gate_report.md`
- required_artifact: `b_class_auxiliary/coding_guards/04_Baseline/workflow_gate_report.md`
- required_artifact: `b_class_auxiliary/coding_guards/04_Baseline/实现依据记录.md`
- required_artifact: `b_class_auxiliary/coding_guards/04_Baseline/runtime_check_report.md`
- required_artifact: `b_class_auxiliary/coding_guards/04_Baseline/runtime_evidence.json`
- required_artifact: `b_class_auxiliary/coding_guards/04_Baseline/runtime_check.log`
- required_artifact: `b_class_auxiliary/coding_guards/04_Baseline/code_quality_gate_report.md`
- missing_artifacts: `b_class_auxiliary/coding_guards/04_Baseline/workflow_gate_report.md`

## 3. 各步结果
### research_alignment_gate
- status: `pass`
- reason: `completed`
- output_path: `/home/featurize/work/Paper/crc_gland_segmentation_project/b_class_auxiliary/coding_guards/04_Baseline/research_alignment_gate_report.md`
- return_code: `0`
- command: `/environment/miniconda3/bin/python /home/featurize/work/Paper/crc_gland_segmentation_project/b_class_auxiliary/tools/check_research_alignment_gate.py --project-root /home/featurize/work/Paper/crc_gland_segmentation_project --research-record b_class_auxiliary/coding_guards/04_Baseline/研究定标记录.md --output b_class_auxiliary/coding_guards/04_Baseline/research_alignment_gate_report.md`

### stage_definition_gate
- status: `pass`
- reason: `completed`
- output_path: `/home/featurize/work/Paper/crc_gland_segmentation_project/b_class_auxiliary/coding_guards/04_Baseline/stage_definition_gate_report.md`
- return_code: `0`
- command: `/environment/miniconda3/bin/python /home/featurize/work/Paper/crc_gland_segmentation_project/b_class_auxiliary/tools/check_stage_definition_gate.py --project-root /home/featurize/work/Paper/crc_gland_segmentation_project --stage-card b_class_auxiliary/coding_guards/04_Baseline/00_阶段实现卡.md --output b_class_auxiliary/coding_guards/04_Baseline/stage_definition_gate_report.md`

### precheck_doc_gate
- status: `pass`
- reason: `completed`
- output_path: `/home/featurize/work/Paper/crc_gland_segmentation_project/b_class_auxiliary/coding_guards/04_Baseline/precheck_doc_gate_report.md`
- return_code: `0`
- command: `/environment/miniconda3/bin/python /home/featurize/work/Paper/crc_gland_segmentation_project/b_class_auxiliary/tools/check_precheck_docs.py --project-root /home/featurize/work/Paper/crc_gland_segmentation_project --precheck-guard b_class_auxiliary/coding_guards/04_Baseline/pre_check_guard.md --output b_class_auxiliary/coding_guards/04_Baseline/precheck_doc_gate_report.md`

### runtime_check
- status: `pass`
- reason: `completed`
- output_path: `/home/featurize/work/Paper/crc_gland_segmentation_project/b_class_auxiliary/coding_guards/04_Baseline/runtime_check_report.md`
- return_code: `0`
- command: `/environment/miniconda3/bin/python /home/featurize/work/Paper/crc_gland_segmentation_project/b_class_auxiliary/tools/run_minimal_runtime_check.py --project-root /home/featurize/work/Paper/crc_gland_segmentation_project --experiment-config configs/experiment/B1_ResNet34_UNet_GlaS_v1_seed3407.yaml --split train --sample-index 0 --output b_class_auxiliary/coding_guards/04_Baseline/runtime_check_report.md --evidence-output b_class_auxiliary/coding_guards/04_Baseline/runtime_evidence.json --log-output b_class_auxiliary/coding_guards/04_Baseline/runtime_check.log --train-runtime-output b_class_auxiliary/coding_guards/04_Baseline/train_runtime_payload.json`

### code_quality_gate
- status: `pass`
- reason: `completed`
- output_path: `/home/featurize/work/Paper/crc_gland_segmentation_project/b_class_auxiliary/coding_guards/04_Baseline/code_quality_gate_report.md`
- return_code: `0`
- command: `/environment/miniconda3/bin/python /home/featurize/work/Paper/crc_gland_segmentation_project/b_class_auxiliary/tools/check_code_quality_gate.py --project-root /home/featurize/work/Paper/crc_gland_segmentation_project --post-qc-guard b_class_auxiliary/coding_guards/04_Baseline/post_qc_guard.md --output b_class_auxiliary/coding_guards/04_Baseline/code_quality_gate_report.md`

## 4. 结论
- workflow_gate_status: `blocked`
- 规则: 任一步不是 `pass`，后续依赖步骤一律 `blocked`，不允许跳步放行。
- 规则: 缺少任何本轮必需正式产物，也不允许宣称“正式任务已通过”。
- 说明: `learning_doc_gate` 与 `formal_doc_gate` 属于后续 `说明文档` 或治理阶段检查，不属于当前 `workflow_gate_report.md` 的前置条件。
