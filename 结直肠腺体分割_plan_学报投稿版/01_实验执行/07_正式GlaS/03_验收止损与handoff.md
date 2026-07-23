# 07验收、独立复核与07→08/10 handoff

## 1. 文档身份与统一状态
- `active_route: journal`
- `plan_object_class: A`
- `plan_status: planned`
- `execution_status: not_run`
- `result_eligibility: false`
- `implementation_permission: false`
- `current_gate: blocked_not_run`
- 本文件是当前/未来正式阶段协议，不是结果报告；不创建指标、不承诺投稿或录用。

## 2. 本轮重写直接依赖的前置文件
- 上游：`00_总览与规范/00_执行导航.md` 至 `07_实验执行全局修订与质检规范.md`，分别约束唯一路线、工程路径、参数、命名、指标、接口、写作和质检。
- 路线：`02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`、`05_研究定标记录.md`、`06_投稿可行性与最低证据包.md`，约束 `planned/not_run`、有限候选、统计边界与最低证据包。
- 文献：`03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md` 定义 TestA/TestB 与对象三指标；`03_DCAN.md` 仅支持 object-contour 思想；`04_MILD-Net.md` 支持 GlaS/CRAG 与轮廓任务背景，不提供本项目结果。
- 方法：`05_方法协议/00_阶段总协议.md` 至 `04_验收与handoff_schema.md` 冻结 N1/N2/N3、有限预算、target/metric 分离和 lineage。
- 差异化角色依赖：同层00-02；下游08 CRAG、10汇总、11总Gate。
- 相关性说明：验收交接文件，明确双下游消费边界。

## 3. 路线依据与文献依据
- 路线依据：当前唯一编号链为 `05→06→07→08→09→10→11`；本文件位于 `07_正式GlaS`，不得跳阶段或把历史 archive 当 current Gate。
- 文献依据：GlaS Challenge 支持 TestA/TestB 分开及 ObjF1/ObjDice/ObjHaus；DCAN 支持对象/轮廓联合思想但其原训练与推理设置不等于本项目协议；MILD-Net 支持CRAG及轮廓任务动机。
- Plan B身份：统一称 `DCAN-inspired adaptation`，明确是受启发适配，**不是严格复现**；仅由预注册的 N3 val 机制门触发一次。

## 4. 本文件唯一变量与禁止重开项
- 唯一变量：只验收证据完整性和协议一致性。
- 禁止重开：split、Test盲态、对象三主指标、四补充指标、Boundary F1 identity、lineage七字段和已冻结方法身份。
- 历史边界：`_historical_archive/20260719_scientific_plan_repair/` 仅作 provenance，不参与 current Gate。

## 5. 核心规则卡片
- 当前结论：独立复核者不得是运行记录唯一作者；核对config/checkpoint/raw/aggregate/blind/lineage hash。
- 规则类型：`官方协议固定项 + 路线层已锁定 + 工程冻结规则`
- 适用阶段：`07_正式GlaS` 及其下游消费者。
- 直接依据：本文件第2-3节所列路线、文献和方法协议。
- 采用原因：保证单变量、盲态、公平、可追溯和有限预算。
- 不采用的相邻方案：测试集调参、运行中扩候选、混合协议并表、未注册后处理和无来源数字。
- 核心公式或定义参考：`handoff_ok = seeds_complete ∧ split_separate ∧ raw_linked ∧ blind_ok ∧ review_pass`。
- 代码落点：`scripts/summarize_stage.py::validate_glas_handoff()`；输出分别面向08（方法/config）和10（raw/aggregate）的handoff。
- 运行记录字段：见第7节。
- 验收方式：质量一般可诚实handoff并附warning；证据不完整必须blocked，不用正向阈值伪造Gate。

## 6. 参数边界与 blind 工程阻断
- GlaS筛查：仅 `train68/val17`；06唯一seed为3407。正式GlaS固定三seed `3407/1234/2025`。
- GlaS测试：`TestA60/TestB20` 分开，配置、checkpoint、threshold、后处理锁定前禁止访问。
- CRAG：`train153/val20/test40`；尺度换算只消费train/val，test40禁止反馈。
- 指标：三主 `ObjF1/ObjDice/ObjHaus`；四补充 `Dice/IoU/HD95/BoundaryF1`；Boundary F1=`project_custom_erosion_xor_3x3_ones_8conn_border0_tol3px`，不等于N1 target宽度。
- 工程阻断：dataloader/CLI/config allowlist不向筛查暴露Test路径；访问日志、split role和lock digest不完整即失败关闭。

