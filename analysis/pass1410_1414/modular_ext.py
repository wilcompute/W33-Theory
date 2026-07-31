from __future__ import annotations

import numpy as np

from pass1370_1374 import core, modular_radicals

from .common import capture, factor_kernel_key, sha


def simple_classes(g, p):
    tensor = np.asarray(g["tensor"], dtype=np.int64) % p
    left = [tensor[:, a, :] % p for a in range(83)]
    factors = modular_radicals.composition_factors(left, p)
    grouped = {}
    for F in factors:
        grouped.setdefault(factor_kernel_key(F, p), []).append(F)
    records = []
    for key, copies in grouped.items():
        records.append({
            "degree": int(copies[0][0].shape[0]),
            "regular_composition_multiplicity": len(copies),
            "factor": copies[0],
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
    return di * dj - modular_radicals.rank(np.asarray(rows, dtype=np.int64), p)


def multiplication_support(tensor):
    out = {}
    for a in range(83):
        for b in range(83):
            nz = np.flatnonzero(tensor[:, a, b])
            out[a, b] = [(int(c), int(tensor[c, a, b])) for c in nz]
    return out


def rank_derivation_rows_p2(row_iter):
    pivots = {}
    for terms in row_iter:
        bits = 0
        for index, coefficient in terms:
            if coefficient & 1:
                bits ^= 1 << index
        while bits:
            column = (bits & -bits).bit_length() - 1
            pivot = pivots.get(column)
            if pivot is None:
                pivots[column] = bits
                break
            bits ^= pivot
    return len(pivots)


def rank_derivation_rows_p3(row_iter, nvars):
    pivots = {}
    for terms in row_iter:
        row = np.zeros(nvars, dtype=np.int8)
        for index, coefficient in terms:
            row[index] = (int(row[index]) + coefficient) % 3
        while np.any(row):
            column = int(np.flatnonzero(row)[0])
            pivot = pivots.get(column)
            if pivot is None:
                if row[column] == 2:
                    row = (-row) % 3
                pivots[column] = row
                break
            row = (row - int(row[column]) * pivot) % 3
    return len(pivots)


def ext_dimension(tensor, support, Fi, Fj, p):
    di = Fi[0].shape[0]
    dj = Fj[0].shape[0]
    block = di * dj
    nvars = 83 * block

    def var(a, u, v):
        return a * block + u * di + v

    def rows():
        for a in range(83):
            left = Fj[a]
            for b in range(83):
                right = Fi[b]
                product = support[a, b]
                for u in range(dj):
                    for v in range(di):
                        terms = [(var(c, u, v), coefficient) for c, coefficient in product]
                        terms.extend((var(b, k, v), -int(left[u, k])) for k in range(dj) if left[u, k])
                        terms.extend((var(a, u, l), -int(right[l, v])) for l in range(di) if right[l, v])
                        yield terms

    rank = rank_derivation_rows_p2(rows()) if p == 2 else rank_derivation_rows_p3(rows(), nvars)
    cocycle_dimension = nvars - rank
    hom = hom_dimension(Fi, Fj, p)
    inner_dimension = di * dj - hom
    ext1_dimension = cocycle_dimension - inner_dimension
    assert ext1_dimension >= 0
    return {
        "cocycle_dimension": cocycle_dimension,
        "inner_dimension": inner_dimension,
        "hom_dimension": hom,
        "ext1_dimension": ext1_dimension,
    }


def analyze_prime(g, p):
    tensor, _factors, simples = simple_classes(g, p)
    support = multiplication_support(tensor)
    profile = modular_radicals.analyze_one(g, core, "full", p)
    for rec in simples:
        rec["endomorphism_field_dimension"] = hom_dimension(rec["factor"], rec["factor"], p)
        numerator = rec["degree"] ** 2
        assert numerator % rec["endomorphism_field_dimension"] == 0
        rec["semisimple_component_dimension"] = numerator // rec["endomorphism_field_dimension"]
    semisimple_dimension = sum(r["semisimple_component_dimension"] for r in simples)
    assert semisimple_dimension == profile["semisimple_quotient_dimension"]

    ext = []
    matrix = []
    for i, source in enumerate(simples):
        row = []
        for j, target in enumerate(simples):
            record = ext_dimension(tensor, support, source["factor"], target["factor"], p)
            record.update({"source": i, "target": j})
            ext.append(record)
            row.append(record["ext1_dimension"])
        matrix.append(row)

    vertices = []
    for rec in simples:
        vertices.append({
            "index": rec["index"],
            "simple_degree_over_base_field": rec["degree"],
            "endomorphism_field_dimension": rec["endomorphism_field_dimension"],
            "semisimple_component_dimension": rec["semisimple_component_dimension"],
            "regular_composition_multiplicity": rec["regular_composition_multiplicity"],
            "annihilator_codimension": 83 - len(rec["kernel_key"]),
            "annihilator_sha256": sha(rec["kernel_key"]),
        })
    arrows = [record for record in ext if record["ext1_dimension"]]
    return {
        "prime": p,
        "vertices": vertices,
        "vertex_count": len(vertices),
        "semisimple_quotient_dimension_reconstructed": semisimple_dimension,
        "all_simple_endomorphism_fields_split": all(x["endomorphism_field_dimension"] == 1 for x in vertices),
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
            "Simple modules are deduplicated by exact annihilator kernels and their endomorphism fields reconstruct the semisimple quotient without a splitness assumption. "
            "Every Ext^1 space is computed as derivations modulo inner derivations using all 83 basis products. "
            "GF(2) elimination is bit-packed and GF(3) elimination is vectorized."
        ),
        "primes": primes,
        "boundary": "The certificate gives the exact Gabriel Ext^1 quiver and Loewy dimensions. Higher quiver relations require Ext^2/Yoneda products.",
    }
    result["sha256"] = sha(result)
    return result
