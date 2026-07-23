# 04_Baseline Pre-check Guard

## 1. 本次任务归属
- 当前阶段：`04_Baseline`
- 当前轮次：`baseline_stability_v2_lr`
- 阶段实现卡路径: `b_class_auxiliary/coding_guards/04_Baseline_stability_recovery/00_阶段实现卡.md`
- 阶段锁定门禁结论: `pass`
- Stage Gate Result: `allow`

## 2. 来自规划的硬约束
- A2/B1 必须各运行 seed 3407、1234、2025。
- split、loss、评估、threshold、TestA/TestB、指标、ddof=0 和历史结果边界不变。
- 当前正式身份名为 `A2_UNet_GlaS_seed<seed>` / `B1_ResNet34_UNet_GlaS_seed<seed>`。

## 3. 来自参考资料的实现依据
- `结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/02_U-Net.md`
- `结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/05_ResNet.md`
- `scripts/train.py`
- `src/engine/trainer.py`

## 4. 当前工程已有能力与缺口
- 已有能力：稳定命名配置、差分学习率参数组、单写者 run lock、CSV epoch 单调保护、stage contract。
- 当前缺口：本轮 runtime、smoke、正式训练、测试和聚合证据尚未生成。

## 5. 本次任务边界
- 明确要做：生成本轮门禁证据并在通过后逐 run 重训。
- 明确不做：复用历史 checkpoint、历史 CSV、历史预测、历史 metrics 或历史 gate 结论。

## 6. 预期代码落点
- 当前配置：`configs/experiment/`
- 当前运行：`experiments/`
- 历史资产：`experiments/_historical_archive/`
- 当前结果：`reports/`

## 7. 最小运行验证
- 阶段定义、Pre-check、contract、formal docs 必须重新检查。
- runtime 和 smoke 必须独立运行并保存证据。
- 正式 run 必须逐目录启动，检查 epoch 严格递增和完整 summary/checkpoint。

## 8. 文档映射
| 对象 | 归类 | 当前路径 | 动作 |
|---|---|---|---|
| 阶段实现卡 | B | `b_class_auxiliary/coding_guards/04_Baseline_stability_recovery/00_阶段实现卡.md` | update |
| stage contract | B | `b_class_auxiliary/coding_guards/04_Baseline_stability_recovery/stage_contract.yaml` | update |
| 正式配置 | A | `configs/experiment/` | fresh run |
| 正式输出 | A | `experiments/` | create |

## 7. 上游 guard 文件回链
- 当前阶段实现卡路径：`b_class_auxiliary/coding_guards/04_Baseline_stability_recovery/00_阶段实现卡.md`
- 当前 stage definition report：`b_class_auxiliary/coding_guards/04_Baseline_stability_recovery/stage_definition_gate_report.md`
- 当前 `pre_check_extraction.md`、`stage_gate_check.md`、`current_codebase_状态.md` 和本文件必须存在。
- 当前 `precheck_doc_gate_report.md` 由 `b_class_auxiliary/tools/check_precheck_docs.py` 生成。

## 6.1 预期文档映射

| 本轮变更对象 | 归类 | 归类依据 | 对象级说明文 | 入口同步项 | 计划动作 | 备注 |
|---|---|---|---|---|---|---|
| `configs/experiment/` | A | 正式实验配置 | `reports/stage_reports/implementation_tracking/04_Baseline_stability_recovery/实现依据记录.md` | `stage_contract.yaml` | update | 稳定 identity，不携带 v1/v2。 |
| `experiments/` | A | 正式训练输出 | `reports/stage_reports/implementation_tracking/04_Baseline_stability_recovery/实现依据记录.md` | `stage_contract.yaml` | create | 只接受 fresh run。 |
| `b_class_auxiliary/coding_guards/04_Baseline_stability_recovery/` | B | 当前门禁证据 | `reports/stage_reports/implementation_tracking/04_Baseline_stability_recovery/实现依据记录.md` | 阶段卡和 contract | update | 由当前工具重新生成。 |
| `experiments/_historical_archive/` | B | 历史 provenance | `reports/stage_reports/implementation_tracking/04_Baseline_stability_recovery/实现依据记录.md` | archive_manifest.md | update | historical_archive_only=true。 |
- 当前 `precheck_doc_gate_report.md` 由工具生成，不引用历史报告。
