"""Pass 11902: in all 104 A8 SO(16)xSO(16) Standard Models the up-sector degeneracy is independent of every Kahler
modulus at the renormalisable level.

Input: the orbifolder field dumps of Pass 11095 (WSL ~/orb/p1109x/a8/a8_sm_all_our_m0_v2.dump and
a8_sm_all_theirs.dump; 104 models). Run with the two dump paths to rescan; the per-model results are frozen in
data/w33_pass11902_census_frozen.json and the certificate is rebuilt from that file.

The quark doublets of the 104 models come in exactly two kinds:
  * 73 models: all three Q UNTWISTED (families = the three complex planes). Every renormalisable up coupling, for every
    up-type Higgs (219 rows), is the untwisted E8 cubic g eps_{ijk}, so the mass matrix is antisymmetric with singular
    values (1, 1, 0): top = charm and a massless up quark. The untwisted matter metric is (T + T^dagger)^{-1} for the
    full Hermitian Kahler matrix T, common to Q and u^c, so canonical normalisation acts by congruence A M A^T, which
    preserves antisymmetry: the (s, s, 0) spectrum holds for every Kahler modulus (checked for random T).
  * 31 models: the three Q at the three fixed points of one Wilson-line-free torus (twisted families). In every one the
    UP-sector triangles are single-pointed on both Wilson-line tori (top (0,0,0), light (1,0,0) on the family torus), so
    m_c = m_u for all nine Kahler moduli by theta evenness (Pass 11901). One model (56) has down-sector triangles that
    are not single-pointed on its Wilson-line tori ((0,1,1) and (1,1,1)): only there could the off-diagonal moduli split
    m_s from m_d, at the cost of a bottom suppressed on both Wilson-line tori.
So in this class no Kahler modulus, including the off-diagonal ones that carry W(3,3) (Passes 11897-11900), can produce
the up-quark hierarchy at the renormalisable level. The lever must be non-renormalisable, non-perturbative, or a
different class.
"""

import json
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.linalg import sqrtm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
OUT = ROOT / "data" / "w33_pass11902_a8_census_kahler_independent_degeneracy.json"
FROZEN = ROOT / "data" / "w33_pass11902_census_frozen.json"


def scan(ours, theirs):
    import w33_pass11097_fractional_fermion_masses as P97
    import w33_pass11098_yukawa_textures as Y
    import w33_so16_selection_rules as S
    US, TH = S.parse_ours(ours), S.parse_theirs(theirs)
    rng = np.random.default_rng(0)
    out = {}
    for m in sorted(US):
        us, th = US[m], TH[m]
        algs, hid, nu1 = P97.prepare(us, th)
        c, oc, ow, qcol = S.sm_data(th, us)
        qb = P97.conj(qcol, "A2")
        ferm = [f for f in us["fields"] if f["m"] == 2]
        scal = [f for f in us["fields"] if f["m"] == 6]

        def pick(L, col, w, Yv):
            return [f for f in L if f["col"] == col and f["w"] == w and f["Y"] == Yv]
        Q, U, D = pick(ferm, qcol, 2, F(1, 6)), pick(ferm, qb, 1, F(-2, 3)), pick(ferm, qb, 1, F(1, 3))
        Hu, Hd = pick(scal, "1", 2, F(1, 2)), pick(scal, "1", 2, F(-1, 2))
        untw = all(q["k"] == 0 and q["l"] == 0 for q in Q)
        tstar = [t for t in range(3) if len({S.classes(q["n"])[t] for q in Q}) == 3]
        rec = dict(label=us["label"], kind="untwisted" if untw else ("twisted_one_torus" if len(tstar) == 1 else "other"),
                   tstar=tstar)
        for name, A, B, HH in (("up", Q, U, Hu), ("down", Q, D, Hd)):
            rows = []
            for h in HH:
                M = np.zeros((len(A), len(B)), complex)
                pats, types = set(), set()
                for i, a in enumerate(A):
                    for j, b in enumerate(B):
                        if not Y.hidden_ok([a, b, h], hid, algs):
                            continue
                        vs = [S.charge_vector(x, True) for x in (a, b, h)]
                        if not P97.cubic_ok(vs, nu1):
                            continue
                        if all(x["k"] == 0 and x["l"] == 0 for x in (a, b, h)):
                            e = Y.eps(Y.plane(a), Y.plane(b), Y.plane(h))
                            if e == 0:
                                continue
                            M[i, j] = e
                            types.add("U")
                        else:
                            ca, cb, ch = S.classes(a["n"]), S.classes(b["n"]), S.classes(h["n"])
                            pats.add(tuple(int(not (ca[u] == cb[u] == ch[u])) for u in range(3)))
                            M[i, j] = rng.normal() + 1j * rng.normal()
                            types.add("T")
                if not types:
                    continue
                sv = np.linalg.svd(M, compute_uv=False)
                rows.append(dict(types="".join(sorted(types)), patterns=sorted(pats),
                                 sv=[round(float(x / sv[0]), 6) for x in sv[:3]]))
            rec[name] = rows
        out[str(m)] = rec
    FROZEN.write_text(json.dumps(out, indent=1))


