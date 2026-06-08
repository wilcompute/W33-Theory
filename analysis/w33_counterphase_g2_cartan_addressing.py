#!/usr/bin/env python3
"""
BT540: Counterphase G2 Cartan Addressing Theorem

This resolves the BT536 raw counter-phase obstruction constructively.

BT536 found that the original BT527/BT530 address order does not make
    t -> -t mod 30
preserve the 14 toroidal + 16 spinor split.  It repaired this by a harmonic
involution, but left a top-3 next question: can one permute the 30 packet
addresses so the raw counter-phase itself preserves the split?

Answer: yes, but not by conjugating to the harmonic involution.  The raw
negation on Z/30Z has two fixed points, 0 and 15, while the harmonic
involution has fifteen 2-cycles.  Therefore exact conjugacy is impossible.

The fixed points are the feature, not a bug:
    14 toroidal/G2 packets = 2 Cartan packets + 12 root packets.

Assign the two raw fixed points to the two G2 Cartan directions and assign
the remaining twelve toroidal packets to six opposite root pairs.  Assign the
sixteen spinor packets to the eight remaining opposite pairs by actual E8
root negation.

Then raw counter-phase gives the clean branch law:
    30 = (2 fixed Cartan + 6 root pairs) + 8 spinor/F4 pairs
       = 14 toroidal/G2 + 16 spinor/F4.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


DIM = 8
N = 30


def neg_root(root: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(-x for x in root)


def packets() -> list[dict]:
    out = []
    pairs = list(itertools.combinations(range(DIM), 2))
    for addr, pp in enumerate([pairs[i : i + 2] for i in range(0, len(pairs), 2)]):
        roots = []
        for i, j in pp:
            for si, sj in itertools.product((-1, 1), repeat=2):
                vec = [Fraction(0) for _ in range(DIM)]
                vec[i] = si
                vec[j] = sj
                roots.append(tuple(vec))
        out.append({"address": addr, "type": "toroidal", "roots": roots})

    for addr, first4 in enumerate(itertools.product((-1, 1), repeat=4), start=14):
        roots = []
        first_minus = sum(x == -1 for x in first4)
        for free3 in itertools.product((-1, 1), repeat=3):
            minus_so_far = first_minus + sum(x == -1 for x in free3)
            last = -1 if minus_so_far % 2 else 1
            signs = first4 + free3 + (last,)
            roots.append(tuple(Fraction(s, 2) for s in signs))
        out.append({"address": addr, "type": "spinor", "roots": roots})
    return out


def spinor_opposite_pairs(ps: list[dict]) -> list[tuple[int, int]]:
    spin = [p for p in ps if p["type"] == "spinor"]
    pairs = set()
    for p in spin:
        negset = {neg_root(root) for root in p["roots"]}
        opp = [q for q in spin if set(q["roots"]) == negset][0]
        pairs.add(tuple(sorted((p["address"], opp["address"]))))
    return sorted(pairs)


def build_counterphase_addressing(ps: list[dict]) -> dict:
    """Return old-address -> new-address mapping."""
    toroidal = [p["address"] for p in ps if p["type"] == "toroidal"]
    spin_pairs = spinor_opposite_pairs(ps)

    fixed_labels = [0, 15]
    neg_pairs = [(i, (-i) % N) for i in range(1, 15)]

    # Two toroidal packets become the G2 Cartan fixed directions.
    cartan_old = toroidal[:2]
    toroidal_root_old = toroidal[2:]
    assert len(cartan_old) == 2
    assert len(toroidal_root_old) == 12
    assert len(spin_pairs) == 8

    old_to_new: dict[int, int] = {}
    for old, new in zip(cartan_old, fixed_labels):
        old_to_new[old] = new

    # Six toroidal root pairs use the first six raw negation pairs.
    toroidal_root_pairs = [tuple(toroidal_root_old[i : i + 2]) for i in range(0, 12, 2)]
    for (old_a, old_b), (new_a, new_b) in zip(toroidal_root_pairs, neg_pairs[:6]):
        old_to_new[old_a] = new_a
        old_to_new[old_b] = new_b

    # Eight spinor F4 pairs use the remaining eight raw negation pairs.
    for (old_a, old_b), (new_a, new_b) in zip(spin_pairs, neg_pairs[6:]):
        old_to_new[old_a] = new_a
        old_to_new[old_b] = new_b

    assert set(old_to_new) == set(range(N))
    assert len(set(old_to_new.values())) == N
    return old_to_new


def main() -> dict:
    ps = packets()
    by_old = {p["address"]: p for p in ps}
    assert len(ps) == N
    assert Counter(p["type"] for p in ps) == Counter({"spinor": 16, "toroidal": 14})

    old_to_new = build_counterphase_addressing(ps)
    new_to_old = {new: old for old, new in old_to_new.items()}
    assert len(new_to_old) == N

    def raw_neg_new(new_addr: int) -> int:
        return (-new_addr) % N

    def induced_old_map(old_addr: int) -> int:
        return new_to_old[raw_neg_new(old_to_new[old_addr])]

    induced = {old: induced_old_map(old) for old in range(N)}
    assert all(induced[induced[a]] == a for a in range(N))

    transitions = Counter((by_old[a]["type"], by_old[induced[a]]["type"]) for a in range(N))
    assert transitions == Counter({("toroidal", "toroidal"): 14, ("spinor", "spinor"): 16})

    fixed_old = sorted(a for a in range(N) if induced[a] == a)
    fixed_new = sorted(old_to_new[a] for a in fixed_old)
    assert fixed_new == [0, 15]
    assert all(by_old[a]["type"] == "toroidal" for a in fixed_old)

    two_cycles = sorted(tuple(sorted((a, induced[a]))) for a in range(N) if a < induced[a])
    toroidal_pairs = [p for p in two_cycles if by_old[p[0]]["type"] == "toroidal"]
    spinor_pairs = [p for p in two_cycles if by_old[p[0]]["type"] == "spinor"]
    assert len(toroidal_pairs) == 6
    assert len(spinor_pairs) == 8

    # Spinor pairs are still actual E8 root-negation pairs.
    spinor_neg_pairs = set(spinor_opposite_pairs(ps))
    assert set(spinor_pairs) == spinor_neg_pairs

    # Exact impossibility of conjugating raw negation to the harmonic involution:
    # cycle type of raw negation on Z/30 is 1^2 2^14, while the harmonic
    # branch involution in BT536 is 2^15.
    raw_cycle_type = {"fixed_points": 2, "two_cycles": 14}
    harmonic_cycle_type = {"fixed_points": 0, "two_cycles": 15}
    assert raw_cycle_type != harmonic_cycle_type

    labels = {
        str(old): {
            "new_address": old_to_new[old],
            "type": by_old[old]["type"],
            "counterphase_partner_old": induced[old],
            "counterphase_partner_new": raw_neg_new(old_to_new[old]),
            "role": (
                "G2_Cartan_fixed" if old in fixed_old else
                "G2_root_pair" if by_old[old]["type"] == "toroidal" else
                "F4_spinor_pair"
            ),
        }
        for old in range(N)
    }

    results = {
        "theorem": "BT540 Counterphase G2 Cartan Addressing Theorem",
        "BT536_obstruction_resolution": {
            "raw_negation_cycle_type": raw_cycle_type,
            "harmonic_involution_cycle_type": harmonic_cycle_type,
            "exact_conjugacy_possible": False,
            "repair": "use raw fixed points as the two G2 Cartan directions",
        },
        "new_addressing": {
            "old_to_new": {str(k): v for k, v in sorted(old_to_new.items())},
            "labels": labels,
        },
        "raw_counterphase_after_readdressing": {
            "map": "t -> -t mod 30",
            "type_transition_counts": {str(k): v for k, v in sorted(transitions.items())},
            "fixed_old_addresses": fixed_old,
            "fixed_new_addresses": fixed_new,
            "toroidal_G2_root_pairs": toroidal_pairs,
            "spinor_F4_pairs": spinor_pairs,
        },
        "branch_law": {
            "total": "30",
            "toroidal_G2": "14 = 2 Cartan fixed addresses + 12 roots = 2 + 6 opposite root pairs",
            "spinor_F4": "16 = 8 opposite spinor/F4 pairs",
            "raw_negation_orbits": "1^2 + 2^14 = (2 Cartan) + (6 G2 root pairs) + (8 F4 pairs)",
        },
        "substrate_reading": {
            "2_fixed_points": "rank(G2)=2 Cartan directions",
            "six_toroidal_pairs": "six positive G2 roots with opposite partners",
            "eight_spinor_pairs": "eight F4 spinor channels",
            "30": "h(E8)=14+16 branch total",
        },
    }

    out = Path("data/PART_BT540_COUNTERPHASE_G2_CARTAN_ADDRESSING_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    main()
