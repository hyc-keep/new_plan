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
- `objdice`: sample_mean=`0.23105729278997494` / aggregate=`0.23105729278997492` / status=`pass`
- `dice`: sample_mean=`0.6416920803500991` / aggregate=`0.641692080350099` / status=`pass`
- `iou`: sample_mean=`0.49413102468047804` / aggregate=`0.4941310246804778` / status=`pass`
- `f1`: sample_mean=`0.24325715487122992` / aggregate=`0.24325715487122992` / status=`pass`
- `boundary_f1`: sample_mean=`0.26235674350526617` / aggregate=`0.2623567435052662` / status=`pass`
- `hd95`: sample_mean=`201.5297032546997` / aggregate=`201.52970325469968` / status=`pass`
- `object_hausdorff`: sample_mean=`414.1260037113495` / aggregate=`414.1260037113495` / status=`pass`

### testB

- sample_count: `20`
- sampled_ids: `GlaS_official_testB_testB_1, GlaS_official_testB_testB_10, GlaS_official_testB_testB_11, GlaS_official_testB_testB_12, GlaS_official_testB_testB_13`
- `objdice`: sample_mean=`0.388626992804233` / aggregate=`0.38862699280423296` / status=`pass`
- `dice`: sample_mean=`0.7161994719503373` / aggregate=`0.7161994719503372` / status=`pass`
- `iou`: sample_mean=`0.5658138275163046` / aggregate=`0.5658138275163047` / status=`pass`
- `f1`: sample_mean=`0.32365079365079363` / aggregate=`0.32365079365079363` / status=`pass`
- `boundary_f1`: sample_mean=`0.32110368566062075` / aggregate=`0.32110368566062075` / status=`pass`
- `hd95`: sample_mean=`186.86994441986081` / aggregate=`186.86994441986081` / status=`pass`
- `object_hausdorff`: sample_mean=`365.2423337558197` / aggregate=`365.2423337558197` / status=`pass`

