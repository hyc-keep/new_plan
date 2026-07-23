# Error Cases

- failure_taxonomy_version: `failure_taxonomy_v1`
- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`
- analyzed_sample_count: `80`

## Split Summary

### testA

- sample_count: `60`
- adhesion_merge: `40`
- unclassified: `14`
- fragmented_complex_region: `5`
- small_gland_miss: `1`

### testB

- sample_count: `20`
- unclassified: `9`
- adhesion_merge: `8`
- fragmented_complex_region: `1`
- boundary_over_smooth: `1`
- small_gland_miss: `1`

## Worst Cases

- `testB` / `GlaS_official_testB_testB_16` / `failure_type=adhesion_merge` / `objdice=0.319474` / `dice=0.806441` / `boundary_f1=0.405902` / `overlay=experiments/C1_R34UNet_LKMA_GlaS_v1_seed2025/visuals/testB/GlaS_official_testB_testB_16_overlay.png`
- `testB` / `GlaS_official_testB_testB_9` / `failure_type=adhesion_merge` / `objdice=0.401114` / `dice=0.769282` / `boundary_f1=0.418691` / `overlay=experiments/C1_R34UNet_LKMA_GlaS_v1_seed2025/visuals/testB/GlaS_official_testB_testB_9_overlay.png`
- `testA` / `GlaS_official_testA_testA_45` / `failure_type=adhesion_merge` / `objdice=0.490770` / `dice=0.868059` / `boundary_f1=0.485458` / `overlay=experiments/C1_R34UNet_LKMA_GlaS_v1_seed2025/visuals/testA/GlaS_official_testA_testA_45_overlay.png`
- `testB` / `GlaS_official_testB_testB_14` / `failure_type=boundary_over_smooth` / `objdice=0.512226` / `dice=0.612450` / `boundary_f1=0.324307` / `overlay=experiments/C1_R34UNet_LKMA_GlaS_v1_seed2025/visuals/testB/GlaS_official_testB_testB_14_overlay.png`
- `testA` / `GlaS_official_testA_testA_1` / `failure_type=adhesion_merge` / `objdice=0.524404` / `dice=0.753553` / `boundary_f1=0.536437` / `overlay=experiments/C1_R34UNet_LKMA_GlaS_v1_seed2025/visuals/testA/GlaS_official_testA_testA_1_overlay.png`
- `testA` / `GlaS_official_testA_testA_10` / `failure_type=adhesion_merge` / `objdice=0.538356` / `dice=0.801638` / `boundary_f1=0.562600` / `overlay=experiments/C1_R34UNet_LKMA_GlaS_v1_seed2025/visuals/testA/GlaS_official_testA_testA_10_overlay.png`
