# Error Cases

- failure_taxonomy_version: `failure_taxonomy_v1`
- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`
- analyzed_sample_count: `80`

## Split Summary

### testA

- sample_count: `60`
- adhesion_merge: `41`
- fragmented_complex_region: `10`
- unclassified: `8`
- small_gland_miss: `1`

### testB

- sample_count: `20`
- adhesion_merge: `11`
- unclassified: `6`
- fragmented_complex_region: `2`
- small_gland_miss: `1`

## Worst Cases

- `testB` / `GlaS_official_testB_testB_16` / `failure_type=adhesion_merge` / `objdice=0.313636` / `dice=0.817479` / `boundary_f1=0.436187` / `overlay=experiments/B1_ResNet34_UNet_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_16_overlay.png`
- `testA` / `GlaS_official_testA_testA_1` / `failure_type=adhesion_merge` / `objdice=0.387728` / `dice=0.740905` / `boundary_f1=0.440197` / `overlay=experiments/B1_ResNet34_UNet_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_1_overlay.png`
- `testB` / `GlaS_official_testB_testB_9` / `failure_type=adhesion_merge` / `objdice=0.444447` / `dice=0.778595` / `boundary_f1=0.426704` / `overlay=experiments/B1_ResNet34_UNet_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_9_overlay.png`
- `testA` / `GlaS_official_testA_testA_7` / `failure_type=adhesion_merge` / `objdice=0.509216` / `dice=0.765195` / `boundary_f1=0.653345` / `overlay=experiments/B1_ResNet34_UNet_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_7_overlay.png`
- `testA` / `GlaS_official_testA_testA_32` / `failure_type=adhesion_merge` / `objdice=0.567134` / `dice=0.733503` / `boundary_f1=0.588928` / `overlay=experiments/B1_ResNet34_UNet_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_32_overlay.png`
- `testA` / `GlaS_official_testA_testA_10` / `failure_type=adhesion_merge` / `objdice=0.573628` / `dice=0.844344` / `boundary_f1=0.617163` / `overlay=experiments/B1_ResNet34_UNet_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_10_overlay.png`
