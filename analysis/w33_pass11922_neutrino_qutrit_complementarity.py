"""Pass 11922: the neutrino Weinberg channel is the qutrit-2 mirror of the up sector, and CKM and PMNS are the two
marginal Schmidt bases of one theta state -- but modulus anisotropy does not make them complementary.

1. Mirror. For every det-3 5bar flux N5 (all 12 forms), the L x L channel (flux 2 N5, the Weinberg operator
   L L H_u H_u) is monomial per Higgs-pair mode (qutrit-2 selection, Pass 11921: K(L_{2 N5})[3] = K5), and its
   top-Yukawa Gram space is exactly 3-dimensional: the Higgs pair is a flavour qutrit h. Because both L carry the same
   Wilson line (and the same hypercharge), the 2-cycle entries are always equal: every single-class neutrino mass
   matrix has an EXACTLY degenerate pair (to 1e-12), and in the qutrit space M_nu(h)_{bb'} = h_{b+b'} g'_{b-b'} with
   g'_+ = g'_- -- automatically symmetric, as a Majorana matrix must be.
2. Marginals. Up quarks and neutrinos are single-qutrit (monomial) sectors; down quarks and charged leptons are the
   two-qutrit theta state across the factorisation. So the CKM is the qutrit-1 (left) Schmidt basis of the down theta
   state read in the up basis, and the PMNS is the qutrit-2 (right) Schmidt basis of the charged-lepton theta state read
   in the neutrino basis.
3. Complementarity test (frozen, A2, Omega = i t (1 + beta J) + real parts, hypercharge Wilson line, radiative H_d,
   240 moduli): CKM and PMNS proxy distances (best generation assignment) are POSITIVELY correlated (+0.47), not
   complementary. beta > 0.4 favours PMNS-like lepton mixing (median log-distance 1.0) but then V_us = 0.4-0.8; the best
   joint point has V_us = 0.38. The 'hierarchical 10 / anarchic 5bar' pattern does not arise from modulus anisotropy.
"""

import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11915_su5_matrix_fluxes_on_t4 as F  # noqa: E402
import w33_pass11918_hypercharge_wilson_scan as S  # noqa: E402

OUT = ROOT / "data" / "w33_pass11922_neutrino_qutrit_complementarity.json"
FROZEN = ROOT / "data" / "w33_pass11922_complementarity_scan_frozen.json"
A2, A2m = [[2, 1], [1, 2]], [[2, -1], [-1, 2]]
J = np.array([[0, 1], [1, 0]])
CKM = np.array([[0.974, 0.2245, 0.0038], [0.221, 0.973, 0.041], [0.0086, 0.040, 0.999]])
PMNS = np.array([[0.82, 0.55, 0.15], [0.37, 0.58, 0.72], [0.42, 0.60, 0.68]])
PERMS = [np.eye(3)[list(p)] for p in itertools.permutations(range(3))]


def _ns(K=6):
    return np.array([(a, b) for a in range(-K, K + 1) for b in range(-K, K + 1)])


def radiative(Ys):
    M = np.array([Y.ravel() for Y in Ys])
    w, V = np.linalg.eigh(M.conj() @ M.T)
    return np.tensordot(V[:, -1], np.array(Ys), 1)


def best(A, target):
    A = abs(A)[:, ::-1]
    bd, bM = np.inf, None
    for P in PERMS:
        M = P @ A
        d = np.sqrt(np.mean(np.log(np.maximum(M, 1e-12) / target) ** 2))
        if d < bd:
            bd, bM = d, M
    return bd, bM


def comp_sample(seed, n, only=None):
    saved = F.NS
    F.NS = _ns()
    try:
        rng = np.random.default_rng(seed)
        rows = []
        for it in range(n):
            t, beta = rng.uniform(0.6, 3.0), rng.uniform(-0.85, 0.85)
            Om = 1j * t * (np.eye(2) + beta * J) + rng.uniform(-0.5, 0.5) * np.eye(2) + rng.uniform(-0.5, 0.5) * J

            def lat(v):
                return v[:2] + Om @ v[2:]

            P = S.positions(A2, A2m, lat(rng.random(4)), lat(rng.random(4)), lat(rng.random(4) - 0.5))
            if only is not None and it not in only:
                continue
            T = F.T4(Om, 12)
            Yd = radiative(F.yukawas(T, A2, A2m, P["Q"], P["d"]))
            Ye = radiative(F.yukawas(T, A2, A2m, P["e"], P["L"]))
            Ud, sd, _ = np.linalg.svd(Yd)
            _, se, Veh = np.linalg.svd(Ye)
            dc, Mc = best(Ud, CKM)
            dp, Mp = best(Veh.conj().T, PMNS)
            rows.append([it, t, beta, dc, dp, Mc[0, 1], Mc[1, 2], Mc[0, 2], *Mp.ravel(), sd[2] / sd[1], sd[1] / sd[0],
                         se[2] / se[1], se[1] / se[0]])
        return np.array(rows)
    finally:
        F.NS = saved


