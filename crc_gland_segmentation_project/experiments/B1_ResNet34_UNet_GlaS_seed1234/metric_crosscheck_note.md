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
- `objdice`: sample_mean=`0.8719888321898611` / aggregate=`0.8719888321898609` / status=`pass`
- `dice`: sample_mean=`0.9225763055651994` / aggregate=`0.9225763055651995` / status=`pass`
- `iou`: sample_mean=`0.8617442399778525` / aggregate=`0.8617442399778525` / status=`pass`
- `f1`: sample_mean=`0.8172626075660017` / aggregate=`0.8172626075660019` / status=`pass`
- `boundary_f1`: sample_mean=`0.7830112796176444` / aggregate=`0.7830112796176442` / status=`pass`
- `hd95`: sample_mean=`32.541906167666106` / aggregate=`32.541906167666106` / status=`pass`
- `object_hausdorff`: sample_mean=`52.8654593096799` / aggregate=`52.86545930967987` / status=`pass`

### testB

- sample_count: `20`
- sampled_ids: `GlaS_official_testB_testB_1, GlaS_official_testB_testB_10, GlaS_official_testB_testB_11, GlaS_official_testB_testB_12, GlaS_official_testB_testB_13`
- `objdice`: sample_mean=`0.8247811015736953` / aggregate=`0.8247811015736953` / status=`pass`
- `dice`: sample_mean=`0.9000434600010326` / aggregate=`0.9000434600010326` / status=`pass`
- `iou`: sample_mean=`0.8303649776647711` / aggregate=`0.8303649776647711` / status=`pass`
- `f1`: sample_mean=`0.7477888124946948` / aggregate=`0.7477888124946948` / status=`pass`
- `boundary_f1`: sample_mean=`0.6970412635438533` / aggregate=`0.6970412635438532` / status=`pass`
- `hd95`: sample_mean=`30.677179839611036` / aggregate=`30.677179839611036` / status=`pass`
- `object_hausdorff`: sample_mean=`94.20404675678613` / aggregate=`94.20404675678613` / status=`pass`

