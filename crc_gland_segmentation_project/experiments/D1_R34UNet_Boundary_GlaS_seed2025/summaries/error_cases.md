# Error Cases

- failure_taxonomy_version: `failure_taxonomy_v1`
- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`
- analyzed_sample_count: `80`

## Split Summary

### testA

- sample_count: `60`
- adhesion_merge: `42`
- unclassified: `13`
- fragmented_complex_region: `4`
- small_gland_miss: `1`

### testB

- sample_count: `20`
- unclassified: `9`
- adhesion_merge: `9`
- fragmented_complex_region: `1`
- small_gland_miss: `1`

## Worst Cases

- `testB` / `GlaS_official_testB_testB_16` / `failure_type=adhesion_merge` / `objdice=0.299872` / `dice=0.761811` / `boundary_f1=0.376742` / `overlay=experiments/D1_R34UNet_Boundary_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_16_overlay.png`
- `testB` / `GlaS_official_testB_testB_9` / `failure_type=adhesion_merge` / `objdice=0.462335` / `dice=0.781236` / `boundary_f1=0.401771` / `overlay=experiments/D1_R34UNet_Boundary_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_9_overlay.png`
- `testA` / `GlaS_official_testA_testA_7` / `failure_type=adhesion_merge` / `objdice=0.526476` / `dice=0.781721` / `boundary_f1=0.673564` / `overlay=experiments/D1_R34UNet_Boundary_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_7_overlay.png`
- `testA` / `GlaS_official_testA_testA_15` / `failure_type=adhesion_merge` / `objdice=0.580420` / `dice=0.700983` / `boundary_f1=0.511712` / `overlay=experiments/D1_R34UNet_Boundary_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_15_overlay.png`
- `testA` / `GlaS_official_testA_testA_10` / `failure_type=adhesion_merge` / `objdice=0.587919` / `dice=0.852281` / `boundary_f1=0.607104` / `overlay=experiments/D1_R34UNet_Boundary_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_10_overlay.png`
- `testA` / `GlaS_official_testA_testA_1` / `failure_type=adhesion_merge` / `objdice=0.609214` / `dice=0.970997` / `boundary_f1=0.738567` / `overlay=experiments/D1_R34UNet_Boundary_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_1_overlay.png`
