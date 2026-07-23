# GlaS / CRAG 主结果数值速查表

这份文档只做一件事：

> 把后续做实验对比、写结果分析时最常查的 `GlaS / CRAG` 主结果数字汇总到一处，避免每次反复打开多篇正式深提取稿。

---

## 1. 文档定位

### 1.1 这份文档负责什么

- 汇总高频会比较的方法主结果数字
- 标明每个数字来自哪篇正式稿、哪张表、哪一页
- 区分“可以直接横比”和“只能参考、不能硬比”的结果

### 1.2 这份文档不负责什么

- 不替代单篇正式深提取稿中的完整上下文
- 不补写论文里没有明确给出的数值
- 不把不同指标口径硬凑成一张统一排行榜

### 1.3 使用规则

1. 如果你要做 `GlaS / CRAG` 主结果表，优先看 `第 2 节`
2. 如果你要找语义分割口径的 `Dice / Jaccard`，看 `第 3 节`
3. 如果你看到的是不同数据拆分、不同任务或不同指标，先不要直接横比，去看 `第 4 节` 的说明

### 1.4 统一记法

- 本表把 `0.xxx` 统一换写成百分数 `xx.x%`
- `ObjDice` 表示 `object-level Dice`
- `ObjHaus` 表示 `object-level Hausdorff`
- 若原文只给 `Dice / Hausdorff`，则保留原文口径，不强行改写成对象级指标

### 1.5 对我们项目最重要的指标优先级

按你当前路线，后续最值得优先盯住的不是所有数字，而是下面这组：

1. `GlaS`：`F1 / ObjDice / ObjHaus`
2. `CRAG`：`F1 / ObjDice / ObjHaus`
3. 语义口径补充：`Dice / IoU(Jaccard)`

原因：

- 你当前主线是腺体任务，不是纯语义分割 benchmark
- `GlaS` 传统比较最稳的是对象级三指标
- `CRAG` 后续做主表时也更适合优先对齐 `F1 / ObjDice / ObjHaus`
- `Dice / IoU` 仍然有用，但更适合作为补充结果或和通用分割方法对话

---

## 2. 严格优先表：对象级协议下可直接优先比较的结果

说明：

- 这一节优先收录 `GlaS challenge` 三指标或 `CRAG` 任务内常用对象级三指标
- 这些数字最适合后续做腺体任务主表、结果讨论和基线定位

