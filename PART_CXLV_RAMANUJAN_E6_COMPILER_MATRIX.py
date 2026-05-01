#!/usr/bin/env python3
"""
PART CXLV — Ramanujan E6 Compiler Matrix
========================================

Part CXLIV showed that the selected QCD coupling is a two-sector Hashimoto
compiler: the positive sector supplies the bare carrier, while the negative
Phi6 sector supplies the QCD-local threshold.

This module identifies the deeper representation-theoretic skeleton behind
that split.

The nontrivial Hashimoto/Ramanujan shell has two complex quadratic sectors:

    lambda =  2: multiplicity 24, field Q(sqrt(-10))
    lambda = -4: multiplicity 15, field Q(sqrt(-7))

When counted as real B-eigenmodes, these are

    2*24 + 2*15 = 48 + 30 = 78.

This is exactly the dimension of E6.  Even more suggestively,

    24 = dim su(5)
    15 = dim so(6) = dim su(4)

so the Ramanujan shell decomposes as a two-adjoint compiler:

    E6_shell = SU(5)_carrier sector + SO(6)/SU(4)_threshold sector
             = 24 complex modes + 15 complex modes
             = 48 real modes + 30 real modes.

The selected QCD branch from CXLIV is then not arbitrary:

    k3_bare = dim SU(5) / Phi3 = 24/13
    tau_QCD = log sqrt(mu/Phi6) from the SO(6)/Phi6 sector.

This is the first clean algebraic explanation of why the RG solution uses
24 in the bare factor and 7 in the threshold: they are the two adjoint halves
of the 78-dimensional Ramanujan/E6 shell.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent

Q = 3
V = 40
K = 12
MU = 4
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
HASHIMOTO_Q = K - 1

POSITIVE_MULT = 24
NEGATIVE_MULT = 15
POSITIVE_REAL_DIM = 2 * POSITIVE_MULT
NEGATIVE_REAL_DIM = 2 * NEGATIVE_MULT
RAMANUJAN_REAL_DIM = POSITIVE_REAL_DIM + NEGATIVE_REAL_DIM
RAMANUJAN_COMPLEX_DIM = POSITIVE_MULT + NEGATIVE_MULT


@dataclass(frozen=True)
class CompilerSector:
    name: str
    adjacency_eigenvalue: int
    complex_multiplicity: int
    real_dimension: int
    hashimoto_roots: str
    quadratic_field: str
    adjoint_identification: str
    compiler_role: str
    qcd_formula_piece: str


def compiler_sectors() -> List[CompilerSector]:
    return [
        CompilerSector(
            name="positive carrier sector",
            adjacency_eigenvalue=2,
            complex_multiplicity=POSITIVE_MULT,
            real_dimension=POSITIVE_REAL_DIM,
            hashimoto_roots="1 ± i√Phi4 = 1 ± i√10",
            quadratic_field="Q(√-Phi4) = Q(√-10)",
            adjoint_identification="dim su(5) = 24",
            compiler_role="bare visible/GUT carrier",
            qcd_formula_piece="k3_bare = 24/Phi3",
        ),
        CompilerSector(
            name="negative threshold sector",
            adjacency_eigenvalue=-4,
            complex_multiplicity=NEGATIVE_MULT,
            real_dimension=NEGATIVE_REAL_DIM,
            hashimoto_roots="-2 ± i√Phi6 = -2 ± i√7",
            quadratic_field="Q(√-Phi6) = Q(√-7)",
            adjoint_identification="dim so(6) = dim su(4) = 15",
            compiler_role="QCD/confinement heavy-threshold carrier",
            qcd_formula_piece="tau = log sqrt(mu/Phi6)",
        ),
    ]


def su_n_adjoint_dim(n: int) -> int:
    return n * n - 1


def so_n_adjoint_dim(n: int) -> int:
    return n * (n - 1) // 2


def ramanujan_e6_audit() -> Dict[str, object]:
    sectors = compiler_sectors()

    checks = {
        "positive_mult_is_su5_adjoint": POSITIVE_MULT == su_n_adjoint_dim(5),
        "negative_mult_is_so6_adjoint": NEGATIVE_MULT == so_n_adjoint_dim(6),
        "negative_mult_is_su4_adjoint": NEGATIVE_MULT == su_n_adjoint_dim(4),
        "real_shell_is_E6_dim": RAMANUJAN_REAL_DIM == 78,
        "complex_shell_is_3Phi3": RAMANUJAN_COMPLEX_DIM == 3 * PHI3,
        "real_shell_is_6Phi3": RAMANUJAN_REAL_DIM == 6 * PHI3,
        "positive_real_dim": POSITIVE_REAL_DIM,
        "negative_real_dim": NEGATIVE_REAL_DIM,
        "split_ratio_complex": f"{POSITIVE_MULT}:{NEGATIVE_MULT}=8:5",
        "split_ratio_real": f"{POSITIVE_REAL_DIM}:{NEGATIVE_REAL_DIM}=8:5",
    }

    assert all(v is True for k, v in checks.items() if k.endswith("adjoint") or k.endswith("dim") or k.startswith("complex") or k.startswith("real_shell"))
    assert RAMANUJAN_REAL_DIM == 78
    assert RAMANUJAN_COMPLEX_DIM == 39

    return {
        "module": "PART_CXLV_RAMANUJAN_E6_COMPILER_MATRIX",
        "w33_atoms": {
            "q": Q,
            "v": V,
            "k": K,
            "mu": MU,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
            "Hashimoto_q": HASHIMOTO_Q,
        },
        "shell_decomposition": {
            "complex_dimensions": "24 + 15 = 39 = 3*Phi3",
            "real_dimensions": "48 + 30 = 78 = dim(E6) = 6*Phi3",
            "ratio": "24:15 = 48:30 = 8:5",
        },
        "compiler_sectors": [asdict(s) for s in sectors],
        "representation_identifications": {
            "positive_24": "dim su(5) = 5^2 - 1 = 24",
            "negative_15": "dim so(6) = 6*5/2 = 15 = dim su(4)",
            "ramanujan_78": "2*(24+15)=78 = dim E6",
            "complex_39": "24+15=39=3*Phi3",
        },
        "qcd_compiler_rule": {
            "carrier": "positive Q(√-10) / su(5)-adjoint sector gives k3_bare=24/Phi3",
            "threshold": "negative Q(√-7) / so(6)-adjoint sector gives tau=log sqrt(mu/Phi6)",
            "compiled_formula": "alpha_s(MGUT)=alpha_unified/(24/Phi3)*(1+alpha_unified/(2π)*log sqrt(mu/Phi6))",
        },
        "checks": checks,
        "theorem_statement": (
            "The 78-dimensional Hashimoto/Ramanujan shell is an E6-sized two-adjoint "
            "compiler: its complex multiplicities 24 and 15 are exactly dim su(5) "
            "and dim so(6)=dim su(4).  The selected QCD coupling uses the su(5)-sized "
            "positive sector as the bare carrier and the so(6)/Phi6 negative sector "
            "as the heavy threshold."
        ),
        "interpretive_note": (
            "This explains why the successful alpha_s formula uses 24/13 and a Phi6 "
            "polar threshold.  The number 24 is not merely convenient; it is the "
            "positive Hashimoto multiplicity and the SU(5) adjoint dimension.  The "
            "number 15 is not passive; it is the negative Hashimoto multiplicity and "
            "the SO(6)/SU(4) adjoint dimension that carries the Phi6 threshold."
        ),
    }


def main() -> int:
    audit = ramanujan_e6_audit()
    out = ROOT / "PART_CXLV_ramanujan_e6_compiler_matrix_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
