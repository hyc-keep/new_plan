# Code Quality Gate Report

## 1. 输入文档
- `/home/featurize/work/Paper/crc_gland_segmentation_project/b_class_auxiliary/coding_guards/06_Boundary/Post-QC Guard.md`

## 2. 本轮是否触发代码质量门禁
- 触发结果: `yes`
- runtime_profile: `full_training_runtime`
- 触发对象: `src/models/boundary_head.py`, `src/models/resnet34_unet.py`, `src/models/__init__.py`, `src/data/boundary_targets.py`, `src/data/datasets.py`, `src/data/__init__.py`, `src/losses/boundary_losses.py`, `src/losses/__init__.py`, `src/engine/trainer.py`, `src/eval/run_eval.py`, `scripts/train.py`, `configs/model/resnet34_unet_boundary.yaml`, `configs/experiment/D1_R34UNet_Boundary_GlaS_seed3407.yaml`

## 3. 检查范围
- 检查 `diagnostics_result.txt` 是否补齐代码质量相关状态项。
- 检查 `实现依据记录.md` 是否真实存在,并回链到本轮正式改动、计划依据和参考资料依据。
- 检查 `runtime_check_report.md` 是否回链到真实存在的 `runtime_evidence.json`。
- 检查 `runtime_evidence.json` 是否真实包含样本路径/身份、shape/dtype、loss finite、backward、optimizer.step 等字段。
- 检查 Post-QC Guard 表格、runtime 报告、runtime 证据 JSON、diagnostics 四者是否一致。
- 检查代码质量门禁是否只在真实运行证据成立时才返回 `pass`。

## 4. 检查结果
- `pass`: 未发现代码质量门禁异常。

## 5. 结论
- `code_quality_gate_status`: `pass`
