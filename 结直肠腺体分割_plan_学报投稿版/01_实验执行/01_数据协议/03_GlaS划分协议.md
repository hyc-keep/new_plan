# 03_GlaS划分协议

## 文档身份与当前状态
A 类 GlaS split 冻结协议。`status=planned`、`split_gate=blocked`、`formal_result=not_run`、`result_eligibility=false`。现存 CSV 仅为 `existing_unverified`，不代表本协议已验收。

## 本轮重写直接依赖的前置文件
active 00-07规范；数据协议00、01、02、04、05、06、07；路线02分阶段路线；active project 文献证据中的 GlaS Challenge 与 MILD-Net 条目；active project `splits/glas`、`src/data/csv_loader.py` 状态。旧计划仅作 provenance。

## 1. 文件角色与执行边界（角色边界）
本文件只冻结 GlaS 的四个 split、seed、grade 分层、CSV schema 和测试盲态，不负责标签转换或模型训练。

## 2. 本轮直接依赖的前置文件（前置依赖）
前置为 active 00-07、数据源/检查协议、路线与 GlaS 文献证据，以及 active project 的现存 split 接口。

## 3. 本阶段唯一允许处理的变量（固定参数与变量边界）
固定 official train85 到 train68/val17 的 seed=3407；仅协议版本和 digest 可变，比例、seed、TestA/TestB 身份不可变。

## 4. 阶段门控表达式（数据阶段门控/通过线）
四个 CSV、manifest、schema、hash和 blind 均有真实证据时才可 accepted；当前为 planned/blocked。

## 角色边界
本文件只冻结 GlaS split 与其消费边界，不创建原始数据、不转换标签、不进行模型训练或测试选择。

## 前置依赖
输入必须是经过配对检查的 official train85、TestA60、TestB20 记录，并绑定 source manifest 与协议版本。

## 变量或边界
固定 train68/val17/TestA60/TestB20、split_seed=3407、grade 分层与 sample_id 互斥；仅 digest 和协议版本可变。

## 门控/通过线
四个 CSV、manifest、schema、hash、数量和 blind 证据全部齐全才可 accepted；当前 split_gate=planned/blocked。

## 上游、同层与下游
- 上游：参数冻结、数据源、检查配对协议，提供 official train85、root和检查 Gate。
- 同层：02提供样本资格，04提供 CRAG 对照，05/06/07消费 split 资产并验收。
- 下游：02-04 train/val；06只做 val selector/threshold/postprocess；07才消费 TestA/TestB。

## 路线依据
当前 route 固定 01-11，N1/N2/N3 属于 05。GlaS官方 `train85/TestA60/TestB20`；工程一次性分层冻结 `train68/val17`，seed=3407。TestA/TestB 永远分开且盲态。

## 文献依据
GlaS Challenge提供官方训练/测试身份及对象级评价背景；MILD-Net等任务文献支持 A/B 分开报告。工程 `val17`是项目冻结，不改称官方 split。

## 固定、可调、禁止参数
- 固定：`official_train85 -> train68 + val17`；`TestA60`、`TestB20`原样保留；`split_seed=3407`；grade分层；CSV主键唯一。
- 可调：仅 `glas_split_protocol_version`、digest、预注册 grade字段解释；不得改比例/seed。
- 禁止：train70/val15、5-fold、合并 TestA/TestB、从测试反推划分、不同阶段重新抽样、直接扫描目录。

## Split规则与输入/输出 schema
输入：经过 02 检查的 official train85、TestA60、TestB20 记录，至少有 `sample_id,image_relpath,mask_relpath,source_partition,grade`。输出：`splits/glas/glas_train68.csv`、`glas_val17.csv`、`glas_testA60.csv`、`glas_testB20.csv`、`glas_manifest.json`。每行增加 `dataset=GlaS,split,blind_state,source_sha256`。输出数量是验收目标，不是当前事实。
消费边界：train68用于训练，val17用于 selector/threshold/postprocess，TestA/TestB仅锁定后正式评估，不能反馈任何选择。

## 代码落地接口
- current/existing：`/home/featurize/work/Paper/crc_gland_segmentation_project_journal/splits/glas/*.csv`、`src/data/csv_loader.py`，均需重新绑定 manifest 才可 current consume。
- planned_not_created：scripts/build_glas_split.py、configs/data/glas.yaml、splits/glas/glas_manifest.json；目录契约为 splits/glas/。
- 历史接口路径只作 historical provenance。

## 运行记录字段与 lineage
记录 `source_stage/source_manifest/source_protocol_version/source_run_name/consumer_stage/consumer_file/consumption_boundary` 及 `glas_split_protocol_version,official_train_count,train_count,val_count,testA_count,testB_count,split_seed,grade_rule,split_sha256,blind_state,status,planned_or_actual,formal_result,result_eligibility`。当前 `source_manifest=planned_not_created`、`source_run_name=not_run`。

