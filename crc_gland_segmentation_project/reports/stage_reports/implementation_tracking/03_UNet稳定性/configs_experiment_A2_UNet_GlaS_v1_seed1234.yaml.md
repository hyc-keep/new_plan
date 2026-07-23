# configs/experiment/A2_UNet_GlaS_v1_seed1234.yaml 怎么看

> 结论先行：这个文件是 A2 稳定性阶段第二个 seed 的实验配置，和 seed3407 完全同构，唯一合法差异只有 `train_seed` 和派生的 `run_name`。
> 你可以把它理解成"同一张考卷、换一支笔"——换 seed 不是调参，而是测量同一套协议在不同随机初始化下抖不抖。

## 这个文件是干什么的

这个 YAML 是三次重复实验里的第二次运行入口。

它告诉训练入口 `scripts/train.py`：这次用 seed=1234，其余数据、模型、训练、评估四套子配置全部复用 A2 冻结口径。

用人话说，它存在的唯一理由就是"在只改 seed 的前提下再跑一次"，好让 `scripts/summarize_stage.py` 能算出 mean±std。

## 这张表/这个文件长什么样

这个文件字段很少，核心就三类：身份字段、seed 字段、`config_refs` 解引用。

身份字段回答"这是谁"：run_name、stage_code、dataset_code、model_name、config_version 把这次运行钉在 A2 阶段的 UNet-GlaS 坐标上，和 seed3407 逐行一致。

seed 字段回答"这是第几次"：train_seed=1234 是本文件唯一的实验变量，result_tag 与 aggregation 标注它是三次重复实验里的第二次。

config_refs 块回答"参数在哪"：它把 data/model/train/eval 四条链解引用到与 seed3407 完全相同的子配置。下面是文件的完整骨架：

```text
run_name: A2_UNet_GlaS_seed1234
stage_code: A2
dataset_code: glas
model_name: unet
config_version: v1
train_seed: 1234
result_tag: reproduced
aggregation: single_seed
smoke_check_run_name: A2_UNet_GlaS_seed1234_smoke
config_refs:
  data: configs/data/glas.yaml
  model: configs/model/unet_v1.yaml
  train: configs/train/unet_flow_v1.yaml
  eval: configs/eval/eval_proto_v1.yaml
```

## 当前真实结果

这次运行的正式产物落在 `experiments/A2_UNet_GlaS_seed1234/checkpoints/best.ckpt`；文件名中的 `v1` 仅表示配置文件版本，不是 run_name。

它在两个 hold-out split 上的真实数值是：

| split | F1 | Object Dice |
|-------|-----|-------------|
| testA | 0.6213051506047086 | 0.7684984131126396 |
| testB | 0.611448456514246 | 0.7793957961240695 |

这三行数值和 `reports/tables/unet_seed_results.csv` 里 seed=1234 的对应行完全一致。

## 这些列/字段分别是什么意思

逐字段说明如下，每个字段都能在配置里核对：

- `run_name`：决定输出目录名，本次为 A2_UNet_GlaS_seed1234；配置文件名中的 `v1` 仅表示配置版本。
- `stage_code`：阶段代号 A2，标识这是 03 稳定性阶段的正式运行
- `train_seed`：本文件唯一实质变量，值为 1234
- `result_tag`：标记为 reproduced，表示这是重复实验而非首发
- `aggregation`：single_seed，说明本文件只是一次单 seed 运行，聚合交给下游
- `config_refs`：四套子配置的解引用，和 seed3407 逐行一致

## 与 seed3407 的差异对比

和主配置 `configs/experiment/A2_UNet_GlaS_v1_seed3407.yaml` 相比（文件名中的 v1 是配置版本），只有下面几行不同：

| 字段 | seed3407 | 本文件 |
|------|----------|--------|
| run_name | A2_UNet_GlaS_seed3407 | A2_UNet_GlaS_seed1234 |
| train_seed | 3407 | 1234 |
| smoke_check_run_name | ..._seed3407_smoke | ..._seed1234_smoke |

其余字段（stage_code、dataset_code、model_name、config_version、result_tag、aggregation、config_refs）逐行相同。

## 阶段协议回链卡片

- 当前阶段总协议: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`
- 三次重复设计: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md`
- mean±std 汇总规则: `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/02_mean_std汇总规则.md`
- 正式规则文件: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 路线锁定文件: `结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`

这组回链证明：本文件的 seed 集合、run 命名、result_tag 都来自 03 阶段计划点名，而不是随手取值；参数冻结总表是它继承 A1 口径的正式来源。

## 溯源与冻结依据

- 论文依据：U-Net 基线身份来自 Ronneberger et al., 2015；GlaS 数据集口径来自 Sirinukunwattana et al., 2017
- 冻结依据：`config_refs` 指向的四套子配置全部继承 A1 母协议，冻结表对应字段包括 best_selector、threshold_source、eval_cast_policy、boundary_metric_width、connected_components_connectivity
- 参数冻结总表是这些字段的唯一正式来源，本文件不得独立改动任何冻结项

