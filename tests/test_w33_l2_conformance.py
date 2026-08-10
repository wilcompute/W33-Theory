#!/usr/bin/env python3
"""The L2 conformance suite as executable properties.  Pass 4696.

Pass 4686 emitted 567 golden vectors and Pass 4687 ran them through a WebAssembly runtime.
Both check the SAME 567 pairs, which is exhaustive over the state space and therefore
complete -- but a table of input/output pairs tells an implementer nothing about WHY those
pairs, so a failing entry localises a bug to one frame and no further.

These are the algebraic properties the table is a consequence of.  A third-party
implementation can run them without reading the blueprint, and a failure names the broken
law rather than the broken row.

    py -3 -m pytest tests/test_w33_l2_conformance.py -q
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CERT = json.loads((ROOT / "data" / "w33_l2_conformance_vectors.json")
                  .read_text(encoding="utf-8"))
VECTORS = CERT["vectors"]
OPS = CERT["opcodes"]
F = 3
FRAMES = list(itertools.product(range(F), repeat=4))

# the reference implementation, rebuilt here so the test does not import the pass
GEN = {
    "F_p":   ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
    "F_f":   ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0)),
    "S_p":   ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
    "S_f":   ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1)),
    "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
    "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1)),
}
TRANSLATION = (1, 0, 0, 0)
# the symplectic form on GF(3)^4 as two hyperbolic planes (xp,zp | xf,zf)
J = ((0, 1, 0, 0), (2, 0, 0, 0), (0, 0, 0, 1), (0, 0, 2, 0))


def apply(op, v):
    if op == "Z_p":
        return tuple((v[i] + TRANSLATION[i]) % F for i in range(4))
    m = GEN[op]
    return tuple(sum(m[i][k] * v[k] for k in range(4)) % F for i in range(4))


def form(u, v):
    return sum(u[i] * J[i][k] * v[k] for i in range(4) for k in range(4)) % F


def test_golden_table_is_exhaustive():
    """Every (opcode, frame) pair appears exactly once -- 7 x 81 = 567."""
    seen = {(r["op"], tuple(r["in"])) for r in VECTORS}
    assert len(seen) == len(VECTORS) == len(OPS) * len(FRAMES) == 567


@pytest.mark.parametrize("op", sorted(GEN) + ["Z_p"])
def test_reference_matches_golden(op):
    """The reference agrees with the stored table on every frame."""
    for r in (r for r in VECTORS if r["op"] == op):
        assert apply(op, tuple(r["in"])) == tuple(r["out"]), (op, r["in"])


@pytest.mark.parametrize("op", sorted(GEN) + ["Z_p"])
def test_every_opcode_is_a_bijection(op):
    """No opcode may lose information: 81 inputs must give 81 distinct outputs."""
    assert len({apply(op, v) for v in FRAMES}) == len(FRAMES)


@pytest.mark.parametrize("op", sorted(GEN))
def test_linear_opcodes_preserve_the_symplectic_form(op):
    """The three-plus-three linear opcodes are symplectic, which is what makes them
    automorphisms of the geometry rather than arbitrary permutations."""
    for u, v in itertools.product(FRAMES[:27], FRAMES[:27]):
        assert form(apply(op, u), apply(op, v)) == form(u, v), (op, u, v)


@pytest.mark.parametrize("op", sorted(GEN))
def test_linear_opcodes_fix_the_origin(op):
    """A linear map fixes 0; only the translation may move it. This is the property that
    let Pass 2772 catch a frame register with no load port synthesising away."""
    assert apply(op, (0, 0, 0, 0)) == (0, 0, 0, 0)


def test_translation_moves_the_origin():
    """Z_p is the load port. If it fixed the origin the machine could not be loaded."""
    assert apply("Z_p", (0, 0, 0, 0)) != (0, 0, 0, 0)


def test_translation_has_order_three():
    v = (0, 0, 0, 0)
    for _ in range(F):
        v = apply("Z_p", v)
    assert v == (0, 0, 0, 0)


def test_minimal_trio_generates_the_full_symplectic_group():
    """F_p, CX_pf, CX_fp alone generate Sp(4,3) of order 51,840 -- the completeness claim
    at L2, verified by closure rather than cited."""
    I = tuple(tuple(int(i == j) for j in range(4)) for i in range(4))

    def mm(a, b):
        return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4)) % F
                           for j in range(4)) for i in range(4))

    gens = [GEN["F_p"], GEN["CX_pf"], GEN["CX_fp"]]
    seen, frontier = {I}, [I]
    while frontier:
        x = frontier.pop()
        for g in gens:
            y = mm(g, x)
            if y not in seen:
                seen.add(y)
                frontier.append(y)
    assert len(seen) == 51840


def test_affine_order_is_the_product():
    """51,840 linear x 81 translations = 4,199,040, the order quoted at L1."""
    assert 51840 * 81 == 4199040


def test_digest_matches_the_stored_table():
    """The certificate hashes what is on disk, per the project's certificate rule."""
    import hashlib
    d = hashlib.sha256(json.dumps(VECTORS, sort_keys=True,
                                  separators=(",", ":")).encode()).hexdigest()
    assert d == CERT["digest"]
