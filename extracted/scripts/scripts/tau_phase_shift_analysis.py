import csv
import json
import itertools
from collections import Counter
from pathlib import Path


def parse_counts(raw: str):
    raw = raw.strip()
    if not raw:
        return {}
    return {int(k): int(v) for k, v in json.loads(raw).items()}


def parse_proj_classes(row):
    raw = (row.get("proj_quartet_str") or "").strip()
    if raw:
        return raw.split()
    raw_list = (row.get("proj_list") or "").strip()
    if raw_list:
        cleaned = raw_list.replace("[", "").replace("]", "").replace("'", "").replace('"', "")
        return [item.strip() for item in cleaned.split(",") if item.strip()]
    return []


def apply_mapping(proj_class, sec_perm, sec_shift):
    if not proj_class.startswith("sec"):
        return proj_class
    sec_part, m_part = proj_class.split("_")
    sec = int(sec_part.replace("sec", ""))
    m = int(m_part.replace("m", ""))
    sec_new = sec_perm[sec]
    m_new = (m + sec_shift[sec]) % 3
    return f"sec{sec_new}_m{m_new}"


def counts_to_vec(counts, size=12):
    return [counts.get(k, 0) for k in range(size)]


def best_shift(counts_a, counts_b):
    vec_a = counts_to_vec(counts_a)
    vec_b = counts_to_vec(counts_b)
    total_a = sum(vec_a)
    total_b = sum(vec_b)
    if total_a == 0 or total_b == 0:
        return 0, 0, 0.0
    best = (0, -1)
    for shift in range(12):
        score = 0
        for k in range(12):
            score += vec_a[k] * vec_b[(k + shift) % 12]
        if score > best[1]:
            best = (shift, score)
    similarity = best[1] / (total_a * total_b)
    return best[0], best[1], similarity


def shift_similarity(counts, shift):
    vec = counts_to_vec(counts)
    total = sum(vec)
    if total == 0:
        return 0.0
    score = 0
    for k in range(12):
        score += vec[k] * vec[(k + shift) % 12]
    return score / (total * total)


def is_order_three(sec_perm, sec_shift):
    classes = [f"sec{s}_m{m}" for s in range(4) for m in range(3)]
    for proj in classes:
        p1 = apply_mapping(proj, sec_perm, sec_shift)
        p2 = apply_mapping(p1, sec_perm, sec_shift)
        p3 = apply_mapping(p2, sec_perm, sec_shift)
        if p3 != proj:
            return False
    return True


