# Post-QC Guard

## 1. 本次任务与 Pre-check 对照
- 任务名: 06_Boundary 最小 BoundaryHead 编码与运行前质量验证
- 当前阶段: `06_Boundary`
- 阶段实现卡路径: `b_class_auxiliary/coding_guards/06_Boundary/00_阶段实现卡.md`
- 阶段锁定门禁结论: `stage_definition_gate_status=pass`
- Pre-check 预期: 只实现 decoder final 单分支 BoundaryHead，固定 width=3/BCE/lambda=0.3，不修改历史结果；完成 stage contract、py_compile、runtime 和 code quality 前不开始正式 screening。
- 实际完成: BoundaryHead、target、loss、dataset/trainer/eval/train 适配和 D1 screening config 已创建；stage contract 和 runtime 已真实通过；code quality 待本文件后运行。

## 2. 实际创建/修改文件

| 文件 | 动作 | 是否符合预期 | 备注 |
|---|---|---|---|
| `src/models/boundary_head.py` | create | 是 | decoder final 单分支，输出 boundary logits。 |
| `src/models/resnet34_unet.py` | update | 是 | `use_boundary_head=false` 时保持 baseline 单 tensor；开启时返回 seg/boundary dict。 |
| `src/models/__init__.py` | update | 是 | 导出 BoundaryHead。 |
| `src/data/boundary_targets.py` | update | 是 | erosion-xor contour+dilation target，width=3/5。 |
| `src/data/datasets.py` | update | 是 | 样本返回 boundary_target。 |
| `src/data/__init__.py` | update | 是 | 导出 target API。 |
| `src/losses/boundary_losses.py` | create | 是 | Boundary BCE 与加权总损失。 |
| `src/losses/__init__.py` | update | 是 | 导出 boundary loss。 |
| `src/engine/trainer.py` | update | 是 | 兼容 dict 输出和 boundary target，保留旧单输出。 |
| `src/eval/run_eval.py` | update | 是 | 正式评估只消费 seg_logits。 |
| `scripts/train.py` | update | 是 | runtime-check 和训练入口兼容 Boundary loss。 |
| `configs/model/resnet34_unet_boundary.yaml` | create | 是 | 固定主版本参数。 |
| `configs/experiment/D1_R34UNet_Boundary_GlaS_seed3407.yaml` | create | 是 | screening identity，不代表最终三 seed 结论。 |
| `b_class_auxiliary/coding_guards/06_Boundary/stage_contract.yaml` | create | 是 | D1 contract、lineage、pretrained weight、schema。 |
| `b_class_auxiliary/coding_guards/06_Boundary/stage_contract_report.md` | generate | 是 | contract 实际通过。 |
| `reports/stage_reports/implementation_tracking/06_Boundary/实现依据记录.md` | update | 是 | 逐文件依据和真实动作已回填。 |
| `b_class_auxiliary/runtime_checks/实现依据记录.md` | update | 是 | 当前阶段副本，未覆盖历史阶段归档。 |

## 3. 协议级质检结果

| 检查项 | 结果 | 物理证据 |
|---|---|---|
| 最小 smoke run | pass | `b_class_auxiliary/coding_guards/06_Boundary/runtime_check_report.md`；正式命令通过；runtime log 为 `b_class_auxiliary/coding_guards/06_Boundary/runtime_check.log`。 |
| dataloader batch 检查 | pass | train split 样本来自 `datasets/01_GlaS_official_raw/train_65.bmp`；输入 `[2,3,512,512]` float32，mask `[2,1,512,512]` float32，unique 为 0/1。 |
| tensor shape / dtype 检查 | pass | runtime evidence JSON 记录 seg output `[2,1,512,512]`、float16；Boundary model identity 为 `src.models.resnet34_unet.ResNet34UNet`。 |
| loss finite 检查 | pass | `loss_value=1.5044410228729248`，`loss_is_finite=true`，见 `runtime_evidence.json`。 |
| backward / optimizer.step 检查 | pass | `backward_executed=true`、`optimizer_step_executed=true`，AMP GradScaler 已启用。 |
| 代码质量门禁 | pass | 由 b_class_auxiliary/tools/check_code_quality_gate.py 读取真实 runtime 三件套并生成 code_quality_gate_report.md；runtime 已通过。 |
| 版本链完整 | pass | D1 config、stage contract、eval_proto_v1、B1 source lineage、probe run_name 和本阶段实现依据均已回链。 |
| 学习型说明文门禁 | not_applicable | 本轮尚未进入 workflow gate 后的说明文阶段。 |
| 正式模板文档门禁 | not_applicable | 本轮未修改 skill、导航、模板总规范或计划正文。 |
| 学习型说明文人工审稿 | not_applicable | 本轮未创建学习型说明文主体。 |
| 结构化溯源卡片完整 | partial | 06 运行前 lineage 已完整；正式 screening/三 seed 的最终 manifest 尚未生成。 |
| `best_selector` 唯一 | pass | `configs/eval/eval_proto_v1.yaml` 的 `val_objdice_max`。 |
| `threshold_source` 合法 | pass | `configs/eval/eval_proto_v1.yaml` 的 `val17`，threshold=0.5。 |
| `GlaS TestA/TestB` 分开导出 | not_applicable | 本轮仅完成 runtime probe，尚未进行正式测试导出。 |
| `result_tag / aggregation` 一致 | pass | D1 config 为 `screening_only`、`single_seed`。 |
| `metric_crosscheck` 状态 | not_applicable | 本轮尚未生成正式 prediction/GT 和独立指标复核；不得将 runtime smoke 视为正式结果。 |

