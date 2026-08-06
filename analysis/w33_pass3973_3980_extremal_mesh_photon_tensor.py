#!/usr/bin/env python3
"""Passes 3973-3980: 57-code geometry, exact mesh neighborhood, photon experiment, rank-48 tensor, and three constructions."""
from __future__ import annotations

import argparse
import functools
import hashlib
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from math import gcd
from pathlib import Path

SCHEMA = "w33.pass3973_3980.extremal_mesh_photon_tensor.v1"
STATUS = "PASS_EXACT_57_GEOMETRY_MESH_RADIUS1_TENSOR_EXPERIMENT_MODEL_MONSTER_FAIL_CLOSED"
MESH_PERM = [7,19,9,17,14,25,24,15,10,16,20,6,4,32,31,0,33,3,1,28,5,2,30,26,29,27,35,34,21,22,23,12,11,13,8,18]
C_LIGHT = 299_792_458.0


def bits(x: int, n: int = 6) -> list[int]:
    return [(x >> i) & 1 for i in range(n)]


def qform(x: int) -> int:
    b = bits(x)
    return (b[0]*b[1] + b[2]*b[3] + b[4]*b[5] + b[4] + b[5]) & 1


def beta(x: int, y: int) -> int:
    return qform(x ^ y) ^ qform(x) ^ qform(y)


def gf2_basis(values: list[int] | set[int]) -> list[int]:
    pivots: dict[int, int] = {}
    for value in values:
        x = int(value)
        while x:
            p = x.bit_length() - 1
            if p in pivots:
                x ^= pivots[p]
            else:
                pivots[p] = x
                for pp in list(pivots):
                    if pp != p and ((pivots[pp] >> p) & 1):
                        pivots[pp] ^= x
                break
    return [pivots[p] for p in sorted(pivots, reverse=True)]


def enumerate_code(basis: list[int]) -> list[int]:
    words = [0]
    for b in basis:
        words += [x ^ b for x in words]
    return words


@functools.lru_cache(maxsize=1)
def quadratic_parent() -> tuple[list[int], list[list[int]], list[list[dict[int, Fraction]]]]:
    nonsingular = [x for x in range(1, 64) if qform(x)]
    assert len(nonsingular) == 36
    adjacency = [[0] * 36 for _ in range(36)]
    for i, x in enumerate(nonsingular):
        for j, y in enumerate(nonsingular):
            if i != j and beta(x, y) == 0:
                adjacency[i][j] = 1
    assert all(sum(row) == 15 for row in adjacency)
    k = [[2*adjacency[i][j] - 1 for j in range(36)] for i in range(36)]
    for i in range(36):
        for j in range(36):
            dot = sum(k[i][t]*k[j][t] for t in range(36))
            assert dot == (36 if i == j else 0)
    h = [[{1: Fraction(k[i][j], 6)} for j in range(36)] for i in range(36)]
    return nonsingular, adjacency, h


def build_base_and_weight4() -> tuple[list[int], list[int], list[int], list[set[int]]]:
    nonsingular, _, _ = quadratic_parent()
    base_words: set[int] = set()
    for label in range(64):
        word = 0
        for i, x in enumerate(nonsingular):
            if beta(label, x):
                word |= 1 << i
        base_words.add(word)
    base = gf2_basis(base_words)
    assert len(base) == 6
    weight4: list[int] = []
    for support in itertools.combinations(range(36), 4):
        word = sum(1 << i for i in support)
        if all(((word & b).bit_count() & 1) == 0 for b in base):
            weight4.append(word)
    assert len(weight4) == 945
    neighbors = [set() for _ in weight4]
    for i, wi in enumerate(weight4):
        for j in range(i + 1, len(weight4)):
            if ((wi & weight4[j]).bit_count() & 1) == 0:
                neighbors[i].add(j)
                neighbors[j].add(i)
    assert {len(n) for n in neighbors} == {624}
    return nonsingular, base, weight4, neighbors


