# Skill 治理记录：运行前契约与单一真源

- record_type: `skill_governance`
- governance_stage: `治理`
- source_stage: `02_UNet流程验证 + 03_UNet稳定性复盘`
- source_protocol_version: `eval_proto_v1`
- current_consumption: `后续 04+ 阶段运行前契约与门禁设计`
- valid_for_current_gate: `true`

## 本轮发现的已知失败模式

| 失败模式 | 根因 | 影响 |
|---|---|---|
| 配置路径与正式 run_name 混用 | 没有唯一身份真源 | Pre-check、manifest、handoff 反复修补 |
| sample-only raw 与 aggregate 语义混淆 | schema 未在运行前锁定 | 汇总 Gate 使用旧字段，结果需要重算 |
| 旧 gate/summary/blocker 与真实结果不同步 | 没有 freshness 规则 | 已通过结果看起来仍 blocked |
| lineage 只存在自然语言 | 缺少七字段硬约束 | 下游无法机器核对消费边界 |
| 规则写在文档中但没有执行落点 | 没有规则自验证流程 | 小问题持续到运行后才暴露 |

## 本轮新增/收紧的规则与执行落点

| 规则 | 执行落点 |
|---|---|
| 正式数值只认脚本生成的 CSV/JSON/YAML/checkpoint | `crc-gland-coding-guard/SKILL.md` 第五铁律；阶段 gate 报告必须回链原始产物 |
| 阶段状态只认当前阶段 gate report | `SKILL.md` 第五铁律；`制度完成定义.md` 状态消费规则 |
| 跨阶段身份只认 manifest | `SKILL.md` 第五铁律；七字段 lineage 写入计划、manifest、实现依据 |
| 正式运行前必须检查 identity/schema/lineage/freshness | `制度完成定义.md`「Pre-check 运行前四项阻断契约」；后续 Pre-check Guard 必须逐项回链 |
| 代码/配置/manifest/评估口径变化后旧 gate 过期 | `SKILL.md` 第五铁律 freshness；重新生成 runtime/code-quality/workflow |
| 规则修改后必须自验证 | `SKILL.md` 第五铁律「规则修改也必须验证」；本记录；`check_formal_stage_docs.py` |
| 同义规则不再散落追加 | `crc-gland-skill-governance/SKILL.md`「每条规则必须有执行落点」 |

## 验证命令与结果

- `python b_class_auxiliary/tools/check_formal_stage_docs.py --project-root /home/featurize/work/Paper/crc_gland_segmentation_project`
- 根入口、项目导航、制度完成定义和本记录均需执行 diagnostics；若返回 `not_applicable`，必须按原始输出留痕，不得改写成 `pass`。

## 本轮 skill 遍历与调用裁决

### 已遍历 skill inventory

- `crc-gland-coding-guard`: `required / consulted`，唯一总入口。
- `crc-gland-skill-governance`: `required / consulted`，本轮正在修改 skill 与项目导航。
- `crc-gland-research-alignment`: `not_applicable`，本轮不是进入新的研究定标，而是治理规则修改。
- `crc-gland-stage-implementation`: `not_applicable`，本轮未进入正式编码。
- `crc-gland-learning-doc`: `not_applicable / blocked`，当前 workflow gate 未通过，且本轮不是说明文档交付。
- `standard-md-rewrite`: `required / consulted`，本轮修改了 `01_实验执行` 下的阶段计划 Markdown。

### 规则变更与执行落点

| 变更 | 唯一落点 | 验证方式 |
|---|---|---|
| 每轮先读取项目内导航并枚举全部 skill | 根入口 `Skill 体系遍历与选择协议`；项目导航 `Skill 遍历与调用矩阵` | 当前路由消息必须输出 inventory 字段 |
| 按触发条件读取/调用专项 skill | 项目导航 skill 矩阵 | 每轮记录 required/consulted/not_applicable/blocked |
| 不把调用总入口等同于遍历全部 skill | 根入口边界条款 | 路由审查逐项列出 skill 状态 |
| 规则体系修改后进行正式文档检查 | `check_formal_stage_docs.py` | 本轮复跑该脚本 |

## 当前边界

- 本记录是 B 类治理文件，不是实验结果，不进入 A 类正式对象清单。
- 当前冻结基线消费字段：`current_baseline=B1 current_standard`、`baseline_ready_for_lkma=frozen_conditional_baseline`、`baseline_status=valid_with_stability_warning`、`stability_warning=true`、`original_gate_b1=false`、`consumption_boundary=frozen_baseline_with_warning`、`formal_handoff=conditional_handoff`。
- 本记录不改变 02/03 历史实验结果，不修改指标 CSV、run_meta 结果字段、checkpoint 或 gate 数字。
- `stage contract checker` 在 04 首次建立，04-11 阶段复用；每阶段只提供自己的契约输入，不复制 checker 实现
- checker 的工作流位置固定为 `research alignment → stage lock → Pre-check → checker → 正式编码/运行 → runtime → code quality → workflow gate`
- 后续阶段若发现规则没有对应 field/template/script/report，必须先回到治理，不得继续编码或训练。
- 2026-07-17 冻结 B1 决策：`original_gate_b1=false` 与 04 原始 handoff blocked 作为历史审计事实保留；后续阶段消费状态为 `frozen_conditional_baseline`，允许在 `frozen_baseline_with_warning` 边界下正式执行，但不得改写原始 Gate 或删除 `stability_warning`。
- 本轮入口一致性修复范围：问题登记、04_Baseline 主协议、05_LKMA 主协议；06_Boundary 只消费 05 的 `current_base`，进入 06 研究定标前再做 05→06 入口复核。
- 执行落点：`current_baseline / baseline_status / stability_warning / original_gate_b1 / consumption_boundary` 写入 05 阶段契约或 manifest；规则一致性由 `check_formal_stage_docs.py` 和各阶段 Pre-check / stage contract checker 复核。
