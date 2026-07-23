# 07_Distance 阶段门控核对

## 1. 当前状态
- 当前编号阶段：`07_Distance`
- 当前 workflow 阶段：`Pre-check`
- research alignment gate：`pass`
- stage definition gate：`pass`
- 06 Boundary workflow gate：`pass`
- 进入条件已同时核对研究记录、阶段卡、两个 gate report 和上游决策记录。
- 06 Boundary decision：`backup`
- 当前默认输入：`boundary_input_base`
- Stage Gate Result: `allow`

## 3. 当前阶段进入条件

| 条件 | 真实证据 | 状态 |
|---|---|---|
| 研究定标完成 | `b_class_auxiliary/runtime_checks/research_alignment_gate_report.md` | pass；研究结论已允许阶段锁定，且已写明 Distance target/loss/lambda 边界。 |
| 阶段实现卡完成 | `b_class_auxiliary/coding_guards/07_Distance/00_阶段实现卡.md` | pass；唯一目标、允许改动、禁止项、运行验证计划均已锁定。 |
| 阶段定义门禁通过 | `b_class_auxiliary/coding_guards/07_Distance/stage_definition_gate_report.md` | pass；机器检查通过，未发现越界变量。 |
| 上阶段已收口 | `b_class_auxiliary/coding_guards/06_Boundary/workflow_gate_report.md` | pass；06 已完成总放行，原始资产只读。 |
| 上阶段 Boundary 交接语义 | `/home/featurize/work/Paper/crc_gland_segmentation_project/reports/stage_reports/implementation_tracking/06_Boundary/boundary_decision_note.md` | backup → boundary_input_base；不得默认继承 BoundaryHead，07 从 B1 主线重新建立证据。 |

进入条件核对结论：以上五项均有真实文件路径和明确状态；因此当前可以继续完成 Pre-check 文档核对，但还不能进入正式编码。
- 研究定标、阶段锁定和上阶段 workflow gate 的真实报告均已存在并显示 pass。
- 当前输入边界是 boundary_input_base，不是 BoundaryHead 主线。
- 当前仅允许完成 Pre-check 文档核对，正式源码仍保持冻结。

## 4. 阻断项

| 阻断项 | 当前状态 | 解除条件 |
|---|---|---|
| Distance target 正式接入 | 未实现；当前只有预览 helper | Pre-check 通过后编码、py_compile 和 target smoke 通过。 |
| Distance loss 正式接入 | 未实现；当前 segmentation loss 只有 BCE+Dice | Pre-check 通过后新增最小 Distance loss 并完成 finite/backward 验证。 |
| D2 config/contract | 未建立；D2 尚未有正式 run identity | 完成代码落点登记后建立 D2 model/experiment config 和 contract checker。 |
| runtime 三件套 | 未生成；当前没有 07 probe 资产 | 正式代码冻结后运行独立 probe，生成 report/evidence/log。 |
| 正式训练/测试 | 未开始；experiments 只有 D1 历史目录 | runtime、smoke、code quality 全部通过后才启动 seed3407 screening。 |

阻断核对结论：Distance target、Distance loss、D2 identity、runtime 和正式训练均尚未产生真实资产；任何一项未解除都禁止正式 screening。
- Distance target 尚未接入 dataset batch，不能宣称数据链已成立。
- Distance loss 尚未接入训练/验证，不能宣称总 loss 已成立。
- D2 config、contract、runtime 三件套和 smoke 仍然缺失，不能开始 seed3407 screening。

## 5.1 本轮允许进入的工程落点

工程落点核对结论：当前只允许建立和修正 Pre-check 文档；正式 Distance 源码、D2 config、contract、runtime 和实验资产仍被阻断。

| 落点 | 当前状态 | Pre-check 后允许动作 |
|---|---|---|
| Pre-check 文档 | 已建立并正在门禁 | 继续修正真实路径和约束证据，直到 gate pass。 |
| Distance target/loss | 未接入正式训练链 | gate pass 后才能新增/修改。 |
| Model/trainer/eval | 已有 baseline/Boundary 接口 | gate pass 后只做最小 Distance 适配，保留旧路径。 |
| D2 config/contract | 尚未建立 | gate pass 后锁定正式 identity 和 schema。 |
| runtime/smoke/reports | 尚未产生 | 正式代码冻结后由脚本产生，不手工填结果。 |

## 4. 本轮允许进入的工程落点

| 类别 | 允许动作 | 当前边界 |
|---|---|---|
| Pre-check 文档 | create/update | 只记录真实现状，不把未实现链路写成已完成。 |
| 正式源码 | blocked until Pre-check pass | 当前不能修改 src/scripts/configs。 |
| D2 训练/测试 | blocked | 不运行正式训练，不运行正式测试。 |
| 历史结果 | read-only | 不修改 B1、C1、D1 结果和 gate。 |

## 5. 通过后的下一步
- Pre-check doc gate 通过后，才允许进入最小 Distance 代码实现。
- 编码前必须重新检查本文件与实现依据记录，确保新增文件逐文件登记。
- 编码后必须运行 py_compile、stage contract、runtime、smoke、code quality，再决定 D2 seed3407 screening。
