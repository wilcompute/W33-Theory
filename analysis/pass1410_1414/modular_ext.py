from __future__ import annotations

import collections
import itertools

import numpy as np

from pass1370_1374 import core, modular_radicals

from .common import SparseRank, capture, factor_kernel_key, sha


def simple_classes(g, p):
    tensor = np.asarray(g["tensor"], dtype=np.int64) % p
    left = [tensor[:, a, :] % p for a in range(83)]
    factors = modular_radicals.composition_factors(left, p)
    grouped = {}
    for F in factors:
        key = factor_kernel_key(F, p)
        grouped.setdefault(key, []).append(F)
    records = []
    for key, copies in grouped.items():
        F = copies[0]
        records.append({
            "degree": int(F[0].shape[0]),
            "regular_composition_multiplicity": len(copies),
            "factor": F,
            "kernel_key": key,
        })
    records.sort(key=lambda r: (r["degree"], r["kernel_key"]))
    for i, rec in enumerate(records):
        rec["index"] = i
    return tensor, factors, records


def hom_dimension(Fi, Fj, p):
    di = Fi[0].shape[0]
    dj = Fj[0].shape[0]
    rows = []
    for a in range(len(Fi)):
        for u in range(dj):
            for v in range(di):
                row = np.zeros(dj * di, dtype=np.int64)
                for k in range(dj):
                    row[k * di + v] += int(Fj[a][u, k])
                for l in range(di):
                    row[u * di + l] -= int(Fi[a][l, v])
                rows.append(row % p)
    rank = modular_radicals.rank(np.asarray(rows, dtype=np.int64), p)
    return di * dj - rank


def ext_dimension(tensor, Fi, Fj, p):
    """Compute Ext^1(S_i,S_j) as derivations modulo inner derivations."""
    di = Fi[0].shape[0]
    dj = Fj[0].shape[0]
    block = di * dj
    nvars = 83 * block
    ranker = SparseRank(p)

    def var(a, u, v):
        return a * block + u * di + v

    nz_products = {}
    for a in range(83):
        for b in range(83):
            nz = np.flatnonzero(tensor[:, a, b])
            nz_products[(a, b)] = [(int(c), int(tensor[c, a, b])) for c in nz]

    for a in range(83):
        Ra = Fj[a]
        for b in range(83):
            Rb = Fi[b]
            prod = nz_products[(a, b)]
            for u in range(dj):
                for v in range(di):
                    row = {}
                    for c, coeff in prod:
                        idx = var(c, u, v)
                        row[idx] = (row.get(idx, 0) + coeff) % p
                    for k in range(dj):
                        coeff = -int(Ra[u, k])
                        if coeff:
                            idx = var(b, k, v)
                            row[idx] = (row.get(idx, 0) + coeff) % p
                    for l in range(di):
                        coeff = -int(Rb[l, v])
                        if coeff:
                            idx = var(a, u, l)
                            row[idx] = (row.get(idx, 0) + coeff) % p
                    ranker.add(row)
    cocycle_dim = nvars - ranker.rank
    hom_dim = hom_dimension(Fi, Fj, p)
    inner_dim = di * dj - hom_dim
    ext_dim = cocycle_dim - inner_dim
    assert ext_dim >= 0
    return {
        "cocycle_dimension": cocycle_dim,
        "inner_dimension": inner_dim,
        "hom_dimension": hom_dim,
        "ext1_dimension": ext_dim,
    }


def analyze_prime(g, p):
    tensor, factors, simples = simple_classes(g, p)
    profile = modular_radicals.analyze_one(g, core, "full", p)
    split_dimension = sum(r["degree"] ** 2 for r in simples)
    assert split_dimension == profile["semisimple_quotient_dimension"]

    ext = []
    matrix = []
    for i, si in enumerate(simples):
        row = []
        for j, sj in enumerate(simples):
            rec = ext_dimension(tensor, si["factor"], sj["factor"], p)
            rec.update({"source": i, "target": j})
            ext.append(rec)
            row.append(rec["ext1_dimension"])
        matrix.append(row)

    vertices = []
    for rec in simples:
        vertices.append({
            "index": rec["index"],
            "simple_degree": rec["degree"],
            "regular_composition_multiplicity": rec["regular_composition_multiplicity"],
            "annihilator_codimension": 83 - len(rec["kernel_key"]),
            "annihilator_sha256": sha(rec["kernel_key"]),
        })
    arrows = [x for x in ext if x["ext1_dimension"]]
    return {
        "prime": p,
        "vertices": vertices,
        "vertex_count": len(vertices),
        "split_semisimple_dimension": split_dimension,
        "ext1_matrix_source_rows_target_columns": matrix,
        "arrows": arrows,
        "arrow_dimension_sum": sum(x["ext1_dimension"] for x in arrows),
        "radical_power_dimensions": profile["radical_power_dimensions"],
        "loewy_layers_top_to_socle": profile["loewy_layers_top_to_socle"],
        "loewy_length": profile["loewy_length"],
    }


def analyze():
    _public, cap = capture()
    g = cap["g"]
    primes = {str(p): analyze_prime(g, p) for p in (2, 3)}
    result = {
        "theorem": "Pass 1410 Exact Modular Gabriel Ext-Quivers",
        "algebra": "83-dimensional selector orbital algebra",
        "convention": "matrix entry (i,j) is dim Ext^1(S_i,S_j), hence arrows i -> j",
        "method": (
            "Simple modules are deduplicated by their exact annihilator kernels in the modular regular module. "
            "For every ordered pair, Ext^1 is computed as algebra derivations A -> Hom(S_i,S_j) modulo inner derivations, "
            "using all 83 basis products and sparse finite-field elimination."
        ),
        "primes": primes,
        "boundary": "The certificate gives the exact Gabriel Ext^1 quiver and Loewy dimensions. Higher quiver relations require Ext^2/Yoneda-product computation and are not inferred from Ext^1 alone.",
    }
    result["sha256"] = sha(result)
    return result
