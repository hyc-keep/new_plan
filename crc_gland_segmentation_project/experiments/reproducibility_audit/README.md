# 规则冻结声明：规则在正式复现前冻结，复现后只追加结果。

# 01–04 阶段复现审计区

## 目录用途

本目录是当前项目的独立复现审计区，位于：

```text
experiments/reproducibility_audit/
```

它用于验证 01–04 阶段的代码、数据协议、模型、训练、测试和环境是否能够重复得到相同结果。

这里的运行不得覆盖正式结果目录：

```text
experiments/A2_UNet_GlaS_seed3407
experiments/A2_UNet_GlaS_seed1234
experiments/A2_UNet_GlaS_seed2025
experiments/B1_ResNet34_UNet_GlaS_seed3407
experiments/B1_ResNet34_UNet_GlaS_seed1234
experiments/B1_ResNet34_UNet_GlaS_seed2025
```

所有复现 run 必须写入：

```text
experiments/reproducibility_audit/repeat_runs/
```

## 当前结论边界

当前已经完成：

- 当前 A2/B1 canonical 配置统一为 `train_proto_v1` / `eval_proto_v1`；
- 当前 baseline 显式关闭 BN policy、差分学习率、LKMA、Boundary、Distance、TTA 和额外后处理；
- Python、NumPy、PyTorch、CUDA RNG 已按 run seed 初始化；
- `PYTHONHASHSEED` 和 `CUBLAS_WORKSPACE_CONFIG` 在训练子进程启动前设置；
- cuDNN deterministic 开启、benchmark 关闭；
- `torch.use_deterministic_algorithms(True)` 开启；
- DataLoader generator 和 worker seed 已固定；当前正式 `num_workers=0`；
- run metadata 会记录软件、CUDA/cuDNN、GPU、源码/config hash 和初始模型状态 hash；
- A2/B1 的冻结 smoke 已通过。

尚未完成：

- 当前冻结代码下 A2 正式 train→test 的独立重复；
- 当前冻结代码下 B1 正式 train→test 的独立重复；
- B1 ResNet34 预训练权重已固定为项目内路径 `weights/resnet34-b627a593.pth`，SHA256=`b627a593bcbe140c234610266fe4f8ae95ea42fc881d091c9b6052e6b1d0590f`；模型构建时路径缺失或 hash 不匹配直接阻断；
- Git commit 可用的源码版本锚点；当前环境若无 Git，只能使用 source tree SHA256；
- 01–03 的完整 stage-level 验证矩阵；
- 04 的正式业务 Gate/handoff 在冻结机制补强后的重新生成。

因此，当前状态不是“已经完美复现”，而是“复现机制已补强，正式重复验证待完成”。

## 旧结果的处理

当前正式 A2/B1 结果继续保留为真实历史资产，但属于：

```text
reproducibility_contract_version: pre_freeze_audit
```

新增复现机制不会回写旧 run 的 `run_meta.yaml`，也不会修改旧 CSV、checkpoint 或 summary。只有在 `repeat_runs/` 中完成独立重复，并与正式结果逐文件比较后，才能决定旧结果是否可以继续作为当前主结果。

## 比较标准

重复 run 至少比较：

- run identity；
- train/val/test 配置 hash；
- Python、PyTorch、torchvision、NumPy、SciPy、CUDA/cuDNN、GPU；
- deterministic、AMP、CUBLAS、Python hash 设置；
- 初始模型 state hash；
- train_log.csv；
- val_metrics.csv；
- testA_metrics.csv；
- testB_metrics.csv；
- best.ckpt 和 last.ckpt SHA256。

- 严格复现要求：在相同代码、数据、配置、权重、环境和 deterministic 设置下，重复 CSV 和 checkpoint 应完全一致或只有可解释的极小浮点差异。若不一致，必须停止下游阶段并定位原因。
- `compare_runs.py` 的允许差异白名单仅包括 run_name、seed、时间戳和输出路径等非科学身份字段；环境、配置、source/model/权重 hash、CSV、checkpoint hash 任一缺失或差异均返回非零并输出详情。

## 目录说明

| 目录 | 用途 |
|---|---|
| `01_data_protocol/` | 01 数据协议的 manifest、split、数据 hash 和检查报告 |
| `02_unet_flow/` | 02 UNet 流程 runtime/smoke 和入口检查 |
| `03_unet_stability/` | 03 A2 三 seed 稳定性和独立重复检查 |
| `04_baseline/` | 04 A2/B1 协议、模型、六项 Gate 和重复验证 |
| `repeat_runs/` | 所有独立重复训练/测试的输出目录 |
| `reports/` | 当前复现矩阵、差异报告和最终裁决 |

## 运行工具

通用逐 run 比较工具仍位于：

```text
reproducibility_audit/compare_runs.py
```

示例：

```bash
python reproducibility_audit/compare_runs.py \
  experiments/A2_UNet_GlaS_seed3407 \
  experiments/reproducibility_audit/repeat_runs/A2_UNet_GlaS_seed3407_repeat1
```
