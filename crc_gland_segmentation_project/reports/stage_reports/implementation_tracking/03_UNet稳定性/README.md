# 03_UNet稳定性 阅读入口

## 先看结论

- source_stage: `03_UNet稳定性`
- source_manifest: `reports/tables/unet_stage_manifest.csv`（04 handoff 总 manifest）
- source_protocol_version: `eval_proto_v1`
- source_run_name: `A2_UNet_GlaS_seed3407`、`A2_UNet_GlaS_seed1234`、`A2_UNet_GlaS_seed2025`
- consumer_stage: `04_Baseline`
- consumer_file: `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md`
- consumption_boundary: `仅作为冻结 A2 baseline 输入；不得重开 A2 协议或冒充 B1 结果`

- 当前 `03_UNet稳定性` 的编号阶段实验 gate: **pass**
- 这里的 `pass` 指的是: A2 三个当前正式 seed 训练完成、协议一致、结果已聚合为 mean±std、稳定性和错误模式分析已完成。
- 当前 workflow/文档审计仍需完成；在当前身份、历史边界和说明文同步完成前，不把编号阶段 pass 扩写为项目整体允许进入 04。
- 这里的 `pass` 不指: 模型已经是 SOTA、评估覆盖了所有可能的数据集、或者 3-seed 具备统计推断意义（n=3 只能描述内部一致性）。
- 当前真正已经形成闭环的是:
  - 3 个 seed 的完整训练产物（checkpoint, train_log, val_metrics, run_meta）
  - 3 个 seed 的 testA/testB 评估产物（sample-only CSV、同空间的 eval image/GT/prediction PNG、独立 PNG+GT 复核、crosscheck note、visual exports）
  - 汇总层产物（unet_seed_results.csv 42 行, unet_mean_std_summary.csv 14 行, unet_stability_note.md, unet_stability_stage_summary.md）
  - 当前清单内 A 类正式对象的学习型说明文（10+ 篇；不等于目录内所有历史/辅助文件都已成为当前消费对象）

## 一眼看的物理证据

不想翻 CSV 的话，先记住这几个真实落盘数（来源 `reports/tables/unet_mean_std_summary.csv`，`n_runs=3`，`seeds="3407,1234,2025"`）:

| split | F1 mean±std | Object Dice mean±std |
|---|---|---|
| testA | 0.5291 ± 0.0653 | 0.7081 ± 0.0529 |
| testB | 0.5865 ± 0.0177 | 0.7756 ± 0.0121 |

主 seed3407 的训练元数据（`run_meta.yaml`）: `best_epoch=53`、`epoch_count=73`、`best_metric_value=0.7564017193729246`、`stop_reason=early_stopping`、`device=cuda`、`metric_crosscheck_result=pass`。这些是判断"训练真的跑完了、协议校验真的过了"的最小锚点，往下所有当前说明文都围着真实 run_meta 展开。

## 最推荐阅读顺序

请直接按下面顺序读:

1. `implementation_status.md` — 看当前阶段的状态概览和资产清单
2. `scripts_train.py.md` — 理解训练入口和三段式实验链
3. `scripts_test.py.md` — 理解评估入口和三层落盘机制
4. `scripts_summarize_stage.py.md` — 理解多 seed 聚合和 A2 验收门
5. `src_data_datasets.py.md` — 理解数据流的 DataConfig frozen 协议
6. `configs_eval_eval_proto_v1.yaml.md` — 理解评估协议的冻结参数
7. `configs_experiment_A2_UNet_GlaS_v1_seed3407.yaml.md` — 理解实验配置解引用机制
8. `reports_tables_unet_seed_results.csv.md` — 查看原始逐 seed 结果
9. `reports_tables_unet_mean_std_summary.csv.md` — 查看聚合后的 mean±std

## 你现在最该先搞明白的四件事

- **三段式实验链是什么**: train.py → test.py → summarize_stage.py。理解三者的分工（造/检/汇）比看懂每一行代码更重要。
- **证据链为什么重要**: run_meta.yaml → 每个 run 的 sample-only 评估 CSV 与同空间 PNG 资产 → 独立 PNG+GT 指标复核 → reports/tables 的 raw 与 mean±std 汇总表；协议字段在 run_meta、逐 run CSV 和汇总表中重复落盘，防止单点证据丢失。
- **A2 验收的 5 个门**: complete_runs → proto_consistent → raw_results_ready → failure_summary_ready → blockers_resolved → gate_a2。mean±std 是独立统计派生层，不是 per-run aggregate 行；全部条件 pass 后进入 04_Baseline 的 research/stage-lock 前置流程。
- **pixel-level vs object-level 指标的差异**: Dice ~0.87-0.88 表示像素分割尚可，但 Object Dice ~0.71-0.78 表示实例分离仍是主要限制。这是 UNet baseline 的自然限制，也是 04+ 阶段的改进方向。

如果你只有 10 分钟，先读完上面四件事，再打开 `unet_mean_std_summary.csv` 看一眼 mean±std，就基本掌握了 A2 阶段的核心结论。

## 这一版和旧版最重要的区别

03_UNet稳定性（A2）与 02_UNet流程验证（A1）相比：
- A1 只验证了单 seed 训练链路能跑通，A2 验证了三 seed 训练链路在不同 seed 下的稳定性
- A1 没有协议一致性校验和 mean±std 聚合，A2 引入了 `_check_proto_consistency` 和 `summarize_stage.py`
- A2 新增了 3 个实验配置文件（seed3407/1234/2025）和评估协议文件 eval_proto_v1.yaml
- 最重要的是：A2 产生了可被 04_Baseline 依赖的 mean±std 基线数据

