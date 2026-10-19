"""Pass 12065: the Landau phases of 12054 against observers -- no phase has a rest frame, the event phase does not
choose the clock, and each ordered phase distinguishes one class of observers (Claude track; 12054, 12059-12061).

Second realisation. The 12054 patterns are rebuilt in the matrix model of 12059 (V = F_3^4, points = projective
points, observers = Kramers J), independently of the root model, and reproduce 12054's exact invariants:
event V15 (35/216, 25/108), event V24 (197/540, 77/540), staggered factorisation V15 (1/8, 1/4), isotropic line V24
(73/360, 59/180), signed hyperbolic line V24 (11/96, 7/96; signs (+,+,-,-) on a hyperbolic line).
Exact results (symmetry = stabiliser of the order parameter in Sp(4,3); observers fixed iff g J g^-1 = +-J):
  * event phase: symmetry Stab(p) (1296), transitive on the 36 observers; it is NOT inside the clock group H_p (index 3),
    so the point condensate does not choose among the three clocks at p -- the tick-level condensate (12055) does.
  * isotropic-line (context) phase: 1296; observers 9 + 27, the 9 = exactly the observers whose sky contains the
    context (the union of the mirror frames of its pairs, 12060).
  * staggered factorisation phase: 576; observers 12 + 24, the 12 = exactly the observers whose time reversal swaps the
    two qutrit factors (J H1 = H2).
  * signed hyperbolic line phase: 96; observers 12 + 24, the same 12 swapping observers.
  So NO ordered phase of the point condensate fixes an observer: every Landau phase is frame-free. Rest frames need
  two compatible clocks (12060-12061), which is a tick-level, not a point-level, order parameter.
Scope: the 12054 quartic Landau patterns; symmetry statements are exact.
"""

import itertools
import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass12059_observers_see_space_not_time as M  # noqa: E402

OUT = ROOT / "data" / "w33_pass12065_landau_phases_have_no_rest_frame.json"