| 方法 | 数据集/拆分 | F1 | ObjDice / Dice | ObjHaus / Haus | 是否可直接放进我们的主结果表 | 对我们项目最有参考价值的指标 | 备注 | 出处 |
|------|-------------|----|----------------|----------------|------------------------------|------------------------------|------|------|
| `DCAN` | `GlaS Part A` | `91.16%` | `89.74%` | `45.42` | `是` | `边界分支最早期强锚点；GlaS 对象级三指标` | `CUMedVision2` 对应 challenge 主结果 | `03_DCAN.md -> challenge tables, p.6-p.8` |
| `DCAN` | `GlaS Part B` | `71.58%` | `78.10%` | `160.35` | `是` | `malignant/困难子集的老锚点` | `CUMedVision2` 对应 challenge 主结果 | `03_DCAN.md -> challenge tables, p.6-p.8` |
| `Deep Multichannel` | `GlaS Test A` | `89.30%` | `90.80%` | `44.13` | `是` | `任务内经典多分支参考，尤其看 ObjDice / Haus` | 多通道融合路线 | `08_Deep-Multichannel.md -> Table III-IV, p.10-p.11` |
| `Deep Multichannel` | `GlaS Test B` | `84.30%` | `83.30%` | `116.82` | `是` | `困难子集下的多通道经典参考` | 多通道融合路线 | `08_Deep-Multichannel.md -> Table III-IV, p.10-p.11` |
| `MILD-Net-RTS` | `GlaS A` | `91.40%` | `91.30%` | `41.54` | `是` | `你当前主线最稳的任务内强基线之一` | `RTS` 后处理版本 | `04_MILD-Net.md -> Table 1/2/3, p.11-p.12` |
| `MILD-Net-RTS` | `GlaS B` | `84.40%` | `83.60%` | `105.89` | `是` | `GlaS 困难子集的主线强基线` | `RTS` 后处理版本 | `04_MILD-Net.md -> Table 1/2/3, p.11-p.12` |
| `MILD-Net-RTS` | `CRAG` | `82.50%` | `87.50%` | `160.14` | `是` | `CRAG 的主线起始对照` | 主线强基线之一 | `04_MILD-Net.md -> Table 1/2/3, p.11-p.12` |
| `TA-Net` | `GlaS` | `90.50%` | `90.20%` | `50.80` | `有条件` | `topology 路线支撑价值高，但 GlaS 为 A/B 平均口径` | 文中为 `Test A/B` 平均口径 | `07_TA-Net.md -> p.6` |
| `TA-Net` | `CRAG` | `84.20%` | `89.30%` | `105.20` | `是` | `CRAG 上 topology 结构先验强锚点，尤其是 ObjHaus` | topology-aware 强参考 | `07_TA-Net.md -> p.6` |
| `DEA-Net` | `GlaS` | `89.30%` | `89.60%` | `60.80` | `是` | `近期任务内边界增强路线的直接对照` | 三项都强，近期任务内方法 | `12_DEA-Net.md -> Table 2, p.3-p.4` |
| `DEA-Net` | `CRAG` | `86.00%` | `89.90%` | `129.40` | `是` | `CRAG 上近期强对照，优先看 F1 / ObjDice` | `F1 / Dice` 最好，但 `Haus` 不是最好 | `12_DEA-Net.md -> Table 2, p.3-p.4` |
| `Prompted SAM-H` | `GlaS Part A` | `92.90%` | `92.10%` | `41.19` | `有条件` | `foundation model 路线是否值得单列对照` | prompted foundation model 路线 | `13_SAM-Grade-Prompt.md -> Table 1-2, p.4` |
| `Prompted SAM-H` | `GlaS Part B` | `84.10%` | `88.10%` | `74.30` | `有条件` | `作为高阶扩展路线参考，不必强制首批复现` | prompted foundation model 路线 | `13_SAM-Grade-Prompt.md -> Table 1-2, p.4` |
| `SDT` | `GlaS Part A` | `93.10%` | `91.90%` | `32.29` | `是` | `如果你要强调 topology / skeleton 表示，这行极有价值；尤其是 Haus` | skeleton-aware distance transform | `14_SkeletonAwareDT.md -> Table 1, p.8` |
| `SDT` | `GlaS Part B` | `86.60%` | `85.10%` | `82.40` | `是` | `困难子集上的 skeleton 表示强参考` | skeleton-aware distance transform | `14_SkeletonAwareDT.md -> Table 1, p.8` |
| `Ours (to be filled)` | `GlaS / CRAG` | `待填` | `待填` | `待填` | `待填` | `后续直接和任务内锚点比较差距` | 结果冻结后再按 `GlaS / CRAG` 正式拆分回填 | `06_我们项目的GlaS_CRAG对照主结果表模板.md` |

### 2.1 当前最适合直接拿来做主表参考的几组

- `GlaS challenge` 经典锚点：`DCAN / MILD-Net-RTS / SDT / Prompted SAM-H`
- `CRAG` 主线强参考：`MILD-Net-RTS / TA-Net / DEA-Net`
- 如果你要强调近期腺体任务路线：优先看 `TA-Net / DEA-Net / SDT`

### 2.2 用这张表时要注意

- `TA-Net` 的 `GlaS` 值是 `Test A/B 平均`，不能直接当成 `Part A` 或 `Part B`
- `DEA-Net` 的 `GlaS / CRAG` 是对象级三指标，但数值写法本身就是百分数
- `Prompted SAM-H` 很强，但它更适合写“foundation model 路线可行”，不应替代全部任务内专用模型的比较
- `Ours` 这一行只是速查占位；正式结果仍优先以 `06` 的主结果表模板持续回填，等最终冻结后再回写这里

### 2.3 我建议你后续主结果表最小先放哪些

如果你下一步要做自己的对比表，最小集合建议是：

- `GlaS`：`DCAN / MILD-Net-RTS / DEA-Net / SDT`
- `CRAG`：`MILD-Net-RTS / TA-Net / DEA-Net`

如果后面你想再加一条“高阶扩展路线”：

- 加 `Prompted SAM-H`

如果你想强调“经典多分支任务内方法也考虑过”：

- 加 `Deep Multichannel`

---

## 3. 补充表：语义分割口径结果

说明：

- 这一节保留对后续实验也有用、但指标口径不是 challenge 对象级三指标的结果
- 更适合写模块有效性、语义分割性能趋势、attention 是否有增益

