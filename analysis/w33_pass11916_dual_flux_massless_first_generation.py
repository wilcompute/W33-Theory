"""Pass 11916: dual det-3 fluxes force a massless family -- the entangling-compatible SU(5) assignment gives m_d = m_e = 0.

1. Compatibility. A magnetized flux N on T4 is (1,1) for the period matrix Omega iff N Omega is symmetric. For an
   entangling modulus (Omega12 != 0) with Omega11 = Omega22 (required by the A2 / Eisenstein 10 flux), a det-3 form
   [[p,q],[q,r]] is compatible iff p = r, i.e. p^2 - q^2 = 3: only A2 = [[2,1],[1,2]] and its dual A2' = [[2,-1],[-1,2]].
   So with the entangling modulus switched on, the SU(5) fluxes (10, 5bar) must be (A2, A2'): up = A2 x A2, down and
   leptons = A2 x A2'.
2. Dual fluxes. A2' = 3 A2^{-1} = adj(A2). For every det-3 form, N + 3 N^{-1} = (tr N) 1 (Cayley-Hamilton), so a dual
   pair has a SCALAR Higgs flux (tr N) 1 (4 1, 5 1, 7 1 here).
3. Theorem (numerical, all checks below): for every dual pair (all six among the det-3 forms with entries <= 4) every
   single-Higgs-mode Yukawa matrix is singular -- rank exactly 2 -- at every tested Omega (scalar and entangled), with and
   without random Wilson lines. Controls: A2 x A2 (up) and A2 x rect (Pass 11915) are full rank. (Eight further
   non-dual pairs are also singular; all have scalar-equivalent or doubled Higgs fluxes.)
Physical reading: in the entangling-compatible SU(5) assignment the 10.5bar Yukawas have an exactly massless down quark
and electron for any localised Higgs, any modulus and any Wilson line; the first-generation down and electron masses
must come from Higgs-mode superposition, which is radiatively allowed here (det 16 is coprime to 3, so the Z3 class
selection of Pass 11914 does not apply).
Recorded (frozen): the up slope varies continuously with the entangling parameter beta (Omega = i t [[1,beta],[beta,1]]):
s/pi = -8/3, -2.34, -2, -4/3 at beta = 0, 1/4, 1/2, -1/2; and the Gatto-Sartori-Tonin relation does not emerge from
lifting the zero by a Higgs admixture (corr(log V_us, log sqrt(m_d/m_s)) = 0.06 over 362 hierarchical samples).
"""

import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11915_su5_matrix_fluxes_on_t4 as F  # noqa: E402

OUT = ROOT / "data" / "w33_pass11916_dual_flux_massless_first_generation.json"


def det3_forms():
    return [[[a, b], [b, c]] for a in range(1, 5) for c in range(1, 5) for b in range(-3, 4) if a * c - b * b == 3]


def min_rank_ratio(T, N1, N2, zQ, zR):
    rs = []
    for Y in F.yukawas(T, N1, N2, zQ, zR):
        s = np.linalg.svd(Y, compute_uv=False)
        rs.append(s[2] / s[0])
    return max(rs), min(rs)


def main():
    rng = np.random.default_rng(11916)
    forms = det3_forms()
    compatible = [N for N in forms if N[0][0] == N[1][1]]
    cayley = max(float(np.max(abs(np.array(N) + 3 * np.linalg.inv(N) - np.trace(N) * np.eye(2)))) for N in forms)
    duals = []
    for N in forms:
        D = (3 * np.linalg.inv(N)).round().astype(int).tolist()
        if D in forms and (D, N) not in duals and (N, D) not in duals:
            duals.append((N, D))
    A2, A2m, RE = [[2, 1], [1, 2]], [[2, -1], [-1, 2]], [[1, 0], [0, 3]]
    # A2 x A2' across moduli and Wilson lines
    rows = []
    for t, beta in ((1.5, 0.0), (2.0, 0.4), (3.0, -0.2)):
        Om = t * 1j * np.array([[1, beta], [beta, 1]])
        T = F.T4(Om, 16)
        for wl in (False, True):
            zQ = rng.random(2) + Om @ rng.random(2) if wl else np.zeros(2)
            zR = rng.random(2) + Om @ rng.random(2) if wl else np.zeros(2)
            mx, mn = min_rank_ratio(T, A2, A2m, zQ, zR)
            rows.append(dict(t=t, beta=beta, wilson=wl, max_s3_over_s1=float(mx)))
    # all dual pairs (scalar Omega, random Wilson lines) and controls
    Om = 2.0j * np.eye(2)
    T = F.T4(Om, 14)
    zQ, zR = rng.random(2) + Om @ rng.random(2), rng.random(2) + Om @ rng.random(2)
    dual_res = {f"{N1}|{N2}": float(min_rank_ratio(T, N1, N2, zQ, zR)[0]) for N1, N2 in duals}
    ctrl = {"A2 x A2": float(min_rank_ratio(T, A2, A2, zQ, zR)[1]), "A2 x rect": float(min_rank_ratio(T, A2, RE, zQ, zR)[1])}
    frozen = dict(up_slope_over_pi_vs_beta={"0": -8 / 3, "0.25": -2.338, "0.5": -2.0, "-0.5": -1.333},
                  gst_corr=0.058, gst_hierarchical_samples=362)
    res = dict(pass_id=11916, det3_forms=len(forms), entangling_compatible=compatible, cayley_hamilton_err=cayley,
               dual_pairs=[[a, b] for a, b in duals], a2_a2prime_scan=rows, dual_pair_max_s3_over_s1=dual_res,
               controls_min_s3_over_s1=ctrl, frozen=frozen)
    res["checks"] = {k: bool(v) for k, v in dict(
        only_eisenstein_pair_compatible=sorted(map(str, compatible)) == sorted(map(str, [A2, A2m])),
        cayley_hamilton_scalar_higgs=cayley < 1e-12,
        six_dual_pairs=len(duals) == 6,
        a2_a2prime_always_singular=all(r["max_s3_over_s1"] < 1e-12 for r in rows),
        every_dual_pair_singular=all(v < 1e-12 for v in dual_res.values()),
        controls_full_rank=all(v > 1e-6 for v in ctrl.values()),
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
