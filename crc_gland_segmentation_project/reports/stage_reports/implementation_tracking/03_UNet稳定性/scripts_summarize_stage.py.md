# scripts/summarize_stage.py 怎么看

> 本文档是 `scripts/summarize_stage.py` 的学习型说明文，覆盖 03_UNet稳定性 阶段的多 seed 聚合与验收脚本。
> 这是 A2 阶段独有的脚本（02 阶段无此功能），是整个实验链的**最终收口**。

## 结构化溯源卡片

- 正式对象: `scripts/summarize_stage.py`
- 对应阶段: `03_UNet稳定性`

### 论文依据
- 论文: 本脚本为项目自研聚合逻辑，无直接外部论文对应
- 章节: N/A
- 公式/定义: mean = Σx_i/n, std = √(Σ(x_i-μ)²/n)（population std, n=3）

### 代码依据
- 仓库: project_local（本项目自建，无外部上游）
- 文件: `scripts/summarize_stage.py`
- 许可证: project_internal

### 冻结回链
- 冻结文件: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `connected_components_connectivity`, `boundary_metric_width`, `eval_cast_policy`, `best_selector`, `threshold_source`

### 当前实现落点
- 文件: `scripts/summarize_stage.py`
- 符号: `main_a2()` / `collect_unet_seed_results()` / `aggregate_seed_metrics()` / `validate_unet_stability_stage()` / `_check_proto_consistency()` / `finalize_stage_a2_handoff()`

## 这个脚本的作用

结论先行：这是整个 A2 阶段的**验收总闸**，负责扫描三个 seed 的产物、做协议一致性校验、聚合 mean±std，并判定 A2 能否放行到 04_Baseline。

你可以把它理解成"期末考试的总分计算器"——train.py 是平时作业，test.py 是单元测试，summarize_stage.py 是期末大考。它不单算 mean±std，还要检查所有作业有没有"作弊"（协议不一致）。

它不负责：训练（那是 `scripts/train.py` 的事）、评估（那是 `scripts/test.py` 的事）、模型定义（那是 `src/models/unet.py` 的事）。

## 这个脚本在整个阶段中的位置

结论先行：summarize_stage.py 是三段式实验链的第三段，读上游三 seed 的产物，产出阶段验收所需的聚合表与结论文档。

它的上游依赖有两层：

- 上游依赖 1：三个 seed 的 run_meta.yaml（train.py + test.py 共同写入）
- 上游依赖 2：三个 seed 的 testA/testB 逐样本 CSV（test.py 写入）

它的下游消费者也很明确：

- 下游消费者 1：阶段验收读取本脚本产出的 mean±std 汇总表与 stage_summary 判定放行
- 下游消费者 2：下一阶段 04_Baseline 读取 handoff 标志确认 A2 已交接

用一张流程图说明本脚本在链路中的位置：

```text
experiments/A2_UNet_GlaS_seed{3407,1234,2025}/
    ├── run_meta.yaml          ← train.py + test.py 共同写入
    ├── testA_metrics.csv       ← test.py 写入
    └── testB_metrics.csv       ← test.py 写入
            ↓
scripts/summarize_stage.py  (本文件 — 聚合 3 seed)
            ↓
reports/tables/unet_seed_results.csv       ← 42 行逐 seed 结果
reports/tables/unet_mean_std_summary.csv   ← 14 行 mean±std
reports/stage_reports/unet_stability_stage_summary.md  ← A2 验收结论与交接状态
```

用人话说就是：train.py 造模型 → test.py 检验模型 → summarize_stage.py 汇总结论。

## 当前实现状态

结论先行：正式可用，A2 验收已执行完毕，gate_a2 = pass，非占位壳。

- 状态：正式可用，`reports/tables/unet_mean_std_summary.csv` 等聚合产物均存在
- 当前真实定位：03_UNet稳定性 阶段验收聚合脚本
- 测试覆盖：3 seed 聚合已完成，协议一致性全部通过

你现在可能会问："这个脚本是 A2 新增的，02 阶段为什么没有？"因为 02 阶段只跑单 run 验证流程能跑通，不需要多 seed 聚合；A2 的核心目标才是稳定性，必须有一个把 3 seed 收口的脚本。

## 脚本核心逻辑

### 主要流程

当用 a2 stage 参数启动时，脚本按下面顺序执行：

