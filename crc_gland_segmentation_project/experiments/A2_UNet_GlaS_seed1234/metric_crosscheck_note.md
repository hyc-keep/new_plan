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
- `objdice`: sample_mean=`0.774237022569451` / aggregate=`0.7742370225694508` / status=`pass`
- `dice`: sample_mean=`0.8996815899009153` / aggregate=`0.8996815899009152` / status=`pass`
- `iou`: sample_mean=`0.8251476269685268` / aggregate=`0.825147626968527` / status=`pass`
- `f1`: sample_mean=`0.6281392603190142` / aggregate=`0.6281392603190141` / status=`pass`
- `boundary_f1`: sample_mean=`0.7014070651677436` / aggregate=`0.7014070651677436` / status=`pass`
- `hd95`: sample_mean=`45.182960805892925` / aggregate=`45.18296080589292` / status=`pass`
- `object_hausdorff`: sample_mean=`96.33649186516604` / aggregate=`96.33649186516602` / status=`pass`

### testB

- sample_count: `20`
- sampled_ids: `GlaS_official_testB_testB_1, GlaS_official_testB_testB_10, GlaS_official_testB_testB_11, GlaS_official_testB_testB_12, GlaS_official_testB_testB_13`
- `objdice`: sample_mean=`0.7895621971122486` / aggregate=`0.7895621971122486` / status=`pass`
- `dice`: sample_mean=`0.8818913866593171` / aggregate=`0.8818913866593171` / status=`pass`
- `iou`: sample_mean=`0.7986724250211884` / aggregate=`0.7986724250211885` / status=`pass`
- `f1`: sample_mean=`0.6182303803008136` / aggregate=`0.6182303803008137` / status=`pass`
- `boundary_f1`: sample_mean=`0.6401471501436056` / aggregate=`0.6401471501436056` / status=`pass`
- `hd95`: sample_mean=`40.76784465074538` / aggregate=`40.76784465074538` / status=`pass`
- `object_hausdorff`: sample_mean=`113.44343735504432` / aggregate=`113.44343735504432` / status=`pass`

