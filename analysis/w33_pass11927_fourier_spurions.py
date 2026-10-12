"""Pass 11927: background Fourier modes of the torus are two-qutrit Paulis -- the local-adjoint flavour spurions.

Setting: magnetized SU(5) on T4 with a det-3 dual pair (N10, N5 = 3 N10^{-1}); the 10 is flavour qutrit 1 and the 5bar
flavour qutrit 2, and A[3] = K(L10) + K(L5) is the W(3,3) factorisation chosen by the flux (Pass 11921). The parallel
packet 34e149d79 found that CKM and PMNS (the two marginal Schmidt bases of one theta state, Pass 11922) are moved
independently only by local adjoint spurions (8,1) + (1,8), and left their origin open.

A background perturbation of the compactification (metric, B-field or flux non-uniformity) is a sum of plane waves
e^{2 pi i (p.x + q.y)} with (p, q) in Z^4. Projected on the zero modes of each matter bundle:
1. every plane wave acts as a single qutrit Weyl (Pauli) operator times a form factor (checked: all classifiable modes
   with |p_i|, |q_i| <= 2, for A2 and for (1,1,4));
2. wavevectors with p, q in N5 Z^2 act as a NON-identity Pauli on the 10 and as a scalar on the 5bar -- a pure (8,1);
   wavevectors in N10 Z^2 act as a scalar on the 10 and a Pauli on the 5bar -- a pure (1,8); all other wavevectors act
   as a Pauli on both, a coupled (8,8). All 8 non-identity Paulis occur in each pure class;
3. the Pauli label is a function of the wavevector mod 3, additive in the wavevector (a homomorphism Z^4 -> F3^2 x F3^2
   with kernel 3 Z^4), so the Fourier lattice mod 3 IS the two-qutrit Pauli space W(3,3), split by the same flux
   factorisation;
4. the form factor is Gaussian in the wavevector (log |c| linear in k^T M k); modes whose form factor falls below 1e-8 of
   the zero mode (down to 1e-10, residuals at the 1e-17 machine floor) are counted as suppressed, not classified.
Reading: the (8,1) + (1,8) spurions are exactly the background Fourier modes whose wavevector lies in one factor plane
of the flux factorisation; generic background modes (and the scalar modulus anisotropy of Pass 11922) are (8,8) and
move CKM and PMNS together. This names the geometric object; its source (a non-flat T4, a blow-up or flux
non-uniformity with those Fourier modes) is not derived here.
"""

import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11915_su5_matrix_fluxes_on_t4 as F  # noqa: E402

OUT = ROOT / "data" / "w33_pass11927_fourier_spurions.json"
W = np.exp(2j * np.pi / 3)
XP = np.roll(np.eye(3), 1, axis=0)
ZP = np.diag([1, W, W * W])
PAULI = {(a, b): np.linalg.matrix_power(XP, a) @ np.linalg.matrix_power(ZP, b) for a in range(3) for b in range(3)}


def which_pauli(M):
    n = np.linalg.norm(M)
    for k, P in PAULI.items():
        c = np.trace(P.conj().T @ M) / 3
        if np.linalg.norm(M - c * P) < 1e-7 * n:
            return k, abs(c)
    return None, None


def inlat(N, v):
    return all(abs(t - round(t)) < 1e-9 for t in np.linalg.solve(np.array(N, float), np.array(v, float)))


