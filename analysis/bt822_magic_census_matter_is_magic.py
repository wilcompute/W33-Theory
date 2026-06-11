#!/usr/bin/env python3
"""
BT822 - The magic census: matter = magic.

In the photon's two-qubit reading (C4 = path (x) polarization), classify
the 40 Witting rays against the full two-qubit stabilizer formalism:

  T1. Enumerate ALL 60 two-qubit stabilizer states (15 maximal commuting
      Pauli triples x 4 joint eigenstates).  Intersect with the 40
      Witting rays: EXACTLY the 4 basis rays are stabilizer states.
  T2. Support lemma verified: every two-qubit stabilizer state has
      support size in {1, 2, 4} - never 3.  All 36 omega-rays have
      support 3, hence are MAGIC (non-stabilizer) automatically.
  T3. Stabilizer fidelity of the magic rays: F = max_s |<s|psi>|^2 over
      the 60 stabilizer states - computed for all 36 (uniform by
      transitivity?), the machine's per-ray magic strength.
  T4. THE TRIALITY: on rays and on contexts, three classifications
      coincide exactly:
        holonet vacuum split   (BT812: 1+12+27 / 4+36)
        entanglement strata    (BT817: Schmidt rank census)
        MAGIC strata           (this packet)
      The matter shell (27 fully-entangled contexts / 36 magic rays) IS
      the machine's non-classical resource sector: matter = magic, gauge
      = the partially classical interface, vacuum = the unique classical
      context.  Contextuality (BT818) and magic are the same fuel seen
      through Kochen-Specker vs resource-theory lenses (Howard et al.,
      Nature 510, 351 (2014): contextuality supplies the magic).
"""
from __future__ import annotations

from itertools import combinations, product
import json

import numpy as np


def witting_rays():
    w = np.exp(2j * np.pi / 3.0)
    s3 = np.sqrt(3.0)
    rays = []
    for i in range(4):
        e = np.zeros(4, dtype=complex)
        e[i] = 1.0
        rays.append(e)
    for mu, nu in product(range(3), repeat=2):
        rays.append(np.array([0, 1, -(w**mu), w**nu]) / s3)
        rays.append(np.array([1, 0, -(w**mu), -(w**nu)]) / s3)
        rays.append(np.array([1, -(w**mu), 0, w**nu]) / s3)
        rays.append(np.array([1, w**mu, w**nu, 0]) / s3)
    return rays


