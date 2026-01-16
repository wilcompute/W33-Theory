import csv
import json
import math
import warnings
from pathlib import Path


def parse_counts(raw: str):
    """Robustly parse JSON-ish count dictionaries into {int: int}.

    Returns empty dict and emits a warning on parse failure.
    """
    if raw is None:
        return {}
    raw = str(raw).strip()
    if not raw:
        return {}
    try:
        items = json.loads(raw)
    except json.JSONDecodeError:
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


def zscore(values):
    mean = sum(values) / len(values)
    var = sum((v - mean) ** 2 for v in values) / len(values)
    std = math.sqrt(var)
    if std == 0:
        return [0.0 for _ in values], mean, std
    return [(v - mean) / std for v in values], mean, std


def rankdata(values):
    indexed = sorted(enumerate(values), key=lambda x: x[1])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i + 1
        while j < len(indexed) and indexed[j][1] == indexed[i][1]:
            j += 1
        rank = (i + j + 1) / 2.0
        for k in range(i, j):
            ranks[indexed[k][0]] = rank
        i = j
    return ranks


def spearman_corr(a, b):
    ra = rankdata(a)
    rb = rankdata(b)
    mean_a = sum(ra) / len(ra)
    mean_b = sum(rb) / len(rb)
    num = sum((ra[i] - mean_a) * (rb[i] - mean_b) for i in range(len(ra)))
    den_a = math.sqrt(sum((ra[i] - mean_a) ** 2 for i in range(len(ra))))
    den_b = math.sqrt(sum((rb[i] - mean_b) ** 2 for i in range(len(rb))))
    if den_a == 0 or den_b == 0:
        return 0.0
    return num / (den_a * den_b)


def solve_linear_system(matrix, vector):
    size = len(vector)
    aug = [row[:] + [vector[i]] for i, row in enumerate(matrix)]
    for col in range(size):
        pivot = None
        for row in range(col, size):
            if abs(aug[row][col]) > 1e-12:
                pivot = row
                break
        if pivot is None:
            continue
        aug[col], aug[pivot] = aug[pivot], aug[col]
        pivot_val = aug[col][col]
        aug[col] = [v / pivot_val for v in aug[col]]
        for row in range(size):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [aug[row][i] - factor * aug[col][i] for i in range(size + 1)]
    return [aug[i][size] for i in range(size)]


