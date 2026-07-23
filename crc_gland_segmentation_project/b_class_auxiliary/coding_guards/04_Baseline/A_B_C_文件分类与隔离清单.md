# 04_Baseline A/B/C 文件分类与隔离清单

## 1. 目的

本清单用于区分当前正式对象、已归档历史对象和来源未裁决候选对象。

本清单不执行删除、不执行覆盖、不把候选文件移动到历史归档；它只定义当前消费边界，避免把“文件存在”误写成“当前正式资产成立”。

## 2. 当前轮裁决

- 当前阶段: `04_Baseline`
- 当前轮次: `fresh_reset_20260714`
- 研究定标: `pass`
- 阶段锁定: `pass`
- Pre-check: `fail`
- 当前正式 B1 结果: `none`
- 当前正式 B1 run: `none`
- 当前正式 B1 experiment config: `none`
- 当前允许消费的历史来源: A2 当前 handoff；不得消费 protocol_v3 B1 结果或历史 gate。

## 3. A 类：当前正式协议/共享正式工程对象，必须保留原路径

| 对象 | 当前路径 | 当前消费边界 | 处理 |
|------|---------|-------------|------|
| 04 总协议 | `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md` | 04 当前唯一总协议 | 保留原路径，不归档，不删除。 |
| 04 结构协议 | `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/01_R34UNet结构与来源.md` | 04 结构细则 | 保留原路径，不归档，不删除。 |
| 04 训练协议 | `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/02_训练协议.md` | 04 训练继承与公平比较边界 | 保留原路径，不归档，不删除。 |
| 04 比较协议 | `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/03_对比与判断规则.md` | 04 比较和 Gate_B1_compare | 保留原路径，不归档，不删除。 |
| 04 验收协议 | `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/04_阶段验收.md` | 04 Gate_B1、handoff、回退 | 保留原路径，不归档，不删除。 |
| 当前评估实现 | `src/metrics/seg_metrics.py` | A2/B1 共享评估实现候选；正式 B1 仍需当前轮 contract/freshness 核验 | 保留原路径，不移动。 |
| 当前训练/测试/汇总入口 | `scripts/train.py`、`scripts/test.py`、`scripts/summarize_stage.py` | 共享工程入口 | 保留原路径，不移动。 |
| A2 当前 handoff | `reports/tables/unet_stage_manifest.csv` | B1 唯一允许消费的上游稳定基线来源 | 保留原路径，只读消费。 |

## 4. B 类：历史/流程证据，可归档或已归档，当前不得作为 B1 gate

| 对象 | 当前/归档路径 | 当前消费边界 | 处理 |
|------|---------------|--------------|------|
| 旧 B1 流程证据 | `b_class_auxiliary/coding_guards/04_Baseline/_historical_archive/04_Baseline__historical_20260714_protocol_v3_reset/` | 仅历史审计，不得冒充当前 gate | 已归档，继续保留。 |
| 旧 B1 研究/阶段锁定/Pre-check | 同上归档批次 | 仅历史追溯 | 已归档，当前不消费。 |
| 旧 B1 runtime/code quality/workflow | 同上归档批次 | 仅历史追溯 | 已归档，当前不消费。 |
| 旧 B1 说明文和实现依据 | 同上归档批次 | 仅历史追溯 | 已归档，当前不消费。 |
| 当前 04 Pre-check 四件套 | `b_class_auxiliary/coding_guards/04_Baseline/pre_check_extraction.md`、`stage_gate_check.md`、`current_codebase_状态.md`、`04_Baseline_pre_check_guard.md` | 当前轮 B 类前置证据；当前 gate 仍 fail | 保留当前路径，修复后重新运行 gate。 |
| 当前 04 研究/阶段锁定证据 | `b_class_auxiliary/coding_guards/04_Baseline/研究定标记录.md`、`00_阶段实现卡.md` 及对应 gate | 当前轮 B 类前置证据 | 保留当前路径，不能移入历史。 |

## 5. C 类：当前存在但来源/正式身份未裁决，隔离消费，不物理移动

| 对象 | 当前路径 | 为什么属于 C 类 | 当前处理 |
|------|---------|------------------|-----------|
| ResNet34-U-Net 候选实现 | `src/models/resnet34_unet.py` | 文件头声明为 stage04 formal，但当前 reset 状态为 not_started；引用的 B1 experiment config 尚不存在；权重缓存、版本和 SHA256 未形成当前轮证据 | 保留原路径；标记为候选输入；当前 B1 gate 不消费；Pre-check/contract 通过后重新审查。 |
| 模型 factory 当前实现 | `src/models/__init__.py` | 当前轮已按标准文件名重写；尚未通过 runtime/code quality；旧候选只在 source snapshot中保留 | 保留原路径；正式消费须等待 runtime/code quality。 |
| ResNet34 model config | `configs/model/resnet34_unet.yaml` | 当前轮标准 model config；不是 seed experiment config；尚未通过 runtime/code quality | 保留原路径；不得直接启动正式训练。 |
| 其他未登记 B1 候选文件 | 当前项目中若后续扫描发现 | 无当前轮 source/manifest/consumer/lineage 回链 | 先登记 C 类，不删除、不移动，直到完成来源裁决。 |

## 6. 明确不允许的操作

- 不把 04 当前五份正式协议移动到历史归档。
- 不把共享 `src/`、`scripts/`、`src/metrics/` 因为来源未裁决而直接移走。
- 不从历史归档复制旧 B1 结果、checkpoint、metrics、gate 或通过结论到当前路径。
- 不把候选 ResNet34-U-Net 代码直接当成当前正式 B1 实现。
- 不删除 C 类文件；只有在后续完成正式交付前清理并留下清理清单后，才允许删除明确无消费边界的副本或缓存。

## 7. 后续清理规则

- 只有明确标记 `historical_archive_only=true` 且已写入归档 manifest 的旧 B 类证据，才允许留在历史归档。
- 只有明确标记为生成缓存、且不属于正式结果、代码、配置、gate 或 handoff 的文件，才允许在交付前清理。
- C 类候选对象必须先完成来源裁决；若确认不消费，应建立只读隔离副本和 archive_manifest，再由交付前清理阶段决定是否删除。
- 当前 04 正式 B1 完成前，不执行大范围清理，以免破坏复现链和排障证据。

## 8. 当前结论

```text
A类正式协议: 保留原路径
B类旧流程证据: 已归档，当前不消费
C类候选代码/配置: 原路径保留，当前隔离消费
历史归档: 生效
Pre-check: 仍fail
正式编码: 禁止
正式训练: 禁止
```