1. 扫描三 seed 产物（`main_a2` → `_read_run_meta`）：遍历三个实验目录，读每个 run 的 run_meta，记录缺失 seed
2. 协议一致性校验（`_check_proto_consistency`）：比对 10 个协议字段，任一缺失或不一致则 proto_consistent=false，不能放行
3. 收集逐 seed 结果（`collect_unet_seed_results`）：从每个 run 的 testA/testB sample-only CSV 读取 sample 行并按 split×metric 重聚合，产出 42 行 raw seed table
4. 聚合 mean±std（`aggregate_seed_metrics` → `build_mean_std_summary`）：按 split_role×metric_name 分组，算 population mean 与 std，产出 14 行表
5. 写稳定性报告（`write_unet_stability_note`）：输出每个 split 的 mean±std 数值
6. A2 验收判定（`validate_unet_stability_stage`）：gate_a2 的基础条件 = complete_runs ∧ proto_consistent ∧ raw_results_ready ∧ failure_summary_ready；最终 stage_pass_a2 还必须满足 blockers_resolved。mean±std 是独立派生统计层。
7. 写正式总结（`finalize_stage_a2_handoff`）：输出 stage_summary 与 blockers 文档

### 关键函数：`_check_proto_consistency()` — 协议一致性校验

这是整个 A2 验收最关键的检查——三次 run 的协议字段必须完全一样。

为什么这么严格？因为如果 seed=3407 用 float32_before_threshold、seed=1234 用 float32_after_threshold，那两次指标根本不能比较。算出来的 std 不是"随机种子的波动"，而是"评估口径的漂移"，稳定性结论就失去意义。

> 溯源锚点：
> - 理论依据：阶段总协议 §8.1 要求所有 run 的协议字段完全一致
> - 冻结表对应：参数冻结总表中 eval 相关字段
> - 当前实现：`scripts/summarize_stage.py` → `_check_proto_consistency()` L325-357

### 关键函数：`collect_unet_seed_results()` — 逐 seed 结果收集

这是汇总层——把三个 run 的 sample-only per-seed 结果汇成统一 raw seed table，再由同一批 raw 行生成 mean±std 表。字段含 run_name, stage, dataset, model_name, config_version, seed, split_role, metric_name, metric_value, best_selector, threshold_source, threshold_value, checkpoint_path, result_tag 等。当前 raw 表为 42 行，聚合表为 14 行。

你现在可能会问："为什么 raw table 上每行都重复写协议字段？"因为这是可审计性的代价——如果未来某个 seed 的 checkpoint 损坏，你要从 CSV 就能直接看到当时跑的协议是什么。协议字段在 run_meta、逐 run CSV 和汇总表中重复落盘，不是为了好看，而是为了防丢失。

> 溯源锚点：
> - 理论依据：阶段总协议 §8.1 的 raw/aggregate 汇总要求；当前实现从 sample-only per-run CSV 重聚合
> - 冻结表对应：参数冻结总表全字段
> - 当前实现：`scripts/summarize_stage.py` → `collect_unet_seed_results()`；读取 sample-only CSV 后按 split×metric 重聚合

### 为什么这样设计（候选方案对比）

| 候选方案 | 看起来的好处 | 实际问题 | 最终决策 |
|---|---|---|---|
| 用 sample std（除以 n-1） | 符合常见统计推断习惯 | n=3 时显著放大波动，给出虚高不确定性 | 为什么不用：否决 |
| 聚合前不做协议一致性校验 | 流程更短 | 口径漂移被当成 seed 波动，稳定性结论不可信 | 为什么不选：否决 |
| population std + 协议一致性校验前置 | 诚实报告 3 run 内部离差，先卡口径 | 需要额外比对 10 个字段 | 最终决策：采用 |

选 population std 的理由：n=3 时诚实报告"当前这三 run 的内部离差有多大"，而不是用 sample std 假装有更可靠的统计推断。

## A2 验收的 5 个门

```text
complete_runs:            三个 seed 的 run_meta.yaml 都存在  → true
proto_consistent:         10 个协议字段完全一致              → true
raw_results_ready:        sample-only raw CSV 覆盖 42 行      → true
failure_summary_ready:    稳定性 note 存在                   → true
                        ↓
gate_a2:                  complete_runs ∧ proto_consistent ∧ raw_results_ready ∧ failure_summary_ready → true
meanstd_export_ready:     mean±std 派生 CSV 覆盖 14 个维度    → true（独立派生统计层，不作为 gate_a2 基础条件）
blockers_resolved:        没有协议层面的 blocker              → true
                        ↓
stage_pass_a2:            gate_a2 ∧ blockers_resolved        → true
handoff_ready_for_b1:                                        → true
```