def main():
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data"
    out_dir = data_dir / "_workbench" / "04_measurement"
    out_dir.mkdir(parents=True, exist_ok=True)

    k12_path = data_dir / "_workbench" / "02_geometry" / "W33_line_phase_k12_map.csv"
    coupling_path = data_dir / "toe_coupling_20260110" / "W33_lines_to_projective_quartets.csv"

    line_counts = {}
    with k12_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            line_id = int(row["line_id"])
            line_counts[line_id] = parse_counts(row["k_mod12_counts"])

    quartet_to_line = {}
    line_quartets = {}
    with coupling_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            line_id = int(row["line_id"])
            proj_classes = parse_proj_classes(row)
            if len(proj_classes) != 4:
                continue
            key = tuple(sorted(proj_classes))
            quartet_to_line[key] = line_id
            line_quartets[line_id] = proj_classes

    best_mapping = None
    best_pairs_count = -1
    candidates = []
    for perm in itertools.permutations(range(4)):
        for shift in itertools.product(range(3), repeat=4):
            if not is_order_three(perm, shift):
                continue
            count = 0
            for proj_classes in line_quartets.values():
                mapped = [apply_mapping(p, perm, shift) for p in proj_classes]
                if tuple(sorted(mapped)) in quartet_to_line:
                    count += 1
            if count > best_pairs_count:
                best_pairs_count = count
                best_mapping = (perm, shift)
                candidates = [(perm, shift, count)]
            elif count == best_pairs_count:
                candidates.append((perm, shift, count))

    pairs = []
    shift_hist = Counter()
    mapping_note = ""
    if best_mapping is not None:
        perm, shift = best_mapping
        mapping_note = f"perm={perm}, shift={shift}"
        for line_id, proj_classes in line_quartets.items():
            mapped = [apply_mapping(p, perm, shift) for p in proj_classes]
            mapped_key = tuple(sorted(mapped))
            mapped_line = quartet_to_line.get(mapped_key)
            if mapped_line is None:
                continue
            counts_a = line_counts.get(line_id, {})
            counts_b = line_counts.get(mapped_line, {})
            best_k12, score, similarity = best_shift(counts_a, counts_b)
            shift_hist[best_k12] += 1
            pairs.append(
                {
                    "line_id": line_id,
                    "tau_line_id": mapped_line,
                    "proj_quartet": " ".join(sorted(proj_classes)),
                    "tau_proj_quartet": " ".join(sorted(mapped)),
                    "best_k12_shift": best_k12,
                    "correlation_score": score,
                    "similarity": round(similarity, 6),
                }
            )

    pair_csv = out_dir / "tau_phase_shift_pairs.csv"
    fieldnames = [
        "line_id",
        "tau_line_id",
        "proj_quartet",
        "tau_proj_quartet",
        "best_k12_shift",
        "correlation_score",
        "similarity",
    ]
    with pair_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(pairs)

    hist_csv = out_dir / "tau_phase_shift_histogram.csv"
    with hist_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["k12_shift", "count"])
        for shift in sorted(shift_hist.keys()):
            writer.writerow([shift, shift_hist[shift]])

    self_rows = []
    for line_id, counts in line_counts.items():
        similarity = shift_similarity(counts, 2)
        self_rows.append(
            {
                "line_id": line_id,
                "shift": 2,
                "similarity": round(similarity, 6),
            }
        )

    self_csv = out_dir / "tau_phase_shift_self.csv"
    with self_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=self_rows[0].keys())
        writer.writeheader()
        writer.writerows(self_rows)

    sims = [row["similarity"] for row in self_rows]
    sim_min = min(sims) if sims else 0.0
    sim_max = max(sims) if sims else 0.0
    sim_mean = sum(sims) / len(sims) if sims else 0.0

    md_path = out_dir / "tau_phase_shift_report.md"
    with md_path.open("w", encoding="utf-8") as handle:
        handle.write("# Tau action vs W33 line phase shifts\n\n")
        handle.write("Search:\n")
        handle.write("- Searched order-3 projective-class actions of the form `sec -> perm(sec)` with per-sector m-shifts.\n")
        handle.write("- Chose mapping that maximizes line-quartet preservation.\n\n")
        handle.write("Inputs:\n")
        handle.write("- `data/_workbench/02_geometry/W33_line_phase_k12_map.csv`\n")
        handle.write("- `data/_toe/coupling_20260110/W33_lines_to_projective_quartets.csv`\n\n")
        handle.write("Outputs:\n")
        handle.write("- `data/_workbench/04_measurement/tau_phase_shift_pairs.csv`\n")
        handle.write("- `data/_workbench/04_measurement/tau_phase_shift_histogram.csv`\n\n")
        handle.write("- `data/_workbench/04_measurement/tau_phase_shift_self.csv`\n\n")
        handle.write(f"Best mapping: {mapping_note}\n")
        handle.write(f"Pairable lines: {len(pairs)}\n\n")
        handle.write("Best k12 shift histogram:\n")
        if not shift_hist:
            handle.write("- none\n")
        else:
            for shift in sorted(shift_hist.keys()):
                handle.write(f"- shift {shift}: {shift_hist[shift]}\n")
        handle.write("\nInternal k12 shift=2 similarity (tau phase proxy):\n")
        handle.write(f"- min: {round(sim_min, 6)}\n")
        handle.write(f"- max: {round(sim_max, 6)}\n")
        handle.write(f"- mean: {round(sim_mean, 6)}\n")


if __name__ == "__main__":
    main()

