# 07_Distance Pre-check Guard

## 1. 本次任务归属
- 当前编号阶段：`07_Distance`
- 当前 workflow 阶段：`Pre-check`
- Stage Gate Result: `allow`
- 上游 research alignment：`pass`
- 上游 stage definition：`pass`
- 上游阶段：`06_Boundary` workflow gate `pass`
- 上游决策：Boundary `backup`
- 阶段实现卡路径: `b_class_auxiliary/coding_guards/07_Distance/00_阶段实现卡.md`
- 阶段锁定门禁结论: `pass`
- 当前默认输入：`boundary_input_base`
- 当前阶段目标：锁定并核对 EDT_norm01 distance supervision 的工程入口，尚未进入正式编码。

## 2. 本轮核对的正式依据
- 07 研究定标记录：`b_class_auxiliary/coding_guards/07_Distance/研究定标记录.md`
- 07 阶段实现卡：`b_class_auxiliary/coding_guards/07_Distance/00_阶段实现卡.md`
- 07 阶段门控核对：`b_class_auxiliary/coding_guards/07_Distance/stage_gate_check.md`
- 07 当前代码库状态：`b_class_auxiliary/coding_guards/07_Distance/current_codebase_状态.md`
- 07 Pre-check 提取：`b_class_auxiliary/coding_guards/07_Distance/pre_check_extraction.md`
- 06 决策记录：`reports/stage_reports/implementation_tracking/06_Boundary/boundary_decision_note.md`
- 06 workflow gate：`b_class_auxiliary/coding_guards/06_Boundary/workflow_gate_report.md`

## 3. 计划约束与当前事实

| 约束 | 当前真实事实 | Pre-check 结论 |
|---|---|---|
| 单一 Distance auxiliary supervision | 当前正式训练链尚未接入 | 允许后续最小编码，不允许现在宣称已实现 |
| EDT_norm01_v1 | `src/data/distance_targets.py` 存在预览 helper，但尚未完成正式 contract 验证 | 必须在 runtime 验证 target range/shape/dtype/finite |
| SmoothL1 + lambda 0.1 | 当前 loss builder 尚无 Distance loss | Pre-check 后实现，默认只做主版本 |
| Boundary backup | 06 decision note 明确 `backup` | 07 必须关闭 BoundaryHead，不得继承 D1 模型配置 |
| eval_proto_v1 | 当前 eval 配置和测试入口存在 | 沿用，不改 threshold/selector/split/metrics |
| 三 seed | 07 尚未正式训练 | 先 seed3407 screening，再按真实证据决定是否补 seed1234/2025 |

## 4. 当前接口核对结论
- dataset：现有 sample dict 返回 image、mask、sample identity；Distance target 尚未进入正式 batch。
- target：现有 `src/data/distance_targets.py` 可复用，但必须核对 per-sample norm01、空/全 mask 和 transform 后尺寸。
- model：`src/models/resnet34_unet.py` 已支持 Boundary dict 输出；07 需要新增独立 distance auxiliary 输出或等价最小接口，并默认 `use_boundary_head=false`。
- loss：`src/losses/seg_losses.py` 已提供 BCE+Dice；07 需要新增 `L_total=L_seg+0.1*L_dist`，Distance loss 采用 SmoothL1，reduction 必须明确。
- trainer：当前 trainer 已能处理 dict 输出，但只认识 boundary target；07 需要新增 distance target/logit 分支并保留旧单输出路径。
- eval：当前评估只应从 outputs 中消费 seg_logits；distance logits 不能参与 threshold 或预测 mask。
- train/test：当前入口按 model config 选择 loss；07 需增加独立 D2 配置并保持 D1/B1 可复用。

## 5. 当前未决但必须在编码前解决
- 空 mask / 全 mask：统一 target 为全零 distance map，并在 target helper 中写单元/shape/range 测试。
- target shape/dtype：`[B,1,H,W]`、float32、finite、min>=0、max<=1。
- distance output：单通道 logits，与 final decoder feature 对齐；只参与辅助 loss。
- loss reduction：SmoothL1 默认 mean，total loss 为 segmentation loss 加权和。
- transform：mask 在 tensor 化后生成 target，保证与训练 image/mask 尺寸一致。
- D2 identity：Pre-check 通过后再锁定正式 model/experiment config、run_name、seed 和 stage contract。

## 6. 预期代码落点
- 仅在 Pre-check gate 通过后允许修改正式代码：
  - `src/data/distance_targets.py`（当前已存在，可复用）
  - `src/data/datasets.py`
  - `src/models/resnet34_unet.py`
  - `src/losses/seg_losses.py`（当前已存在；Distance loss 模块尚未建立，后续扩展文件名待编码前锁定）
  - `src/losses/__init__.py`
  - `src/engine/trainer.py`
  - `src/eval/run_eval.py`
  - `scripts/train.py`
  - `scripts/test.py`
