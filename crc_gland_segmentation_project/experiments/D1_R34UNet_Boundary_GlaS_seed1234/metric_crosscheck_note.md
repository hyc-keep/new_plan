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
- `objdice`: sample_mean=`0.8471165150239142` / aggregate=`0.8471165150239138` / status=`pass`
- `dice`: sample_mean=`0.9217561396164365` / aggregate=`0.9217561396164365` / status=`pass`
- `iou`: sample_mean=`0.8602692839896326` / aggregate=`0.8602692839896326` / status=`pass`
- `f1`: sample_mean=`0.790564295109169` / aggregate=`0.7905642951091695` / status=`pass`
- `boundary_f1`: sample_mean=`0.7700341854559524` / aggregate=`0.7700341854559521` / status=`pass`
- `hd95`: sample_mean=`33.113328227202075` / aggregate=`33.11332822720207` / status=`pass`
- `object_hausdorff`: sample_mean=`64.55559101494646` / aggregate=`64.55559101494649` / status=`pass`

### testB

- sample_count: `20`
- sampled_ids: `GlaS_official_testB_testB_1, GlaS_official_testB_testB_10, GlaS_official_testB_testB_11, GlaS_official_testB_testB_12, GlaS_official_testB_testB_13`
- `objdice`: sample_mean=`0.8506911535852248` / aggregate=`0.8506911535852251` / status=`pass`
- `dice`: sample_mean=`0.923017640066405` / aggregate=`0.923017640066405` / status=`pass`
- `iou`: sample_mean=`0.8650513785435144` / aggregate=`0.8650513785435143` / status=`pass`
- `f1`: sample_mean=`0.7352586465821761` / aggregate=`0.735258646582176` / status=`pass`
- `boundary_f1`: sample_mean=`0.7234117181993713` / aggregate=`0.7234117181993711` / status=`pass`
- `hd95`: sample_mean=`27.426637477874742` / aggregate=`27.42663747787474` / status=`pass`
- `object_hausdorff`: sample_mean=`86.40694616448783` / aggregate=`86.40694616448783` / status=`pass`