| 方法 | 数据集 | Dice | Jaccard / IoU | 其他 | 是否建议放进我们的补充结果表 | 对我们项目最有参考价值的指标 | 备注 | 出处 |
|------|--------|------|---------------|------|----------------------------------|------------------------------|------|------|
| `SCAU-Net (SA+CA)` | `GlaS` | `90.63%` | `Jaccard 83.32%` | `RVD 0.0197` | `是` | `Dice / Jaccard`，用于 attention 模块补充对照 | 语义分割口径，不是对象级三指标 | `10_SCAU-Net.md -> 主结果表, p.6-p.7` |
| `SCAU-Net (SA+CA)` | `CRAG` | `91.00%` | `Jaccard 83.81%` | `RVD -0.0074` | `是` | `Dice / Jaccard`，用于 attention 模块补充对照 | 语义分割口径，不是对象级三指标 | `10_SCAU-Net.md -> 主结果表, p.6-p.7` |
| `MAC-Net` | `GlaS` | `81.00%` | `IoU 70.10%` | `Accuracy 80.1%` | `否` | `只看 zero-shot 泛化趋势，不看绝对数值` | `EBHI-Seg` 训练后 zero-shot 到 `GlaS`，只作泛化参考 | `01_MAC-Net.md -> Table 2-3, p.8-p.10` |

### 3.1 这一节怎么用

- 如果后面你的实验主表也只报 `Dice / IoU`，这张表很方便
- 但如果你要对齐 `GlaS challenge` 传统腺体文献，仍应优先回到 `第 2 节`

### 3.2 语义口径里最值得你盯的

- `SCAU-Net`：最值得看 `GlaS / CRAG` 上的 `Dice / Jaccard`
- `MAC-Net`：最值得看的是“跨数据泛化趋势”，不是绝对精度

---

## 4. 不建议直接横比，但值得保留的参考结果

说明：

- 这些论文有价值，但与当前主线的拆分、任务定义或指标口径不完全一致
- 可以写 related work、历史脉络或任务难度差异，别直接塞进主结果总表做一行对一行比较

| 方法 | 数据集/设置 | 结果 | 为什么不建议直接横比 | 出处 |
|------|-------------|------|----------------------|------|
| `Semantic Segmentation + TVS` | `早期 GlaS 版本 Test A` | `F1 68.0%, ObjDice 75.0%, Haus 103.49` | 早期数据总量口径为 `161/16` 版本，不是后续常用主线口径 | `02_Semantic-Segmentation-TVS.md -> Table 1, p.9-p.10` |
| `Semantic Segmentation + TVS` | `早期 GlaS 版本 Test B` | `F1 55.0%, ObjDice 61.0%, Haus 213.58` | 同上 | `02_Semantic-Segmentation-TVS.md -> Table 1, p.9-p.10` |
| `Automatic Mucous Glands` | `Warwick-QU benign subset` | `Dice 92.0%, object Dice 88.0%` | 只用 benign 子集，不是完整 `GlaS` 或 `CRAG` | `11_Automatic-Mucous-Glands.md -> p.7-p.8` |
| `Automatic Mucous Glands` | `PATH-DT-MSU without open glands` | `Dice 78.0%, object Dice 77.0%` | 自建数据集，难度与定义不同 | `11_Automatic-Mucous-Glands.md -> p.7-p.8` |
| `Automatic Mucous Glands` | `PATH-DT-MSU with open glands` | `Dice 77.0%, object Dice 70.0%` | 自建数据集，且 open glands 设置不同 | `11_Automatic-Mucous-Glands.md -> p.7-p.8` |

---

## 5. 后续实验时最实用的用法

### 5.1 如果你要定主结果表

- `GlaS` 优先从 `第 2 节` 选 `DCAN / MILD-Net-RTS / SDT / Prompted SAM-H`
- `CRAG` 优先从 `第 2 节` 选 `MILD-Net-RTS / TA-Net / DEA-Net`

### 5.2 如果你要写“为什么我们的模块合理”

- attention 路线：看 `SCAU-Net`
- topology / structure 路线：看 `TA-Net / SDT`
- boundary-enhanced 路线：看 `DEA-Net`

### 5.3 如果你只想快速查一个锚点数字

- `DCAN, GlaS Part A`：`F1 91.16 / ObjDice 89.74 / ObjHaus 45.42`
- `MILD-Net-RTS, CRAG`：`F1 82.5 / ObjDice 87.5 / ObjHaus 160.14`
- `TA-Net, CRAG`：`F1 84.2 / ObjDice 89.3 / ObjHaus 105.2`
- `DEA-Net, CRAG`：`F1 86.0 / ObjDice 89.9 / ObjHaus 129.4`
- `SDT, GlaS Part A`：`F1 93.1 / Dice 91.9 / Haus 32.29`

