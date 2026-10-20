"""Passes 12102-12105 (Claude track; 12091-12100). One producer, four parts.

12102 -- PRIOR ART identified: the event-fibre families inherit the corpus's 11271 rule. When the family SU(3) is the
  fibre A2(x) of an event (12098), every one of the 540 zero-sum cubics among the (27,3)+(27bar,3bar) matter roots of that event uses three DISTINCT
  family phases (checked for all 40 events): the cubic coupling is d_ABC epsilon_ijk in the family index. For one Weyl
  species in (27,3) the symmetric self-Yukawa then vanishes -- Pass 11271 (applied in 11483) and the matter81 packet
  (2026-09-21, 'one root from each external phase'). Family masses need a Higgs in (27, 6bar), as 11271 states.
12103 -- NEGATIVE: feeding the chiral matter back does not select the three-family shift. With
  V = -(N0_all - r N0_matter) (bosonic adjoint minus r x the Standard-Model matter roots, Z3 holonomy on a circle), over
  r in [0, 5] the minimum is always a non-chiral shift (fixed dim 134 for small r, 80 for larger r); the three-family
  shifts (86, with 58 matter roots of phase 0) never win.
12104 -- the rule for a perfect (three-family shift, clean fermion parity) pair: sigma is EVEN on the family a2 (the
  fermion parity commutes with the family SU(3)). All 40 perfect pairs have sigma even on all 6 family roots (and odd on
  32 of the 72 e6 roots); all 60 imperfect pairs have sigma odd on 4 family roots.
12105 -- the X/Y couplings are a perfect matching: each Q sector couples to exactly one (u, e) sector and each L sector
  to exactly one (d, N) sector. Gauge-mediated dimension-6 operators are diagonal in the grading index (the SU(5)'
  copy), so proton decay is flavour-diagonal in that index at tree level; branching ratios then follow minimal-SU(5)
  gauge exchange (no grading-induced enhancement of nu K+).
"""

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12053_gate_sets_and_real_forms import setup  # noqa: E402
from w33_pass12087_standard_model_sectors import Gradings  # noqa: E402

OUT = ROOT / "data" / "w33_pass12102_to_12105_families_parity_proton.json"
SIMPLE = np.array([
    [0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5], [1, 1, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, 0, 0, 0],
    [0, 0, -1, 1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, 0, 0], [0, 0, 0, 0, -1, 1, 0, 0], [0, 0, 0, 0, 0, -1, 1, 0]])
GEN = {"Q": (6, 1), "uc": (3, -4), "dc": (3, 2), "L": (2, -3), "ec": (1, 6)}


