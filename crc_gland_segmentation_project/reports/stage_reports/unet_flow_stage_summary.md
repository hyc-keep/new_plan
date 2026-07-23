# UNet Flow Stage Summary

## 1. Inputs
- run_dir: `experiments/A1_UNet_GlaS_v1_seed3407`
- run_meta: `experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`
- run_summary: `experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md`
- debug_note: `notes/debug_note.md`

## 2. Gate Status
- pass_train: `true`
- pass_val: `true`
- pass_test: `true`
- pass_eval: `true`
- pass_visual: `true`
- pass_record: `true`
- stage_pass: `true`
- protocol_error: `false`
- freeze_status: `true`
- handoff_ready_for_a2: `true`
- next_action: `enter_03_unet_stability`

## 3. Current Baseline Identity
- source_stage: `02_UNet流程验证`
- source_run_name: `A1_UNet_GlaS_v1_seed3407`
- source_run_meta: `experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`
- device: `cuda`
- amp_active: `true`
- best_selector: `val_objdice_max`
- best_epoch: `50`
- epoch_count: `70`
- stop_reason: `early_stopping`

## 4. Split Counts
- testA_expected_count: `60`
- testA_actual_count: `60`
- testB_expected_count: `20`
- testB_actual_count: `20`

## 5. Blocking Reasons
- none

## 6. Conclusion
- truthful_interpretation: current stage summary confirms formal stage02 closure: non-smoke A1 training ended normally, full TestA60/TestB20 are present, evaluation and visual assets are aligned, and handoff is ready for stage03.
