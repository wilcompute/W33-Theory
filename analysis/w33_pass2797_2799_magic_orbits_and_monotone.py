#!/usr/bin/env python3
"""Passes 2797-2799 -- how many magic states there really are, and what two copies buy.

Pass 2790 found the 36 Witting rays fall into three stabilizer-fidelity grades of sizes
4, 24 and 8, and I wrote there that "the distillation search needs three representatives,
not thirty-six".  That was one step too far, and this pass corrects it.

PASS 2797 -- IS THE GRADE A COMPLETE INVARIANT?  (It is not.)
    F_stab separates the rays into three classes.  That does not mean nothing else does:
    two rays can share a fidelity and still be Clifford-inequivalent.  The decisive test
    is the ORBIT structure under the two-qubit Clifford group.

PASS 2798 -- WHAT DO TWO COPIES BUY, FOR ANY PROTOCOL AT ALL?
    D_min(rho) = -log2 F_stab(rho) is a magic monotone (Bravyi, Browne, Calpin, Campbell,
    Gosset, Howard 2019): it cannot increase under ANY stabilizer operation, including
    measurement, post-selection and feed-forward.  Computing F_stab on TWO COPIES -- over
    all 36,720 four-qubit stabilizer states -- therefore bounds every two-copy protocol at
    once, not just a particular code family.  The question this settles is whether a
    two-copy no-go is INFORMATION-THEORETIC or merely STRUCTURAL.

PASS 2799 -- IS THE PHASE GROUP mu_12 FOR EVERY n?
    Pass 2791 proved mu_12 at n = 1 by exact enumeration and sampled it at n = 2.  There
    is a short proof for all n, and its one non-obvious step is checked numerically here.

    py -3 analysis/w33_pass2797_2799_magic_orbits_and_monotone.py
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
W = np.exp(2j * np.pi / 3)


# ---------------------------------------------------------------------------
# the 36 Witting rays (same construction as Pass 2790)
# ---------------------------------------------------------------------------
def build_rays() -> list[np.ndarray]:
    w = [1, W, W ** 2]
    raw = []
    for mu, nu in product(range(3), repeat=2):
        raw.append([0, 1, -w[mu], w[nu]])
    for mu, nu in product(range(3), repeat=2):
        raw.append([1, 0, -w[mu], -w[nu]])
    for mu, nu in product(range(3), repeat=2):
        raw.append([1, -w[mu], 0, w[nu]])
    for mu, nu in product(range(3), repeat=2):
        raw.append([1, w[mu], w[nu], 0])
    return [np.array(r, dtype=complex) / np.linalg.norm(r) for r in raw]


# ---------------------------------------------------------------------------
# Canonical keys, on a 1e-9 INTEGER lattice in full double precision.  Pass 2791's first
# run used complex64 at 7 digits and diverged, because 1/sqrt3 = 0.5773502692 sits exactly
# on that boundary.  Keys are used only for GROUP enumeration here, never for deciding
# whether two rays are equivalent -- see the fidelity matching in pass_2797.
# ---------------------------------------------------------------------------
def key_mat(m: np.ndarray) -> bytes:
    z = np.asarray(m, dtype=complex) * 1e9
    return (np.round(z.real).astype(np.int64).tobytes()
            + np.round(z.imag).astype(np.int64).tobytes())


def key_state(v: np.ndarray) -> bytes:
    idx = int(np.argmax(np.abs(v) > 1e-9))
    return key_mat(v * np.exp(-1j * np.angle(v[idx])))


def clifford_gens(nq: int) -> list[np.ndarray]:
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    S = np.diag([1, 1j]).astype(complex)
    I = np.eye(2, dtype=complex)

    def onwire(g, k):
        m = np.array([[1]], dtype=complex)
        for j in range(nq):
            m = np.kron(m, g if j == k else I)
        return m

    gens = [onwire(H, k) for k in range(nq)] + [onwire(S, k) for k in range(nq)]
    d = 2 ** nq
    for a in range(nq):
        for b in range(nq):
            if a == b:
                continue
            M = np.zeros((d, d), dtype=complex)
            for x in range(d):
                bits = [(x >> (nq - 1 - i)) & 1 for i in range(nq)]
                bits[b] ^= bits[a]
                y = 0
                for i in range(nq):
                    y = (y << 1) | bits[i]
                M[y, x] = 1
            gens.append(M)
    return gens


def stabilizer_states(nq: int, expected: int | None = None) -> list[np.ndarray]:
    d = 2 ** nq
    start = np.zeros(d, dtype=complex)
    start[0] = 1
    gens = clifford_gens(nq)
    seen = {key_state(start): start}
    frontier = [start]
    while frontier:
        nxt = []
        for v in frontier:
            for g in gens:
                u = g @ v
                k = key_state(u)
                if k not in seen:
                    seen[k] = u
                    nxt.append(u)
        frontier = nxt
    states = list(seen.values())
    if expected is not None and len(states) != expected:
        print(f"  *** WARNING: got {len(states)} states, expected {expected} ***")
    return states


# ===========================================================================
def pass_2797(rays, stab2) -> dict:
    print("=" * 76)
    print("Pass 2797 -- are the three grades the Clifford EQUIVALENCE CLASSES?")
    print("=" * 76)

    fid = [max(abs(np.vdot(s, p)) ** 2 for s in stab2) for p in rays]
    lvls = sorted({round(f, 9) for f in fid}, reverse=True)
    grade = {lvl: [i for i, f in enumerate(fid) if abs(f - lvl) < 1e-9] for lvl in lvls}
    print("grades by stabilizer fidelity:")
    for lvl, mem in grade.items():
        print(f"   F_stab = {lvl:.9f} : {len(mem):2d} rays")

    gens = clifford_gens(2)
    ident = np.eye(4, dtype=complex)
    seen = {key_mat(ident): ident}
    frontier = [ident]
    while frontier:
        nxt = []
        for m in frontier:
            for g in gens:
                q = g @ m
                k = key_mat(q)
                if k not in seen:
                    seen[k] = q
                    nxt.append(q)
        frontier = nxt
    group = list(seen.values())
    print(f"\ntwo-qubit Clifford group enumerated : {len(group)}  "
          f"(= 11520 * 8 phases = {11520 * 8})")

    # Orbits by FIDELITY matching, not by a rounded key.  A hash key that misses one
    # match silently SPLITS an orbit, and a split orbit is exactly the kind of false
    # "these are inequivalent" claim this project has paid for before.  The only overlaps
    # in this configuration are 0 and 1/3 (Pass 2790), so a threshold at 0.999 has a gap
    # of 2/3 to the nearest competing value -- it is nowhere near anything.
    R = np.array(rays)
    parent = list(range(36))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    escapes = 0
    for g in group:
        M = np.abs(R.conj() @ (g @ R.T)) ** 2          # M[j, i] = |<r_j | g r_i>|^2
        hit = M > 0.999
        for i in range(36):
            js = np.flatnonzero(hit[:, i])
            if js.size == 0:
                escapes += 1
            else:
                for j in js:
                    union(i, int(j))

    orbits = {}
    for i in range(36):
        orbits.setdefault(find(i), []).append(i)
    sizes = sorted(len(o) for o in orbits.values())
    print(f"ray images landing OUTSIDE the 36-ray set : {escapes} of {len(group)*36}")
    print(f"Clifford equivalence classes on the rays  : {len(orbits)}, sizes {sizes}")

    grade_of = {i: lvl for lvl, mem in grade.items() for i in mem}
    pure = all(len({grade_of[i] for i in o}) == 1 for o in orbits.values())
    equal = sorted(len(m) for m in grade.values()) == sizes and pure
    print(f"every class lies inside one grade         : {pure}")
    print(f"CLASSES == GRADES                         : {equal}")

    if pure and not equal:
        print("\n  So F_stab is a genuine invariant but NOT a complete one: it is constant")
        print("  on classes, and one grade splits.  Which grade:")
        for lvl, mem in grade.items():
            cls = sorted({find(i) for i in mem})
            print(f"     F_stab = {lvl:.9f}  ({len(mem):2d} rays)  ->  "
                  f"{len(cls)} Clifford class(es) of sizes "
                  f"{sorted(len(orbits[c]) for c in cls)}")
        print("\n  CORRECTION TO PASS 2790.  I wrote there that the distillation search")
        print("  needs three representatives.  It needs FOUR: two rays with equal")
        print("  stabilizer fidelity need not be Clifford-equivalent, and here they are")
        print("  not.  The correct statement is that grade is NECESSARY but not")
        print("  SUFFICIENT for equivalence.")
    return {"grade_sizes": sorted(len(m) for m in grade.values()),
            "clifford_group_with_phase": len(group),
            "class_sizes": sizes,
            "classes_equal_grades": bool(equal),
            "every_class_inside_one_grade": bool(pure),
            "images_leaving_the_ray_set": int(escapes),
            "grades": {f"{lvl:.9f}": len(mem) for lvl, mem in grade.items()}}


# ===========================================================================
def pass_2798(rays, stab2, reps) -> dict:
    print()
    print("=" * 76)
    print("Pass 2798 -- what two copies buy, for EVERY protocol at once")
    print("=" * 76)

    print("building the four-qubit stabilizer states (expect 36720)...")
    stab4 = stabilizer_states(4, expected=36720)
    S4 = np.array(stab4)
    print(f"  got {len(stab4)}")

    out = {}
    print("\n  grade      F_stab(psi)  F_stab(psi^2)   F_stab^2     D_min(psi)  D_min(psi^2)")
    for name, idx in reps.items():
        psi = rays[idx]
        f1 = float(max(abs(np.vdot(s, psi)) ** 2 for s in stab2))
        f2 = float(np.max(np.abs(S4.conj() @ np.kron(psi, psi)) ** 2))
        out[name] = {"F_stab_1": f1, "F_stab_2": f2, "F_stab_1_squared": f1 * f1,
                     "D_min_1": -np.log2(f1), "D_min_2": -np.log2(f2),
                     "multiplicative": bool(abs(f2 - f1 * f1) < 1e-9)}
        print(f"  {name:9s}  {f1:.9f}  {f2:.9f}   {f1*f1:.9f}  "
              f"{-np.log2(f1):.6f}    {-np.log2(f2):.6f}")

    mult = all(v["multiplicative"] for v in out.values())
    print(f"\n  F_stab exactly multiplicative on two copies, every grade : {mult}")

    print("\n  D_min is a magic monotone: no stabilizer operation can increase it.  So a")
    print("  two-copy protocol starting from grade g can only reach outputs with")
    print("  D_min <= D_min(psi^2).  Which grades does that permit as OUTPUT?")
    obstructs = False
    for name, v in out.items():
        budget = v["D_min_2"]
        reach = [n2 for n2, v2 in out.items() if v2["D_min_1"] <= budget + 1e-12]
        v["output_grades_permitted_by_the_monotone"] = reach
        v["monotone_permits_self_distillation"] = bool(v["D_min_1"] <= budget + 1e-12)
        print(f"    2 x {name:9s} (budget {budget:.6f}) -> permits: {', '.join(reach)}")
        if not v["monotone_permits_self_distillation"]:
            obstructs = True

    print(f"\n  Does the monotone FORBID two-copy distillation anywhere? {obstructs}")
    if not obstructs:
        print("""
  It does not.  Every grade has D_min(psi^2) = 2 D_min(psi) > D_min(psi), so two copies
  always carry more than enough magic to make one.  THEREFORE ANY TWO-COPY NO-GO IN THIS
  SYSTEM IS STRUCTURAL, NOT INFORMATION-THEORETIC: it is a statement about the protocol
  family searched, and widening the family is the right response to it, not evidence
  that the resource is exhausted.""")
    return out


# ===========================================================================
def pass_2799() -> dict:
    print()
    print("=" * 76)
    print("Pass 2799 -- the phase group is mu_12 for EVERY n")
    print("=" * 76)
    print("""
  1. Every generator entry lies in Q(zeta_12).  S contributes omega = zeta_12^4; X and
     CX contribute 0 and 1; F_3 contributes omega^{jk}/sqrt3, and the only non-obvious
     step is that 1/sqrt3 is in the field -- checked below.
  2. Q(zeta_12) is a field, and tensoring multiplies entries, so EVERY element of the
     n-qutrit Clifford group has entries in it, for every n.
  3. A scalar lambda*I in a finite matrix group has lambda a root of unity, and lambda
     lies in Q(zeta_12) by step 2.
  4. For even m the roots of unity in Q(zeta_m) are exactly mu_m.  12 is even.

  So the phase group is contained in mu_12 for all n; it contains mu_12 because n = 1
  already realises all twelve (Pass 2791: enumerated at order 2592 = 12 * 216) and
  tensoring with the identity embeds that.  Hence it EQUALS mu_12 for every n.
