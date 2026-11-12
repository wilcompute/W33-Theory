"""Check integer rotor sea flow and finite-inertia Gaussian dressing in W33."""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import json
from pathlib import Path

import sympy as sp

import toe_20261113_monopole_rotor_threshold_operators as threshold


OUT = threshold.ROOT / "data/toe_20261113_monopole_rotor_sea_flow.json"


def signed_frames(states, alpha, magnetic):
    sums = Counter()
    frames = defaultdict(list)
    for state in states:
        weight = state[:4]
        sector, sign = threshold.grading([weight], alpha, magnetic)[0]
        sums[sector] += sign
        # Orient both radial directions to q = sector, conjugating when needed.
        frames[sector].append(sign * int(sum(w * m for w, m in zip(weight, magnetic))))
    return sums, frames


def sector_flow(incoming, outgoing, alpha, magnetic):
    inc_sums, inc_frames = signed_frames(incoming, alpha, magnetic)
    out_sums, out_frames = signed_frames(outgoing, alpha, magnetic)
    assert inc_frames.keys() == out_frames.keys()
    rows = []
    for sector in sorted(inc_frames):
        inc = sorted(inc_frames[sector])
        out = sorted(out_frames[sector])
        assert len(inc) == len(out)
        bulk = Fraction(inc_sums[sector] + out_sums[sector], 2)
        determinant = Fraction(sum(inc) - sum(out), 2)
        assert bulk.denominator == 1 and determinant == -bulk
        rows.append(dict(sector=sector, incoming_pairings=inc, outgoing_pairings=out,
                         covariant_bulk_flow=int(bulk), rotor_determinant_winding=int(determinant)))
    flow = {row["sector"]: row["covariant_bulk_flow"] for row in rows}
    assert sorted(flow.values()) == [-3, -3, 0, 0, 0, 3, 3]
    assert all(sum(sector[i] * n for sector, n in flow.items()) == 0 for i in range(4))
    return rows, flow


def integer_winding_check(flow):
    cases = json.loads(threshold.OUT.read_text(encoding="utf-8"))["results"]
    out = {}
    for name, case in cases.items():
        pairing = case["pairing_from_quadratic_grading"]
        coefficients = {tuple(sector): n for sector, n in pairing["coefficients"]}
        units_per_turn = sum(coefficients[sector] * n for sector, n in flow.items())
        deficit = pairing["target_pairing"] - pairing["inferred_pairing"]
        required_turns = Fraction(deficit, units_per_turn)
        assert required_turns == Fraction(1, 6)
        assert all((required_turns * n).denominator == 2 for n in flow.values() if n)
        single = {tuple(sector): n for sector, n in case["single_grading"]}
        for witness in case["triple_witnesses"]:
            diff = Counter({tuple(sector): n for sector, n in witness["grading"]})
            diff.subtract(single)
            # Each explicit witness changes a sector with zero bulk anomaly.
            assert any(n and not flow[sector] for sector, n in diff.items())
        out[name] = dict(pairing_deficit=deficit, pairing_units_per_full_turn=units_per_turn,
                         hypothetical_turns_required_by_pairing_alone=str(required_turns))
    return out


def sources(insertions):
    """Each term is a signed coefficient at an independent retarded time."""
    a, b = Counter(), Counter()
    for side, step, sign, time, dress_time in insertions:
        (a if side == "out" else b)[time] += step * sign
        if dress_time is not None:
            assert side == "out"
            a[dress_time] -= step * sign
            b[dress_time] += step * sign
    return dict(A=sorted((k, n) for k, n in a.items() if n),
                B=sorted((k, n) for k, n in b.items() if n))


