#!/usr/bin/env python3
"""Exact deck-Z2 block reduction of the full 59x24 Hamiltonian (flux and no-flux).

This script is intentionally *pure Python* (NumPy/SciPy only), so it runs in the
standard repo environment (see ENV.md). Sage/PySymmetry is optional; if present,
use scripts/pysymmetry_deck_z2_reduction.py for a PySymmetry API check.

Outputs (under data/_workbench/05_symmetry):
- H_total_flux_even_708.npz
- H_total_flux_odd_708.npz
- H_total_noflux_even_708.npz
- H_total_noflux_odd_708.npz
- deck_z2_blockify_fullH_summary.md
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sp

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

PROJ_RECON = DATA / "_toe" / "projector_recon_20260110"
H_TRANSPORT_NPZ = (
    PROJ_RECON / "N12_58_orbit0_H_transport_59x24_sparse_20260109T205353Z.npz"
)
COIN_NPZ = PROJ_RECON / "N12_58_sector_coin_C24_K4_by_k_sparse_20260109T205353Z.npz"
H_TOTAL_NPZ = (
    PROJ_RECON
    / "TOE_H_total_transport_plus_lambda_coin_59x24_lam0.5_20260109T205353Z.npz"
)
EDGES_CSV = PROJ_RECON / "N12_58_orbit0_edges_with_2T_connection_20260109T043900Z.csv"

OUT = DATA / "_workbench" / "05_symmetry"


def load_csr_npz(path: Path) -> sp.csr_matrix:
    z = np.load(path, allow_pickle=True)
    return sp.csr_matrix(
        (z["data"], z["indices"], z["indptr"]), shape=tuple(z["shape"])
    )


def deck_pairs():
    pairs = []
    for s in range(4):
        base = s * 6
        for ph in range(3):
            pairs.append((base + ph, base + ph + 3))
    return pairs


def build_T_even_odd_from_pairs(pairs):
    n_pairs = len(pairs)
    val = 1.0 / math.sqrt(2.0)
    rows_e = []
    cols_e = []
    data_e = []
    rows_o = []
    cols_o = []
    data_o = []
    for k, (i, j) in enumerate(pairs):
        rows_e += [i, j]
        cols_e += [k, k]
        data_e += [val, val]
        rows_o += [i, j]
        cols_o += [k, k]
        data_o += [val, -val]
    Te = sp.csr_matrix((data_e, (rows_e, cols_e)), shape=(24, n_pairs))
    To = sp.csr_matrix((data_o, (rows_o, cols_o)), shape=(24, n_pairs))
    return Te, To


def set_block_lil(
    M_lil: sp.lil_matrix, u: int, v: int, block_mat: np.ndarray, d: int = 24
):
    r0 = u * d
    c0 = v * d
    for i in range(d):
        row = r0 + i
        cols = M_lil.rows[row]
        data = M_lil.data[row]
        new_cols = []
        new_data = []
        for col, val in zip(cols, data):
            if not (c0 <= col < c0 + d):
                new_cols.append(col)
                new_data.append(val)
        M_lil.rows[row] = new_cols
        M_lil.data[row] = new_data
        for j in range(d):
            val = block_mat[i, j]
            if val != 0:
                M_lil[row, c0 + j] = float(val)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    H_transport = load_csr_npz(H_TRANSPORT_NPZ)
    coin = load_csr_npz(COIN_NPZ)
    H_total_flux = load_csr_npz(H_TOTAL_NPZ)

    # Reconstruct H_total to verify convention (H_total already equals this by design).
    I59 = sp.eye(59, format="csr")
    H_total_check = H_transport + 0.5 * sp.kron(I59, coin, format="csr")
    if (H_total_flux - H_total_check).nnz != 0:
        raise RuntimeError("H_total does not match H_transport + 0.5*(I⊗coin).")

    # Build no-flux transport by toggling the 4 defect edges e* -> e (identity block).
    edges = pd.read_csv(EDGES_CSV)
    defect = edges.loc[edges["edge_elem_2T"] == "e*", ["u", "v"]]
    defect_edges = [tuple(map(int, x)) for x in defect.to_numpy()]

    I24 = np.eye(24)
    H_nf_lil = H_transport.tolil(copy=True)
    for u, v in defect_edges:
        set_block_lil(H_nf_lil, u, v, I24)
        set_block_lil(H_nf_lil, v, u, I24)
    H_transport_noflux = H_nf_lil.tocsr()

    H_total_noflux = H_transport_noflux + 0.5 * sp.kron(I59, coin, format="csr")

    # Deck Z2 block basis (even/odd).
    pairs = deck_pairs()
    Te, To = build_T_even_odd_from_pairs(pairs)
    Ke = sp.kron(I59, Te, format="csr")
    Ko = sp.kron(I59, To, format="csr")

    # Blocks.
    H_flux_even = Ke.T @ H_total_flux @ Ke
    H_flux_odd = Ko.T @ H_total_flux @ Ko
    H_nf_even = Ke.T @ H_total_noflux @ Ke
    H_nf_odd = Ko.T @ H_total_noflux @ Ko
    H_off = Ke.T @ H_total_flux @ Ko

    d_even = H_flux_even - H_nf_even
    d_odd = H_flux_odd - H_nf_odd

    off_norm = float(np.linalg.norm(H_off.data)) if H_off.nnz else 0.0
    d_even_norm = float(np.linalg.norm(d_even.data)) if d_even.nnz else 0.0
    d_odd_norm = float(np.linalg.norm(d_odd.data)) if d_odd.nnz else 0.0

    sp.save_npz(OUT / "H_total_flux_even_708.npz", H_flux_even.tocsr())
    sp.save_npz(OUT / "H_total_flux_odd_708.npz", H_flux_odd.tocsr())
    sp.save_npz(OUT / "H_total_noflux_even_708.npz", H_nf_even.tocsr())
    sp.save_npz(OUT / "H_total_noflux_odd_708.npz", H_nf_odd.tocsr())

    # Summary.
    summary = OUT / "deck_z2_blockify_fullH_summary.md"
    with summary.open("w", encoding="utf-8") as f:
        f.write("# Deck Z2 blockify: full 59x24 Hamiltonian\n\n")
        f.write("Inputs:\n")
        f.write(f"- {H_TRANSPORT_NPZ}\n")
        f.write(f"- {COIN_NPZ}\n")
        f.write(f"- {H_TOTAL_NPZ}\n")
        f.write(f"- {EDGES_CSV}\n\n")
        f.write("Defect edges toggled (e* -> e):\n")
        for u, v in defect_edges:
            f.write(f"- ({u},{v})\n")
        f.write("\n")
        f.write("Sanity checks (should be exact zeros in this dataset):\n")
        f.write(f"- ||Ke^T H Ko||_F = {off_norm:.6e}\n")
        f.write(f"- ||ΔH_even||_F    = {d_even_norm:.6e}\n")
        f.write(f"- ||ΔH_odd||_F     = {d_odd_norm:.6e}\n")

    print("Wrote:", summary)
    print("Blocks under:", OUT)


if __name__ == "__main__":
    main()
