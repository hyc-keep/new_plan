# 当前计划可靠性评估、修改建议与 SCI 升级路径

## 文档身份与当前结论

- 归属：A 类，当前路线可靠性与投稿升级裁决；不是结果报告或录用承诺。
- 当前唯一方法路线：`B1（historical_provenance_only） -> N1 -> N2 -> N3`。
- 当前编号路线：`05_方法协议 -> 06_val筛查 -> 07_正式GlaS -> 08_CRAG验证 -> 09_外部对比 -> 10_结果汇总 -> 11_总验收与止损`。
- B1=`valid_with_stability_warning`；N1/N2/N3=`planned/not_run`。formal checker 须以本轮实际变更文档重跑；旧空输入回执不构成 pass，且本文件不预写 research/stage pass。

## 本轮重写直接依赖的前置文件

- 上游：`01_实验执行/00_总览与规范/00-07`，约束 active root、评估、字段、代码和 Gate 语义。
- 同层：路线 01-03、05-06，约束主线、分阶段执行、研究定标和最低证据包。
- 文献：GlaS Challenge、DCAN、MILD-Net、TA-Net、DEA-Net、Gated-SCNN 深提取稿，回答对象评估、轮廓监督、相邻方案和证据边界。
- 下游：`01_实验执行/05_方法协议/00-04` 与 06-11，消费方法身份、blind、handoff、验收与回退。

## 上游、同层与下游

- 上游：全局规范、研究定标、正式参考资料和旧计划差异矩阵，回答协议、证据和历史边界问题。
- 同层：路线总锁定、分阶段标准、投稿止损和最低证据包，分别提供当前主线、执行门、投稿门和资产门。
- 下游：阶段锁定、Pre-check、代码质量、结果汇总和总验收；可靠性评估不能替代这些 Gate。

## 路线与文献依据

当前方案可靠的原因不是预期提升，而是可证伪、可分层和可止损：N1 验证实例轮廓 target，N2 验证区域/轮廓融合，N3 验证轮廓引导实例恢复。每一步只改变一个机制，06 只在 train68/val17 选择，07/08 才消费锁定候选进行 TestA/TestB 与 CRAG test 盲评。

GlaS 论文支持对象级评价和 TestA/TestB 分开报告；Object F1 primary identity 采用挑战论文语义 `overlap/|G_i| >= 0.5`。本地 DCAN 风格 `>0.5` 只作 compatibility audit，要求恰好 `0.5` 的边界单测和差异报告，不声称官方脚本已核验。DCAN 支持 object-contour 联合方向，但不足以支持 strict replication 声明，因此 Plan B 只能称 `DCAN-inspired object-contour joint inference adaptation`。

## 可靠性分解

| 维度 | 当前判断 | 验收证据 | 失败动作 |
|---|---|---|---|
| 协议可靠性 | 有条件成立 | active root、split、评估 identity、七字段一致 | 回治理/研究定标 |
| 方法可解释性 | 有条件成立 | N1/N2/N3 单变量机制证据 | 逐级回退，不扩模块 |
| 评估可引用性 | 待边界单测和差异报告 | Object F1 primary/compatibility 分离 | 不进入主表 |
| 学报可行性 | 待真实结果包 | B1 对照、消融、TestA/TestB、CRAG、失败案例 | 暂不写稿或降低主张 |
| SCI 升级 | 非当前承诺 | 双数据集稳定证据、direct comparison、统计和成本 | 保持学报定位 |

## A/B/C 与差异依赖

- A：路线协议、05 方法协议、06-11 阶段验收，承担当前/未来正式结论。
- B：审计表、模板、manifest、统计脚本和投稿清单，只辅助 A 类，不替代结果。
- C：同时保留旧路线执行建议和当前 N1-N3 指令的混合件；必须先剥离历史部分，未裁决前不得消费。

旧 LKMA/Boundary/Distance 结果及命名只保留真实历史来源，不删除、不重跑、不改写为当前结果；它们不再是当前阶段、当前工程或升级路线。

## 固定、可调与禁止参数

- 固定：active route、B1/N1/N2/N3、GlaS blind 边界、三 seed、metric identity 和投稿结果状态 `not_run/false`。
- 可调：仅在 val 预注册的 candidate budget、direct comparison 复现范围和英文增强项；必须有变更记录。
- 禁止：用测试结果证明路线可靠性、把引用值写成复现值、把 formal checker pass 写成 research/stage pass、因不确定性增加无关模块。

## 运行记录字段

可靠性判断只能读取带 `run_name/stage/status/planned_or_actual/formal_result/result_eligibility/config_digest/code_digest/data_digest/checkpoint_sha256/metric_identity/artifact_manifest/decision/rollback_target` 和七字段 lineage 的证据；当前规划文件保持 `formal_result=not_run`、`result_eligibility=false`。

## 代码落地接口

