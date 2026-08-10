#!/usr/bin/env python3
"""Standalone bounded-LSQ candidate computation (prints JSON to stdout).
This duplicates the core logic of tools/constrained_lsq_mixed_patch.py but
is runnable as a standalone script to avoid package import issues.
"""
from __future__ import annotations

import importlib.util
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import lsq_linear

ROOT = Path(__file__).resolve().parents[1]

# load toe module by path
spec = importlib.util.spec_from_file_location(
    "toe", ROOT / "tools" / "toe_e8_z3graded_bracket_jacobi.py"
)
toe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(toe)


# helpers
def flatten(e):
    return np.concatenate(
        [e.e6.reshape(-1), e.sl3.reshape(-1), e.g1.reshape(-1), e.g2.reshape(-1)]
    )


# prepare data
E6_basis = np.load(
    ROOT / "artifacts" / "e6_27rep_basis_export" / "E6_basis_78.npy"
).astype(np.complex128)
proj = toe.E6Projector(E6_basis)
all_triads = toe._load_signed_cubic_triads()
rat = json.loads(
    (ROOT / "artifacts" / "linfty_coord_search_results_rationalized.json").read_text(encoding="utf-8")
)
bad9 = set(tuple(sorted(t)) for t in rat["original"]["fiber_triads"])
br_l2 = toe.E8Z3Bracket(
    e6_projector=proj,
    cubic_triads=[t for t in all_triads if tuple(sorted(t[:3])) not in bad9],
    scale_g1g1=1.0,
    scale_g2g2=-1.0 / 6.0,
    scale_e6=1.0,
    scale_sl3=1.0 / 6.0,
)
br_fibers = [
    toe.E8Z3Bracket(
        e6_projector=proj,
        cubic_triads=[T],
        scale_g1g1=1.0,
        scale_g2g2=-1.0 / 6.0,
        scale_e6=1.0,
        scale_sl3=1.0 / 6.0,
    )
    for T in [t for t in all_triads if tuple(sorted(t[:3])) in bad9]
]

# failing triple
from tools.exhaustive_homotopy_check_rationalized_l3 import basis_elem_g1, basis_elem_g2

x = basis_elem_g1(toe, (0, 0))
y = basis_elem_g1(toe, (17, 1))
z = basis_elem_g2(toe, (3, 0))
J = toe._jacobi(br_l2, x, y, z)
Jf = flatten(J)
inds = np.where(np.abs(Jf) > 1e-12)[0]

# build columns
Scols = []
for brf in br_fibers:
    j1 = brf.bracket(x, br_l2.bracket(y, z))
    j2 = brf.bracket(y, br_l2.bracket(z, x))
    j3 = brf.bracket(z, br_l2.bracket(x, y))
    f1 = br_l2.bracket(brf.bracket(x, y), z)
    f2 = br_l2.bracket(brf.bracket(y, z), x)
    f3 = br_l2.bracket(brf.bracket(z, x), y)
    ff1 = brf.bracket(x, brf.bracket(y, z))
    ff2 = brf.bracket(y, brf.bracket(z, x))
    ff3 = brf.bracket(z, brf.bracket(x, y))
    S = j1 + j2 + j3 + f1 + f2 + f3 + ff1 + ff2 + ff3
    Scols.append(flatten(S))
A = np.array(Scols).T
A_sub = A[inds, :]
uniform = np.array([1.0 / 9.0] * A_sub.shape[1])
r_uniform = (A_sub @ uniform) + Jf[inds]

# bounded LSQ
lb = -0.02 * np.ones(A_sub.shape[1])
ub = 0.02 * np.ones(A_sub.shape[1])
res = lsq_linear(A_sub, -r_uniform, bounds=(lb, ub), lsmr_tol="auto", max_iter=10000)
delta = res.x
rats = [Fraction(float(d)).limit_denominator(120) for d in delta]
delta_rat = np.array([float(r) for r in rats])
cand = uniform + delta_rat

# evaluate failing triple residual under candidate
l3 = toe.E8Z3.zero()
for cval, brf in zip(cand, br_fibers):
    j1 = brf.bracket(x, br_l2.bracket(y, z))
    j2 = brf.bracket(y, br_l2.bracket(z, x))
    j3 = brf.bracket(z, br_l2.bracket(x, y))
    f1 = br_l2.bracket(brf.bracket(x, y), z)
    f2 = br_l2.bracket(brf.bracket(y, z), x)
    f3 = br_l2.bracket(brf.bracket(z, x), y)
    ff1 = brf.bracket(x, brf.bracket(y, z))
    ff2 = brf.bracket(y, brf.bracket(z, x))
    ff3 = brf.bracket(z, brf.bracket(x, y))
    S = j1 + j2 + j3 + f1 + f2 + f3 + ff1 + ff2 + ff3
    l3 = l3 + S.scale(-float(cval))
res_total = toe.E8Z3(
    e6=J.e6 + l3.e6, sl3=J.sl3 + l3.sl3, g1=J.g1 + l3.g1, g2=J.g2 + l3.g2
)
res_max = float(
    max(
        np.max(np.abs(res_total.e6)),
        np.max(np.abs(res_total.sl3)),
        np.max(np.abs(res_total.g1)),
        np.max(np.abs(res_total.g2)),
    )
)

