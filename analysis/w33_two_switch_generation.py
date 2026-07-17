#!/usr/bin/env python3
"""
TINKER + TEST: do two abstract generators generate the finite gate group?

This is a finite group calculation.  The target is
Sp(4,3) = Aut(W(3,3)) (the two-qutrit Clifford group modulo Pauli, order 51840),
and the question is whether two named symplectic matrices generate it.  If they
do, a binary word in those generators reaches every group element.  Throughout
this file, a ``switch'' means an abstract selected group generator; the search
does not construct an optical braid, a worldline implementation, a clock, or a
hardware schedule.

The two natural switches:
  g1 = single-qutrit FOURIER on mode 1 (x) identity   (a one-mode gate -- the
       'tritter'/phase-plate switch),
  g2 = CONTROLLED-Z between the two modes              (the entangling switch).
On the symplectic phase space F_3^4 = (x1,x2,p1,p2) these are 4x4 matrices over
F_3. We verify that selected pairs are symplectic and enumerate their generated
subgroups, testing whether the order reaches |Sp(4,3)| = 51840.  A separate
compiler or hardware certificate would be required to assign these matrices to
physical switches or braids.
"""
from __future__ import annotations

import json

F = 3
# symplectic form J = [[0, I2],[-I2, 0]] over F_3 on (x1,x2,p1,p2)
J = [[0, 0, 1, 0],
     [0, 0, 0, 1],
     [2, 0, 0, 0],   # -1 = 2 mod 3
     [0, 2, 0, 0]]


def mm(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(4)) % F
                       for j in range(4)) for i in range(4))


def transpose(A):
    return tuple(tuple(A[j][i] for j in range(4)) for i in range(4))


def is_symplectic(M):
    # M^T J M == J
    MT = transpose(M)
    return mm(mm(MT, [list(r) for r in J]), M) == tuple(tuple(r) for r in J)


def gen_order(gens, cap=60000):
    I4 = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
    seen = {I4}
    frontier = [I4]
    while frontier:
        M = frontier.pop()
        for g in gens:
            N = mm(M, g)
            if N not in seen:
                seen.add(N)
                frontier.append(N)
        if len(seen) > cap:
            break
    return len(seen)


def main():
    sp43 = 51840
    # library of natural 'switch' gates on (x1,x2,p1,p2), all symplectic
    lib = {
        "F1": ((0, 0, 1, 0), (0, 1, 0, 0), (2, 0, 0, 0), (0, 0, 0, 1)),  # Fourier m1
        "F2": ((1, 0, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0), (0, 2, 0, 0)),  # Fourier m2
        "S1": ((1, 0, 0, 0), (0, 1, 0, 0), (1, 0, 1, 0), (0, 0, 0, 1)),  # phase m1 (p1+=x1)
        "S2": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 1, 0, 1)),  # phase m2 (p2+=x2)
        "CZ": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 1, 1, 0), (1, 0, 0, 1)),  # p1+=x2,p2+=x1
        "SUM": ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 2), (0, 0, 0, 1)),  # x2+=x1, p1-=p2
    }
    print("[switch library: all symplectic?]")
    for k, M in lib.items():
        ok = is_symplectic(M)
        print(f"  {k}: symplectic={ok}")
        assert ok, k

    # products give richer single 'switches' too
    prod = {
        "F1*F2": mm(lib["F1"], lib["F2"]),
        "F1*CZ": mm(lib["F1"], lib["CZ"]),
        "S1*CZ": mm(lib["S1"], lib["CZ"]),
        "F1*S2": mm(lib["F1"], lib["S2"]),
        "F1*SUM": mm(lib["F1"], lib["SUM"]),
        "F2*S1": mm(lib["F2"], lib["S1"]),
    }
    cand = {**lib, **prod}

    print("\n[search: which PAIRS of switches 2-generate Sp(4,3)=51840?]")
    names = list(cand.keys())
    winners = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            o = gen_order([cand[a], cand[b]])
            if o == sp43:
                winners.append((a, b))
    print(f"  found {len(winners)} two-switch generating pairs; examples:")
    for a, b in winners[:6]:
        print(f"    <{a}, {b}> = Sp(4,3) (order {sp43})")
    assert winners, "no 2-generating pair found among natural switches"

    a, b = winners[0]
    print(f"\n  minimal-activation pair: switch A = {a}, switch B = {b}")
    print("\nRESULT (tested, learned from a first NEGATIVE): the naive pair")
    print("  (Fourier-on-mode-1, CZ) only reaches a 108-element subgroup -- two")
    print("  switches are NOT automatically enough. But a search over natural")
    print(f"  switches finds {len(winners)} generating pairs: e.g. <{a},{b}>")
    print("  generates ALL of Sp(4,3) (51840 = the entire finite target). Thus")
    print("  two well-chosen abstract generators suffice: a binary word in them")
    print("  reaches every group element. The two switches must be a generating")
    print("  pair; the one-mode-gate + CZ naive choice is not. This establishes")
    print("  no physical braid, carrier, or timing interpretation.")

    out = {
        "result": "two well-chosen switches generate all of Sp(4,3)=51840",
        "naive_pair_F1_CZ_subgroup_order": gen_order([lib["F1"], lib["CZ"]]),
        "generating_pairs_found": len(winners),
        "example_generating_pairs": [f"<{a},{b}>" for a, b in winners[:8]],
        "minimal_activation_pair": f"<{a},{b}>",
        "Sp43_order": sp43,
        "interpretation": ("A binary word in two selected abstract symplectic "
                           "generators reaches every Sp(4,3) element exactly when "
                           "the pair generates the full group. The calculation "
                           "distinguishes generating pairs from F1+CZ, which has "
                           "order 108."),
        "hardware_boundary": ("No physical-switch, braid, carrier, clock, or "
                              "fault-tolerance implementation follows from this "
                              "finite subgroup-generation calculation."),
        "sources": ["Majorana braiding TQC (Nature Commun. 14, 2023); worldlines "
                    "of Majorana zero modes = the computational model",
                    "Sp(4,3) is 2-generated (finite group theory)"],
    }
    with open("data/w33_two_switch_generation.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/w33_two_switch_generation.json")


if __name__ == "__main__":
    main()
