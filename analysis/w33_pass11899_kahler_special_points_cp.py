"""Pass 11899: special points of the Kahler moduli of two Z3 tori -- the W(3,3) dictionary of the symmetric vacua, and CP.

Passes 11897-11898: the Hermitian Kahler moduli Z of T^4/Z3 act on the nine twisted fixed points by the two-qutrit Weil
representation, and the moduli-dependent couplings are the five even thetas, which fill P^4 with the Burkhardt group
PSp(4,3) (order 25920) acting. Modular-invariant potentials have critical points at the points with nontrivial residual
symmetry, so these are the candidate symmetric vacua. CP of the Kahler moduli (Z -> -conj Z) acts on the thetas as
complex conjugation, theta(-conj Z) = conj theta(Z).

Results:
  * The isolated special points (one-dimensional eigenspaces of group elements) number 13805 and form 11 orbits with
    projective stabilisers 648, 576, 162, 120, 108, 48, 36, 16, 12, 9, 5 (orbits 40, 45, 160, 216, 240, 540, 720, 1620,
    2160, 2880, 5184).
  * The 40 (stabiliser 648) contain the theta value at infinity: they are the cusps (large-volume limits). Their
    symplectic stabiliser fixes exactly one totally isotropic plane: the 40 cusps are the 40 lines of W(3,3) (the maximal
    commuting Pauli sets; at the cusp the couplings are diagonal in that context).
  * The 45 (stabiliser 576) fix exactly one unordered split {P, P^perp}: the 45 tensor factorisations of the two qutrits
    (factors exchanged); the 160 (stabiliser 162) fix one point and one line through it: the flags of W(3,3); the 240
    fix one point, the 720 one line.
  * The ten non-cusp orbits are reached at finite Kahler moduli (Newton to residual 1e-12, Im Z positive definite): they
    are interior symmetric vacua.
  * Every special orbit is CP-conserving (conj theta lies in the group orbit of theta, to 1e-15), while generic Kahler
    points are not (control); their CP violation shrinks exponentially toward the cusp (large volume). So, as for the Siegel fixed points (Pass 11874), CP violation in the twisted couplings requires the
    Kahler moduli away from every symmetric point.
"""

import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11897_11898_kahler_moduli_two_qutrit_weil as K  # noqa: E402

OUT = ROOT / "data" / "w33_pass11899_kahler_special_points_cp.json"
OM = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [-1, 0, 0, 0], [0, -1, 0, 0]])


def canon(v):
    v = v / np.linalg.norm(v)
    k = np.argmax(abs(v) > 1e-6)
    return v * abs(v[k]) / v[k]


def key(v):
    return (np.round(canon(v), 5) + 0).tobytes()


def w33_objects():
    vecs = [np.array(v) for v in itertools.product(range(3), repeat=4) if any(v)]
    pts = []
    for v in vecs:
        if not any(((2 * v) % 3 == p).all() for p in pts):
            pts.append(v)
    planes = set()
    for a, b in itertools.combinations(pts, 2):
        planes.add(frozenset(tuple((x * a + y * b) % 3) for x in range(3) for y in range(3) if (x, y) != (0, 0)))
    iso = [p for p in planes if all((np.array(u) @ OM @ np.array(w)) % 3 == 0 for u in p for w in p)]
    nondeg = [p for p in planes if p not in iso]

    def perp(p):
        return frozenset(tuple(v) for v in vecs if all((v @ OM @ np.array(w)) % 3 == 0 for w in p))
    splits = []
    for p in nondeg:
        pr = frozenset([p, perp(p)])
        if pr not in splits:
            splits.append(pr)
    return pts, iso, splits


