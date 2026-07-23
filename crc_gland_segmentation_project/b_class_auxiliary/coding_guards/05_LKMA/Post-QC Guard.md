# Post-QC Guard

## 1. 当前阶段
- 当前阶段: C1 / 05_LKMA
- 当前工作流位置: 运行后证据收口 -> 总放行后说明文档门禁
- 当前结论: 三个正式 seed、独立 prediction/GT 指标复核、派生汇总、C1 决策和 workflow gate 已真实完成；C1 模型决策为 `drop`，后续模型起点回到 B1。

## 2. 实际创建/修改文件

| 文件 | 动作 | 归类 | 真实状态 |
|---|---|---|---|
| `b_class_auxiliary/tools/summarize_lkma_stage.py` | create | B | 只读 C1/B1 原始资产，生成派生汇总、成本、manifest 和决策记录 |
| `reports/tables/lkma_per_seed_summary.csv` | create | B | 从三个 C1/B1 原始 metrics CSV 派生 |
| `reports/tables/baseline_vs_lkma_mean_std.csv` | create | B | 逐 split、逐指标生成 mean+-std 和 delta |
| `reports/tables/lkma_cost_comparison.csv` | create | B | 从真实 checkpoint 计算参数量和 SHA256 |
| `reports/tables/lkma_stage_manifest.csv` | create | B | 回链三个 C1 run、checkpoint、raw CSV 和独立复核 JSON |
| `reports/stage_reports/lkma_stage_summary.md` | create | B | C1 阶段收口摘要，非 A 类学习说明文 |
| `reports/stage_reports/lkma_decision_note.md` | create | B | C1 keep/backup/drop 决策留痕，非 A 类学习说明文 |
| `b_class_auxiliary/coding_guards/05_LKMA/independent_metric_check_seed*.json` | create | B | 三 seed prediction/GT 独立复核结果 |
| `b_class_auxiliary/coding_guards/05_LKMA/workflow_gate_report.md` | update | B | 本轮总放行流程报告 |

本轮是 C1 正式运行后的 closeout turn。编码阶段创建的 A 类 LKMA 代码和配置不是本轮修改对象；本轮只读取它们并消费其真实产物。

## 3. 协议级质检结果

| 检查项 | 结果 | 物理证据 |
|---|---|---|
| 最小 smoke run | pass | runtime_check_report.md 与 runtime_evidence.json 的 smoke_run_pass=pass |
| dataloader batch 检查 | pass | runtime_evidence.json 的真实样本路径、input/target shape、dtype 和 finite 字段 |
| tensor shape / dtype 检查 | pass | runtime_evidence.json 的 input_shape、target_shape、output_shape、dtype 字段 |
| loss finite 检查 | pass | runtime_evidence.json 的 loss_value 和 loss_is_finite=true |
| backward / optimizer.step 检查 | pass | runtime_evidence.json 的 backward_executed=true、optimizer_step_executed=true |
| 代码质量门禁 | pass | check_code_quality_gate.py 基于本轮真实 runtime、实现依据和本表重新生成报告 |

## 4. Diagnostics 结果
- `diagnostics_result.txt` 路径: `diagnostics_result.txt`
- 结论: partial
- 原因: runtime、正式训练/测试、独立指标复核和派生汇总已完成；代码质量门禁报告已重新生成，待门禁复核结果确认。

## 4.1 对象-说明文映射回填

| 本轮变更对象 | 归类 | 对象级说明文 | 计划动作 | 备注 |
|---|---|---|---|---|---|
| `b_class_auxiliary/tools/summarize_lkma_stage.py` | B | `not_applicable` | `not_applicable` | 阶段收口辅助工具，计划未点名为正式模型/数据对象 |
| `reports/tables/lkma_per_seed_summary.csv` | B | `not_applicable` | `not_applicable` | 派生审计汇总，不是原始实验结果真源 |
| `reports/tables/baseline_vs_lkma_mean_std.csv` | B | `not_applicable` | `not_applicable` | 派生统计表，不承担正式模型实现 |
| `reports/tables/lkma_cost_comparison.csv` | B | `not_applicable` | `not_applicable` | 收口成本审计表 |
| `reports/tables/lkma_stage_manifest.csv` | B | `not_applicable` | `not_applicable` | 运行后 lineage manifest |
| `reports/stage_reports/lkma_stage_summary.md` | B | `not_applicable` | `not_applicable` | 阶段 gate/决策收口摘要 |
| `reports/stage_reports/lkma_decision_note.md` | B | `not_applicable` | `not_applicable` | 阶段 keep/backup/drop 决策留痕 |
| `b_class_auxiliary/coding_guards/05_LKMA/independent_metric_check_seed*.json` | B | `not_applicable` | `not_applicable` | 独立复核门禁证据 |

本轮实际创建/修改对象全部归 B 类流程与收口证据，不进入 A 类学习型说明文映射。编码阶段的 A 类对象仍按其原有阶段说明文映射处理，本轮不重复创建或重写。

## 5.1 关键回链
- `runtime_check_report.md` 路径: `runtime_check_report.md`
- `实现依据记录.md` 路径: `实现依据记录.md`
- `diagnostics_result.txt` 路径: `diagnostics_result.txt`
- `workflow_gate_report.md` 路径: `workflow_gate_report.md`
- `lkma_stage_summary.md` 路径: `reports/stage_reports/lkma_stage_summary.md`
- `lkma_decision_note.md` 路径: `reports/stage_reports/lkma_decision_note.md`

## 6. 最终状态
- Final Status: partial
- 解释: C1 正式实验和派生决策已形成；C1 workflow gate 仍需单独运行，不能将代码质量 pass 扩写为阶段总放行。