def mirror_checks():
    saved = F.NS
    F.NS = _ns()
    rng = np.random.default_rng(11922)
    forms = [[[a, b], [b, c]] for a in range(1, 5) for c in range(1, 5) for b in range(-3, 4) if a * c - b * b == 3]
    mono, top3, deg, sym, gsame = True, True, 0.0, 0.0, 0.0
    try:
        for N in forms:
            Na = np.array(N, float)
            Om = 1j * (1.3 * np.eye(2) + 0.1 * Na) + 0.2 * np.eye(2)
            T = F.T4(Om, 16)  # G = 10 leaves grid residuals ~3e-6 at flux 2N up to 8; G = 14, 18 give 5e-12, 2e-15
            zL = rng.random(2) + Om @ rng.random(2)
            Ys = np.array(F.yukawas(T, N, N, zL, zL))
            for Y in Ys:
                A = abs(Y) > 1e-9 * abs(Y).max()
                mono &= bool((A.sum(0) == 1).all() and (A.sum(1) == 1).all())
                s = np.linalg.svd(Y, compute_uv=False)
                deg = max(deg, min(abs(s[0] - s[1]), abs(s[1] - s[2])) / s[0])
                sym = max(sym, float(np.max(abs(Y - Y.T)) / abs(Y).max()))
            M = Ys.reshape(len(Ys), 9)
            w = np.linalg.eigvalsh(M.conj() @ M.T)[::-1]
            top3 &= bool(abs(w[2] / w[0] - 1) < 1e-9 and w[3] / w[0] < 0.99)
            C = M.conj() @ M.T
            supp = [tuple(np.flatnonzero(abs(Y.ravel()) > 1e-9 * abs(Y).max())) for Y in Ys]
            cls = {}
            for k, s_ in enumerate(supp):
                cls.setdefault(s_, []).append(k)
            g = {}
            for ks in cls.values():
                ww, vv = np.linalg.eigh(C[np.ix_(ks, ks)])
                Mk = np.tensordot(vv[:, -1], Ys[ks], 1)
                nz = np.argwhere(abs(Mk) > 1e-9 * abs(Mk).max())
                k = {int((a + b) % 3) for a, b in nz}
                if len(k) != 1:
                    gsame = np.inf
                    continue
                g[k.pop()] = {int((a - b) % 3): Mk[a, b] for a, b in nz}
            if sorted(g) == [0, 1, 2]:
                for k in (1, 2):
                    r = np.array([g[k][d] / g[0][d] for d in range(3)])
                    gsame = max(gsame, float(np.ptp(abs(r)) / abs(r).mean() + np.ptp(np.angle(r / r[0]))))
                gsame = max(gsame, float(abs(abs(g[0][1]) - abs(g[0][2])) / abs(g[0][0])))
            else:
                gsame = np.inf
    finally:
        F.NS = saved
    return dict(forms=len(forms), monomial=mono, top_space_three=top3, max_degenerate_gap=deg, max_asymmetry=sym,
                h_form_and_gplus_eq_gminus_spread=gsame)


def main():
    mc = mirror_checks()
    fz = json.loads(FROZEN.read_text())
    rr = comp_sample(fz["check_seed"], fz["check_it"] + 1, only=[fz["check_it"]])
    repro = float(np.max(abs(rr[0] - np.array(fz["check_row"]))))
    res = dict(pass_id=11922, mirror=mc, complementarity=fz, reproduced_row_max_diff=repro)
    res["checks"] = {k: bool(v) for k, v in dict(
        weinberg_channel_monomial_all_forms=mc["monomial"],
        neutrino_higgs_pair_is_qutrit=mc["top_space_three"],
        single_class_degenerate_pair=mc["max_degenerate_gap"] < 1e-12,
        majorana_matrix_symmetric=mc["max_asymmetry"] < 1e-12,
        m_nu_equals_h_bplusb_g_symmetric=mc["h_form_and_gplus_eq_gminus_spread"] < 1e-8,
        no_complementarity=fz["corr_ckm_pmns_dist"] > 0.2,
        best_joint_vus_too_large=fz["best_joint"]["Vus"] > 0.3,
        scan_reproduces=repro < 1e-10,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
