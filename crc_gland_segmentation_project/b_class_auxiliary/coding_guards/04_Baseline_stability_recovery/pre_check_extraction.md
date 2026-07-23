# 04_Baseline Pre-check 约束提取

## 1. 本轮任务归属
- 当前阶段: `04_Baseline`
- 当前轮次: `baseline_stability_v2_lr`
- 当前目标: 重新生成 A2/B1 稳定身份三 seed 正式 baseline。

## 2. 规划约束提取

| 约束类型 | 约束内容 | 依据文件 | 本轮执行方式 |
|---|---|---|---|
| 官方协议固定项 | train68 / val17 / TestA60 / TestB20；七项指标；TestA/TestB 分开；ddof=0 | `b_class_auxiliary/coding_guards/04_Baseline_stability_recovery/stage_contract.yaml` | 六个 run 使用同一 contract 和 eval proto。 |
| 路线层已锁定 | A2 为 U-Net 控制，B1 为 ResNet34-U-Net；seed 固定 3407、1234、2025 | `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/02_训练协议.md` | 不新增结构变量，不消费历史 04 资产。 |
| 论文支持的候选范围 | U-Net decoder/skip 和 ResNet34 residual encoder 保持现有实现语义 | `结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/02_U-Net.md`；`结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/05_ResNet.md` | 只使用现有模型入口和冻结配置。 |
| 工程冻结规则 | AdamW；encoder_lr=1e-4；decoder_lr=1e-3；weight_decay=1e-4；不改 loss/scheduler/early stopping/threshold/metrics | `configs/train/unet_flow_v2.yaml`；`scripts/train.py`；`src/engine/trainer.py` | run lock 独占写入，CSV epoch 严格单调，历史目录只读。 |

## 2.1 预期工程落点
- 正式配置：`configs/experiment/A2_UNet_GlaS_seed3407.yaml`、`configs/experiment/A2_UNet_GlaS_seed1234.yaml`、`configs/experiment/A2_UNet_GlaS_seed2025.yaml`、`configs/experiment/B1_ResNet34_UNet_GlaS_seed3407.yaml`、`configs/experiment/B1_ResNet34_UNet_GlaS_seed1234.yaml`、`configs/experiment/B1_ResNet34_UNet_GlaS_seed2025.yaml`。
- 正式输出：`experiments/`，每个稳定身份单独目录。
- 历史边界：`experiments/_historical_archive/04_Baseline__historical_20260721_stable_identity_reset/`。
- 当前门禁：`b_class_auxiliary/coding_guards/04_Baseline_stability_recovery/`。
- 当前实现依据：`reports/stage_reports/implementation_tracking/04_Baseline_stability_recovery/实现依据记录.md`。

## 3. 路线层约束提取
- A2 与 B1 必须使用配对 seed，不能只训练单个 seed 后宣称 stability。
- 正式身份名不携带 v1/v2；版本和协议写入 config_version、train_proto_version、model_version、result_tag。
- 每个正式 run 必须逐一启动，不能让多个进程写同一输出目录。

## 4. 文献/参考实现提取
- U-Net 依据锁定 contracting path、expanding path 和 skip 语义。
- ResNet 依据锁定 residual/basic block encoder 语义。
- 项目评估入口和 GlaS 对象级指标实现是当前结果口径，不能另写替代指标。

## 5. 当前阶段唯一允许改动的变量
- 允许改：当前轮次的稳定命名配置、run lock/CSV 保护、当前轮次 gate/runtime/smoke 证据和全新实验输出。
- 不允许改：模型结构、数据 split、标签、输入尺寸、normalization、augmentation、loss、scheduler、early stopping、threshold、指标实现、统计规则和任何历史对象。

## 6. Pre-check 结论边界
当前允许继续执行机器门禁、runtime 和 smoke；Pre-check 通过不等于正式训练完成，也不等于阶段最终验收通过。
