# experiments_A1_UNet_GlaS_v1_seed3407_last.ckpt.md

> 历史资产说明：本文记录的是旧轮次 full-run last checkpoint（epoch=68），属于历史旧轮次，当前不可消费。当前 A1 唯一结果来源是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`：best_epoch=50、best_metric_value=0.7515312717616618、epoch_count=70、device=cuda、testA_objdice=0.6949207519755126、testB_objdice=0.750951634413634。本文旧 checkpoint 仅供历史追溯。

## 这份文件的定位

这份文档解释的是主 run 的最后状态 checkpoint `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/last.ckpt`。

当前它记录的是 full run 实际停表时的最终训练状态。

## 一眼先抓住什么

- 本文旧轮次 `last.ckpt` 说明对应旧 full run 的最后一轮状态，当前不可消费。
- 本文旧轮次最后轮次是 `epoch=68`。
- 本文旧轮次最后的 metric 是 `0.7340940301447756`，当前不可消费
- 它与历史旧轮次说明中的 `epoch_count=68`、`stop_reason=early_stopping` 一致；这些旧值当前不可消费，当前真实 epoch_count=70 以 run_meta.yaml 为准。
- 它和 `best.ckpt` 不同: `last.ckpt` 记录最后停在哪，`best.ckpt` 记录最佳是谁。

## 这个文件是干什么的

它回答的是:

1. 主 run full run 最后停在什么状态
2. 如果要继续恢复最后训练态，应该从哪份 checkpoint 接
3. 最后一轮和最佳轮是否相同

当前正式答案以真实资产为准：

- 当前最后轮是 `70`
- 当前最佳轮是 `50`
- 两者不同，因此当前正式 `last.ckpt` 和 `best.ckpt` 必须并存；本文旧轮次的 68/48 仅用于历史追溯

## 当前真实结果

当前关键事实如下:

- 路径: `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/last.ckpt`
- `epoch=68`
- `metric_value=0.7340940301447756`
- `model_state_dict` 存在
- `optimizer_state_dict` 存在
- `run_meta.yaml` 对应 `epoch_count=68`
- `run_meta.yaml` 对应 `stop_reason=early_stopping`
- `train_log.csv` / `val_metrics.csv` 都已经到 `68`

所以它只代表历史旧 full run 的停训状态，不能代表当前正式停训状态。

## 它和上下游怎么衔接

上游依赖:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/train_log.csv`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/val_metrics.csv`
3. `../../../../src/engine/trainer.py`

下游用途:

1. 训练恢复
2. 训练停表核对
3. 与 `best.ckpt` 做 “最后一轮 vs 最佳一轮” 对账

## 对应代码里的真实协议痕迹

关键逻辑如下:

1. `../../../../src/engine/trainer.py` 每轮验证后都会无条件写 `last.ckpt`。
2. `../../../../src/engine/trainer.py` 保存 `epoch`、`model_state_dict`、`optimizer_state_dict`、`metric_value`。
3. 因此 `last.ckpt` 的语义是 latest training state，不是 best model。

当前正式 GPU full run 已跑到 `70` 并以 `early_stopping` 收尾；本文旧 checkpoint 的 68 轮说明只能用于历史追溯。

## 如何手工验证这个文件的正确性

检查方法:

1. 读取 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/last.ckpt`
2. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/train_log.csv`
3. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/val_metrics.csv`
4. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`

通过标准:

- `epoch=68`
- `metric_value=0.7340940301447756`
- `epoch_count=68`（历史旧轮次，当前不可消费）
- `stop_reason=early_stopping`
- `best_epoch=48`（历史旧轮次，当前不可消费），且与旧 `last.ckpt` 不同轮

## 这个文件没说明什么

本文能证明的历史事实是:

1. 旧 full run 最后一轮状态曾真实落盘。
2. 历史主 run 曾可从最后训练态继续恢复；该历史资产当前不可消费。
3. 当前正式 last checkpoint 必须以真实实体、run_meta、train_log 和 val_metrics 重新核验。
4. 当前正式停表位置与日志和 `run_meta.yaml` 是否一致，必须重新核验真实资产。

当前文件不替代的是:

1. `best.ckpt` 的最佳模型语义
2. `testA_metrics.csv` / `testB_metrics.csv` 的正式测试结果
3. `run_summary.md` / `stage_summary.md` 的阶段收口解释

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_best.ckpt.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_train_log.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_val_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md`

## 学完后你应该具备什么能力

学完后，至少应能回答:

1. 为什么当前正式 `last.ckpt` 应以 epoch=70 的真实实体为准；本文旧 epoch=68 仅作历史追溯。
2. 为什么它不能和 `best.ckpt` 混为一谈。
3. 当前 epoch=70 的 last checkpoint 如何与真实日志和 run_meta 对账；旧 epoch=68 仅用于历史追溯。
