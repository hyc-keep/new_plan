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
- `objdice`: sample_mean=`0.8080344212211815` / aggregate=`0.8080344212211816` / status=`pass`
- `dice`: sample_mean=`0.9108007798030447` / aggregate=`0.910800779803045` / status=`pass`
- `iou`: sample_mean=`0.845066020204913` / aggregate=`0.845066020204913` / status=`pass`
- `f1`: sample_mean=`0.7214907114386581` / aggregate=`0.7214907114386582` / status=`pass`
- `boundary_f1`: sample_mean=`0.7449741249121673` / aggregate=`0.7449741249121673` / status=`pass`
- `hd95`: sample_mean=`32.80215909361837` / aggregate=`32.80215909361837` / status=`pass`
- `object_hausdorff`: sample_mean=`82.39250045049728` / aggregate=`82.3925004504973` / status=`pass`

### testB

- sample_count: `20`
- sampled_ids: `GlaS_official_testB_testB_1, GlaS_official_testB_testB_10, GlaS_official_testB_testB_11, GlaS_official_testB_testB_12, GlaS_official_testB_testB_13`
- `objdice`: sample_mean=`0.817087810391729` / aggregate=`0.8170878103917291` / status=`pass`
- `dice`: sample_mean=`0.9019949843346806` / aggregate=`0.9019949843346804` / status=`pass`
- `iou`: sample_mean=`0.832735392184907` / aggregate=`0.832735392184907` / status=`pass`
- `f1`: sample_mean=`0.6695441307058954` / aggregate=`0.6695441307058954` / status=`pass`
- `boundary_f1`: sample_mean=`0.694492336680715` / aggregate=`0.6944923366807151` / status=`pass`
- `hd95`: sample_mean=`31.968905696868894` / aggregate=`31.968905696868894` / status=`pass`
- `object_hausdorff`: sample_mean=`98.86045188281088` / aggregate=`98.86045188281086` / status=`pass`

