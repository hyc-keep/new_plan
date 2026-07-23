# 07_Distance Pre-check 提取

## 1. 当前阶段与输入
- 当前阶段：`07_Distance`
- 上游 research alignment：`pass`
- 上游 stage definition：`pass`
- 当前 base：`boundary_input_base`
- 06 Boundary decision：`backup`
- 当前 Pre-check 结论：尚未通过，本文只记录运行前核对结果。

## 2. 规划约束提取

| 约束类型 | 计划/协议依据 | 当前执行约束 | 物理落点 |
|---|---|---|---|
| 官方协议固定项 | `configs/eval/eval_proto_v1.yaml`、全局参数冻结表 | GlaS train68/val17/TestA60/TestB20；val_objdice_max；threshold 0.5；float32；8-connectivity；TestA/TestB 分开 | `configs/eval/eval_proto_v1.yaml`、现有 test/eval 入口 |
| 路线层已锁定 | 07 阶段总协议、阶段实现卡 | 单一 EDT_norm01 距离辅助监督；默认 B1 主线；不叠加 BoundaryHead；不引入 topology/后处理 | 07 阶段实现卡、D2 配置待锁定 |
| 论文支持的候选范围 | Distance-Map-Loss、Shape-Aware-SDM 计划证据 | geometry-aware auxiliary supervision；主 lambda 0.1；候选 0.05/0.2；SmoothL1 是工程候选，不冒充论文最优 | Distance target/loss 模块待 Pre-check 后实现 |
| 工程冻结规则 | `src/data/datasets.py`、`src/losses/seg_losses.py`、`src/engine/trainer.py`、`src/eval/run_eval.py` | 保持旧单输出 baseline；Distance target 必须 shape/dtype/range/finiteness 可验证；distance logits 不参与 segmentation threshold | 现有 dataset/trainer/eval 最小适配 |

## 2.1 预期工程落点
- 目标对象：Distance target、Distance auxiliary loss、模型辅助输出、dataset batch 字段、trainer/eval loss 调用、D2 model/experiment config、07 contract/runtime/report。
- 预期路径：src/data/distance_targets.py、src/losses/seg_losses.py 的最小 Distance 扩展、src/models/resnet34_unet.py 的最小 distance 分支、src/data/datasets.py、src/engine/trainer.py、src/eval/run_eval.py、scripts/train.py、scripts/test.py、configs/model/、configs/experiment/。
- 当前状态：上述 Distance 正式链尚未接入；不得把已有 `/home/featurize/work/Paper/crc_gland_segmentation_project/src/data/distance_targets.py` 预览工具视为正式训练实现。
- 允许改：新增 Distance target/loss 和最小辅助输出，且只能在 Pre-check gate 通过后进行。
- 不允许改：split、eval protocol、Boundary backup 决策、历史结果，或引入 topology/后处理。

## 3. 路线层约束提取
- 先主版本 seed3407 screening，再决定是否运行 seed1234/2025。
- 不在 07 首轮同时搜索 BoundaryHead、target 类型、loss 类型、lambda 和后处理。
- 不消费 06 Boundary 的 `boundary_kept_base`，当前只消费 `boundary_input_base`。
- 正式输出必须保留 segmentation logits、distance logits、各项 loss、checkpoint identity 和 TestA/TestB raw 资产。

## 4. 文献/参考实现提取
- Distance/shape 资料只支撑 geometry-aware supervision 的研究动机和候选范围，不等于当前组合的最优证明。
- GlaS 参考评估要求按样本和 split 导出，并保留 Object Dice/F1/Hausdorff、HD95、Boundary F1。
- 正式评估继续消费 segmentation logits；distance logits 不能被 threshold 成测试 mask。

## 5. 当前阶段唯一允许改动的变量
- 允许改：Distance target/loss 接口和登记的 `lambda_dist` 候选；首轮主版本固定 `EDT_norm01_v1 + SmoothL1 + 0.1`。
- 不允许改：split、eval protocol、Boundary backup 决策、历史结果、topology、后处理和未登记的模型结构变量。
- 主版本允许改动：Distance target/loss 接口和 `lambda_dist`，但首轮固定 `EDT_norm01_v1 + SmoothL1 + 0.1`。
- 候选变量：仅登记 0.05/0.2，必须在主版本 screening 链路和结果可解释后选择性运行。
- 明确不允许：BoundaryHead、SDM 多通道、clDice/topology、TA-Net、SkeletonAwareDT、marker/watershed、postprocess、eval proto、split、threshold、checkpoint selector。

## 6. Pre-check 尚待核对的运行前问题
- 当前 distance target helper 的实现是否与 07 的 per-sample norm01 及空/全 mask 规则一致。
- 现有 dataset transform 后的 mask 是否仍适合 EDT，target 是否与 image/mask 尺寸对齐。
- 模型 distance 输出的 feature/channel、dtype 和训练/评估返回结构。
- SmoothL1 reduction、loss finite、AMP 下的数值稳定性。
- D2 正式 run/config identity、stage contract 和 probe run_name。
