# Pre-check Guard

## 1. 本次任务归属
- 当前阶段: 04_Baseline 的 frozen_reproduction_pending future round
- 上一阶段: `04_Baseline historic v1 recovery（仅历史审计）`
- 当前任务: `future frozen reproduction 的 Pre-check 文档、契约、配置和脚本语法验证`
- 阶段实现卡路径: `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/00_阶段实现卡.md`
- 阶段锁定门禁结论: `pass`
- Stage Gate Result: `allow`

## 2. 来自规划的硬约束
- future A2/B1 必须保持 train_proto_v1、eval_proto_v1、GlaS split、seed 3407/1234/2025、TestA/TestB 分离、七项指标与 ddof=0 （训练协议与对比规则均位于 04_Baseline 正式计划目录）。
- historic v1 recovery 仅作审计边界；future round 必须使用新 run_name 和未创建 output_dir，不能消费 historic 指标 (`reports/stage_reports/implementation_tracking/项目问题与决策登记.md`)。
- 正式训练、测试、runtime、smoke、独立复核和正式 Gate 未运行，绝不因本 Pre-check 通过而声称模型实验通过。

## 3. 来自参考资料的实现依据
- A2 plain U-Net 与 B1 ResNet34-U-Net 的对照边界来自 `结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/02_U-Net.md` 和 `结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/05_ResNet.md`；本轮不引入额外模块。
- `configs/eval/eval_proto_v1.yaml` 是未来配置共同引用的固定评估协议；本轮不调用评估。
- `b_class_auxiliary/tools/stage_contract_checker.py` 只核对 pre-run identity/schema/lineage/freshness；不生成运行或指标证据。

## 4. 当前工程已有能力与缺口
- 已有能力: six future YAML、future stage contract、三类文档 checker、stage contract checker、训练/测试入口和固定数据/split/config 路径均真实存在。
- 当前缺口: future output_dir、run_meta、checkpoint、metrics、prediction、runtime、smoke、独立复核和正式 Gate 均不存在或未运行。

## 5. 本次任务边界
- 明确要做: 只补齐 B 类 research、stage lock、四个 Pre-check 文档、专用 checker 报告、实现依据记录，并运行 checker 与 py_compile。
- 明确不做: 不编辑 six YAML，不编辑 `experiments/**`，不运行正式训练/测试/runtime/smoke/独立复核/正式 Gate，不写未来指标。

## 6. 预期代码落点
- 新建文件: `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/研究定标记录.md`、`b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/00_阶段实现卡.md`、四件套和实现依据；专用报告为 `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_research_alignment_gate_report.md`。
- 修改文件: 旧 `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_研究定标记录.md`、`b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_阶段实现卡.md`、`b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_precheck_四件套.md`、`b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_实现依据记录.md` 仅改为导航/历史兼容说明。
- 影响的 run / report / external: 不影响任何 run；不编辑实验目录；不消费 external；仅新增 04 专用 B 类报告。
- 越界核对: 任一新增实验目录、训练/测试命令、runtime/smoke 证据或历史指标转写，均视为超出本轮文档与契约范围。

## 6.1 预期最小运行验证
- Python 语法编译: 编译四个 checker，验证语法；不导入训练链。
- `最小运行验证命令`: not_applicable；用户明确禁止 runtime，本轮只执行文档 checker 与 py_compile。
- `smoke run`: not_applicable；未来仅可使用独立 `__smoke` run_name 执行。
- `dataloader batch`: not_applicable；未运行、无 shape/dtype 证据。
- 优化单步: not_applicable；未运行、无 loss、finite、backward 或 step 证据。
- 计划生成的 runtime 检查报告: `not_applicable`，未来真实 runtime 后生成。
- 计划生成的代码质量门禁报告: `not_applicable`，未来真实 runtime 后生成。

预期文档映射总计 7 个 B 类对象；每个对象均不需要学习型说明文，也不触发 A 类入口同步。

## 6.1 预期文档映射

| 本轮变更对象 | 归类 | 归类依据 | 对应学习型说明文 | 入口同步项 | 计划动作 | 备注 |
|---|---|---|---|---|---|---|
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/研究定标记录.md` | B | `crc_gland_segmentation_project/.trae/skills/制度完成定义.md` 的 gate/流程文件归 B | not_applicable | not_applicable | not_applicable | 已创建的研究前置记录，不是实验交付物。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/00_阶段实现卡.md` | B | `crc_gland_segmentation_project/.trae/skills/制度完成定义.md` 的 gate/流程文件归 B | not_applicable | not_applicable | not_applicable | 已创建的阶段锁定前置记录。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/pre_check_extraction.md` | B | `crc_gland_segmentation_project/.trae/skills/制度完成定义.md` 的 Pre-check 文件归 B | not_applicable | not_applicable | not_applicable | 已创建的四件套之一。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/stage_gate_check.md` | B | `crc_gland_segmentation_project/.trae/skills/制度完成定义.md` 的 Pre-check 文件归 B | not_applicable | not_applicable | not_applicable | 已创建；仅允许进入准备，不放行实验结果。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/current_codebase_状态.md` | B | `crc_gland_segmentation_project/.trae/skills/制度完成定义.md` 的流程扫描文件归 B | not_applicable | not_applicable | not_applicable | 已创建，留下十目录真实扫描。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/Pre-check Guard.md` | B | `crc_gland_segmentation_project/.trae/skills/制度完成定义.md` 的 guard 文件归 B | not_applicable | not_applicable | not_applicable | 已创建的 Pre-check 汇总件。 |
| `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_precheck_doc_gate_report.md` | B | `crc_gland_segmentation_project/.trae/skills/制度完成定义.md` 明确 gate report 属 B | not_applicable | not_applicable | not_applicable | 专用报告，不覆盖共享路径。 |

## 7. 上游 guard 文件回链
- 阶段卡正式输出名 00_阶段实现卡.md: `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/00_阶段实现卡.md`；已完成，边界为 future pending。
- 阶段锁定门禁报告 stage_definition_gate_report.md: `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_stage_definition_gate_report.md`；已运行，结论 pass。
- `pre_check_extraction.md`: `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/pre_check_extraction.md`；已完成，明确不运行实验。
- `stage_gate_check.md`: `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/stage_gate_check.md`；已完成，Stage Gate Result=allow，仅进入准备。
- `current_codebase_状态.md`: `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction/current_codebase_状态.md`；已完成，记录 ten-directory 扫描。
- `precheck_doc_gate_report.md`: `b_class_auxiliary/coding_guards/04_Baseline/frozen_reproduction_precheck_doc_gate_report.md`；将由 checker 专用路径生成，结论不得外推为 runtime 或模型实验通过。
