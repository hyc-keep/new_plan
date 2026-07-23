# Error Cases

- failure_taxonomy_version: `failure_taxonomy_v1`
- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`
- analyzed_sample_count: `80`

## Split Summary

### testA

- sample_count: `60`
- adhesion_merge: `37`
- unclassified: `18`
- fragmented_complex_region: `3`
- small_gland_miss: `2`

### testB

- sample_count: `20`
- unclassified: `9`
- adhesion_merge: `8`
- boundary_over_smooth: `1`
- small_gland_miss: `1`
- fragmented_complex_region: `1`

## Worst Cases

- `testB` / `GlaS_official_testB_testB_16` / `failure_type=adhesion_merge` / `objdice=0.312684` / `dice=0.780044` / `boundary_f1=0.387229` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_16_overlay.png`
- `testB` / `GlaS_official_testB_testB_9` / `failure_type=adhesion_merge` / `objdice=0.427067` / `dice=0.797344` / `boundary_f1=0.437668` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_9_overlay.png`
- `testA` / `GlaS_official_testA_testA_1` / `failure_type=adhesion_merge` / `objdice=0.516038` / `dice=0.533128` / `boundary_f1=0.496113` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_1_overlay.png`
- `testA` / `GlaS_official_testA_testA_7` / `failure_type=adhesion_merge` / `objdice=0.598283` / `dice=0.741745` / `boundary_f1=0.687725` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_7_overlay.png`
- `testB` / `GlaS_official_testB_testB_14` / `failure_type=boundary_over_smooth` / `objdice=0.642331` / `dice=0.691510` / `boundary_f1=0.394433` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_14_overlay.png`
- `testA` / `GlaS_official_testA_testA_31` / `failure_type=adhesion_merge` / `objdice=0.676140` / `dice=0.974093` / `boundary_f1=0.926455` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_31_overlay.png`