如果你看到 gate_a2 = false，最快的排查顺序是：先查 complete_runs（是不是有 seed 没跑完），再查 proto_consistent（是不是有字段不一致），最后查 raw_results_ready（sample-only CSV 是否生成且覆盖 42 行）。

## A2 阶段新增与变化

相比 02 阶段，summarize_stage.py 是全新脚本，核心增量有三点：

1. 多 seed 聚合能力：02 阶段无此需求，A2 才需要把 3 seed 收口成 mean±std
2. 协议一致性前置卡口：把口径漂移与 seed 波动区分开
3. 汇总层固化：raw 与 mean±std 表重复写协议字段，并以 sample-only per-run CSV 作为可重算输入

## 如何运行这个脚本

环境要求：Python 3.10+，依赖 PyYAML/numpy（纯 CPU 即可，不需要 GPU）。

聚合验收命令：

```bash
cd crc_gland_segmentation_project
python scripts/summarize_stage.py --stage a2
```

运行成功后，reports/tables/ 下会有 unet_seed_results.csv、unet_mean_std_summary.csv、unet_stage_manifest.csv，reports/stage_reports/ 下会有 unet_stability_note.md、unet_stability_stage_summary.md，终端会打印 stage_pass_a2=true。

### 期望输出（文件）

| 文件 | 行数 | 说明 |
|------|------|------|
| `reports/tables/unet_seed_results.csv` | 43（1 header + 42 data） | 3 seed × 2 split × 7 metrics |
| `reports/tables/unet_mean_std_summary.csv` | 15（1 header + 14 data） | 2 split × 7 metrics |
| `reports/stage_reports/unet_stability_note.md` | ~60+ 行 | 稳定性分析与错误模式 |
| `reports/stage_reports/unet_stability_stage_summary.md` | ~30 行 | A2 验收结论与交接状态 |

## 如何验证脚本运行结果

下面三个验证点按顺序执行，可确认 raw table 行数正确、mean±std 数值合理、阶段验收状态为 pass。

### 验证点 1：raw table 行数
- 操作：数 `reports/tables/unet_seed_results.csv` 的行数
- 通过标准：43 行（1 header + 42 data）= 3 seed × 2 split × 7 metrics
- 实际结果：43 行，42 data rows

### 验证点 2：mean±std 数值合理性
- 操作：从当前 `reports/tables/unet_mean_std_summary.csv` 抽查 testA/testB F1 与 Object Dice 的 mean/std
- 通过标准：数值与当前汇总 CSV 一致；std 如实反映三 seed 离散度
- 实际结果：testA F1 mean=0.5290508133298323、std=0.06534870542228736；testB F1 mean=0.5864995222306099、std=0.017711580461373767；testA Object Dice=0.7081049877960447±0.0528843478663972，testB Object Dice=0.7755628763239749±0.01214631192503348。当前结果源为 `reports/tables/unet_mean_std_summary.csv`，当前评估协议为 `eval_proto_v1`；`protocol_v3` 仅作历史追溯，不作当前消费。

### 验证点 3：stage_summary 状态
- 操作：查看 `reports/stage_reports/unet_stability_stage_summary.md` 中的判定行
- 通过标准：stage_pass_a2=true、handoff_ready_for_b1=true
- 实际结果：全部 true

## 误区和排错点

### 误区 1：std 小就是好事

std 小（如 0.005）说明三次 run 稳定，这确实是好事。但如果所有指标 std 都极小（如 0.0001），反而要警惕是不是有地方把不确定性消除了（seed 没真的影响初始化、或三次 run 读到了同一个缓存结果）。

### 误区 2：gate_a2=false 就一定不能进 04_Baseline

严格说是的。但如果 block 原因是 failure_summary_ready_failed（只是没写 error pattern analysis），补上分析后可重新判定；如果是 proto_consistent_failed，那必须回退重跑不一致的那个 run。

### 误区 3：seed 越多越好

3 seed 是 A2 的硬性要求。更多 seed 当然更好，但对于"判断稳定性"这个目标，3 seed 已足够区分抖动的模型（std > 0.03）和稳定的模型（std < 0.01）。

