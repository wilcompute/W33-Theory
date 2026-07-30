#!/usr/bin/env python3
from __future__ import annotations
from fractions import Fraction
import sympy as sp
from w33_pass1320_1324_common import RelationAlgebra,fstr,NONCOMMUTATIVE_BLOCKS
def build_noncentral_matrix_units(alg: RelationAlgebra, decomposition: list[dict]) -> dict:
    multiplicities = {row["irrep"]: row["multiplicity"] for row in decomposition}
    all_units: dict[str, dict[tuple[int, int], list[Fraction]]] = {}
    blocks_json = {}

    for name, multiplicity in multiplicities.items():
        center = alg.central[name]
        if multiplicity == 1:
            all_units[name] = {(0, 0): center}
            blocks_json[name] = {
                "multiplicity": 1,
                "splitter": "central primitive idempotent",
                "matrix_units": {"0,0": [fstr(x) for x in center]},
            }
            continue

        raw_ideal = [alg.mul(center, e) for e in alg.std]
        ideal_basis = alg.independent_basis(raw_ideal)
        assert len(ideal_basis) == multiplicity * multiplicity
        coordinates = alg.coordinate_solver(ideal_basis)

        candidates = []
        for i in range(alg.r):
            symmetric = alg.add(alg.std[i], alg.std[alg.star_map[i]])
            candidate = alg.mul(center, symmetric)
            if any(candidate):
                candidates.append((f"A_{i}+A_{alg.star_map[i]}", candidate))
        initial = list(candidates[:16])
        for i in range(len(initial)):
            for j in range(i + 1, len(initial)):
                candidates.append((f"({initial[i][0]})+({initial[j][0]})", alg.add(initial[i][1], initial[j][1])))

        chosen = None
        for label, candidate in candidates:
            left = alg.left_matrix(candidate, ideal_basis, coordinates)
            eigenvalues = left.eigenvals()
            if (
                len(eigenvalues) == multiplicity
                and all(value.is_Rational for value in eigenvalues)
                and all(int(count) == multiplicity for count in eigenvalues.values())
            ):
                chosen = (label, candidate, eigenvalues)
                break
        assert chosen is not None, name
        splitter_label, splitter, eigenvalue_map = chosen
        eigenvalues = sorted(
            [Fraction(int(value.p), int(value.q)) for value in eigenvalue_map],
            key=float,
        )

        primitive = []
        for eigenvalue in eigenvalues:
            idem = list(center)
            for other in eigenvalues:
                if other == eigenvalue:
                    continue
                factor = alg.scale(
                    alg.sub(splitter, alg.scale(center, other)),
                    Fraction(1, 1) / (eigenvalue - other),
                )
                idem = alg.mul(idem, factor)
            assert alg.mul(idem, idem) == idem
            assert alg.star(idem) == idem
            primitive.append(idem)
        assert [sum(x[i] for x in primitive) for i in range(alg.r)] == center
        for i, idem in enumerate(primitive):
            rank = idem[alg.diag_label] * 432
            degree = next(row["degree"] for row in decomposition if row["irrep"] == name)
            assert rank == degree
            for other in primitive[i + 1 :]:
                assert alg.mul(idem, other) == alg.zero

        base = primitive[0]
        u = [base]
        v = [base]
        bridge_scales = [Fraction(1)]
        for i in range(1, multiplicity):
            target = primitive[i]
            bridge = None
            for trial in alg.std + ideal_basis:
                candidate = alg.mul(target, alg.mul(trial, base))
                if any(candidate):
                    bridge = candidate
                    break
            assert bridge is not None
            reverse = alg.star(bridge)
            product = alg.mul(reverse, bridge)
            anchor = next(j for j, value in enumerate(base) if value)
            alpha = product[anchor] / base[anchor]
            assert alpha > 0
            assert product == alg.scale(base, alpha)
            assert alg.mul(bridge, reverse) == alg.scale(target, alpha)
            u.append(bridge)
            v.append(alg.scale(reverse, Fraction(1, 1) / alpha))
            bridge_scales.append(alpha)

        units = {}
        for i in range(multiplicity):
            for j in range(multiplicity):
                units[(i, j)] = alg.mul(u[i], v[j])
        for i in range(multiplicity):
            for j in range(multiplicity):
                for k in range(multiplicity):
                    for l in range(multiplicity):
                        target = units[(i, l)] if j == k else alg.zero
                        assert alg.mul(units[(i, j)], units[(k, l)]) == target
        all_units[name] = units
        blocks_json[name] = {
            "multiplicity": multiplicity,
            "splitter": splitter_label,
            "splitter_eigenvalues": [fstr(x) for x in eigenvalues],
            "primitive_idempotent_ranks": [
                int(x[alg.diag_label] * 432) for x in primitive
            ],
            "bridge_scales": [fstr(x) for x in bridge_scales],
            "matrix_units": {
                f"{i},{j}": [fstr(x) for x in units[(i, j)]]
                for i in range(multiplicity)
                for j in range(multiplicity)
            },
        }

    ordered_basis = []
    ordered_labels = []
    for row in decomposition:
        name = row["irrep"]
        multiplicity = row["multiplicity"]
        for i in range(multiplicity):
            for j in range(multiplicity):
                ordered_basis.append(all_units[name][(i, j)])
                ordered_labels.append((name, i, j))
    assert len(ordered_basis) == 26
    coordinates = alg.coordinate_solver(ordered_basis)
    for index, basis_element in enumerate(ordered_basis):
        coordinate = coordinates(basis_element)
        assert coordinate == [Fraction(int(i == index)) for i in range(26)]

    return {
        "units": all_units,
        "ordered_basis": ordered_basis,
        "ordered_labels": ordered_labels,
        "coordinates": coordinates,
        "json": {
            "wedderburn_dimension": len(ordered_basis),
            "noncommutative_blocks": list(NONCOMMUTATIVE_BLOCKS),
            "blocks": blocks_json,
            "all_matrix_unit_laws_verified": True,
        },
    }


