# 冻结复现轮实现依据记录

- 阶段: `04_Baseline`
- 轮次: `frozen_reproduction_pending`
- 文件归类: 本表所列 markdown、gate report 和 contract checker 留痕均为 B 类流程/门禁对象；six configs 为已有 A 类正式配置，本轮只读核对。
- 真实性边界: 正式训练、测试、runtime、smoke、独立复核和正式 Gate 均未运行；未产生或修改任何 future 实验指标。

| 正式改动文件 | 归类 | 本次动作 | 依据与本轮决定 |
|---|---|---|---|
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/研究定标记录.md` | B | create | 依据 `模板R_研究定标记录.md` 与 `check_research_alignment_gate.py` 必填章节；锁定 future-only 与 historic 排除，不声称实验通过。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/00_阶段实现卡.md` | B | create | 依据 `模板0_阶段实现卡.md` 与 `check_stage_definition_gate.py`；锁定可进入 Pre-check 的范围，明确 runtime/smoke/训练均未运行。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/pre_check_extraction.md` | B | create | 依据 `模板5_Pre-check提取.md`；提取固定协议、future identity、historic 排除和本轮禁止运行边界。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/stage_gate_check.md` | B | create | 依据 `模板6_阶段门控检查.md`；allow 仅用于完成 Pre-check/进入准备，不外推为模型实验通过。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/current_codebase_状态.md` | B | create | 依据 `模板7_当前代码库状态.md` 与 `check_precheck_docs.py`；逐目录记录真实样本路径、文件数与 future output 未创建。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/Pre-check Guard.md` | B | create | 依据 `模板8_Pre-check Guard.md` 与 `check_precheck_docs.py`；回链独立四件套、阶段卡和专用报告。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_研究定标记录.md` | B | update | 旧过简路径改为导航/历史兼容，保留引用并指向独立正式研究记录。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_阶段实现卡.md` | B | update | 旧过简路径改为导航/历史兼容，保留引用并指向 `00_阶段实现卡.md`。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_precheck_四件套.md` | B | update | 旧汇总件保留为导航，明确不作为 checker 输入并列出独立四件套。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_research_alignment_gate_report.md` | B | update | 由 `check_research_alignment_gate.py` 专用输出路径生成；记录研究门禁，不是运行证据。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_stage_definition_gate_report.md` | B | update | 由 `check_stage_definition_gate.py` 专用输出路径生成；记录阶段锁定门禁，不是运行证据。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_precheck_doc_gate_report.md` | B | update | 由 `check_precheck_docs.py` 专用输出路径生成；记录 Pre-check，不是 runtime/模型 Gate。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_stage_contract_gate_report.md` | B | update | 由 `stage_contract_checker.py` 专用输出路径生成；只验证 pre-run contract。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/stage_definition_gate_report.md` | B | update | checker 因 Pre-check 固定同目录输入而生成的标准路径副本；与专用 04 报告同为 pass。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/precheck_doc_gate_report.md` | B | update | checker 因 Pre-check 固定同目录输入而生成的标准路径副本；与专用 04 报告同为 pass。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/stage_contract_gate_report.md` | B | update | stage contract checker 的同目录标准路径报告；专用 04 报告同为 pass。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_实现依据记录.md` | B | update | 依据 `模板I_实现依据记录.md` 和逐文件审计规则，登记本轮所有 md/yaml 正式改动与 checker 生成报告。 |

## 已有配置的只读依据

| 文件 | 归类 | 本轮动作 | 依据与本轮决定 |
|---|---|---|---|
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_stage_contract.yaml` | B | read_only_verify | 由 stage contract checker 验证 identity/schema/lineage/freshness；training_status 保持 `pending_not_run`。 |
| `configs/experiment/A2_UNet_GlaS_frozen_repro_seed3407.yaml` | A | read_only_verify | future A2 seed3407 config；新 run_name/output_dir，不编辑。 |
| `configs/experiment/A2_UNet_GlaS_frozen_repro_seed1234.yaml` | A | read_only_verify | future A2 seed1234 config；新 run_name/output_dir，不编辑。 |
| `configs/experiment/A2_UNet_GlaS_frozen_repro_seed2025.yaml` | A | read_only_verify | future A2 seed2025 config；新 run_name/output_dir，不编辑。 |
| `configs/experiment/B1_ResNet34_UNet_GlaS_frozen_repro_seed3407.yaml` | A | read_only_verify | future B1 seed3407 config；新 run_name/output_dir，不编辑。 |
| `configs/experiment/B1_ResNet34_UNet_GlaS_frozen_repro_seed1234.yaml` | A | read_only_verify | future B1 seed1234 config；新 run_name/output_dir，不编辑。 |
| `configs/experiment/B1_ResNet34_UNet_GlaS_frozen_repro_seed2025.yaml` | A | read_only_verify | future B1 seed2025 config；新 run_name/output_dir，不编辑。 |

## 未改动且禁止触碰的对象

- `experiments/**` 下的结果、checkpoint、run_meta、metrics、prediction 和日志均未编辑。
- 未运行正式训练、正式测试、runtime、smoke、独立指标复核或正式 Gate。
- historic v1 的任何指标均未被写入 future round 文档为本轮结果。