### 协议违规风险

- 不要手动修改 `reports/tables/unet_seed_results.csv` 或 `reports/tables/unet_mean_std_summary.csv`，它们是自动生成物，应由脚本重跑产生
- 不要单独改一个 run 的 run_meta 让 proto_consistent 通过——那会掩盖真正的协议漂移

## 与项目其他部分的关联

- 上游依赖：三个 seed 的 run_meta.yaml 与 testA/testB CSV（由 `scripts/train.py` 和 `scripts/test.py` 写入）
- 下游消费者：阶段验收与下一阶段 04_Baseline handoff
- 比对基准：`configs/eval/eval_proto_v1.yaml`（proto_consistent 的字段来源）

## 阶段协议回链卡片

- 当前阶段总协议: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`
- 三次重复设计: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md`
- 上一阶段放行文件: `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 正式规则文件: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 路线锁定文件: `结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`

## 建议联读

- `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_train.py.md` — 上游训练入口
- `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_test.py.md` — 上游评估入口
- `reports/stage_reports/implementation_tracking/03_UNet稳定性/reports_tables_unet_mean_std_summary.csv.md` — 本脚本产出的聚合表

## 学完后你应该具备什么能力

- 理解 A2 阶段的 5 个 gate 分别检查什么
- 能独立运行聚合脚本并解读终端输出
- 能判断 gate_a2=false 时应从哪里开始排查
- 知道 sample-only per-run CSV、raw seed 表和 mean±std 汇总表之间的关系

### 5 分钟自检任务

- [x] 运行聚合脚本确认 stage_pass_a2=true
- [x] 打开 unet_seed_results.csv 确认有 42 行数据
- [x] 打开 unet_mean_std_summary.csv 确认 testA F1 mean±std 在合理范围
- [x] 说出协议一致性校验包含哪些字段
- [x] 说出 gate_a2 的前置条件：complete_runs、proto_consistent、raw_results_ready、failure_summary_ready、blockers_resolved

## 当前消费口径与审计闭环

当前只聚合三个正式身份 `A2_UNet_GlaS_seed3407`、`A2_UNet_GlaS_seed1234`、`A2_UNet_GlaS_seed2025`，协议为 `eval_proto_v1`；`protocol_v3` 仅作历史追溯。当前精确结果来源 `reports/tables/unet_mean_std_summary.csv`：Object F1 testA=`0.5290508133298323±0.06534870542228736`、testB=`0.5864995222306099±0.017711580461373767`；Object Dice testA=`0.7081049877960447±0.0528843478663972`、testB=`0.7755628763239749±0.01214631192503348`；Pixel Dice testA=`0.8687005312137156±0.014245648618802897`、testB=`0.8785019406751632±0.007950925190263055`；IoU testA=`0.7802676159056027±0.023159000977374777`、testB=`0.7926352354780709±0.009535961930616718`。当前 `stage_pass_a2=true`、`workflow_gate_status=pass`、`handoff_ready_for_b1=true`，不等于 04 自身通过。

`run_stage02_training()` 若在训练说明中出现，是源码历史函数名；当前消费阶段是 A2。直接依赖：三份 run_meta、六份评估 CSV、eval_proto_v1、阶段验收规则和聚合表。冲突裁决：旧 F1/旧协议不得进入当前聚合。回退条件：身份、协议、资产、聚合或 gate 任一失真即 blocked 并重跑对应链路。

## 文件质量自检

- [x] 聚合身份、协议、精确结果和 gate/handoff 边界已明确。
- [x] 接口、依赖、冲突裁决与回退条件可回查。

## Diagnostics 闭环

已扫描本阶段 Markdown 的脚本函数名、协议、身份和旧数字；合法保留项均有历史语境，未发现当前消费残留。

## 审计对表

聚合规则 → 脚本流程；当前 CSV → 精确结果；阶段验收 → gate/handoff；全目录扫描 → diagnostics；缺口：无。

## 版本更新记录

| 日期 | 改动内容 | 影响范围 | 是否需要重新验证 |
|------|---------|---------|----------------|
| 2026-07-10 | A2 阶段首次创建学习型说明文 | 本文档 | 是 |
| 2026-07-10 | 按门禁补齐设计取舍/衔接章节与阶段协议回链卡片，清理无法解析的路径锚点与内联命令 | 本文档 | 是 |
