# 05 方法验收、止损与 planning handoff schema

## 1. 文件角色与执行边界

- `plan_object_class=A`：05 正式验收与跨阶段交接协议。
- `protocol_version=05-handoff-v2.0-20260719`
- `plan_status=planned`；`execution_status=not_run`
- `result_eligibility=false`；`implementation_permission=false`
- `gate_status=blocked_not_run`
- `consumer_stage=06_val筛查`，但 `consumer_release=false`。

本文件只定义未来 handoff 的结构与放行门，不生成 manifest 文件，不代表 06 已获准训练或筛查。

## 2. 本轮直接依赖的前置文件

| 角色 | 依赖 | 相关性 |
|---|---|---|
| 上游治理 | `00_总览与规范/03_命名与结果记录规范.md`、`06_实验执行证据化写作模板.md`、`07_实验执行全局修订与质检规范.md` | lineage、四状态、Gate 和证据闭环 |
| 同层生产者 | `00_阶段总协议.md`、`01_N1实例轮廓协议.md`、`02_N2融合协议.md`、`03_N3实例恢复协议.md` | 提供可交接的方法身份、候选和止损规则 |
| 下游消费者 | `06_val筛查/00_阶段总协议.md`、`03_screening_manifest_schema.md` | 消费字段、train68/val17、seed3407；当前未放行 |
| 路线/证据 | 路线锁定、研究定标、GlaS/DCAN/Gated-SCNN/TA-Net/DEA-Net/MILD-Net 提取 | 验收不得超出论文/代码证据，也不得使用 test 选择 |

## 路线依据

05 到 06 是“规划协议 → val screening”的单向交接，不是结果交接。GlaS TestA/TestB 与 CRAG test40 不得出现在 `selection_source`，06 当前仍未放行。

## 文献依据

GlaS、DCAN 及边界/融合/watershed 文献只支撑机制候选；未报告参数已在 01—03 标为项目候选。Plan B 只允许未来 val 机制门触发一次 `DCAN-inspired adaptation, non-strict replication`。

## 4. 阶段门控表达式

令 \(G_{N1},G_{N2},G_{N3},G_{schema},G_{research},G_{lock},G_{precheck}\in\{0,1\}\)。N2 被合规删除时定义 \(G_{N2}=1\)。放行条件为：

\[
G_{05\to06}=G_{N1}\land G_{N2}\land G_{N3}\land G_{schema}\land G_{research}\land G_{lock}\land G_{precheck}.
\]

当前 `G_research/G_lock/G_precheck=0 (not_run)`，所以 `G_05_to_06=0`、`gate_status=blocked_not_run`，不得仅因正文写完改为 passed。

## 方法验收清单

- N1：唯一逐实例 target identity；`grad/in/out`、width `{1,2,3}`、小实例三选一、触边、校验和有限 loss 均可枚举；metric identity 分离。
- N2：相对冻结 N1 只变固定层算子；候选仅 `concat+1x1/add/gate`；成本同口径；允许 `n2_decision=deleted`。
- N3：矩阵恰 12 组；threshold、marker、elevation、connectivity、compactness、min area 与异常行为完全定义。
- Plan B：仅 val17 N3 机制门失败后一次，名称与参数冻结，`plan_b_trigger_count∈{0,1}`。
- 证据：论文原文、真实代码、本项目候选、未来验证四层不混写；当前无结果资格。

## 3. 本阶段唯一允许处理的变量

