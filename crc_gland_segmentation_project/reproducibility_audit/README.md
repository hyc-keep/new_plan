# 当前 Baseline 可复现审计

## 目标

本目录只服务当前 `04_Baseline` 的复现性审计，不参与正式指标计算，不覆盖正式 run，也不消费历史 v1/v2/v3 结果。

正式实验要被称为“同一实验的复现”，必须同时满足：

- 同一实验配置文件及 SHA256；
- 同一数据 manifest、split CSV、数据文件和 SHA256；
- 同一模型代码、训练代码、测试代码和源码 SHA256；
- ResNet34 预训练权重必须来自配置中的本地 `pretrained_weights_path`，并匹配 `pretrained_weights_sha256`；当前 B1 使用项目内 `weights/resnet34-b627a593.pth`，SHA256 为 `b627a593bcbe140c234610266fe4f8ae95ea42fc881d091c9b6052e6b1d0590f`，缺失或 hash 不匹配在模型构建时失败。
- 同一 Python、PyTorch、torchvision、NumPy、SciPy、Pillow、PyYAML 版本；
- 同一 CUDA、cuDNN、GPU 和驱动环境；
- 同一 `train_seed`、DataLoader generator、worker 设置和排序；
- 同一 deterministic algorithms、cuDNN、CUBLAS 和 AMP 设置；
- 同一 best checkpoint 选择规则和 threshold；
- 同一 TestA/TestB 评估实现。

仅仅 seed 相同或主要超参数相同，不足以称为严格复现。

## 当前冻结规则

当前 A2/B1 正式协议仍为：

```text
train_proto_v1
eval_proto_v1
lr=1e-3
weight_decay=1e-4
batch_size=2
AMP=true
BCE+Dice
ReduceLROnPlateau
val_objdice best selector
threshold=0.5 from val17
TestA/TestB separate
seeds=3407/1234/2025
```

B1 只使用 `r34_unet_v1` ResNet34 encoder + U-Net decoder。baseline 不启用 BN policy、差分学习率、LKMA、Boundary、Distance、TTA 或额外后处理。后续阶段需要的模块代码保留在正式工程中，但不被当前 baseline 配置消费。

## 已实现的确定性机制

- Python、NumPy、PyTorch 和 CUDA RNG 按 `train_seed` 初始化；
- DataLoader generator 按 `train_seed` 初始化；
- worker seed helper 已固定；当前正式 `num_workers=0`；
- `cudnn.deterministic=true`；
- `cudnn.benchmark=false`；
- `torch.use_deterministic_algorithms(true)`；
- Python 进程启动前设置 `CUBLAS_WORKSPACE_CONFIG=:4096:8`；
- run_meta 写入环境版本、GPU、CUDA/cuDNN、源码/config hash、初始模型状态 hash；
- train/test 都使用同一 seed 初始化；
- 新增 `compare_runs.py` 进行逐字段、逐 CSV、逐 checkpoint 对比；缺失资产、严格 metadata 差异、CSV 差异或 checkpoint hash 差异均返回非零并打印差异详情。
- `PYTHONHASHSEED` 必须由 launcher 在 Python 启动前设置并等于配置 seed；train/test 入口会在导入 torch/numpy 前阻断缺失或不一致值。
- test 只接受当前 run 的 `checkpoints/best.ckpt` 或其 checkpoints 子目录内路径，并强制核对 run_meta/checkpoint 的身份字段、best path 与 hash。

## 使用方式

严格复现审计应在独立目录名下运行，不能覆盖正式 run：

```bash
python reproducibility_audit/compare_runs.py \
  experiments/A2_UNet_GlaS_seed3407 \
  experiments/repro_A2_UNet_GlaS_seed3407_repeat
```

输出至少应检查：

```text
meta_identity_equal
initial_model_state_sha256_equal
train_log.csv_equal
val_metrics.csv_equal
testA_metrics.csv_equal
testB_metrics_equal
checkpoints/best.ckpt_sha256_equal
checkpoints/last.ckpt_sha256_equal
```

## 当前结果边界

现有 A2/B1 正式结果是在本目录机制补强之前生成的，不能ย้อนหลัง补写为已使用新机制。它们仍可作为真实历史结果保存，但要声明：

```text
reproducibility_contract_version: pre_freeze_audit
```

如果需要证明当前代码版本的数值复现能力，应在本目录建立独立 repeat run，完成至少一个 A2 seed 和一个 B1 seed 的完整 train→test 对比。重复结果若不一致，必须先定位环境、预训练权重、源码或确定性链，而不是修改统计结果。

## 代码边界

- `src/utils/seed.py`：随机源和确定性开关；
- `src/utils/reproducibility.py`：环境、源码、配置和模型状态 hash；
- `scripts/train.py`：写入正式 run 的复现元数据；
- `scripts/test.py`：测试前按 run seed 初始化；
- `reproducibility_audit/compare_runs.py`：独立 run 对比；
- `configs/model/resnet34_unet_lkma_v1.yaml`、boundary、distance 以及 `configs/train/unet_flow_v2.yaml`、v3：后续/历史配置，不属于当前 baseline 消费边界。
