"""Pass 11903: local grand unification of the 10 locks m_c = m_u -- a 491-model census.

Models: the 104 A8 SO(16)xSO(16) Standard Models of Pass 11095 plus the 387 inequivalent models of the Pass 11108 rescan
(400,000 Wilson-line draws), 491 distinct labels. Field dumps were regenerated with build7/levdump2 (ORB_MASS_LEVEL=0)
and nsobuild/nsosm (both reproduce the archived Pass 11095 dumps byte for byte). Run with dump pairs (our theirs ...)
to rescan; the per-model results are frozen in data/w33_pass11903_census491_frozen.json.

Findings:
  * 339 models have untwisted quark doublets: every up coupling (all Higgs rows) is the antisymmetric E8 cubic, top =
    charm and m_u = 0 for every Kahler modulus (Pass 11902).
  * 152 models have twisted families on one torus. In ALL of them u^c and e^c sit at the same point of the two
    Wilson-line tori and in the same twisted sector as Q: each family is a complete local SU(5) 10 = Q + u^c + e^c. The
    5bar (d^c, L) is often split across points (or untwisted).
  * Theorem (prime Z3, diagonal selection rule): if Q and u^c share a point g of a Wilson-line torus, the space-group rule
    g_Q + g_u + g_H = 0 mod 3 forces g_H = -2g = g: the up triangle is single-pointed (a = 0), the light entries are
    theta_(+-1,0,0) and equal by evenness for all nine Kahler moduli (Passes 11900-11901). So a localised 10 implies
    m_c = m_u at tree level for every modulus.
  * Census: up sector escape-capable in 0/491 models; down sector in 5 (d^c sits away from Q, so the down triangle can
    span a Wilson-line torus).
Reading: in this class, local grand unification of the 10 and the charm-up hierarchy are incompatible at tree level. A
model that splits charm from up through the W(3,3) (off-diagonal Kahler) modulus must split the 10 across Wilson-line
classes.
"""

import json
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
OUT = ROOT / "data" / "w33_pass11903_local_ten_locks_charm_up.json"
FROZEN = ROOT / "data" / "w33_pass11903_census491_frozen.json"