| 字段 | 类型 | 必填/枚举或约束 |
|---|---|---|
| `active_route` | string enum | 必填；仅 `journal` |
| `protocol_version` | non-empty string | 必填；与 source protocol 一致 |
| `method_id` | string enum | `N1_instance_contour_target/N2_region_contour_fusion/N3_contour_guided_watershed/DCAN_inspired_adaptation` |
| `method_parent` | string | 必填；N1=`B1_historical_readonly`，N2=`N1...`，N3=冻结网络身份 |
| `candidate_id` | non-empty string | 必填且由参数唯一决定 |
| `plan_status` | string enum | `planned/locked`；当前 `planned` |
| `execution_status` | string enum | `not_run/running/completed/failed`；当前 `not_run` |
| `result_eligibility` | boolean | 当前 `false` |
| `implementation_permission` | boolean | 当前 `false` |
| `gate_status` | string enum | `blocked_not_run/blocked_invalid/ready_for_consumer/passed/failed`；当前 `blocked_not_run` |
| `target_identity` | string/null | N1/N2 必填；N3 继承输入 identity |
| `metric_identity` | object | Boundary F1 固定 `project_custom_erosion_xor_3x3_ones_8conn_border0_tol3px`；Object F1 primary 固定挑战论文 `overlap/|G_i| >= 0.5`，本地 DCAN `>0.5` 仅 compatibility audit |
| `split_role` | string enum | `planning_only/train68/val17`；当前 `planning_only` |
| `tuning_allowed` | boolean | 当前 `false`；未来仅 val17 为 true |
| `seed` | integer | 固定 `3407`；纯规划可保留该预注册值 |
| `params` | object | 只含 01—03 的封闭字段，禁止自由键调参 |
| `cost_schema` | object | params/FLOPs/latency/device/precision/input shape/digest |
| `selection_rule` | non-empty string enum | `target_hard_gate_then_val_mechanism_stability_cost` |
| `stop_rule` | non-empty string enum | `finite_candidates_then_delete_or_stop_no_test_tuning` |
| `plan_b_trigger_count` | integer enum | `0/1` |
| `blocked_reasons` | array[string] | blocked 时至少 1 项；ready/passed 时必须空 |
| `lineage` | object | 以下七字段全部必填，禁止 null |

### Lineage 七字段类型

| 字段 | 类型 | 枚举/约束 |
|---|---|---|
| `source_stage` | string enum | 仅 `05_方法协议` |
| `source_manifest` | absolute path string | 必须指向 active 根内未来 handoff manifest；当前 planning 实例指向本文件锚点 |
| `source_protocol_version` | non-empty string | 当前 `05-handoff-v2.0-20260719` |
| `source_run_name` | non-empty string | 规划允许 `not_applicable_planning`；运行时不得使用该值 |
| `consumer_stage` | string enum | 仅 `06_val筛查` |
| `consumer_file` | absolute path string | 固定指向 06 screening manifest schema |
| `consumption_boundary` | string enum | `planning_schema_only_blocked/val_screening_only_released`；当前前者 |

## 真实 planning lineage 实例

```yaml
source_stage: 05_方法协议
source_manifest: /home/featurize/work/Paper/结直肠腺体分割_plan_学报投稿版/01_实验执行/05_方法协议/04_验收与handoff_schema.md
source_protocol_version: 05-handoff-v2.0-20260719
source_run_name: not_applicable_planning
consumer_stage: 06_val筛查
consumer_file: /home/featurize/work/Paper/结直肠腺体分割_plan_学报投稿版/01_实验执行/06_val筛查/03_screening_manifest_schema.md
consumption_boundary: planning_schema_only_blocked
```

该实例七字段均具体，但只证明 planning lineage 可解析。由于 `consumer_release=false`，06 不得据此创建 run、训练或读取候选结果。

## 当前 blocked handoff 实例

```yaml
active_route: journal
protocol_version: 05-handoff-v2.0-20260719
plan_status: planned
execution_status: not_run
result_eligibility: false
implementation_permission: false
gate_status: blocked_not_run
split_role: planning_only
tuning_allowed: false
seed: 3407
plan_b_trigger_count: 0
blocked_reasons:
  - research_gate_not_run
  - stage_lock_not_run
  - precheck_gate_not_run
  - consumer_06_not_released
```

## 运行字段与证据资产

未来每个候选还必须携带 `config_digest, code_digest, data_manifest_digest, environment_digest, checkpoint_digest, prediction_digest, metrics_path, cost_path, created_at, completed_at, operator`。规划阶段统一使用 `not_created/not_run`，不得创建空文件冒充证据。计划、config、run_name、run_meta、manifest、gate 与 handoff 任一不一致即 blocked。

