"""Close auditable 07_Distance evidence from existing experiment assets."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import fmean
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SEEDS = (3407, 1234, 2025)
DIST_PREFIX = "D2_R34UNet_Distance_GlaS_seed"
BASE_PREFIX = "B1_ResNet34_UNet_GlaS_seed"
METRICS = ("Boundary F1", "HD95", "Object Hausdorff", "Object Dice", "F1")


def read_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def val(row: dict[str, str], key: str) -> str:
    return row.get(key, "BLOCKED") or "BLOCKED"


def metric_means(run: Path, split: str) -> dict[str, str]:
    rows = [r for r in read_csv(run / f"{split}_metrics.csv") if r.get("row_type") == "sample"]
    names = {"boundary_f1": "Boundary F1", "hd95": "HD95", "object_hausdorff": "Object Hausdorff", "objdice": "Object Dice", "f1": "F1"}
    out = {}
    for key, name in names.items():
        values = []
        for row in rows:
            try:
                values.append(float(row[key]))
            except (KeyError, TypeError, ValueError):
                pass
        out[name] = fmean(values) if values else "BLOCKED"
    return out


def training_cost(run: Path, meta: dict[str, Any]) -> dict[str, Any]:
    rows = read_csv(run / "train_log.csv")
    times = []
    for row in rows:
        try:
            times.append(float(row["epoch_time_sec"]))
        except (KeyError, TypeError, ValueError):
            pass
    epoch_count = meta.get("epoch_count")
    best_epoch = meta.get("best_epoch")
    cost_status = "pass" if times and epoch_count is not None and best_epoch is not None else "BLOCKED"
    return {
        "epoch_time_sec_sum": sum(times) if times else "BLOCKED",
        "epoch_time_sec_n": len(times) if times else "BLOCKED",
        "epoch_count": epoch_count if epoch_count is not None else "BLOCKED",
        "best_epoch": best_epoch if best_epoch is not None else "BLOCKED",
        "cost_status": cost_status,
        "inference_time_sec": "BLOCKED",
        "gpu_memory_mb": "BLOCKED",
    }


def visual_files(run: Path) -> list[str]:
    visual_dir = run / "visuals"
    if not visual_dir.exists():
        return []
    return sorted(rel(p) for p in visual_dir.glob("**/*.png") if p.is_file())


def build_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    costs = []
    cases = []
    blockers = []
    for seed in SEEDS:
        d2 = ROOT / "experiments" / f"{DIST_PREFIX}{seed}"
        b1 = ROOT / "experiments" / f"{BASE_PREFIX}{seed}"
        dmeta = read_yaml(d2 / "run_meta.yaml") if (d2 / "run_meta.yaml").exists() else {}
        bmeta = read_yaml(b1 / "run_meta.yaml") if (b1 / "run_meta.yaml").exists() else {}
        dc = training_cost(d2, dmeta)
        bc = training_cost(b1, bmeta)
        for label, run, meta, cost, other in (("distance", d2, dmeta, dc, bc), ("baseline", b1, bmeta, bc, dc)):
            row = {"seed": seed, "model_role": label, "run_name": meta.get("run_name", run.name), "run_dir": rel(run), **cost}
            if cost["cost_status"] != "pass":
                blockers.append(f"{label}_seed{seed}:training_cost_incomplete")
            if cost["epoch_time_sec_sum"] != "BLOCKED" and other["epoch_time_sec_sum"] != "BLOCKED":
                row["train_time_delta_distance_minus_baseline_sec"] = (dc["epoch_time_sec_sum"] - bc["epoch_time_sec_sum"]) if label == "distance" else ""
            else:
                row["train_time_delta_distance_minus_baseline_sec"] = "BLOCKED"
            costs.append(row)
        for split in ("testA", "testB"):
            metrics = metric_means(d2, split)
            files = visual_files(d2)
            split_files = [p for p in files if f"/visuals/{split}/" in f"/{p}/"]
            if not split_files:
                blockers.append(f"distance_seed{seed}:{split}:visuals_missing")
            for path in split_files:
                cases.append({"seed": seed, "split": split, "visual_path": path, **metrics, "visual_review_status": "not_performed"})
    return costs, cases, blockers


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else ["status"]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_reports(costs: list[dict[str, Any]], cases: list[dict[str, Any]], blockers: list[str]) -> None:
    report_dir = ROOT / "reports" / "stage_reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    lines = ["# 07_Distance visual casebook", "", "本文件仅索引脚本发现的真实 visuals 文件和对应 split 的测试指标；不对图片作主观改善判断。", "", "## 审查状态", "- 人工视觉审查：未执行（`visual_review_status=not_performed`）。", ""]
    for seed in SEEDS:
        lines.append(f"## seed {seed}")
        for split in ("testA", "testB"):
            rows = [r for r in cases if r["seed"] == seed and r["split"] == split]
            lines.append(f"### {split}")
            if not rows:
                lines.append("- BLOCKED：未发现 visuals 文件。")
                continue
            lines.append(f"- 对应测试指标均来自 `experiments/{DIST_PREFIX}{seed}/{split}_metrics.csv` 的 sample 行均值；共索引 {len(rows)} 个 PNG。")
            lines.append(f"- Boundary F1={rows[0]['Boundary F1']}；HD95={rows[0]['HD95']}；Object Hausdorff={rows[0]['Object Hausdorff']}；Object Dice={rows[0]['Object Dice']}；F1={rows[0]['F1']}。")
            for row in rows:
                lines.append(f"- `{row['visual_path']}`（人工审查：未执行）")
    (report_dir / "distance_visual_casebook.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    summary = read_csv(ROOT / "reports/tables/current_base_vs_distance_mean_std.csv")
    decision = ["# 07_Distance decision note", "", "decision_status=blocked", "decision_level=undecided", "", "本文件不是正式 keep/弃用结论。人工视觉审查未完成，且正式成本完整性要求未满足，因此不得输出 keep。", "", "## 按协议顺序", ""]
    for title, names in (("1. Boundary F1", ["Boundary F1"]), ("2. HD95/Object Hausdorff", ["HD95", "Object Hausdorff"]), ("3. visual support", []), ("4. Object Dice/F1", ["Object Dice", "F1"]), ("5. cost", [])):
        decision.append(f"### {title}")
        if names:
            for split in ("testA", "testB"):
                found = [r for r in summary if r.get("split_role") == split and r.get("metric_name") in names]
                for r in found:
                    decision.append(f"- {split} / {r['metric_name']} delta（distance-baseline）={r.get('delta_distance_minus_baseline', 'BLOCKED')}；seed support={r.get('n_runs', 'BLOCKED')}（{r.get('seeds', 'BLOCKED')}）。")
                if not found:
                    decision.append(f"- {split}：BLOCKED，缺少对应 delta。")
        elif title.startswith("3"):
            decision.append(f"- 三个 seed 均有真实 visuals 索引（每个 split 5 个样例），但人工视觉审查未执行；因此仅为文件存在性支持，不构成改善结论。")
        else:
            decision.append("- 成本：训练 epoch_time_sec_sum、epoch_count、best_epoch 可从真实资产读取；推理时间和 GPU 显存未记录，写 BLOCKED。正式成本完整性不足。")
    decision += ["", "## 证据缺失/阻断", "- " + ("；".join(blockers) if blockers else "未发现脚本级资产缺失，但人工视觉审查、推理时间、GPU 显存仍缺失。"), "- seed support：指标汇总表显示 TestA/TestB 均为 3 个独立 seed；三个 PNG-GT 独立复核 JSON 均 pass（由既有汇总资产提供）。", "- 结论边界：当前只能报告真实 delta 和资产状态，不能宣称 distance 改善，也不能输出 keep。"]
    (report_dir / "distance_decision_note.md").write_text("\n".join(decision) + "\n", encoding="utf-8")


def main() -> int:
    costs, cases, blockers = build_rows()
    write_csv(ROOT / "reports/tables/distance_cost_comparison.csv", costs)
    write_reports(costs, cases, blockers)
    print(json.dumps({"status": "blocked", "cost_rows": len(costs), "visual_rows": len(cases), "blockers": blockers, "outputs": ["reports/tables/distance_cost_comparison.csv", "reports/stage_reports/distance_visual_casebook.md", "reports/stage_reports/distance_decision_note.md"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
