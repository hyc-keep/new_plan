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

## 已完成的 01 正式复现

- 原 `prepare_glas_split.py` 已使用 seed 3407 向本轮独立 `01_data/splits/` 生成四份 split；
- 四份新 split 与历史 CSV 逐行完全一致，行数为 68/17/60/20；165 个样本跨 split 无重复，330 个 image/mask 可读；
- 本轮 `data_stage_acceptance.md` 的 `data_stage_pass=true`、`handoff_ready=true`、`preflight_pass=true`；
- 本轮 `asset_manifest.json` 已登记隔离 data config，7 份本轮 A1/A2/B1 config 均显式引用该 manifest；
- 01 preflight 的 `direct_preflight_payload.json` 证明训练入口实际使用本轮 data config、manifest、train split 和真实 image/mask 样本。该画像仅证明数据协议入口，不代表 A1 模型训练已完成。

## 当前裁决

```text
pre_run_readiness: pass
01_formal_reproduction: pass
02_runtime_and_smoke: allowed
02_formal_training: blocked_until_runtime_and_smoke_pass
03_to_04_formal_reproduction: blocked_by_predecessor
next_allowed_action: prepare and run isolated A1 runtime, then A1 smoke
```