# sampled checks
rng = np.random.default_rng(20260212)


def sample_check_g1(coeffs, trials=40):
    for _ in range(trials):
        xa = toe._random_element(
            rng,
            E6_basis,
            scale0=0,
            scale1=2,
            scale2=0,
            include_g0=False,
            include_g2=False,
        )
        ya = toe._random_element(
            rng,
            E6_basis,
            scale0=0,
            scale1=2,
            scale2=0,
            include_g0=False,
            include_g2=False,
        )
        za = toe._random_element(
            rng,
            E6_basis,
            scale0=0,
            scale1=2,
            scale2=0,
            include_g0=False,
            include_g2=False,
        )
        j_l2 = toe._jacobi(br_l2, xa, ya, za)
        l3s = toe.E8Z3.zero()
        for cval, brf in zip(coeffs, br_fibers):
            j1 = brf.bracket(xa, br_l2.bracket(ya, za))
            j2 = brf.bracket(ya, br_l2.bracket(za, xa))
            j3 = brf.bracket(za, br_l2.bracket(xa, ya))
            f1 = br_l2.bracket(brf.bracket(xa, ya), za)
            f2 = br_l2.bracket(brf.bracket(ya, za), xa)
            f3 = br_l2.bracket(brf.bracket(za, xa), ya)
            ff1 = brf.bracket(xa, brf.bracket(ya, za))
            ff2 = brf.bracket(ya, brf.bracket(za, xa))
            ff3 = brf.bracket(za, brf.bracket(xa, ya))
            S = j1 + j2 + j3 + f1 + f2 + f3 + ff1 + ff2 + ff3
            l3s = l3s + S.scale(-float(cval))
        total = toe.E8Z3(
            e6=j_l2.e6 + l3s.e6,
            sl3=j_l2.sl3 + l3s.sl3,
            g1=j_l2.g1 + l3s.g1,
            g2=j_l2.g2 + l3s.g2,
        )
        if (
            float(
                max(
                    np.max(np.abs(total.e6)),
                    np.max(np.abs(total.sl3)),
                    np.max(np.abs(total.g1)),
                    np.max(np.abs(total.g2)),
                )
            )
            > 1e-8
        ):
            return False
    return True


def sample_check_g2(coeffs, trials=40):
    for _ in range(trials):
        xa = toe._random_element(
            rng,
            E6_basis,
            scale0=0,
            scale1=0,
            scale2=2,
            include_g0=False,
            include_g1=False,
        )
        ya = toe._random_element(
            rng,
            E6_basis,
            scale0=0,
            scale1=0,
            scale2=2,
            include_g0=False,
            include_g1=False,
        )
        za = toe._random_element(
            rng,
            E6_basis,
            scale0=0,
            scale1=0,
            scale2=2,
            include_g0=False,
            include_g1=False,
        )
        j_l2 = toe._jacobi(br_l2, xa, ya, za)
        l3s = toe.E8Z3.zero()
        for cval, brf in zip(coeffs, br_fibers):
            j1 = brf.bracket(xa, br_l2.bracket(ya, za))
            j2 = brf.bracket(ya, br_l2.bracket(za, xa))
            j3 = brf.bracket(za, br_l2.bracket(xa, ya))
            f1 = br_l2.bracket(brf.bracket(xa, ya), za)
            f2 = br_l2.bracket(brf.bracket(ya, za), xa)
            f3 = br_l2.bracket(brf.bracket(za, xa), ya)
            ff1 = brf.bracket(xa, brf.bracket(ya, za))
            ff2 = brf.bracket(ya, brf.bracket(za, xa))
            ff3 = brf.bracket(za, brf.bracket(xa, ya))
            S = j1 + j2 + j3 + f1 + f2 + f3 + ff1 + ff2 + ff3
            l3s = l3s + S.scale(-float(cval))
        total = toe.E8Z3(
            e6=j_l2.e6 + l3s.e6,
            sl3=j_l2.sl3 + l3s.sl3,
            g1=j_l2.g1 + l3s.g1,
            g2=j_l2.g2 + l3s.g2,
        )
        if (
            float(
                max(
                    np.max(np.abs(total.e6)),
                    np.max(np.abs(total.sl3)),
                    np.max(np.abs(total.g1)),
                    np.max(np.abs(total.g2)),
                )
            )
            > 1e-8
        ):
            return False
    return True


ok_g1 = sample_check_g1(cand)
ok_g2 = sample_check_g2(cand)

out = {
    "delta_rational": [str(r) for r in rats],
    "candidate_rational": [str(Fraction(c).limit_denominator(240)) for c in cand],
    "candidate_float": [float(round(c, 12)) for c in cand],
    "failing_triple_residual": res_max,
    "pure_sample_g1_ok": ok_g1,
    "pure_sample_g2_ok": ok_g2,
}
print(json.dumps(out, indent=2))
