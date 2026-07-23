# 01 数据协议冻结后复现报告

## 1. 复现身份

```text
阶段：01_DataProtocol
状态：PASS
Git commit：43fcf59
日期：2026-07-23
设备：不适用（本阶段执行文件、split、格式和 hash 验证，不进行模型计算）
```

## 2. 已验证内容

- `train68/val17/TestA60/TestB20` 行数分别为 `68/17/60/20`；
- 四个 split 的 `sample_id` 均无重复；
- 所有 split 引用的 330 个图像/掩膜文件均存在；
- 图像模式全部为 `RGB`；
- 掩膜模式全部为 `L`；
- 数据配置、四个 split、asset manifest 和实际数据文件 hash 已真实计算并记录；
- 当前验证未修改数据、split、配置或正式实验结果。

## 3. 真实 hash

```text
data_config_sha256: 833b8628ad9135318f60b636931707eeaea761cd785df88f18c8b767d921d1bc
split_manifest_sha256: 77503f51331d3ae89b4640543ee28635e915a1c4fc1a46a38744007fbdd3eff7
asset_manifest_sha256: 320c7d1158e6a228ff14136bcc58133e14cd8f44d6a9e678e77eb848b9fa8f83
dataset_files_sha256: 13baa6646f8099d62736b8d823df7bdacef7cba57645999a0135d8f1d04e06ac
```

## 4. 结果边界

本报告只证明 01 数据协议验证通过，不证明：

- 02 UNet forward/loss/backward/optimizer.step 流程已通过；
- 03 三个 seed 稳定性实验已通过；
- 04 A2/B1 完整 train→test 已通过；
- 全项目严格数值复现已经完成。

后续若数据配置、split、manifest、图像或掩膜文件发生变化，必须重新计算上述 hash，旧报告不能继续作为当前证据。
