"""
Apply W(3,3) line/projective-class clock projectors to the 59x24 orbit0 clock Hamiltonian evolution.

Inputs (expected in /mnt/data):
- TOE_H_total_transport_plus_lambda_coin_59x24_lam0.5_20260109T205353Z.npz
- TOE_W33_clock_projector_masks_20260109T210928Z.npz  (contains w33_masks[40,24], projective_masks[12,24])

Outputs:
- TOE_time_evolution_W33_line_projector_probs_lam0.5_<timestamp>.csv

Notes:
- Projective-class projectors (12) partition the 24-state clock, so their probabilities sum to 1.
- W33 line projectors (40) overlap (except the 12 monochrome ones), so line probabilities are "membership weights"
  rather than a single projective measurement.
"""

from datetime import datetime

import numpy as np
import pandas as pd
import scipy.sparse as sp
import scipy.sparse.linalg as spla

BASE = "/mnt/data"


def load_csr_npz(path: str) -> sp.csr_matrix:
    z = np.load(path, allow_pickle=True)
    shape = tuple(z["shape"])
    return sp.csr_matrix((z["data"], z["indices"], z["indptr"]), shape=shape)


def evolve_and_measure(
    H_path: str = f"{BASE}/TOE_H_total_transport_plus_lambda_coin_59x24_lam0.5_20260109T205353Z.npz",
    masks_path: str = f"{BASE}/TOE_W33_clock_projector_masks_20260109T210928Z.npz",
    times=(0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0),
    node0: int = 0,
    clock0: int = 0,
):
    H = load_csr_npz(H_path)
    data = np.load(masks_path, allow_pickle=True)
    w33_masks = data["w33_masks"].astype(np.float64)  # (40,24)
    proj_masks = data["projective_masks"].astype(np.float64)  # (12,24)
    proj_classes = [str(x) for x in data["projective_classes"]]

    n = H.shape[0]
    assert n == 59 * 24, n

    psi0 = np.zeros((n,), dtype=np.complex128)
    psi0[node0 * 24 + clock0] = 1.0

    A = (-1j) * H
    times = np.array(list(times), dtype=float)
    psis = spla.expm_multiply(
        A, psi0, start=times[0], stop=times[-1], num=len(times), endpoint=True
    )

    rows = []
    for t, psi in zip(times, psis):
        mat = psi.reshape((59, 24))
        clock_mass = np.sum(np.abs(mat) ** 2, axis=0)
        proj_probs = proj_masks @ clock_mass
        line_probs = w33_masks @ clock_mass

        row = {"t": float(t)}
        for i, c in enumerate(proj_classes):
            row[c] = float(proj_probs[i])
        for lid in range(40):
            row[f"line_{lid:02d}"] = float(line_probs[lid])
        rows.append(row)

    out = pd.DataFrame(rows)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out_path = f"{BASE}/TOE_time_evolution_W33_line_projector_probs_lam0.5_{ts}.csv"
    out.to_csv(out_path, index=False)
    print("Wrote", out_path)
    return out_path


if __name__ == "__main__":
    evolve_and_measure()
