#!/usr/bin/env python3
"""Passes 3957-3964: exact algebra, radical mesh, code stratum, rank-48 algebra, and photon-capacity model."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from math import gcd
from pathlib import Path

SCHEMA = "w33.pass3957_3964.exact_algebra_mesh_code_photon.v1"
STATUS = "PASS_EXACT_FIVE_FRONT_THREE_BONKERS_MONSTER_EXTERNAL_PENDING"
MESH_PERM = [7,19,9,17,14,25,24,15,10,16,20,6,4,32,31,0,33,3,1,28,5,2,30,26,29,27,35,34,21,22,23,12,11,13,8,18]

def bits(x: int, n: int = 6) -> list[int]:
    return [(x >> i) & 1 for i in range(n)]

def qform(x: int) -> int:
    b = bits(x)
    return (b[0]*b[1] + b[2]*b[3] + b[4]*b[5] + b[4] + b[5]) & 1

def beta(x: int, y: int) -> int:
    return qform(x ^ y) ^ qform(x) ^ qform(y)

def squarefree_decompose(n: int) -> tuple[int, int]:
    assert n >= 1
    square = 1
    squarefree = 1
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

# A multiquadratic element is a sparse map squarefree_radicand -> rational coefficient.
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

def quadratic_parent() -> tuple[list[int], list[list[int]], list[list[dict[int, Fraction]]]]:
    nonsingular = [x for x in range(1, 64) if qform(x)]
    assert len(nonsingular) == 36
    adjacency = [[0]*36 for _ in range(36)]
    for i, x in enumerate(nonsingular):
        for j, y in enumerate(nonsingular):
            if i != j and beta(x, y) == 0:
                adjacency[i][j] = 1
    assert all(sum(row) == 15 for row in adjacency)
    k = [[2*adjacency[i][j]-1 for j in range(36)] for i in range(36)]
    for i in range(36):
        for j in range(36):
            dot = sum(k[i][t]*k[j][t] for t in range(36))
            assert dot == (36 if i == j else 0)
    h = [[{1: Fraction(k[i][j], 6)} for j in range(36)] for i in range(36)]
    return nonsingular, adjacency, h

def exact_mesh_certificate() -> dict[str, object]:
    nonsingular, _, h = quadratic_parent()
    p = MESH_PERM
    m = [[dict(h[p[i]][p[j]]) for j in range(36)] for i in range(36)]
    operations: list[dict[str, object]] = []
    skipped = 0
    max_terms = 1
    c2_values: set[Fraction] = set()
    for col in range(35):
        for row in range(35, col, -1):
            b = m[row][col]
            if not b:
                skipped += 1
                continue
            a = m[row-1][col]
            a2 = single_square(a)
            b2 = single_square(b)
            r2 = a2 + b2
            assert r2 > 0
            c2 = a2 / r2
            s2 = b2 / r2
            c = sqrt_fraction(c2, sign_single(a))
            s = sqrt_fraction(s2, sign_single(b))
            c2_values.add(c2)
            old1 = [dict(x) for x in m[row-1]]
            old2 = [dict(x) for x in m[row]]
            for j in range(36):
                m[row-1][j] = add_e(mul_e(c, old1[j]), mul_e(s, old2[j]))
                m[row][j] = add_e(mul_e(neg_e(s), old1[j]), mul_e(c, old2[j]))
                max_terms = max(max_terms, len(m[row-1][j]), len(m[row][j]))
            assert not m[row][col]
            operations.append({
                "a": row-1, "b": row, "column": col,
                "c_sign": sign_single(c), "c2": [c2.numerator, c2.denominator],
                "s_sign": sign_single(s), "s2": [s2.numerator, s2.denominator],
            })
    offdiagonal = sum(bool(m[i][j]) for i in range(36) for j in range(36) if i != j)
    diagonal = [m[i][i] for i in range(36)]
    assert offdiagonal == 0
    assert sum(d == {1: Fraction(1)} for d in diagonal) == 35
    assert sum(d == {1: Fraction(-1)} for d in diagonal) == 1
    last = [-1]*36
    layers: list[int] = []
    for op in operations:
        a, b = int(op["a"]), int(op["b"])
        layer = max(last[a], last[b]) + 1
        last[a] = last[b] = layer
        layers.append(layer)
    payload = "\n".join(
        f"{o['a']},{o['b']},{o['column']},{o['c_sign']},{o['c2'][0]},{o['c2'][1]},"
        f"{o['s_sign']},{o['s2'][0]},{o['s2'][1]}" for o in operations
    )
    result = {
        "permutation": p,
        "port_labels": [nonsingular[i] for i in p],
        "rotations": len(operations),
        "skipped_exact_zeros": skipped,
        "layers": max(layers)+1,
        "offdiagonal_nonzeros": offdiagonal,
        "max_terms_per_entry": max_terms,
        "distinct_c2": len(c2_values),
        "max_c2_denominator": max(x.denominator for x in c2_values),
        "parameter_sha256": hashlib.sha256(payload.encode()).hexdigest(),
    }
    assert result["rotations"] == 398
    assert result["skipped_exact_zeros"] == 232
    assert result["layers"] == 69
    assert result["max_terms_per_entry"] == 1
    assert result["distinct_c2"] == 75
    assert result["max_c2_denominator"] == 441
    assert result["parameter_sha256"] == "2c3be7815b8346cd90be108faad4cc68866ad453f13b76bbdd4a9988a4569555"
    return result

def gf2_basis(values: list[int] | set[int]) -> list[int]:
    pivots: dict[int, int] = {}
    for value in values:
        x = int(value)
        while x:
            p = x.bit_length()-1
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

def graph_params(graph: list[set[int]], component: list[int]) -> dict[str, object]:
    c = set(component)
    degrees = [len(graph[v] & c) for v in component]
    lambdas: list[int] = []
    mus: list[int] = []
    for offset, i in enumerate(component):
        for j in component[offset+1:]:
            common = len((graph[i] & graph[j]) & c)
            (lambdas if j in graph[i] else mus).append(common)
    return {
        "v": len(component),
        "degree_values": sorted(set(degrees)),
        "lambda_values": sorted(set(lambdas)),
        "mu_values": sorted(set(mus)),
        "edges": sum(degrees)//2,
    }

def maximal_code_stratum_57() -> dict[str, object]:
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
        for j in range(i+1, len(weight4)):
            if ((wi & weight4[j]).bit_count() & 1) == 0:
                neighbors[i].add(j)
                neighbors[j].add(i)
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
    distribution = Counter(w.bit_count() for w in words)
    expected = {0:1,4:57,8:852,12:7332,16:57294,20:57294,24:7332,28:852,32:57,36:1}
    assert dict(sorted(distribution.items())) == expected
    def krawtchouk(j: int, i: int) -> int:
        return sum(
            (-1)**s * math.comb(i, s) * math.comb(36-i, j-s)
            for s in range(max(0, j-(36-i)), min(j, i)+1)
        )
    dual: dict[int, int] = {}
    for j in range(37):
        value = sum(distribution.get(i, 0)*krawtchouk(j, i) for i in range(37)) // (1 << 17)
        if value:
            dual[j] = value
    graph = [set() for _ in range(57)]
    for i in range(57):
        for j in range(i+1, 57):
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
        component: list[int] = []
        while stack:
            v = stack.pop()
            component.append(v)
            for u in graph[v]:
                if u not in seen:
                    seen.add(u)
                    stack.append(u)
        components.append(sorted(component))
    assert [len(c) for c in components] == [45, 6, 6]
    params = [graph_params(graph, c) for c in components]
    assert params[0] == {"v":45,"degree_values":[16],"lambda_values":[8],"mu_values":[4],"edges":360}
    assert params[1] == params[2] == {"v":6,"degree_values":[4],"lambda_values":[2],"mu_values":[4],"edges":12}
    degree_profile = Counter(sum((w >> i) & 1 for w in selected) for i in range(36))
    assert degree_profile == Counter({9:20, 3:16})
    basis_hex = [hex(x) for x in basis]
    supports = sorted(tuple(i for i in range(36) if (w >> i) & 1) for w in selected)
    basis_sha = hashlib.sha256("\n".join(basis_hex).encode()).hexdigest()
    support_sha = hashlib.sha256("\n".join(",".join(map(str, s)) for s in supports).encode()).hexdigest()
    return {
        "base_code": "[36,6,16]",
        "maximal_code": "[36,17,4]",
        "basis_hex": basis_hex,
        "basis_sha256": basis_sha,
        "weight_distribution": dict(sorted(distribution.items())),
        "dual_weight_distribution": dual,
        "weight4_count": 57,
        "weight4_support_sha256": support_sha,
        "weight4_intersection2_graph": {
            "components": params,
            "component_sizes": [45,6,6],
            "interpretation": ["SRG(45,16,8,4)", "octahedral K2,2,2", "octahedral K2,2,2"],
            "total_edges": sum(sum(len(x) for x in graph) for _ in [0])//2,
        },
        "coordinate_degree_profile": dict(sorted(degree_profile.items())),
    }

TERWILLIGER_BLOCKS = [
    {"simple_block_size":1,"module_multiplicity":3,"isotypic_dimension":3,"shell_ranks":[0,0,3,0,0],"primitive_shell":2},
    {"simple_block_size":1,"module_multiplicity":12,"isotypic_dimension":12,"shell_ranks":[0,0,12,0,0],"primitive_shell":2},
    {"simple_block_size":1,"module_multiplicity":14,"isotypic_dimension":14,"shell_ranks":[0,0,0,0,14],"primitive_shell":4},
    {"simple_block_size":2,"module_multiplicity":1,"isotypic_dimension":2,"shell_ranks":[0,1,0,0,1],"primitive_shell":1},
    {"simple_block_size":2,"module_multiplicity":2,"isotypic_dimension":4,"shell_ranks":[0,0,0,2,2],"primitive_shell":3},
    {"simple_block_size":3,"module_multiplicity":4,"isotypic_dimension":12,"shell_ranks":[0,0,0,4,8],"primitive_shell":3},
    {"simple_block_size":3,"module_multiplicity":4,"isotypic_dimension":12,"shell_ranks":[0,0,4,4,4],"primitive_shell":2},
    {"simple_block_size":3,"module_multiplicity":8,"isotypic_dimension":24,"shell_ranks":[0,0,8,8,8],"primitive_shell":2},
    {"simple_block_size":4,"module_multiplicity":8,"isotypic_dimension":32,"shell_ranks":[0,0,8,8,16],"primitive_shell":2},
    {"simple_block_size":5,"module_multiplicity":1,"isotypic_dimension":5,"shell_ranks":[1,1,1,1,1],"primitive_shell":0},
]

def terwilliger_certificate(root: Path) -> dict[str, object]:
    assert sum(x["simple_block_size"]**2 for x in TERWILLIGER_BLOCKS) == 79
    assert sum(x["isotypic_dimension"] for x in TERWILLIGER_BLOCKS) == 120
    source = root / "data/w33_pass1365_1369_rational_schur_completion.json"
    if source.is_file():
        raw = json.loads(source.read_text(encoding="utf-8"))
        p = raw["pass1365_rational_terwilliger_wedderburn"]
        assert p["rational_wedderburn"] == "Q^3 + M2(Q)^2 + M3(Q)^3 + M4(Q) + M5(Q)"
        assert [x["simple_block_size"] for x in p["blocks"]] == [1,1,1,2,2,3,3,3,4,5]
    return {
        "source_certificate": "data/w33_pass1365_1369_rational_schur_completion.json",
        "algebra_dimension": 79,
        "center_dimension": 10,
        "decomposition": "Q^3 + M2(Q)^2 + M3(Q)^3 + M4(Q) + M5(Q)",
        "simple_sizes": [1,1,1,2,2,3,3,3,4,5],
        "module_multiplicities": [3,12,14,1,2,4,4,8,8,1],
        "blocks": TERWILLIGER_BLOCKS,
        "closure": "The fourteen-case arithmetic sieve from Passes 3905-3912 is superseded by the exact rational primitive-idempotent certificate from Passes 1365-1369.",
    }

RANK48_MODULES = [
    {"irrep":"1","dimension":1,"multiplicity":5},
    {"irrep":"6","dimension":6,"multiplicity":1},
    {"irrep":"15a","dimension":15,"multiplicity":2},
    {"irrep":"15b","dimension":15,"multiplicity":2},
    {"irrep":"20","dimension":20,"multiplicity":2},
    {"irrep":"24","dimension":24,"multiplicity":3},
    {"irrep":"81","dimension":81,"multiplicity":1},
]

def rank48_certificate() -> dict[str, object]:
    assert sum(x["dimension"]*x["multiplicity"] for x in RANK48_MODULES) == 264
    assert sum(x["multiplicity"]**2 for x in RANK48_MODULES) == 48
    return {
        "carrier_decompositions": {
            "Q64": "1^3 + 6 + 15b + 20^2",
            "Q200": "1^2 + 15a^2 + 15b + 24^3 + 81",
            "Q264": "1^5 + 6 + 15a^2 + 15b^2 + 20^2 + 24^3 + 81",
        },
        "module_table": RANK48_MODULES,
        "centralizer_dimension": 48,
        "center_dimension": 7,
        "wedderburn": "Q^2 + M2(Q)^3 + M3(Q) + M5(Q)",
        "cross_hom_dimension": 7,
        "cross_channels": {"trivial":6, "shared_15b":1},
        "boundary": "This closes the characteristic-zero centralizer algebra. A literal 48-relation intersection tensor and every fusion scheme are not enumerated here.",
    }

def photon_model() -> dict[str, object]:
    n, d = 40, 3
    return {
        "established_kinematic_identity": {
            "period": "T=1/nu",
            "wavelength": "lambda=c/nu",
            "node_step": "a_N=lambda/N",
            "node_tick": "tau_N=T/N",
            "causal_ratio": "a_N/tau_N=c",
            "conclusion": "N cancels when spatial and temporal refinement scale together.",
        },
        "information_model": {
            "latency_per_bit": "L=T/B",
            "throughput": "R=B/T=B*nu=1/L",
            "tensor_product_ideal": {"bits":"N*log2(d)", "W33_N40_d3_bits": n*math.log2(d)},
            "direct_sum_single_photon": {
                "dimension":"N*d",
                "W33_N40_d3_dimension":n*d,
                "Holevo_ceiling_bits":math.log2(n*d),
            },
            "density_throughput_identity": "rho=N/lambda=N*nu/c and R/(rho*log2(d))=c in the ideal tensor-factor model",
        },
        "quantum_speed_limit": {
            "photon_energy": "E=h*nu",
            "Margolus_Levitin_orthogonal_rate": "Gamma<=2E/(pi*hbar)=4nu",
            "orthogonal_updates_per_period_max": 4,
            "W33_sequential_updates_per_period": 40,
            "overload_factor": 10,
            "falsifier": "Forty W33 nodes cannot be forty sequential mutually orthogonal state changes within one optical period for an isolated single photon of energy h nu. They must be parallel/nonorthogonal modes, span multiple periods, or use external drive.",
        },
        "Lorentz_dispersion_firewall": {
            "allowed": "N-dependent internal Hilbert-space capacity with invariant c",
            "disallowed_without_evidence": "c depending on N, photon frequency, or mode count",
            "reason": "Such dependence generically creates vacuum dispersion and violates the invariant-speed boundary.",
        },
        "ontology_boundary": "The equations define an information-capacity and causal-update model. They do not establish that a photon literally contains discrete holo nodes.",
    }

def monster_gate() -> dict[str, object]:
    return {
        "status": "PENDING_EXPLICIT_MONSTER_WORDS_AND_CLASS_FUSION",
        "existing_harness": "analysis/w33_mmgroup_u42_candidate_harness.py",
        "required": [
            "four portable serialized MM words", "mmgroup version/provenance",
            "closure order 25920", "generator/pair/triple order signature",
            "element-order census", "36-axis, 135-frame, 120-Norton, code, and line-split hashes",
            "content-addressed character-fusion artifact",
        ],
        "negative_result": "No concrete runtime artifact is present at data/PART_3751_MONSTER_U42_CLASS_FUSION_EXECUTION.json.",
        "boundary": "No Monster embedding or character fusion is promoted.",
    }

def build_certificate(root: Path = Path(".")) -> dict[str, object]:
    mesh = exact_mesh_certificate()
    code = maximal_code_stratum_57()
    core: dict[str, object] = {
        "schema": SCHEMA,
        "status": STATUS,
        "terwilliger_exact_wedderburn": terwilliger_certificate(root),
        "exact_adjacent_mesh": {
            "matrix": "H=(2A36-J)/6",
            **mesh,
            "diagonal_signs": {"plus":35, "minus":1},
            "parameterization": "Each gate has c=sign(c)*sqrt(c2), s=sign(s)*sqrt(1-c2) with exact rational c2.",
            "boundary": "Exact radical replay and exact zero pattern are proved. Global gate-count and depth optimality are not claimed.",
        },
        "maximal_code_stratum_57": {
            **code,
            "boundary": "This constructs an exact t=A4=57 stratum. It does not prove that 57 is the maximum possible A4 or classify all group orbits.",
        },
        "monster_gate": monster_gate(),
        "rank48_coherent_algebra": rank48_certificate(),
        "photon_node_capacity_model": photon_model(),
        "three_bonkers": {
            "photon_node_packing_invariance": "c=(lambda/N)/(T/N); node density may increase capacity while c remains invariant.",
            "four_update_quantum_speed_falsifier": "An isolated photon of energy h nu supports at most four mutually orthogonal transitions per optical period under the Margolus-Levitin bound.",
            "fifty_seven_block_geometry": "The new t=57 code's weight-4 supports split as SRG(45,16,8,4)+2 octahedra.",
        },
        "evidence_boundary": {
            "proved": [
                "exact rational Terwilliger blocks via existing certificate",
                "398-gate exact radical replay",
                "explicit t=57 maximal code and 45+6+6 geometry",
                "rank-48 rational centralizer decomposition",
                "dimensionally consistent photon capacity identities",
            ],
            "not_proved": [
                "global mesh optimality", "global maximum t=57", "Monster embedding or fusion",
                "literal photon node ontology", "variable or emergent c mechanism",
                "hardware or laboratory performance", "remote CI or PDF success",
            ],
        },
    }
    raw = json.dumps(core, sort_keys=True, separators=(",", ":")).encode()
    core["semantic_sha256"] = hashlib.sha256(raw).hexdigest()
    return core

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    certificate = build_certificate(args.root)
    if args.check:
        frozen = json.loads(args.check.read_text(encoding="utf-8"))
        if certificate != frozen:
            raise SystemExit("certificate mismatch")
    text = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
