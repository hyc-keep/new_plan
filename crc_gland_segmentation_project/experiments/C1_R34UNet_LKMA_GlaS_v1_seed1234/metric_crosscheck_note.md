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
- `objdice`: sample_mean=`0.837558837665939` / aggregate=`0.8375588376659384` / status=`pass`
- `dice`: sample_mean=`0.9257540168768805` / aggregate=`0.9257540168768806` / status=`pass`
- `iou`: sample_mean=`0.8656603944025113` / aggregate=`0.8656603944025114` / status=`pass`
- `f1`: sample_mean=`0.7637934967607131` / aggregate=`0.7637934967607134` / status=`pass`
- `boundary_f1`: sample_mean=`0.772961093323563` / aggregate=`0.7729610933235629` / status=`pass`
- `hd95`: sample_mean=`34.08705036083855` / aggregate=`34.08705036083856` / status=`pass`
- `object_hausdorff`: sample_mean=`72.3558254591515` / aggregate=`72.3558254591515` / status=`pass`

### testB

- sample_count: `20`
- sampled_ids: `GlaS_official_testB_testB_1, GlaS_official_testB_testB_10, GlaS_official_testB_testB_11, GlaS_official_testB_testB_12, GlaS_official_testB_testB_13`
- `objdice`: sample_mean=`0.823401122216389` / aggregate=`0.823401122216389` / status=`pass`
- `dice`: sample_mean=`0.9081687013127933` / aggregate=`0.9081687013127933` / status=`pass`
- `iou`: sample_mean=`0.8400432999085382` / aggregate=`0.8400432999085382` / status=`pass`
- `f1`: sample_mean=`0.7085618479387829` / aggregate=`0.7085618479387829` / status=`pass`
- `boundary_f1`: sample_mean=`0.7045960006327577` / aggregate=`0.7045960006327577` / status=`pass`
- `hd95`: sample_mean=`31.287384314537036` / aggregate=`31.287384314537036` / status=`pass`
- `object_hausdorff`: sample_mean=`98.85585318016743` / aggregate=`98.85585318016741` / status=`pass`