## 验收与放行

schema 校验必须验证类型、枚举、绝对路径存在、七字段完整、blocked reason 一致、candidate ID 唯一、N3 行数=12、Plan B 次数≤1。Object F1 还必须验证 primary=`overlap/|G_i| >= 0.5`、compatibility=`>0.5`、恰好 `0.5` 边界单测和 `object_f1_boundary_diff.csv`；当前官方 MATLAB 脚本未验证，不得标记 official parity。只有研究、锁定、Pre-check 与 schema 均真实通过后，才可将 `consumption_boundary` 改为 `val_screening_only_released`；本轮不执行该状态改变。

## 回退条件

任一必填字段缺失/null、路径指向历史根、归档被当 current source、枚举越界、06 文件不匹配、状态互相矛盾或 gate 无证据时，保持/改为 `blocked_invalid` 并回到 05 治理修订。N1 失败回研究定标；N2 可删除；N3/Plan B 失败按 03 收缩；不得绕过 04 直接进入 06。

## 代码落地接口

均为 `planned_not_created`：

- `src/contracts/method_handoff.py::validate_method_handoff(payload: dict) -> dict`；验证字段类型、枚举、七字段和状态一致性。
- `src/contracts/method_handoff.py::validate_lineage(lineage: dict) -> dict`；拒绝 null、历史根和未放行消费边界。
- `src/contracts/method_handoff.py::compute_gate_status(method_reports, governance_reports) -> str`；实现上述布尔公式，不接受人工 passed。
- `src/contracts/method_handoff.py::validate_candidate_budget(payloads) -> dict`；N3 恰 12、Plan B≤1、N2 三算子。

## 冲突裁决记录

1. `consumer_stage=06_val筛查` 只定义目标消费者；当前 `consumer_release=false`，不是放行信号。
2. planning lineage 可用 `source_run_name=not_applicable_planning`，其余字段不得含糊或 null。
3. `source_manifest` 当前指向本文件实例锚点；未来真实 manifest 创建后必须改成其绝对路径并同步 digest。
4. 历史归档 `current_gate_eligible=false`，不可作为 source manifest。

## 文件质量自检

- [x] A 类验收/handoff 身份和四状态明确。
- [x] 依赖按跨阶段消费者角色差异化。
- [x] 路线/文献边界和 Gate 公式完整。
- [x] N1/N2/N3/Plan B 验收逐项明确。
- [x] handoff 字段有类型、枚举和约束。
- [x] 七字段 lineage 有真实具体 planning 实例。
- [x] blocked 状态、原因与 06 未放行一致。
- [x] 运行字段、证据资产、验收和独立回退明确。
- [x] 函数级接口均 `planned_not_created`。
- [x] 冲突、审计和 Diagnostics 独立。

## 审计对表

| 已读证据 | 正文落点 | 自检 | Diagnostics | 缺口/修复 |
|---|---|---|---|---|
| 命名/模板/质检规范 | schema、Gate、接口 | 1、3、5、8—10 | 0项，通过 | 旧稿只有字段名；已类型化 |
| 00—03 同层协议 | 方法验收与预算 | 4、5、8 | 0项，通过 | 规则不可验证；已逐项化 |
| 06 总协议/schema | lineage、consumer 边界 | 2、6、7 | 0项，通过 | 消费者似已放行；已 blocked |
| 路线与文献 | 证据边界 | 3、4 | 0项，通过 | Plan B 身份冲突；已统一 |

## Diagnostics 闭环

已运行逐文件 Markdown diagnostics：0 项。planning lineage 七字段逐项存在且消费者路径检查通过；blocked 实例与 `consumer_release=false` 一致；N3=12、Plan B≤1 的预算检查通过。首轮合并的路线/文献标题已拆分；Gate 仍为 `blocked_not_run`。
