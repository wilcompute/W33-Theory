import csv
from pathlib import Path
from statistics import mean


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader)


import argparse
import os

ROOT = Path(__file__).resolve().parents[1]
# Allow tests or external callers to override the repo root directory.
# Priority: CLI --root, then TOE_ROOT env var, else default ROOT above.
if args.root:
    ROOT = Path(args.root).resolve()
else:
    env_root = os.environ.get("TOE_ROOT")
    if env_root:
        ROOT = Path(env_root).resolve()
ac_path = (
    ROOT / "data" / "_workbench" / "04_measurement" / "action_candidate_features.csv"
)
phase_path = ROOT / "data" / "_workbench" / "02_geometry" / "W33_line_phase_map.csv"
out_path = ROOT / "data" / "_docs" / "toe_key_lines.csv"
md_path = ROOT / "data" / "_docs" / "toe_key_lines.md"

ac = {int(r["line_id"]): r for r in read_csv(ac_path)}
ph = {int(r["line_id"]): r for r in read_csv(phase_path)}

# try to load node-commutator predictor scores if available
node_path = (
    ROOT / "data" / "_workbench" / "04_measurement" / "node_commutator_line_scores.csv"
)
node_scores = {}
if node_path.exists():
    with open(node_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for rr in reader:
            try:
                node_scores[int(rr["line_id"])] = float(rr.get("score") or 0.0)
            except Exception:
                continue
    top_node5 = sorted(node_scores.items(), key=lambda x: -x[1])[:5]
    top_node5_set = {lid for lid, _ in top_node5}
else:
    top_node5_set = set()

# try to load mixed predictor (oddness + defect mass) scores if available
mixed_path = (
    ROOT
    / "data"
    / "_workbench"
    / "04_measurement"
    / "mixed_predictor_oddness_defect_scores.csv"
)
mixed_scores = {}
if mixed_path.exists():
    with open(mixed_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for rr in reader:
            try:
                mixed_scores[int(rr["line_id"])] = float(rr.get("score") or 0.0)
            except Exception:
                continue
    top_mixed5 = sorted(mixed_scores.items(), key=lambda x: -x[1])[:5]
    top_mixed5_set = {lid for lid, _ in top_mixed5}
else:
    top_mixed5_set = set()

# try to load e* oddness per-line if available
e_star_path = (
    ROOT / "data" / "_workbench" / "04_measurement" / "e_star_oddness_per_line.csv"
)
e_star = {}
if e_star_path.exists():
    with open(e_star_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for rr in reader:
            try:
                e_star[int(rr["line_id"])] = float(rr.get("odd_fraction") or 0.0)
            except Exception:
                continue
    top_e5 = sorted(e_star.items(), key=lambda x: -x[1])[:5]
    top_e5_set = {lid for lid, _ in top_e5}
else:
    top_e5_set = set()

# build merged rows
rows = []

# ranks and top lists

top_n = 10
top_native = {r["line_id"] for r in rows_sorted_native[:top_n]}
top_prior = {r["line_id"] for r in rows_sorted_prior[:top_n]}
top_fit = {r["line_id"] for r in rows_sorted_fit[:top_n]}
top_node = {r["line_id"] for r in rows_sorted_node[:5]}
top_mixed = {r["line_id"] for r in rows_sorted_mixed[:5]}
top_e_star = {r["line_id"] for r in rows_sorted_e_star[:5]}

# write CSV
fieldnames = [
    "line_id",
    "native_mean_abs_delta",
    "var_q_class",
    "var_q_r",
    "unique_k_mod6",
    "unique_k_mod3",
    "k12_entropy",
    "k12_kl_global",
    "tau_shift_similarity",
    "prior_score",
    "fit_score",
    "node_commutator_score",
    "mixed_score",
    "e_star_oddness",
    "rank_native",
    "rank_prior",
    "rank_fit",
    "rank_node_commutator",
    "rank_mixed",
    "rank_e_star_oddness",
    "in_top_native",
    "in_top_prior",
    "in_top_fit",
    "in_top_node_commutator",
    "in_top_mixed",
    "in_top_e_star_oddness",
]
# ensure output dir exists

# write short md summary
md_lines = [
    "# TOE key lines digest",
    "",
    f"- top_native (by native_mean_abs_delta): {sorted(top_native)}",
    f"- top_prior: {sorted(top_prior)}",
    f"- top_fit: {sorted(top_fit)}",
    f"- union_top ({len(union_top)} lines): {union_top}",
    "",
    "See `toe_key_lines.csv` for per-line metrics and ranks.",
]


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", type=str, default=None)
    args, _ = parser.parse_known_args()
    for line_id in sorted(set(list(ac.keys()) + list(ph.keys()))):
        a = ac.get(line_id, {})
        p = ph.get(line_id, {})
        row = {
            "line_id": line_id,
            "native_mean_abs_delta": float(a.get("native_mean_abs_delta") or 0.0),
            "var_q_class": a.get("var_q_class", ""),
            "var_q_r": float(a.get("var_q_r") or 0.0),
            "k12_entropy": float(a.get("k12_entropy") or 0.0),
            "k12_kl_global": float(a.get("k12_kl_global") or 0.0),
            "tau_shift_similarity": float(a.get("tau_shift_similarity") or 0.0),
            "prior_score": float(a.get("prior_score") or 0.0),
            "fit_score": float(a.get("fit_score") or 0.0),
            "unique_k_mod6": int(p.get("unique_k_mod6") or 0),
            "unique_k_mod3": int(p.get("unique_k_mod3") or 0),
            "node_commutator_score": float(node_scores.get(line_id, 0.0)),
            "in_top_node_commutator": int(line_id in top_node5_set),
            "mixed_score": float(mixed_scores.get(line_id, 0.0)),
            "in_top_mixed": int(line_id in top_mixed5_set),
            "e_star_oddness": float(e_star.get(line_id, 0.0)),
            "in_top_e_star_oddness": int(line_id in top_e5_set),
        }
        rows.append(row)
    rows_sorted_native = sorted(
        rows, key=lambda r: r["native_mean_abs_delta"], reverse=True
    )
    rows_sorted_prior = sorted(rows, key=lambda r: r["prior_score"], reverse=True)
    rows_sorted_fit = sorted(rows, key=lambda r: r["fit_score"], reverse=True)
    rows_sorted_node = sorted(
        rows, key=lambda r: r["node_commutator_score"], reverse=True
    )
    rows_sorted_mixed = sorted(rows, key=lambda r: r["mixed_score"], reverse=True)
    rows_sorted_e_star = sorted(rows, key=lambda r: r["e_star_oddness"], reverse=True)
    for r in rows:
        r["rank_native"] = next(
            i + 1
            for i, rr in enumerate(rows_sorted_native)
            if rr["line_id"] == r["line_id"]
        )
        r["rank_prior"] = next(
            i + 1
            for i, rr in enumerate(rows_sorted_prior)
            if rr["line_id"] == r["line_id"]
        )
        r["rank_fit"] = next(
            i + 1
            for i, rr in enumerate(rows_sorted_fit)
            if rr["line_id"] == r["line_id"]
        )
        r["rank_node_commutator"] = next(
            i + 1
            for i, rr in enumerate(rows_sorted_node)
            if rr["line_id"] == r["line_id"]
        )
        r["rank_mixed"] = next(
            i + 1
            for i, rr in enumerate(rows_sorted_mixed)
            if rr["line_id"] == r["line_id"]
        )
        r["rank_e_star_oddness"] = next(
            i + 1
            for i, rr in enumerate(rows_sorted_e_star)
            if rr["line_id"] == r["line_id"]
        )
        r["in_top_native"] = int(r["line_id"] in top_native)
        r["in_top_prior"] = int(r["line_id"] in top_prior)
        r["in_top_fit"] = int(r["line_id"] in top_fit)
        r["in_top_node_commutator"] = int(r["line_id"] in top_node)
        r["in_top_mixed"] = int(r["line_id"] in top_mixed)
        r["in_top_e_star_oddness"] = int(r["line_id"] in top_e_star)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in sorted(rows, key=lambda r: r["line_id"]):
            writer.writerow({k: r.get(k, "") for k in fieldnames})
    union_top = sorted(list(top_native | top_prior | top_fit))
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print("Wrote", out_path)
    print("Wrote", md_path)


if __name__ == "__main__":
    main()