def main():
    I2 = np.eye(2)
    Xq = np.array([[0, 1], [1, 0]], dtype=complex)
    Zq = np.diag([1, -1]).astype(complex)
    Yq = 1j * Xq @ Zq

    paulis = {}
    for a, b in product(range(2), repeat=2):
        for c, d in product(range(2), repeat=2):
            if (a, b, c, d) == (0, 0, 0, 0):
                continue
            P1 = np.linalg.matrix_power(Xq, a) @ np.linalg.matrix_power(Zq, b)
            P2 = np.linalg.matrix_power(Xq, c) @ np.linalg.matrix_power(Zq, d)
            paulis[(a, b, c, d)] = np.kron(P1, P2)
    assert len(paulis) == 15

    # maximal commuting triples: pairs {P,Q} commuting generate {P,Q,PQ}
    keys = list(paulis)
    triples = set()
    for u, v in combinations(keys, 2):
        if np.allclose(paulis[u] @ paulis[v], paulis[v] @ paulis[u]):
            wkey = tuple((u[i] + v[i]) % 2 for i in range(4))
            triples.add(frozenset((u, v, wkey)))
    assert len(triples) == 15
    print(f"T1 maximal commuting Pauli triples: {len(triples)} "
          f"(the doily W(3,2) lines)")

    # joint eigenbases -> 60 stabilizer states
    rng = np.random.default_rng(3)
    stab_states = []
    for T in triples:
        M = sum((rng.normal() + 1j * rng.normal()) * paulis[k] for k in T)
        _, vecs = np.linalg.eig(M)
        for k in range(4):
            psi = vecs[:, k] / np.linalg.norm(vecs[:, k])
            # dedupe by ray
            if not any(abs(np.vdot(psi, s))**2 > 1 - 1e-9
                       for s in stab_states):
                stab_states.append(psi)
    print(f"T1 two-qubit stabilizer states: {len(stab_states)} (expect 60)")
    assert len(stab_states) == 60

    rays = witting_rays()
    is_stab = []
    for r in rays:
        hit = any(abs(np.vdot(r, s))**2 > 1 - 1e-9 for s in stab_states)
        is_stab.append(hit)
    n_stab = sum(is_stab)
    print(f"T1 Witting rays that are stabilizer states: {n_stab} "
          f"(the 4 basis rays)")
    assert n_stab == 4 and all(is_stab[:4]) and not any(is_stab[4:])

    # T2: support lemma
    supports = sorted({int(np.sum(np.abs(s) > 1e-9)) for s in stab_states})
    print(f"T2 stabilizer-state supports: {supports} (never 3)")
    assert 3 not in supports
    assert all(int(np.sum(np.abs(r) > 1e-9)) == 3 for r in rays[4:])
    print("T2 all 36 omega-rays have support 3 => MAGIC automatically")

    # T3: stabilizer fidelity of the magic rays - THREE MAGIC GRADES
    from collections import Counter
    grade_of = {}
    for idx, r in enumerate(rays):
        if idx < 4:
            continue
        F = round(max(abs(np.vdot(r, s))**2 for s in stab_states), 6)
        grade_of[idx] = F
    grades = Counter(grade_of.values())
    deep = round((2 + np.sqrt(3)) / 6, 6)
    mid = round((5 + 2 * np.sqrt(3)) / 12, 6)
    shallow = 0.75
    print(f"T3 THREE MAGIC GRADES among the 36 rays:")
    print(f"   deep    F = (2+sqrt3)/6  = {deep}:  {grades[deep]} rays = 2^q")
    print(f"   mid     F = (5+2sqrt3)/12 = {mid}: {grades[mid]} rays = f")
    print(f"   shallow F = 3/4 = q/mu (Werner!):   {grades[shallow]} rays = mu")
    assert grades == Counter({deep: 8, mid: 24, shallow: 4})

    # T4: the triality on contexts
    orth = [[abs(np.vdot(rays[i], rays[j])) < 1e-9 for j in range(40)]
            for i in range(40)]
    contexts = [c for c in combinations(range(40), 4)
                if all(orth[i][j] for i, j in combinations(c, 2))]
    assert len(contexts) == 40
    profile = {}
    for c in contexts:
        k = sum(1 for r in c if is_stab[r])
        profile[k] = profile.get(k, 0) + 1
    print(f"T4 contexts by stabilizer-ray count: "
          f"{dict(sorted(profile.items(), reverse=True))}")
    assert profile == {4: 1, 1: 12, 0: 27}
    print("T4 TRIALITY: magic strata = entanglement strata (BT817) =")
    print("   holonet split (BT812): 1 classical + 12 interface + 27")
    print("   fully-magic contexts.  MATTER = MAGIC: the substrate's")
    print("   matter shell is exactly its non-classical resource sector.")

    # T5: THE CUBE INSIDE THE MAGIC - grade signatures of the 27
    sig_count = Counter()
    for c in contexts:
        if any(r < 4 for r in c):
            continue
        sig = tuple(sorted(grade_of[r] for r in c))
        sig_count[sig] += 1
    census = sorted(sig_count.values())
    print(f"\nT5 grade signatures of the 27 fully-magic contexts: "
          f"{census}")
    assert census == [1, 6, 8, 12]
    print("T5 THE CUBE CELL CENSUS: 27 = 1 + 8 + 12 + 6")
    print("   (body + vertices + edges + faces of the cube = 3^3).")
    print("   signature dictionary:")
    print("     shallow^4 (all 3/4)        x 1   = the body")
    print("     mid^3 shallow              x 8   = the vertices")
    print("     deep^2 mid^2               x 12  = the edges")
    print("     mid^4                      x 6   = the faces")
    print("   The involution cube (BT773) reappears INSIDE the magic")
    print("   structure of the matter shell: 27 = 3^3 as cube cells.")

    out = {
        "theorem": "BT822 magic census: matter = magic",
        "stabilizer_states": 60,
        "stabilizer_rays": 4,
        "magic_rays": 36,
        "stab_supports": supports,
        "magic_grades": {"deep_(2+sqrt3)/6": 8,
                         "mid_(5+2sqrt3)/12": 24,
                         "shallow_3/4_werner": 4},
        "cube_census_27": [1, 8, 12, 6],
        "context_magic_strata": {str(k): v for k, v in profile.items()},
        "triality": "holonet = entanglement = magic (rays and contexts)",
    }
    with open("data/bt822_magic_census.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt822_magic_census.json")


if __name__ == "__main__":
    main()