def main():
    rng = np.random.default_rng(11899)
    E = K.even_basis()
    Ep = np.linalg.pinv(E)
    D = np.sqrt(np.diag(E.T @ E))
    g5 = [np.diag(D) @ Ep @ g @ E @ np.diag(1 / D) for g in K.GENS.values()]
    G = np.array(K.closure(g5, False, dim=5))
    unitary = float(np.max(abs(np.einsum("gij,gkj->gik", G, G.conj()) - np.eye(5))))
    gset = set((np.round(g, 4) + 0).tobytes() for g in G)
    conj_normalises = all((np.round(g.conj(), 4) + 0).tobytes() in gset for g in G)
    # special points
    pts = {}
    ev, vec = np.linalg.eig(G)
    for g in range(len(G)):
        for i in range(5):
            if np.sum(abs(ev[g] - ev[g][i]) < 1e-6) == 1:
                v = canon(vec[g][:, i])
                pts.setdefault(key(v), v)
    P = list(pts.values())
    keys = {k: i for i, k in enumerate(pts)}
    used = np.zeros(len(P), bool)
    orbits = []
    for i in range(len(P)):
        if used[i]:
            continue
        GPi = G @ P[i]
        orb = set(key(w) for w in GPi)
        for k in orb:
            if k in keys:
                used[keys[k]] = True
        cp = float(np.max(abs(GPi @ P[i])))  # |<g p, conj p>|: 1 iff conj p in the orbit of p
        orbits.append(dict(rep=i, orbit=len(orb), stabiliser=25920 // len(orb), cp_overlap=cp))
    orbits.sort(key=lambda o: -o["stabiliser"])
    # cusp: theta at infinity
    e0 = np.zeros(5, complex)
    e0[0] = 1
    for o in orbits:
        o["contains_infinity_cusp"] = bool(np.max(abs(G @ P[o["rep"]] @ e0)) > 1 - 1e-9)
    O = K.lattice(6)

    def th(z):
        return D * (Ep @ K.theta2(np.array([[z[0], z[1]], [z[2], z[3]]]), O))
    cusp_approach = []
    for y in (1.0, 2.0, 4.0):
        t = th(np.array([1j * y, 0, 0, 1j * y]))
        cusp_approach.append(float(1 - abs(t[0]) / np.linalg.norm(t)))
    # W(3,3) objects fixed by the symplectic stabiliser
    G9 = np.array(K.closure(list(K.GENS.values()), False))
    wpts, iso, splits = w33_objects()

    def img(s, p):
        return frozenset(tuple((s @ np.array(w)) % 3) for w in p)
    for o in orbits:
        x = E @ (P[o["rep"]] / D)
        x /= np.linalg.norm(x)
        S = G9[abs((G9 @ x) @ x.conj()) > 1 - 1e-8]
        sym = [K.symplectic_image(g) for g in S]
        fp = [p for p in wpts if all(any(((s @ p) % 3 == (c * p) % 3).all() for c in (1, 2)) for s in sym)]
        fl = [p for p in iso if all(img(s, p) == p for s in sym)]
        fs = [pr for pr in splits if all(frozenset(img(s, p) for p in pr) == pr for s in sym)]
        o["fixed_w33_points"], o["fixed_w33_lines"], o["fixed_splits"] = len(fp), len(fl), len(fs)
        o["flag"] = bool(len(fp) == 1 and len(fl) == 1 and tuple(fp[0]) in fl[0])
    # interior: Newton theta(Z) ~ v for the non-cusp orbits

    def ymin(z):
        Z = np.array([[z[0], z[1]], [z[2], z[3]]])
        return float(np.min(np.linalg.eigvalsh((Z - Z.conj().T) / 2j)))
    for o in orbits:
        if o["contains_infinity_cusp"]:
            continue
        v0 = P[o["rep"]]
        found = None
        for w in [v0] + [G[g] @ v0 for g in rng.choice(len(G), 8, replace=False)]:
            k = int(np.argmax(abs(w)))
            for _ in range(6):
                Z0 = K.rand_Z(rng, ymin=0.5, yscale=3.0)
                z = np.array([Z0[0, 0], Z0[0, 1], Z0[1, 0], Z0[1, 1]])
                for _ in range(60):
                    t = th(z)
                    if not np.isfinite(t).all() or ymin(z) < 0.05:
                        break
                    f = np.delete(t / t[k] - w / w[k], k)
                    if np.linalg.norm(f) < 1e-12:
                        break
                    J = np.zeros((4, 4), complex)
                    for a in range(4):
                        dz = np.zeros(4, complex)
                        dz[a] = 1e-6
                        t2 = th(z + dz)
                        J[:, a] = (np.delete(t2 / t2[k], k) - np.delete(t / t[k], k)) / 1e-6
                    step = np.linalg.lstsq(J, -f, rcond=None)[0]
                    z = z + step * min(1.0, 0.9 / max(1e-12, np.linalg.norm(step)))
                t = th(z)
                if np.isfinite(t).all() and ymin(z) > 0.05 and np.linalg.norm(np.delete(t / t[k] - w / w[k], k)) < 1e-12:
                    found = z
                    break
            if found is not None:
                break
        o["interior_point"] = None if found is None else [[float(c.real), float(c.imag)] for c in found]
        o["interior_ymin"] = None if found is None else ymin(found)
        o["interior_max_abs"] = None if found is None else float(np.max(abs(found)))
    # CP control: generic Kahler points
    ctrl = []
    for _ in range(5):
        t = th(np.array(list(K.rand_Z(rng, ymin=0.5, yscale=3.0).ravel())))
        t = t / np.linalg.norm(t)
        ctrl.append(float(np.max(abs((G @ t) @ t))))
    # CP violation along a ray toward the cusp: 1 - overlap shrinks exponentially
    Zb = K.rand_Z(rng, ymin=0.3, yscale=3.0)
    cpy = []
    for lam in (1.0, 2.0, 3.0):
        Zl = (Zb + Zb.conj().T) / 2 + lam * (Zb - Zb.conj().T) / 2
        t = th(np.array(list(Zl.ravel())))
        t = t / np.linalg.norm(t)
        cpy.append(float(1 - np.max(abs((G @ t) @ t))))
    res = dict(pass_id=11899, cp_violation_toward_cusp=cpy, group_order_on_even5=len(G), unitary_err=unitary, conj_normalises=conj_normalises,
               special_points=len(P), orbits=orbits, cusp_approach_defect=cusp_approach, cp_control_generic=ctrl)
    st = [o["stabiliser"] for o in orbits]
    non_cusp = [o for o in orbits if not o["contains_infinity_cusp"]]
    by = {o["stabiliser"]: o for o in orbits}
    res["checks"] = {k: bool(v) for k, v in dict(
        group_25920_projective=len(G) == 51840 and unitary < 1e-12 and conj_normalises,
        special_points_13805=len(P) == 13805,
        eleven_orbits=st == [648, 576, 162, 120, 108, 48, 36, 16, 12, 9, 5],
        cusps_are_the_40=[o["stabiliser"] for o in orbits if o["contains_infinity_cusp"]] == [648],
        cusp_approach=cusp_approach[-1] < 1e-5 and cusp_approach[0] > cusp_approach[1] > cusp_approach[2],
        cusps_fix_one_w33_line=by[648]["fixed_w33_lines"] == 1 and by[648]["fixed_w33_points"] == 0,
        nodes_fix_one_split=by[576]["fixed_splits"] == 1 and by[576]["fixed_w33_points"] == 0
        and by[576]["fixed_w33_lines"] == 0,
        flags_160=by[162]["flag"],
        point_240_line_720=by[108]["fixed_w33_points"] == 1 and by[36]["fixed_w33_lines"] == 1,
        non_cusp_orbits_interior=all(o["interior_point"] is not None for o in non_cusp),
        all_special_cp_conserving=all(o["cp_overlap"] > 1 - 1e-8 for o in orbits),
        generic_kahler_cp_violating=max(ctrl) < 1 - 1e-8,
        cp_violation_suppressed_toward_cusp=cpy[0] > cpy[1] > cpy[2] > 0,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps({k: res[k] for k in ("special_points", "cp_control_generic", "checks", "all_checks_pass")}, indent=1))
    for o in orbits:
        print({k: o[k] for k in o if k not in ("interior_point",)})


if __name__ == "__main__":
    main()
