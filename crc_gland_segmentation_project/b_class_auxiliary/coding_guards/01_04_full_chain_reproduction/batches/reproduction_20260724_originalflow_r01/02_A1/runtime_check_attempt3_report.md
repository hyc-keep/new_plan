# Runtime Check Report

## 1. Inputs
- project_root: `/home/featurize/work/Paper/crc_gland_segmentation_project`
- experiment_config: `b_class_auxiliary/coding_guards/01_04_full_chain_reproduction/batches/reproduction_20260724_originalflow_r01/configs/A1_UNet_GlaS_repro_r01_seed3407.yaml`
- run_name: `A1_UNet_GlaS_repro_r01_seed3407`
- stage_code: `A1`
- dataset_code: `glas`
- model_code: `unknown`
- model_identity: `unknown.unknown`
- runtime_profile: `full_training_runtime`

## 2. Config Resolution
- data_config_exists: `pass` -> `b_class_auxiliary/coding_guards/01_04_full_chain_reproduction/batches/reproduction_20260724_originalflow_r01/configs/glas_reproduction_r01.yaml`
- model_config_exists: `pass` -> `configs/model/unet_v1.yaml`
- train_config_exists: `pass` -> `configs/train/unet_flow_v1.yaml`
- eval_config_exists: `pass` -> `configs/eval/eval_proto_v1.yaml`
- missing_configs: `none`

## 3. Formal Chain Readiness
- train_entrypoint: `pass` -> `scripts/train.py` (implemented)
- dataset_module: `pass` -> `src/data/datasets.py` (implemented)
- trainer: `pass` -> `src/engine/trainer.py` (implemented)
- model_registry: `pass` -> `src/models/__init__.py` (implemented)
- model_module: `pass` -> `src/models/unet.py` (implemented)
- loss_module: `pass` -> `src/losses/seg_losses.py` (implemented)

## 4. Raw Sample Evidence
- sample_source: `split_csv`
- sample_status: `pass`
- sample_reason: `split_csv_sample_readable`
- split_name: `train`
- split_csv: `b_class_auxiliary/coding_guards/01_04_full_chain_reproduction/batches/reproduction_20260724_originalflow_r01/01_data/splits/glas_train68.csv`
- sample_id: `GlaS_official_train_train_1`
- image_path: `datasets/01_GlaS_official_raw/train_1.bmp`
- mask_path: `datasets/01_GlaS_official_raw/train_1_anno.bmp`
- image_shape_hw: `[522, 775]`
- image_dtype: `uint8`
- mask_shape_hw: `[522, 775]`
- mask_dtype: `uint8`
- mask_unique_values: `['0', '1', '2', '3', '4', '5', '6', '7']`

## 5. Formal Runtime Execution
- runtime_execution_attempted: `True`
- runtime_execution_status: `fail`
- runtime_execution_reason: `subprocess_exit_1`
- runtime_execution_exit_code: `1`
- runtime_blocking_reasons: `[]`
- runtime_command: `/environment/miniconda3/bin/python /home/featurize/work/Paper/crc_gland_segmentation_project/scripts/train.py --config b_class_auxiliary/coding_guards/01_04_full_chain_reproduction/batches/reproduction_20260724_originalflow_r01/configs/A1_UNet_GlaS_repro_r01_seed3407.yaml --run-name A1_UNet_GlaS_repro_r01_seed3407__runtime_probe_attempt3 --runtime-check --runtime-check-output b_class_auxiliary/coding_guards/01_04_full_chain_reproduction/batches/reproduction_20260724_originalflow_r01/02_A1/train_runtime_attempt3_payload.json --device cuda --max-steps 1`
- runtime_log: `b_class_auxiliary/coding_guards/01_04_full_chain_reproduction/batches/reproduction_20260724_originalflow_r01/02_A1/runtime_attempt3.log`
- runtime_evidence_json: `b_class_auxiliary/coding_guards/01_04_full_chain_reproduction/batches/reproduction_20260724_originalflow_r01/02_A1/runtime_attempt3_evidence.json`

## 6. Runtime Fields
- sample_path: `datasets/01_GlaS_official_raw/train_1.bmp`
- sample_id: `GlaS_official_train_train_1`
- input_shape: `None`
- input_dtype: `None`
- target_shape: `None`
- target_dtype: `None`
- target_unique_values: `['0', '1', '2', '3', '4', '5', '6', '7']`
- output_shape: `None`
- output_dtype: `None`
- loss_value: `None`
- loss_is_finite: `None`
- backward_executed: `None`
- optimizer_step_executed: `None`

## 7. Runtime Check Status
- smoke_run_pass: fail (formal runtime-check subprocess failed: subprocess_exit_1)
- dataloader_batch_check_pass: partial (raw sample assets are readable, but no truthful formal dataloader batch evidence was produced)
- tensor_shape_dtype_pass: partial (raw sample assets exist, but formal tensor evidence is still missing)
- loss_finite_pass: fail (loss finite evidence missing or non-finite: None)
- grad_step_pass: fail (formal runtime payload does not confirm both backward and optimizer.step)

## 8. Conclusion
- runtime_check_status: `fail`
- truthful_interpretation: only evidence produced by the formal runtime subprocess may upgrade this report to `pass`; supporting raw-asset inspection alone cannot do that.
