# 当前 Baseline 严格复现冻结契约

## 1. 目的

本文件冻结当前 A2 UNet 与 B1 ResNet34-UNet 的正式训练、测试和复现边界。它只描述当前正式 baseline，不吸收历史 v1/v2/v3 结果，也不把历史结果改写为当前版本结果。

## 2. 当前正式协议

```text
stage: 04_Baseline
config_version: original_protocol_reproduction
train_proto_version: train_proto_v1
eval_proto_version: eval_proto_v1
data: GlaS train68 / val17 / TestA60 / TestB20
input: RGB 512x512
normalization: ImageNet mean/std
augmentation: light_aug_v1
loss: BCE + Dice
optimizer: AdamW
lr: 1e-3
weight_decay: 1e-4
scheduler: ReduceLROnPlateau, monitor=val_objdice
max_epoch: 120
early_stopping: patience=20
batch_size: 2
AMP: true
best_selector: val_objdice_max
threshold: 0.5, source=val17
postprocess: none_in_v1
seeds: 3407 / 1234 / 2025
metrics: F1, Object Dice, Object Hausdorff, Dice, IoU, HD95, Boundary F1
statistics: population std, ddof=0
```

## 3. 模型边界

```text
A2: plain UNet
B1: ResNet34 encoder + U-Net decoder
```

B1 允许 ImageNet-1K ResNet34 预训练初始化和必要的 decoder/skip 通道尺寸适配。B1 baseline 明确关闭：

```text
BN policy freezing
encoder/decoder differential learning rate
LKMA
Boundary head
Distance head
TTA
extra postprocess
```

LKMA、Boundary、Distance 的代码和配置保留给后续 05–07 阶段，不属于当前 baseline 消费边界。

## 4. 随机与确定性冻结

每个训练/测试进程必须在导入 torch 前设置：

```text
PYTHONHASHSEED=<run seed>
CUBLAS_WORKSPACE_CONFIG=:4096:8
```

代码固定：

- Python random seed；
- NumPy seed；
- PyTorch CPU seed；
- CUDA seed all；
- cuDNN deterministic=true；
- cuDNN benchmark=false；
- `torch.use_deterministic_algorithms(true)`；
- DataLoader generator seed；
- worker seed；
- 当前正式 num_workers=0；
- train/test 使用 run 的 `train_seed`；
- best checkpoint 选择和 threshold 固定。

如果 deterministic algorithm 在某个环境中不支持，程序必须失败并记录，而不能静默退回非确定性算法。

## 5. 必须记录的环境与 lineage

每个新正式 run 的 `run_meta.yaml` 必须记录：

- Python、PyTorch、torchvision、NumPy、SciPy、Pillow、PyYAML 版本；
- Python executable 和 platform；
- CUDA runtime、cuDNN、GPU 型号和 GPU 数量；
- deterministic、cuDNN、CUBLAS 和 Python hash 设置；
- Git commit；
- 冻结源码/配置集合 SHA256；
- 初始模型 state dict SHA256 和 finite 状态；
- ResNet34 预训练权重来源、版本和 hash（若运行环境提供可定位的权重文件）。

## 6. 严格复现定义

同一个 seed 不足以定义同一个实验。严格复现必须同时使用：

```text
同一数据文件和 split
同一配置文件和 hash
同一模型/训练/测试源码和 hash
同一预训练权重和 hash
同一 Python/依赖版本
同一 CUDA/cuDNN/GPU/驱动条件
同一 deterministic/AMP/CUBLAS 设置
同一 DataLoader 顺序
同一 checkpoint 选择和 threshold
```

在这些条件都相同的情况下，重复训练的 CSV、checkpoint 和测试结果应完全相同或只存在可解释的极小浮点差异。若差异明显，必须停止下游实验并进入复现审计。

## 7. 独立复现审计

复现审计工具位于：

```text
crc_gland_segmentation_project/reproducibility_audit/compare_runs.py
```

重复实验必须使用独立 run_name，不得覆盖正式 run。审计至少比较：

```text
run_meta identity
initial_model_state_sha256
train_log.csv
val_metrics.csv
testA_metrics.csv
testB_metrics.csv
best.ckpt SHA256
last.ckpt SHA256
```

## 8. 当前旧结果边界

在本冻结契约补强之前生成的 A2/B1 正式结果继续保留为真实历史资产，但不能ย้อนหลัง声称已经使用本文件中的完整环境快照和 deterministic contract。若需要证明当前代码的严格复现能力，必须在独立目录重新运行至少一个 A2 seed 和一个 B1 seed 的完整 train→test 审计。

如果重新运行后的结果与现有正式结果不一致，不能手动修改任何 CSV 或指标；必须以新代码、环境和真实产物为准，并把旧结果归档为冻结前版本。
