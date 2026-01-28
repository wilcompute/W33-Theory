#!/usr/bin/env python3
"""PySymmetry D6 incidence reduction on 12 points and 15 rainbow lines."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path("external/pysymmetry").resolve()))

from pysymmetry import FiniteGroup, representation  # type: ignore
from sage.all import CC, Permutation, PermutationGroup, matrix  # type: ignore


def resolve_repo_root(start: Path) -> Path:
    for parent in [start] + list(start.parents):
        if (parent / ".git").exists():
            return parent
    return start.parents[2]


ROOT = resolve_repo_root(Path(__file__).resolve())
DATA = ROOT / "data"
OUT_DIR = DATA / "_workbench" / "05_symmetry"

POINT_MAPS = (
    DATA
    / "_is"
    / "incidence_autgroup_20260110"
    / "automorphism_group_order12_point_maps.csv"
)
LINES_CSV = (
    DATA / "_is" / "incidence_autgroup_20260110" / "incidence_12points_15lines.csv"
)
KERNEL_CSV = (
    DATA / "_workbench" / "04_measurement" / "nativeC24_mode1_pairwise_kernel.csv"
)


def load_point_perms(path: Path):
    with path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        labels = header[1:]
        perms = {}
        for row in reader:
            auto_id = int(row[0])
            images = [labels.index(x) + 1 for x in row[1:]]  # 1-based
            perms[auto_id] = Permutation(images)
    return labels, perms


def find_generators(perms):
    ids = list(perms.keys())
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            g1 = perms[ids[i]]
            g2 = perms[ids[j]]
            G = PermutationGroup([g1, g2])
            if G.order() == 12:
                return (ids[i], ids[j]), (g1, g2)
    raise RuntimeError("No D6 generators found.")


def load_lines(path: Path):
    lines = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            line_id = int(row["w33_rainbow_line_id"])
            quartet = tuple(row["full_quartet"].split())
            lines.append((line_id, frozenset(quartet)))
    return lines


def line_permutation(perms, labels, lines):
    label_index = {l: i for i, l in enumerate(labels)}
    line_index = {line_id: i for i, (line_id, _) in enumerate(lines)}
    quartet_to_line = {quartet: line_id for line_id, quartet in lines}

    line_perms = {}
    for auto_id, p in perms.items():
        mapping = []
        for line_id, quartet in lines:
            mapped = []
            for lab in quartet:
                mapped.append(labels[p(label_index[lab] + 1) - 1])
            mapped_line = quartet_to_line[frozenset(mapped)]
            mapping.append(line_index[mapped_line] + 1)  # 1-based
        line_perms[auto_id] = Permutation(mapping)
    return line_perms


def load_kernel(path: Path, labels):
    idx = {lab: i for i, lab in enumerate(labels)}
    K = np.zeros((len(labels), len(labels)), dtype=float)
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            a = idx[row["class_a"]]
            b = idx[row["class_b"]]
            w = float(row["weight"])
            K[a, b] = w
            K[b, a] = w
    return K


def commutator_norms(perms, K):
    norms = []
    for auto_id, p in perms.items():
        P = np.zeros_like(K)
        for i in range(K.shape[0]):
            P[i, p(i + 1) - 1] = 1.0
        comm = P @ K - K @ P
        norms.append((auto_id, float(np.linalg.norm(comm))))
    return norms


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    labels, perms = load_point_perms(POINT_MAPS)
    (gen_id1, gen_id2), (g1, g2) = find_generators(perms)

    Gp = PermutationGroup([g1, g2])
    G = FiniteGroup(Gp, field=CC)
    gens = G.gens()
    rep12 = representation(gens, [g.matrix() for g in gens], field=CC)
    block12 = G.quick_block_prevision(rep12, block_prevision=True)

    # Line representation.
    lines = load_lines(LINES_CSV)
    line_perms = line_permutation(perms, labels, lines)
    lg1 = line_perms[gen_id1]
    lg2 = line_perms[gen_id2]
    Gp_lines = PermutationGroup([lg1, lg2])
    Gl = FiniteGroup(Gp_lines, field=CC)
    gens_l = Gl.gens()
    rep15 = representation(gens_l, [g.matrix() for g in gens_l], field=CC)
    block15 = Gl.quick_block_prevision(rep15, block_prevision=True)

    # Mode-1 pairwise kernel equivariance (commutator norms).
    K = load_kernel(KERNEL_CSV, labels)
    comm_norms = commutator_norms(perms, K)
    comm_max = max(n for _, n in comm_norms)
    comm_mean = float(np.mean([n for _, n in comm_norms]))

    summary_path = OUT_DIR / "pysymmetry_d6_incidence_summary.md"
    with summary_path.open("w", encoding="utf-8") as f:
        f.write("# PySymmetry D6 incidence reduction\n\n")
        f.write("Generators (auto_id):\n")
        f.write(f"- {gen_id1}\n")
        f.write(f"- {gen_id2}\n\n")
        f.write(f"Point action group order: {int(G.order())}\n")
        f.write(f"Line action group order: {int(Gl.order())}\n\n")
        f.write("Block prevision (12-point action):\n")
        f.write(f"- {block12}\n\n")
        f.write("Block prevision (15-line action):\n")
        f.write(f"- {block15}\n\n")
        f.write("Mode-1 kernel equivariance (commutator norms):\n")
        f.write(f"- mean: {comm_mean:.6e}\n")
        f.write(f"- max: {comm_max:.6e}\n")

    block12_path = OUT_DIR / "pysymmetry_d6_points_block_info.csv"
    with block12_path.open("w", encoding="utf-8") as f:
        f.write("degree,multiplicity\n")
        for row in block12[1:]:
            f.write(f"{row[0]},{row[1]}\n")

    block15_path = OUT_DIR / "pysymmetry_d6_lines_block_info.csv"
    with block15_path.open("w", encoding="utf-8") as f:
        f.write("degree,multiplicity\n")
        for row in block15[1:]:
            f.write(f"{row[0]},{row[1]}\n")

    comm_path = OUT_DIR / "pysymmetry_d6_kernel_commutators.csv"
    with comm_path.open("w", encoding="utf-8") as f:
        f.write("auto_id,commutator_frobenius\n")
        for auto_id, norm in comm_norms:
            f.write(f"{auto_id},{norm:.6e}\n")


if __name__ == "__main__":
    main()