计划接口均属于 active journal 的 `planned_not_created`；未完成 stage lock、代码质量和运行证据前，不得创建正式运行资产。

## 公式、参数与代码边界

- `F1_obj=2TP/(2TP+FN+FP)`，primary TP 边界为 `>=0.5`。
- N1 contour target、N2 fusion、N3 watershed 参数只在 05 冻结候选边界、06 用 val17 筛选；test 不回调。
- 计划代码接口：`src/data/targets/instance_contour.py`、`src/models/heads/contour_head.py`、`src/models/modules/region_contour_fusion.py`、`src/postprocess/contour_guided_watershed.py`、`src/metrics/object_metrics.py`。
- 未创建接口标 `planned_not_created`；不得由文档把计划状态改写成实现完成。

## 七字段 planning 实例

```yaml
source_stage: s06_val_screening
source_manifest: planned:reports/stage_reports/s06_val_screening_manifest.json
source_protocol_version: val_screening_v1
source_run_name: planned:selected_n1_n2_or_n3
consumer_stage: s07_formal_glas
consumer_file: 01_实验执行/07_正式GlaS/00_阶段总协议.md
consumption_boundary: accepted_val_candidate_only; TestA_TestB_blind_until_lock
```

缺字段、manifest 不可读、hash 不一致、候选未 accepted 或 blind_state 破坏时，07 Gate 必须 blocked。

## 投稿验收与 blind / handoff

学报最低证据包必须包括：B1 lineage、N1-N3 单变量消融、N3 三 seed（若 N3 被选）、TestA/TestB 分开对象级结果、CRAG test、外部 direct comparison、失败案例、成本、统计语义和限制。只有 accepted run bundle 可写“结果显示”；planned/not_run 只能写“拟验证”。

SCI 升级只在最低包完整且双数据集机制证据稳定后裁决；不得靠增加无关模块、复用 test 调参或把 CRAG 单次结果夸成广泛泛化。handoff 必须同步 `plan/config/run_name/run_meta/manifest/gate/handoff`、七字段、blind_state、metric identity 和 rollback target。

## 独立回退条件

- 协议、lineage、blind 或 Object F1 identity 不一致：回 pre-check/研究定标。
- N1 target 不成立回 B1；N2 无 val 机制收益回 N1；N3 val 机制失败且排除实现错误后才允许一次 Plan B。
- Plan B 失败回 N2/B1，停止扩展，不恢复旧路线。
- TestA/TestB/CRAG test 参与选择：相关结果作废，回最近未泄漏 manifest。
- 最低证据包不完整：不进入投稿写作；SCI 条件不足：保持学报定位。

## 冲突裁决记录

1. 旧路线可靠性判断与当前路线冲突：旧判断只在历史归档回查，当前正文仅评价 N1-N3。
2. strict DCAN 与证据边界冲突：统一 adaptation + 差异报告。
3. Object F1 `>=0.5` 与本地 `>0.5` 冲突：primary/compatibility 分离。
4. formal pass 与 research/stage pass 冲突：只陈述 formal 事实，不越级。
5. 投稿潜力与实证状态冲突：可靠性是条件判断，不预承诺提升、显著性或录用。

## 审计对表

| 已读文件 | 正文落点 | 自检落点 | Diagnostics | 缺口/修复状态 | 对照模板 | 补齐项 |
|---|---|---|---|---|---|---|
| 规范 00-07 | 身份、字段、评估、回退 | 下表 1-4 | 待实跑 | 已同步 active 口径 | 路线 01 | A/B/C、七字段 |
| 路线 01-06 | 可靠性与投稿门 | 下表 2-5 | 待实跑 | 已移除旧路线当前态 | 路线 03 | blind/handoff |
| GlaS/DCAN 等证据 | 文献与指标裁决 | 下表 3 | 待实跑 | 已修 strict/阈值冲突 | 规范 04 | 单测/差异报告 |
| 05 当前协议 | 接口与逐级回退 | 下表 4-6 | 待实跑 | 未预写 stage pass | 05/00 | planning 实例 |

## 文件质量自检

- [x] A 类身份和差异化上游/同层/下游依赖明确。
- [x] 路线、文献、公式、参数、代码、字段、验收和独立回退可定位。
- [x] A/B/C、七字段 planning、blind/handoff 已写明。
- [x] Object F1 双 identity 和 Plan B adaptation 已裁决。
- [x] 旧根、旧编号、旧路线与旧文献计数不承担当前态。
- [x] 不预写 research/stage pass、结果提升或录用结论。
- [x] 审计对表与同层路线 01/03 模板强度一致。

## Diagnostics 闭环

本轮须运行章节、路径、禁词、lineage、Markdown diagnostics 与适用 formal checker；发现旧路线当前态、strict replication、旧计数口径、状态越级、缺字段或坏路径时先回写本文件。真实命令和结果以本轮最终回执为准。
