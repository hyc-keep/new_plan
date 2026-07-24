# r02 A1 正式训练冻结记录

## 冻结对象

- 批次：`reproduction_20260724_originalflow_r02`
- 正式 run：`A1_UNet_GlaS_repro_r02_seed3407`
- 正式 config：`configs/A1_UNet_GlaS_repro_r02_seed3407.yaml`
- 代码提交：`e95656ea6284a7c6d9ccf580891e48154046ea9b`
- 环境锁：`environment_lock.yaml`
- 本轮 01 manifest：`01_data/asset_manifest.json`

## 已通过的前置证据

1. 原 01 划分脚本重新生成 r02 四份 split；它们与历史 CSV 逐行一致，165 个样本跨 split 无重复。
2. r02 数据验收为 `data_stage_pass=true`、`handoff_ready=true`、`preflight_pass=true`。
3. r02 A1 runtime 已证明正式数据入口、dataloader、forward、finite loss、backward 与 optimizer step 均可执行。
4. r02 A1 smoke 已生成训练/验证日志、best checkpoint、run_meta，并记录 CUDA、cuDNN、seed 和确定性字段。
5. r01 的 AMP overflow 缺陷已由隔离调试复现并修复：AMP 下由 GradScaler 跳过溢出 step 并回退 scale；非 AMP 非有限梯度仍硬失败。

## 冻结边界

从本文件生成后直到正式 A1 完成，不修改：

- `src/engine/trainer.py`、`scripts/train.py`、`scripts/test.py`；
- r02 A1 config、r02 data config、01 manifest；
- 模型、训练、评估、数据、seed、指标或比较口径。

正式运行只允许写入：

```text
experiments/reproduction_20260724_originalflow_r02/02_A1/A1_UNet_GlaS_repro_r02_seed3407/
```

该目录目前不存在。若正式运行失败，保留该目录并建立新批次；不得 resume 或覆盖 r02。
