# experiments_A1_UNet_GlaS_v1_seed3407_train_log.csv.md

## 这份文件的定位

这份文档解释的是主 run 的训练日志 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/train_log.csv`。

当前它记录的是一次 full run 的完整训练轨迹，是覆盖 `68` 个 epoch 的正式训练表。

## 一眼先抓住什么

- 本文旧轮次训练日志覆盖到 `epoch 68`；该记录当前不可消费。
- 本文旧轮次 `epoch_count=68`，当前不可消费；当前 A1 真实 epoch_count=70 以 run_meta.yaml 为准。
- 本文旧轮次以 `early_stopping` 正常结束；当前正式 run 的停止方式和 epoch_count 必须以真实 run_meta.yaml 为准。
- 日志中旧的半截 `45` 已经清掉，当前 `45` 与 `val 45` 对得上。
- 本文旧轮次表只能支撑历史训练侧追溯；当前正式训练侧验收必须回查真实 70 epoch 资产链。

## 这个文件是干什么的

它负责记录 full run 每一轮训练侧的正式数值，包括:

1. `epoch`
2. `epoch_train_loss`
3. `epoch_loss_bce`
4. `epoch_loss_dice`
5. `lr`
6. `batch_size`
7. `amp`
8. `epoch_time_sec`

如果没有它，就无法审计对应轮次的训练轨迹，也无法核对 `last.ckpt`、学习率衰减和早停位置；当前正式核验必须以真实 70 epoch 日志为准。

## 历史旧轮次记录

本文只记录旧轮次训练现实，属于历史旧轮次，当前不可消费。当前 A1 训练轮数以真实 run_meta.yaml 的 epoch_count=70 为准。

- 历史旧轮次总 epoch 数: `68`（当前不可消费）
- 历史旧轮次最后一轮: `epoch=68`
- 历史旧表内连续记录 `epoch 1..68`，当前不可消费
- 历史旧 `lr` 随 scheduler 衰减到末轮 `3.90625e-06`
- 历史训练轨迹覆盖旧轮次 early stopping 之前的长程过程

当前表中最关键的阶段性事实包括:

- `epoch 48` 对应最佳验证期附近
- `epoch 68` 对应实际停训位置
- 旧的半截 `45` 已删除，只保留与 `val_metrics.csv` 对得上的正式 `45`

## 它和上下游怎么衔接

上游依赖:

1. `../../../../src/engine/trainer.py`

下游消费:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/curves/train_curve.csv`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/last.ckpt`
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`
4. 阶段验收里的 `pass_train`

## 对应代码里的真实协议痕迹

关键逻辑如下:

1. `../../../../src/engine/trainer.py` 每个 epoch 结束后构造 `train_row`
2. 通过 `_append_csv_row(...)` 追加到 `train_log.csv`
3. 训练结束后再把 `train_rows` 重写为 `train_curve.csv`

因此现在讨论这份文件时，应把它理解成旧轮次 full run 的原始训练主表；当前正式主表必须直接读取真实 train_log.csv。

## 如何手工验证这个文件的正确性

检查方法:

1. 打开 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/train_log.csv`
2. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`
3. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/last.ckpt`

通过标准:

- 当前正式标准：真实训练日志应与 run_meta.yaml `epoch_count=70` 和 last checkpoint epoch 70 一致
- 当前正式 `stop_reason=early_stopping`
- 本文旧轮次 `1..68`、旧末轮 68 和旧 scheduler 轨迹仅作历史 provenance

## 这个文件没说明什么

当前文件能证明的是:

1. full run 训练主表已经完整落盘。
2. 历史主 run 的训练侧资产链曾完整落盘；该历史链当前不可消费。
3. 训练侧正式验收所需的逐轮记录已经具备。

当前文件不单独替代的是:

1. `val_metrics.csv` 的验证结果
2. `best.ckpt` / `last.ckpt` 的模型状态
3. `testA_metrics.csv` / `testB_metrics.csv` 的正式测试结果
4. `run_summary.md` / `stage_summary.md` 的收口结论

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_val_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_last.ckpt.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md`
- `src_engine_trainer.py.md`

## 学完后你应该具备什么能力

学完后，至少应能回答:

1. 为什么当前 `train_log.csv` 是 full run 的长程训练主表。
2. 为什么当前正式 `epoch_count=70` 依然可以是正式完成，因为它对应 `early_stopping`；旧 `epoch_count=68` 只属于历史轮次。
3. 为什么清掉旧的重复 `45` 对正式审计一致性是必要的。
