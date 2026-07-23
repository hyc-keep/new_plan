# experiments_A1_UNet_GlaS_v1_seed3407_val_metrics.csv.md

> 历史资产说明：本文记录的是旧轮次逐轮验证表（best_epoch=48、val_objdice=0.7626771700880477、epoch_count=68），属于历史旧轮次，当前不可消费。当前 A1 唯一结果来源是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`：best_epoch=50、best_metric_value=0.7515312717616618、epoch_count=70、device=cuda、testA_objdice=0.6949207519755126、testB_objdice=0.750951634413634。本文表内旧值仅供历史追溯。

## 这份文件的定位

这份文档解释的是主 run 的验证结果表 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/val_metrics.csv`。

本文记录的是旧轮次的逐轮验证主表，覆盖 `epoch 1..68`，属于历史旧轮次，当前不可消费。当前 A1 的 best 选择、run_meta 字段和阶段判定必须直接回查真实 `run_meta.yaml`。

## 一眼先抓住什么

- 本文对应主 run `A1_UNet_GlaS_v1_seed3407` 的旧轮次 `val_metrics.csv` 说明；当前不可消费。
- 本文旧轮次是 `smoke_check=false` 的 full run，验证记录连续覆盖 `epoch 1..68`，当前不可消费；当前正式覆盖必须以真实 `val_metrics.csv` 和 `run_meta.yaml epoch_count=70` 为准。
- 本文旧轮次表内共有 `68` 行 epoch 结果，从 `1` 连续到 `68`；当前不可消费。
- 历史旧轮次最佳验证轮是 `epoch=48`，对应 `val_objdice=0.7626771700880477`；当前不可消费。
- 历史旧轮次最后一轮是 `epoch=68`，对应 `val_objdice=0.7340940301447756`；当前不可消费。
- 当前表头同时保留 loss、pixel、boundary 和 object distance 四组指标。
- 当前文件已经足够支撑 `pass_val=true`，但它本身不替代 `TestA60/TestB20` 的正式测试资产。

## 这个文件是干什么的

这份 `val_metrics.csv` 是主 run 的逐轮验证成绩单。

它负责记录每个 epoch 的正式验证输出，包括:

1. 验证 loss
2. pixel/object 主指标
3. boundary 指标
4. object distance 指标

如果没有这张表，就无法审计:

1. 当前正式 `best_epoch=50` 是怎样从真实验证表得出的；旧 `best_epoch=48` 仅属历史轮次
2. 当前 `best.ckpt` 为什么应该指向 `epoch 50`（当前真实 checkpoint）
3. 当前 `last.ckpt=epoch 70` 与最佳轮为何可以不同
4. 验证链是否真的完整跑完并持续写表

## 当前真实结果

## 历史旧轮次记录

以下字段均属于历史旧轮次，当前不可消费；当前正式 A1 唯一来源是 run_meta.yaml。历史字段包括:

- 当前总 epoch 数: `68`
- 当前首轮: `epoch=1`
- 本文旧轮次末轮: `epoch=68`；当前不可消费
- 历史旧轮次最佳轮: `epoch=48`（当前不可消费）
- 历史旧轮次最佳 `val_objdice`: `0.7626771700880477`（当前不可消费）
- 历史旧轮次最后一轮 `val_objdice`: `0.7340940301447756`（当前不可消费）
- 历史旧轮次 `epoch 48` 的关键字段:
  - `val_loss=0.5105387204223208`
  - `val_loss_bce=0.2922302318943871`
  - `val_loss_dice=0.2183084918393029`
  - `val_objdice=0.7626771700880477`
  - `val_boundary_f1=0.588072956700251`
  - `val_hd95=74.38899973140042`
  - `val_object_hausdorff=112.88298861735748`
- 当前 `epoch 68` 的关键字段:
  - `val_loss=0.5386648211214278`
  - `val_loss_bce=0.31687527315484154`
  - `val_loss_dice=0.22178955210579765`
  - `val_objdice=0.7340940301447756`
  - `val_boundary_f1=0.5877693107887435`
  - `val_hd95=97.21606386409086`
  - `val_object_hausdorff=142.529637399756`

这说明本文记录的是历史旧轮次的完整长程验证轨迹，当前不可消费。

## 它和上下游怎么衔接

上游依赖:

1. `../../../../src/eval/run_eval.py`
2. `../../../../src/metrics/seg_metrics.py`
3. `../../../../src/engine/trainer.py`
4. `../../../../configs/eval/eval_proto_v1.yaml`

下游消费:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/best.ckpt`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/last.ckpt`
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md`
5. `../../../../reports/stage_reports/unet_flow_stage_summary.md`

因此它不是孤立结果表，而是 best 选择链和阶段收口链里的核心中间资产。

## 对应代码里的真实协议痕迹

关键逻辑有四层:

1. `../../../../src/eval/run_eval.py` 聚合 `val_loss` 与 segmentation metrics。
2. `../../../../src/metrics/seg_metrics.py` 计算 `objdice`、`dice`、`iou`、`boundary_f1`、`hd95` 等字段。
3. `../../../../src/engine/trainer.py` 每轮把验证结果追加进 `val_metrics.csv`。
4. `../../../../configs/eval/eval_proto_v1.yaml` 冻结 `best_selector=val_objdice_max`、`threshold_value=0.5`、`threshold_source=val17`。

所以当前这些列不是临时拼出来的，它们是评估协议和 trainer 共同产出的正式字段。

## 如何手工验证这个文件的正确性

检查方法:

1. 打开 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/val_metrics.csv`
1. 对照真实 `val_metrics.csv` 的 epoch 覆盖与行数
2. 查真实 `run_meta.yaml` 的 `best_epoch=50` 和 `best_metric_value=0.7515312717616618`
3. 对照真实 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/best.ckpt`
4. 对照真实 `last.ckpt` 与 epoch 70

通过标准:

- 行号覆盖 `1..68`
- 行号覆盖 `1..68`
- 旧说明中的 `best_epoch=48`、`best_metric_value=0.7626771700880477` 与旧 checkpoint 对得上，但整组旧值当前不可消费；当前真实 best_epoch=50、best_metric_value=0.7515312717616618。
- `last.ckpt` 与 `epoch 68` 对得上

## 这个文件没说明什么

- 本文能证明的历史事实是:

1. 旧主 run 的验证主表曾完整落盘。
2. 旧轮次的 `val_objdice`、boundary 和 object distance 指标曾逐轮记录。
3. 当前 `best.ckpt` 的选择依据必须从真实当前验证表、run_meta 和 checkpoint 重新回查。

当前文件不单独替代的是:

1. `train_log.csv` 的训练侧逐轮记录
2. `testA_metrics.csv` / `testB_metrics.csv` 的正式测试结果
3. `metric_crosscheck_note.md` 的 sample/aggregate 对账说明
4. `run_summary.md` / `stage_summary.md` 的阶段收口结论

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_best.ckpt.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_last.ckpt.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_train_log.csv.md`
- `src_eval_run_eval.py.md`

## 学完后你应该具备什么能力

学完后，至少应能回答:

1. 为什么当前 `val_metrics.csv` 是 full run 的逐轮验证主表。
2. 为什么当前 `best_epoch=50` 和 `epoch_count=70` 可以同时成立；旧 48/68 只作为历史版本对照。
3. 为什么 `val_metrics.csv` 必须和 `best.ckpt`、`run_meta.yaml`、`run_summary.md` 保持一致。