def main():
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data"
    out_dir = data_dir / "_workbench" / "04_measurement"
    out_dir.mkdir(parents=True, exist_ok=True)

    line_feature_path = data_dir / "_workbench" / "02_geometry" / "line_feature_table.csv"
    k12_path = data_dir / "_workbench" / "02_geometry" / "W33_line_phase_k12_map.csv"
    tau_self_path = out_dir / "tau_phase_shift_self.csv"

    line_features = {}
    with line_feature_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            line_id = int(row["line_id"])
            line_features[line_id] = {
                "var_q_class": row.get("var_q_class", ""),
                "var_q_r": float(row["var_q_r"]) if row["var_q_r"] else 0.0,
                "native_mean_abs_delta": float(row["native_mean_abs_delta"])
                if row["native_mean_abs_delta"]
                else 0.0,
            }

    k12_counts = {}
    global_counts = {k: 0 for k in range(12)}
    with k12_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"line_id", "k_mod12_counts"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError(f"Missing required columns in {k12_path}: {required - set(reader.fieldnames or [])}")
        for row in reader:
            try:
                line_id = int(row["line_id"])
            except Exception:
                warnings.warn(f"Skipping row with invalid line_id: {row}")
                continue
            counts = parse_counts(row.get("k_mod12_counts", ""))
            k12_counts[line_id] = counts
            for k, v in counts.items():
                global_counts[k] += v

    total = sum(global_counts.values())
    global_probs = {k: (global_counts[k] / total if total else 0.0) for k in range(12)}

    tau_self = {}
    with tau_self_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            line_id = int(row["line_id"])
            tau_self[line_id] = float(row["similarity"])

    rows = []
    for line_id, feature in line_features.items():
        counts = k12_counts.get(line_id, {})
        entropy = entropy_from_counts(counts)
        kl = kl_divergence(counts, global_probs, list(range(12)))
        rows.append(
            {
                "line_id": line_id,
                "var_q_class": feature["var_q_class"],
                "var_q_r": feature["var_q_r"],
                "k12_entropy": entropy,
                "k12_kl_global": kl,
                "tau_shift_similarity": tau_self.get(line_id, 0.0),
                "native_mean_abs_delta": feature["native_mean_abs_delta"],
            }
        )

    var_vals = [row["var_q_r"] for row in rows]
    ent_vals = [row["k12_entropy"] for row in rows]
    kl_vals = [row["k12_kl_global"] for row in rows]
    tau_vals = [row["tau_shift_similarity"] for row in rows]
    y_vals = [row["native_mean_abs_delta"] for row in rows]

    z_var, var_mean, var_std = zscore(var_vals)
    z_ent, ent_mean, ent_std = zscore(ent_vals)
    z_kl, kl_mean, kl_std = zscore(kl_vals)
    z_tau, tau_mean, tau_std = zscore(tau_vals)

    prior_scores = [
        (-z_var[i]) + (-z_ent[i]) + (z_kl[i]) + (-z_tau[i]) for i in range(len(rows))
    ]

    # Fit linear model on standardized features.
    x_cols = [z_var, z_ent, z_kl, z_tau]
    x_matrix = []
    for i in range(len(rows)):
        x_matrix.append([1.0] + [col[i] for col in x_cols])

    xtx = [[0.0 for _ in range(5)] for _ in range(5)]
    xty = [0.0 for _ in range(5)]
    for i in range(len(rows)):
        xi = x_matrix[i]
        yi = y_vals[i]
        for r in range(5):
            xty[r] += xi[r] * yi
            for c in range(5):
                xtx[r][c] += xi[r] * xi[c]
    beta = solve_linear_system(xtx, xty)

    fit_scores = []
    for i in range(len(rows)):
        xi = x_matrix[i]
        pred = sum(beta[j] * xi[j] for j in range(5))
        fit_scores.append(pred)

    spearman_prior = spearman_corr(prior_scores, y_vals)
    spearman_fit = spearman_corr(fit_scores, y_vals)

    top_n = 10
    native_rank = sorted(range(len(rows)), key=lambda i: y_vals[i], reverse=True)
    prior_rank = sorted(range(len(rows)), key=lambda i: prior_scores[i], reverse=True)
    fit_rank = sorted(range(len(rows)), key=lambda i: fit_scores[i], reverse=True)

    top_native = set(native_rank[:top_n])
    top_prior = set(prior_rank[:top_n])
    top_fit = set(fit_rank[:top_n])

    overlap_prior = len(top_native & top_prior)
    overlap_fit = len(top_native & top_fit)

    for i, row in enumerate(rows):
        row["prior_score"] = prior_scores[i]
        row["fit_score"] = fit_scores[i]

    out_csv = out_dir / "action_candidate_features.csv"
    fieldnames = [
        "line_id",
        "var_q_class",
        "var_q_r",
        "k12_entropy",
        "k12_kl_global",
        "tau_shift_similarity",
        "native_mean_abs_delta",
        "prior_score",
        "fit_score",
    ]
    with out_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    md_path = out_dir / "action_candidate_summary.md"
    with md_path.open("w", encoding="utf-8") as handle:
        handle.write("# Action candidate (geometry-only) vs native flux sensors\n\n")
        handle.write("Features:\n")
        handle.write("- var_q_r: Q12 variance (low is better)\n")
        handle.write("- var_q_class: Q12 variance label\n")
        handle.write("- k12_entropy: entropy of k mod 12 phases\n")
        handle.write("- k12_kl_global: KL divergence from global k mod 12 distribution\n")
        handle.write("- tau_shift_similarity: self-similarity under k12 shift=2 (lower is better)\n\n")
        handle.write("Candidate score (prior):\n")
        handle.write("- score = -z(var_q_r) - z(k12_entropy) + z(k12_kl_global) - z(tau_shift_similarity)\n\n")
        handle.write("Fitted score (least squares, standardized features):\n")
        handle.write(f"- intercept: {round(beta[0], 6)}\n")
        handle.write(
            f"- weights: var_q={round(beta[1], 6)}, k12_entropy={round(beta[2], 6)}, "
            f"k12_kl={round(beta[3], 6)}, tau_shift={round(beta[4], 6)}\n\n"
        )
        handle.write("Evaluation (native mean_abs_delta):\n")
        handle.write(f"- spearman_prior: {round(spearman_prior, 4)}\n")
        handle.write(f"- spearman_fit: {round(spearman_fit, 4)}\n")
        handle.write(f"- top{top_n} overlap prior: {overlap_prior}\n")
        handle.write(f"- top{top_n} overlap fit: {overlap_fit}\n\n")
        handle.write("Outputs:\n")
        handle.write("- `data/_workbench/04_measurement/action_candidate_features.csv`\n")


if __name__ == "__main__":
    main()
