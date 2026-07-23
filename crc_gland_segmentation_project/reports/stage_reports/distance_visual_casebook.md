# 07_Distance visual casebook

本文件索引脚本发现的真实 visuals 文件和对应 split 的测试指标，并单独记录有限人工视觉复核；不将有限抽查外推为整体改善判断。

## 审查状态
- 人工视觉审查：已完成有限人工复核（`visual_review_status=limited_manual_review_completed`）。
- 复核范围：仅人工抽查以下 4 张真实 overlay，属于有限抽查，非全量视觉复核；本记录不替代全量审查，也不构成 Distance 稳定改善证据。

## 人工视觉复核记录
以下观察来自对真实 overlay 的人工抽查。每张记录均明确支持或不支持结论；“支持”仅表示该图中可见对应现象，不表示支持 Distance 整体改善。

1. `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_13_overlay.png`
   - 观察：大片黄色前景覆盖，细长/狭窄结构边界偏移，局部仍有红色边缘残留。
   - 结论：不支持该样本显示出稳定的边界改善；支持存在前景覆盖与边界误差现象。
2. `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_12_overlay.png`
   - 观察：多目标/狭窄结构中黄色预测与绿色误差区域并存，局部轮廓不稳定。
   - 结论：不支持该样本显示出稳定的多目标或狭窄结构改善；支持存在局部轮廓不稳定现象。
3. `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_10_overlay.png`
   - 观察：多个腺体附近绿色区域明显，提示存在欠分割或轮廓不匹配。
   - 结论：不支持该样本显示出稳定的腺体覆盖或轮廓改善；支持存在欠分割/轮廓不匹配现象。
4. `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_14_overlay.png`
   - 观察：边缘区域大片绿色/黄色交错，存在边界偏移和前景覆盖问题。
   - 结论：不支持该样本显示出稳定的边缘改善；支持存在边界偏移与前景覆盖现象。

综上，4 张有限抽查均暴露出边界偏移、前景覆盖、欠分割或局部轮廓不稳定问题；该抽查不证明 Distance 稳定改善，亦不能据此完成全量视觉结论。

## seed 3407
### testA
- 对应测试指标均来自 `experiments/D2_R34UNet_Distance_GlaS_seed3407/testA_metrics.csv` 的 sample 行均值；共索引 20 个 PNG。
- Boundary F1=0.7671826543069215；HD95=31.98865834712981；Object Hausdorff=59.97228617237169；Object Dice=0.8529445991431763；F1=0.7701528514456251。
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_13_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_13_overlay.png`（人工审查：已完成有限抽查（非全量））
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_13_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_13_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_18_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_18_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_18_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_18_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_1_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_1_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_1_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_1_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_31_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_31_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_31_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_31_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_7_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_7_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_7_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testA/GlaS_official_testA_testA_7_raw.png`（人工审查：未执行）
### testB
- 对应测试指标均来自 `experiments/D2_R34UNet_Distance_GlaS_seed3407/testB_metrics.csv` 的 sample 行均值；共索引 20 个 PNG。
- Boundary F1=0.7219223670607018；HD95=25.906810870170585；Object Hausdorff=82.9933188195697；Object Dice=0.8509274203377449；F1=0.7309094818150546。
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_12_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_12_overlay.png`（人工审查：已完成有限抽查（非全量））
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_12_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_12_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_14_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_14_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_14_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_14_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_15_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_15_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_15_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_15_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_16_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_16_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_16_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_16_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_9_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_9_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_9_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed3407/visuals/testB/GlaS_official_testB_testB_9_raw.png`（人工审查：未执行）
## seed 1234
### testA
- 对应测试指标均来自 `experiments/D2_R34UNet_Distance_GlaS_seed1234/testA_metrics.csv` 的 sample 行均值；共索引 20 个 PNG。
- Boundary F1=0.7449741249121674；HD95=32.80215909361837；Object Hausdorff=82.39250045049731；Object Dice=0.8080344212211816；F1=0.7214907114386583。
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_10_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_10_overlay.png`（人工审查：已完成有限抽查（非全量））
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_10_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_10_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_1_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_1_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_1_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_1_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_27_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_27_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_27_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_27_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_54_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_54_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_54_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_54_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_5_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_5_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_5_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testA/GlaS_official_testA_testA_5_raw.png`（人工审查：未执行）
### testB
- 对应测试指标均来自 `experiments/D2_R34UNet_Distance_GlaS_seed1234/testB_metrics.csv` 的 sample 行均值；共索引 20 个 PNG。
- Boundary F1=0.6944923366807151；HD95=31.968905696868894；Object Hausdorff=98.86045188281086；Object Dice=0.8170878103917291；F1=0.6695441307058954。
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_12_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_12_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_12_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_12_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_14_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_14_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_14_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_14_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_16_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_16_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_16_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_16_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_19_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_19_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_19_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_19_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_9_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_9_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_9_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed1234/visuals/testB/GlaS_official_testB_testB_9_raw.png`（人工审查：未执行）
## seed 2025
### testA
- 对应测试指标均来自 `experiments/D2_R34UNet_Distance_GlaS_seed2025/testA_metrics.csv` 的 sample 行均值；共索引 20 个 PNG。
- Boundary F1=0.7569685093658918；HD95=39.502018922964716；Object Hausdorff=83.21937875849288；Object Dice=0.8180253640686928；F1=0.744299086778737。
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_15_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_15_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_15_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_15_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_18_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_18_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_18_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_18_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_21_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_21_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_21_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_21_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_24_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_24_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_24_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_24_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_45_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_45_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_45_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testA/GlaS_official_testA_testA_45_raw.png`（人工审查：未执行）
### testB
- 对应测试指标均来自 `experiments/D2_R34UNet_Distance_GlaS_seed2025/testB_metrics.csv` 的 sample 行均值；共索引 20 个 PNG。
- Boundary F1=0.7196367803585112；HD95=25.65455338001251；Object Hausdorff=90.40675429510088；Object Dice=0.8295660218362964；F1=0.7214786602286603。
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_12_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_12_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_12_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_12_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_14_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_14_overlay.png`（人工审查：已完成有限抽查（非全量））
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_14_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_14_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_16_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_16_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_16_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_16_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_2_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_2_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_2_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_2_raw.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_9_gt.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_9_overlay.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_9_pred.png`（人工审查：未执行）
- `experiments/D2_R34UNet_Distance_GlaS_seed2025/visuals/testB/GlaS_official_testB_testB_9_raw.png`（人工审查：未执行）
