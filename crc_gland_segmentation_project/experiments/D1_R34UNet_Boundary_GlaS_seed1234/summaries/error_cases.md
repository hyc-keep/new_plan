# Error Cases

- failure_taxonomy_version: `failure_taxonomy_v1`
- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`
- analyzed_sample_count: `80`

## Split Summary

### testA

- sample_count: `60`
- adhesion_merge: `38`
- unclassified: `19`
- fragmented_complex_region: `2`
- small_gland_miss: `1`

### testB

- sample_count: `20`
- unclassified: `10`
- adhesion_merge: `8`
- fragmented_complex_region: `1`
- small_gland_miss: `1`

## Worst Cases

- `testB` / `GlaS_official_testB_testB_16` / `failure_type=adhesion_merge` / `objdice=0.343475` / `dice=0.783178` / `boundary_f1=0.342868` / `overlay=experiments/D1_R34UNet_Boundary_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_16_overlay.png`
- `testB` / `GlaS_official_testB_testB_9` / `failure_type=adhesion_merge` / `objdice=0.394616` / `dice=0.744975` / `boundary_f1=0.341907` / `overlay=experiments/D1_R34UNet_Boundary_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_9_overlay.png`
- `testA` / `GlaS_official_testA_testA_1` / `failure_type=adhesion_merge` / `objdice=0.548056` / `dice=0.662780` / `boundary_f1=0.492657` / `overlay=experiments/D1_R34UNet_Boundary_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_1_overlay.png`
- `testA` / `GlaS_official_testA_testA_54` / `failure_type=adhesion_merge` / `objdice=0.550544` / `dice=0.900116` / `boundary_f1=0.730387` / `overlay=experiments/D1_R34UNet_Boundary_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_54_overlay.png`
- `testA` / `GlaS_official_testA_testA_24` / `failure_type=adhesion_merge` / `objdice=0.642475` / `dice=0.900154` / `boundary_f1=0.637743` / `overlay=experiments/D1_R34UNet_Boundary_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_24_overlay.png`
- `testA` / `GlaS_official_testA_testA_15` / `failure_type=unclassified` / `objdice=0.669452` / `dice=0.679452` / `boundary_f1=0.531060` / `overlay=experiments/D1_R34UNet_Boundary_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_15_overlay.png`
