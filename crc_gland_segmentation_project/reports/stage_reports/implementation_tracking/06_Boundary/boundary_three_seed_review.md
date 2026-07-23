# Boundary 三 Seed 结果严格审查

## 1. 审查范围
- 当前阶段: `06_Boundary`
- 当前版本: `boundary_v1`，decoder_final，boundary_width=3，Boundary BCE，lambda=0.3
- 正式 seed: 3407、1234、2025
- 正式 split: TestA60、TestB20
- baseline 对照: B1 `reports/tables/baseline_mean_std.csv` 与 `baseline_per_seed_summary.csv`
- 本文只审查真实产出的 CSV、run_meta、summary、crosscheck 和 B1 表；不修改任何结果文件。

## 2. 资产完整性

| 检查项 | 结果 | 证据 |
|---|---|---|
| 三 seed run_meta | pass | 三个 D1 run 目录的 `run_meta.yaml` |
| best/last checkpoint | pass | 三个 run 的 checkpoints 目录 |
| TestA raw 行数 | pass | 每个 `testA_metrics.csv` 为 60 个 sample 行 |
| TestB raw 行数 | pass | 每个 `testB_metrics.csv` 为 20 个 sample 行 |
| predictions/GT/eval assets | pass | 三个 run 的 TestA/TestB assets |
| metric crosscheck | pass | 三个 `metric_crosscheck_note.md` 均为 `metric_crosscheck_result=pass` |
| checkpoint identity | pass | 三个 `run_meta.yaml` 均为 `checkpoint_identity_status=pass` |
| 训练停止 | pass | 三个 run 均为 early_stopping，best epoch 分别为 38、48、35 |
| 成本记录 | missing | 当前 run_meta/summary 尚无正式 params_m、flops_g、latency_ms 成本表 |
| 三 seed 阶段汇总 | missing | 当前尚无 boundary_per_seed_summary.csv、boundary_mean_std.csv |
| decision note/handoff | missing | 当前尚无 boundary_decision_note.md 和正式 handoff |

## 3. 三 seed 原始聚合结果

| Split | 指标 | Seed 3407 | Seed 1234 | Seed 2025 | Mean | Std |
|---|---|---:|---:|---:|---:|---:|
| TestA | F1 | 0.777928 | 0.790564 | 0.747677 | 0.772056 | 0.022038 |
| TestA | Object Dice | 0.832938 | 0.847117 | 0.833105 | 0.837720 | 0.008138 |
| TestA | Object Hausdorff | 71.187057 | 64.555591 | 72.400852 | 69.381167 | 4.222909 |
| TestA | Dice | 0.916133 | 0.921756 | 0.923431 | 0.920440 | 0.003823 |
| TestA | IoU | 0.851787 | 0.860269 | 0.862426 | 0.858161 | 0.005624 |
| TestA | HD95 | 33.579219 | 33.113328 | 32.398513 | 33.030353 | 0.594710 |
| TestA | Boundary F1 | 0.762933 | 0.770034 | 0.764621 | 0.765863 | 0.003710 |
| TestB | F1 | 0.726145 | 0.735259 | 0.679535 | 0.713646 | 0.029890 |
| TestB | Object Dice | 0.834624 | 0.850691 | 0.820578 | 0.835298 | 0.015068 |
| TestB | Object Hausdorff | 98.114094 | 86.406946 | 100.267179 | 94.929406 | 7.458766 |
| TestB | Dice | 0.920104 | 0.923018 | 0.918322 | 0.920481 | 0.002371 |
| TestB | IoU | 0.859167 | 0.865051 | 0.856505 | 0.860241 | 0.004373 |
| TestB | HD95 | 27.428105 | 27.426637 | 27.074957 | 27.309900 | 0.203468 |
| TestB | Boundary F1 | 0.707440 | 0.723412 | 0.711182 | 0.714011 | 0.008353 |

## 4. 与 B1 三 seed mean 的对比

