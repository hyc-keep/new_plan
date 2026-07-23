# Experiments Directory

## Current Status

- stage_name: `02_UNet流程验证`
- directory_status: `formal_gpu_a1_completed`
- strict_stage_status: `pass`
- current_truth: `正式单 GPU + AMP A1 已完成，TestA60/TestB20/crosscheck/visuals/error_cases 全部落盘，metric_crosscheck_result=pass，02 阶段严格通过`

## Directory Roles

当前 `experiments/` 目录下的资产需要按身份分开理解，不能把不同运行阶段混成一个“正式 A1”。

### 1. 历史 CPU 主 run

- directory: `experiments/A1_UNet_GlaS_v1_seed3407_cpu_historical_20260707/`
- role: `historical_cpu_connectivity_and_preformal_evidence`
- truthful_interpretation:
  - 该目录保留为真实历史证据。
  - 它证明训练入口、数据读取、训练闭环、测试导出与记录链曾经真实跑通。
  - 但它记录的是 `device: cpu` 与 `amp_active: false`，因此不能继续承担严格规划意义下的最终正式 A1 身份。

### 2. 规范 smoke run

- directory: `experiments/A1_UNet_GlaS_v1_seed3407_smoke/`
- role: `historical_smoke_reference`
- truthful_interpretation:
  - 该目录只用于保留规范 smoke 资产链的历史参照。
  - 它不是当前严格口径下的正式主目录。

### 3. 当前服务器 GPU smoke probe

- directory: `experiments/A1_UNet_GlaS_v1_seed3407_smoke_gpu_probe_20260707/`
- role: `server_gpu_smoke_probe_not_for_table`
- truthful_interpretation:
  - 该目录用于证明服务器侧 `single GPU + AMP + forward/backward/optimizer.step` 已经可执行。
  - 该目录明确是 smoke 目录，不承担正式 A1 最终结果身份。

### 4. 正式 GPU A1 主目录（已完成）

- directory: `experiments/A1_UNet_GlaS_v1_seed3407/`
- role: `formal_gpu_a1_completed`
- truthful_interpretation:
  - 该目录是严格规划意义下的正式主目录，已完整落盘所有必需资产。
  - 训练以 early stopping 在第 70 epoch 正常结束，best epoch 为第 50 epoch。
  - TestA60 / TestB20 推理、评估指标、metric crosscheck、visuals、error_cases 与 run_summary 均已生成。
  - `metric_crosscheck_result: pass`，所有指标 sample_mean 与 aggregate 一致。

## Key Results

正式 A1 的核心指标（`threshold_source: val17`，`threshold_value: 0.5`）：

| split | sample_count | objdice | dice |
|---|---|---|---|
| testA | 60 | 0.6949 | 0.8583 |
| testB | 20 | 0.7510 | 0.8716 |

- `device: cuda`，`amp_active: true`，`smoke_check: false`
- `stop_reason: early_stopping`，`epoch_count: 70`，`best_epoch: 50`
- `best_val_objdice: 0.7515`，`metric_crosscheck_result: pass`

## Stage Verdict

- `02_UNet流程验证`：**严格通过**
- 正式 A1 为单 GPU（`device: cuda`）+ `AMP on`（`amp_active: true`）
- 正式资产链（train / val / test / eval / visual / record）在同一轮 GPU 语义下完整一致
- 下一阶段：**`03_UNet稳定性`**

## Next Required Action

无需重跑。可直接进入 `03_UNet稳定性`。

## Reading Rule

如果你现在只是想判断当前真实状态，请按下面顺序理解：

1. 先看历史 CPU 主 run 归档目录，把它理解为历史联通/前检证据。
2. 再看 `smoke_gpu_probe_20260707`，把它理解为服务器 GPU smoke 已通过的证据。
3. 然后确认 `A1_UNet_GlaS_v1_seed3407/` 是正式 GPU A1 主目录。
4. 再确认 `A2_UNet_GlaS_seed3407/1234/2025/` 是当前正式三 seed 目录，并读取当前 A2 stage summary、raw/mean±std 表和各 run_meta；不要把 crosscheck 的 derived aggregate 当成 per-run CSV 行。