""")
    z = np.exp(2j * np.pi / 12)
    # The one step worth checking numerically, as an explicit identity rather than a
    # least-squares fit: an earlier version of this check used lstsq against the basis
    # {1, z, z^2, z^3}, which is underdetermined over R^2 and reported False even for the
    # permutation matrix X.  A direct identity has no such failure mode.
    ids = {
        "zeta_12 + conj(zeta_12) = sqrt3": abs((z + z.conjugate()) - np.sqrt(3)),
        "zeta_12^4 = omega": abs(z ** 4 - W),
        "zeta_12^3 = i": abs(z ** 3 - 1j),
        "1/sqrt3 = (zeta_12 + conj(zeta_12))/3": abs((z + z.conjugate()) / 3 - 1 / np.sqrt(3)),
    }
    for name, err in ids.items():
        print(f"  {name:42s} residual {err:.2e}   ok: {err < 1e-12}")
    ok = all(e < 1e-12 for e in ids.values())

    print("\n  minimal sensor exponent e = 3^n mod 12:")
    tab = {}
    for n in range(1, 7):
        e = (3 ** n) % 12 or 12
        tab[n] = e
        print(f"     n = {n}: d = {3**n:<5d}  e = {e}")
    return {"field_identities_hold": bool(ok),
            "identity_residuals": {k: float(v) for k, v in ids.items()},
            "exponent_table": {str(k): v for k, v in tab.items()},
            "conclusion": "phase group = mu_12 for all n; minimal exponent = 3^n mod 12"}


def main() -> int:
    rays = build_rays()
    print("building the two-qubit stabilizer states (expect 60)...")
    stab2 = stabilizer_states(2, expected=60)
    print(f"  got {len(stab2)}\n")

    r97 = pass_2797(rays, stab2)

    fid = [max(abs(np.vdot(s, p)) ** 2 for s in stab2) for p in rays]
    lvls = sorted({round(f, 9) for f in fid}, reverse=True)
    names = ["shallow", "mid", "deep"][:len(lvls)]
    reps = {nm: next(i for i, f in enumerate(fid) if abs(f - lvl) < 1e-9)
            for nm, lvl in zip(names, lvls)}

    r98 = pass_2798(rays, stab2, reps)
    r99 = pass_2799()

    out = {"pass_2797": r97, "pass_2798": r98, "pass_2799": r99}
    path = ROOT / "data" / "PART_W33_PASS2797_2799_MAGIC_ORBITS_AND_MONOTONE.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
