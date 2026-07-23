# Error Cases

- failure_taxonomy_version: `failure_taxonomy_v1`
- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`
- analyzed_sample_count: `4`

## Split Summary

### testA

- sample_count: `2`
- all_background: `2`

### testB

- sample_count: `2`
- all_background: `2`

## Worst Cases

- `testA` / `GlaS_official_testA_testA_1` / `failure_type=all_background` / `objdice=0.000000` / `dice=0.000000` / `boundary_f1=0.000000` / `overlay=experiments/C1_R34UNet_LKMA_GlaS_v1_seed3407__smoke/visuals/testA/GlaS_official_testA_testA_1_overlay.png`
- `testA` / `GlaS_official_testA_testA_10` / `failure_type=all_background` / `objdice=0.000000` / `dice=0.000000` / `boundary_f1=0.000000` / `overlay=not_exported`
- `testB` / `GlaS_official_testB_testB_1` / `failure_type=all_background` / `objdice=0.000000` / `dice=0.000000` / `boundary_f1=0.000000` / `overlay=experiments/C1_R34UNet_LKMA_GlaS_v1_seed3407__smoke/visuals/testB/GlaS_official_testB_testB_1_overlay.png`
- `testB` / `GlaS_official_testB_testB_10` / `failure_type=all_background` / `objdice=0.000000` / `dice=0.000000` / `boundary_f1=0.000000` / `overlay=not_exported`
