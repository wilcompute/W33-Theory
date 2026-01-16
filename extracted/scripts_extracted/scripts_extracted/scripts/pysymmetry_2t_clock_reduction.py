#!/usr/bin/env python3
"""PySymmetry 2T clock reduction: left/right actions and equivariance checks."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
import scipy.sparse as sp

import sys
sys.path.append(str(Path("external/pysymmetry").resolve()))

from pysymmetry import FiniteGroup, representation  # type: ignore
from sage.all import CC, Permutation, PermutationGroup, matrix  # type: ignore


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT_DIR = DATA / "_workbench" / "05_symmetry"

TABLE_PATH = DATA / "_toe" / "projector_recon_20260110" / "binary_tetrahedral_2T_multiplication_table.csv"
COIN_NPZ = DATA / "_toe" / "projector_recon_20260110" / (
    "N12_58_sector_coin_C24_K4_by_k_sparse_20260109T205353Z.npz"
)
H_NPZ = DATA / "_toe" / "projector_recon_20260110" / (
    "TOE_H_total_transport_plus_lambda_coin_59x24_lam0.5_20260109T205353Z.npz"
)


def load_table(path: Path):
    with path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        elems = [h.strip() for h in header[1:] if h.strip()]
        table = {}
        for row in reader:
            row_elem = row[0].strip()
            for col_elem, prod in zip(elems, row[1:]):
                table[(row_elem, col_elem)] = prod.strip()
    return elems, table


def perm_from_action(elems, table, elem, side: str):
    idx = {e: i for i, e in enumerate(elems)}
    images = []
    for col_elem in elems:
        prod = table[(elem, col_elem)] if side == "left" else table[(col_elem, elem)]
        images.append(idx[prod] + 1)  # 1-based for Sage
    return Permutation(images)


def find_generators(elems, table, side: str):
    perms = {e: perm_from_action(elems, table, e, side) for e in elems}
    for g1 in elems:
        if g1 == "e":
            continue
        for g2 in elems:
            if g2 in ("e", g1):
                continue
            G = PermutationGroup([perms[g1], perms[g2]])
            if G.order() == 24:
                return (g1, g2), (perms[g1], perms[g2])
    raise RuntimeError(f"No generators found for {side} action.")


def load_csr_npz(path: Path) -> sp.csr_matrix:
    z = np.load(path, allow_pickle=True)
    return sp.csr_matrix((z["data"], z["indices"], z["indptr"]), shape=tuple(z["shape"]))


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


def block_sizes(block_info):
    sizes = []
    for degree, mult in block_info[1:]:
        sizes.append(int(round(float(degree) * float(mult))))
    return sizes


def action_summary(side: str, elems, table):
    (g1, g2), (p1, p2) = find_generators(elems, table, side)
    Gp = PermutationGroup([p1, p2])
    G = FiniteGroup(Gp, field=CC)
    gens = G.gens()
    rep = representation(gens, [g.matrix() for g in gens], field=CC)

    block_info = G.quick_block_prevision(rep, block_prevision=True)

    coin = load_csr_npz(COIN_NPZ)
    coin_sage = csr_to_sage(coin)
    coin_equiv = rep.is_equivariant_to(coin_sage)
    off_block_ratio = None
    if coin_equiv:
        P = G.base_equivariant_to_blocks(rep)
        coin_block = P.inverse() * coin_sage * P
        coin_np = np.array(coin_block, dtype=np.complex128)
        sizes = block_sizes(block_info)
        mask = np.zeros(coin_np.shape, dtype=bool)
        idx = 0
        for size in sizes:
            mask[idx : idx + size, idx : idx + size] = True
            idx += size
        off_block = coin_np[~mask]
        off_block_ratio = float(np.linalg.norm(off_block) / np.linalg.norm(coin_np))

    # Full-H commutator norms (generator-level).
    H = load_csr_npz(H_NPZ)
    I59 = sp.eye(59, format="csr")
    gen_info = []
    for gen in gens:
        perm24 = sp.csr_matrix(gen.matrix().numpy(dtype=float))
        g_full = sp.kron(I59, perm24, format="csr")
        comm = g_full.dot(H) - H.dot(g_full)
        gen_info.append((str(gen), fro_norm_sparse(comm)))

    return {
        "side": side,
        "generators": (g1, g2),
        "group_order": int(G.order()),
        "block_info": block_info,
        "coin_equivariant": coin_equiv,
        "coin_off_block_ratio": off_block_ratio,
        "gen_commutators": gen_info,
    }


def write_summary(res, out_path: Path):
    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"# PySymmetry 2T clock reduction ({res['side']} action)\n\n")
        f.write("Generators (by 2T labels):\n")
        f.write(f"- {res['generators'][0]}\n")
        f.write(f"- {res['generators'][1]}\n\n")
        f.write(f"Group order: {res['group_order']}\n\n")
        f.write("Block prevision (degree, multiplicity):\n")
        f.write(f"- {res['block_info']}\n\n")
        f.write("Equivariance:\n")
        f.write(f"- coin C24 equivariant: {res['coin_equivariant']}\n")
        if res["coin_off_block_ratio"] is not None:
            f.write(f"- coin off-block ratio: {res['coin_off_block_ratio']:.6e}\n")
        f.write("\nGenerator commutators (full H):\n")
        for gen, norm in res["gen_commutators"]:
            f.write(f"- {gen}: {norm:.6e}\n")


def write_blocks(res, out_path: Path):
    with out_path.open("w", encoding="utf-8") as f:
        f.write("degree,multiplicity\n")
        for row in res["block_info"][1:]:
            f.write(f"{row[0]},{row[1]}\n")


def write_commutators(res, out_path: Path):
    with out_path.open("w", encoding="utf-8") as f:
        f.write("generator,commutator_frobenius\n")
        for gen, norm in res["gen_commutators"]:
            f.write(f"\"{gen}\",{norm:.6e}\n")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    elems, table = load_table(TABLE_PATH)

    for side in ("left", "right"):
        res = action_summary(side, elems, table)
        write_summary(res, OUT_DIR / f"pysymmetry_2t_{side}_summary.md")
        write_blocks(res, OUT_DIR / f"pysymmetry_2t_{side}_block_info.csv")
        write_commutators(res, OUT_DIR / f"pysymmetry_2t_{side}_commutators.csv")


if __name__ == "__main__":
    main()
