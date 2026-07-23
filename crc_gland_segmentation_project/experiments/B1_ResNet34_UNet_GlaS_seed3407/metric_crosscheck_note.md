# Metric Crosscheck Note

- crosscheck_scope: `python_reaggregation_from_split_csv`
- official_reference_type: `project_internal_reaggregation_sanity_check`
- threshold_source: `val17`
- threshold_value: `0.5`
- metric_crosscheck_result: `pass`
- boundary_metric_width: `3`
- boundary_metric_impl: `binary_erosion_xor_plus_binary_dilation`
- connected_components_connectivity: `8`

## Split Checks

### testA

- sample_count: `60`
- sampled_ids: `GlaS_official_testA_testA_1, GlaS_official_testA_testA_10, GlaS_official_testA_testA_11, GlaS_official_testA_testA_12, GlaS_official_testA_testA_13`
- `objdice`: sample_mean=`0.7959707472837643` / aggregate=`0.7959707472837647` / status=`pass`
- `dice`: sample_mean=`0.9036527392470665` / aggregate=`0.9036527392470662` / status=`pass`
- `iou`: sample_mean=`0.8312296136450056` / aggregate=`0.8312296136450056` / status=`pass`
- `f1`: sample_mean=`0.6572524065359923` / aggregate=`0.6572524065359922` / status=`pass`
- `boundary_f1`: sample_mean=`0.7200427504106368` / aggregate=`0.7200427504106367` / status=`pass`
- `hd95`: sample_mean=`38.006063938140855` / aggregate=`38.006063938140855` / status=`pass`
- `object_hausdorff`: sample_mean=`83.95235218913025` / aggregate=`83.95235218913022` / status=`pass`

### testB

- sample_count: `20`
- sampled_ids: `GlaS_official_testB_testB_1, GlaS_official_testB_testB_10, GlaS_official_testB_testB_11, GlaS_official_testB_testB_12, GlaS_official_testB_testB_13`
- `objdice`: sample_mean=`0.8326697028206805` / aggregate=`0.8326697028206805` / status=`pass`
- `dice`: sample_mean=`0.9142674232453535` / aggregate=`0.9142674232453535` / status=`pass`
- `iou`: sample_mean=`0.8490353314889122` / aggregate=`0.8490353314889122` / status=`pass`
- `f1`: sample_mean=`0.6666923917156117` / aggregate=`0.6666923917156116` / status=`pass`
- `boundary_f1`: sample_mean=`0.702122865075256` / aggregate=`0.7021228650752559` / status=`pass`
- `hd95`: sample_mean=`30.29373172044752` / aggregate=`30.29373172044753` / status=`pass`
- `object_hausdorff`: sample_mean=`97.55786113495802` / aggregate=`97.55786113495802` / status=`pass`

