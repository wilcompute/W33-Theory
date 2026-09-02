#!/usr/bin/env python3
"""Materialize chain-level injections from both rank-two buildings into 1080.

Prior exact certificates identify two irreducible building-homology modules for
G=PSp4(3)~=U4(2):

  H1(W(3,3))      : dimension 81,
  H1(GQ(4,2))     : dimension 64.

The obstruction carrier 27 charts x 40 W33 lines contains three copies of each,
and six explicit primitive commutant projectors are already available.  This
script closes the remaining gap between character/multiplicity statements and
actual chain maps.

For each building it:
  1. forms the oriented Levi boundary d1:C1->C0 and an exact rational cycle
     basis Z=ker(d1);
  2. enumerates the complete source-chamber -> obstruction orbital Hom basis
     from the stabilizer of one chamber;
  3. for each of the three primitive target projectors, chooses the first
     orbital incidence map whose projected self-Gram is nonzero;
  4. constructs the projected chain map P X Z explicitly over Q;
  5. proves full column rank (81 or 64) modulo two good primes, verifies
     equivariance for the four deterministic generators, and freezes SHA256
     hashes of the integer numerators.

A nonzero equivariant map between irreducibles is an isomorphism, so the
self-Gram test is exact representation theory; the explicit matrices are an
independent chain-level materialization of those six isomorphisms.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
from functools import lru_cache
from pathlib import Path

import numpy as np
import sympy as sp

import w33_20260901_packet48_bt796_crossid as shell
import w33_20260901_obstruction_wedderburn_steinberg_projectors as obs
import w33_20260901_double_steinberg_64_81 as dual
from w33_20260901_steinberg_frame_common import build as build_frame
from w33_20260831_c5_wedderburn_kernel import center_equations, generic_center, mulvec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/PART_W33_20260901_BUILDING_CHAIN_INJECTIONS.json'
PRIMES = (1000003, 1000033)


def lcm_den(v):
    d = 1
    for q in v:
        d = math.lcm(d, int(sp.denom(q)))
    return d


def rank_mod(A, p):
    A = np.asarray(A, dtype=np.int64).copy() % p
    m, n = A.shape
    r = 0
    for c in range(n):
        nz = np.flatnonzero(A[r:, c])
        if not len(nz):
            continue
        z = r + int(nz[0])
        if z != r:
            A[[r, z]] = A[[z, r]]
        inv = pow(int(A[r, c]), -1, p)
        A[r] = (A[r] * inv) % p
        rows = np.flatnonzero(A[:, c])
        rows = rows[rows != r]
        for i in rows:
            A[i] = (A[i] - int(A[i, c]) * A[r]) % p
        r += 1
        if r == m:
            break
    return r


def integer_cycle_basis(nleft, nright, edges):
    B = sp.zeros(nleft + nright, len(edges))
    for j, (a, b) in enumerate(edges):
        B[a, j] = -1
        B[nleft + b, j] = 1
    ns = B.nullspace()
    Z = sp.Matrix.hstack(*ns)
    assert B * Z == sp.zeros(B.rows, Z.cols)
    assert Z.cols == len(edges) - (nleft + nright) + 1
    den = 1
    for q in Z:
        den = math.lcm(den, int(sp.denom(q)))
    Zi = np.array([[int(den * Z[i, j]) for j in range(Z.cols)] for i in range(Z.rows)], dtype=np.int64)
    # Primitive nullspace output for an incidence matrix should already be integral.
    g = 0
    for x in Zi.flat:
        g = math.gcd(g, abs(int(x)))
    if g > 1:
        Zi //= g
        den //= g
    assert all(rank_mod(np.asarray(B.tolist(), dtype=np.int64) @ Zi, p) == 0 for p in PRIMES)
    return Zi, den


def main():
    D = shell.build()
    pts, wlines, supports, charts, G = D['pts'], D['wlines'], D['supports'], D['charts'], D['G']
    assert (len(pts), len(wlines), len(supports), len(charts), len(G)) == (40, 40, 45, 27, 25920)

    F = build_frame()
    rel, reps, T, diag = F['rel'], F['reps'], F['T'], F['diag']
    acts = F['acts']
    frame81 = list(F['frame'])

    # Recover/split the degree-64 isotypic block in the same 59-orbital algebra.
    Zc = center_equations(T).nullspace()
    one = sp.zeros(59, 1)
    one[diag] = 1
    z, _L, _cp, factors, _coeff = generic_center(Zc, T)
    records, idempotents = obs.central_records(z, factors, T, one, diag)
    i64 = next(i for i, r in enumerate(records) if r['complexIrrepDegree'] == 64)
    E64 = idempotents[i64]
    split64_label, split64_vals, frame64, _left64 = dual.split_three_copies(E64, rel, reps, T, 64, diag)

    # Geometry action helpers.  shell.G elements are (p40,p45,p27).
    lidx = {frozenset(L): i for i, L in enumerate(wlines)}

    @lru_cache(maxsize=None)
    def line_perm(gi):
        p40 = G[gi][0]
        return tuple(lidx[frozenset(p40[x] for x in L)] for L in wlines)

    def target_one(gi, y):
        c, ell = divmod(y, 40)
        return G[gi][2][c] * 40 + line_perm(gi)[ell]

    # Check the four generator conventions agree with the obstruction algebra.
    gen_indices = []
    for a in acts:
        hit = None
        for gi in range(len(G)):
            ok = True
            for y in (0, 1, 39, 40, 217, 1079):
                if target_one(gi, y) != a[y]:
                    ok = False
                    break
            if ok and all(target_one(gi, y) == a[y] for y in range(1080)):
                hit = gi
                break
        assert hit is not None
        gen_indices.append(hit)

    wch = [(p, ell) for ell, L in enumerate(wlines) for p in L]
    fch = [(packet, c) for c, C in enumerate(charts) for packet in C]
    assert len(wch) == 160 and len(fch) == 135
    wi = {x: i for i, x in enumerate(wch)}
    fi = {x: i for i, x in enumerate(fch)}

    def wsrc_one(gi, s):
        p, ell = wch[s]
        return wi[(G[gi][0][p], line_perm(gi)[ell])]

    def fsrc_one(gi, s):
        packet, c = fch[s]
        return fi[(G[gi][1][packet], G[gi][2][c])]

    Z81, Z81den = integer_cycle_basis(40, 40, wch)
    Z64, Z64den = integer_cycle_basis(45, 27, fch)
    assert Z81.shape == (160, 81) and Z64.shape == (135, 64)

    zero59 = sp.zeros(59, 1)

    def source_orbit_data(source_n, source_one):
        base = 0
        transport = [None] * source_n
        H = []
        for gi in range(len(G)):
            s = source_one(gi, base)
            if transport[s] is None:
                transport[s] = gi
            if s == base:
                H.append(gi)
        assert all(x is not None for x in transport)
        assert len(H) == len(G) // source_n

        unseen = set(range(1080))
        orbits = []
        while unseen:
            y = min(unseen)
            O = {target_one(gi, y) for gi in H}
            unseen -= O
            orbits.append(tuple(sorted(O)))
        orbits.sort(key=lambda O: (len(O), O[0]))
        return transport, orbits

    def columns_for_orbit(transport, O):
        return [tuple(sorted(target_one(transport[s], y) for y in O)) for s in range(len(transport))]

    def selfgram_orbital(columns):
        row = np.zeros(1080, dtype=np.int64)
        for C in columns:
            if 0 in C:
                row[list(C)] += 1
        oval = [None] * 59
        for y, v in enumerate(row.tolist()):
            r = int(rel[0, y])
            if oval[r] is None:
                oval[r] = v
            else:
                assert oval[r] == v
        assert all(v is not None for v in oval)
        return sp.Matrix(oval)

    def projector_integer(P):
        den = lcm_den(P)
        coeff = np.array([int(den * q) for q in P], dtype=np.int64)
        return coeff[np.asarray(rel, dtype=np.int64)], den, coeff

    def source_generator_perm(source_n, source_one, gi):
        return np.array([source_one(gi, s) for s in range(source_n)], dtype=np.int64)

    def materialize(building, degree, source_n, source_one, cycle, cycle_den, frame):
        transport, orbits = source_orbit_data(source_n, source_one)
        col_cache = {}
        gram_cache = {}
        chosen = []
        for k, P in enumerate(frame):
            found = None
            for oi, O in enumerate(orbits):
                cols = col_cache.setdefault(oi, columns_for_orbit(transport, O))
                V = gram_cache.setdefault(oi, selfgram_orbital(cols))
                hit = mulvec(P, mulvec(V, P, T), T)
                if hit != zero59:
                    found = (oi, O, cols)
                    break
            assert found is not None
            oi, O, cols = found
            Pnum, Pden, coeff = projector_integer(P)
            # A = P X without forming X densely: each source column is the sum
            # of projector columns indexed by its target-orbit fibre.
            A = np.zeros((1080, source_n), dtype=np.int64)
            for s, C in enumerate(cols):
                A[:, s] = Pnum[:, list(C)].sum(axis=1)
            Y = A @ cycle
            ranks = {str(p): rank_mod(Y, p) for p in PRIMES if (Pden * cycle_den) % p}
            assert ranks and set(ranks.values()) == {degree}

            equiv = True
            for gi, gt in zip(gen_indices, acts):
                gs = source_generator_perm(source_n, source_one, gi)
                # Entrywise G-invariance of the intertwiner A.
                if not np.array_equal(A[np.ix_(np.array(gt, dtype=np.int64), gs)], A):
                    equiv = False
                    break
            assert equiv

            # The rational map is Y/(Pden*cycle_den).  Freeze canonical integer
            # numerator and enough metadata to reconstruct it exactly.
            h = hashlib.sha256(np.asarray(Y, dtype='<i8').tobytes()).hexdigest()
            chosen.append({
                'primitiveIndex': k,
                'sourceTargetOrbitalIndex': oi,
                'sourceStabilizerOrbitSize': len(O),
                'sourceStabilizerOrbitRepresentative': int(O[0]),
                'projectorDenominator': int(Pden),
                'cycleBasisDenominator': int(cycle_den),
                'rationalMapDenominator': int(Pden * cycle_den),
                'numeratorShape': list(Y.shape),
                'numeratorSHA256Int64LE': h,
                'rankModuloGoodPrimes': ranks,
                'generatorEquivarianceVerified': True,
                'projectorOrbitalCoefficients': [[i, int(coeff[i])] for i in range(59) if coeff[i]],
            })
        return {
            'building': building,
            'C1Chambers': source_n,
            'H1Dimension': degree,
            'sourceTargetHomOrbitalCount': len(orbits),
            'sourceStabilizerOrder': len(G) // source_n,
            'cycleBasisShape': list(cycle.shape),
            'cycleBasisDenominator': int(cycle_den),
            'cycleBasisSHA256Int64LE': hashlib.sha256(np.asarray(cycle, dtype='<i8').tobytes()).hexdigest(),
            'primitiveInjections': chosen,
        }

    W = materialize('W(3,3) Levi building', 81, 160, wsrc_one, Z81, Z81den, frame81)
    U = materialize('GQ(4,2) / cubic 27-line-45-tritangent Levi building', 64, 135, fsrc_one, Z64, Z64den, frame64)

    out = {
        'schema': 'w33.20260901.building-chain-injections.v1',
        'status': 'PASS',
        'groupOrder': 25920,
        'targetCarrier': '27 completion charts x 40 W33 lines = 1080',
        'split64Operator': split64_label,
        'split64Eigenvalues': [str(v) for v in split64_vals],
        'W33_H1_81': W,
        'GQ42_H1_64': U,
        'sixPrimitiveChainInjectionsMaterialized': len(W['primitiveInjections']) + len(U['primitiveInjections']) == 6,
        'theorem': (
            'Each of the three primitive degree-81 obstruction channels receives an explicit full-rank G-equivariant chain map from the 81-cycle space of the W(3,3) Levi building, and each of the three primitive degree-64 channels receives an explicit full-rank G-equivariant chain map from the 64-cycle space of the GQ(4,2)/cubic Levi building. Thus all six abstract multiplicity copies are now tied to concrete building cycles, not only to character multiplicities or central projectors.'
        ),
        'boundary': (
            'The maps are characteristic-zero finite-group intertwiners. Their primitive-channel labels depend on the deterministic rational projector frames. They are not physical propagation channels, particle generations, or continuum fields.'
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps({
        'status': 'PASS',
        'W33': [x['sourceTargetOrbitalIndex'] for x in W['primitiveInjections']],
        'GQ42': [x['sourceTargetOrbitalIndex'] for x in U['primitiveInjections']],
        'six': out['sixPrimitiveChainInjectionsMaterialized'],
    }, sort_keys=True))


if __name__ == '__main__':
    main()