| Split | 指标 | B1 mean | Boundary mean | Δ | 方向 |
|---|---|---:|---:|---:|---|
| TestA | F1 | 0.749783 | 0.772056 | +0.022273 | higher better |
| TestA | Object Dice | 0.835853 | 0.837720 | +0.001867 | higher better |
| TestA | Object Hausdorff | 67.331024 | 69.381167 | +2.050143 | worse |
| TestA | Dice | 0.916890 | 0.920440 | +0.003550 | higher better |
| TestA | IoU | 0.853529 | 0.858161 | +0.004631 | higher better |
| TestA | HD95 | 33.353000 | 33.030353 | -0.322647 | better |
| TestA | Boundary F1 | 0.761593 | 0.765863 | +0.004270 | higher better |
| TestB | F1 | 0.672565 | 0.713646 | +0.041081 | higher better |
| TestB | Object Dice | 0.822468 | 0.835298 | +0.012829 | higher better |
| TestB | Object Hausdorff | 97.696140 | 94.929406 | -2.766733 | better |
| TestB | Dice | 0.913559 | 0.920481 | +0.006922 | higher better |
| TestB | IoU | 0.849994 | 0.860241 | +0.010247 | higher better |
| TestB | HD95 | 25.699712 | 27.309900 | +1.610187 | worse |
| TestB | Boundary F1 | 0.708971 | 0.714011 | +0.005040 | higher better |

## 5. 逐 seed 退化审查

Boundary 相对同 seed B1 的 delta：

| Split | 指标 | Seed 3407 | Seed 1234 | Seed 2025 |
|---|---|---:|---:|---:|
| TestA Object Dice | +0.004945 | +0.009030 | -0.008375 |
| TestA Boundary F1 | +0.009919 | -0.003335 | +0.006224 |
| TestA Object Hausdorff | +4.602713 | -5.036032 | +6.583748 |
| TestB Object Dice | -0.007636 | +0.041924 | +0.004199 |
| TestB Boundary F1 | -0.003160 | +0.025357 | -0.007076 |
| TestB Object Hausdorff | +8.956180 | -18.196815 | +0.940435 |
| TestA HD95 | +1.477090 | +0.657769 | -3.102800 |
| TestB HD95 | +2.474331 | -2.001808 | +4.358040 |

## 6. 严格科学判断

### 6.1 工程可行性
- 结论: `pass`
- 原因: 三 seed、两个 split、checkpoint、raw CSV、predictions/GT/eval assets、visuals 和独立 metric crosscheck 均完整；没有发现测试失败、样本数缺失或 checkpoint identity 错误。

### 6.2 科学可行性
- 结论: `partial`
- 支持证据:
  - Boundary F1 三 seed mean 在 TestA/TestB 均高于 B1 mean。
  - TestB 的 F1、Object Dice、Object Hausdorff、Dice、IoU 均值改善。
  - TestA 的 F1、Object Dice、Dice、IoU、HD95 均值改善。
- 反向证据:
  - TestA Object Hausdorff 均值变差 `+2.050143`。
  - TestB HD95 均值变差 `+1.610187`。
  - TestA Object Dice 在 seed2025 下降 `-0.008375`。
  - TestB F1、Boundary F1 在 seed2025 分别下降 `-0.009185`、`-0.007076`。
  - 三 seed 结果尚未形成正式 mean/std、成本、案例和 decision/handoff 资产。

### 6.3 是否需要回退
- 当前不需要回退代码、数据、checkpoint 或重新训练。
- 当前必须回退“阶段裁决动作”：禁止直接进入 07_Distance，禁止写 `keep`，禁止把 Boundary 作为已确认主线模块。
- 当前建议决策状态: `backup_pending`，但在正式 protocol 三档输出中，尚不能写最终 `backup`，因为成本表、案例证据、阶段汇总和 decision note 尚未完成。
- 正式下一步起点暂定: `boundary_input_base`，直到 decision_level 正式写为 keep 才允许下游消费 `boundary_kept_base`。

## 7. 结论
- 当前结果不是失败实验，也不是可以直接进入主线的稳定收益证明。
- 最稳妥的科学表述是：BoundaryHead 在固定协议下产生了跨 split 的正向平均趋势，尤其是 TestB 的对象级和 F1 指标，但存在 HD95/TestA Object Hausdorff 冲突、单 seed 退化和完整阶段决策资产缺失，因此当前只能判为“有价值但证据不足以 keep”，待补齐正式汇总、成本和案例证据后裁决为 `backup` 或 `drop`。
- 未经正式 decision note/handoff/workflow gate，不得将本审查文档视为最终阶段结论。
