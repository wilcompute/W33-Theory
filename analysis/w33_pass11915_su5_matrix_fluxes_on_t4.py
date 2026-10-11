"""Pass 11915: SU(5)-structured det-3 matrix fluxes on T4 -- what the two W(3,3) theta systems do for flavour.

Idea selection (a long list was ranked; this pursues the top entry). Three generations on magnetized T4 need a flux
matrix N with det N = 3. Positive binary forms of determinant 3 fall into exactly TWO classes: the A2 / Eisenstein form
[[2,1],[1,2]] and the rectangular form x^2 + 3y^2 = diag(1,3) -- the two theta systems of this corpus (Eisenstein /
Hermitian, Pass 11897; level-3 sqrt3 Z, Pass 11869). In SU(5), Q, u^c, e^c sit in the 10 (flux N10) and d^c, L in the
5bar (flux N5): the up Yukawa is 10.10 (Higgs flux 2 N10), the down and lepton Yukawas are both 10.5bar (Higgs flux
N10 + N5). So I_down = I_lepton is automatic (data: 1.91e-5 vs 1.64e-5, Pass 11910), and the up/down difference becomes
a statement about the two classes.

Construction (verified here): zero modes psi^{j,N}(z) ~ exp(i pi (Nz).(Im Omega)^{-1}.Im z) theta[j,0](Nz, N Omega),
j in N^{-1} Z^2 / Z^2, on T4 with Omega = i t 1 (both classes are (1,1) for scalar Omega); |psi|^2 periodic (1e-14),
det N orthonormal modes; Yukawas as direct 4D overlap integrals.

Results:
  1. Gaussian slopes are QUANTISED: ln I = s t + c with s/pi = -4/3 (rect x rect), -8/3 or -2/3 (A2 x A2), and for
     A2 x (rect class) -2, -1 or -4 depending on the relative orientation (all twelve det-3 forms with entries <= 4,
     frozen scan). The attainable up/down log-ratios are therefore {1/3, 2/3, 1, 4/3, 2, 8/3, ...}; the observed
     1.605 +- 0.03 is not among them (nearest 4/3), so with scalar Omega the SU(5) det-3 fluxes cannot produce the
     up/down ratio -- a non-scalar Omega (the entangling modulus) is required.
  2. Class selection broken geometrically: the up Higgs lattice (det 2N10 = 12) keeps the Z3 one-entry-per-row
     selection, but the down Higgs lattice (det(N10 + N5) = 14, coprime to 3) does not -- the down Yukawas are full 3x3
     matrices, so the CKM is nonzero without any cross-class Higgs admixture (removing Pass 11914's obstruction in
     principle).
  3. But with generic Wilson lines (40 random samples, t = 1.8, A2 / rect) the CKM is mostly tiny (median V_us 0.011,
     V_cb 1e-4) or permutation-misordered, with no CKM-like hierarchical pattern; the down masses are realistic-ish
     (median m_s/m_b 0.010, m_d/m_s 0.12) and the up light pair under-split (median m_u/m_c 0.55).
  4. Side result (idea ranked fifth): a within-class Higgs admixture (allowed radiatively) moves the Gaussian invariant
     strongly (eps = 0.01 -> x8), so the up/down ratio could come from the Higgs profile, at the price of a free
     parameter.
"""

import itertools
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11915_su5_matrix_fluxes_on_t4.json"
SLOPES = ROOT / "data" / "w33_pass11915_slope_scan_frozen.json"
CKMS = ROOT / "data" / "w33_pass11915_ckm_wilson_sample_frozen.json"
NS = np.array([(a, b) for a in range(-4, 5) for b in range(-4, 5)])
A2, RE = [[2, 1], [1, 2]], [[1, 0], [0, 3]]


def chars(N):
    N = np.array(N)
    Ni = np.linalg.inv(N)
    d = int(round(abs(np.linalg.det(N))))
    seen = []
    for m in itertools.product(range(d), repeat=2):
        j = (Ni @ np.array(m)) % 1.0
        if not any(np.allclose((j - s + 0.5) % 1 - 0.5, 0, atol=1e-9) for s in seen):
            seen.append(j)
    return seen


def psi_at(z, j, N, Om):
    N = np.array(N)
    Nz = z @ N.T
    Pi = N @ Om
    pref = np.exp(1j * np.pi * np.einsum("pi,ij,pj->p", Nz, np.linalg.inv(Om.imag), z.imag))
    return pref * sum(np.exp(1j * np.pi * ((n + j) @ Pi @ (n + j)) + 2j * np.pi * (Nz @ (n + j))) for n in NS)


class T4:
    def __init__(self, Om, G):
        self.Om = np.array(Om)
        xs = (np.arange(G) + 0.5) / G
        X = np.array(np.meshgrid(xs, xs, xs, xs, indexing="ij")).reshape(4, -1).T
        self.z = X[:, :2] + X[:, 2:] @ self.Om.T

    def psi(self, j, N, zeta=np.zeros(2)):
        p = psi_at(self.z + zeta, j, N, self.Om)
        return p / np.sqrt(np.mean(abs(p) ** 2))


