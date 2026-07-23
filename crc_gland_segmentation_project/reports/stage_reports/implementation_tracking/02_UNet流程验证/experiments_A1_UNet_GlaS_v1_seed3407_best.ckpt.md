# experiments_A1_UNet_GlaS_v1_seed3407_best.ckpt.md

> 历史资产说明：本文记录的是旧轮次 checkpoint 说明（best_epoch=48、val_objdice=0.7626771700880477），属于历史旧轮次，当前不可消费。当前 A1 唯一结果来源是 `experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`：best_epoch=50、best_metric_value=0.7515312717616618、epoch_count=70、device=cuda、testA_objdice=0.6949207519755126、testB_objdice=0.750951634413634。本文旧 checkpoint 语义仅供历史追溯。

## 这份文件的定位

这份文档解释的是主 run 的正式最优 checkpoint `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/best.ckpt`。

本文记录的是旧轮次按 `val_objdice_max` 选出的 checkpoint 快照，属于历史旧轮次，当前不可消费。当前 A1 的 checkpoint 选择和真实 best 字段必须回查 `experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`。

## 一眼先抓住什么

- 本文 `best.ckpt` 对应旧轮次权重，属于历史旧轮次，当前不可消费。
- 历史旧轮次最优轮次是 `epoch=48`，当前不可消费。
- 历史旧轮次指标值是 `metric_value=0.7626771700880477`；当前 A1 真实 best_metric_value=0.7515312717616618。
- 这个历史结果只与旧轮次说明一致，不代表当前 run_meta.yaml 的正式 best。
- 本文旧 checkpoint 不得被后续当前 A1 测试消费；当前测试入口必须按真实 run_meta.yaml 的 best_epoch=50 和 best_checkpoint_path 回查。

## 这个文件是干什么的

它回答的是:

1. 当前 full run 里哪一轮被认定为最佳
2. 最佳模型的参数快照保存在哪里
3. 后续正式测试应该默认加载哪个 checkpoint

本文不能作为当前 A1 推理入口；当前 `TestA/TestB` 推理必须依据真实 run_meta.yaml 的 best_epoch=50 和 best_checkpoint_path 执行。

## 历史旧轮次记录

当前最关键的真实信息是:

- 路径: `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/best.ckpt`
- `epoch=48`
- `metric_value=0.7626771700880477`
- `model_state_dict` 存在
- `optimizer_state_dict` 存在
- 历史旧轮次曾使用这份 checkpoint 导出 `TestA60/TestB20`；该旧测试链当前不可消费

这只说明旧轮次曾把它作为 best 资产保存；当前正式测试必须按真实 run_meta.yaml 的 best_epoch=50 和 best_checkpoint_path 消费。

## 它和上下游怎么衔接

上游依赖:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/val_metrics.csv`
2. `../../../../src/eval/checkpoint_selector.py`
3. `../../../../src/engine/trainer.py`

下游消费:

1. `../../../../scripts/test.py`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/predictions/*`
5. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/*`

## 对应代码里的真实协议痕迹

关键逻辑很清楚:

1. `../../../../src/eval/checkpoint_selector.py` 按 `val_objdice` 决定当前轮是否刷新 best。
2. `../../../../src/engine/trainer.py` 在 `is_best` 为真时写入 `best.ckpt`。
3. `../../../../scripts/test.py` 默认解析 `run_dir/checkpoints/best.ckpt` 作为正式测试入口。

所以现在讨论 `best.ckpt` 时，应直接把它理解成 full run 的正式最佳 checkpoint。

## 如何手工验证这个文件的正确性

检查方法:

1. 读取 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/best.ckpt`
2. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`
3. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/val_metrics.csv`

通过标准:

- 当前正式标准：`epoch=50`
- 当前正式标准：`metric_value=0.7515312717616618`
- 真实 `run_meta.yaml` 中 `best_epoch=50`
- 真实 `run_meta.yaml` 中 `best_checkpoint_epoch=50`
- 本文旧 checkpoint 的 `epoch=48` / `0.7626771700880477` 仅作历史 provenance
- `scripts/test.py` 默认使用这份 checkpoint 成功导出 `TestA60/TestB20`

## 这个文件没说明什么

当前文件能证明的是:

1. full run 最优模型快照已经真实落盘。
2. 正式测试默认消费的最佳模型入口已经成立。
3. 历史主 run 的旧最佳模型入口曾落盘并可回查；当前正式入口必须以真实 run_meta.yaml 为准。

当前文件不单独替代的是:

1. `val_metrics.csv` 的逐轮对比表
2. `last.ckpt` 的最后停轮状态
3. `testA_metrics.csv` / `testB_metrics.csv` 的测试结果
4. `run_summary.md` / `run_meta.yaml` 的收口结论页

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_val_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_last.ckpt.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_run_summary.md`

## 学完后你应该具备什么能力

学完后，至少应能回答:

1. 为什么真实 `best.ckpt` 是当前 full run 的最佳模型入口。
2. 为什么正式测试默认应该加载它，而不是 `last.ckpt`。
3. 当前 `epoch=50` 和 `metric_value=0.7515312717616618` 如何与真实 `run_meta.yaml`、`val_metrics.csv` 对账；旧 48 轮只用于历史追溯。
