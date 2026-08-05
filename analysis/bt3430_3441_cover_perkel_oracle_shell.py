#!/usr/bin/env python3
"""Passes 3430--3441 exact verifier.

Finite computations promoted here:
* frozen complete-cover census and representative-ledger contract;
* all fifteen aggregate inter-block defect realizations;
* explicit 135-state arithmetic Hamming-orbifold oracle;
* odd Hamming character/Krawtchouk shell reversal;
* explicit Perkel graph and 57-cell comparison;
* equitable-partition and group-order falsifiers;
* the rational rank-20 Perkel/signature projector comparison.

The full 327 representative ledger and objectwise switch graph are produced by
an accompanying compiled workflow and are not promoted until that artifact is
present and checked.
"""
from __future__ import annotations
import collections
import hashlib
import itertools
import json
import math
import random
from pathlib import Path

import networkx as nx
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_BT3430_BT3441_COVER_PERKEL_ORACLE_SHELL_results.json"
CERT = ROOT / "data/w33_pass1821_1825_complete_cover_signature.json"
LEDGER = ROOT / "data/PART_BT3430_BT3433_CANONICAL_COVER_REPRESENTATIVES.json"


def canon(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"))


def sha(x):
    return hashlib.sha256(canon(x).encode()).hexdigest()


def cover_census_contract():
    cert = json.loads(CERT.read_text())
    c = cert["pass1821_complete_cover_census"]
    s = cert["pass1822_nonlinear_signature_classification"]
    assert c["cover_orbits"] == 327
    assert c["global_covers"] == 3_547_800
    assert c["fixed_frame_covers"] == 394_200
    assert c["stabilizer_order_histogram"] == {"2": 228, "4": 84, "8": 15}
    orbit_rows = s["signature_orbits"]
    assert [x["cover_orbits"] for x in orbit_rows] == [270, 6, 24, 27]
    assert [x["global_covers"] for x in orbit_rows] == [3_149_280, 38_880, 233_280, 126_360]
    cap_joint = {
        "signature_6": {"stab4": 6},
        "signature_24": {"stab2": 12, "stab4": 12},
        "signature_27": {"stab4": 12, "stab8": 15},
    }
    status = "PENDING_COMPILED_CANONICAL_LEDGER"
    ledger_checks = None
    if LEDGER.exists():
        z = json.loads(LEDGER.read_text())
        reps = z["orbits"]
        assert len(reps) == 327
        assert all(len(r["representative"]) == 60 for r in reps)
        assert all(len(set(r["representative"])) == 60 for r in reps)
        assert all(all(0 <= u < 540 for u in r["representative"]) for r in reps)
        assert sum(r["orbit_size"] for r in reps) == 3_547_800
        assert all(r["orbit_size"] * r["stabilizer_order"] == 25_920 for r in reps)
        hist = collections.Counter(r["stabilizer_order"] for r in reps)
        assert hist == {2: 228, 4: 84, 8: 15}
        status = "PASS_327_CANONICAL_REPRESENTATIVE_LEDGER"
        ledger_checks = {
            "representatives": len(reps),
            "representative_rows": sum(len(r["representative"]) for r in reps),
            "orbit_sum": sum(r["orbit_size"] for r in reps),
            "stabilizer_histogram": dict(hist),
            "ledger_sha256": hashlib.sha256(LEDGER.read_bytes()).hexdigest(),
        }
    return {
        "status": status,
        "expected": {
            "orbits": 327,
            "global_covers": 3_547_800,
            "fixed_frame_covers": 394_200,
            "stabilizer_histogram": {"2": 228, "4": 84, "8": 15},
            "fixed_cover_binary_sha256": c["covers_binary_sha256"],
        },
        "signature_orbit_counts": [270, 6, 24, 27],
        "exceptional_cap_joint_partition": cap_joint,
        "ledger_checks": ledger_checks,
        "boundary": "No objectwise switch component is promoted before the compiled canonical ledger and switch artifact pass all checks.",
    }


def split_templates():
    out = []
    for m in range(1, 6):
        n = 10 - m
        for c in range(-2916, 325, 15):
            if c % 15 != 9:
                continue
            if m == 1:
                if -324 - n * c:
                    continue
                a = None
            else:
                a, r = divmod(-324 - n * c, m - 1)
                if r:
                    continue
            b, r = divmod(-324 - m * c, n - 1)
            if r:
                continue
            vals = [x for x in (a, b, c) if x is not None]
            if any(x % 15 != 9 for x in vals):
                continue
            lam_a = [] if m == 1 else [324 - a] * (m - 1)
            lam_b = [324 - b] * (n - 1)
            lam_q = 3240 - sum(lam_a) - sum(lam_b)
            spectrum = sorted(lam_a + lam_b + [0, lam_q])
            if min(spectrum) < 0:
                continue
            edge_counts = {
                k: (v + 2916) // 15
                for k, v in (("within_A", a), ("within_B", b), ("cross", c))
                if v is not None
            }
            if any(v < 0 for v in edge_counts.values()):
                continue
            out.append({
                "split": [m, n], "a": a, "b": b, "c": c,
                "spectrum": spectrum, "edge_counts": edge_counts,
            })
    assert collections.Counter(t["split"][0] for t in out) == {1: 1, 2: 1, 3: 5, 4: 3, 5: 5}
    assert len({tuple(t["spectrum"]) for t in out}) == 11
    return out


def local_block_witness():
    rng = random.Random(33903401)
    colours = [i for i in range(10) for _ in range(54)]
    rng.shuffle(colours)

    def violations(block):
        seen = {}
        bad = 0
        for cell in range(3):
            for colour in set(colours[block * 12 + 4 * cell:block * 12 + 4 * (cell + 1)]):
                if colour in seen and seen[colour] != cell:
                    bad += 1
                seen[colour] = cell
        return bad

    scores = [violations(b) for b in range(45)]
    total = sum(scores)
    temperature = 2.0
    for iteration in range(400_000):
        if total == 0:
            break
        i, j = rng.sample(range(540), 2)
        if colours[i] == colours[j]:
            continue
        bi, bj = i // 12, j // 12
        old = scores[bi] + (scores[bj] if bj != bi else 0)
        colours[i], colours[j] = colours[j], colours[i]
        ni = violations(bi)
        nj = violations(bj) if bj != bi else ni
        new = ni + (nj if bj != bi else 0)
        delta = new - old
        if delta <= 0 or rng.random() < math.exp(-delta / max(temperature, 1e-12)):
            scores[bi] = ni
            if bj != bi:
                scores[bj] = nj
            total += delta
        else:
            colours[i], colours[j] = colours[j], colours[i]
        temperature *= 0.99995
    assert total == 0
    assert collections.Counter(colours) == {i: 54 for i in range(10)}
    local = np.zeros((10, 10), dtype=int)
    for block in range(45):
        cells = [collections.Counter(colours[block * 12 + 4 * c:block * 12 + 4 * (c + 1)]) for c in range(3)]
        for c, d in ((0, 1), (0, 2), (1, 2)):
            for i, ni in cells[c].items():
                for j, nj in cells[d].items():
                    if i != j:
                        local[i, j] += ni * nj
                        local[j, i] += ni * nj
    assert np.all(local.sum(axis=1) == 432)
    return colours, local, iteration


def template_matrix(t):
    m, _ = t["split"]
    e = np.zeros((10, 10), dtype=int)
    for i in range(10):
        for j in range(i + 1, 10):
            if i < m and j < m:
                value = t["edge_counts"]["within_A"]
            elif i >= m and j >= m:
                value = t["edge_counts"]["within_B"]
            else:
                value = t["edge_counts"]["cross"]
            e[i, j] = e[j, i] = value
    return e


def balanced_degrees(residual):
    degrees = np.zeros((10, 54, 10), dtype=int)
    for colour in range(10):
        floors = {j: int(residual[colour, j] // 54) for j in range(10) if j != colour}
        remainders = {j: int(residual[colour, j] % 54) for j in range(10) if j != colour}
        target = 24 - sum(floors.values())
        assert sum(remainders.values()) == 54 * target
        flow = nx.DiGraph()
        source, sink = "source", "sink"
        for j, demand in remainders.items():
            flow.add_edge(source, ("colour", j), capacity=demand)
            for v in range(54):
                flow.add_edge(("colour", j), ("vertex", v), capacity=1)
        for v in range(54):
            flow.add_edge(("vertex", v), sink, capacity=target)
        value, assignment = nx.maximum_flow(flow, source, sink)
        assert value == sum(remainders.values())
        for v in range(54):
            for j in floors:
                degrees[colour, v, j] = floors[j] + assignment[("colour", j)][("vertex", v)]
        assert np.all(degrees[colour].sum(axis=1) == 24)
    return degrees


def realize_abstract_interblock(residual):
    degrees = balanced_degrees(residual)
    graph = nx.Graph()
    graph.add_nodes_from((i, v) for i in range(10) for v in range(54))
    for i in range(10):
        for j in range(i + 1, 10):
            left = list(map(int, degrees[i, :, j]))
            right = list(map(int, degrees[j, :, i]))
            assert sum(left) == sum(right) == int(residual[i, j])
            bip = nx.algorithms.bipartite.havel_hakimi_graph(left, right, create_using=nx.Graph())
            for u, v in bip.edges():
                if u >= 54:
                    u, v = v, u
                graph.add_edge((i, u), (j, v - 54))
    assert graph.number_of_edges() == 6480
    assert set(dict(graph.degree()).values()) == {24}
    assert nx.is_connected(graph)
    counts = np.zeros((10, 10), dtype=int)
    for (i, _), (j, _) in graph.edges():
        counts[i, j] += 1
        counts[j, i] += 1
    assert np.array_equal(counts, residual)
    edge_stream = sorted((10 * u[0] + 540 * u[1] + v[0], v[1]) for u, v in graph.edges())
    return hashlib.sha256(canon(edge_stream).encode()).hexdigest()


def interblock_realizability():
    templates = split_templates()
    colours, local, iterations = local_block_witness()
    rows = []
    for index, template in enumerate(templates):
        total = template_matrix(template)
        residual = total - local
        assert residual.min() >= 0
        assert total.sum() // 2 == 8640
        assert residual.sum() // 2 == 6480
        assert np.all(residual.sum(axis=1) == 1296)
        rows.append({
            "template": index,
            "split": template["split"],
            "residual_min": int(residual[np.triu_indices(10, 1)].min()),
            "residual_max": int(residual.max()),
            "residual_edges": int(residual.sum() // 2),
            "abstract_connected_24_regular_sha256": realize_abstract_interblock(residual),
        })
    return {
        "status": "PASS_ALL_15_CONNECTED_SIMPLE_AGGREGATE_REALIZATIONS",
        "templates": 15,
        "distinct_spectra": 11,
        "local_iterations": iterations,
        "local_pair_range": [int(local[np.triu_indices(10, 1)].min()), int(local.max())],
        "local_assignment_sha256": hashlib.sha256(bytes(colours)).hexdigest(),
        "rows": rows,
        "boundary": "These are connected simple 24-regular abstract realizations with exact pair counts; they are not embeddings into the fixed 6480-edge inter-block graph.",
    }


def tau(state):
    x1, x2, x3, x4, x5 = state
    return ((-x4) % 3, (1 - x3) % 3, (1 - x2) % 3, (-x1) % 3, x5)


def arithmetic_oracle():
    states = list(itertools.product(range(3), repeat=5))
    assert all(tau(tau(x)) == x for x in states)
    seen = set()
    orbits = []
    for x in states:
        if x in seen:
            continue
        orbit = tuple(sorted({x, tau(x)}))
        seen.update(orbit)
        orbits.append(orbit)
    orbits.sort(key=lambda o: o[0])
    assert len(orbits) == 135
    assert collections.Counter(map(len, orbits)) == {1: 27, 2: 108}
    orbit_id = {x: i for i, orbit in enumerate(orbits) for x in orbit}
    tokens = [(coordinate, delta) for coordinate in range(5) for delta in (1, 2)]
    table = []
    for orbit in orbits:
        x = orbit[0]
        row = []
        for coordinate, delta in tokens:
            y = list(x)
            y[coordinate] = (y[coordinate] + delta) % 3
            row.append(orbit_id[tuple(y)])
        table.append(row)
    assert sum(len(set(row)) for row in table) == 1242
    assert collections.Counter(len(set(row)) for row in table) == {6: 27, 10: 108}
    weights = [len(o) for o in orbits]
    directed = collections.Counter()
    for i, row in enumerate(table):
        for j in row:
            directed[i, j] += weights[i]
    for (i, j), value in directed.items():
        assert value == directed[j, i]
    # XOR-target involution is exhaustive over all 8-bit targets.
    involution_cases = 0
    for i, row in enumerate(table):
        for target in row:
            for z in range(256):
                assert (z ^ target) ^ target == z
                involution_cases += 1
    return {
        "status": "PASS_EXPLICIT_ARITHMETIC_ORACLE",
        "species": 135,
        "fixed_orbits": 27,
        "paired_orbits": 108,
        "tokens": 1350,
        "distinct_directed_destinations": 1242,
        "involution_cases": involution_cases,
        "table_sha256": hashlib.sha256(canon(table).encode()).hexdigest(),
        "canonicalization": "lexicographic minimum of x and tau(x)",
        "primitive_schedule": [
            "decode five base-3 digits", "select coordinate and nonzero delta",
            "add modulo 3", "compute affine tau image", "lexicographically compare",
            "select canonical representative", "rank canonical orbit", "XOR 8-bit target",
        ],
        "boundary": "This is an exhausted logical arithmetic compiler, not an optimized Clifford+T minimum or hardware synthesis.",
    }


def shell_character_theorem(max_r=8):
    y = sp.symbols("y")
    rows = []
    for r in range(max_r + 1):
        n = 2 * r + 1
        full = sp.expand((1 + 3 * y) ** n)
        trace = sp.expand((1 + 3 * y) * (1 + 3 * y ** 2) ** r)
        invariant = sp.expand((full + trace) / 2)
        anti = sp.expand((full - trace) / 2)
        m_plus = [int(invariant.coeff(y, j)) for j in range(n + 1)]
        m_minus = [int(anti.coeff(y, j)) for j in range(n + 1)]
        x = sp.symbols("x")
        quotient_shell = sp.expand(((x + 3) ** n + (x + 3) * (x ** 2 + 3) ** r) / 2)
        shells = [int(quotient_shell.coeff(x, s)) for s in range(n + 1)]
        assert m_plus == list(reversed(shells))
        assert sum(m_plus) + sum(m_minus) == 4 ** n
        rows.append({"r": r, "n": n, "quotient_shells": shells, "invariant_multiplicities": m_plus})
    assert rows[2]["quotient_shells"] == [135, 207, 144, 48, 9, 1]
    return {
        "status": "PASS_CHARACTER_KRAWTCHOUK_REVERSAL_THROUGH_H17_4",
        "full_grade_character": "(1+3y)^(2r+1)",
        "tau_grade_trace": "(1+3y)(1+3y^2)^r",
        "invariant_character": "((1+3y)^(2r+1)+(1+3y)(1+3y^2)^r)/2",
        "shell_polynomial": "((x+3)^(2r+1)+(x+3)(x^2+3)^r)/2",
        "theorem": "m_plus[j] = quotient_shell[2r+1-j]",
        "instances": rows,
    }


def perkel_graph():
    graph = nx.Graph()
    graph.add_nodes_from((i, j) for i in range(3) for j in range(19))
    for i, j in list(graph.nodes()):
        rhs = pow(2, 6 * i, 19)
        for k in range(19):
            if pow((k - j) % 19, 3, 19) == rhs:
                graph.add_edge((i, j), ((i + 1) % 3, k))
    return graph


def intersection_array(graph):
    root = min(graph.nodes())
    distance = nx.single_source_shortest_path_length(graph, root)
    shells = collections.Counter(distance.values())
    local = {}
    for d in range(max(distance.values()) + 1):
        triples = set()
        for v in (u for u in graph if distance[u] == d):
            count = collections.Counter(distance[w] for w in graph[v])
            triples.add((count.get(d - 1, 0), count.get(d, 0), count.get(d + 1, 0)))
        assert len(triples) == 1
        local[d] = next(iter(triples))
    return shells, local


def equitable_partition_falsifier():
    sizes = (12, 30, 15)
    compositions = [row for row in itertools.product(range(7), repeat=3) if sum(row) == 6]
    x = sp.symbols("x")
    alpha = (3 + sp.sqrt(5)) / 2
    beta = (3 - sp.sqrt(5)) / 2
    allowed = {
        sp.expand((x - 6) ** 3),
        sp.expand((x - 6) ** 2 * (x + 3)),
        sp.expand((x - 6) * (x + 3) ** 2),
        sp.expand((x - 6) * (x - alpha) * (x - beta)),
    }
    balanced = []
    spectral = []
    for rows in itertools.product(compositions, repeat=3):
        if not all(sizes[i] * rows[i][j] == sizes[j] * rows[j][i] for i in range(3) for j in range(3)):
            continue
        matrix = sp.Matrix(rows)
        polynomial = sp.expand(matrix.charpoly(x).as_expr())
        balanced.append([list(row) for row in rows])
        if polynomial in allowed:
            spectral.append({"matrix": [list(row) for row in rows], "characteristic_polynomial": str(sp.factor(polynomial))})
    assert len(balanced) == 10
    assert len(spectral) == 3
    assert all(sum(1 for j in range(3) if item["matrix"][i][j] and i != j) == 0 for item in spectral for i in range(3))
    return {
        "status": "PASS_NO_CONNECTED_PERKEL_EQUITABLE_12_30_15_PARTITION",
        "balanced_quotients": len(balanced),
        "spectrally_compatible_quotients": spectral,
        "conclusion": "Every spectrally compatible quotient is block diagonal; a connected Perkel graph cannot preserve the cap stabilizer partition equitably.",
    }


def perkel_and_group_audit():
    graph = perkel_graph()
    assert graph.number_of_nodes() == 57
    assert graph.number_of_edges() == 171
    assert set(dict(graph.degree()).values()) == {6}
    assert nx.is_connected(graph) and nx.diameter(graph) == 3
    shells, local = intersection_array(graph)
    assert shells == {0: 1, 1: 6, 2: 30, 3: 20}
    assert local == {0: (0, 0, 6), 1: (1, 0, 5), 2: (1, 3, 2), 3: (3, 3, 0)}
    adjacency = nx.to_numpy_array(graph, nodelist=sorted(graph.nodes()), dtype=int)
    eig = collections.Counter(round(float(v), 10) for v in np.linalg.eigvalsh(adjacency))
    expected = {6.0: 1, round((3 + math.sqrt(5)) / 2, 10): 18, round((3 - math.sqrt(5)) / 2, 10): 18, -3.0: 20}
    assert eig == expected
    psl = 3420
    psp = 25920
    affine = 4199040
    assert psl == 19 * 18 * 20 // 2
    assert affine == 81 * 51840
    assert psp % 57 != 0 and affine % 57 != 0
    assert math.gcd(psl, psp) == math.gcd(psl, affine) == 180
    return {
        "status": "PASS_EXPLICIT_PERKEL_AND_GROUP_SEPARATION",
        "perkel": {
            "vertices": 57, "edges": 171, "degree": 6, "diameter": 3,
            "distance_shells": [1, 6, 30, 20],
            "intersection_array": {"b": [6, 5, 2], "c": [1, 1, 3]},
            "spectrum": {"6": 1, "(3+sqrt(5))/2": 18, "(3-sqrt(5))/2": 18, "-3": 20},
        },
        "orders": {"PSL(2,19)": psl, "PSp(4,3)": psp, "ASp(4,3)": affine},
        "gcd_with_PSL": {"PSp(4,3)": 180, "ASp(4,3)": 180},
        "transitive_57_action_divisibility": {"PSp(4,3)": False, "ASp(4,3)": False},
        "instruction_diameter_19_boundary": "The shared integer 19 is not explained by a PSL(2,19) subgroup or a transitive Perkel action; 19 does not divide 4,199,040.",
        "equitable_partition_test": equitable_partition_falsifier(),
    }


def rank_twenty_shadow():
    x = sp.symbols("x")
    perkel_projector = -sp.expand((x - 6) * (x ** 2 - 3 * x + 1)) / 171
    anchor_projector = sp.expand((x - 32) * (x - 2)) / 216
    assert sp.simplify(perkel_projector.subs(x, -3)) == 1
    assert all(sp.simplify(perkel_projector.subs(x, value)) == 0 for value in (6, (3 + sp.sqrt(5)) / 2, (3 - sp.sqrt(5)) / 2))
    assert sp.simplify(anchor_projector.subs(x, -4)) == 1
    assert all(sp.simplify(anchor_projector.subs(x, value)) == 0 for value in (32, 2))
    return {
        "status": "PASS_TWO_RATIONAL_RANK_20_PROJECTORS",
        "perkel_minus3_projector": str(perkel_projector),
        "anchor_minus4_projector": str(anchor_projector),
        "dimensions": {"Perkel_minus3": 20, "cover_signature_minus4": 20},
        "boundary": "Equal dimension and rational projector formulas do not supply an intertwiner between PSL(2,19) and PSp(4,3). The next exact test is restriction to explicitly chosen common A5 subgroups.",
    }


def main():
    data = {
        "schema": "w33.pass3430_3441.cover_perkel_oracle_shell.v1",
        "status": "PASS_EXACT_LIGHTWEIGHT_FRONTS_HEAVY_LEDGER_GATED",
        "pass3430_3433_cover_contract": cover_census_contract(),
        "pass3434_3435_interblock": interblock_realizability(),
        "pass3436_3437_arithmetic_oracle": arithmetic_oracle(),
        "pass3438_3439_shell_character": shell_character_theorem(),
        "pass3440_perkel_57cell_audit": perkel_and_group_audit(),
        "pass3441_bonkers_rank20_shadow": rank_twenty_shadow(),
        "evidence_boundary": {
            "chromatic": "10 <= chi(H) <= 11",
            "not_promoted": [
                "canonical 327-ledger before compiled artifact", "objectwise switch components",
                "embedding abstract inter-block witnesses into the fixed graph", "ten-colour SAT or UNSAT",
                "optimized Clifford+T minimum", "Perkel identification of the exceptional cap",
                "remote CI or PDF result", "hardware or physical interpretation",
            ],
        },
    }
    data["semantic_sha256"] = sha(data)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(data["status"], data["semantic_sha256"])


if __name__ == "__main__":
    main()