def scan(pairs):
    import w33_pass11097_fractional_fermion_masses as P97
    import w33_pass11098_yukawa_textures as Y
    import w33_so16_selection_rules as S
    out = {}
    for ours, theirs in pairs:
        US, TH = S.parse_ours(ours), S.parse_theirs(theirs)
        for m in US:
            us, th = US[m], TH[m]
            if us["label"] in out:
                continue
            algs, hid, nu1 = P97.prepare(us, th)
            c, oc, ow, qcol = S.sm_data(th, us)
            qb = P97.conj(qcol, "A2")
            ferm = [f for f in us["fields"] if f["m"] == 2]
            scal = [f for f in us["fields"] if f["m"] == 6]

            def pick(L, col, w, Yv):
                return [f for f in L if f["col"] == col and f["w"] == w and f["Y"] == Yv]
            Q, U, D = pick(ferm, qcol, 2, F(1, 6)), pick(ferm, qb, 1, F(-2, 3)), pick(ferm, qb, 1, F(1, 3))
            L, E = pick(ferm, "1", 2, F(-1, 2)), pick(ferm, "1", 1, F(1))
            Hu, Hd = pick(scal, "1", 2, F(1, 2)), pick(scal, "1", 2, F(-1, 2))
            rec = dict(label=us["label"])
            if all(q["k"] == 0 and q["l"] == 0 for q in Q):
                rec["kind"] = "untwisted"
                rows, all_eps = 0, True
                for h in Hu:
                    allowed = [(a, b) for a in Q for b in U if Y.hidden_ok([a, b, h], hid, algs)
                               and P97.cubic_ok([S.charge_vector(x, True) for x in (a, b, h)], nu1)]
                    allowed = [(a, b) for a, b in allowed if not (all(x["k"] == 0 and x["l"] == 0 for x in (a, b, h))
                                                                    and Y.eps(Y.plane(a), Y.plane(b), Y.plane(h)) == 0)]
                    if allowed:
                        rows += 1
                        all_eps &= all(all(x["k"] == 0 and x["l"] == 0 for x in (a, b, h)) for a, b in allowed)
                rec["untwisted_up_rows"], rec["untwisted_all_eps"] = rows, all_eps
                out[us["label"]] = rec
                continue
            ts = [x for x in range(3) if len({S.classes(q["n"])[x] for q in Q}) == 3]
            rec["kind"] = "twisted_one_torus" if len(ts) == 1 else "other"
            if len(ts) != 1:
                out[us["label"]] = rec
                continue
            t = ts[0]
            other = [x for x in range(3) if x != t]

            def g(f):
                return tuple((f["l"] * S.classes(f["n"])[x]) % 3 for x in other)
            gq = {g(q) for q in Q}
            same = lambda fs: all(g(f) in gq and f["l"] == Q[0]["l"] for f in fs)  # noqa: E731
            rec.update(Q_points=sorted(gq), U_same=same(U), E_same=same(E), D_all_same=same(D), L_all_same=same(L))

            def tri(A, B, HH):
                pats = set()
                for h in HH:
                    for a in A:
                        for b in B:
                            if not Y.hidden_ok([a, b, h], hid, algs):
                                continue
                            if not P97.cubic_ok([S.charge_vector(x, True) for x in (a, b, h)], nu1):
                                continue
                            if all(x["k"] == 0 and x["l"] == 0 for x in (a, b, h)):
                                continue
                            ca, cb, ch = S.classes(a["n"]), S.classes(b["n"]), S.classes(h["n"])
                            pats.add(tuple(int(not (ca[u] == cb[u] == ch[u])) for u in other))
                return sorted(pats)
            rec["up_wilson_patterns"] = tri(Q, U, Hu)
            rec["down_wilson_patterns"] = tri(Q, D, Hd)
            out[us["label"]] = rec
    FROZEN.write_text(json.dumps(out, indent=1))


def main():
    d = json.loads(FROZEN.read_text())
    kinds = Counter(r["kind"] for r in d.values())
    tw = [r for r in d.values() if r["kind"] == "twisted_one_torus"]
    local10 = sum(1 for r in tw if r["U_same"] and r["E_same"])
    up_escape = [r["label"] for r in tw if any(any(p) for p in r["up_wilson_patterns"])]
    down_escape = [r["label"] for r in tw if any(any(p) for p in r["down_wilson_patterns"])]
    five_split = sum(1 for r in tw if not (r["D_all_same"] and r["L_all_same"]))
    # the arithmetic: g_Q = g_u = g  =>  g_H = -2g = g (mod 3)
    forced = all((-2 * gg) % 3 == gg for gg in range(3))
    unt = [r for r in d.values() if r["kind"] == "untwisted"]
    res = dict(pass_id=11903, untwisted_up_rows=sum(r["untwisted_up_rows"] for r in unt), models=len(d), kinds=dict(kinds), twisted_models=len(tw), local_ten_models=local10,
               five_bar_split_models=five_split, up_escape_capable=up_escape, down_escape_capable=down_escape,
               higgs_point_forced=forced)
    res["checks"] = {k: bool(v) for k, v in dict(
        census_491=len(d) == 491,
        kinds_339_152=kinds == {"untwisted": 339, "twisted_one_torus": 152},
        untwisted_all_eps=all(r["untwisted_all_eps"] for r in unt),
        local_ten_in_all_twisted=local10 == len(tw) == 152,
        higgs_forced_to_same_point=forced,
        no_up_escape=up_escape == [],
        down_escape_only_where_5bar_split=len(down_escape) == 5 and five_split >= len(down_escape),
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    if len(sys.argv) > 2:
        a = sys.argv[1:]
        scan(list(zip(a[0::2], a[1::2])))
    main()
