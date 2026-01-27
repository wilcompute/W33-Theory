#!/usr/bin/env python3
"""PySymmetry Z2 deck reduction on C24 and equivariance check for full H."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import scipy.sparse as sp

# PySymmetry is a local Sage-based package; add it to the path explicitly.
sys.path.append(str(Path("external/pysymmetry").resolve()))

from pysymmetry import FiniteGroup, representation  # type: ignore
from sage.all import CC, CyclicPermutationGroup, matrix  # type: ignore


def resolve_repo_root(start: Path) -> Path:
    for parent in [start] + list(start.parents):
        if (parent / ".git").exists():
            return parent
    return start.parents[2]


ROOT = resolve_repo_root(Path(__file__).resolve())
DATA = ROOT / "data"
OUT_DIR = DATA / "_workbench" / "05_symmetry"

COIN_NPZ = DATA / "_toe" / "projector_recon_20260110" / (
    "N12_58_sector_coin_C24_K4_by_k_sparse_20260109T205353Z.npz"
)
H_NPZ = DATA / "_toe" / "projector_recon_20260110" / (
    "TOE_H_total_transport_plus_lambda_coin_59x24_lam0.5_20260109T205353Z.npz"
)


def load_csr_npz(path: Path) -> sp.csr_matrix:
    z = np.load(path, allow_pickle=True)
    return sp.csr_matrix((z["data"], z["indices"], z["indptr"]), shape=tuple(z["shape"]))


def deck_swap_24() -> sp.csr_matrix:
    rows = []
    cols = []
    data = []
    for sector in range(4):
        base = sector * 6
        for phase in range(6):
            i = base + phase
            j = base + ((phase + 3) % 6)
            rows.append(i)
            cols.append(j)
            data.append(1.0)
    return sp.csr_matrix((data, (rows, cols)), shape=(24, 24))


def csr_to_sage(m: sp.csr_matrix):
    entries = {}
    indptr = m.indptr
    indices = m.indices
    data = m.data
    for i in range(m.shape[0]):
        start = indptr[i]
        end = indptr[i + 1]
        for k in range(start, end):
            j = int(indices[k])
            v = data[k]
            if v != 0:
                entries[(i, j)] = CC(v)
    return matrix(CC, m.shape[0], m.shape[1], entries, sparse=True)


def fro_norm_sparse(m: sp.csr_matrix) -> float:
    if m.nnz == 0:
        return 0.0
    return float(np.linalg.norm(m.data))


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    z24 = deck_swap_24()
    z24_sage = csr_to_sage(z24)

    coin = load_csr_npz(COIN_NPZ)
    coin_sage = csr_to_sage(coin)

    # Build Z2 representation on the 24-dim clock.
    G = FiniteGroup(CyclicPermutationGroup(2), field=CC)
    gens = G.gens()
    rep = representation(gens, [z24_sage], field=CC)

    block_info = G.quick_block_prevision(rep, block_prevision=True)

    coin_equivariant = rep.is_equivariant_to(coin_sage)
    P = G.base_equivariant_to_blocks(rep)
    coin_block = P.inverse() * coin_sage * P
    coin_block_np = np.array(coin_block, dtype=np.complex128)

    # For Z2, the equivariant blocks are expected to split 24 -> 12 + 12.
    block_cut = 12
    off_block = np.concatenate(
        [coin_block_np[:block_cut, block_cut:].ravel(), coin_block_np[block_cut:, :block_cut].ravel()]
    )
    off_block_norm = float(np.linalg.norm(off_block))
    total_norm = float(np.linalg.norm(coin_block_np.ravel()))
    off_block_ratio = off_block_norm / total_norm if total_norm else 0.0

    # Full H equivariance check via commutator in sparse arithmetic.
    h_full = load_csr_npz(H_NPZ)
    z_full = sp.kron(sp.eye(59, format="csr"), z24, format="csr")
    comm = z_full.dot(h_full) - h_full.dot(z_full)
    comm_norm = fro_norm_sparse(comm)

    # Deck parity of the u_- clock profile.
    u_minus_6 = np.array([1.0, 1.0, 1.0, -1.0, -1.0, -1.0], dtype=float) / math.sqrt(6.0)
    u_minus_24 = np.tile(u_minus_6, 4)
    deck_parity_error = float(np.linalg.norm(z24.dot(u_minus_24) + u_minus_24))

    # Write summary.
    summary_path = OUT_DIR / "pysymmetry_deck_z2_summary.md"
    with summary_path.open("w", encoding="utf-8") as f:
        f.write("# PySymmetry deck Z2 reduction (C24)\n\n")
        f.write("Inputs:\n")
        f.write(f"- {COIN_NPZ}\n")
        f.write(f"- {H_NPZ}\n\n")
        f.write("PySymmetry block prevision (degree, multiplicity):\n")
        f.write(f"- {block_info}\n\n")
        f.write("Equivariance checks:\n")
        f.write(f"- coin C24 equivariant: {coin_equivariant}\n")
        f.write(f"- full H commutator Frobenius norm: {comm_norm:.6e}\n\n")
        f.write("Block-diagonalization (coin C24):\n")
        f.write(f"- off-block Frobenius ratio: {off_block_ratio:.6e}\n\n")
        f.write("Deck parity check:\n")
        f.write(f"- ||Z u_minus + u_minus||_2 = {deck_parity_error:.6e}\n")

    block_path = OUT_DIR / "pysymmetry_deck_z2_block_info.csv"
    with block_path.open("w", encoding="utf-8") as f:
        f.write("degree,multiplicity\n")
        for row in block_info[1:]:
            f.write(f"{row[0]},{row[1]}\n")

    equiv_path = OUT_DIR / "pysymmetry_deck_z2_equivariance.csv"
    with equiv_path.open("w", encoding="utf-8") as f:
        f.write("matrix,is_equivariant,commutator_frobenius\n")
        f.write(f"coin_C24,{coin_equivariant},\n")
        f.write(f"H_full,,{comm_norm:.6e}\n")


if __name__ == "__main__":
    main()
