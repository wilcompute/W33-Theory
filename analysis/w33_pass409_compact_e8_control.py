#!/usr/bin/env python3
"""Pass 409: explicit two-control theorem in the compact real form of E8.

The diagonal-weld pass proves that a structured grade-one vector x and its
paired grade-two compact conjugate y generate the complex Chevalley algebra.
This verifier constructs the compact real basis explicitly, materializes the
two real controls A=x+y and B=i(x-y), and checks their 248 by 248 adjoint
matrices against the negative-definite compact Killing form.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_pass409_compact_e8_control.json"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest_matrix(matrix: np.ndarray) -> str:
    return hashlib.sha256(np.asarray(matrix, dtype="<i8").tobytes()).hexdigest()


def main(write: bool = True):
    dw = load(ROOT / "analysis/w33_diagonal_weld_e8_lie_generation.py", "diag")
    ri = load(ROOT / "analysis/w33_e8_split_real_form_involution.py", "realform")
    compiler, bridge, table = dw.load_inputs()
    amplitudes = dw.backgrounds(bridge)
    vectors = dw.source_generators(compiler, amplitudes)
    sc = json.loads((ROOT / "artifacts/e8_structure_constants_w33_discrete.json").read_text())

    roots = [tuple(map(int, r)) for r in sc["basis"]["roots"]]
    root_index = {r: 8 + i for i, r in enumerate(roots)}
    negative = {8 + i: root_index[tuple(-x for x in r)] for i, r in enumerate(roots)}
    phase = {}
    pair_killing = {}
    for a in range(8, 248):
        k = ri.killing(sc, a, negative[a])
        assert k in (-60, 60)
        phase[a] = -1 if k > 0 else 1
        pair_killing[a] = k
    assert all(phase[a] == phase[negative[a]] for a in phase)

    def sigma_real(v):
        out = {}
        for k, value in v.items():
            target, coefficient = (k, -value) if k < 8 else (negative[k], phase[k] * value)
            out[target] = out.get(target, 0) + coefficient
            if out[target] == 0:
                del out[target]
        return out

    checked = 0
    for a in range(247):
        for b in range(a + 1, 248):
            lhs = sigma_real(ri.bracket_vec(sc, {a: 1}, {b: 1}))
            rhs = ri.bracket_vec(sc, sigma_real({a: 1}), sigma_real({b: 1}))
            assert lhs == rhs
            checked += 1
    assert checked == 30628

    root_pairs = [(a, negative[a]) for a in range(8, 248) if a < negative[a]]
    assert len(root_pairs) == 120
    compact_basis = []
    for i in range(8):
        compact_basis.append(({}, {i: 1}, f"i*h{i}"))
    for a, b in root_pairs:
        c = phase[a]
        compact_basis.append(({a: 1, b: c}, {}, f"e{a}+({c})e{b}"))
        compact_basis.append(({}, {a: 1, b: -c}, f"i(e{a}-({c})e{b})"))
    assert len(compact_basis) == 248

    cartan_killing = np.array([[ri.killing(sc, i, j) for j in range(8)] for i in range(8)], dtype=np.int64)
    compact_killing = np.zeros((248, 248), dtype=np.int64)
    compact_killing[:8, :8] = -cartan_killing
    for i in range(8, 248):
        compact_killing[i, i] = -120
    assert np.all(np.linalg.eigvalsh(compact_killing.astype(float)) < -1e-9)

    def complex_bracket(u, v):
        ur, ui = u
        vr, vi = v
        rr = ri.bracket_vec(sc, ur, vr)
        ii = ri.bracket_vec(sc, ui, vi)
        ri1 = ri.bracket_vec(sc, ur, vi)
        ir1 = ri.bracket_vec(sc, ui, vr)
        real = dict(rr)
        for k, value in ii.items():
            real[k] = real.get(k, 0) - value
            if real[k] == 0:
                del real[k]
        imag = dict(ri1)
        for k, value in ir1.items():
            imag[k] = imag.get(k, 0) + value
            if imag[k] == 0:
                del imag[k]
        return real, imag

    def compact_coordinates(v):
        real, imag = v
        coords = [0] * 248
        for i in range(8):
            assert real.get(i, 0) == 0
            coords[i] = imag.get(i, 0)
        offset = 8
        for a, b in root_pairs:
            c = phase[a]
            ra, rb = real.get(a, 0), real.get(b, 0)
            ia, ib = imag.get(a, 0), imag.get(b, 0)
            assert rb == c * ra and ib == -c * ia
            coords[offset], coords[offset + 1] = ra, ia
            offset += 2
        return coords

    def adjoint_matrix(control):
        matrix = np.zeros((248, 248), dtype=np.int64)
        for j, (real, imag, _) in enumerate(compact_basis):
            matrix[:, j] = compact_coordinates(complex_bracket(control, (real, imag)))
        assert np.array_equal(matrix.T @ compact_killing + compact_killing @ matrix, np.zeros((248, 248), dtype=np.int64))
        return matrix

    results = {}
    for orientation in ("plus", "minus"):
        x = list(map(int, vectors[(1, orientation)]))
        y = [0] * 248
        for a, value in enumerate(x):
            if not value:
                continue
            if a < 8:
                y[a] -= value
            else:
                y[negative[a]] += phase[a] * value
        assert sigma_real({i: v for i, v in enumerate(x) if v}) == {i: v for i, v in enumerate(y) if v}
        control_a = ({i: x[i] + y[i] for i in range(248) if x[i] + y[i]}, {})
        control_b = ({}, {i: x[i] - y[i] for i in range(248) if x[i] - y[i]})
        coords_a = compact_coordinates(control_a)
        coords_b = compact_coordinates(control_b)
        ad_a, ad_b = adjoint_matrix(control_a), adjoint_matrix(control_b)
        ka = int(np.array(coords_a, dtype=np.int64) @ compact_killing @ np.array(coords_a, dtype=np.int64))
        kb = int(np.array(coords_b, dtype=np.int64) @ compact_killing @ np.array(coords_b, dtype=np.int64))
        kab = int(np.array(coords_a, dtype=np.int64) @ compact_killing @ np.array(coords_b, dtype=np.int64))
        closures = {}
        for prime in (103, 109):
            basis, _ = dw.closure((x, y), table, dw.ModularBasis(prime), prime)
            closures[str(prime)] = {
                "dimension": len(basis.rows),
                "grading": dw.grade_counts(sorted(basis.rows), compiler),
                "maximum_bracket_depth": max(basis.depths),
            }
            assert len(basis.rows) == 248
        results[orientation] = {
            "A_compact_coordinates": [[i, v] for i, v in enumerate(coords_a) if v],
            "B_compact_coordinates": [[i, v] for i, v in enumerate(coords_b) if v],
            "source_supports": {"x_grade1": sum(bool(v) for v in x), "sigma_x_grade2": sum(bool(v) for v in y)},
            "killing_gram_on_controls": [[ka, kab], [kab, kb]],
            "adjoint_A": {"shape": [248, 248], "nonzero": int(np.count_nonzero(ad_a)), "sha256_int64_le": digest_matrix(ad_a), "metric_skew": True},
            "adjoint_B": {"shape": [248, 248], "nonzero": int(np.count_nonzero(ad_b)), "sha256_int64_le": digest_matrix(ad_b), "metric_skew": True},
            "complex_closure_replays": closures,
        }
        assert ka < 0 and kb < 0 and ka * kb - kab * kab > 0

    out = {
        "schema": "w33.pass409.compact_e8_two_control.v1",
        "status": "PASS_TWO_EXPLICIT_COMPACT_REAL_CONTROLS_GENERATE_E8",
        "theorem": "For each diagonal H27 orientation, A=x+sigma(x) and B=i(x-sigma(x)) are explicit elements of compact e8. Their complex span recovers x and sigma(x); the certified complex Lie closure is E8_C, hence the real Lie algebra generated by A and B has dimension 248 and equals compact e8.",
        "compact_conjugation": {
            "cartan": "sigma(h_i)=-h_i",
            "roots": "sigma(e_alpha)=c_alpha e_-alpha with c_alpha=-sign K(e_alpha,e_-alpha)",
            "unordered_bracket_pairs_checked": checked,
            "fixed_basis_dimension": len(compact_basis),
            "fixed_root_plane_killing_values": [-120],
            "killing_inertia": {"positive": 0, "negative": 248, "zero": 0},
            "killing_sha256_int64_le": digest_matrix(compact_killing),
        },
        "controls": results,
        "rank_condition": "Lie_C<x,sigma(x)>=E8_C and x=(A-iB)/2, sigma(x)=(A+iB)/2. Therefore Lie_R<A,B> complexifies to E8_C. Since it lies in the 248D compact fixed form, it is compact e8.",
        "boundary": "This is exact algebraic controllability for two compact-real adjoint Hamiltonians. It does not set pulse amplitudes, drift, bandwidth, laboratory normalization, decoherence, or an experimental error threshold.",
        "parents": [
            "data/w33_diagonal_weld_e8_lie_generation.json",
            "data/w33_e8_split_real_form_involution.json",
            "artifacts/e8_structure_constants_w33_discrete.json",
        ],
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