def analyse(N10, G=20, R=2):
    N5 = np.round(3 * np.linalg.inv(N10)).astype(int).tolist()
    Om = 1j * (1.1 * np.eye(2) + 0.15 * np.array(N10, float)) + 0.1 * np.eye(2)
    T = F.T4(Om, G)
    xs = (np.arange(G) + 0.5) / G
    Xg = np.array(np.meshgrid(xs, xs, xs, xs, indexing="ij")).reshape(4, -1).T
    m10 = np.array([T.psi(j, N10) for j in F.chars(N10)])
    m5 = np.array([T.psi(j, N5) for j in F.chars(N5)])
    ref = float(np.linalg.norm(np.array([[np.mean(np.conj(a) * b) for b in m10] for a in m10])))

    def K(modes, k):
        ph = np.exp(2j * np.pi * (Xg @ np.array(k)))
        return np.array([[np.mean(np.conj(a) * b * ph) for b in modes] for a in modes])

    rows, small_unclassified, big_unclassified = [], 0, 0
    for k in itertools.product(range(-R, R + 1), repeat=4):
        if not any(k):
            continue
        A, B = K(m10, k), K(m5, k)
        if min(np.linalg.norm(A), np.linalg.norm(B)) < 1e-8 * ref:   # Gaussian-suppressed below the grid floor
            small_unclassified += 1
            continue
        (pa, ca), (pb, cb) = which_pauli(A), which_pauli(B)
        if pa is None or pb is None:
            big_unclassified += 1
            continue
        cls = "N5" if inlat(N5, k[:2]) and inlat(N5, k[2:]) else ("N10" if inlat(N10, k[:2]) and inlat(N10, k[2:]) else "other")
        rows.append(dict(k=list(k), cls=cls, p10=list(pa), p5=list(pb), c10=float(ca), c5=float(cb)))
    return rows, small_unclassified, big_unclassified, ref


def main():
    out = {}
    checks = {}
    for name, N10 in (("A2", [[2, 1], [1, 2]]), ("114", [[1, 1], [1, 4]])):
        rows, small, big, ref = analyse(N10)
        by = lambda c: [r for r in rows if r["cls"] == c]
        pure81 = all(r["p5"] == [0, 0] and r["p10"] != [0, 0] for r in by("N5"))
        pure18 = all(r["p10"] == [0, 0] and r["p5"] != [0, 0] for r in by("N10"))
        mixed = all(r["p10"] != [0, 0] and r["p5"] != [0, 0] for r in by("other"))
        all8_10 = len({tuple(r["p10"]) for r in by("N5")}) == 8
        all8_5 = len({tuple(r["p5"]) for r in by("N10")}) == 8
        # label depends only on k mod 3 and is additive
        lab = {}
        consistent = True
        for r in rows:
            km = tuple(np.array(r["k"]) % 3)
            v = (tuple(r["p10"]), tuple(r["p5"]))
            if km in lab and lab[km] != v:
                consistent = False
            lab[km] = v
        additive, tested = True, 0
        keys = list(lab)
        for a, b in itertools.product(keys[:40], keys[:40]):
            c = tuple((np.array(a) + np.array(b)) % 3)
            if c in lab and any(c):
                tested += 1
                s10 = tuple((np.array(lab[a][0]) + np.array(lab[b][0])) % 3)
                s5 = tuple((np.array(lab[a][1]) + np.array(lab[b][1])) % 3)
                additive &= (s10, s5) == lab[c]
        # Gaussian form factor: log c10 against a quadratic form in k (least squares fit over the 10 classes)
        kk = np.array([r["k"] for r in rows], float)
        y = np.log(np.array([r["c10"] for r in rows]))
        Q = np.array([[a * b for a, b in itertools.combinations_with_replacement(v, 2)] for v in kk])
        A = np.c_[Q, np.ones(len(kk))]
        coef, res, *_ = np.linalg.lstsq(A, y, rcond=None)
        r2 = 1 - np.sum((A @ coef - y) ** 2) / np.sum((y - y.mean()) ** 2)
        out[name] = dict(modes=len(rows), counts={c: len(by(c)) for c in ("N5", "N10", "other")},
                         unclassified_small=small, unclassified_large=big, residue_classes=len(lab),
                         label_consistent_mod3=consistent, additive_pairs_tested=tested, additive=additive,
                         gaussian_formfactor_r2=float(r2))
        checks.update({f"{name}_{k}": v for k, v in dict(
            pure_81_from_N5=pure81, pure_18_from_N10=pure18, generic_modes_are_88=mixed,
            all_8_paulis_each=all8_10 and all8_5, label_is_function_of_k_mod3=consistent,
            label_additive=additive and tested > 50, unclassified_only_suppressed=big == 0,
            formfactor_gaussian=r2 > 0.999).items()})
    res = dict(pass_id=11927, results=out, checks={k: bool(v) for k, v in checks.items()})
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
