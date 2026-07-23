# 我们项目的 GlaS / CRAG 对照主结果表模板

这份文档不是文献综述，也不是结果速查表，而是后续你真正做实验时要持续回填的主结果表工作底稿。

---

## 1. 文档定位

### 1.1 这份文档负责什么

- 把你后续自己的实验结果和文献对照结果放到同一套表头下
- 提前锁死 `GlaS / CRAG` 的最小必报指标，避免后面越做越乱
- 让你在实验过程中持续记录“是否已复现、是否公平对比、是否能进论文主表”

### 1.2 这份文档不负责什么

- 不负责解释单篇论文内容，那是单篇正式深提取稿
- 不负责汇总所有历史文献数字，那是 `05_GlaS_CRAG_主结果数值速查表.md`
- 不负责替代正式实验日志、训练配置记录和消融设计文档

### 1.3 正确使用顺序

1. 先看 `05_GlaS_CRAG_主结果数值速查表.md`，确定要对齐哪些文献方法
2. 再回本文件，把准备纳入主表的方法先列出来
3. 每跑完一个结果，就立刻回填本文件
4. 真正写论文主表时，以本文件为准，而不是临时回忆

---

## 2. 先锁死的规则

### 2.1 主表最低限度必须报什么

- `GlaS`：`F1 / ObjDice / ObjHaus`
- `CRAG`：`F1 / ObjDice / ObjHaus`

### 2.2 补充表建议报什么

- `Dice`
- `IoU / Jaccard`

### 2.3 哪些情况不能直接横比

- `GlaS Part A / Part B` 与 `A/B 平均` 混在一起
- 对象级三指标与纯语义分割 `Dice / IoU` 混在一起
- `zero-shot external test` 与同协议训练测试混在一起
- 只用 benign 子集、自建数据集或早期旧拆分的结果混进主表

### 2.4 哪些列后面不要乱改

- `方法`
- `是否纳入主表`
- `是否公平对比`
- `GlaS / CRAG` 指标列顺序
- `证据出处`

---

## 3. 你现在最适合先纳入的对照方法

### 3.1 主结果表最小集合

- `UNet`
- `ResNet34-U-Net（我们的主 baseline）`
- `DCAN`
- `MILD-Net-RTS`
- `DEA-Net`
- `TA-Net`
- `SDT`

### 3.2 第二批可选扩展

- `Deep Multichannel`
- `Prompted SAM-H`
- `SCAU-Net`（更适合放补充结果表）

### 3.3 我对这些方法的建议定位

| 方法 | 建议定位 | 是否建议首批进入主表 | 理由 |
|------|----------|----------------------|------|
| `UNet` | 最基础外部基线 | `是` | 必须有最基础参照 |
| `ResNet34-U-Net` | 你的主 baseline | `是` | 是你当前路线的起点 |
| `DCAN` | 经典任务内边界锚点 | `是` | 早期 contour-aware 代表 |
| `MILD-Net-RTS` | 强任务内基线 | `是` | `GlaS + CRAG` 都能对齐 |
| `DEA-Net` | 近期任务内强对照 | `是` | 很适合与你的边界增强路线对比 |
| `TA-Net` | topology 强对照 | `是` | 尤其适合 `CRAG` |
| `SDT` | structure / skeleton 强对照 | `是` | 若你要强调结构建模，非常关键 |
| `Deep Multichannel` | 经典多分支补充 | `可选` | 可增强任务内脉络完整性 |
| `Prompted SAM-H` | foundation model 扩展 | `可选` | 不是第一批必须复现 |
| `SCAU-Net` | 语义口径补充对照 | `补充表` | 更适合 `Dice / IoU` 表 |

---

## 4. 主结果表模板

说明：

- 这张表是后续论文主表的工作底稿
- `是否纳入主表` 只允许填：`是 / 否 / 待定`
- `是否已复现` 只允许填：`是 / 否 / 进行中`
- `是否公平对比` 只允许填：`是 / 有条件 / 否`