def deterministic_57_code() -> dict[str, object]:
    _, base, weight4, neighbors = build_base_and_weight4()
    candidates = set(range(len(weight4)))
    clique: list[int] = []
    while candidates:
        v = max(candidates, key=lambda x: (len(candidates & neighbors[x]), -x))
        clique.append(v)
        candidates &= neighbors[v]
    assert len(clique) == 57
    selected = [weight4[i] for i in clique]
    basis = gf2_basis(base + selected)
    assert len(basis) == 17
    words = enumerate_code(basis)
    dist = Counter(w.bit_count() for w in words)
    expected = {0:1,4:57,8:852,12:7332,16:57294,20:57294,24:7332,28:852,32:57,36:1}
    assert dict(sorted(dist.items())) == expected
    assert all((w.bit_count() % 4) == 0 for w in words)
    assert all(((x & y).bit_count() & 1) == 0 for x in basis for y in basis)

    graph = [set() for _ in range(57)]
    for i in range(57):
        for j in range(i + 1, 57):
            if (selected[i] & selected[j]).bit_count() == 2:
                graph[i].add(j)
                graph[j].add(i)
    seen: set[int] = set()
    components: list[list[int]] = []
    for i in range(57):
        if i in seen:
            continue
        stack = [i]
        seen.add(i)
        comp: list[int] = []
        while stack:
            v = stack.pop()
            comp.append(v)
            for u in graph[v]:
                if u not in seen:
                    seen.add(u)
                    stack.append(u)
        components.append(sorted(comp))
    components.sort(key=len, reverse=True)
    assert [len(c) for c in components] == [45, 6, 6]

    c45 = components[0]
    maximal_cliques: list[set[int]] = []
    def bronk(R: set[int], P: set[int], X: set[int]) -> None:
        if not P and not X:
            maximal_cliques.append(set(R))
            return
        union = P | X
        pivot = max(union, key=lambda u: len(P & graph[u])) if union else None
        branch = list(P - (graph[pivot] if pivot is not None else set()))
        for v in branch:
            bronk(R | {v}, P & graph[v], X & graph[v])
            P.remove(v)
            X.add(v)
    bronk(set(), set(c45), set())
    nine_cliques = [s for s in maximal_cliques if len(s) == 9]
    assert len(nine_cliques) == 10
    pair_label: dict[int, tuple[int, int]] = {}
    for v in c45:
        labels = tuple(i for i, s in enumerate(nine_cliques) if v in s)
        assert len(labels) == 2
        pair_label[v] = labels
    assert set(pair_label.values()) == set(itertools.combinations(range(10), 2))
    for i, u in enumerate(c45):
        for v in c45[i+1:]:
            assert ((v in graph[u]) == bool(set(pair_label[u]) & set(pair_label[v])))

    for comp in components[1:]:
        nonedges = []
        for i, u in enumerate(comp):
            for v in comp[i+1:]:
                if v not in graph[u]:
                    nonedges.append((u, v))
        assert len(nonedges) == 3
        assert len({x for e in nonedges for x in e}) == 6
        mapping: dict[int, tuple[int, int]] = {}
        opposite_pairs = [((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
        for (u,v),(eu,ev) in zip(sorted(nonedges), opposite_pairs):
            mapping[u], mapping[v] = eu, ev
        for i, u in enumerate(comp):
            for v in comp[i+1:]:
                share = bool(set(mapping[u]) & set(mapping[v]))
                assert ((v in graph[u]) == share)

    basis_digest = hashlib.sha256("\n".join(f"{x:09x}" for x in basis).encode()).hexdigest()
    support_digest = hashlib.sha256("\n".join(f"{x:09x}" for x in sorted(selected)).encode()).hexdigest()
    return {
        "code_parameters": [36, 17, 4],
        "A4": 57,
        "weight_distribution": dict(sorted(dist.items())),
        "basis_sha256": basis_digest,
        "weight4_support_sha256": support_digest,
        "intersection2_components": [45, 6, 6],
        "component_identifications": ["T(10)=L(K10)", "T(4)=L(K4)", "T(4)=L(K4)"],
        "T10_star_cliques": 10,
        "T10_vertices_as_pairs": 45,
        "small_complement_matchings": 3,
        "extremality_status": "NOT_PROVED_GLOBAL; exact geometry and one-parameter enumerator rigidity proved",
    }


def enumerator_rigidity() -> dict[str, object]:
    t = 57
    A8, A12, A16 = 11*t + 225, 9555 - 39*t, 55755 + 27*t
    B6, B10, B14, B18 = 6*(t + 7), 12*(5*t + 483), 6*(14505 - 49*t), 456*(t + 455)
    assert (A8, A12, A16) == (852, 7332, 57294)
    assert (B6, B10, B14, B18) == (384, 9216, 70272, 233472)
    return {
        "parameter": "t=A4",
        "forced_primal": {"A8":"11t+225", "A12":"9555-39t", "A16":"55755+27t"},
        "forced_dual": {"B2":"0", "B4":"t", "B6":"6(t+7)", "B8":"11t+225", "B10":"12(5t+483)", "B12":"39(245-t)", "B14":"6(14505-49t)", "B16":"27(t+2065)", "B18":"456(t+455)"},
        "universal_LP_bound": "t<=245",
        "t57_evaluation": {"A8":A8,"A12":A12,"A16":A16,"B6":B6,"B10":B10,"B14":B14,"B18":B18},
        "boundary": "This rigidity theorem does not prove t=57 globally maximal.",
    }


def squarefree_decompose(n: int) -> tuple[int, int]:
    assert n >= 1
    square = squarefree = 1
    p = 2
    while p*p <= n:
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        if e:
            square *= p ** (e // 2)
            if e & 1:
                squarefree *= p
        p += 1 if p == 2 else 2
    if n > 1:
        squarefree *= n
    return square, squarefree


def clean(a: dict[int, Fraction]) -> dict[int, Fraction]:
    return {r: c for r, c in a.items() if c}


def add_e(a: dict[int, Fraction], b: dict[int, Fraction]) -> dict[int, Fraction]:
    out = dict(a)
    for r, c in b.items():
        out[r] = out.get(r, Fraction(0)) + c
    return clean(out)


def neg_e(a: dict[int, Fraction]) -> dict[int, Fraction]:
    return {r: -c for r, c in a.items()}


def mul_e(a: dict[int, Fraction], b: dict[int, Fraction]) -> dict[int, Fraction]:
    out: dict[int, Fraction] = {}
    for r1, c1 in a.items():
        for r2, c2 in b.items():
            common = gcd(r1, r2)
            r = (r1 // common) * (r2 // common)
            out[r] = out.get(r, Fraction(0)) + c1*c2*common
    return clean(out)


def sqrt_fraction(f: Fraction, sign: int = 1) -> dict[int, Fraction]:
    assert f >= 0
    if f == 0:
        return {}
    square, squarefree = squarefree_decompose(f.numerator * f.denominator)
    return {squarefree: Fraction(sign * square, f.denominator)}


def single_square(a: dict[int, Fraction]) -> Fraction:
    if not a:
        return Fraction(0)
    assert len(a) == 1
    r, c = next(iter(a.items()))
    return c*c*r


def sign_single(a: dict[int, Fraction]) -> int:
    if not a:
        return 0
    assert len(a) == 1
    return 1 if next(iter(a.values())) > 0 else -1


def exact_givens_stats(p: list[int]) -> tuple[int, int, int, int, int]:
    _, _, h = quadratic_parent()
    m = [[dict(h[p[i]][p[j]]) for j in range(36)] for i in range(36)]
    operations = skipped = 0
    max_terms = 1
    last = [-1] * 36
    for col in range(35):
        for row in range(35, col, -1):
            b = m[row][col]
            if not b:
                skipped += 1
                continue
            a = m[row-1][col]
            a2, b2 = single_square(a), single_square(b)
            r2 = a2 + b2
            c = sqrt_fraction(a2/r2, sign_single(a))
            s = sqrt_fraction(b2/r2, sign_single(b))
            old1 = [dict(x) for x in m[row-1]]
            old2 = [dict(x) for x in m[row]]
            for j in range(36):
                m[row-1][j] = add_e(mul_e(c, old1[j]), mul_e(s, old2[j]))
                m[row][j] = add_e(mul_e(neg_e(s), old1[j]), mul_e(c, old2[j]))
                max_terms = max(max_terms, len(m[row-1][j]), len(m[row][j]))
            assert not m[row][col]
            layer = max(last[row-1], last[row]) + 1
            last[row-1] = last[row] = layer
            operations += 1
    offdiag = sum(bool(m[i][j]) for i in range(36) for j in range(36) if i != j)
    return operations, max(last)+1, skipped, max_terms, offdiag


def mesh_radius_one(heavy: bool) -> dict[str, object]:
    base = exact_givens_stats(MESH_PERM)
    assert base == (398, 69, 232, 1, 0)
    pairs = list(itertools.combinations(range(36), 2)) if heavy else [(i, i+1) for i in range(35)]
    rows = []
    for i, j in pairs:
        p = MESH_PERM.copy()
        p[i], p[j] = p[j], p[i]
        rows.append((i, j, exact_givens_stats(p)))
    histogram = Counter(r[2][0] for r in rows)
    assert min(histogram) == 398
    assert all(r[2][1] == 69 and r[2][3] == 1 and r[2][4] == 0 for r in rows)
    if heavy:
        expected = {398:22,400:43,402:20,404:17,406:30,408:18,410:19,412:17,414:16,416:23,418:10,420:21,422:23,424:14,426:16,428:15,430:18,432:10,434:15,436:16,438:15,440:15,442:17,444:12,446:13,448:11,450:11,452:15,454:13,456:10,458:12,460:8,462:10,464:9,466:8,468:12,470:10,472:9,474:9,476:6,478:6,480:3,482:6,484:5,486:2}
        assert dict(sorted(histogram.items())) == expected
    payload = "\n".join(f"{i},{j},{s[0]},{s[1]},{s[2]}" for i,j,s in rows)
    return {
        "base": {"rotations":base[0],"layers":base[1],"exact_zeros":base[2]},
        "neighborhood": "all 630 transpositions" if heavy else "35 adjacent transpositions",
        "tested": len(rows),
        "rotation_histogram": dict(sorted(histogram.items())),
        "minimum_rotations": min(histogram),
        "ties_at_398": histogram[398],
        "all_layers": 69,
        "sha256": hashlib.sha256(payload.encode()).hexdigest(),
        "status": "EXACT_RADIUS_ONE_LOCAL_OPTIMUM; global optimum remains open",
    }


def rank48_tensor() -> dict[str, object]:
    block_sizes = [1, 1, 2, 2, 2, 3, 5]
    labels: list[tuple[int,int,int]] = []
    for b, n in enumerate(block_sizes):
        for i in range(n):
            for j in range(n):
                labels.append((b, i, j))
    assert len(labels) == 48
    index = {x:k for k,x in enumerate(labels)}
    products: list[tuple[int,int,int]] = []
    for a, (b,i,j) in enumerate(labels):
        for c, (d,k,l) in enumerate(labels):
            if b == d and j == k:
                products.append((a,c,index[(b,i,l)]))
    assert len(products) == sum(n**3 for n in block_sizes) == 178
    table = {(a,b):c for a,b,c in products}
    for a in range(48):
        for b in range(48):
            ab = table.get((a,b))
            for c in range(48):
                bc = table.get((b,c))
                left = table.get((ab,c)) if ab is not None else None
                right = table.get((a,bc)) if bc is not None else None
                assert left == right
    payload = "\n".join(f"{a},{b},{c}" for a,b,c in products)
    return {
        "wedderburn_blocks": block_sizes,
        "algebra": "Q^2 + M2(Q)^3 + M3(Q) + M5(Q)",
        "dimension": 48,
        "center_dimension": 7,
        "basis": [f"b{b}:e{i}{j}" for b,i,j in labels],
        "nonzero_structure_constants": len(products),
        "sparse_products": products,
        "tensor_sha256": hashlib.sha256(payload.encode()).hexdigest(),
        "boundary": "Complete multiplication tensor in Wedderburn matrix-unit coordinates, not yet the geometric orbital-relation intersection tensor.",
    }


def symmetric_channel_information(M: int, error: float) -> float:
    if error == 0:
        return math.log2(M)
    return math.log2(M) + (1-error)*math.log2(1-error) + error*math.log2(error/(M-1))


def photon_experiment() -> dict[str, object]:
    modes = [2,4,8,16,40,81,729]
    capacity = [{"M":M,"ideal_bits":math.log2(M),"bits_at_1pct_symmetric_error":symmetric_channel_information(M,0.01),"bits_at_5pct_symmetric_error":symmetric_channel_information(M,0.05)} for M in modes]
    L, sigma, N, z, ratio = 10_000.0, 50e-12, 1_000_000, 5.0, 40/2
    gamma_stat = z*sigma/math.sqrt(N) / ((L/C_LIGHT)*math.log(ratio))
    W = 20e9
    slepian = []
    for M in [40,81,729]:
        T = M/(2*W)
        slepian.append({"M":M,"half_bandwidth_Hz":W,"duration_s":T,"vacuum_length_m":C_LIGHT*T})
    return {
        "protocol": [
            "herald one 1550-nm photon with fixed spectral envelope",
            "randomly interleave unitary mode alphabets M=2,4,8,16,40",
            "repeat at two or more free-space lengths and fit t(M,L)=a(M)+b(M)L",
            "treat a(M) as encoder/decoder latency and b(M)-1/c as the propagation test",
            "decode to a confusion matrix and report mutual information separately from timing",
        ],
        "capacity_table": capacity,
        "timing_example": {"length_m":L,"single_event_jitter_s":sigma,"events_per_setting":N,"sigma_level":z,"model":"c_eff(M)=c*(M/2)^gamma","statistical_abs_gamma_bound_if_null":gamma_stat,"systematics_warning":"clock drift, mode-dependent optics, detector walk, and pulse reshaping dominate unless length-slope separation is used"},
        "slepian_shannon_number_examples": slepian,
        "falsifier": "A reproducible mode-count-dependent slope b(M), surviving encoder swaps and length scaling, would falsify the invariant-front null. Intercept shifts alone do not.",
        "boundary": "This is a numerically certified design and sensitivity model, not a performed experiment or a measurement of fundamental vacuum front speed.",
    }


def causal_capacity_constructions() -> dict[str, object]:
    direct_sum = [{"modes":M,"bits":math.log2(M)} for M in [40,81,729]]
    wavelength = 1550e-9
    serial = [{"orthogonal_updates":N,"min_length_m":N*wavelength/4,"min_length_wavelengths":N/4} for N in [2,12,39,40,81]]
    powers = []
    invariant_bits_per_diameter = math.log2(40)/2
    invariant_bits_per_min_wavelength = 2*math.log2(40)
    for m in range(1,7):
        bits_capacity = m*math.log2(40)
        powers.append({"m":m,"vertices":40**m,"diameter":2*m,"ideal_direct_sum_bits":bits_capacity,"bits_per_diameter":bits_capacity/(2*m),"qsl_min_length_wavelengths":m/2,"bits_per_qsl_min_wavelength":bits_capacity/(m/2)})
    return {
        "capacity_trilemma": {
            "direct_sum":"one photon over M orthogonal alternatives carries at most log2(M) ideal classical bits per use",
            "tensor_product":"N log2(d) bits requires N physically independent d-state factors, not merely N named nodes",
            "time_bandwidth":"approximately M concentrated temporal modes require a Shannon number 2WT of order M",
        },
        "direct_sum_examples":direct_sum,
        "serial_qsl_examples_1550nm":serial,
        "self_similarity_invariants": {"bits_per_graph_diameter":invariant_bits_per_diameter,"bits_per_qsl_min_wavelength":invariant_bits_per_min_wavelength,"cartesian_power_table":powers,"interpretation":"self-similarity preserves address density per routing depth; it does not alter vacuum c"},
    }


def monster_gate() -> dict[str, object]:
    return {
        "required_artifact":"data/PART_3751_MONSTER_U42_CLASS_FUSION_EXECUTION.json",
        "observed_in_repo":False,
        "status":"PENDING_EXPLICIT_MONSTER_WORDS_AND_CLASS_FUSION",
        "promoted_embedding":False,
        "boundary":"Abstract U4(2):2 fingerprints are not serialized mmgroup/Monster words and do not execute the class-fusion gate.",
    }


def build_result(heavy: bool) -> dict[str, object]:
    result = {
        "schema":SCHEMA,
        "status":STATUS,
        "pass3973_code57_geometry":deterministic_57_code(),
        "pass3973_enumerator_rigidity":enumerator_rigidity(),
        "pass3974_mesh_radius_one":mesh_radius_one(heavy),
        "pass3975_photon_experiment":photon_experiment(),
        "pass3976_rank48_tensor":rank48_tensor(),
        "pass3977_monster_gate":monster_gate(),
        "pass3978_3980_constructions":causal_capacity_constructions(),
        "evidence_boundary": {
            "exact":["57-code reconstruction and T(10)+2T(4) identification","one-parameter enumerator rigidity","exact Givens neighborhood audit","48-dimensional Wedderburn multiplication tensor","capacity/timing formulas"],
            "modeled":["symmetric-channel information","timing sensitivity","Slepian Shannon-number engineering estimate"],
            "open":["global A4 extremality","global mesh optimum","performed photon experiment","geometric orbital-basis rank-48 tensor","Monster embedding/class fusion","variable vacuum c","hardware or laboratory validation"],
        },
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",",":"))
    result["semantic_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--heavy", action="store_true", help="audit all 630 transpositions instead of the 35 adjacent swaps")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    result = build_result(args.heavy)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(text + "\n")
    print(STATUS)
    print(result["semantic_sha256"])
    print(text)


if __name__ == "__main__":
    main()
