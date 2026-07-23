# Error Cases

- failure_taxonomy_version: `failure_taxonomy_v1`
- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`
- analyzed_sample_count: `80`

## Split Summary

### testA

- sample_count: `60`
- adhesion_merge: `41`
- unclassified: `15`
- fragmented_complex_region: `3`
- small_gland_miss: `1`

### testB

- sample_count: `20`
- unclassified: `9`
- adhesion_merge: `8`
- fragmented_complex_region: `1`
- boundary_over_smooth: `1`
- small_gland_miss: `1`

## Worst Cases

- `testA` / `GlaS_official_testA_testA_21` / `failure_type=adhesion_merge` / `objdice=0.189540` / `dice=0.707686` / `boundary_f1=0.538020` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_21_overlay.png`
- `testB` / `GlaS_official_testB_testB_16` / `failure_type=adhesion_merge` / `objdice=0.313502` / `dice=0.780246` / `boundary_f1=0.386362` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_16_overlay.png`
- `testB` / `GlaS_official_testB_testB_9` / `failure_type=adhesion_merge` / `objdice=0.427103` / `dice=0.790780` / `boundary_f1=0.379834` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_9_overlay.png`
- `testA` / `GlaS_official_testA_testA_18` / `failure_type=adhesion_merge` / `objdice=0.452215` / `dice=0.727816` / `boundary_f1=0.498525` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_18_overlay.png`
- `testA` / `GlaS_official_testA_testA_45` / `failure_type=adhesion_merge` / `objdice=0.566606` / `dice=0.860896` / `boundary_f1=0.554814` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_45_overlay.png`
- `testA` / `GlaS_official_testA_testA_15` / `failure_type=adhesion_merge` / `objdice=0.567127` / `dice=0.696615` / `boundary_f1=0.554283` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_15_overlay.png`
