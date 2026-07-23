# 04_Baseline 当前状态、CUDA 故障与本轮修改说明

状态: [OPEN]
更新范围: 04_Baseline 当前轮

> 本文件只记录真实读取到的实验资产、服务器诊断证据和本轮实际修改。任何未真实运行或未真实读取的内容均不写成已完成。

## 1. 先给结论

你在最开始已经完成了三个正式 B1 seed 的训练和测试，这一点已经从当前磁盘上的正式实验目录和 `run_meta.yaml` 读取确认，不需要因为这次服务器 CUDA 故障重新训练：

- `experiments/B1_ResNet34_UNet_GlaS_seed1234`
- `experiments/B1_ResNet34_UNet_GlaS_seed2025`
- `experiments/B1_ResNet34_UNet_GlaS_seed3407`

三个正式 run 都有训练日志、checkpoint、TestA/TestB 指标、可视化/评估资产，并记录了：

- `stop_reason: early_stopping`
- `device: cuda`
- `amp_active: true`
- `checkpoint_identity_status: pass`
- `metric_crosscheck_result: pass`
- TestA 60 个样本
- TestB 20 个样本

另有 smoke 目录：

- `experiments/B1_ResNet34_UNet_GlaS_seed3407__smoke`

因此，当前问题不是“训练没有完成”，而是：

1. 重新租用的服务器/KVM 虚拟机当前无法初始化 RTX A4000；
2. 当前正式 CUDA runtime 不能重新取得证据；
3. 之前的汇总/Gate 状态与当前真实资产存在旧报告不同步问题，本轮已修补汇总逻辑并重新生成部分报告；
4. B1 的真实 TestB Object Dice 稳定性门仍然失败，这与服务器 CUDA 故障是两个独立问题。

## 2. 三个正式实验的真实状态

已读取：

- `experiments/B1_ResNet34_UNet_GlaS_seed1234/run_meta.yaml`
- `experiments/B1_ResNet34_UNet_GlaS_seed2025/run_meta.yaml`
- `experiments/B1_ResNet34_UNet_GlaS_seed3407/run_meta.yaml`
- 三个 run 的 `testA_metrics.csv`
- 三个 run 的 `testB_metrics.csv`
- 三个 run 的 `metric_crosscheck_note.md`
- smoke run 的 `run_meta.yaml`

当前 B1 汇总真实记录：

- 三个正式 run 完整：`complete_runs: true`
- 评估协议一致：`proto_consistent: true`
- 公平比较成立：`fair_compare: true`
- 配置/评估身份检查已修复为：`standard_identity_ok: true`
- 正式资产完整：`baseline_assets_ready: true`
- checkpoint/指标交叉复核已存在并通过
- `stability_not_weaker: false`
- `stage_pass_b1: false`
- `handoff_ready_for_c1: false`

真实稳定性阻断为：

```text
TestB Object Dice:
B1 std = 0.014335...
A2 std = 0.012146...
B1 std > A2 std
```

这项结果不能通过修改文档、修改阈值或修改 CSV 来消除。它必须按阶段验收规则保持为真实阻断，除非后续依据正式计划重新设计并重新运行实验。

## 3. 服务器 CUDA 故障的真实证据

当前服务器终端已经真实执行并返回：

```text
lspci:
10:00.0 VGA compatible controller: NVIDIA Corporation GA104GL [RTX A4000]

NVRM version: 580.95.05
nvidia-smi: No devices found

nvmlInit_v2_return = 0
nvml_device_count = 0

/dev/nvidia0 open = fail: [Errno 5] Input/output error
/dev/nvidiactl open = pass
/dev/nvidia-uvm open = pass

systemd-detect-virt:
kvm
```

内核日志反复出现：

```text
NVRM: GPU 0000:10:00.0: RmInitAdapter failed! (0x62:0x65:2661)
```

因此当前根因已经收敛为：

```text
PCI 能看到 RTX A4000，NVIDIA 内核模块也已加载，
但 KVM 虚拟机中的 NVIDIA GPU adapter 初始化失败。
```

这不是项目训练代码导致的，也不是已有三个正式 B1 run 的失败。当前服务器需要由宿主机/虚拟化层修复 GPU passthrough、PCI reset 或 NVIDIA 驱动初始化。

## 4. 本轮我实际修改过的文件

### 4.1 `scripts/summarize_stage.py`

实际修改：