| 方法 | 类别 | 是否纳入主表 | 是否已复现 | GlaS F1 | GlaS ObjDice | GlaS ObjHaus | CRAG F1 | CRAG ObjDice | CRAG ObjHaus | 是否公平对比 | 证据出处 | 备注 |
|------|------|--------------|------------|---------|--------------|--------------|---------|--------------|--------------|--------------|----------|------|
| `UNet` | `外部基线` | `是` | `否` |  |  |  |  |  |  | `是` | `待填` | 你的最基础基线 |
| `ResNet34-U-Net（我们）` | `主 baseline` | `是` | `否` |  |  |  |  |  |  | `是` | `待填` | 我们自己的起始模型 |
| `DCAN` | `任务内经典` | `是` | `否` |  |  |  |  |  |  | `是` | `03_DCAN.md` | contour-aware 代表 |
| `MILD-Net-RTS` | `任务内强基线` | `是` | `否` |  |  |  |  |  |  | `是` | `04_MILD-Net.md` | `GlaS + CRAG` 强参考 |
| `DEA-Net` | `任务内近期强对照` | `是` | `否` |  |  |  |  |  |  | `是` | `12_DEA-Net.md` | 边界增强路线对照 |
| `TA-Net` | `拓扑路线` | `是` | `否` |  |  |  |  |  |  | `有条件` | `07_TA-Net.md` | `GlaS` 为 A/B 平均口径 |
| `SDT` | `结构表示路线` | `是` | `否` |  |  |  |  |  |  | `是` | `14_SkeletonAwareDT.md` | skeleton-aware 强参考 |
| `Deep Multichannel` | `任务内补充` | `待定` | `否` |  |  |  |  |  |  | `是` | `08_Deep-Multichannel.md` | 是否进入主表后定 |
| `Prompted SAM-H` | `高阶扩展` | `待定` | `否` |  |  |  |  |  |  | `有条件` | `13_SAM-Grade-Prompt.md` | 可放扩展对照 |
| `我们的方法 V1` | `主方法` | `是` | `否` |  |  |  |  |  |  | `是` | `待填` | 第一版主方法 |
| `我们的方法 + LKMA` | `主方法消融` | `待定` | `否` |  |  |  |  |  |  | `是` | `待填` | 大核模块增益 |
| `我们的方法 + Boundary Head` | `主方法消融` | `待定` | `否` |  |  |  |  |  |  | `是` | `待填` | 边界分支增益 |
| `我们的方法 + Distance-aware Loss` | `主方法消融` | `待定` | `否` |  |  |  |  |  |  | `是` | `待填` | loss 增益 |

---

## 5. 补充结果表模板

说明：

- 这张表用来装 `Dice / IoU` 等补充结果
- 更适合承接 `SCAU-Net`、你自己的语义口径结果和补充实验

| 方法 | 是否纳入补充表 | 是否已复现 | GlaS Dice | GlaS IoU/Jaccard | CRAG Dice | CRAG IoU/Jaccard | 证据出处 | 备注 |
|------|----------------|------------|-----------|------------------|-----------|------------------|----------|------|
| `UNet` | `是` | `否` |  |  |  |  | `待填` | 语义口径基础参照 |
| `ResNet34-U-Net（我们）` | `是` | `否` |  |  |  |  | `待填` | 主 baseline |
| `SCAU-Net` | `是` | `否` |  |  |  |  | `10_SCAU-Net.md` | attention 语义口径对照 |
| `我们的方法 V1` | `是` | `否` |  |  |  |  | `待填` | 当前主方法 |
| `我们的方法最佳版` | `是` | `否` |  |  |  |  | `待填` | 最终结果 |

---

## 6. 回填时的固定检查表

每填一行前，先确认下面 6 件事：

1. 指标口径是不是和主表一致
2. `GlaS` 是 `Part A/B` 还是平均
3. `CRAG` 是否是标准 test 口径
4. 是对象级指标还是语义分割指标
5. 数字有没有明确出处
6. 这行是否真的值得放进论文主表

---

## 7. 结果表冻结建议

### 7.1 第一阶段冻结

- 先只冻结：
  - `UNet`
  - `ResNet34-U-Net`
  - `MILD-Net-RTS`
  - `DEA-Net`
  - `TA-Net`
  - `SDT`
  - `我们的方法 V1`

### 7.2 第二阶段再考虑

- 再决定要不要加：
  - `DCAN`
  - `Deep Multichannel`
  - `Prompted SAM-H`

### 7.3 不要一开始就全塞进去

- 主表行数太多会削弱可读性
- 第一版先保证“能跑、能比、能解释”
- 后面写论文时再决定哪些放主文、哪些放补充材料

---

## 当前状态与结果资格