def yukawas(T, NQ, NR, zQ=np.zeros(2), zR=np.zeros(2)):
    NQ, NR = np.array(NQ), np.array(NR)
    NH = NQ + NR
    zH = np.linalg.solve(NH, NQ @ zQ + NR @ zR)
    Q = [T.psi(j, NQ, zQ) for j in chars(NQ)]
    R = [T.psi(j, NR, zR) for j in chars(NR)]
    out = []
    for jh in chars(NH):
        H = np.conj(T.psi(jh, NH, zH))
        out.append(np.array([[np.mean(q * r * H) for r in R] for q in Q]))
    return out


def lnI(Y):
    s = np.sort(np.linalg.svd(Y, compute_uv=False))
    return np.log(s[0] * s[1] / s[2] ** 2) if s[0] > 1e-14 * s[2] else None


def main():
    rng = np.random.default_rng(11915)
    Om = 2.5j * np.eye(2)
    per = []
    for N in (A2, RE):
        j = chars(N)[1]
        x, y = rng.random((5, 2)), rng.random((5, 2))
        z = x + y @ Om.T
        base = abs(psi_at(z, j, N, Om)) ** 2
        for e in np.eye(2):
            per.append(float(np.max(abs(abs(psi_at(z + e, j, N, Om)) ** 2 - base) / base)))
            per.append(float(np.max(abs(abs(psi_at(z + Om @ e, j, N, Om)) ** 2 - base) / base)))
    T = T4(Om, 18)
    gram = max(float(np.max(abs(np.array([[np.mean(np.conj(a) * b) for b in P] for a in P]) - np.eye(3))))
               for P in ([T.psi(j, N) for j in chars(N)] for N in (A2, RE)))
    counts = {str(N): len(chars(N)) for N in (A2, RE, [[4, 2], [2, 4]], [[3, 1], [1, 5]])}
    # key slopes recomputed (t = 2.5, 3.5)
    Ts = {t: T4(t * 1j * np.eye(2), 20) for t in (2.5, 3.5)}

    def slopes(NQ, NR):
        vals = {}
        for t, Tt in Ts.items():
            for k, Y in enumerate(yukawas(Tt, NQ, NR)):
                v = lnI(Y)
                if v is not None:
                    vals.setdefault(k, {})[t] = v
        return sorted(set(round((v[3.5] - v[2.5]) / np.pi, 2) for v in vals.values() if len(v) == 2))
    key = {"rect x rect": slopes(RE, RE), "A2 x A2": slopes(A2, A2), "A2 x rect": slopes(A2, RE)}
    # class selection: patterns at t = 2.5, zero Wilson lines
    up = yukawas(Ts[2.5], A2, A2)
    dn = yukawas(Ts[2.5], A2, RE)
    one_per_row_up = all(int(np.sum(abs(Y) > 1e-10 * abs(Y).max())) == 3 for Y in up if abs(Y).max() > 0)
    full_down = sum(int(np.sum(abs(Y) > 1e-10 * abs(Y).max())) > 3 for Y in dn)
    frozen_slopes = json.loads(SLOPES.read_text())
    attainable = sorted({round(-u / -d, 3) for v in frozen_slopes.values() for u in v["self"]
                         for w in frozen_slopes.values() for d in w["with_A2"] if d})
    ck = np.array(json.loads(CKMS.read_text()))
    med = np.median(ck, axis=0)
    res = dict(pass_id=11915, periodicity_max=max(per), gram_offdiag_max=gram, mode_counts=counts, key_slopes_over_pi=key,
               attainable_up_over_down_ratios=attainable, observed_ratio=1.605, up_one_entry_per_row=one_per_row_up,
               down_full_matrices=full_down, ckm_sample_medians=dict(mc_mt=med[0], mu_mc=med[1], ms_mb=med[2],
                                                                    md_ms=med[3], Vus=med[4], Vcb=med[5], Vub=med[6]))
    res["checks"] = {k: bool(v) for k, v in dict(
        zero_modes_periodic=max(per) < 1e-10,
        zero_modes_orthonormal=gram < 1e-8,
        mode_counts_det=counts == {str(A2): 3, str(RE): 3, "[[4, 2], [2, 4]]": 12, "[[3, 1], [1, 5]]": 14},
        slopes_quantised=key["rect x rect"] == [-1.33] and -2.67 in key["A2 x A2"] and -2.0 in key["A2 x rect"],
        observed_ratio_not_attainable=all(abs(r - 1.605) > 0.1 for r in attainable),
        up_keeps_class_selection=one_per_row_up,
        down_breaks_class_selection=full_down > 0,
        generic_wilson_ckm_too_small=med[4] < 0.05 and med[5] < 0.01,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(res, indent=1, default=float))


if __name__ == "__main__":
    main()