def main():
    checks, res = {}, {}
    g = Gradings()
    R, fib = g.R, g.fib
    Adj, invs, tick, _ = setup()
    key = {tuple(np.round(r * 2).astype(int)): i for i, r in enumerate(R)}
    # 12102
    ok102 = True
    for x in range(40):
        A2 = R[fib[x]]
        Pa = A2.T @ np.linalg.pinv(A2.T)
        far = [y for y in range(40) if y != x and not Adj[x, y]]
        matter = sorted(i for y in far for i in fib[y])
        phase = {i: tuple(np.round(Pa @ R[i] * 6).astype(int)) for i in matter}
        ms = set(matter)
        ntri = 0
        for a, b in itertools.combinations(matter, 2):
            c = key.get(tuple(np.round(-(R[a] + R[b]) * 2).astype(int)))
            if c is not None and c in ms and c > b:
                ok102 &= len({phase[a], phase[b], phase[c]}) == 3
                ntri += 1
        ok102 &= ntri == 540
    checks["12102: for every event, all 540 zero-sum matter cubics (270 in (27,3)^3 + 270 conjugate) use three distinct family phases (d epsilon_ijk; = 11271)"] = bool(ok102)
    # common setup on one SM grading
    PH = np.round((np.array(list(itertools.product(range(3), repeat=8))) @ SIMPLE) @ R.T).astype(int) % 3
    PH = PH[PH.any(1)]
    gens = g.sm_flag(7)
    V = g.span_of(gens)
    sec, Y, xy = g.sectors(gens)
    lab = {ch: g.label(ch, c) for ch, c in sec.items()}
    gauge = [i for c in g.comps(g.fixedmask(V)) for i in c]
    Y6 = np.round(R @ Y * 6).astype(int)
    eps = np.array([[int(g.vecs[h][a]) for h in gens] for a in range(240)])
    rlab = np.array([lab[tuple(e)] for e in eps])
    orbsize = np.zeros(240, int)
    for i in range(240):
        orb, st = {i}, [i]
        while st:
            a = st.pop()
            for b in gauge:
                j = g.rkey[tuple(np.round((R[a] - (R[a] @ R[b]) * R[b]) * 2).astype(int))]
                if j not in orb:
                    orb.add(j)
                    st.append(j)
        orbsize[i] = len(orb)
    comp = [ph for ph in PH if not np.any(ph[gauge] != 0)]
    fam = np.array([(lambda N: len(set(N)) == 1 and abs(N[0]) == 3)(
        [int(np.sum((orbsize == o) & (Y6 == y) & (ph == 1)) - np.sum((orbsize == o) & (Y6 == -y) & (ph == 1))) // o for o, y in GEN.values()])
        for ph in comp])
    matter = np.isin(rlab, ["Q", "ue", "dN", "L"])
    N0all = np.array([8 + int(np.sum(ph == 0)) for ph in comp])
    N0mat = np.array([int(np.sum((ph == 0) & matter)) for ph in comp])
    wins = Counter()
    for r in np.linspace(0, 5, 501):
        E = -(N0all - r * N0mat)
        best = np.flatnonzero(E == E.min())
        wins[bool(fam[best].all())] += 1
    res["12103_family_shift_wins"] = wins[True]
    checks["12103: over r in [0,5] the three-family shifts never win (fam N0all = 86, N0mat = 58)"] = (
        wins[True] == 0 and set(N0all[fam]) == {86} and set(N0mat[fam]) == {58})
    clean = []
    for h in V:
        if g.kinds[h] != "split":
            continue
        odd_labels = {lab[ch] for ch in sec if any(g.vecs[h][a] for a in range(240) if tuple(eps[a]) == ch)}
        if "XY" not in odd_labels and "gauge" not in odd_labels:
            clean.append(h)
    feat = Counter()
    for ph, f in zip(comp, fam):
        if not f:
            continue
        comps = g.comps(ph == 0)
        a2 = next(c for c in comps if len(c) == 6)
        e6 = next(c for c in comps if len(c) == 72)
        for s in clean:
            sig = g.vecs[s]
            No = tuple(int(np.sum((orbsize == o) & (Y6 == y) & (ph == 1) & sig) - np.sum((orbsize == o) & (Y6 == -y) & (ph == 1) & sig)) // o for o, y in GEN.values())
            feat[(len(set(No)) == 1 and abs(No[0]) == 3, int(sig[a2].sum()), int(sig[e6].sum()))] += 1
    res["12104"] = {str(k): v for k, v in feat.items()}
    checks["12104: perfect iff sigma even on the family a2 (40 perfect: 0 odd a2 roots; 60 imperfect: 4)"] = feat == Counter({(True, 0, 32): 40, (False, 4, 40): 60})
    chXY = next(ch for ch, l in lab.items() if l == "XY")
    pairs = [(a, b) for a, b in itertools.combinations(sorted(sec), 2)
             if tuple((x + y) % 2 for x, y in zip(a, b)) == chXY and {lab[a], lab[b]} in ({"Q", "ue"}, {"L", "dN"})]
    deg = Counter()
    for a, b in pairs:
        deg[a] += 1
        deg[b] += 1
    checks["12105: X/Y couplings form a perfect matching (each Q with one (u,e), each L with one (d,N))"] = (
        len(pairs) == 15 and set(deg.values()) == {1} and len(deg) == 30)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
