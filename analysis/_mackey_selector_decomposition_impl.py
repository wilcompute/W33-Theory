#!/usr/bin/env python3
"""Passes 1375--1379: exact Mackey decomposition of the selector stabilizer.

The literal 120-selector permutation action is used to reconstruct
H=C3^3:(D8xC2), its complete little-group character table, the exact
permutation-character decomposition, the fourteen orbital central projectors,
and their 14->10 Terwilliger fusion.  Cyclotomic arithmetic is exact in
Z[omega], omega^2+omega+1=0.  No database character table or floating
spectral calculation is used.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
import math
import random
import sys
from pathlib import Path

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from pass1370_1374 import core

DEFAULT_OUT = ROOT / "data" / "w33_pass1375_1379_mackey_selector_decomposition.json"

# a+b*w with w^2=-1-w.
def zadd(x, y): return (x[0] + y[0], x[1] + y[1])
def zscale(n, x): return (n * x[0], n * x[1])
def zconj(x): return (x[0] - x[1], -x[1])
def zmul(x, y):
    a, b = x; c, d = y
    return (a*c-b*d, a*d+b*c-b*d)
ZETA = ((1, 0), (0, 1), (-1, -1))


def analyze():
    g = core.add_orbital_and_T(core.build())
    H = sorted(g["H"])
    identity = tuple(range(120))

    def compose(p, q): return tuple(p[q[i]] for i in range(len(p)))
    def inverse(p):
        out = [0] * len(p)
        for i, j in enumerate(p): out[j] = i
        return tuple(out)
    def order(p):
        seen = [False] * len(p); out = 1
        for i in range(len(p)):
            if seen[i]: continue
            j = i; length = 0
            while not seen[j]:
                seen[j] = True; length += 1; j = p[j]
            out = math.lcm(out, length)
        return out
    def closure(gens):
        seen = {identity}; queue = collections.deque([identity])
        while queue:
            x = queue.popleft()
            for a in gens:
                y = compose(a, x)
                if y not in seen: seen.add(y); queue.append(y)
        return seen
    def power(x, exponent):
        out = identity
        for _ in range(exponent): out = compose(out, x)
        return out

    orders = {h: order(h) for h in H}
    N = {h for h in H if orders[h] in (1, 3)}
    assert len(N) == 27
    assert all(compose(a, b) == compose(b, a) for a in N for b in N)

    two = [h for h in H if orders[h] in (2, 4, 8, 16)]
    K = None; rng = random.Random(1375)
    for _ in range(10000):
        candidate = closure(rng.sample(two, 3))
        if len(candidate) == 16 and candidate & N == {identity}:
            K = candidate; break
    if K is None:
        for a, b in itertools.combinations(two, 2):
            candidate = closure([a, b])
            if len(candidate) == 16 and candidate & N == {identity}:
                K = candidate; break
    assert K is not None
    K = sorted(K)

    n_basis = []; generated = {identity}
    for x in sorted(N):
        if x not in generated:
            n_basis.append(x); generated = closure(n_basis)
        if len(generated) == 27: break
    assert len(n_basis) == 3
    vec_to_n = {}; n_to_vec = {}
    for vector in itertools.product(range(3), repeat=3):
        x = identity
        for exponent, basis in zip(vector, n_basis):
            x = compose(x, power(basis, exponent))
        vec_to_n[vector] = x; n_to_vec[x] = vector
    assert len(n_to_vec) == 27

    matrices = {}
    for k in K:
        ki = inverse(k)
        columns = [n_to_vec[compose(compose(k, b), ki)] for b in n_basis]
        matrices[k] = np.array(columns, dtype=np.int64).T % 3
    assert len({tuple(matrix.reshape(-1)) for matrix in matrices.values()}) == 16

    h_coordinates = {}
    for k in K:
        for vector, n in vec_to_n.items():
            h = compose(n, k)
            assert h not in h_coordinates
            h_coordinates[h] = (vector, k)
    assert set(h_coordinates) == set(H)

    # Concrete D8 x C2 coordinates on K.
    r = s = None
    for rr in K:
        if order(rr) != 4: continue
        for ss in K:
            if order(ss) == 2 and compose(compose(ss, rr), ss) == inverse(rr):
                if len(closure([rr, ss])) == 8:
                    r, s = rr, ss; break
        if r is not None: break
    assert r is not None
    D = closure([r, s])
    center_K = [x for x in K if all(compose(x, y) == compose(y, x) for y in K)]
    t = next(x for x in center_K if order(x) == 2 and x not in D and len(closure([r, s, x])) == 16)
    K_coordinates = {}
    for a in range(4):
        for b in range(2):
            for c in range(2):
                x = compose(power(r, a), compose(power(s, b), power(t, c)))
                assert x not in K_coordinates
                K_coordinates[x] = (a, b, c)
    assert set(K_coordinates) == set(K)

    def dual_action(k, covector):
        return tuple(int(x) for x in (matrices[inverse(k)].T @ np.array(covector, dtype=np.int64)) % 3)

    unseen = set(itertools.product(range(3), repeat=3)); dual_orbits = []
    while unseen:
        representative = min(unseen)
        orbit = {dual_action(k, representative) for k in K}
        dual_orbits.append((representative, orbit)); unseen -= orbit
    dual_orbits.sort(key=lambda item: (len(item[1]), item[0]))
    assert [len(orbit) for _rep, orbit in dual_orbits] == [1, 2, 4, 4, 8, 8]

    def subgroup_type(subgroup):
        census = collections.Counter(order(x) for x in subgroup)
        expected = {
            16: collections.Counter({1: 1, 2: 11, 4: 4}),
            8: collections.Counter({1: 1, 2: 5, 4: 2}),
            4: collections.Counter({1: 1, 2: 3}),
            2: collections.Counter({1: 1, 2: 1}),
            1: collections.Counter({1: 1}),
        }
        assert census == expected[len(subgroup)]
        return {16: "D8xC2", 8: "D8", 4: "V4", 2: "C2", 1: "1"}[len(subgroup)]

    def d8_coordinates(subgroup):
        subgroup = set(subgroup); rr = ss = None
        for candidate_r in subgroup:
            if order(candidate_r) != 4: continue
            for candidate_s in subgroup:
                if order(candidate_s) == 2 and compose(compose(candidate_s, candidate_r), candidate_s) == inverse(candidate_r):
                    if closure([candidate_r, candidate_s]) == subgroup:
                        rr, ss = candidate_r, candidate_s; break
            if rr is not None: break
        assert rr is not None
        coordinates = {}
        for a in range(4):
            for b in range(2): coordinates[compose(power(rr, a), power(ss, b))] = (a, b)
        assert set(coordinates) == subgroup
        return coordinates

    def elementary_coordinates(subgroup):
        subgroup = set(subgroup); basis = []; generated = {identity}
        for x in sorted(subgroup - {identity}):
            if x not in generated:
                basis.append(x); generated = closure(basis)
            if len(generated) == len(subgroup): break
        rank = int(round(math.log2(len(subgroup))))
        assert len(basis) == rank
        coordinates = {}
        for vector in itertools.product(range(2), repeat=rank):
            x = identity
            for exponent, b in zip(vector, basis):
                if exponent: x = compose(x, b)
            coordinates[x] = vector
        assert set(coordinates) == subgroup
        return coordinates

    def little_characters(stabilizer):
        stabilizer = set(stabilizer); kind = subgroup_type(stabilizer); records = []
        if kind == "D8xC2":
            for alpha, beta, gamma in itertools.product(range(2), repeat=3):
                def character(x, alpha=alpha, beta=beta, gamma=gamma):
                    a, b, c = K_coordinates[x]
                    return -1 if (alpha*(a % 2)+beta*b+gamma*c) % 2 else 1
                records.append((f"lin_{alpha}{beta}{gamma}", 1, character))
            for gamma in range(2):
                def character(x, gamma=gamma):
                    a, b, c = K_coordinates[x]
                    value = 0 if b or a in (1, 3) else (2 if a == 0 else -2)
                    return value * (-1 if gamma*c % 2 else 1)
                records.append((f"std_{gamma}", 2, character))
        elif kind == "D8":
            coordinates = d8_coordinates(stabilizer)
            for alpha, beta in itertools.product(range(2), repeat=2):
                def character(x, alpha=alpha, beta=beta):
                    a, b = coordinates[x]
                    return -1 if (alpha*(a % 2)+beta*b) % 2 else 1
                records.append((f"lin_{alpha}{beta}", 1, character))
            def standard(x):
                a, b = coordinates[x]
                return 0 if b or a in (1, 3) else (2 if a == 0 else -2)
            records.append(("std", 2, standard))
        else:
            coordinates = elementary_coordinates(stabilizer)
            rank = len(next(iter(coordinates.values())))
            for dual in itertools.product(range(2), repeat=rank):
                def character(x, dual=dual):
                    return -1 if sum(a*b for a, b in zip(dual, coordinates[x])) % 2 else 1
                records.append(("lin_" + "".join(map(str, dual)), 1, character))
        assert sum(degree*degree for _label, degree, _char in records) == len(stabilizer)
        return kind, records

    def coset_reps(stabilizer):
        unseen = set(K); out = []
        while unseen:
            x = min(unseen); out.append(x); unseen -= {compose(x, y) for y in stabilizer}
        return out

    irreducibles = []
    for orbit_index, (covector, orbit) in enumerate(dual_orbits):
        stabilizer = {k for k in K if dual_action(k, covector) == covector}
        kind, little = little_characters(stabilizer); reps = coset_reps(stabilizer)
        assert len(stabilizer)*len(orbit) == 16 and len(reps) == len(orbit)
        for little_label, little_degree, tau in little:
            values = []
            for h in H:
                vector, k = h_coordinates[h]; total = (0, 0)
                for x in reps:
                    xi = inverse(x); conjugate_k = compose(compose(xi, k), x)
                    if conjugate_k not in stabilizer: continue
                    transformed = matrices[xi] @ np.array(vector, dtype=np.int64) % 3
                    exponent = sum(covector[i]*int(transformed[i]) for i in range(3)) % 3
                    total = zadd(total, zscale(tau(conjugate_k), ZETA[exponent]))
                values.append(total)
            degree = len(orbit)*little_degree
            assert values[H.index(identity)] == (degree, 0)
            irreducibles.append({
                "orbit_index": orbit_index, "orbit_size": len(orbit), "covector": list(covector),
                "stabilizer_order": len(stabilizer), "stabilizer_type": kind,
                "little_label": little_label, "little_degree": little_degree,
                "degree": degree, "values": values,
            })

    assert len(irreducibles) == 27
    assert sum(record["degree"]**2 for record in irreducibles) == 432

    def inner(left, right):
        total = (0, 0)
        for a, b in zip(left, right): total = zadd(total, zmul(a, zconj(b)))
        assert total[0] % 432 == 0 and total[1] % 432 == 0
        return (total[0]//432, total[1]//432)

    for i, left in enumerate(irreducibles):
        for j, right in enumerate(irreducibles):
            assert inner(left["values"], right["values"]) == ((1, 0) if i == j else (0, 0))
    assert all(value[1] == 0 for record in irreducibles for value in record["values"])

    permutation_character = [(sum(h[i] == i for i in range(120)), 0) for h in H]
    nonzero = []
    for index, record in enumerate(irreducibles):
        multiplicity = inner(permutation_character, record["values"])
        assert multiplicity[1] == 0 and multiplicity[0] >= 0
        record["multiplicity"] = multiplicity[0]
        integer_values = [value[0] for value in record["values"]]
        record["character_sha256"] = hashlib.sha256(json.dumps(integer_values, separators=(",", ":")).encode()).hexdigest()
        if multiplicity[0]: nonzero.append((index, record))

    assert len(nonzero) == 14
    assert sorted(r["degree"] for _i, r in nonzero) == [1,1,1,2,2,2,4,4,4,4,8,8,8,8]
    assert sorted(r["multiplicity"] for _i, r in nonzero) == [1,1,1,1,1,1,1,2,2,3,3,3,4,5]
    assert sum(r["degree"]*r["multiplicity"] for _i, r in nonzero) == 120
    assert sum(r["multiplicity"]**2 for _i, r in nonzero) == 83

    H_index = {h: i for i, h in enumerate(H)}
    inverse_index = {h: H_index[inverse(h)] for h in H}
    character_projectors = []
    for character_index, record in nonzero:
        degree = record["degree"]; values = [value[0] for value in record["values"]]
        coordinates = []
        for i, j in g["reps"]:
            numerator = sum(values[inverse_index[h]] for h in H if h[j] == i)
            coordinates.append(sp.Rational(degree*numerator, 432))
        projector = sp.Matrix(coordinates)
        assert core.mul_q(g, projector, projector) == projector
        assert int(core.trace_q(g, projector)) == degree*record["multiplicity"]
        character_projectors.append({"character_index": character_index, "projector": projector, "record": record})

    t_records = core.center_T(g); s2, s4 = core.splitters(g); splitter = s2+s4
    full_records = core.refine_full(g, t_records, splitter)
    unmatched = set(range(14))
    for item in character_projectors:
        matches = [index for index, full in enumerate(full_records) if full["z"] == item["projector"]]
        assert len(matches) == 1
        block_index = matches[0]; unmatched.remove(block_index); full = full_records[block_index]; record = item["record"]
        assert full["n"] == record["multiplicity"] and full["m"] == record["degree"]
        item["block_index"] = block_index
        left = core.mul_q(g, item["projector"], splitter)
        right = core.mul_q(g, splitter, item["projector"])
        assert left == right
        if record["multiplicity"] == 1:
            pivot = next(i for i, value in enumerate(item["projector"]) if value != 0)
            scalar = sp.cancel(left[pivot]/item["projector"][pivot])
            assert left == scalar*item["projector"]
            item["splitter_eigenvalue"] = str(scalar)
        else:
            item["splitter_eigenvalue"] = None
    assert not unmatched

    fusion = []
    for t_index, t_record in enumerate(t_records):
        children = []; child_sum = sp.zeros(83, 1)
        for item in character_projectors:
            product = core.mul_q(g, t_record["z"], item["projector"])
            if product == item["projector"]:
                children.append(item); child_sum += item["projector"]
            else: assert product == sp.zeros(83, 1)
        assert child_sum == t_record["z"]
        fusion.append({
            "terwilliger_index": t_index, "terwilliger_block_size": t_record["n"],
            "isotypic_dimension": t_record["iso"], "child_count": len(children),
            "children": [{
                "character_index": child["character_index"], "degree": child["record"]["degree"],
                "multiplicity": child["record"]["multiplicity"], "orbit_index": child["record"]["orbit_index"],
                "little_label": child["record"]["little_label"], "splitter_eigenvalue": child["splitter_eigenvalue"],
            } for child in children],
        })
    assert sorted(item["child_count"] for item in fusion) == [1,1,1,1,1,1,1,2,2,3]
    assert sum(item["child_count"]-1 for item in fusion) == 4

    orbit_payload = []
    for orbit_index, (covector, orbit) in enumerate(dual_orbits):
        stabilizer = {k for k in K if dual_action(k, covector) == covector}
        orbit_payload.append({
            "orbit_index": orbit_index, "representative": list(covector), "orbit_size": len(orbit),
            "stabilizer_order": len(stabilizer), "stabilizer_type": subgroup_type(stabilizer),
            "little_irrep_count": len(little_characters(stabilizer)[1]),
        })

    public_irreducibles = []
    for index, record in enumerate(irreducibles):
        public_irreducibles.append({key: value for key, value in record.items() if key != "values"} | {"character_index": index})
    public_constituents = []
    for item in character_projectors:
        record = item["record"]
        public_constituents.append({
            "character_index": item["character_index"], "block_index": item["block_index"],
            "orbit_index": record["orbit_index"], "orbit_size": record["orbit_size"],
            "stabilizer_type": record["stabilizer_type"], "little_label": record["little_label"],
            "degree": record["degree"], "multiplicity": record["multiplicity"],
            "isotypic_dimension": record["degree"]*record["multiplicity"],
            "splitter_eigenvalue": item["splitter_eigenvalue"], "character_sha256": record["character_sha256"],
        })
    public_constituents.sort(key=lambda item: item["block_index"])

    return {
        "schema": "w33.pass1375_1379.mackey_selector_decomposition.v1", "status": "PASS",
        "pass1375_little_group_character_table": {
            "group": "C3^3 : (D8 x C2)", "group_order": 432, "dual_orbits": orbit_payload,
            "dual_orbit_sizes": [1,2,4,4,8,8], "irreducible_count": 27,
            "irreducible_degree_census": {"1":8,"2":6,"4":9,"8":4},
            "sum_squared_degrees": 432, "all_character_values_rational_integers": True,
            "rational_group_algebra": "Q^8 + M2(Q)^6 + M4(Q)^9 + M8(Q)^4",
            "irreducibles": public_irreducibles,
        },
        "pass1376_selector_permutation_character": {
            "degree": 120, "nonzero_constituents": 14,
            "constituent_degree_profile": [1,1,1,2,2,2,4,4,4,4,8,8,8,8],
            "multiplicity_profile": [1,1,1,1,1,1,1,2,2,3,3,3,4,5],
            "dimension_check": 120, "commutant_dimension_from_multiplicities": 83,
            "constituents": public_constituents,
        },
        "pass1377_mackey_wedderburn_identification": {
            "orbital_algebra": "End_H(Q^120)", "dimension": 83, "center_dimension": 14,
            "wedderburn": "Q^7 + M2(Q)^2 + M3(Q)^3 + M4(Q) + M5(Q)",
            "exact_projector_matches": 14,
            "conclusion": "Every orbital central projector is exactly one nonzero Mackey character projector; matrix sizes are selector multiplicities.",
        },
        "pass1378_terwilliger_fusion_explanation": {
            "terwilliger_center_dimension": 10, "orbital_center_dimension": 14,
            "fusion_group_sizes": sorted(item["child_count"] for item in fusion), "schur_defect": 4,
            "fusion": fusion,
            "conclusion": "Seven sectors are already separated by T; three scalar packets of sizes 2,2,3 account for (2-1)+(2-1)+(3-1)=4 missing central directions.",
        },
        "pass1379_boundary": {
            "mathematics": "Literal permutation-group reconstruction, exact little-group induction, and Z[omega] arithmetic; no database table or floating eigensolver.",
            "physics": "Finite rational representation theory only; no particle, gauge, generation, hardware, or laboratory identification.",
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    result = analyze(); encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    digest = hashlib.sha256(encoded.encode()).hexdigest()
    if args.check:
        if not args.output.exists() or args.output.read_text() != encoded: raise SystemExit(f"certificate drift: {args.output}")
    elif not args.verify_only:
        args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(encoded)
    print(f"PASS 1375-1379: Mackey selector decomposition sha256={digest}")

if __name__ == "__main__": main()
