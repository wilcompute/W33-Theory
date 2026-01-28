import csv
import json
import math
import warnings
from collections import defaultdict
from pathlib import Path


def parse_counts(raw: str):
    """Robustly parse JSON-ish count dictionaries into {int: int}.

    On parse failure, returns an empty dict and emits a warning instead of
    raising. Non-integer keys or values are skipped with a warning.
    """
    if raw is None:
        return {}
    raw = str(raw).strip()
    if not raw:
        return {}
    try:
        items = json.loads(raw)
    except json.JSONDecodeError:
        # Handle doubled quotes or accidental single quotes.
        cleaned = raw.replace('""', '"').replace("'", '"')
        try:
            items = json.loads(cleaned)
        except Exception:
            warnings.warn(f"Could not parse counts: {raw!r}")
            return {}
    try:
        result = {}
        for k, v in items.items():
            try:
                result[int(k)] = int(v)
            except Exception:
                warnings.warn(f"Non-integer key/value in counts: {k!r}: {v!r}")
                continue
        return result
    except Exception as e:
        warnings.warn(f"Unexpected counts structure: {e}")
        return {}


def parse_proj_classes(row):
    raw = (row.get("proj_quartet_str") or "").strip()
    if raw:
        return raw.split()
    raw_list = (row.get("proj_list") or "").strip()
    if raw_list:
        cleaned = (
            raw_list.replace("[", "").replace("]", "").replace("'", "").replace('"', "")
        )
        return [item.strip() for item in cleaned.split(",") if item.strip()]
    return []


def entropy_from_counts(counts):
    total = sum(counts.values())
    if total <= 0:
        return 0.0
    ent = 0.0
    for value in counts.values():
        if value <= 0:
            continue
        p = value / total
        ent -= p * math.log(p, 2)
    return ent


def dominant_from_counts(counts):
    if not counts:
        return None, 0.0
    total = sum(counts.values())
    key, value = max(counts.items(), key=lambda kv: kv[1])
    return key, (value / total if total else 0.0)


def parse_sec_m(proj_class):
    if not proj_class.startswith("sec"):
        return None, None
    try:
        sec_part, m_part = proj_class.split("_")
        sec = int(sec_part.replace("sec", ""))
        m = int(m_part.replace("m", ""))
        return sec, m
    except ValueError:
        return None, None


def normalize_probs(counts, keys):
    total = sum(counts.get(k, 0) for k in keys)
    if total <= 0:
        return {k: 0.0 for k in keys}
    return {k: counts.get(k, 0) / total for k in keys}


def kl_divergence(counts, baseline_probs, keys, eps=1e-9):
    total = sum(counts.get(k, 0) for k in keys)
    if total <= 0:
        return 0.0
    kl = 0.0
    for k in keys:
        p = (counts.get(k, 0) + eps) / (total + eps * len(keys))
        q = baseline_probs.get(k, eps)
        kl += p * math.log(p / q, 2)
    return kl