## 7. planned代码落地接口与运行字段
- 当前接口状态：`planned_not_created`；本文件不声称代码存在或已运行。
- 接口：`scripts/summarize_stage.py::validate_glas_handoff()`；输出分别面向08（方法/config）和10（raw/aggregate）的handoff。
- 公共输入：图像 `B×3×512×512 float32`、mask/实例图 `B×1×512×512 uint8/int32` 或结构化manifest。
- 公共输出：结构化manifest、raw schema、decision/handoff schema；不得输出虚构指标。
- 依赖配置：`config_version,data_proto_version,train_proto_version,eval_proto_version,model_version,loss_version,postprocess_version,best_selector,threshold_source`。
- 必填运行字段：`run_name,status,seed,dataset,split_role,blind_state,config_digest,code_digest,checkpoint_sha256,metric_identity,artifact_manifest,decision,rollback_target` 和第8节七字段lineage。

## 8. 完整planning七字段实例
```yaml
source_stage: 05_方法协议
source_manifest: planned_not_created
source_protocol_version: planned_stage_lock_required
source_run_name: not_applicable_planning
consumer_stage: 07_正式GlaS
consumer_file: 07_正式GlaS/03_验收止损与handoff.md
consumption_boundary: planning_only_no_result_consumption
```
七字段缺一即 `blocked`；配置、run_name、run_meta、manifest、Gate 与 handoff 不同步时回到治理/阶段锁定。

## 9. 验收、独立复核与handoff
- 验收：质量一般可诚实handoff并附warning；证据不完整必须blocked，不用正向阈值伪造Gate。
- 独立复核：由未单独控制该次运行选择的人核对原始路径、hash、blind日志、schema、选择规则和缺失项；复核记录不可由口头结论替代。
- handoff：只传递已验收的冻结身份、配置摘要、manifest路径、warning、missing_items及七字段lineage；任一关键对象缺失即 `blocked`。
- 当前handoff：`blocked_not_run`。

## 10. 独立回退条件
Test泄漏则回到最近未泄漏checkpoint；统计错误回raw；方法机制不成立只收缩主张，不看Test改模型。
- 通用回退：测试泄漏、指标身份漂移、lineage缺失、config/run_meta/manifest/Gate不同步时，结果作废并回到最近未泄漏的阶段。

## 11. 冲突裁决记录
- 冲突对象：旧短稿、旧路线表述、Plan B命名和当前科学计划强度。
- 冲突来源：旧稿仅列状态/schema，且路线文件曾把Plan B写成DCAN严格复现；这与05已冻结的“不是严格复现”和本轮用户要求冲突。
- 裁决结论：当前正文统一采用 `DCAN-inspired adaptation`，保持planned/not_run；archive只读且不进入Gate。
- 裁决理由：真实实现只能按受启发适配声明，避免把未逐项复刻的结构、训练和推理冒充DCAN严格复现。
- 受影响文件：本批06-11现有20份Markdown及其下游manifest消费者。
- 是否需要回流修订：本批内部已统一；若代码或配置仍使用严格复现命名，必须在阶段锁定前修复。
- 代码实现影响：模型注册名、配置字段、表注、manifest identity和写作claim必须同步。

## 12. 审计对表
| 已读证据 | 正文落点 | 自检落点 | diagnostics | 当前缺口 | 修复状态 |
|---|---|---|---|---|---|
| 总览00-07 | 状态、参数、接口、指标、盲态 | 文件质量自检 | 静态检查已通过 | 旧稿过短 | 已整篇重写 |
| 路线02/05/06 | 路线、预算、统计、止损 | 文件质量自检 | 关键词检查已通过 | Plan B旧称冲突 | 已统一为 adaptation |
| GlaS/DCAN/MILD-Net | 指标、数据、方法身份边界 | 文件质量自检 | 路径检查已通过 | 引用/复现易混 | 已显式分层 |
| 05方法协议与06-11 | handoff、lineage、下游消费 | 文件质量自检 | Markdown diagnostics已通过 | 旧稿交接不足 | 已补齐 |

## 13. 文件质量自检
- [x] 已完整读取 `00_总览与规范` 00-07、路线投稿、相关证据、05 全部协议及06-11同层/下游文件。
- [x] 已写明 A 类归属、差异化依赖、路线/文献、定义或公式、参数边界和相邻方案。
- [x] 已写明 planned 接口、I/O、dtype、运行字段、验收、独立回退、blind 与 handoff。
- [x] 已保留 `planned/not_run`，没有生成、推断或占位实验数字。
- [x] 已写明冲突裁决、审计对表、planning 七字段实例和 Diagnostics 闭环。
- [x] 已对照同阶段最近文件的完整收尾强度；本文件未缩减独立回退、自检或 diagnostics。

## 14. Diagnostics 闭环
- 本文件落盘后纳入本批统一静态检查：绝对根路径、阶段关键词、`planned/not_run`、blind、lineage 七字段、Plan B 命名、标题层级和 Markdown diagnostics。
- 通过条件：无新增 Markdown diagnostics；不存在测试集调参、结果数字、旧 active root、严格复现旧称或 archive 进入 current Gate。
- 当前结论：`passed`；本轮编辑器 Markdown diagnostics 为0，路径/状态/关键词/lineage/标题静态检查通过。该结论只放行文档质量，不改变 `planned/not_run` 与实验 Gate。

