# Stage Gate Check

## 1. 阶段信息
- 当前阶段: `04_Baseline`
- 上一阶段: `03_UNet稳定性`
- 当前任务: `04_Baseline_Pre-check`

## 2. 上一阶段通过证据
- 通过文件: `reports/stage_reports/unet_stability_stage_summary.md`、`reports/tables/unet_stage_manifest.csv`、`b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/workflow_gate_report.md`、`b_class_auxiliary/coding_guards/20260708_03_unet_stability_stage_lock/code_quality_gate_report.md`
- 通过状态: A2 阶段总结记录 complete_runs=true、proto_consistent=true、raw_results_ready=true、aggregated_results_ready=true、failure_summary_ready=true、blockers_resolved=true、gate_a2=true、handoff_ready_for_b1=true；上游 workflow/code quality 为 pass。
- 关键交付物: A2 三正式 run、raw=42、mean+-std=14、当前 eval_proto_v1、A2 handoff manifest。

## 3. 当前阶段进入条件

| 条件 | 证据文件 | 检查方法 | 结果 |
|------|---------|---------|------|
| 阶段实现卡已存在且写清唯一目标 | `b_class_auxiliary/coding_guards/04_Baseline/00_阶段实现卡.md` | 检查唯一目标、允许/禁止边界和未决问题章节 | pass |
| 阶段锁定门禁已通过 | `b_class_auxiliary/coding_guards/04_Baseline/stage_definition_gate_report.md` | 检查 `stage_definition_gate_status=pass` | pass |
| 上一阶段正式通过 | `reports/stage_reports/unet_stability_stage_summary.md` | 检查 Gate_A2、handoff_ready_for_b1、A2 三 run 和 42/14 资产 | pass |
| 当前阶段需要的上游资产可回链 | `reports/tables/unet_stage_manifest.csv` | 检查 source protocol、consumer_stage、run identities 和资产路径；历史 protocol_v3 不消费 | pass |
| 当前任务没有越界到后续阶段 | `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md` | 对照唯一变量和禁止 LKMA/Boundary/Distance/TTA/额外后处理 | pass |
| 当前轮 B1 代码、权重和 experiment identity 已冻结 | `b_class_auxiliary/coding_guards/04_Baseline/current_codebase_状态.md` | 检查当前代码、候选代码 freshness、权重来源与缓存 SHA256、离线策略、B1 experiment config、三 seed run mapping 和 eval/postprocess version | fail |

## 4. 阻断项

| 阻断项 | 是否触发 | 说明 |
|-------|---------|------|
| `00_阶段实现卡.md` 缺失或仍是空壳 | 否 | 阶段卡存在且 stage definition gate 已 pass。 |
| 阶段锁定门禁未通过 | 否 | `stage_definition_gate_report.md` 中记录 `stage_definition_gate_status=pass`。 |
| 上一阶段未正式 pass | 否 | A2 summary、manifest、workflow、code quality 均有上游证据。 |
| 当前任务越界到后续阶段 | 否 | 本轮只做 Pre-check，不做 B1 训练和后续模块。 |
| 数据/评估/命名协议仍未冻结 | 是 | 当前轮没有 B1 experiment config、正式 run mapping、eval/postprocess version 和预训练权重缓存 SHA256。 |
| 本轮拟修改文件不属于当前阶段允许范围 | 否 | 当前拟生成文件均为 04 专属 B 类 Pre-check 留痕。 |
| 当前代码来源/freshness 未裁决 | 否 | 当前轮模型代码、factory和标准model config已重写；旧候选已进入04 clean-restart source snapshot。 |

## 5. 结论
- Stage Gate Result: `blocked`
- 结论说明: 上游 A2、研究定标和阶段锁定均已通过，但当前 B1 的正式 experiment config、三 seed identity、权重来源/缓存/离线策略、eval/postprocess version 和候选代码 freshness 尚未完成当前轮冻结。因此只能停留在 Pre-check，不能进入正式编码或实验。

## 5.1 本轮允许进入的工程落点

| 对象 | 允许动作 | 预期落点 |
|------|---------|---------|
| 正式代码 | not_applicable | 当前 Pre-check 不修改 `src/models/resnet34_unet.py` 或 `src/models/__init__.py`。 |
| 配置与正式资产 | not_applicable | 当前不创建 `configs/experiment/B1_*.yaml`、`experiments/B1_*` 或正式结果表。 |
| 模板与协议文档 | create | 只创建 `b_class_auxiliary/coding_guards/04_Baseline/pre_check_extraction.md`、`stage_gate_check.md`、`current_codebase_状态.md` 和 `04_Baseline_pre_check_guard.md`。 |