def main():
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data"
    out_dir = data_dir / "_workbench" / "02_geometry"
    out_dir.mkdir(parents=True, exist_ok=True)

    phase_map_path = out_dir / "W33_line_phase_map.csv"
    coupling_path = (
        data_dir / "toe_coupling_20260110" / "W33_lines_to_projective_quartets.csv"
    )

    line_phase = {}
    global_k6 = defaultdict(int)
    global_k3 = defaultdict(int)
    with phase_map_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"line_id", "k_mod6_counts", "k_mod3_counts"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError(
                f"Missing required columns in {phase_map_path}: {required - set(reader.fieldnames or [])}"
            )
        for row in reader:
            try:
                line_id = int(row["line_id"])
            except Exception:
                warnings.warn(f"Skipping row with invalid line_id: {row}")
                continue
            k6_counts = parse_counts(row.get("k_mod6_counts", ""))
            k3_counts = parse_counts(row.get("k_mod3_counts", ""))
            for k, v in k6_counts.items():
                global_k6[k] += v
            for k, v in k3_counts.items():
                global_k3[k] += v
            line_phase[line_id] = {"k6": k6_counts, "k3": k3_counts}

    proj_to_counts = defaultdict(
        lambda: {"k6": defaultdict(int), "k3": defaultdict(int), "lines": 0}
    )
    sec_to_counts = defaultdict(
        lambda: {"k6": defaultdict(int), "k3": defaultdict(int), "lines": 0}
    )
    m_to_counts = defaultdict(
        lambda: {"k6": defaultdict(int), "k3": defaultdict(int), "lines": 0}
    )

    with coupling_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            line_id = int(row["line_id"])
            proj_classes = parse_proj_classes(row)
            if not proj_classes:
                continue
            phase = line_phase.get(line_id)
            if not phase:
                continue
            for proj in proj_classes:
                proj_counts = proj_to_counts[proj]
                for k, v in phase["k6"].items():
                    proj_counts["k6"][k] += v
                for k, v in phase["k3"].items():
                    proj_counts["k3"][k] += v
                proj_counts["lines"] += 1
                sec, m = parse_sec_m(proj)
                if sec is not None:
                    sec_counts = sec_to_counts[sec]
                    for k, v in phase["k6"].items():
                        sec_counts["k6"][k] += v
                    for k, v in phase["k3"].items():
                        sec_counts["k3"][k] += v
                    sec_counts["lines"] += 1
                if m is not None:
                    m_counts = m_to_counts[m]
                    for k, v in phase["k6"].items():
                        m_counts["k6"][k] += v
                    for k, v in phase["k3"].items():
                        m_counts["k3"][k] += v
                    m_counts["lines"] += 1

    k6_keys = list(range(6))
    k3_keys = list(range(3))
    global_k6_probs = normalize_probs(global_k6, k6_keys)
    global_k3_probs = normalize_probs(global_k3, k3_keys)

    proj_rows = []
    for proj, counts in sorted(proj_to_counts.items()):
        k6_dom, k6_frac = dominant_from_counts(counts["k6"])
        k3_dom, k3_frac = dominant_from_counts(counts["k3"])
        k6_kl = kl_divergence(counts["k6"], global_k6_probs, k6_keys)
        k3_kl = kl_divergence(counts["k3"], global_k3_probs, k3_keys)
        proj_rows.append(
            {
                "proj_class": proj,
                "lines_count": counts["lines"],
                "k6_total": sum(counts["k6"].values()),
                "k6_dom_k": k6_dom if k6_dom is not None else "",
                "k6_dom_frac": round(k6_frac, 4),
                "k6_entropy": round(entropy_from_counts(counts["k6"]), 4),
                "k6_kl_global": round(k6_kl, 6),
                "k3_dom_k": k3_dom if k3_dom is not None else "",
                "k3_dom_frac": round(k3_frac, 4),
                "k3_entropy": round(entropy_from_counts(counts["k3"]), 4),
                "k3_kl_global": round(k3_kl, 6),
                "k6_counts_json": json.dumps(counts["k6"], sort_keys=True),
                "k3_counts_json": json.dumps(counts["k3"], sort_keys=True),
            }
        )

    proj_csv = out_dir / "projective_class_phase_alignment.csv"
    with proj_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=proj_rows[0].keys())
        writer.writeheader()
        writer.writerows(proj_rows)

    def summarize_group(group_counts, label):
        rows = []
        for key in sorted(group_counts.keys()):
            counts = group_counts[key]
            k6_dom, k6_frac = dominant_from_counts(counts["k6"])
            k3_dom, k3_frac = dominant_from_counts(counts["k3"])
            k6_kl = kl_divergence(counts["k6"], global_k6_probs, k6_keys)
            k3_kl = kl_divergence(counts["k3"], global_k3_probs, k3_keys)
            rows.append(
                {
                    label: key,
                    "lines_count": counts["lines"],
                    "k6_dom_k": k6_dom if k6_dom is not None else "",
                    "k6_dom_frac": round(k6_frac, 4),
                    "k6_entropy": round(entropy_from_counts(counts["k6"]), 4),
                    "k6_kl_global": round(k6_kl, 6),
                    "k3_dom_k": k3_dom if k3_dom is not None else "",
                    "k3_dom_frac": round(k3_frac, 4),
                    "k3_entropy": round(entropy_from_counts(counts["k3"]), 4),
                    "k3_kl_global": round(k3_kl, 6),
                    "k6_counts_json": json.dumps(counts["k6"], sort_keys=True),
                    "k3_counts_json": json.dumps(counts["k3"], sort_keys=True),
                }
            )
        return rows

    sec_rows = summarize_group(sec_to_counts, "sec")
    m_rows = summarize_group(m_to_counts, "m")

    sec_csv = out_dir / "projective_sector_phase_alignment.csv"
    with sec_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=sec_rows[0].keys())
        writer.writeheader()
        writer.writerows(sec_rows)

    m_csv = out_dir / "projective_m_phase_alignment.csv"
    with m_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=m_rows[0].keys())
        writer.writeheader()
        writer.writerows(m_rows)

    proj_rows_sorted = sorted(
        proj_rows, key=lambda r: (-r["k6_kl_global"], -r["k6_dom_frac"])
    )
    top_proj = proj_rows_sorted[:6]

    md_path = out_dir / "projective_phase_alignment.md"
    with md_path.open("w", encoding="utf-8") as handle:
        handle.write("# Projective class vs W33 phase alignment\n\n")
        handle.write("Inputs:\n")
        handle.write("- `data/_workbench/02_geometry/W33_line_phase_map.csv`\n")
        handle.write(
            "- `data/_toe/coupling_20260110/W33_lines_to_projective_quartets.csv`\n\n"
        )
        handle.write("Outputs:\n")
        handle.write(
            "- `data/_workbench/02_geometry/projective_class_phase_alignment.csv`\n"
        )
        handle.write(
            "- `data/_workbench/02_geometry/projective_sector_phase_alignment.csv`\n"
        )
        handle.write(
            "- `data/_workbench/02_geometry/projective_m_phase_alignment.csv`\n\n"
        )
        handle.write("Global phase distribution:\n")
        handle.write(
            f"- k mod 6 counts: {json.dumps(dict(sorted(global_k6.items())))}\n"
        )
        handle.write(
            f"- k mod 3 counts: {json.dumps(dict(sorted(global_k3.items())))}\n\n"
        )
        handle.write(
            "Most phase-biased projective classes (by k mod 6 KL to global):\n"
        )
        for row in top_proj:
            handle.write(
                f"- {row['proj_class']}: k6_dom={row['k6_dom_k']} "
                f"(frac={row['k6_dom_frac']}), kl={row['k6_kl_global']}, "
                f"entropy={row['k6_entropy']}\n"
            )


if __name__ == "__main__":
    main()