- 删除了错误的跨阶段判断：不能因为 A2 的 `config_version: v1` 与 B1 的 `config_version: current_standard` 不同，就把 `standard_identity_ok` 判为失败。
- 保留真正需要一致的评估协议和正式 run 完整性检查。
- 当前 B1 与 A2 是不同阶段/不同模型配置，配置版本字符串不同本身不是身份污染。

没有修改：

- 任何实验结果 CSV；
- 任何 checkpoint；
- 任何 B1 `run_meta.yaml`；
- 任何测试指标数字。

之后真实运行了：

```bash
/environment/miniconda3/bin/python scripts/summarize_stage.py --stage b1
```

结果真实生成了当前 summary、manifest、per-seed summary、mean/std 和 comparison。运行输出显示：

- raw 42 行；
- mean/std 14 行；
- comparison 14 行；
- `standard_identity_failed` 消失；
- 仍保留真实稳定性阻断。

### 4.2 `b_class_auxiliary/tools/run_minimal_runtime_check.py`

实际修改：

- 当正式 runtime 子进程在 CUDA 初始化阶段失败、没有生成 payload 时，使用已解析的 model config 回填模型身份。
- 失败报告现在可以明确显示：

```text
model_code: resnet34_unet
model_identity: src.models.resnet34_unet.unresolved_before_formal_forward
```

- 这只是改善失败证据的可追溯性，不会把失败改成通过。

没有修改：

- `train.py` 的 CUDA 强制检查；
- `--device cuda` 的正式语义；
- 训练模型结构；
- loss、optimizer、数据集或评估实现；
- 任何正式实验结果。

随后真实运行了语法检查和 runtime 检查。当前真实结果仍为：

```text
runtime_check_status=fail
smoke_run_pass=fail
dataloader_batch_check_pass=partial
tensor_shape_dtype_pass=partial
loss_finite_pass=fail
grad_step_pass=fail
```

原因是服务器在 `train.py` 解析 CUDA device 时退出：

```text
CUDA requested via --device='cuda', but no usable CUDA device is available.
```

### 4.3 `b_class_auxiliary/coding_guards/04_Baseline/04_Baseline_post_qc_guard.md`

实际修改：

- 把旧的“正式 CUDA runtime pass”改成当前真实状态；
- 把旧的 code-quality pass 改成当前 runtime 失败后的真实 fail；
- 补充三个正式 B1 seed 已完成训练、测试和指标交叉复核；
- 明确 TestB Object Dice 稳定性门仍失败。

这只是同步状态留痕，不是修改实验结果。

## 5. 本轮真实运行/覆盖过的流程产物

以下文件由正式脚本重新生成或覆盖，原因是旧报告与当前实验资产不同步：

- `reports/stage_reports/baseline_stage_summary.md`
- `reports/tables/baseline_stage_manifest.csv`
- `reports/tables/baseline_per_seed_summary.csv`
- `reports/tables/baseline_mean_std.csv`
- `reports/tables/unet_vs_r34unet_comparison.csv`
- `notes/b1_blockers.md`
- `b_class_auxiliary/coding_guards/04_Baseline/runtime_check_report.md`
- `b_class_auxiliary/coding_guards/04_Baseline/runtime_evidence.json`
- `b_class_auxiliary/coding_guards/04_Baseline/runtime_check.log`
- `b_class_auxiliary/coding_guards/04_Baseline/code_quality_gate_report.md`
- `b_class_auxiliary/coding_guards/04_Baseline/workflow_gate_report.md`

这些报告中的结果来自脚本读取当前实验资产或当前服务器真实运行，不是手工填写。

注意：runtime 失败时没有 payload，因此不存在有效的 `train_runtime_payload.json`。不能伪造该文件来补齐 forward/loss/backward/optimizer.step 证据。

## 6. 没有修改的关键正式实验资产

本轮没有修改以下内容：

- `experiments/B1_ResNet34_UNet_GlaS_seed1234/**`
- `experiments/B1_ResNet34_UNet_GlaS_seed2025/**`
- `experiments/B1_ResNet34_UNet_GlaS_seed3407/**`
- `experiments/B1_ResNet34_UNet_GlaS_seed3407__smoke/**`
- 三个正式 run 的 `run_meta.yaml`；
- 三个正式 run 的训练/测试 CSV；
- 三个正式 run 的 checkpoint；
- 正式测试预测、可视化和评估资产。