def gaussian_checks():
    charge_ledger = threshold.ROOT / "data/toe_20261113_monopole_triplet_charge.json"
    steps = json.loads(charge_ledger.read_text(encoding="utf-8"))["exact_charge_ledger"]["rotor_steps"]
    assert steps == [1, 1, 1, 0]
    result = {}
    for step in sorted(set(steps)):
        for first in ("in", "out"):
            for second in ("in", "out"):
                insertions = [(first, step, 1, "s1", "s1" if first == "out" else None),
                              (second, step, -1, "s2", "s2" if second == "out" else None)]
                result[f"step_{step}_{first}_{second}"] = sources(insertions)
    assert all(not pair["A"] for pair in result.values())
    control = sources([("out", 1, 1, "s1", "offset"), ("in", 1, -1, "s2", None)])
    assert control["A"] and control["B"]
    return dict(triplet_steps=steps, dressed_sources=result, mistimed_control=control,
                gaussian_correction="1 for all dressed rows, including nonzero oscillator inertia")


def boundary_twists(flow, alpha, magnetic):
    path = threshold.ROOT / threshold.boundary.OUT
    fixture = json.loads(path.read_text(encoding="utf-8"))
    incoming = fixture["incoming_signed_pair_order"]
    outgoing = threshold.boundary.columns(fixture["outgoing_particle_order"])
    assert (magnetic.T * sp.Matrix(alpha))[0] == 2
    gluing = fixture["exact_abelian_gluing"]
    results = {}
    for name, candidate in gluing.items():
        block = candidate["block_indices_zero_based"][0]
        normal = sp.zeros(len(incoming), 1)
        for i in block:
            normal[i] = 1
        shift = 2 * normal / normal.dot(normal)
        reflection = threshold.boundary.reflection(block)
        assert reflection[:, block[0]] == sp.eye(len(incoming))[:, block[0]] - shift
        assert reflection.T * reflection == sp.eye(len(incoming))
        order = int(sp.ilcm(1, *(x.q for x in shift)))

        for candidate_block in candidate["block_indices_zero_based"]:
            assert len(candidate_block) == len(block)
            lifted_charge = sum((outgoing[:, i] for i in candidate_block), sp.zeros(4, 1))
            assert lifted_charge * sp.Rational(2, len(block)) == sp.Matrix(alpha)
            sector_shift = Counter()
            for index in candidate_block:
                sector, sign = threshold.grading([incoming[index]], alpha, magnetic)[0]
                sector_shift[sector] += sign * sp.Rational(2, len(block))
            assert all(sector_shift[sector] == Fraction(n, 6) for sector, n in flow.items())

        # Free fermion bosonization with each unit vertex of weight 1/2.
        # Minimize the norm in each unconstrained occupation coset.
        weights = []
        for k in range(order):
            representative = [k*x - sp.floor(k*x + sp.Rational(1, 2)) for x in shift]
            weights.append(str(sum(x*x for x in representative) / 2))
        results[name] = dict(one_block_order=order, nonzero_slots=len(block),
                             one_block_twist_coset_weights=weights,
                             first_twist_weight_at_charge_alpha=weights[1],
                             first_twist_cartan_charge=tuple(alpha),
                             shift_by_sector=sorted((s, str(n)) for s, n in sector_shift.items()))
    assert results["collective"]["one_block_twist_coset_weights"] == ["0", "1/6", "2/3", "3/2", "2/3", "1/6"]
    assert results["family"]["one_block_twist_coset_weights"] == ["0", "1/2"]
    return results


def calculate():
    incoming, outgoing, alpha = threshold.color.flavor_weights()
    _, _, magnetic, _ = threshold.boundary.angular_weights()
    sectors, flow = sector_flow(incoming, outgoing, alpha, magnetic)
    return dict(status="PASS", sectors=sectors, compact_integer_flow=integer_winding_check(flow),
                noncompact_gaussian_oscillator=gaussian_checks(),
                boundary_twist_candidates=boundary_twists(flow, alpha, magnetic))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    result = calculate()
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Full-turn coefficients:", [row["covariant_bulk_flow"] for row in result["sectors"]])
    print("Compact integer-flow checks:", result["compact_integer_flow"])
    print("Finite-inertia Gaussian source checks:", len(result["noncompact_gaussian_oscillator"]["dressed_sources"]))
