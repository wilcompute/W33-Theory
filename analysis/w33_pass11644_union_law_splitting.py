"""Pass 11644: the 'if' half of the union law -- a per-solution theorem, k = 0 off the isotropic locus, and a 3-adic
splitting criterion that PROVES the union law class by class without enumerating frames.

Setting (Passes 11350, 11537): U = W(a) V_M T1; a solution (Q, k) of (S) gives the anti-symplectic A = Q J with
A M A^-1 = s^k M^-1 and A z1 = -z1.  K = ker(M - I), K0 = K cap z1^perp, N_Q = (I - A^-1) K0.

THEOREM 1 (the frames of ONE solution, every n).  r_Q = 0 and, with pairing omega(u, a):
    frames(Q, k) = N_Q^perp  cap  { a : omega(v_Q, a) = c_Q },
  where   case 1 (z1 not in Im(M - I)):  pick w1 in K with c1 = omega(w1, z1) != 0;  x_Q = w1 - k c1 z1;
          case 2 (z1 in Im(M - I)):      pick w0 with (I - M) w0 = z1, c0 = omega(w0, z1);  x_Q = w0 + (1 - k c0) z1;
  v_Q = (I - A^-1) x_Q, and c_Q = omega(w, base) (w = w1 or w0; base the right-hand side of (F) at a = 0).
  PROOF: (F) is solvable iff its right-hand side pairs to zero with K' = {w : (I - M) w in span z1}; K' = K0 + span(w1)
  or K0 + span(w0) (since K^perp = Im(M - I)); the K0 part gives N_Q^perp (Pass 11537), and the extra vector gives the
  stated affine condition (s^k w = w + k omega(w, z1) z1, A^-1 z1 = -z1, M w0 = w0 - z1).  Checked against the decider on
  every (Q, k) below.
THEOREM 2 (k = 0 off the isotropic locus, every n).  If the M-cyclic span of z1 is not totally isotropic, every solution
  has k = 0.  PROOF: A conjugates M to s^k M^-1 = (I + k z1 e_x1^T) M^-1, so both have the characteristic polynomial of M,
  which is that of M^-1.  By the matrix determinant lemma, the difference is k * sum_j omega(M^-j z1, z1) t^-j (times the
  characteristic polynomial); k != 0 forces omega(M^j z1, z1) = 0 for all j, i.e. an isotropic cyclic span.
THEOREM 3 (splitting, every n).  For k = 0: c_Q = 0 and A preserves K0 and Kt = K0 + span(x_Q), acting trivially on
  Kt/K0.  Then frames(Q, 0) = N_Q^perp  iff  (A - I) x_Q lies in (A - I) K0  iff  A has a fixed vector in Kt outside K0.
  This HOLDS whenever the order m of A on Kt is prime to 3 (in particular when A^2 = I): sum_{j<m} A^j x_Q is fixed and
  equals m x_Q mod K0.
COROLLARY (union law, class by class).  If every solution of (S) for M has k = 0 and 3 not dividing ord(A_Q | Kt), then the
  reversible frames are exactly the union of the N_Q^perp: Pass 11537's law is PROVED for that class by linear algebra,
  with no frame enumeration.  (Solutions with k != 0 in case 2 and c0 = 0 have v_Q in N_Q and c_Q = k != 0: they reverse
  no frame at all.)
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11350_linear_decider as L  # noqa: E402
import w33_pass11352_three_qutrit_geometry as GEO  # noqa: E402
import w33_pass11498_magic_axis_law_all_n as T  # noqa: E402

OUT = ROOT / "data" / "w33_pass11644_union_law_splitting.json"
R = L.R


def null(A):
    A = np.asarray(A) % 3
    s = L.solve_affine(A, np.zeros(A.shape[0], np.int64))
    return [np.asarray(b) % 3 for b in s[1]] if s and s[1] else []


def in_span(B, x):
    if not len(B):
        return not (np.asarray(x) % 3).any()
    return L.solve_affine(np.array(B).T % 3, np.asarray(x) % 3) is not None


def analyse(D, M, cap=3 ** 8, check_frames=True):
    """per-class certificate: list of per-solution records, or None if a solution space exceeds cap"""
    N2 = D.N2
    z = D.z1
    Om = D.wl.Om
    I = np.eye(N2, dtype=np.int64)
    lab = D.wl.labels.astype(np.int64)

    def om(u, v):
        return int(u @ Om @ v) % 3
    M = np.asarray(M) % 3
    Minv = R._inv_mod3(M) % 3
    K = null((M - I) % 3)
    K0 = null(np.concatenate([(M - I) % 3, (z @ Om)[None, :] % 3]))
    w1 = next((w for w in K if om(w, z)), None)
    case = 1 if w1 is not None else 2
    w0 = None if case == 1 else L.solve_affine((I - M) % 3, z)[0]
    cyc = [z]
    for _ in range(N2):
        cyc.append((M @ cyc[-1]) % 3)
    iso = all(om(cyc[0], c) == 0 for c in cyc)
    e1 = np.zeros(N2, np.int64)
    e1[0] = 1
    recs = []
    for k in range(3):
        sols = T.solutions(D, M, k, cap)
        if sols is None:
            return None, dict(iso=iso, case=case)
        for Q in sols:
            A = (Q @ D.J) % 3
            Ai = R._inv_mod3(A) % 3
            rQ = D.r_frame(Q) if check_frames else np.zeros(N2, np.int64)
            t_k = (D.gframe(e1 * k) - e1 * k) % 3
            base = ((-t_k - D.sinv_pow[k] @ rQ) % 3 - ((I - Minv) % 3) @ (k * e1)) % 3
            if case == 1:
                wx, c = w1, om(w1, z)
                x = (w1 - k * c * z) % 3
            else:
                wx, c = w0, om(w0, z)
                x = (w0 + (1 - k * c) * z) % 3
            vQ = (x - Ai @ x) % 3
            cQ = om(wx, base)
            NQ = [(w - Ai @ w) % 3 for w in K0]
            member = in_span(NQ, vQ)
            rec = dict(k=k, r_zero=not rQ.any(), member=member, c_zero=cQ == 0)
            if k == 0:
                Kt = np.array(list(K0) + [x]).T % 3
                cur = I.copy()
                order = None
                for o in range(1, 400):
                    cur = (A @ cur) % 3
                    if not ((cur @ Kt - Kt) % 3).any():
                        order = o
                        break
                rec["order_on_Kt"] = order
                rec["split_by_averaging"] = order is not None and order % 3 != 0
                rec["involution"] = not (((A @ A) % 3 - I) % 3).any()
            if check_frames:
                pred = np.ones(len(lab), bool)
                for v in NQ:
                    pred &= (lab @ (Om.T @ v)) % 3 == 0
                NQperp = pred.copy()
                pred &= (lab @ (Om.T @ vQ)) % 3 == cQ
                sQ = (D.sinv_pow[k] @ Q) % 3
                Lm = (Minv + sQ @ D.J) % 3
                Y = ((I - Minv) % 3)[:, 1:]
                _, Nb = L.solve_affine(Y.T, np.zeros(N2 - 1, dtype=np.int64))
                act = (((np.array(Nb) @ ((base[None, :] - lab @ Lm.T) % 3).T) % 3 == 0).all(axis=0)
                       if Nb else np.ones(len(lab), bool))
                rec["theorem1_formula_matches_decider"] = bool((pred == act).all())
                rec["exact"] = bool((act == NQperp).all())
            recs.append(rec)
    return recs, dict(iso=iso, case=case)


def summarise(D, M, recs, info, st, mass, weight):
    cell = GEO.cell(np.asarray(M) % 3, D.z1, D.wl.Om)
    if recs is None:
        st[f"{cell}: solution space beyond cap"] += 1
        mass["beyond cap"] += weight
        return
    for r in recs:
        if r["k"] != 0:
            st["k != 0 solutions"] += 1
            st["k != 0 with ISOTROPIC cyclic span (Theorem 2)"] += info["iso"]
            st["k != 0 solutions reversing no frame (member and c != 0)"] += r["member"] and not r["c_zero"]
        else:
            st["k = 0 solutions"] += 1
            st["k = 0: c_Q = 0"] += r["c_zero"]
            st["k = 0: split by averaging (3 does not divide order)"] += r["split_by_averaging"]
            st["k = 0: involutive reverser"] += r["involution"]
            if "exact" in r:
                st["k = 0 and 3 does not divide order: exact (Theorem 3)"] += r["split_by_averaging"] and r["exact"]
                st["k = 0 and 3 | order: exact anyway"] += (not r["split_by_averaging"]) and r["exact"]
                st["k = 0 and 3 | order: NOT exact"] += (not r["split_by_averaging"]) and not r["exact"]
        if "theorem1_formula_matches_decider" in r:
            st["Theorem 1 formula = decider"] += r["theorem1_formula_matches_decider"]
            st["pairs checked against decider"] += 1
            st["r_Q = 0"] += r["r_zero"]                     # only meaningful when frames (and r_Q) are computed
    proved = len(recs) > 0 and all(r["k"] == 0 and r["split_by_averaging"] for r in recs)
    nosol = len(recs) == 0
    st[f"{cell}: union law PROVED by the criterion"] += proved
    st[f"{cell}: no solution (no reversible frame; Pass 11537 necessity)"] += nosol
    st[f"{cell}: criterion silent"] += not (proved or nosol)
    mass["proved"] += weight * proved
    mass["no solution"] += weight * nosol
    mass["silent"] += weight * (not (proved or nosol))
    mass["total"] += weight


def _job2(idx):
    import w33_pass11330_orbit_census as O
    D = L.Decider(2)
    Ms = np.array(O.all_symplectic(D.wl)[0]) % 3
    st, mass = Counter(), Counter()
    for i in idx:
        recs, info = analyse(D, Ms[i], cap=3 ** 8, check_frames=True)
        summarise(D, Ms[i], recs, info, st, mass, 1)
    return st, mass


def run_n2(nproc=6):
    from multiprocessing import Pool
    idx = list(range(51840))
    chunks = [idx[i::60] for i in range(60)]
    st, mass = Counter(), Counter()
    with Pool(nproc) as pool:
        for s, m in pool.imap_unordered(_job2, chunks):
            st.update(s)
            mass.update(m)
    return dict(counts=dict(st), classes=dict(mass))


def _job3(items):
    D = L.Decider(3)
    st, mass = Counter(), Counter()
    for M, size in items:
        recs, info = analyse(D, M, cap=3 ** 9, check_frames=False)
        summarise(D, M, recs, info, st, mass, size)
    return st, mass


def run_n3(nproc=6):
    import w33_pass11373_three_qutrit_exact_fraction as X
    from multiprocessing import Pool
    items = [(np.asarray(M) % 3, int(s)) for M, s in X.read_orbits(3)]
    chunks = [items[i::48] for i in range(48)]
    st, mass = Counter(), Counter()
    with Pool(nproc) as pool:
        for s, m in pool.imap_unordered(_job3, chunks):
            st.update(s)
            mass.update(m)
    tot = mass["total"]
    return dict(counts=dict(st), mass={k: str(Fraction(v, tot)) for k, v in mass.items()},
                mass_float={k: v / tot for k, v in mass.items()})


def main():
    stage = sys.argv[1] if len(sys.argv) > 1 else "n2"
    res = json.load(open(OUT)) if OUT.exists() else dict(pass_id=11644)
    out = run_n2() if stage == "n2" else run_n3()
    print(out, flush=True)
    res = json.load(open(OUT)) if OUT.exists() else dict(pass_id=11644)
    res[stage] = out
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
