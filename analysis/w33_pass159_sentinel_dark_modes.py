#!/usr/bin/env python3
"""Pass 159: the sentinel space is the trade lattice -- dark modes, quantized.

The holonet security layer detects intrusion as a spectral anomaly against
the g=15 sentinel eigenspace, with "legal traffic sentinel-dark".  Pass 158
proved the (-4)-eigenlattice is the incidence kernel (the trade lattice).
This witness turns that identification into an exact readout-security
theorem package:

1. READOUT SPECTRAL LAW.  The context readout map N (line-point incidence)
   has Gram N^T N = mu*I + A with exact spectrum {16, 6, 0} and
   multiplicities {1, 24, 15}: readout gain 16 = 2^mu on the Perron mode,
   6 = q! on the gauge sector, 0 on the sentinel sector.  The line-side
   Gram N N^T is the concurrence graph, again SRG(40,12,2,4) -- same parameters, not self-dual (q=3 odd; W(3,q) is self-dual iff q even -- Pass 4563/4755).

2. READOUT/DARK DUALITY.  The context-generated code lattice im(N^T) is
   saturated (SNF of N = diag(1^25, 0^15)) and its determinant equals the
   dark lattice's: det(im N^T) = det(ker N) = 2^17 3^10 =
   [Z^40 : im(N^T) + ker(N)].

3. EXTERNAL BALANCE.  Every minimal dark mode is invisible off its own
   support pointwise: each of the 32 off-support points sees equally many
   +1 and -1 support neighbors, so the restricted K44 crossbar drive alone
   carries the full eigenvector equation.

4. THE SENTINEL CODE.  The F2 reduction ker_F2(N) is a [40,15] binary code
   whose full weight enumerator is computed; its minimum distance is the
   dark-mode support quantum, and its minimum-weight words are exactly the
   45 trade supports.  Consequence: every nonzero integer tamper pattern
   of support < d_min excites at least one measurement context.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys

import numpy as np
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass158_chiral_trade_lattice_two_480s import (
    build_w33,
    fincke_pohst,
    lattices_equal,
    minimal_shell,
    saturated_kernel,
    w33_lines,
)

OUT = ROOT / "data" / "w33_pass159_sentinel_dark_modes.json"


def main():
    points, adjacency, _ = build_w33()
    identity = np.eye(40, dtype=np.int64)
    lines = w33_lines(adjacency)
    checks = {}

    incidence = np.zeros((40, 40), dtype=np.int64)
    for row, line in enumerate(lines):
        for point in line:
            incidence[row, point] = 1

    # ------------------------------------------------------------------
    # 1. readout spectral law
    # ------------------------------------------------------------------
    point_gram = incidence.T @ incidence
    checks["readout_gram_is_muI_plus_A"] = bool(
        np.array_equal(point_gram, 4 * identity + adjacency)
    )
    eigenvalues = np.linalg.eigvalsh(point_gram.astype(float))
    spectrum = Counter(int(round(v)) for v in eigenvalues)
    checks["readout_spectrum_16_6_0"] = spectrum == Counter({16: 1, 6: 24, 0: 15})

    line_gram = incidence @ incidence.T
    line_adjacency = (line_gram > 0).astype(np.int64) - np.eye(40, dtype=np.int64)
    la2 = line_adjacency @ line_adjacency
    degrees_ok = bool((line_adjacency.sum(axis=1) == 12).all())
    srg_ok = degrees_ok
    for a, b in combinations(range(40), 2):
        expected = 2 if line_adjacency[a, b] else 4
        if la2[a, b] != expected:
            srg_ok = False
            break
    checks["line_concurrence_is_srg_40_12_2_4"] = bool(srg_ok)
    checks["line_gram_is_muI_plus_dual_A"] = bool(
        np.array_equal(line_gram, 4 * np.eye(40, dtype=np.int64) + line_adjacency)
    )

    # ------------------------------------------------------------------
    # 2. readout/dark duality
    # ------------------------------------------------------------------
    incidence_snf = smith_normal_form(Matrix(incidence.tolist()), domain=ZZ)
    diag = [abs(int(incidence_snf[i, i])) for i in range(40)]
    checks["incidence_snf_trivial"] = sorted(diag) == [0] * 15 + [1] * 25

    dark = saturated_kernel(adjacency + 4 * identity)
    trade = saturated_kernel(incidence)
    checks["dark_equals_trade"] = lattices_equal(dark, trade)

    # saturated image of N^T: the orthogonal complement of the dark lattice
    # inside Z^40, built as the saturated kernel of dark^T (padded square)
    padded = np.zeros((40, 40), dtype=np.int64)
    padded[:15, :] = dark.T
    code = saturated_kernel(padded)
    checks["code_rank_25"] = code.shape == (40, 25)

    def in_span_integrally(basis, vector):
        mat = Matrix(basis.tolist())
        target = Matrix([[int(v)] for v in vector])
        gram_b = mat.T * mat
        solution = gram_b.solve(mat.T * target)
        if mat * solution != target:
            return False
        return all(value.is_Integer for value in solution)

    checks["code_contains_all_context_rows"] = all(
        in_span_integrally(code, incidence[r]) for r in range(40)
    )
    code_det = int(Matrix((code.T @ code).tolist()).det())
    dark_det = int(Matrix((dark.T @ dark).tolist()).det())
    checks["duality_det_code_equals_det_dark"] = code_det == dark_det
    checks["duality_det_is_2_17_3_10"] = dark_det == 2**17 * 3**10
    stack = np.column_stack([code, dark])
    glue_index = abs(int(Matrix(stack.tolist()).det()))
    checks["duality_index_equals_det"] = glue_index == dark_det

    # ------------------------------------------------------------------
    # 3. external balance of the minimal dark modes
    # ------------------------------------------------------------------
    min_norm, shell, _, _ = minimal_shell(dark)
    checks["ninety_dark_modes_norm_8"] = min_norm == 8 and len(shell) == 90
    balance_ok = True
    balance_profile = Counter()
    crossbar_ok = True
    for vector in shell:
        vector = np.asarray(vector, dtype=np.int64)
        support = np.flatnonzero(vector)
        support_set = set(support.tolist())
        for p in range(40):
            if p in support_set:
                continue
            neighbor_values = vector[np.flatnonzero(adjacency[p])]
            plus = int((neighbor_values == 1).sum())
            minus = int((neighbor_values == -1).sum())
            if plus != minus:
                balance_ok = False
            balance_profile[(plus, minus)] += 1
        sub = adjacency[np.ix_(support, support)]
        if not np.array_equal(sub @ vector[support], -4 * vector[support]):
            crossbar_ok = False
    checks["external_balance_law"] = bool(balance_ok)
    checks["crossbar_drive_carries_eigenvalue"] = bool(crossbar_ok)

    # ------------------------------------------------------------------
    # 4. the F2 sentinel code
    # ------------------------------------------------------------------
    basis_2 = (dark % 2).astype(np.uint8)
    # row-reduce over F2 to an independent generator set
    work = basis_2.T.copy()
    pivot_rows = []
    col = 0
    row = 0
    while row < work.shape[0] and col < 40:
        pivot = None
        for r in range(row, work.shape[0]):
            if work[r, col]:
                pivot = r
                break
        if pivot is None:
            col += 1
            continue
        work[[row, pivot]] = work[[pivot, row]]
        for r in range(work.shape[0]):
            if r != row and work[r, col]:
                work[r] ^= work[row]
        pivot_rows.append(row)
        row += 1
        col += 1
    generators = work[: len(pivot_rows)]
    dim = generators.shape[0]
    checks["sentinel_code_dimension_15"] = dim == 15

    coefficients = np.array(
        [[(m >> b) & 1 for b in range(dim)] for m in range(2**dim)],
        dtype=np.uint8,
    )
    codewords = (coefficients @ generators) % 2
    weights = codewords.sum(axis=1)
    enumerator = Counter(int(w) for w in weights)
    min_weight = min(w for w in enumerator if w > 0)
    checks["sentinel_min_distance_8"] = min_weight == 8
    weight8 = codewords[weights == 8]
    supports_from_code = {frozenset(np.flatnonzero(word).tolist()) for word in weight8}
    supports_from_shell = {
        frozenset(np.flatnonzero(np.asarray(v)).tolist()) for v in shell
    }
    checks["weight8_words_are_the_45_supports"] = (
        len(weight8) == 45 and supports_from_code == supports_from_shell
    )
    checks["all_codewords_kill_every_line_mod2"] = bool(
        ((codewords @ incidence.T) % 2 == 0).all()
    )

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass159.sentinel_dark_modes.v1",
        "status": "PASS" if all_pass else "FAIL",
        "readout_law": {
            "point_gram": "N^T N = 4 I + A",
            "spectrum": {"16": 1, "6": 24, "0": 15},
            "reading": (
                "readout gain 2^mu=16 on the Perron mode, q!=6 on the "
                "gauge sector, 0 on the g=15 sentinel sector: the sentinel "
                "eigenspace is exactly the readout kernel"
            ),
            "line_side": "N N^T = 4 I + A_dual, concurrence SRG(40,12,2,4)",
        },
        "duality": {
            "det_code_lattice": code_det,
            "det_dark_lattice": dark_det,
            "glue_index": glue_index,
            "identity": "det(im N^T) = det(ker N) = [Z^40 : im + ker] = 2^17 3^10",
        },
        "dark_modes": {
            "count": len(shell),
            "norm": int(min_norm),
            "external_balance_profile": {
                str(k): int(v) for k, v in sorted(balance_profile.items())
            },
            "reading": (
                "every off-support point sees equal +/- support neighbors, "
                "so each dark mode is pointwise invisible outside its own "
                "K44 crossbar, which alone carries A x = -4 x"
            ),
        },
        "sentinel_code": {
            "parameters": "[40, 15, 8] over F2",
            "weight_enumerator": {
                str(k): int(v) for k, v in sorted(enumerator.items())
            },
            "minimum_weight_words": 45,
            "identification": (
                "the 45 weight-8 codewords are exactly the 45 trade "
                "supports (binary-polar K44 octads)"
            ),
            "security_reading": (
                "any nonzero integer tamper pattern of support < 8 has a "
                "nonzero odd part of weight < 8, hence lies outside the "
                "code and excites at least one of the 40 contexts: "
                "sub-8 anomalies are always context-visible, and the "
                "cheapest context-invisible excitation is quantized at "
                "norm 8 with exactly 90 modes"
            ),
        },
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