- 文档角色：B 类结果表模板，不是结果报告，不生成指标，不授予投稿准入。
- 当前状态：`planned_only`；所有本项目行固定为 `formal_result=not_run`、`result_eligibility=false`、`是否已复现=否`；不得填入预测值或手工数字。
- 文献行必须标记 `quoted_from_original_paper`，只有通过统一协议重跑并具备 checkpoint、raw、manifest、独立复核的行才允许标记 `reproduced`。
- 当前方法身份应使用 `B1 historical read-only`、`N1`、`N2`、`N3`；旧 `LKMA/Boundary/Distance` 行只能放历史 provenance 或另表，不能冒充当前主线。

## 本轮重写直接依赖的前置文件

- `01_结直肠腺体分割_冻结版论文清单.md`：冻结证据范围和功能层级。
- `02_结直肠腺体分割_具体论文名与库内状态清单.md`：逐篇定位和状态。
- `03_结直肠腺体分割_一次性补全与实验用文献映射.md`：按阶段路由证据。
- `05_GlaS_CRAG_主结果数值速查表.md`：只读文献参考数字。
- `01_实验执行/00_总览与规范/03-06`：结果 schema、评估 identity、证据化写作和代码边界。

## 上游、同层与下游

- 上游：文献索引、正式深提取稿、评估协议和结果命名规范。
- 同层：05 速查表、单篇正式证据文件和计划路线文件。
- 下游：`10_结果汇总`、`11_总验收与止损` 和稿件；只消费 accepted run bundle，不消费本模板空白或引用数字。

## 代码落地接口

本模板对应 active journal 的 `reports/stage_reports/s10_results_summary/`、`scripts/summarize_stage.py` 和 artifact validator；当前正式接入状态以 active project 为准，未创建接口写 `planned_not_created`。本文件不调用训练、测试或预测入口。

## 运行记录字段与 lineage

每个结果行或结果包必须绑定：`run_name/stage/status/planned_or_actual/formal_result/result_eligibility/dataset/split/blind_state/seed/config_digest/code_digest/checkpoint_sha256/metric_identity/artifact_manifest/decision/rollback_target`，以及 `source_stage/source_manifest/source_protocol_version/source_run_name/consumer_stage/consumer_file/consumption_boundary`。缺字段即 `blocked`。

## 独立回退条件

- 结果行无 raw/aggregate 区分、checkpoint、manifest 或独立复核：回退为 `not_run`。
- TestA/TestB/CRAG test 在冻结前被消费：作废整包并回到最近未泄漏阶段。
- 文献协议不等价或来源不清：移出主表，保留在 reference-only 表。
- 发现手工修 CSV、伪造数字或多进程污染：结果包标记 `invalid_contaminated`，不得修数字后继续使用。

## 冲突裁决记录

- 当前路线与旧历史方法冲突：当前表只接受 B1/N1/N2/N3 身份，旧方法移入 provenance。
- primary Object F1 与 compatibility `>0.5` 冲突：主表使用 `>=0.5`，compatibility 另列。
- 结果模板与实际 Gate 冲突：Gate 优先，模板不得反向放行结果。

## 文件质量自检

- [x] 主表和补充表的指标 identity、split 和公平比较边界明确。
- [x] 文献引用值、本项目复现值和未运行状态分离。
- [x] 当前方法身份、三 seed、blind、raw/aggregate 和七字段 lineage 已写明。
- [x] 代码落点、验收、独立回退、冲突裁决和禁止手工改结果已写明。

## Diagnostics 闭环

本轮检查模板列、状态枚举、当前路线身份、文献/复现分离、blind 和 lineage 字段；没有生成任何实验结果。专项检查未通过时本模板保持 `planned_only`，不得用于投稿。

## 审计对表

| 已读文件 | 正文落点 | 自检落点 | Diagnostics | 当前缺口 | 修复状态 |
|---|---|---|---|---|---|
| 01-03 文献索引与映射 | 依赖、证据状态、方法身份 | 文件质量自检 | 待专项实跑 | 单篇证据仍需逐项抽查 | 已补模板边界 |
| 05 速查表 | 文献/reference-only 规则 | 文件质量自检 | 待专项实跑 | 逐行公平性需回原文核验 | 已补消费边界 |
| 01_实验执行/00-07 | schema、lineage、回退 | 文件质量自检 | 待专项实跑 | 结果汇总接口尚未正式接入 | 已标 planned/blocked |

## 一句话版本

> 先锁证据身份和结果 schema，再填数字；在 formal run bundle 被验收前，所有本项目结果都保持 `not_run`。
