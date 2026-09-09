#!/usr/bin/env python3
"""Observer-information lattice for the retained-noise W33 timing toy model.

The target is a two-sample timing record O. Primitive side-information
generators are Y (final counter), S0 and S1 (two independent two-bit noise
cells). All eight observer states are enumerated with Shannon entropy,
guessing probability and conditional min-entropy.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_OBSERVER_INFORMATION_LATTICE.json"


def v2(n):
    k = 0
    while n and n % 2 == 0:
        n //= 2
        k += 1
    return k


def increment_trace(x):
    return tuple(3 + 2*v2(x + j + 1) for j in range(2))


def error_cell(z):
    return 2 * ((z & 1) + (z >> 1) - 1)


def observed(x, s0, s1):
    t0, t1 = increment_trace(x)
    return (t0 + error_cell(s0), t1 + error_cell(s1))


def sample_space():
    rows = []
    for x in range(8):
        y = x + 2
        for s0 in range(4):
            for s1 in range(4):
                rows.append({"O": observed(x, s0, s1), "Y": y, "S0": s0, "S1": s1})
    assert len(rows) == 128
    return rows


def entropy(counter):
    total = sum(counter.values())
    return -sum((n/total) * math.log2(n/total) for n in counter.values() if n)


def conditional_entropy(rows, target, side):
    joint, marginal = Counter(), Counter()
    for row in rows:
        skey = tuple(row[s] for s in side)
        joint[(row[target], skey)] += 1
        marginal[skey] += 1
    return entropy(joint) - entropy(marginal)


def guess_probability(rows, target, side):
    groups = {}
    for row in rows:
        skey = tuple(row[s] for s in side)
        groups.setdefault(skey, Counter())[row[target]] += 1
    return Fraction(sum(max(c.values()) for c in groups.values()), len(rows))


def powerset(items):
    out = []
    for r in range(len(items) + 1):
        out.extend(combinations(items, r))
    return out


def verify():
    rows = sample_space()
    generators = ("Y", "S0", "S1")
    lattice = []
    by_key = {}
    for side in powerset(generators):
        h = conditional_entropy(rows, "O", side)
        pguess = guess_probability(rows, "O", side)
        hmin = -math.log2(float(pguess))
        key = "+".join(side) if side else "EMPTY"
        row = {
            "observer_state": key,
            "side_information": list(side),
            "H_O_given_side_bits": h,
            "P_guess_O_given_side": str(pguess),
            "Hmin_O_given_side_bits": hmin,
        }
        lattice.append(row)
        by_key[frozenset(side)] = row

    edges = []
    for a in by_key:
        for g in generators:
            if g in a:
                continue
            b = frozenset(set(a) | {g})
            ra, rb = by_key[a], by_key[b]
            assert rb["H_O_given_side_bits"] <= ra["H_O_given_side_bits"] + 1e-12
            assert rb["Hmin_O_given_side_bits"] <= ra["Hmin_O_given_side_bits"] + 1e-12
            edges.append({
                "from": ra["observer_state"],
                "to": rb["observer_state"],
                "delta_H_bits": ra["H_O_given_side_bits"] - rb["H_O_given_side_bits"],
                "delta_Hmin_bits": ra["Hmin_O_given_side_bits"] - rb["Hmin_O_given_side_bits"],
            })

    assert abs(by_key[frozenset({"Y"})]["H_O_given_side_bits"] - 3.0) < 1e-12
    assert abs(by_key[frozenset({"Y", "S0"})]["H_O_given_side_bits"] - 1.5) < 1e-12
    assert abs(by_key[frozenset({"Y", "S1"})]["H_O_given_side_bits"] - 1.5) < 1e-12
    assert by_key[frozenset(generators)]["H_O_given_side_bits"] == 0.0
    assert by_key[frozenset(generators)]["P_guess_O_given_side"] == "1"

    decryptability_distance = {}
    for state in by_key:
        available = [g for g in generators if g not in state]
        for r in range(4):
            hit = False
            for extra in combinations(available, r):
                target = frozenset(set(state) | set(extra))
                if abs(by_key[target]["H_O_given_side_bits"]) < 1e-12:
                    decryptability_distance[by_key[state]["observer_state"]] = r
                    hit = True
                    break
            if hit:
                break

    return {
        "schema": "w33.observer-information-lattice.v1",
        "status": "PASS",
        "target": "two-sample timing record O",
        "primitive_generators": list(generators),
        "lattice": lattice,
        "cover_edges": edges,
        "decryptability_distance_in_generators": decryptability_distance,
        "key_identity": "H(O|I)-H(O|I,K)=I(O;K|I)",
        "core_result": (
            "The same record has different randomness profiles for different observers. "
            "With Y alone H(O|Y)=3 bits; each independent seed cell removes 1.5 bits; "
            "Y+S0+S1 makes the record exactly decryptable."
        ),
        "boundary": (
            "These are exact finite information-theory values for the retained-noise model; "
            "they do not by themselves measure computational hardness or quantum adversary side information."
        ),
    }


if __name__ == "__main__":
    result = verify()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
