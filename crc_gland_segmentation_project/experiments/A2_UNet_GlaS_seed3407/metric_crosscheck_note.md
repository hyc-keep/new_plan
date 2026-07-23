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
- `objdice`: sample_mean=`0.6985296230265656` / aggregate=`0.6985296230265656` / status=`pass`
- `dice`: sample_mean=`0.8622817317003199` / aggregate=`0.8622817317003201` / status=`pass`
- `iou`: sample_mean=`0.767883963059051` / aggregate=`0.7678839630590509` / status=`pass`
- `f1`: sample_mean=`0.46511982476602637` / aggregate=`0.4651198247660265` / status=`pass`
- `boundary_f1`: sample_mean=`0.6006110924568391` / aggregate=`0.6006110924568391` / status=`pass`
- `hd95`: sample_mean=`59.36049590110777` / aggregate=`59.360495901107775` / status=`pass`
- `object_hausdorff`: sample_mean=`130.164214440302` / aggregate=`130.16421444030203` / status=`pass`

### testB

- sample_count: `20`
- sampled_ids: `GlaS_official_testB_testB_1, GlaS_official_testB_testB_10, GlaS_official_testB_testB_11, GlaS_official_testB_testB_12, GlaS_official_testB_testB_13`
- `objdice`: sample_mean=`0.7554450357666719` / aggregate=`0.7554450357666719` / status=`pass`
- `dice`: sample_mean=`0.8651023657298401` / aggregate=`0.8651023657298401` / status=`pass`
- `iou`: sample_mean=`0.7756160389465188` / aggregate=`0.7756160389465188` / status=`pass`
- `f1`: sample_mean=`0.4998039097125783` / aggregate=`0.49980390971257843` / status=`pass`
- `boundary_f1`: sample_mean=`0.598653420257438` / aggregate=`0.5986534202574381` / status=`pass`
- `hd95`: sample_mean=`50.1383007788658` / aggregate=`50.1383007788658` / status=`pass`
- `object_hausdorff`: sample_mean=`134.2456336962769` / aggregate=`134.2456336962769` / status=`pass`