因此，原先已经训练和测试成功的结果仍然保留。

## 7. 当前应该怎么做

### 第一步：不要重训，不要删除正式 run

保留并备份路径记录，但不要删除：

```text
experiments/B1_ResNet34_UNet_GlaS_seed1234
experiments/B1_ResNet34_UNet_GlaS_seed2025
experiments/B1_ResNet34_UNet_GlaS_seed3407
```

这些是已经存在的真实实验资产。

### 第二步：先修复服务器 GPU，不要改项目代码绕过

让服务器管理员处理：

- KVM 的 PCI passthrough/VFIO；
- RTX A4000 的 PCI reset；
- 宿主机是否占用 GPU；
- NVIDIA 驱动初始化；
- `RmInitAdapter failed (0x62:0x65:2661)`；
- `/dev/nvidia0` 打开返回 I/O error。

修复后的最低验收条件：

```bash
nvidia-smi
```

能正常列出 RTX A4000，并且：

```bash
/environment/miniconda3/bin/python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.device_count())"
```

输出应为：

```text
True
1
```

### 第三步：GPU 恢复后只重新运行 runtime 证据

GPU 恢复后运行：

```bash
cd /home/featurize/work/Paper/crc_gland_segmentation_project

/environment/miniconda3/bin/python \
  b_class_auxiliary/tools/run_minimal_runtime_check.py \
  --project-root /home/featurize/work/Paper/crc_gland_segmentation_project \
  --experiment-config configs/experiment/B1_ResNet34_UNet_GlaS_seed3407.yaml \
  --split train \
  --sample-index 0 \
  --device cuda \
  --max-steps 1 \
  --output b_class_auxiliary/coding_guards/04_Baseline/runtime_check_report.md \
  --evidence-output b_class_auxiliary/coding_guards/04_Baseline/runtime_evidence.json \
  --log-output b_class_auxiliary/coding_guards/04_Baseline/runtime_check.log \
  --train-runtime-output b_class_auxiliary/coding_guards/04_Baseline/train_runtime_payload.json
```

只有真实输出全部为 `pass`，才能继续 code-quality 和 workflow gate。

### 第四步：重新运行 code-quality 和 workflow gate

runtime 通过后运行：

```bash
/environment/miniconda3/bin/python \
  b_class_auxiliary/tools/check_code_quality_gate.py \
  --project-root /home/featurize/work/Paper/crc_gland_segmentation_project \
  --post-qc-guard b_class_auxiliary/coding_guards/04_Baseline/04_Baseline_post_qc_guard.md \
  --output b_class_auxiliary/coding_guards/04_Baseline/code_quality_gate_report.md
```

然后重新运行已有的 workflow gate 命令。不要手工编辑 Gate 数字。

### 第五步：再单独处理 B1 稳定性门

即使 CUDA runtime 和 code-quality 恢复通过，当前阶段仍需根据真实汇总处理：

```text
B1 TestB Object Dice 标准差高于 A2
```

这不是服务器故障造成的报告问题，而是已经完成的三个 seed 真实结果产生的阶段验收阻断。必须依据计划决定接受该基线边界还是重新设计/重新运行，不得修改结果数字或阈值来强行放行。

## 8. 关于“要不要恢复我改的文件”

当前不建议盲目恢复或删除修改：

- `summarize_stage.py` 的修改修复了错误的跨模型配置版本判定；
- `run_minimal_runtime_check.py` 的修改只增强失败证据中的模型身份；
- Post-QC Guard 的修改把过期的 pass 状态改成了真实 fail；
- 这些修改没有触碰三个正式实验的训练/测试结果。

项目目录没有可用的 Git 仓库，无法通过 Git 自动回滚或展示历史 diff。因此本文件承担本轮修改清单和恢复边界记录。

如果后续要恢复，必须逐文件审查，不能执行不加区分的全目录删除或回滚。

## 9. 最终状态

```text
正式实验：已完成，结果资产保留
当前服务器：GPU PCI 可见，但 NVIDIA adapter 初始化失败
正式 CUDA runtime：blocked
code-quality gate：blocked/fail
B1 汇总：已重新生成
B1 身份一致性：已修复并通过
B1 TestB 稳定性门：真实失败
是否重训：当前不需要
是否删除正式 run：禁止
当前最优先动作：修复服务器/KVM GPU 初始化，然后只补跑 runtime 与 Gate 证据
```