- 仅在 Pre-check gate 通过后允许新增 D2 config、contract、runtime 和 implementation tracking 资产。
- 不修改 D1/B1/C1 原始结果、历史 checkpoint、历史 metrics 或 eval protocol。

## 7. 上游 guard 文件回链
- pre_check_extraction.md
- stage_gate_check.md
- current_codebase_状态.md
- 00_阶段实现卡.md
- stage_definition_gate_report.md
- precheck_doc_gate_report.md
- b_class_auxiliary/runtime_checks/research_alignment_gate_report.md
- b_class_auxiliary/coding_guards/06_Boundary/workflow_gate_report.md

## 7.1 运行前物理核对计划
- 真实路径：核对 datasets、splits、configs、src、scripts、tools、b_class_auxiliary、experiments、external、reports。
- 真实接口：读取 dataset sample dict、model forward、loss forward、trainer train/validation、eval segmentation logits 消费。
- 真实依赖：确认 scipy distance transform、torch SmoothL1、现有 DataLoader transform 可用。
- 真实证据：Pre-check 通过前不运行正式训练；通过后先 py_compile、target unit smoke、独立 runtime probe 和最小 smoke。

## 6.1 预期文档映射

| 本轮变更对象 | 对应学习型说明文 | 计划动作 | 备注 |
|---|---|---|---|
| `src/data/distance_targets.py` | reports/stage_reports/implementation_tracking/07_Distance/distance_learning_note.md | create | 正式代码对象，Pre-check 通过后才允许创建。 |
| Distance loss module (filename to be locked before coding) | reports/stage_reports/implementation_tracking/07_Distance/distance_learning_note.md | create | 正式代码对象，Pre-check 通过后才允许创建。 |
| `src/models/resnet34_unet.py` | reports/stage_reports/implementation_tracking/07_Distance/distance_learning_note.md | update | 保留 baseline/Boundary 行为，新增 Distance 最小分支。 |
| `src/data/datasets.py` | reports/stage_reports/implementation_tracking/07_Distance/distance_learning_note.md | update | 增加 distance_target，不改变已有字段语义。 |
| `src/engine/trainer.py` | reports/stage_reports/implementation_tracking/07_Distance/distance_learning_note.md | update | 增加 Distance loss，保留旧单输出。 |
| `src/eval/run_eval.py` | reports/stage_reports/implementation_tracking/07_Distance/distance_learning_note.md | update | 正式评估只消费 seg_logits。 |
| `scripts/train.py` | reports/stage_reports/implementation_tracking/07_Distance/distance_learning_note.md | update | 按 D2 config 构建 Distance loss。 |
| `scripts/test.py` | reports/stage_reports/implementation_tracking/07_Distance/distance_learning_note.md | update | 按 D2 config 保持 TestA/TestB 评估。 |

## 8. 预期文档映射

### 8.1 预期文档映射

| 本轮变更对象 | 对应学习型说明文 | 计划动作 | 备注 |
|---|---|---|---|
| `src/data/distance_targets.py` | not_applicable | create | 正式代码对象，完成后由实现依据记录回链。 |
| Distance loss module (filename to be locked before coding) | not_applicable | create | 正式代码对象，完成后记录 SmoothL1 和 loss 组合。 |
| `src/models/resnet34_unet.py` | not_applicable | update | 保留旧 baseline/Boundary 分支，新增 Distance 最小分支。 |
| `src/data/datasets.py` | not_applicable | update | 增加 distance_target，不改变旧字段语义。 |
| `src/engine/trainer.py` | not_applicable | update | 增加 distance target/logit/loss，保留旧单输出。 |
| `src/eval/run_eval.py` | not_applicable | update | 评估只消费 seg_logits。 |
| `scripts/train.py` | not_applicable | update | 按 D2 config 构建 Distance loss。 |
| `scripts/test.py` | not_applicable | update | 按 D2 config 评估并保持 TestA/TestB。 |

## 9. 上游 guard 文件回链
- pre_check_extraction.md
- stage_gate_check.md
- current_codebase_状态.md
- 00_阶段实现卡.md
- stage_definition_gate_report.md
- precheck_doc_gate_report.md
- `b_class_auxiliary/runtime_checks/research_alignment_gate_report.md`
- `b_class_auxiliary/coding_guards/06_Boundary/workflow_gate_report.md`

## 10. 当前 Pre-check 结论
- `Stage Gate Result: allow`
- 该 allow 只表示允许执行 Pre-check 文档核对，不表示 Pre-check 已通过。
- 当前仍禁止正式代码、正式配置、runtime、smoke、训练、测试和 workflow gate。
