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
- `objdice`: sample_mean=`0.8167102126416362` / aggregate=`0.8167102126416363` / status=`pass`
- `dice`: sample_mean=`0.9124893088880527` / aggregate=`0.9124893088880524` / status=`pass`
- `iou`: sample_mean=`0.8460403747335784` / aggregate=`0.8460403747335783` / status=`pass`
- `f1`: sample_mean=`0.6988948861369665` / aggregate=`0.6988948861369665` / status=`pass`
- `boundary_f1`: sample_mean=`0.748780118922816` / aggregate=`0.7487801189228162` / status=`pass`
- `hd95`: sample_mean=`32.35862205187479` / aggregate=`32.35862205187479` / status=`pass`
- `object_hausdorff`: sample_mean=`77.59987713288498` / aggregate=`77.59987713288497` / status=`pass`

### testB

- sample_count: `20`
- sampled_ids: `GlaS_official_testB_testB_1, GlaS_official_testB_testB_10, GlaS_official_testB_testB_11, GlaS_official_testB_testB_12, GlaS_official_testB_testB_13`
- `objdice`: sample_mean=`0.833227769336831` / aggregate=`0.8332277693368308` / status=`pass`
- `dice`: sample_mean=`0.9152193372187727` / aggregate=`0.9152193372187727` / status=`pass`
- `iou`: sample_mean=`0.8542149381433944` / aggregate=`0.8542149381433941` / status=`pass`
- `f1`: sample_mean=`0.7116510604978097` / aggregate=`0.7116510604978097` / status=`pass`
- `boundary_f1`: sample_mean=`0.710573510217741` / aggregate=`0.7105735102177408` / status=`pass`
- `hd95`: sample_mean=`25.81537765979765` / aggregate=`25.815377659797644` / status=`pass`
- `object_hausdorff`: sample_mean=`92.54732282952665` / aggregate=`92.54732282952665` / status=`pass`

