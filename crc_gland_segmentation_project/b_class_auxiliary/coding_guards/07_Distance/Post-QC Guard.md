# 07_Distance Post-QC Guard

## 1. 本次任务与前置门禁
- 任务名：07_Distance 最小 EDT_norm01 Distance supervision 编码与运行前质量验证
- 当前阶段：`07_Distance`
- 阶段实现卡路径：`b_class_auxiliary/coding_guards/07_Distance/00_阶段实现卡.md`
- 阶段锁定门禁结论：`stage_definition_gate_status=pass`
- Pre-check 门禁结论：`precheck_doc_gate_status=pass`
- stage contract：`stage_contract_status=pass`
- 当前主线输入：`boundary_input_base`
- 06 Boundary 决策：`backup`
- 当前正式运行：尚未开始；本轮只完成最小代码和 runtime，code quality 正在重新生成。

## 2. 实际创建/修改文件

| 文件 | 动作 | 依据 | 当前状态 |
|---|---|---|---|
| `src/data/distance_targets.py` | update | 07/02 距离图与 lambda 范围 | EDT signed target、per-sample norm01、空/全 mask 全零。 |
| `src/data/datasets.py` | update | 07/00、07/02 | batch 增加 distance_target。 |
| `src/data/__init__.py` | update | 07 工程映射 | 导出 build_distance_target。 |
| `src/losses/seg_losses.py` | update | 07/00、07/02 | 增加 DistanceBCEDiceLoss 和 build_distance_loss。 |
| `src/losses/__init__.py` | update | 07 工程映射 | 导出 Distance loss。 |
| `src/models/resnet34_unet.py` | update | 07/00、07/01 | 增加 use_distance_head；保留旧单输出和 Boundary 分支。 |
| `src/engine/trainer.py` | update | 07/03、全局 AMP/训练协议 | 训练路径消费 distance_target 和 distance_logits，记录 distance loss。 |
| `src/eval/run_eval.py` | update | eval_proto_v1 | 验证 loss 支持 Distance；正式 segmentation 仍只消费 seg_logits。 |
| `scripts/train.py` | update | 07/03 | D2 config 选择 Distance loss。 |
| `scripts/test.py` | update | eval_proto_v1 | D2 config 选择 Distance loss。 |
| `configs/model/resnet34_unet_distance.yaml` | create | 07 阶段实现卡 | distance_v1、BoundaryHead=false、DistanceHead=true、lambda=0.1。 |
| `configs/experiment/D2_R34UNet_Distance_GlaS_seed3407.yaml` | create | 07/03、identity 规范 | D2 seed3407 screening identity。 |
| `b_class_auxiliary/coding_guards/07_Distance/stage_contract.yaml` | create | contract 规范 | identity、schema、lineage、freshness、required paths。 |
| `b_class_auxiliary/coding_guards/07_Distance/实现依据记录.md` | create | 编码 skill | 逐文件计划依据和工程收敛边界。 |

## 3. 协议级质检结果

| 检查项 | 结果 | 物理证据 |
|---|---|---|
| 最小 smoke run | pass | `b_class_auxiliary/coding_guards/07_Distance/runtime_check_report.md` |
| dataloader batch 检查 | pass | `b_class_auxiliary/coding_guards/07_Distance/runtime_evidence.json` |
| tensor shape / dtype 检查 | pass | `b_class_auxiliary/coding_guards/07_Distance/runtime_evidence.json` |
| loss finite 检查 | pass | `b_class_auxiliary/coding_guards/07_Distance/runtime_evidence.json` |
| backward / optimizer.step 检查 | pass | `b_class_auxiliary/coding_guards/07_Distance/runtime_evidence.json` |
| 代码质量门禁 | pass | `b_class_auxiliary/coding_guards/07_Distance/code_quality_gate_report.md` |

## 3.1 真实验证结果

| 检查项 | 结果 | 物理证据 |
|---|---|---|
| py_compile | pass | 本轮 `python -m py_compile` 覆盖 distance target/dataset/loss/model/trainer/eval/train/test。 |
| target smoke | pass | 空 mask、全 mask、局部 mask 均检查 shape、float32、finite、range [0,1]。 |
| model output | pass | distance model 返回 seg_logits 和 distance_logits，shape 对齐。 |
| loss finite | pass | DistanceBCEDiceLoss total loss finite。 |
| backward | pass | target/model/loss smoke 完成 backward。 |
| stage contract | pass | `b_class_auxiliary/coding_guards/07_Distance/stage_contract_report.md`。 |
| runtime probe | pass | `runtime_check_report.md`、`runtime_evidence.json`、`runtime_check.log`。 |
| code quality | 待本 Guard 建立后运行 | 不提前宣称 pass。 |
| formal screening | not_started | 不能把 runtime 当正式实验结果。 |

## 3.1 协议级质检结果表

| 检查项 | 状态 | 证据 |
|---|---|---|
| runtime 三件套 | pass | 07 Distance runtime report/evidence/log |
| dataloader batch | pass | runtime evidence |
| tensor shape/dtype | pass | runtime evidence |
| loss finite | pass | runtime evidence |
| backward/optimizer.step | pass | runtime evidence |
| formal screening | not_started | 尚未运行 |

## 4. 诚实边界
- 本轮证明的是 Distance 训练入口的最小工程闭环，不证明 Distance 科学效果。
- 尚未完成 smoke training、正式 seed3407 screening、TestA/TestB、独立指标复核、三 seed 和 keep/backup/drop。
- 不修改 B1、C1、D1 历史结果，不把 06 Boundary backup 改写为 keep。
- code quality 通过后仍需最小 smoke training；smoke 通过后才允许正式 screening。

## 5.1 关键回链
- 阶段卡正式输出名: `b_class_auxiliary/coding_guards/07_Distance/00_阶段实现卡.md`
- 阶段锁定门禁报告: `b_class_auxiliary/coding_guards/07_Distance/stage_definition_gate_report.md`
- Pre-check Guard: `b_class_auxiliary/coding_guards/07_Distance/Pre-check Guard.md`
- `实现依据记录.md` 路径: b_class_auxiliary/coding_guards/07_Distance/实现依据记录.md
- diagnostics_result.txt: b_class_auxiliary/coding_guards/07_Distance/diagnostics_result.txt
- `runtime_check_report.md` 路径: `b_class_auxiliary/coding_guards/07_Distance/runtime_check_report.md`

## 6. 后续动作
- code quality gate 通过后，运行独立 D2 smoke training/evaluation。
- smoke 通过且代码/配置冻结后，用户再运行 seed3407 screening。
- seed3407 screening 完成后才决定是否建立 seed1234/2025 正式配置。
