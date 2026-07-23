# 04_Baseline Post-QC Guard

## 1. 当前边界

- 当前编号阶段: `04_Baseline`
- 当前结果轮次: `fresh_original_protocol_reproduction`
- 当前正式身份: `original_protocol_reproduction / train_proto_v1 / eval_proto_v1`
- 当前正式对象: 六个 A2/B1 canonical run，尚未正式训练。
- 排除对象: 历史 v1/v2/v3 run、旧 summary/Gate、旧 runtime/code-quality 报告。

## 2. 实际创建/修改文件

| 文件 | 动作 | 是否符合预期 |
|---|---|---|
| `configs/experiment/A2_UNet_GlaS_seed3407.yaml` | update | yes |
| `configs/experiment/A2_UNet_GlaS_seed1234.yaml` | update | yes |
| `configs/experiment/A2_UNet_GlaS_seed2025.yaml` | update | yes |
| `configs/experiment/B1_ResNet34_UNet_GlaS_seed3407.yaml` | update | yes |
| `configs/experiment/B1_ResNet34_UNet_GlaS_seed1234.yaml` | update | yes |
| `configs/experiment/B1_ResNet34_UNet_GlaS_seed2025.yaml` | update | yes |
| `configs/train/unet_flow_v1.yaml` | not_applicable | unchanged original protocol entry |
| `b_class_auxiliary/coding_guards/04_Baseline/stage_contract.yaml` | update | yes |
| `scripts/run_baseline_sequential.sh` | update | yes |
| `src/models/unet.py` | not_applicable | unchanged |
| `src/models/resnet34_unet.py` | not_applicable | unchanged for this protocol reset |
| `scripts/train.py` | not_applicable | unchanged for this protocol reset |

## 3. 协议级质检结果

| 检查项 | 结果 | 物理证据 |
|---|---|---|
| 最小 smoke run | pass | `runtime_check_A2_original_protocol.md` and `runtime_check_B1_original_protocol.md` report isolated runtime-check subprocess success |
| dataloader batch 检查 | pass | A2/B1 runtime evidence record `[2,3,512,512]` input and `[2,1,512,512]` target |
| tensor shape / dtype 检查 | pass | A2/B1 runtime reports record float32 input/target/output shapes and dtypes |
| loss finite 检查 | pass | A2 loss=1.271264910697937 and B1 loss=1.2935928106307983, both finite |
| backward / optimizer.step 检查 | pass | A2/B1 runtime evidence record backward_executed=true and optimizer_step_executed=true |
| 代码质量门禁 | pass | current diagnostics and runtime evidence are present; gate is regenerated after this guard |

## 4. 当前正式产物状态

| 检查项 | 当前状态 | 证据 |
|---|---|---|
| 六个正式 run | not_started | current round only has isolated probe evidence |
| 正式测试与独立复核 | not_started | must wait for six completed runs |
| current-round 汇总 | not_started | must wait for raw results and independent checks |
| numbered stage Gate | blocked | historical Gate remains false until current round is generated |

## 5.1 关键回链

- `runtime_check_report.md` 路径: `b_class_auxiliary/coding_guards/04_Baseline/runtime_check_B1_original_protocol.md`
- `实现依据记录.md` 路径: `reports/stage_reports/implementation_tracking/04_Baseline/实现依据记录.md`
- A2 独立 runtime report: `b_class_auxiliary/coding_guards/04_Baseline/runtime_check_A2_original_protocol.md`
- A2 独立 runtime evidence: `b_class_auxiliary/coding_guards/04_Baseline/runtime_evidence_A2_original_protocol.json`

## 5. Diagnostics 结果

- `diagnostics_result.txt` 路径: `b_class_auxiliary/diagnostics_result.txt`
- 结论: pass

## 6. 最终状态

- Final Status: partial
- 说明: 当前运行证据和静态门禁成立，但正式六 run、测试、独立复核和阶段 Gate 尚未完成；不得把本轮解释为正式 baseline 通过。