### 5.4 我建议你自己的实验最小必报指标

如果你后面想让结果表既稳又不乱，我建议最低限度报：

- `GlaS`：`F1 / ObjDice / ObjHaus`
- `CRAG`：`F1 / ObjDice / ObjHaus`
- 补充表：`Dice / IoU`

如果篇幅不够：

- 主表只保留 `F1 / ObjDice / ObjHaus`
- 把 `Dice / IoU` 放到补充实验或附录

如果后面你要突出边界/结构优势：

- 优先看 `ObjHaus`

如果后面你要突出实例识别能力：

- 优先看 `F1`

如果后面你要突出整体分割重叠质量：

- 优先看 `ObjDice`

---

## 本轮重写直接依赖的前置文件

- `01_结直肠腺体分割_冻结版论文清单.md`、`02_结直肠腺体分割_具体论文名与库内状态清单.md`：确认引用论文 identity。
- `03_结直肠腺体分割_一次性补全与实验用文献映射.md`：确认这些数字的阅读和写作用途。
- 单篇正式深提取稿及原文页码：确认表格、split 和指标定义。
- active `01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`：确认 current metric identity。

## 上游、同层与下游

- 上游：原文、单篇深提取稿和评估规范；同层：文献索引与项目结果模板；下游：related work、结果汇总和投稿表。
- 相关性：本表只提供 reference-only 数字，下游不得把它当作 current run bundle。

## 当前证据状态与禁止消费边界

- 本文件中的数字全部属于 `quoted_from_original_paper` 或 `reference_only`，不是本项目 `reproduced` 结果。
- 不得把本文件数字写入 current journal 的 TestA/TestB/CRAG test 结果、Gate、aggregate 或投稿结论。
- `Ours`、`待填`、空白和任何规划数字均保持 `not_run`，不得补写预测值。
- 直接横比前必须同时核对数据 split、指标 identity、后处理、训练协议和来源页码；不等价时只能写 related-work reference。

## 代码落地接口

本文件只消费正式深提取稿和 `03_文献证据` 索引，不调用训练代码。结果汇总阶段如需使用，必须在 manifest 中记录 `source_stage=s03_literature_evidence`、`source_manifest`、`source_protocol_version`、`source_run_name=reference_only`、`consumer_stage=s10_results_summary`、`consumer_file`、`consumption_boundary=quoted_reference_only_no_current_result`。

## 独立回退条件

若页码、表号、split、指标定义或来源状态无法核验，该行降级为 `unverified` 并从可比较主表移除；不得用相邻论文或旧计划数字替代。若发现本项目结果混入本表，回退到结果汇总前的证据清理并作废受污染表。

## 冲突裁决记录

- 文献数字与本项目数字冲突：以带 checkpoint、raw、manifest 的 `reproduced` 资产为 current；本表仍保持 reference-only。
- GlaS A/B 与 A/B 平均冲突：分开标记，禁止合并。
- Object F1 与 pixel Dice 冲突：保留原始指标 identity，不改名、不换算冒充。

## 文件质量自检

- [x] 所有数字有论文/表格/页码来源或明确标记为待核验。
- [x] 文献值与本项目结果状态分离。
- [x] 不同 split、指标和任务设置未强制横比。
- [x] 已写明代码边界、lineage、验收、回退和冲突裁决。

## Diagnostics 闭环

本轮检查数字来源标记、`Ours/待填` 禁止消费、current route 术语和 lineage；未创建或修改实验结果。若专项检查非 `pass`，本文件保持 `reference_only`，不进入投稿主表。

## 审计对表

| 已读文件 | 正文落点 | 自检落点 | Diagnostics | 当前缺口 | 修复状态 |
|---|---|---|---|---|---|
| 01-04 文献索引与映射 | 当前证据状态、引用规则 | 文件质量自检 | 待专项实跑 | 直接横比需逐行核验 | 已补边界 |
| 01_实验执行/00-07 | 代码、lineage、消费边界 | 文件质量自检 | 待专项实跑 | 不替代 current Gate | 已补边界 |

## 一句话版本

> 本表只提供可追溯的文献参考数字，不提供本项目实验结果；任何 current 结果必须来自正式运行资产。
