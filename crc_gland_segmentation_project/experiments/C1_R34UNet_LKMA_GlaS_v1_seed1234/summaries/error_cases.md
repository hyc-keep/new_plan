# Error Cases

- failure_taxonomy_version: `failure_taxonomy_v1`
- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`
- analyzed_sample_count: `80`

## Split Summary

### testA

- sample_count: `60`
- adhesion_merge: `38`
- unclassified: `17`
- fragmented_complex_region: `3`
- small_gland_miss: `2`

### testB

- sample_count: `20`
- adhesion_merge: `9`
- unclassified: `8`
- fragmented_complex_region: `2`
- small_gland_miss: `1`

## Worst Cases

- `testB` / `GlaS_official_testB_testB_16` / `failure_type=adhesion_merge` / `objdice=0.306987` / `dice=0.772589` / `boundary_f1=0.370915` / `overlay=experiments/C1_R34UNet_LKMA_GlaS_v1_seed1234/visuals/testB/GlaS_official_testB_testB_16_overlay.png`
- `testB` / `GlaS_official_testB_testB_9` / `failure_type=adhesion_merge` / `objdice=0.414481` / `dice=0.770756` / `boundary_f1=0.385419` / `overlay=experiments/C1_R34UNet_LKMA_GlaS_v1_seed1234/visuals/testB/GlaS_official_testB_testB_9_overlay.png`
- `testA` / `GlaS_official_testA_testA_1` / `failure_type=adhesion_merge` / `objdice=0.454104` / `dice=0.856579` / `boundary_f1=0.615716` / `overlay=experiments/C1_R34UNet_LKMA_GlaS_v1_seed1234/visuals/testA/GlaS_official_testA_testA_1_overlay.png`
- `testA` / `GlaS_official_testA_testA_10` / `failure_type=adhesion_merge` / `objdice=0.588452` / `dice=0.844770` / `boundary_f1=0.625394` / `overlay=experiments/C1_R34UNet_LKMA_GlaS_v1_seed1234/visuals/testA/GlaS_official_testA_testA_10_overlay.png`
- `testA` / `GlaS_official_testA_testA_45` / `failure_type=adhesion_merge` / `objdice=0.612116` / `dice=0.861084` / `boundary_f1=0.552473` / `overlay=experiments/C1_R34UNet_LKMA_GlaS_v1_seed1234/visuals/testA/GlaS_official_testA_testA_45_overlay.png`
- `testA` / `GlaS_official_testA_testA_24` / `failure_type=adhesion_merge` / `objdice=0.613988` / `dice=0.877663` / `boundary_f1=0.612176` / `overlay=experiments/C1_R34UNet_LKMA_GlaS_v1_seed1234/visuals/testA/GlaS_official_testA_testA_24_overlay.png`
