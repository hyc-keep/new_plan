# 01–04 当前复现冻结矩阵

| 阶段 | 固定对象 | 当前状态 | 是否需要独立重复 |
|---|---|---|---|
| 01 数据协议 | 数据文件、split、标签、输入尺寸、归一化、manifest/hash | 配置和入口已固定；完整 hash 矩阵待生成 | 是 |
| 02 UNet 流程 | A2 模型、forward、loss、backward、optimizer、checkpoint、test entrypoint | runtime/smoke 已通过；正式重复待完成 | 是 |
| 03 UNet 稳定性 | A2 seeds 3407/1234/2025、TestA/TestB、mean/std、Gate | 现有正式结果有效；新契约下重复待完成 | 是 |
| 04 Baseline | A2/B1 成对协议、B1 encoder 变量、七项指标、六项 stability Gate | 当前正式结果有效；新契约下重复待完成 | 是 |

## 当前 canonical 协议

```text
train_proto_v1
eval_proto_v1
lr=1e-3
weight_decay=1e-4
batch_size=2
AMP=true
BCE+Dice
ReduceLROnPlateau monitor=val_objdice
max_epoch=120
patience=20
best_selector=val_objdice_max
threshold=0.5 source=val17
TestA/TestB separate
seeds=3407/1234/2025
```

## 当前 baseline 模型边界

```text
A2: plain UNet
B1: ResNet34 encoder + U-Net decoder
```

当前 baseline 明确不消费：

```text
BN policy freezing
differential learning rate
LKMA
Boundary head
Distance head
TTA
extra postprocess
```

后续阶段代码保留，但必须由对应阶段配置显式启用；不能把保留代码误认为当前 baseline 已使用。

## 影响判断

复现机制补强会改变“新训练运行时写入的 metadata 和 deterministic 行为”，不应被当成对旧指标文件的无害文档修改。旧结果不会被覆盖，也不会自动变成新契约结果。

因此严格处理为：

```text
旧正式结果：真实、保留、冻结前版本
新代码/新契约：用于 repeat_runs 独立验证
重复一致：旧结果可继续作为主结果，但需注明版本锚点
重复不一致：新契约结果替代旧结果，旧结果转历史参考
```

## 当前阻断

在至少一个 A2 seed 和一个 B1 seed 完成独立正式 train→test 并与当前正式结果逐项比较前：

- 不宣布 01–04 完成严格复现；
- 不进入 05 正式实现/训练；
- 不删除或覆盖旧正式 run；
- 不手工修改任何指标 CSV。
