# 04_CRAG划分协议

## 文档身份与当前状态
A 类 CRAG split 冻结协议。`status=planned`、`split_gate=blocked`、`formal_result=not_run`、`result_eligibility=false`。该协议冻结项目布局，不宣称 universal official split。

## 2. 本轮直接依赖的前置文件（前置依赖）
active 00-07规范；数据协议00、01、02、03、05、06、07；路线02-03；active project 文献证据中的 MILD-Net 与 TA-Net 条目；active project `splits/crag` 和 `src/data` 实际状态。旧协议/旧工程仅作 provenance。

## 1. 文件角色与执行边界（角色边界）
本文件只冻结 CRAG 本地布局的 split、source_subset、schema和盲态，不把本地工程口径冒充 universal official split。

## 前置依赖文件
前置为 active 00-07、数据源/检查协议、路线、MILD-Net/TA-Net证据和 active project 的 CRAG CSV状态。

## 3. 本阶段唯一允许处理的变量（固定参数与变量边界）
固定 train_sup16 union train_unsup137=train153、val20、test40；仅 local layout版本和 digest 可按裁决变更。

## 4. 阶段门控表达式（数据阶段门控/通过线）

合并

## 角色边界
本文件只冻结 CRAG 项目本地布局、source_subset、split 与盲态，不能把项目冻结布局写成 official universal split。

## 前置依赖
输入是经 source 和配对检查登记的 CRAG local layout，必须保留 train_sup、train_unsup、val、test 来源字段。

## 变量或边界
固定 train_sup16 union train_unsup137=train153、val20、test40、local provenance 和 test blind；仅版本与 digest 可变。

## 门控/通过线
subset、数量、互斥性、schema、manifest、hash、config 和 blind 均有真实证据才可 accepted；当前 planned/blocked。

## 上游、同层与下游
- 上游：数据源身份、检查配对、路线和 CRAG benchmark证据。
- 同层：03保证 CSV schema一致，05标签，06资产，07总验收。
- 下游：02-04可消费 train/val；06只在 val选择；08 CRAG验证只在配置冻结后消费 test40；10只读真实结果。

## 路线依据
CRAG是第二 benchmark，固定 `train153/val20/test40`；CRAG test盲态。当前路线仍为 01-11，N1/N2/N3不是阶段。

## 文献依据
MILD-Net、TA-Net支持 CRAG任务身份和对象级比较背景，但未授权当前项目声称全社区唯一 split。因此固定 `split_provenance_type=project_frozen_from_local_layout`、`official_universal_split_claim=false`。

## 固定、可调、禁止参数
- 固定：`train153 = train_sup16 union train_unsup137`；`val20`；`test40`；source_subset必留；test blind。
- 可调：local layout版本、digest、source_subset命名映射，必须升级协议版本并记录裁决。
- 禁止：把 train_unsup137丢失、把 test40加入选择、把本地布局写成 official universal、私自重划或按模型改 split。

## Split与输入/输出 schema
输入：CRAG local layout记录，字段至少 `sample_id,image_relpath,mask_relpath,source_partition,source_subset`，并通过02六步检查。输出：`splits/crag/crag_train153.csv`、`crag_val20.csv`、`crag_test40.csv`、`crag_manifest.json`；每行含 `dataset=CRAG,split,source_subset,blind_state,source_sha256`。消费边界同03：train/val用于开发，test40只用于锁定后正式评估。

## 代码落地接口
- current/existing：`/home/featurize/work/Paper/crc_gland_segmentation_project_journal/splits/crag/*.csv`、`src/data/csv_loader.py`，状态 `existing_unverified`。
- planned_not_created：scripts/build_crag_split.py、configs/data/crag.yaml、splits/crag/crag_manifest.json；目录契约为 splits/crag/。
- historical provenance：旧 project 或旧计划路径不作为 current entry/Gate/downstream。

## 运行记录字段与 lineage
记录 `source_stage/source_manifest/source_protocol_version/source_run_name/consumer_stage/consumer_file/consumption_boundary` 及 `crag_split_protocol_version,split_provenance_type,official_universal_split_claim,train_sup_count,train_unsup_count,train_count,val_count,test_count,source_subset,split_sha256,blind_state,status,formal_result,result_eligibility`。当前使用 `source_run_name=not_run`、manifest `planned_not_created`。

## 验收
检查153=16+137、20、40目标数量、source_subset完整、无sample跨split、CSV schema、manifest/hash、config绑定、test blind。当前无真实检查结果，`pass_split_crag=planned/blocked`，不写实际 pass。

