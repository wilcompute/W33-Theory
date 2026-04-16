#!/usr/bin/env python3
"""
Global CKM fit: jointly optimize diagonal row/column scalings and a complex 3x3 matrix
to minimize || |U| - diag(L) M diag(R) ||_F^2 with a unitarity penalty on U.

Writes `data/ckm_global_fit.json` with fitted scales, unitary, and diagnostics.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np

try:
    from scipy.optimize import minimize
except Exception as e:  # pragma: no cover - SciPy may be absent
    raise RuntimeError("scipy is required for this script; install with `pip install scipy`")


DATA_DIR = Path("data")


def load_json(p: Path):
    if not p.exists():
        return None
    return json.loads(p.read_text())


def save_json(p: Path, d: dict):
    p.parent.mkdir(exist_ok=True)
    p.write_text(json.dumps(d, indent=2))


def unitary_penalty(U: np.ndarray) -> float:
    # U expected shape (3,3) complex
    I = np.eye(3, dtype=complex)
    C = U.conj().T @ U - I
    return float(np.linalg.norm(C, ord='fro') ** 2)


def loss_and_metrics(x, M, mu=50.0):
    # x: length 24 => 18 for U (real/imag), 3 log-left, 3 log-right
    U_re = x[:9].reshape(3, 3)
    U_im = x[9:18].reshape(3, 3)
    U = U_re + 1j * U_im
    l = x[18:21]
    r = x[21:24]
    sL = np.exp(l)
    sR = np.exp(r)
    S = (np.diag(sL) @ M @ np.diag(sR)).astype(float)

    mag = np.abs(U)
    data_term = float(np.linalg.norm(mag - S, ord='fro') ** 2)
    pen = unitary_penalty(U)
    total = data_term + mu * pen
    return total, dict(data_term=float(data_term), unitary_penalty=float(pen), sL=sL.tolist(), sR=sR.tolist(), S=S.tolist(), U=U)


def run_global_fit():
    src = load_json(DATA_DIR / "ckm_from_grams.json")
    if not src:
        print("Missing data/ckm_from_grams.json — run the upstream pipeline first.")
        return 2

    M = np.array(src.get("overlap_matrix", []), dtype=float)
    exp = np.array(src.get("experimental", []), dtype=float)

    # Use existing fitted scales and phase-reconstruction as initialization if available
    fit = load_json(DATA_DIR / "ckm_fitted_scalings.json") or {}
    pr = load_json(DATA_DIR / "ckm_phase_reconstruction.json") or {}

    left0 = np.array(fit.get("left_scales", [1.0, 1.0, 1.0]), dtype=float)
    right0 = np.array(fit.get("right_scales", [1.0, 1.0, 1.0]), dtype=float)

    if pr and pr.get("unitary_real") and pr.get("unitary_imag"):
        U0 = np.array(pr["unitary_real"]) + 1j * np.array(pr["unitary_imag"])  # shape 3x3
    else:
        # fallback: random orthonormal via QR
        q, _ = np.linalg.qr(np.random.randn(3, 3) + 1j * np.random.randn(3, 3))
        U0 = q

    # initial x
    x0 = np.zeros(24, dtype=float)
    x0[:9] = U0.real.reshape(-1)
    x0[9:18] = U0.imag.reshape(-1)
    x0[18:21] = np.log(left0)
    x0[21:24] = np.log(right0)

    # objective wrapper
    def obj(x):
        val, _ = loss_and_metrics(x, M, mu=50.0)
        return val

    print("Starting global fit: optimizing U (18 reals) + log-scales (6)")
    res = minimize(obj, x0, method="L-BFGS-B", options={"maxiter": 2000, "ftol": 1e-12})

    total, metrics = loss_and_metrics(res.x, M, mu=50.0)
    U = metrics["U"]
    sL = metrics["sL"]
    sR = metrics["sR"]
    S = np.array(metrics["S"], dtype=float)

    # project U to nearest unitary via SVD
    try:
        u, s, vh = np.linalg.svd(U)
        U_proj = (u @ vh).astype(complex)
        proj_pen = unitary_penalty(U_proj)
    except Exception:
        U_proj = U
        proj_pen = unitary_penalty(U_proj)

    abs_mat = np.abs(U_proj)
    abs2 = (abs_mat ** 2).tolist()

    out = {
        "left_scales": sL,
        "right_scales": sR,
        "scaled_matrix": S.tolist(),
        "unitary_real": U_proj.real.tolist(),
        "unitary_imag": U_proj.imag.tolist(),
        "abs": abs_mat.tolist(),
        "abs2": abs2,
        "final_loss": float(total),
        "final_unitary_penalty": float(proj_pen),
        "optimizer_success": bool(res.success),
        "optimizer_message": str(res.message),
    }

    save_json(DATA_DIR / "ckm_global_fit.json", out)
    print("Wrote data/ckm_global_fit.json — success:", res.success, res.message)
    print("Final loss:", total, "unitarity penalty:", proj_pen)
    return 0


if __name__ == "__main__":
    raise SystemExit(run_global_fit())
