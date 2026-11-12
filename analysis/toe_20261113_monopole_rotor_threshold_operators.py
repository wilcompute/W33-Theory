"""Check local operators for the split W33 monopole rotor thresholds."""

import argparse
from collections import Counter
from fractions import Fraction
import json
from math import factorial
from pathlib import Path

import toe_20261110_monopole_boundary_lattice as boundary
import toe_20261110_monopole_color_operators as color


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/toe_20261113_monopole_rotor_threshold_operators.json"


def perpendicular(weight, alpha, magnetic):
    pairing = sum(w * m for w, m in zip(weight, magnetic))
    assert pairing in (-1, 1)
    return tuple(2 * w - int(pairing) * a for w, a in zip(weight, alpha))


def grading(weights, alpha, magnetic):
    charges = Counter()
    for weight in weights:
        q = perpendicular(weight, alpha, magnetic)
        if any(q):
            opposite = boundary.negative(q)
            representative = max(q, opposite)
            charges[representative] += 1 if q == representative else -1
    return [(q, n) for q, n in sorted(charges.items()) if n]


def dotted_count(weights, magnetic):
    # Incoming particles annihilate through psi, outgoing particles create
    # through psi-dagger. Replacing a particle with its hole swaps the field.
    return sum(sum(w * m for w, m in zip(weight, magnetic)) == 1 for weight in weights)


def flavor_counts(layers, degree, target):
    char = layers[degree]
    labels = sorted({w[4:] for w in char if w[:4] == target})
    return [(label, n) for label in labels
            if (n := color.irrep_multiplicity(char.__getitem__, target + label))]


def phase_space(degree):
    coefficient = Fraction(1, factorial(degree - 1))
    return {"energy_power": degree - 1, "coefficient": str(coefficient)}


def analyze(signed_states, target, witnesses, direction, alpha, magnetic):
    single_grading = grading([target], alpha, magnetic)
    triples = []
    for witness in witnesses:
        assert tuple(map(sum, zip(*witness))) == target
        signature = grading(witness, alpha, magnetic)
        assert signature != single_grading
        dotted = dotted_count((*witness, target), magnetic)
        assert dotted == (1 if direction == "incoming" else 3)
        triples.append(dict(weights=witness, grading=signature,
                            undotted=4-dotted, dotted=dotted))

    layers = color.exterior_characters(signed_states, 5)
    flavors = {degree: flavor_counts(layers, degree, target) for degree in (1, 3, 5)}
    return dict(target=target, single_grading=single_grading, triple_witnesses=triples,
                formal_3B_L_singlet_counts=flavors,
                free_triple_phase_space=phase_space(3), free_quintet_phase_space=phase_space(5))


def pairing_from_grading(states, target, alpha, magnetic):
    coefficients = {}
    for state in states:
        weight = state[:4]
        q = perpendicular(weight, alpha, magnetic)
        assert any(q)
        sector, sign = grading([weight], alpha, magnetic)[0]
        pairing = int(sum(w * m for w, m in zip(weight, magnetic)))
        coefficient = pairing * sign
        assert coefficients.setdefault(sector, coefficient) == coefficient

    inferred = sum(coefficients[sector] * n for sector, n in grading([target], alpha, magnetic))
    target_pairing = int(sum(w * m for w, m in zip(target, magnetic)))
    assert inferred == -target_pairing
    compatible_weight = tuple(w + (inferred-target_pairing)*a//2 for w, a in zip(target, alpha))
    assert perpendicular(compatible_weight, alpha, magnetic) == perpendicular(target, alpha, magnetic)
    return dict(coefficients=sorted(coefficients.items()), target_pairing=target_pairing,
                inferred_pairing=inferred, compatible_weight=compatible_weight)


def calculate():
    fixture = json.loads((ROOT / "data/toe_20261113_monopole_triplet_charge.json")
                         .read_text(encoding="utf-8"))["exact_charge_ledger"]
    incoming, outgoing, alpha = color.flavor_weights()
    _, _, magnetic, _ = boundary.angular_weights()
    assert tuple(alpha) == tuple(fixture["rotor_root"])
    candidates = fixture["between_threshold_multiparticle_candidates"]
    results = {}
    for direction, states, key, expected in [
        ("incoming", incoming, "incoming_without_Hu_or_its_hole", [((0, 0), 9)]),
        ("outgoing", outgoing, "outgoing_without_a_rotor_step", [((1, 0), 3), ((1, 1), 9)]),
    ]:
        row = candidates[key]
        target = tuple(row["target_weight"])
        signed = states + [boundary.negative(w) for w in states]
        if direction == "incoming":
            hu_weights = (target, boundary.negative(target))
            assert [w for w in signed if w[:4] == target] == [target + (0, 0)]
            assert [w for w in signed if w[:4] == hu_weights[1]] == [hu_weights[1] + (0, 0)]
            signed = [w for w in signed if w[:4] not in hu_weights]
        witnesses = [tuple(map(tuple, group)) for group in row["unordered_weight_witnesses"]]
        result = analyze(signed, target, witnesses, direction, tuple(alpha), magnetic)
        assert result["formal_3B_L_singlet_counts"][1] == []
        assert result["formal_3B_L_singlet_counts"][3] == expected
        assert sum(count for _, count in expected) == row["residual_color_singlet_multiplicity"]
        result["pairing_from_quadratic_grading"] = pairing_from_grading(signed, target, tuple(alpha), magnetic)
        if direction == "incoming":
            pairing = result["pairing_from_quadratic_grading"]
            # On restoring Hu, its net occupation x changes the inferred pairing
            # from the restricted prediction by (n_Hu - n_inferred) * x.
            correction = pairing["target_pairing"] - pairing["inferred_pairing"]
            assert correction == -2
            result["net_Hu_required_at_fixed_weight"] = 1
            result["pairing_correction_per_net_Hu"] = correction
        results[key] = result

    counts = results["incoming_without_Hu_or_its_hole"]["formal_3B_L_singlet_counts"]
    assert dict(counts[5])[(0, -1)] == 27
    return dict(status="PASS", scope="unit-flux asymptotic modes and split rotor thresholds",
                rotor_root=tuple(alpha), results=results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    result = calculate()
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for key, row in result["results"].items():
        print(key, row["formal_3B_L_singlet_counts"],
              row["pairing_from_quadratic_grading"]["compatible_weight"])