## 如果你从 02_UNet流程验证 直接过来

02 阶段验证了"单 seed 训练 + 评估链路跑得通"，03 阶段回答了"这条链路在不同 seed 下有多稳定"。

关键增量：
- 从 1 seed → 3 seed（3407, 1234, 2025）
- 从无协议一致性校验 → `_check_proto_consistency` 跨 10 个字段比对
- 从无 mean±std → `aggregate_seed_metrics` 产出 population mean/std；当前 raw 表按 sample-only CSV 重聚合，不依赖 per-run aggregate 行
- 新增 `summarize_stage.py`（02 阶段不存在此脚本）
- 实验配置文件从 1 个变成 3 个（当前 run_name 为 A2_UNet_GlaS_seed{N}；配置文件名保留 v1 版本标记）

## 后面进入 04_Baseline 前先确认什么

1. `stage_pass_a2 = true` 且 `handoff_ready_for_b1 = true`（已确认）
2. 三个 seed 的 checkpoint 和评估产物全部存在（已确认）
3. `_check_proto_consistency` 无 mismatch（已确认）
4. 你理解为什么 A2 的 mean±std 是 04_Baseline 的"对比基线"——如果在 04 换了数据、模型或评估协议导致指标变了，A2 的 mean±std 就是你判断"变化是有意义的还是噪声"的参照

## 建议联读

- `../reports/stage_reports/unet_stability_stage_summary.md` — A2 验收结论
- `../reports/stage_reports/unet_stability_note.md` — 错误模式分析
- `../reports/tables/unet_mean_std_summary.csv` — mean±std 数据

## 当前 A2 正式口径

- 当前正式身份仅为 `A2_UNet_GlaS_seed3407`、`A2_UNet_GlaS_seed1234`、`A2_UNet_GlaS_seed2025`；配置文件分别为 `A2_UNet_GlaS_v1_seed3407.yaml`、`A2_UNet_GlaS_v1_seed1234.yaml`、`A2_UNet_GlaS_v1_seed2025.yaml`，`v1` 仅是配置路径版本说明，不是 run_name。
- 当前评估协议为 `eval_proto_v1`。`protocol_v3` 仅作历史追溯，不参与当前汇总或 gate。
- 当前精确聚合值（来源 `reports/tables/unet_mean_std_summary.csv`）：testA Object F1=`0.5290508133298323±0.06534870542228736`，testB Object F1=`0.5864995222306099±0.017711580461373767`；testA Object Dice=`0.7081049877960447±0.0528843478663972`，testB Object Dice=`0.7755628763239749±0.01214631192503348`；testA Pixel Dice=`0.8687005312137156±0.014245648618802897`，testB Pixel Dice=`0.8785019406751632±0.007950925190263055`；testA IoU=`0.7802676159056027±0.023159000977374777`，testB IoU=`0.7926352354780709±0.009535961930616718`。
- 当前状态是 A2 numbered stage gate=`true`、`workflow_gate_status=pass`、`handoff_ready_for_b1=true`；这些状态不等于 `04_Baseline` 自身通过。

## 本轮重写直接依赖的前置文件

`00_总览与规范` 全部规范文件、`02_路线与投稿` 相关路线文件、`03_文献证据` 的 GlaS 指标依据、`implementation_status.md`、`scripts_summarize_stage.py.md`、`configs_eval_eval_proto_v1.yaml.md` 与当前聚合结果说明文。它们分别提供写作规则、路线/论文口径、阶段状态、聚合接口、协议字段与真实数值。

## 代码落地接口

训练、评估、聚合链为 `scripts/train.py` → `scripts/test.py` → `scripts/summarize_stage.py`；源码中的 `run_stage02_training()` 是历史函数名，当前消费阶段是 A2，不代表当前执行 02 阶段。

## 冲突裁决记录

旧 F1 高值、把 F1 当 Pixel Dice 的描述均标为历史错误口径，不得当前消费；旧 `A2_UNet_GlaS_v1_seed*` 只保留配置路径版本映射；`protocol_v3` 只保留历史追溯。

## 回退条件

任一正式 seed 产物、协议字段、聚合表、workflow gate 或 handoff 字段失真时，回退为 blocked，重新执行对应评估、聚合与 gate；不手改结果 CSV。

## 文件质量自检

- [x] 当前身份、协议、精确聚合值和阶段边界已写明。
- [x] 历史身份、旧数字、旧协议均标注为不可当前消费。
- [x] 前置文件、代码接口、冲突裁决和回退边界可回查。

## Diagnostics 闭环

当前 03 目录中的历史说明文必须按 `historical_archive_only=true`、`valid_for_current_gate=false` 处理；当前消费入口只认本 README、implementation_status、当前正式对象清单、总 handoff manifest 和当前 workflow gate。

已对本目录当前可见 Markdown 扫描身份、协议、旧数字、gate 与函数名；结果中保留的旧项均有历史或配置版本语境，未发现未标注的当前消费残留。

## 审计对表

已读文件 → README 当前 A2 正式口径/阅读入口；实现依据 → 代码落地接口与冲突裁决；聚合表说明 → 精确主结论；扫描结果 → Diagnostics 闭环；当前缺口：无未标注残留。

## 版本更新记录

| 日期 | 改动内容 | 影响范围 | 是否需要重新验证 |
|------|---------|---------|----------------|
| 2026-07-10 | A2 阶段首次创建 README | 本文档 | 否（仅入口文档） |
