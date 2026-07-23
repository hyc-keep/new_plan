# Error Cases

- failure_taxonomy_version: `failure_taxonomy_v1`
- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`
- analyzed_sample_count: `80`

## Split Summary

### testA

- sample_count: `60`
- adhesion_merge: `40`
- unclassified: `15`
- fragmented_complex_region: `5`

### testB

- sample_count: `20`
- adhesion_merge: `10`
- unclassified: `6`
- fragmented_complex_region: `3`
- small_gland_miss: `1`

## Worst Cases

- `testB` / `GlaS_official_testB_testB_16` / `failure_type=adhesion_merge` / `objdice=0.275403` / `dice=0.762555` / `boundary_f1=0.399169` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_16_overlay.png`
- `testB` / `GlaS_official_testB_testB_9` / `failure_type=adhesion_merge` / `objdice=0.362074` / `dice=0.716219` / `boundary_f1=0.331492` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_9_overlay.png`
- `testA` / `GlaS_official_testA_testA_1` / `failure_type=adhesion_merge` / `objdice=0.411375` / `dice=0.416910` / `boundary_f1=0.354942` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_1_overlay.png`
- `testA` / `GlaS_official_testA_testA_54` / `failure_type=adhesion_merge` / `objdice=0.440501` / `dice=0.904158` / `boundary_f1=0.716518` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_54_overlay.png`
- `testA` / `GlaS_official_testA_testA_5` / `failure_type=adhesion_merge` / `objdice=0.514737` / `dice=0.911378` / `boundary_f1=0.657863` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_5_overlay.png`
- `testA` / `GlaS_official_testA_testA_27` / `failure_type=adhesion_merge` / `objdice=0.590077` / `dice=0.860267` / `boundary_f1=0.711144` / `overlay=experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_27_overlay.png`