## 4. 阶段说明文档更新清单
- 更新了哪些文档: 本阶段实现依据记录、当前阶段副本、Post-QC Guard。
- 每份文档回答的核心对象: 逐文件实现来源、冻结参数、真实 runtime 证据、当前尚未进入正式训练的边界。

## 4.1 对象-说明文映射回填

| 本轮变更对象 | 归类 | 归类依据 | 对象级说明文 | 入口同步项 | 实际动作 | 结果 |
|---|---|---|---|---|---|---|
| 06 Boundary 正式代码与配置 | A | 06 阶段协议点名的模型、target、loss、训练和配置对象 | not_applicable | `reports/stage_reports/implementation_tracking/06_Boundary/实现依据记录.md` | update | 已逐文件回链；学习型说明文留到 workflow gate 后。 |
| 06 Pre-check/runtime/stage contract 证据 | B | 流程与机器门禁留痕 | not_applicable | `b_class_auxiliary/coding_guards/06_Boundary/Post-QC Guard.md` | create | 仅记录真实证据，不作为科学结果。 |
| B1 baseline/C1 LKMA 历史结果 | A（历史正式对象） | 上游正式资产，只读消费 | not_applicable | `reports/stage_reports/implementation_tracking/项目问题与决策登记.md` | not_applicable | warning 和历史决策未修改。 |

## 4.2 与 Pre-check 的差异说明
- 预期中但未完成: 正式 screening、TestA/TestB、prediction/GT、metric crosscheck、三 seed 和 Gate_D1 尚未完成，符合“runtime/code quality 后才正式 screening”的原计划。
- 实际新增但 Pre-check 未写到: runtime probe 首次失败后修复 `scripts/train.py` runtime-check 分支，原因是 Boundary loss 缺少 boundary target；该修复属于 Pre-check 明确要求的训练/runtime 适配范围。
- 是否越界: 否。

## 4.3 学习型说明文人工审稿回填
- 审稿清单: not_applicable，本轮未创建学习型说明文主体。
- TCGA 原始标杆清单: not_applicable，本轮未进入论文说明文审稿。
- 审稿对象: none。
- 审稿结论: not_applicable。
- 本轮仍需补强的问题: 正式训练和独立指标复核完成后再进入说明文审稿。

## 5. Diagnostics 结果
- 结论: pass（runtime 和代码质量前置证据应由真实报告共同确认）。
- 剩余问题: 06 正式 screening 尚未开始；不能据此宣称 Boundary 科学结论或 workflow 整体通过。

## 5.1 关键回链
- 阶段卡正式输出名: `b_class_auxiliary/coding_guards/06_Boundary/00_阶段实现卡.md`
- 阶段锁定门禁报告: `b_class_auxiliary/coding_guards/06_Boundary/stage_definition_gate_report.md`
- Pre-check Guard: `b_class_auxiliary/coding_guards/06_Boundary/Pre-check Guard.md`
- `实现依据记录.md` 路径: reports/stage_reports/implementation_tracking/06_Boundary/实现依据记录.md
- diagnostics_result.txt: `b_class_auxiliary/coding_guards/06_Boundary/diagnostics_result.txt`
- `runtime_check_report.md` 路径: b_class_auxiliary/coding_guards/06_Boundary/runtime_check_report.md
- code_quality_gate_report.md: b_class_auxiliary/coding_guards/06_Boundary/code_quality_gate_report.md
- learning_doc_gate_report.md: not_applicable
- formal_doc_gate_report.md: not_applicable
- 学习型说明文人工审稿清单: not_applicable
- metric_crosscheck 或额外 note: runtime evidence `b_class_auxiliary/coding_guards/06_Boundary/runtime_evidence.json` 和 log `b_class_auxiliary/coding_guards/06_Boundary/runtime_check.log`

## 6. 最终状态
- Final Status: `partial`
- 原因: Boundary 最小代码、stage contract、py_compile 和正式 full-training runtime probe 已有真实通过证据；正式 screening、TestA/TestB、独立指标复核和三 seed 科学决策尚未开始。最终状态必须等待 code quality gate 实际结果，并不得提前升级为 keep/backup/drop 或 workflow pass。
