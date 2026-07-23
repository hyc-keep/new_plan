# 04_Baseline Stage Gate Check

## 1. 当前阶段
- stage: `04_Baseline`
- current_round: `baseline_stability_v2_lr`
- Stage Gate Result: `allow`

## 2. 进入条件
- 当前阶段实现卡已通过 stage definition gate。
- 六个稳定身份正式配置已存在且 config_version、train_proto_version 一致。
- 旧正式输出、smoke 和过程证据已移入 `_historical_archive/` 并标记历史 only。
- stage contract、formal docs 和 Pre-check 必须由当前路径重新检查。

## 3. 当前阶段进入条件
| 条件 | 当前状态 | 证据 |
|---|---|---|
| 阶段定义 | pass | `stage_definition_gate_report.md` |
| 正式文档 | pass | `formal_stage_docs_check_report.md` |
| contract | pass | `stage_contract_check_report.md` |
| 正式输出 freshness | clean | `experiments/` 下稳定身份目录不存在 |

## 4. 阻断项
| 阻断项 | 当前状态 | 解除动作 |
|---|---|---|
| runtime evidence | 未生成 | 执行独立 runtime probe。 |
| smoke evidence | 未生成 | 使用当前 config 执行 smoke。 |
| formal training | 未开始 | runtime/smoke/code quality 通过后逐 run 启动。 |
| TestA/TestB and aggregation | 未生成 | 正式 run 完成后独立生成和复核。 |

## 5.1 本轮允许进入的工程落点
| 对象 | 允许动作 | 路径 |
|---|---|---|
| 当前门禁报告 | 生成/更新 | `b_class_auxiliary/coding_guards/04_Baseline_stability_recovery/` |
| runtime/smoke | 生成 | `b_class_auxiliary/runtime_checks/`、`experiments/*__runtime_probe`、`experiments/*__smoke` |
| 正式训练 | 暂缓至前置 gate 通过 | `experiments/` 下稳定身份目录 |
| 历史资产 | 只读 | `experiments/_historical_archive/` |

## 6. 结论
当前允许进入 Pre-check、runtime 和 smoke 验证；不代表正式训练或阶段验收已经通过。