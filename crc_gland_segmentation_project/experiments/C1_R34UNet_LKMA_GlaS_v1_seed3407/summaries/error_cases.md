# Error Cases

- failure_taxonomy_version: `failure_taxonomy_v1`
- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`
- analyzed_sample_count: `80`

## Split Summary

### testA

- sample_count: `60`
- adhesion_merge: `38`
- unclassified: `15`
- fragmented_complex_region: `5`
- small_gland_miss: `2`

### testB

- sample_count: `20`
- unclassified: `9`
- adhesion_merge: `8`
- fragmented_complex_region: `1`
- boundary_over_smooth: `1`
- small_gland_miss: `1`

## Worst Cases

- `testB` / `GlaS_official_testB_testB_16` / `failure_type=adhesion_merge` / `objdice=0.291872` / `dice=0.788361` / `boundary_f1=0.402332` / `overlay=experiments/C1_R34UNet_LKMA_GlaS_v1_seed3407/visuals/testB/GlaS_official_testB_testB_16_overlay.png`
- `testB` / `GlaS_official_testB_testB_9` / `failure_type=adhesion_merge` / `objdice=0.365654` / `dice=0.707844` / `boundary_f1=0.302960` / `overlay=experiments/C1_R34UNet_LKMA_GlaS_v1_seed3407/visuals/testB/GlaS_official_testB_testB_9_overlay.png`
- `testA` / `GlaS_official_testA_testA_22` / `failure_type=adhesion_merge` / `objdice=0.635098` / `dice=0.867496` / `boundary_f1=0.573665` / `overlay=experiments/C1_R34UNet_LKMA_GlaS_v1_seed3407/visuals/testA/GlaS_official_testA_testA_22_overlay.png`
- `testA` / `GlaS_official_testA_testA_24` / `failure_type=adhesion_merge` / `objdice=0.648287` / `dice=0.890242` / `boundary_f1=0.623165` / `overlay=experiments/C1_R34UNet_LKMA_GlaS_v1_seed3407/visuals/testA/GlaS_official_testA_testA_24_overlay.png`
- `testB` / `GlaS_official_testB_testB_14` / `failure_type=boundary_over_smooth` / `objdice=0.656515` / `dice=0.694413` / `boundary_f1=0.377670` / `overlay=experiments/C1_R34UNet_LKMA_GlaS_v1_seed3407/visuals/testB/GlaS_official_testB_testB_14_overlay.png`
- `testA` / `GlaS_official_testA_testA_21` / `failure_type=adhesion_merge` / `objdice=0.663018` / `dice=0.762555` / `boundary_f1=0.611270` / `overlay=experiments/C1_R34UNet_LKMA_GlaS_v1_seed3407/visuals/testA/GlaS_official_testA_testA_21_overlay.png`
