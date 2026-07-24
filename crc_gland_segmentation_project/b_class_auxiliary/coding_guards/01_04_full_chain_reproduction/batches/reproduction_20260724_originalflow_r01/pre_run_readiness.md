# reproduction_20260724_originalflow_r01 运行前就绪记录

## 范围

本记录只证明正式复现开始前的对象、配置、环境和输出隔离已做静态核验。它不包含 01 划分、runtime、smoke、训练、测试或指标结果，不能作为任何阶段的通过结论。

## 已通过的静态核验

| 项目 | 真实核验 | 结果 |
| --- | --- | --- |
| 01 原始划分入口 | `tools/stage01_data_protocol/prepare_glas_split.py` 支持 `--output-dir`，固定 `GLAS_SPLIT_SEED=3407`，按 grade 分层、排序并生成四份 CSV | `pass` |
| 历史对象锁 | `reproduction_object_lock.yaml` 记录历史基线、SHA256、历史比较来源和禁止输入；03 使用多份同轮证据支持的 `A2_UNet_GlaS_v1_seed*.yaml` 重建基线 | `pass` |
| 环境锁 | `environment_lock.yaml` 记录 Python、PyTorch、CUDA、cuDNN、GPU、驱动与关键依赖；GPU 驱动实际采样为 `595.71.05` | `pass` |
| 训练配置机械差异 | 7 份本轮训练配置逐键比较：仅允许 run identity、输出根、结果标签、配置版本和本轮 data config 引用变化；model/train/eval 引用保持历史基线不变 | `pass` |
| 本轮数据配置差异 | `glas_reproduction_r01.yaml` 与原 data config 比较：仅 `split_dir` 与 `asset_status` 不同；split seed 和全部数据/预处理字段保持不变 | `pass` |
| 训练入口解析 | 本轮 8 份可训练 YAML 均由项目 YAML loader 解析；新 data config 可被 `load_data_config()` 读取 | `pass` |
| 输出隔离 | `scripts/train.py`/`scripts/test.py` 均支持 `experiment_root`；本轮输出固定于 `experiments/reproduction_20260724_originalflow_r01/<stage>/` | `pass` |
| 新旧比较规则 | `result_comparison_contract.yaml` 已锁定历史真源、计划验收路径、字段和失败条件；历史数值不同不是隐含失败阈值 | `pass` |

## 尚未运行的正式步骤

```text
01：使用原 prepare_glas_split.py 写入本轮 01_data/splits，随后验证并比较新旧 split。
02：仅在 01 数据验收通过后，运行 A1。
03：仅在新 A1 完成后，运行三个 A2 seed。
04：仅在新 A2 三 seed 完成后，运行三个 B1 seed 并做公平比较。
```

## 当前裁决

```text
pre_run_readiness: pass
01_formal_reproduction: pending_not_run
02_to_04_formal_reproduction: blocked_by_predecessor
permission_to_start_formal_training: blocked
next_allowed_action: run stage-01 split generation and data validation only
```

原因：运行前静态准备已经成立，但正式复现必须从 01 的新 split 生成和数据验收开始。任何 A1/A2/B1 runtime、smoke、训练或测试都仍然不允许启动。