def main():
    checks, res = {}, {}
    pts = sorted({M.norm(v) for v in M.VEC if v.any()})
    P = np.array(pts)
    Adj = np.array([[int(i != j and M.om(P[i], P[j]) == 0) for j in range(40)] for i in range(40)])
    G = M.build_group(pts)
    _, Js = M.kramers()
    pix = {p: i for i, p in enumerate(pts)}
    ptperm = np.array([[pix[M.norm(g @ P[i])] for i in range(40)] for g in G])
    ev, U = np.linalg.eigh(Adj.astype(float))
    V15, V24 = U[:, np.isclose(ev, -4)], U[:, np.isclose(ev, 2)]
    Ei, Ej = np.nonzero(np.triu(Adj))


    def q(phi):
        phi = phi / np.linalg.norm(phi)
        return np.sum(phi ** 4), np.sum(phi[Ei] ** 2 * phi[Ej] ** 2)


    proj = lambda V, x: V @ (V.T @ x)  # noqa: E731
    p = 0
    nb = list(np.nonzero(Adj[p])[0])
    far = [x for x in range(40) if x != p and not Adj[p, x]]
    line = [p, nb[0]] + [r for r in nb if Adj[nb[0], r]]
    qf = far[0]
    H2 = [x for x in range(40) if Adj[p, x] and Adj[qf, x]]
    H1 = [x for x in range(40) if all(Adj[x, y] for y in H2) and x not in H2]
    assert len(H1) == 4 and len(H2) == 4 and p in H1 and qf in H1
    stag = np.zeros(40); stag[H1] = 1; stag[H2] = -1
    e = np.eye(40)[p]
    pats = {"event_V15": proj(V15, e), "event_V24": proj(V24, e), "staggered_factorisation_V15": stag,
            "isotropic_line_V24": proj(V24, np.isin(np.arange(40), line).astype(float))}
    # signed hyperbolic line in V24: search sign patterns on H1
    for signs in itertools.product((1, -1), repeat=3):
        x = np.zeros(40); x[H1] = (1,) + signs
        a, b = q(proj(V24, x))
        if abs(a - 11 / 96) < 1e-9 and abs(b - 7 / 96) < 1e-9:
            pats["signed_hyperbolic_line_V24"] = proj(V24, x)
            res['signed_line_signs'] = [1] + list(signs)
            break
    x = np.zeros(40); x[H1] = 1
    pats["hyperbolic_line_V15"] = proj(V15, x)
    exact = {"event_V15": (Fr(35, 216), Fr(25, 108)), "event_V24": (Fr(197, 540), Fr(77, 540)),
             "staggered_factorisation_V15": (Fr(1, 8), Fr(1, 4)), "isotropic_line_V24": (Fr(73, 360), Fr(59, 180)),
             "signed_hyperbolic_line_V24": (Fr(11, 96), Fr(7, 96))}
    checks["second realisation reproduces all five exact 12054 invariants"] = all(
        k in pats and np.allclose(q(pats[k]), [float(exact[k][0]), float(exact[k][1])], atol=1e-12) for k in exact)
    Om_inv = (2 * M.Om) % 3
    Jkey = {}
    for i, J in enumerate(Js):
        Jkey[M.key(J)] = i
        Jkey[M.key(2 * J)] = i

    def orbs(mask):
        perm = np.array([[Jkey[M.key((G[g] @ J @ Om_inv @ G[g].T @ M.Om) % 3)] for J in Js] for g in np.nonzero(mask)[0]])
        seen, out = set(), []
        for j in range(36):
            if j not in seen:
                o = set(perm[:, j].tolist())
                seen |= o
                out.append(sorted(o))
        return out
    Jpt = lambda j, x: pix[M.norm(Js[j] @ P[x])]  # noqa: E731
    sky_L = {j for j in range(36) if {Jpt(j, x) for x in line} == set(line)}
    swap = {j for j in range(36) if {Jpt(j, x) for x in H1} == set(H2)}
    table = {}
    for k in exact:
        vv = np.round(pats[k] / np.abs(pats[k]).max(), 9)
        mask = np.array([np.allclose(vv[ptperm[g]], vv) for g in range(len(G))])
        o = orbs(mask)
        table[k] = (int(mask.sum()), sorted(map(len, o)), o, mask)
    res["phases"] = {k: dict(symmetry=v[0], observer_orbits=v[1]) for k, v in table.items()}
    checks["no phase fixes an observer (frame-free)"] = all(min(v[1]) > 1 for v in table.values())
    checks["event phase: 1296, transitive on the 36 observers"] = all(table[k][:2] == (1296, [36]) for k in ("event_V15", "event_V24"))
    checks["context phase: 1296, observers 9 + 27, the 9 = observers whose sky contains the context"] = (
        table["isotropic_line_V24"][:2] == (1296, [9, 27]) and any(set(o) == sky_L for o in table["isotropic_line_V24"][2]))
    checks["staggered factorisation 576 and signed hyperbolic line 96: observers 12 + 24, the 12 = J swapping H1, H2"] = (
        table["staggered_factorisation_V15"][:2] == (576, [12, 24]) and table["signed_hyperbolic_line_V24"][:2] == (96, [12, 24])
        and all(any(set(o) == swap for o in table[k][2]) for k in ("staggered_factorisation_V15", "signed_hyperbolic_line_V24")))
    # clock choice: the event symmetry Stab(p) is not inside its clock group (index 3)
    stab_p = table["event_V15"][3]
    idx = np.nonzero(stab_p)[0]
    orders3 = sum(1 for g in idx if M.order(G[g]) == 3)
    res["event_symmetry_order3_elements"] = orders3
    checks["event phase symmetry has order-3 elements outside the clock group's 26 (permutes the three clocks)"] = orders3 > 26
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