def congruence_check(rng):
    """untwisted eps-Yukawa: singular values after Kahler normalisation A M A^T stay (s, s, 0)"""
    worst, ctrl = 0.0, []
    for _ in range(20):
        B = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
        P = B @ B.conj().T + 0.3 * np.eye(3)  # T + T^dagger for a random Hermitian Kahler matrix
        A = sqrtm(P)  # canonical fields: C = A C_hat, since the matter metric is P^{-1}
        h = rng.normal(size=3) + 1j * rng.normal(size=3)
        eps = np.zeros((3, 3, 3))
        for i, j, k, s in ((0, 1, 2, 1), (1, 2, 0, 1), (2, 0, 1, 1), (1, 0, 2, -1), (0, 2, 1, -1), (2, 1, 0, -1)):
            eps[i, j, k] = s
        M = np.einsum("ijk,k->ij", eps, h)
        sv = np.linalg.svd(A.T @ M @ A, compute_uv=False)
        worst = max(worst, abs(sv[0] - sv[1]) / sv[0], sv[2] / sv[0])
        Ms = M + np.diag(rng.normal(size=3))  # control: not antisymmetric -> no protected (s, s, 0)
        svc = np.linalg.svd(A.T @ Ms @ A, compute_uv=False)
        ctrl.append(min(abs(svc[0] - svc[1]) / svc[0], svc[2] / svc[0]))
    return float(worst), float(min(ctrl))


def main():
    d = json.loads(FROZEN.read_text())
    kinds = Counter(r["kind"] for r in d.values())
    untw_rows = [row for r in d.values() if r["kind"] == "untwisted" for row in r["up"]]
    untw_ok = all(row["types"] == "U" and row["sv"] == [1.0, 1.0, 0.0] for row in untw_rows)
    tw = {m: r for m, r in d.items() if r["kind"] == "twisted_one_torus"}
    up_single, down_escape = [], []
    for m, r in tw.items():
        t = r["tstar"][0]

        def single(rows):
            return all(not any(p[u] for u in range(3) if u != t) for row in rows for p in row["patterns"])
        if single(r["up"]):
            up_single.append(m)
        if not single(r["down"]):
            down_escape.append(m)
    cong, cong_ctrl = congruence_check(np.random.default_rng(11902))
    res = dict(pass_id=11902, models=len(d), kinds=dict(kinds), untwisted_up_rows=len(untw_rows),
               twisted_models_up_single_pointed=len(up_single), twisted_models=len(tw),
               down_escape_capable_models=down_escape, congruence_worst=cong,
               congruence_control_min=cong_ctrl)
    res["checks"] = {k: bool(v) for k, v in dict(
        all_104=len(d) == 104,
        two_kinds_73_31=kinds == {"untwisted": 73, "twisted_one_torus": 31},
        untwisted_top_equals_charm_all_rows=untw_ok and len(untw_rows) == 219,
        congruence_preserves_s_s_0=cong < 1e-10 and cong_ctrl > 1e-3,
        twisted_up_single_pointed_all=len(up_single) == len(tw) == 31,
        only_model_56_down_escape=down_escape == ["56"],
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    if len(sys.argv) > 2:
        scan(*sys.argv[1:3])
    main()
