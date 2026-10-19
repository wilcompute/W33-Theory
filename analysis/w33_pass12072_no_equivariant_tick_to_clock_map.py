"""Pass 12072: there is no equivariant tick-to-clock map (Claude track; settles the question flagged in 12068).

The 120 Clifford ticks of 12055 (eigenprojector labels (p, k)) and the 120 clock involutions of E8 (12052) are equal
in number. Exact results:
  1. Ticks are affine hyperplanes. Pauli conjugation shifts labels, W_r Pi_k(p) W_r^dag = Pi_{k + c omega(r,p)}(p), so
     the 120 ticks carry the action of the affine symplectic group ASp(4,3) = F_3^4 : Sp(4,3) on the 120 affine
     hyperplanes {omega(x, p) = k} of phase space.
  2. Every Sp(4,3) inside the Clifford group fixes 40 ticks. H^1(Sp(4,3), F_3^4) = 0 (GAP: one complement class of the
     translations in ASp(4,3), order 4199040), so every complement is a point stabiliser of AG(4,3) and fixes the 40
     hyperplanes through that point. Directly in the 12055 operator model: with symmetric Weyl labels
     (D_v = w^{-a.b} X^a Z^b) the 40 label-0 ticks are Weil elements and act on the 120 tick projectors with orbits
     40 + 80. (With 12055's own non-symmetric labels the label-0 ticks also generate translations and are transitive.)
  3. Clocks are one orbit of 120 under Sp(4,3) with stabiliser of order 432, and the point stabiliser (1296) fixes
     NONE of the three clocks at its point (it permutes them through SL(2,3)/Q8 = Z3).
  So no bijection between ticks and clocks is equivariant for any copy of Sp(4,3) acting on both. A tick determines
  its event (the map tick -> point is equivariant) but not its clock.
Consequences (recorded): 12055's '120 = the clock involutions' is a count only; 12061's spectra and inequalities stand,
but its reading 'a two-tick condensate carries the 12060 rest frames' is WITHDRAWN (it assumed ticks are clocks);
12060's statements about clock groups are unaffected. The clock choice at an event is not a tick datum.
"""

import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12055_microscopic_tick_model import PROJ, PTS, FORM, pauli  # noqa: E402

OUT = ROOT / "data" / "w33_pass12072_no_equivariant_tick_to_clock_map.json"
REC = ROOT / "analysis" / "search_drivers_12072" / "complements.out"
w = np.exp(2j * np.pi / 3)


def main():
    checks, res = {}, {}
    P = [PROJ[i][k] for i in range(40) for k in range(3)]

    def which(M):
        for a, Q in enumerate(P):
            if np.allclose(M, Q, atol=1e-9):
                return a
        return None
    shift_ok = True
    for i, k in itertools.product(range(0, 40, 7), range(3)):
        for r in PTS[::5]:
            W = pauli(r)
            a = which(W @ PROJ[i][k] @ W.conj().T)
            shift_ok &= a is not None and a // 3 == i and (a % 3 - k) % 3 in ({0} if FORM(r, PTS[i]) == 0 else {1, 2})
    checks["Pauli conjugation fixes the point and shifts the label iff omega(r,p) != 0 (affine-hyperplane action)"] = bool(shift_ok)
    def Dsym(v):  # symmetric Weyl operator D_v = w^{-a.b} X^a Z^b (exact Weil covariance for odd q)
        a1, a2, b1, b2 = v
        return w ** ((2 * (a1 * b1 + a2 * b2)) % 3) * pauli(v)
    S0 = [(np.eye(9) + Dsym(v) + Dsym(v) @ Dsym(v)) / 3 for v in PTS]
    checks["symmetric label-0 projectors are tick projectors (one per point)"] = sorted(which(Q) // 3 for Q in S0) == list(range(40))

    def orbs_of(Us):
        perms = [[which(u @ Q @ u.conj().T) for Q in P] for u in Us]
        if any(None in pm for pm in perms):
            return None
        seen, out = set(), []
        for a in range(120):
            if a in seen:
                continue
            o, st = {a}, [a]
            while st:
                b = st.pop()
                for pm in perms:
                    c = pm[b]
                    if c not in o:
                        o.add(c)
                        st.append(c)
            seen |= o
            out.append(sorted(o))
        return out
    weil = orbs_of([Q + w * (np.eye(9) - Q) for Q in S0])
    res["orbits_under_weil_label0_ticks"] = sorted(len(o) for o in weil)
    checks["the Weil copy of Sp(4,3) (symmetric label-0 ticks) has orbits 40 + 80 on ticks; the 40 = its label-0 ticks"] = bool(
        sorted(map(len, weil)) == [40, 80] and sorted(next(o for o in weil if len(o) == 40)) == sorted(which(Q) for Q in S0))
    raw = orbs_of([np.eye(9) + (w - 1) * (np.eye(9) - PROJ[i][0]) for i in range(40)])
    res["orbits_under_12055_label0_ticks"] = sorted(len(o) for o in raw)
    checks["control: 12055's own label-0 ticks (non-symmetric labels) generate translations too -- transitive on 120"] = sorted(map(len, raw)) == [120]
    rec = REC.read_text()
    checks["H^1(Sp(4,3), F_3^4) = 0: one complement class of translations in ASp(4,3) (GAP, |ASp| = 4199040)"] = (
        "|ASp|=4199040" in rec and "ASp(4,3): " in rec and rec.split("ASp(4,3): ")[1].strip().startswith("1"))
    from w33_pass12053_gate_sets_and_real_forms import setup, sp43_from_ticks  # noqa: E402
    Adj, invs, tick, fib = setup()
    G = sp43_from_ticks(tick)
    clocks = [s for k, s in invs if k == "clock"]
    p = 0
    atp = [s for s in clocks if {x for x in range(40) if not s[fib[x]].any()} == set(np.nonzero(Adj[p])[0])]
    Sp_ = np.array([set(g[fib[p]]) == set(fib[p]) for g in G])
    fixes = [bool(np.all(np.all(s[G[Sp_]] == s[None, :], axis=1))) for s in atp]
    stab = [int(np.all(s[G] == s[None, :], axis=1).sum()) for s in atp]
    checks["clocks: point stabiliser (1296) fixes none of the 3 clocks at p; clock stabiliser 432"] = (
        int(Sp_.sum()) == 1296 and len(atp) == 3 and not any(fixes) and stab == [432, 432, 432])
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
