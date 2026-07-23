# 07_Distance 当前代码库状态

## 0. 本轮最小扫描范围

| 目录 | 为什么必须扫描 | 最低检查动作 |
|---|---|---|
| datasets/ | 确认 GlaS 原始数据与 mask 入口 | 扫描文件数并抽查 `datasets/01_GlaS_official_raw/train_65.bmp` |
| splits/ | 确认 train/val/TestA/TestB 边界 | 扫描 `splits/README.md`、`splits/glas/README.md`，核对 10 个文件和 68/17/60/20 计数 |
| configs/ | 确认 B1/D1 配置和 07 新配置缺口 | 扫描 11 个 yaml 文件并读取 `configs/train/unet_flow_v1.yaml` 和 `configs/eval/eval_proto_v1.yaml` |
| src/ | 确认 distance target、loss、model、dataset、trainer、eval 现状 | 扫描 26 个 Python 文件并抽查 `src/data/distance_targets.py`、`src/models/resnet34_unet.py` |
| scripts/ | 确认 train/test 入口和参数 | 扫描脚本数量并抽查 `scripts/train.py`、`scripts/test.py` |
| tools/ | 确认数据协议与辅助工具 | 扫描工具数量并抽查 `tools/stage01_data_protocol/build_distance_targets.py` |
| b_class_auxiliary/ | 确认当前阶段 gate、runtime 和报告工具 | 扫描文件数量并抽查 `b_class_auxiliary/tools/check_precheck_docs.py` |
| experiments/ | 确认历史正式 run 与当前 07 空间隔离 | 扫描 3 个 D1 目录并核对 `experiments/D1_R34UNet_Boundary_GlaS_seed3407/run_meta.yaml`；D2 目录未开始 |
| external/ | 确认外部参考代码边界 | 扫描 `external/README.md`，记录真实外部资料边界并不修改外部目录 |
| reports/ | 确认 B1/D1 manifest、汇总和交接 | 扫描 19 个报告文件并抽查 `reports/tables/baseline_stage_manifest.csv`、`reports/tables/boundary_mean_std.csv` |

## 1. 当前阶段相关目录扫描

| 目录 | 已有文件/资产 | 状态 | 本次是否受影响 |
|---|---|---|---|
| datasets/ | `datasets/01_GlaS_official_raw/train_65.bmp`；真实文件数 165 | 已存在，GlaS 原始入口可读 | 否，沿用 |
| splits/ | `splits/README.md`、`splits/glas/README.md`、真实文件数 10；计数边界记录为 train68/val17，TestA60/TestB20 由 eval protocol 消费 | 已存在，split 边界可解析 | 否，沿用 |
| configs/ | 真实 yaml 文件数 11；`configs/train/unet_flow_v1.yaml`、`configs/eval/eval_proto_v1.yaml`、D1 Boundary configs 存在 | 已存在；07 D2 config 尚未建立 | 是，后续新增 D2 config |
| src/ | 真实 Python 文件数 26；`src/data/distance_targets.py` 已存在，`src/losses/seg_losses.py` 和 `src/models/resnet34_unet.py` 可读 | 已存在；distance preview helper 可复用，但正式训练链未接入 | 是，后续新增/最小更新 |
| scripts/ | 真实脚本文件数 7；`scripts/train.py`、`scripts/test.py` 存在 | 已存在；当前支持 baseline/Boundary，不支持 Distance loss | 是，后续最小更新 |
| tools/ | 真实工具文件数 9；`tools/stage01_data_protocol/build_distance_targets.py` 存在 | 已存在；可用于 target 预览，不是正式训练证据 | 否，读取复用 |
| b_class_auxiliary/ | 真实文件数 31；06 gate/runtime 资产存在，07 研究与阶段卡已存在 | 已存在；07 Pre-check 正在建立 | 是，新增 07 gate/runtime 文档 |
| experiments/ | 真实实验目录数 3 个 D1；`experiments/D1_R34UNet_Boundary_GlaS_seed3407` 存在 | 已存在；D2 目录未开始，历史资产只读 | 是，后续新建 D2 输出目录 |
| external/ | 真实文件数 0；当前无外部源码消费 | 空目录，not_applicable | 否，不修改 |
| reports/ | 真实报告文件数 19；B1 baseline 和 D1 Boundary 汇总/决策存在 | 已存在；07 报告尚未产生 | 是，后续新增 07 派生资产 |

## 2. 已实现能力
- B1 segmentation baseline：已实现并有历史只读资产。
- D1 BoundaryHead：已实现、三 seed 已训练测试、metric crosscheck 通过、正式决策为 backup。
- Distance preview：`src/data/distance_targets.py` 和 `tools/stage01_data_protocol/build_distance_targets.py` 已存在，可读且可复用，但尚未证明正式 dataset→model→loss→checkpoint→eval 链。
- 当前模型：`src/models/resnet34_unet.py` 支持普通 segmentation 单输出和 Boundary 双输出；07 必须显式使用不带 BoundaryHead 的路径。
- 当前训练/评估：`src/engine/trainer.py`、`src/eval/run_eval.py`、`scripts/train.py`、`scripts/test.py` 支持 segmentation/Boundary，但尚未支持 Distance loss。

## 3. 缺口与风险
- Distance target 尚未按 07 contract 接入 dataset batch。
- Distance loss 和 distance output head 尚未接入模型/训练/验证。
- 空 mask/全 mask 约定、target dtype/range、loss reduction 尚未由正式代码验证。
- 07 D2 model/config、experiment config、stage contract、runtime、smoke 和 crosscheck 尚未建立。
- 不能把 D1 Boundary 的 backup 结果冒充 07 Distance 的先验结果。

## 4. 本次预计新增/修改
- Pre-check 通过后，新增/修改 Distance target、Distance loss、model output、dataset/trainer/eval/train/test 的最小接口。
- 新增 D2 model/experiment config、stage contract、runtime 三件套、implementation tracking、raw/summary/decision 资产。
- 不修改 D1 原始实验目录、B1/C1 历史结果或 eval_proto_v1。

## 5. 预期工程落点汇总
- target：`src/data/distance_targets.py`，必要时由实际接口决定是否新增正式 builder。
- loss：现有 `src/losses/seg_losses.py` 的最小 Distance 扩展；具体新文件名待 Pre-check 后锁定。
- model：`src/models/resnet34_unet.py` 的 distance auxiliary 输出，默认关闭 BoundaryHead。
- dataset/trainer/eval：复用现有 sample dict、训练双输出分支和 segmentation-only evaluation。
- config：`configs/model/`、`configs/experiment/` 下 D2 独立身份。
- gate：07 阶段 gate 目录已存在并包含研究/阶段锁定/Pre-check 文档。
- reports：现有 `reports/tables/`；07 implementation tracking 目录将在正式运行资产确定后建立。
