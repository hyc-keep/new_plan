# Error Cases

- failure_taxonomy_version: `failure_taxonomy_v1`
- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`
- analyzed_sample_count: `80`

## Split Summary

### testA

- sample_count: `60`
- adhesion_merge: `48`
- fragmented_complex_region: `9`
- unclassified: `2`
- boundary_over_smooth: `1`

### testB

- sample_count: `20`
- adhesion_merge: `10`
- unclassified: `5`
- fragmented_complex_region: `3`
- boundary_over_smooth: `1`
- small_gland_miss: `1`

## Worst Cases

- `testA` / `GlaS_official_testA_testA_43` / `failure_type=adhesion_merge` / `objdice=0.287083` / `dice=0.926861` / `boundary_f1=0.681828` / `overlay=experiments/A2_UNet_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_43_overlay.png`
- `testA` / `GlaS_official_testA_testA_10` / `failure_type=adhesion_merge` / `objdice=0.323626` / `dice=0.831698` / `boundary_f1=0.482860` / `overlay=experiments/A2_UNet_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_10_overlay.png`
- `testA` / `GlaS_official_testA_testA_1` / `failure_type=adhesion_merge` / `objdice=0.325057` / `dice=0.657468` / `boundary_f1=0.367505` / `overlay=experiments/A2_UNet_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_1_overlay.png`
- `testA` / `GlaS_official_testA_testA_54` / `failure_type=adhesion_merge` / `objdice=0.333979` / `dice=0.880794` / `boundary_f1=0.535680` / `overlay=experiments/A2_UNet_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_54_overlay.png`
- `testA` / `GlaS_official_testA_testA_45` / `failure_type=adhesion_merge` / `objdice=0.347011` / `dice=0.734705` / `boundary_f1=0.284913` / `overlay=experiments/A2_UNet_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_45_overlay.png`
- `testB` / `GlaS_official_testB_testB_16` / `failure_type=adhesion_merge` / `objdice=0.356588` / `dice=0.785831` / `boundary_f1=0.358120` / `overlay=experiments/A2_UNet_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_16_overlay.png`
