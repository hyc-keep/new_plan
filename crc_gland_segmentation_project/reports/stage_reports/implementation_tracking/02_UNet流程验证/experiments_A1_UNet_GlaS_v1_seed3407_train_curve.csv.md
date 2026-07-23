# experiments_A1_UNet_GlaS_v1_seed3407_train_curve.csv.md

> 历史资产说明：本文记录的是旧轮次训练曲线（epoch_count=68），属于历史旧轮次，当前不可消费。当前 A1 唯一结果来源是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`：best_epoch=50、best_metric_value=0.7515312717616618、epoch_count=70、device=cuda、testA_objdice=0.6949207519755126、testB_objdice=0.750951634413634。本文曲线旧值仅供历史追溯。

## 这份文件的定位

这份文档解释的是主 run 的训练曲线表 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/curves/train_curve.csv`。

本文解释的是旧轮次 full run `epoch 1..68` 的训练趋势表，当前不可消费；当前正式训练曲线必须以真实 `train_log.csv`、`curves/train_curve.csv` 和 `run_meta.yaml` 为准。它由 `train_log.csv` 提炼而来，专门服务训练趋势回看、曲线绘制和阶段总结。

## 一眼先抓住什么

- 本文对应主 run 旧轮次训练曲线表，当前不可消费。
- 本文旧轮次表内共有 `68` 个 epoch 点，从 `1` 连续到 `68`；当前不可消费。
- 当前保留的列是 `epoch`、`epoch_train_loss`、`epoch_loss_bce`、`epoch_loss_dice`、`lr`。
- 历史旧轮次最后一轮是 `epoch=68`，对应 `epoch_train_loss=0.36910491918816285`，`lr=3.90625e-06`；当前不可消费。
- 当前它服务的是趋势阅读，不替代原始训练日志。

## 这个文件是干什么的

这份 `train_curve.csv` 是从 `train_log.csv` 提炼出的轻量训练趋势表。

它把最适合画训练曲线的字段单独整理出来，方便回答:

1. 训练 loss 怎样随 epoch 变化
2. BCE 和 Dice 分量怎样变化
3. 学习率在哪些阶段发生衰减

## 当前真实结果

本文只保留旧轮次字段，当前不可消费；当前 A1 真实结果唯一以 run_meta.yaml 为准。旧轮次字段包括:

- `epoch_count=68`
- `epoch 1`: `epoch_train_loss=1.0170458257198334`, `lr=0.001`
- `epoch 45`: `epoch_train_loss=0.4180636331439018`, `lr=6.25e-05`
- `epoch 48`: `epoch_train_loss=0.3866350580664242`, `lr=3.125e-05`
- `epoch 68`: `epoch_train_loss=0.36910491918816285`, `epoch_loss_bce=0.2372638903119985`, `epoch_loss_dice=0.1318410301909727`, `lr=3.90625e-06`

这说明当前文件记录的是完整长程训练趋势。

## 它和上下游怎么衔接

上游依赖:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/train_log.csv`
2. `../../../../src/engine/trainer.py`

下游消费:

1. 曲线绘制
2. 趋势回看
3. `run_summary.md` 和阶段总结中的训练趋势解释

因此它是训练主表的曲线视图，不是新的训练来源表。

## 对应代码里的真实协议痕迹

关键逻辑有三层:

1. `../../../../src/engine/trainer.py` 在主循环中累计 `train_rows`。
2. 训练结束后，`trainer.py` 把 `train_rows` 导出为 `curves/train_curve.csv`。
3. 结果目录中的曲线表与 `train_log.csv`、`run_meta.yaml`、`run_summary.md` 共同组成主 run 的训练资产链。

## 如何手工验证这个文件的正确性

检查方法:

1. 打开真实 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/curves/train_curve.csv`
2. 确认当前正式曲线 epoch 从 `1` 连续到 `70`
3. 对照真实 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/train_log.csv`
4. 对照 `run_meta.yaml epoch_count=70`，旧轮次 1..68 与旧末轮 lr 仅作历史 provenance

通过标准:

- 当前正式曲线点覆盖应与真实训练日志和 `run_meta.yaml epoch_count=70` 一致
- 当前正式末轮应为 epoch 70
- 当前正式 lr 衰减轨迹与训练日志一致
- 本文旧轮次曲线覆盖 1..68，仅作为历史 provenance

## 这个文件没说明什么

当前文件能证明的是:

1. 主 run 的训练趋势表已经完整落盘。
2. 训练损失与学习率可以被单独回查。
3. 训练曲线资产链已经和 full run 现实对齐。

当前文件不单独替代的是:

1. `train_log.csv` 的完整训练日志
2. `val_curve.csv` / `val_metrics.csv` 的验证趋势
3. `run_summary.md` 的阶段结论

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_train_log.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_val_curve.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_run_summary.md`
- `src_engine_trainer.py.md`

## 学完后你应该具备什么能力

学完后，至少应能回答:

1. 为什么历史 `train_curve.csv` 是旧 full run 的训练趋势表，当前不可消费。
2. 它和 `train_log.csv` 的分工差异是什么。
3. 为什么它适合看趋势，但不替代原始训练日志。
