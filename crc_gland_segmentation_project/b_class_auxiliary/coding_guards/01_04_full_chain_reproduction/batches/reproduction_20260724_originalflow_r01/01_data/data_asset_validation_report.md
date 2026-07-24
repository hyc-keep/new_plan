# Data Asset Validation Report

- project_root: `/home/featurize/work/Paper/crc_gland_segmentation_project`

## glas
- status: `pass`
- dataset_code: `glas`
- dataset_role: `primary_benchmark`
- dataset_root: `datasets/01_GlaS_official_raw`
- dataset_root_exists: `True`
- dataset_source_note: `datasets/DATASET_SOURCE_NOTES.md`
- asset_status: `reproduction_r01_pending`
- split_train: `b_class_auxiliary/coding_guards/01_04_full_chain_reproduction/batches/reproduction_20260724_originalflow_r01/01_data/splits/glas_train68.csv` exists=`True` rows=`68`
- split_val: `b_class_auxiliary/coding_guards/01_04_full_chain_reproduction/batches/reproduction_20260724_originalflow_r01/01_data/splits/glas_val17.csv` exists=`True` rows=`17`
- split_testA: `b_class_auxiliary/coding_guards/01_04_full_chain_reproduction/batches/reproduction_20260724_originalflow_r01/01_data/splits/glas_testA60.csv` exists=`True` rows=`60`
- split_testB: `b_class_auxiliary/coding_guards/01_04_full_chain_reproduction/batches/reproduction_20260724_originalflow_r01/01_data/splits/glas_testB20.csv` exists=`True` rows=`20`
- conclusion: `all frozen dataset assets required by this config exist`

## data_stage_gates
- pass_pair: `True`
- pass_label: `True`
- pass_binary_mask: `True`
- pass_dtype: `True`
- pass_resize_rule: `True`
- pass_boundary_target: `True`
- pass_distance_target: `True`
- pass_check: `True`
- manual_audit_status: `pass`
- pass_preview: `True`
- pass_config: `True`
- pass_source: `True`
- handoff_ready: `True`
- assets_traceable: `True`
- protocol_explainable: `True`
- data_stage_pass: `True`
- preflight_pass: `True`
- next_action: `enter_02_unet`