## 独立回退条件
合并池数量不符、source_subset丢失、test进入选择、official claim误写、layout/digest不一致、配置或manifest缺失时，回退到01/02或本文件重建；不得手工修结果表。

## 冲突裁决记录
- CRAG benchmark角色由文献支持，当前 split来源由本项目本地布局冻结；两者不混同。
- active project现存 CSV只作 existing_unverified。
- 旧工程/旧计划不提供 current CRAG split。

## 实施与状态转移
- 输入先保留 `source_subset=train_sup/train_unsup/val/test`，再构造 `train153=train_sup16+train_unsup137`；不得在生成后丢失来源字段。
- 每行 CSV 至少写 `sample_id,image_relpath,mask_relpath,source_partition,source_subset,dataset,split,blind_state,source_sha256`，并生成互斥性检查记录。
- 状态按 `planned_not_created -> existing_unverified -> checked -> accepted` 递进；`official_universal_split_claim=false` 必须随 manifest 传递。
- train153/val20 可供开发，test40 只在配置、selector、threshold 和 postprocess 冻结后正式消费；CRAG test 不参与选择。
- 任何 subset 丢失、数量变化或 test 泄漏都触发回退到 01/02，不得以文献报告数字覆盖当前本地资产事实。

## 字段级验收清单
- 核对 train_sup16、train_unsup137、val20、test40 的 source_subset 均保留且计数可回查。
- 核对 `train153=train_sup16+train_unsup137`，不把 union 结果误写成官方 universal split。
- 核对每行含 `sample_id,image_relpath,mask_relpath,source_partition,source_subset,dataset,split,blind_state,source_sha256`。
- 核对 train153/val20/test40 sample_id 互斥，CRAG test40 标记 blind 且不进入选择证据。
- 核对 `split_provenance_type=project_frozen_from_local_layout` 与 `official_universal_split_claim=false` 随 manifest 传递。
- 核对 config、manifest、CSV 的 protocol_version 和 digest 一致，缺项为 blocked。
- 核对 local layout 变化升级 protocol_version 并保留裁决记录，不直接覆盖旧来源。
- 核对文档 checker 结果只反映文档结构，不改变 CRAG split_gate。
- 核对 train_unsup137 的来源记录不被静默删除或重复计入 train153。

## 复核动作
- 复核 train_sup16、train_unsup137、val20、test40 的来源计数。
- 复核 train153 union 不重复、不丢失 source_subset。
- 复核 test40 blind 与 selector/threshold/postprocess 隔离。
- 复核 local provenance 和 official claim 标记同步。
- 复核 manifest、config、CSV 的 digest 绑定及 blocked 状态。
- 复核未运行事实，不把 checker 结果写成 split 通过。
- 复核 CRAG test40 的标签不进入任何选择、阈值或后处理记录。
- 复核 CRAG 的 local layout 版本、source_subset 和 blind_state 在交接记录中一致。

## 文件质量自检
- [x] train_sup16+train_unsup137、train153/val20/test40、source_subset和盲态已写死。
- [x] `project_frozen_from_local_layout` 与 `official_universal_split_claim=false` 已显式写出。
- [x] 输入/输出 schema、代码状态、lineage、验收、回退、裁决完整。
- [ ] CRAG manifest/hash和真实 Gate尚未运行。

## Diagnostics 闭环
已核对 active `splits/crag` 现存 CSV与接口文件；未发现可证明当前 protocol、layout provenance、manifest/hash已闭环的完整资产，因此正文标记 existing_unverified/planned_not_created。对照模板为 GlaS协议和 active `01_工程目录框架.md`；补齐了 CRAG local provenance和train池合并规则。

## 审计对表
| 已读文件 | 正文落点 | 自检落点 | diagnostics | 当前缺口 | 修复状态 | 对照模板 | 补齐项 |
|---|---|---|---|---|---|---|---|
| active 00-07 | 前置、路线、接口、Gate | 自检1-4 | 已核对 | manifest未建 | 已修状态语义 | active 03_GlaS | CRAG provenance |
| MILD-Net/TA-Net | 文献依据、冲突裁决 | 自检1-2 | 已核对 | 无当前结果 | 已区分 benchmark/split | active 03 | 无 |
| active project crag | schema、Diagnostics | 自检3-4 | existing_unverified | config/hash未绑定 | 已标 blocked | active 01 | 无 |