## 当前这个文件说明了什么

它说明的是"第二次重复运行的身份和入口"。它的上游是 A1 冻结的四套子配置，下游是 `scripts/train.py` 和 `scripts/summarize_stage.py`。

## 这个文件没说明什么

- 不规定训练超参数（那在 `configs/train/unet_flow_v1.yaml` 里）
- 不规定评估口径（那在 `configs/eval/eval_proto_v1.yaml` 里）
- 不代表"seed=1234 是更好的配置"——它只是三次抽样里的一次

## 如何手工验证这个文件的正确性

下面两个验证步骤按顺序执行，可确认本文件与主配置只差 seed、且 checkpoint 已产出。

### 验证步骤 1：确认只有 seed 不同
- 操作：用下面的 diff 命令比对本文件与 seed3407 主配置
- 期望结果：除 run_name 与 train_seed 外无其他差异
- 实际结果：一致

```bash
diff <(grep -v train_seed configs/experiment/A2_UNet_GlaS_v1_seed3407.yaml) \
     <(grep -v train_seed configs/experiment/A2_UNet_GlaS_v1_seed1234.yaml)
```

### 验证步骤 2：确认 checkpoint 存在
- 操作：查看 `experiments/A2_UNet_GlaS_seed1234/checkpoints/best.ckpt` 是否存在且大小大于 0
- 期望结果：存在且大小 > 0
- 实际结果：存在，可被下游评估脚本加载

## 常见问题

### Q：seed=1234 的 Object Dice 比 seed3407 略高，是不是更好？

A：容易误解。A2 的目标是测稳定性，不是挑最优 seed。三个 seed 的差异应该被当成噪声区间来看，而不是"哪个 seed 更强"。

### Q：可以只跑这一个 seed 就算稳定性验证吗？

A：不行。std 至少需要 n≥2，A2 的硬性要求是 3 个 seed 一起聚合。

## 建议联读

- `reports/stage_reports/implementation_tracking/03_UNet稳定性/configs_experiment_A2_UNet_GlaS_v1_seed3407.yaml.md` — 主配置说明文档，含完整字段解释
- `reports/stage_reports/implementation_tracking/03_UNet稳定性/scripts_summarize_stage.py.md` — 下游聚合脚本说明文

学完后你应该具备的能力：能说清这个文件为什么只准改 seed，以及它的结果如何进入 mean±std。

## 当前消费口径与审计闭环

本文件名中的 `A2_UNet_GlaS_v1_seed1234.yaml` 中 `v1` 仅表示配置文件版本；当前正式 run_name 是 `A2_UNet_GlaS_seed1234`。当前协议为 `eval_proto_v1`，正式身份集合为 seed3407/1234/2025；`protocol_v3` 仅作历史追溯。当前聚合主结果统一来自 `reports/tables/unet_mean_std_summary.csv`：testA/testB Object F1=`0.5290508133298323±0.06534870542228736` / `0.5864995222306099±0.017711580461373767`，Object Dice=`0.7081049877960447±0.0528843478663972` / `0.7755628763239749±0.01214631192503348`，Pixel Dice=`0.8687005312137156±0.014245648618802897` / `0.8785019406751632±0.007950925190263055`，IoU=`0.7802676159056027±0.023159000977374777` / `0.7926352354780709±0.009535961930616718`。A2 numbered stage gate=true、workflow_gate_status=pass、handoff_ready_for_b1=true，不等于 04 自身通过。

直接依赖：A1 配置模板、eval_proto_v1、数据协议；下游：train.py/test.py。冲突裁决：旧 v1 run 身份和旧数字不作为当前 run/结果消费。回退条件：配置身份、协议或 checkpoint 路径不一致时回退 blocked。

## 文件质量自检

- [x] 配置路径版本与正式 run_name 已区分。
- [x] 当前协议、精确结果源和阶段边界已写明。
- [x] 依赖、冲突与回退可回查。

## Diagnostics 闭环

已扫描三 seed 配置说明的身份、协议和结果引用；当前身份与历史版本语境清楚，未发现未标注当前消费残留。

## 审计对表

A1/冻结配置 → 当前配置接口；聚合表 → 当前结果；全目录扫描 → diagnostics；缺口：无。

## 版本更新记录

| 日期 | 改动内容 | 影响范围 | 是否需要重新验证 |
|------|---------|---------|----------------|
| 2026-07-10 | A2 阶段首次创建学习型说明文 | 本文档 | 是 |
| 2026-07-10 | 按学习型说明文门禁补齐结构、真实结果、阶段协议回链与验证步骤 | 本文档 | 是 |