## 验收
检查目标计数68/17/60/20、grade分层规则、无跨split sample_id、TestA/TestB标签盲态、CSV schema、manifest/hash和config绑定。未实际检查前 `pass_split_glas=planned/blocked`，不得写 pass 或结果数字为事实。

## 独立回退条件
发现数量错误、seed漂移、grade字段丢失、重复/交叉样本、TestA/TestB合并、CSV与manifest不一致、config不存在或测试被选择消费，回退到 02 检查或本文件重建；不得通过手工改CSV掩盖。

## 冲突裁决记录
- 官方 train85 与工程 train68/val17并存：前者保留 benchmark 身份，后者是 project_frozen split。
- active journal root优先于旧 project root。
- 现存 split CSV不是已验收 current asset，必须有当前 manifest/hash。

## 实施与状态转移
- 输入记录先按 `source_partition` 区分 official train85、TestA60、TestB20；只有 train85 允许按 grade 分层抽取 train68/val17。
- 生成 CSV 时逐行写入 `sample_id,image_relpath,mask_relpath,source_partition,grade,dataset,split,blind_state,source_sha256`，并检查 sample_id 互斥。
- split 状态按 `planned_not_created -> existing_unverified -> checked -> accepted` 管理；旧 CSV 不能跳过 manifest/hash 复核。
- val17 只能被 06 用于 selector、threshold、postprocess；TestA/TestB 的标签与统计不得出现在选择记录中。
- 若 seed、grade 分布或数量不符，删除本轮 split 产物并回到 02 的检查输入，不直接编辑 CSV 逃避重建。

## 字段级验收清单
- 核对四个 CSV 的表头完全一致，并包含 `sample_id,image_relpath,mask_relpath,source_partition,grade,dataset,split,blind_state,source_sha256`。
- 核对 official train85 只拆为 train68 与 val17，`split_seed=3407` 固定且 grade 分层记录可回查。
- 核对 TestA60、TestB20 原样保留、互斥且均标记 blind；不能把测试标签写入选择日志。
- 核对 train68、val17、TestA60、TestB20 的 sample_id 交集为空，manifest 与四 CSV digest 一致。
- 核对 val17 的消费者仅为 06 selector/threshold/postprocess；02-04 不读取测试标签。
- 核对现存 CSV 若无 current manifest 仍是 existing_unverified，不得作为 accepted handoff。
- 核对 seed、数量或 grade 失败时按回退条件重建，而不是手改行数。
- 核对本文件的 planned_not_created 脚本和 config 没有被写成已实现接口。
- 核对 formal_result、result_eligibility 和 split_gate 状态没有被 checker 结果覆盖。
- 核对 grade 分层统计使用 train85 输入，不从 TestA/TestB 反推训练划分。

## 复核动作
- 复核四个 CSV 的总计数和 sample_id 互斥表。
- 复核 seed3407 与 grade 分层输入记录。
- 复核 TestA/TestB 盲态和选择日志无测试标签。
- 复核 manifest、config 与 CSV 的 digest 绑定。
- 复核现存 CSV 状态仍为 existing_unverified，未运行不写 accepted。
- 复核 CSV 行数与目标数量只作为验收输入，不冒充当前资产事实。
- 复核 split_seed、grade_rule 和 source_partition 在 run_meta 与 manifest 中一致。

## 文件质量自检
- [x] 四个 split、seed3407、grade分层、盲态和禁止重划已明确。
- [x] 输入/输出 schema、消费者、代码状态、lineage和回退已明确。
- [x] `formal_result=not_run,result_eligibility=false`，未伪造split通过。
- [ ] 当前 split manifest/hash和真实 checker尚未运行。

## Diagnostics 闭环
已读取并核对 active `splits/glas` 的现存 CSV 与 active `csv_loader.py`，但未将其视为通过；规划中的 build/config/manifest未创建，故 Gate保持 blocked。对照模板为 CRAG同层协议与 active `01_工程目录框架.md`；本文件补齐了 TestA/TestB blind、seed3407和 official/project provenance差异。

## 审计对表
| 已读文件 | 正文落点 | 自检落点 | diagnostics | 当前缺口 | 修复状态 | 对照模板 | 补齐项 |
|---|---|---|---|---|---|---|---|
| active 00-07 | 前置、固定项、接口、验收 | 自检1-4 | 已核对 | manifest未建 | 已修 current route | active 01 | split schema |
| GlaS文献/路线 | 路线、文献、split规则 | 自检1 | 已核对 | 无官方脚本新结果 | 已区分 official/project | active 04_CRAG | 无 |
| active project splits | schema、状态、Diagnostics | 自检2-3 | existing_unverified | digest/config未绑定 | 已标 blocked | active 01 | 增加现存/规划区分 |
