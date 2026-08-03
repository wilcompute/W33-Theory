#!/usr/bin/env python3
"""Pass 2790 -- what ARE the 36 magic rays, geometrically?

The parallel track's Pass 2784 (PR #206, provisional id 2777) proves an exact two-copy
no-go: over all 5355 binary [[4,2]] stabilizer codes and 4 syndromes, no branch that
closes back onto the M36 orbit improves fidelity anywhere in its magic-witness interval.
Their next step is to search three-copy, catalytic and non-identical schemes.

That search is enormous, and its size is set by how many INEQUIVALENT magic states there
are.  If all 36 rays are equivalent under the machine's own symmetry group, then a
protocol either works for all of them or none, and the search collapses.  If they split
into orbits, the orbits are the only distinctions that can matter, and any protocol has
to be indexed by orbit rather than by ray.

So before searching harder, ask a cheaper question: what is the ORBIT STRUCTURE of the
36 rays, and does it match the 8 + 24 + 4 deep/mid/shallow grading the census reports?

The grading is defined by overlap with stabilizer states, which is invariant under the
Clifford group.  So:

    if the symmetry group is TRANSITIVE on the 36 rays, the grading cannot be
    Clifford-invariant, and 8+24+4 must come from a choice of basis rather than from
    the geometry;

    if the grading IS the orbit decomposition, then it is group-theoretic, the three
    grades are genuinely inequivalent resources, and the distillation search only needs
    three representatives instead of 36.

This settles it exactly, with integer arithmetic, from the Gram matrix -- no group
enumeration needed, because the Gram profile is invariant under ANY unitary symmetry and
therefore separates orbits without knowing the group.

    py -3 analysis/w33_pass2790_witting_ray_geometry.py
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# Exact arithmetic in Z[omega], omega = e^{2 pi i / 3}, as pairs (a, b) = a + b*omega
# with the relation omega^2 = -1 - omega.  Everything below is integer arithmetic; no
# floating point is used anywhere in the classification.
# ---------------------------------------------------------------------------

def zw_mul(x, y):
    (a, b), (c, d) = x, y
    # (a + b w)(c + d w) = ac + (ad + bc) w + bd w^2,  w^2 = -1 - w
    return (a * c - b * d, a * d + b * c - b * d)


def zw_add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def zw_conj(x):
    # conj(w) = w^2 = -1 - w, so conj(a + b w) = (a - b) - b w
    a, b = x
    return (a - b, -b)


def zw_norm(x):
    """|x|^2 as an ordinary integer:  N(a + b w) = a^2 - a b + b^2."""
    a, b = x
    return a * a - a * b + b * b


ZERO = (0, 0)
ONE = (1, 0)
W = (0, 1)
W2 = (-1, -1)
POW = {0: ONE, 1: W, 2: W2}


def neg(x):
    return (-x[0], -x[1])


# ---------------------------------------------------------------------------
# The 36 rays, exactly as the parallel track's Pass 2784 lists them.  Written WITHOUT
# the 1/sqrt3 normalisation: every ray is an integer vector in Z[omega]^4 of squared
# norm 3, so all overlaps below are exact integers.
#
#   (0, 1, -w^mu,  w^nu)      (1, 0, -w^mu, -w^nu)
#   (1, -w^mu, 0,  w^nu)      (1,  w^mu,  w^nu, 0)      mu, nu in F_3
# ---------------------------------------------------------------------------

def build_rays():
    rays, tags = [], []
    for mu, nu in product(range(3), repeat=2):
        rays.append((ZERO, ONE, neg(POW[mu]), POW[nu]));      tags.append(("A", mu, nu))
    for mu, nu in product(range(3), repeat=2):
        rays.append((ONE, ZERO, neg(POW[mu]), neg(POW[nu]))); tags.append(("B", mu, nu))
    for mu, nu in product(range(3), repeat=2):
        rays.append((ONE, neg(POW[mu]), ZERO, POW[nu]));      tags.append(("C", mu, nu))
    for mu, nu in product(range(3), repeat=2):
        rays.append((ONE, POW[mu], POW[nu], ZERO));           tags.append(("D", mu, nu))
    return rays, tags


def inner(u, v):
    """<u|v> in Z[omega], unnormalised."""
    s = ZERO
    for a, b in zip(u, v):
        s = zw_add(s, zw_mul(zw_conj(a), b))
    return s


def main() -> int:
    rays, tags = build_rays()
    n = len(rays)
    print(f"rays: {n}")
    for r in rays:
        assert sum(zw_norm(c) for c in r) == 3, "every ray must have squared norm 3"
    print("all 36 rays have squared norm 3 (exact)")

    # 9 * |<i|j>|^2 is an integer because the normalisation is 1/sqrt3 on each side.
    gram = [[zw_norm(inner(rays[i], rays[j])) for j in range(n)] for i in range(n)]

    vals = Counter(gram[i][j] for i in range(n) for j in range(n) if i != j)
    print("\ndistinct off-diagonal 9|<i|j>|^2 values and multiplicities:")
    for v, c in sorted(vals.items()):
        print(f"   9|<i|j>|^2 = {v:2d}  ->  |<i|j>|^2 = {v}/9   count {c}")

    # The profile of a ray: how many other rays it meets at each overlap value.  This is
    # invariant under any unitary symmetry, so rays with different profiles CANNOT be in
    # the same orbit of any group.
    profiles = {}
    for i in range(n):
        prof = tuple(sorted(Counter(gram[i][j] for j in range(n) if j != i).items()))
        profiles.setdefault(prof, []).append(i)

    print(f"\ndistinct Gram profiles: {len(profiles)}")
    for prof, members in sorted(profiles.items(), key=lambda kv: -len(kv[1])):
        fams = Counter(tags[i][0] for i in members)
        print(f"   {len(members):2d} rays   families {dict(fams)}")
        print(f"        profile {prof}")

    sizes = sorted(len(m) for m in profiles.values())
    print(f"\nprofile class sizes: {sizes}")

    graded = sizes == [4, 8, 24]
    transitive_possible = len(profiles) == 1
    print(f"matches the 8 + 24 + 4 census grading : {graded}")
    print(f"a transitive symmetry group is possible: {transitive_possible}")

    # The orthogonality graph: rays i ~ j iff <i|j> = 0.  Its parameters are a hard,
    # basis-free invariant of the configuration.
    deg = [sum(1 for j in range(n) if j != i and gram[i][j] == 0) for i in range(n)]
    degs = Counter(deg)
    print(f"\northogonality graph degrees: {dict(degs)}")

    srg = None
    if len(degs) == 1:
        k = deg[0]
        lam, mu = set(), set()
        for i in range(n):
            for j in range(i + 1, n):
                common = sum(1 for t in range(n)
                             if t != i and t != j and gram[i][t] == 0 and gram[j][t] == 0)
                (lam if gram[i][j] == 0 else mu).add(common)
        if len(lam) == 1 and len(mu) == 1:
            srg = (n, k, lam.pop(), mu.pop())
            print(f"orthogonality graph is STRONGLY REGULAR: SRG{srg}")
        else:
            print(f"not strongly regular: lambda values {sorted(lam)}, mu values {sorted(mu)}")

    print()
    if graded:
        print("  The 8 + 24 + 4 grading IS a Gram-profile partition, so it is invariant")
        print("  under every unitary symmetry of the configuration.  No group can mix the")
        print("  grades.  The three grades are genuinely inequivalent magic resources, and")
        print("  a distillation search needs THREE representatives, not thirty-six.")
    elif transitive_possible:
        print("  All 36 rays have the same Gram profile, so a transitive symmetry group is")
        print("  not excluded -- and then the 8/24/4 grading cannot be Clifford-invariant.")

    # -----------------------------------------------------------------------------
    # The Gram profile is uniform, so the grading cannot come from how the rays sit
    # relative to EACH OTHER.  It is defined by overlap with STABILIZER states, which is
    # a different invariant -- and a Clifford-invariant one.  So test it directly:
    # compute the stabilizer fidelity
    #
    #     F_stab(psi) = max over stabilizer states s of |<s|psi>|^2
    #
    # for every ray.  If it takes three values with multiplicities 8, 24 and 4, the
    # grading is a genuine Clifford invariant.  If it is constant, the grading is not
    # Clifford-invariant and comes from somewhere else.
    # -----------------------------------------------------------------------------
    import numpy as np

    w = np.exp(2j * np.pi / 3)

    def to_complex(r):
        v = np.array([a + b * w for (a, b) in r], dtype=complex)
        return v / np.linalg.norm(v)

    psis = [to_complex(r) for r in rays]

    # The 60 two-qubit stabilizer states, as the Clifford orbit of |00>.
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    S = np.diag([1, 1j]).astype(complex)
    I2 = np.eye(2, dtype=complex)
    CNOT01 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
    CNOT10 = np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]], dtype=complex)
    gens = [np.kron(H, I2), np.kron(I2, H), np.kron(S, I2), np.kron(I2, S),
            CNOT01, CNOT10]

    def canon(v):
        """A state up to global phase, as a hashable rounded key."""
        idx = int(np.argmax(np.abs(v) > 1e-9))
        v = v * np.exp(-1j * np.angle(v[idx]))
        return tuple(np.round(v, 6).tolist())

    start = np.array([1, 0, 0, 0], dtype=complex)
    seen = {canon(start): start}
    frontier = [start]
    while frontier:
        nxt = []
        for v in frontier:
            for g in gens:
                u = g @ v
                k = canon(u)
                if k not in seen:
                    seen[k] = u
                    nxt.append(u)
        frontier = nxt
    stab = list(seen.values())
    print(f"\ntwo-qubit stabilizer states generated: {len(stab)} (expected 60)")

    fid = [max(abs(np.vdot(s, p)) ** 2 for s in stab) for p in psis]
    tally = Counter(round(f, 6) for f in fid)
    print("stabilizer fidelity  F_stab = max_s |<s|psi>|^2  over the 36 rays:")
    for v, c in sorted(tally.items(), reverse=True):
        print(f"   F_stab = {v:.6f}   on {c:2d} rays")

    fid_sizes = sorted(tally.values())
    grading_is_clifford_invariant = fid_sizes == [4, 8, 24]
    print(f"\nF_stab multiplicities {fid_sizes};  "
          f"reproduces 8 + 24 + 4 : {grading_is_clifford_invariant}")

    # Closed forms.  Every value is a twelfth.
    r3 = np.sqrt(3.0)
    CLOSED = {"shallow (4 rays)": 9 / 12,
              "mid     (24 rays)": (5 + 2 * r3) / 12,
              "deep    (8 rays)": (4 + 2 * r3) / 12}
    print("\nclosed forms, all twelfths:")
    closed_ok = True
    for name, v in CLOSED.items():
        # compare against the UNROUNDED fidelities; the tally keys are rounded to six
        # decimals for display and (5 + 2 sqrt3)/12 does not survive that rounding
        hits = sum(1 for f in fid if abs(v - f) < 1e-9)
        closed_ok &= hits > 0
        print(f"   {name}:  F_stab = {v:.9f}   exact on {hits:2d} rays")

    # And the thresholds fall out of ONE formula.  For rho_p = (1-p)|m><m| + p I/4 the
    # target overlap is <m|rho_p|m> = 1 - 3p/4, so the witness certifies non-stabilizer
    # exactly while 1 - 3p/4 > F_stab, i.e.
    #
    #                          p  <  4 (1 - F_stab) / 3 .
    #
    # The parallel track's Pass 2767 states three separate thresholds.  They are this one
    # formula evaluated at the three stabilizer fidelities.
    QUOTED = {"shallow (4 rays)": 1 / 3,
              "mid     (24 rays)": (7 - 2 * r3) / 9,
              "deep    (8 rays)": (8 - 2 * r3) / 9}
    print("\none formula  p < 4(1 - F_stab)/3  reproduces all three quoted thresholds:")
    all_ok = True
    for name, F in CLOSED.items():
        derived = 4 * (1 - F) / 3
        quoted = QUOTED[name]
        ok = abs(derived - quoted) < 1e-12
        all_ok &= ok
        print(f"   {name}:  derived {derived:.12f}   quoted {quoted:.12f}   equal: {ok}")
    print(f"\nall three thresholds derived from the fidelity spectrum: {all_ok}")

    out = {
        "pass": 2790,
        "rays": n,
        "stabilizer_states": len(stab),
        "stabilizer_fidelity_tally": {f"{v:.6f}": c for v, c in sorted(tally.items())},
        "grading_is_stabilizer_fidelity": grading_is_clifford_invariant,
        "stabilizer_fidelity_closed_forms_twelfths": {
            "shallow_4_rays": "9/12",
            "mid_24_rays": "(5 + 2 sqrt3)/12",
            "deep_8_rays": "(4 + 2 sqrt3)/12",
        },
        "one_threshold_formula": "p < 4 (1 - F_stab) / 3",
        "all_quoted_thresholds_derived": bool(all_ok),
        "overlap_values_9x": {str(k): v for k, v in sorted(vals.items())},
        "gram_profile_classes": sizes,
        "matches_8_24_4_grading": graded,
        "orthogonality_degrees": {str(k): v for k, v in sorted(degs.items())},
        "orthogonality_srg": list(srg) if srg else None,
        "prior_art": {
            "census_8_24_4": "parallel track BT822 / Pass 2767",
            "two_copy_no_go": "parallel track Pass 2784 (PR #206, provisional 2777)",
        },
    }
    path = ROOT / "data" / "PART_W33_PASS2790_WITTING_RAY_GEOMETRY.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
