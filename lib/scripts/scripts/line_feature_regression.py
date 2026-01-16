#!/usr/bin/env python3
import math
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

POINTS_CSV = ROOT / "data/_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv"
LINES_CSV = ROOT / "data/_sources/w33/W33_lines_tetrads_from_checkpoint_20260109.csv"
PHASE_MAP_CSV = ROOT / "data/_workbench/02_geometry/W33_line_phase_map.csv"
CANON_CSV = ROOT / "data/_toe/flux_response_rankings_20260110/line_flux_response_summary.csv"
NATIVE_CSV = ROOT / "data/_toe/native_fullgrid_20260110/nativeC24_line_flux_response_ranking_summary.csv"
OUT_CSV = ROOT / "data/_workbench/02_geometry/line_feature_regression.csv"
OUT_MD = ROOT / "data/_workbench/02_geometry/line_feature_regression.md"


def parse_complex(val: str) -> complex:
    return complex(val.replace("j", "j"))


def q12_expect(v: np.ndarray) -> float:
    # Q12 = diag(+1, -1, -1, +1)
    return (abs(v[0]) ** 2) - (abs(v[1]) ** 2) - (abs(v[2]) ** 2) + (abs(v[3]) ** 2)


def main() -> None:
    if not POINTS_CSV.exists():
        raise FileNotFoundError(POINTS_CSV)
    if not LINES_CSV.exists():
        raise FileNotFoundError(LINES_CSV)
    if not PHASE_MAP_CSV.exists():
        raise FileNotFoundError(PHASE_MAP_CSV)
    if not CANON_CSV.exists():
        raise FileNotFoundError(CANON_CSV)
    if not NATIVE_CSV.exists():
        raise FileNotFoundError(NATIVE_CSV)

    points = pd.read_csv(POINTS_CSV)
    for col in ["v0", "v1", "v2", "v3"]:
        points[col] = points[col].map(parse_complex)

    points["q12"] = points[["v0", "v1", "v2", "v3"]].apply(
        lambda r: q12_expect(r.values), axis=1
    )

    lines = pd.read_csv(LINES_CSV)
    lines["point_ids"] = lines["point_ids"].astype(str)

    phase_map = pd.read_csv(PHASE_MAP_CSV)
    canon = pd.read_csv(CANON_CSV)
    native = pd.read_csv(NATIVE_CSV)

    # Build quick lookup maps
    q12_by_point = points.set_index("point_id")["q12"].to_dict()
    phase_map = phase_map.set_index("line_id")
    canon = canon.set_index("line_id")
    native = native.set_index("line_id")

    rows = []
    for _, row in lines.iterrows():
        line_id = int(row["line_id"])
        ids = [int(x) for x in row["point_ids"].split()]
        qvals = [q12_by_point[i] for i in ids]
        mean_q = float(np.mean(qvals))
        var_q = float(np.var(qvals))
        abs_mean_q = abs(mean_q)
        sign_mean_q = 0
        if mean_q > 0:
            sign_mean_q = 1
        elif mean_q < 0:
            sign_mean_q = -1

        phase = phase_map.loc[line_id] if line_id in phase_map.index else None
        canon_row = canon.loc[line_id] if line_id in canon.index else None
        native_row = native.loc[line_id] if line_id in native.index else None

        rows.append(
            {
                "line_id": line_id,
                "mean_q": mean_q,
                "abs_mean_q": abs_mean_q,
                "sign_mean_q": sign_mean_q,
                "var_q": var_q,
                "unique_k_mod6": int(phase["unique_k_mod6"]) if phase is not None else np.nan,
                "unique_k_mod3": int(phase["unique_k_mod3"]) if phase is not None else np.nan,
                "canon_mean_abs_delta": float(canon_row["mean_abs_delta"])
                if canon_row is not None
                else np.nan,
                "canon_mean_delta": float(canon_row["mean_delta"])
                if canon_row is not None
                else np.nan,
                "native_mean_abs_delta": float(native_row["mean_abs_delta"])
                if native_row is not None
                else np.nan,
                "native_mean_delta": float(native_row["mean_delta"])
                if native_row is not None
                else np.nan,
            }
        )

    df = pd.DataFrame(rows).sort_values("line_id").reset_index(drop=True)
    df.to_csv(OUT_CSV, index=False)

    # Simple correlations
    def corr(a: str, b: str) -> float:
        x = df[a].to_numpy()
        y = df[b].to_numpy()
        mask = ~np.isnan(x) & ~np.isnan(y)
        if mask.sum() == 0:
            return float("nan")
        return float(np.corrcoef(x[mask], y[mask])[0, 1])

    corr_native_abs = {
        "var_q": corr("native_mean_abs_delta", "var_q"),
        "mean_q": corr("native_mean_abs_delta", "mean_q"),
        "abs_mean_q": corr("native_mean_abs_delta", "abs_mean_q"),
        "unique_k_mod6": corr("native_mean_abs_delta", "unique_k_mod6"),
        "unique_k_mod3": corr("native_mean_abs_delta", "unique_k_mod3"),
        "canon_mean_abs_delta": corr("native_mean_abs_delta", "canon_mean_abs_delta"),
    }

    corr_sign = {
        "mean_q_vs_native_mean_delta": corr("mean_q", "native_mean_delta"),
        "mean_q_vs_canon_mean_delta": corr("mean_q", "canon_mean_delta"),
    }

    # Linear regression: predict native_mean_abs_delta from features
    feats = ["var_q", "abs_mean_q", "unique_k_mod6", "unique_k_mod3", "canon_mean_abs_delta"]
    X = df[feats].to_numpy(dtype=float)
    y = df["native_mean_abs_delta"].to_numpy(dtype=float)
    mask = ~np.isnan(X).any(axis=1) & ~np.isnan(y)
    X = X[mask]
    y = y[mask]

    # Raw regression
    X_design = np.column_stack([np.ones(len(X)), X])
    beta, *_ = np.linalg.lstsq(X_design, y, rcond=None)
    y_pred = X_design @ beta
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")

    # Standardized regression (z-score features)
    means = X.mean(axis=0)
    stds = X.std(axis=0, ddof=0)
    stds_safe = np.where(stds == 0, 1.0, stds)
    Xz = (X - means) / stds_safe
    Xz_design = np.column_stack([np.ones(len(Xz)), Xz])
    beta_z, *_ = np.linalg.lstsq(Xz_design, y, rcond=None)
    y_pred_z = Xz_design @ beta_z
    ss_res_z = np.sum((y - y_pred_z) ** 2)
    r2_z = 1.0 - ss_res_z / ss_tot if ss_tot > 0 else float("nan")

    md_lines = [
        "# Line feature regression",
        "",
        "Outputs:",
        "- `data/_workbench/02_geometry/line_feature_regression.csv`",
        "",
        "## Correlations with native mean_abs_delta",
    ]
    for k, v in corr_native_abs.items():
        md_lines.append(f"- {k}: {v:.6f}")
    md_lines += [
        "",
        "## Sign/mean correlations",
    ]
    for k, v in corr_sign.items():
        md_lines.append(f"- {k}: {v:.6f}")
    md_lines += [
        "",
        "## Linear regression (native_mean_abs_delta, raw)",
        f"- features: {', '.join(feats)}",
        f"- R2: {r2:.6f}",
        "- coefficients (intercept + features):",
        f"  - intercept: {beta[0]:.6f}",
    ]
    for name, coef in zip(feats, beta[1:]):
        md_lines.append(f"  - {name}: {coef:.6f}")

    md_lines += [
        "",
        "## Linear regression (native_mean_abs_delta, standardized features)",
        f"- R2: {r2_z:.6f}",
        "- coefficients (intercept + z-scored features):",
        f"  - intercept: {beta_z[0]:.6f}",
    ]
    for name, coef in zip(feats, beta_z[1:]):
        md_lines.append(f"  - {name}: {coef:.6f}")

    OUT_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()

