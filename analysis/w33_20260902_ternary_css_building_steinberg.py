#!/usr/bin/env python3
"""Explicit characteristic-3 identification of the W33 CSS logical H1 with building homology.

The canonical W33 clique complex has

    C0 = 40, C1 = 240, C2 = 160, C3 = 40,

and over F3 the edge CSS logical quotient is

    H1 = ker(d1:C1->C0) / im(d2:C2->C1),  dim H1 = 81.

Independently the type-preserving W(3,3) Levi building has 40 point vertices,
40 line vertices and 160 chambers, hence cycle rank 160-80+1 = 81.  Its top
homology is the defining-characteristic Steinberg module.

This script constructs a natural F3 chain map from building chambers to clique
edges.  For a chamber (p,L), send it to the oriented three-edge star

    Phi(p,L) = sum_{q in L\{p}} [p -> q].

For a building cycle x, the clique boundary at a vertex r is

  sum_{L contains r} sum_{p in L\{r}} x_(p,L) - 3 sum_{L contains r} x_(r,L).

The second term vanishes in F3.  The line-cycle relation replaces the first
term by minus the point-cycle relation, so d1 Phi(x)=0.  We then verify
computationally that Phi has rank 81 on the building cycle space and that its
image is disjoint from the rank-120 triangle-boundary space.  Consequently

    ker d1 = im d2 direct-sum Phi(H1_building)

and the CSS logical quotient is explicitly isomorphic, as a PSp4(3)-module, to
building H1 / the modular Steinberg module.  Generator equivariance is checked
on the chain map itself, including orientation signs on clique edges.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import numpy as np

import w33_20260901_packet48_bt796_crossid as shell
from w33_20260901_building_chain_injections import integer_cycle_basis, rank_mod

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/PART_W33_20260902_TERNARY_CSS_BUILDING_STEINBERG.json'
P = 3


def signed_edge_image(g, edge, ei):
    a, b = edge
    u, v = g[a], g[b]
    if u < v:
        return ei[(u, v)], 1
    return ei[(v, u)], -1


def main():
    D = shell.build()
    pts, lines, G = D['pts'], D['wlines'], D['G']
    assert len(pts) == len(lines) == 40 and len(G) == 25920

    # Canonical oriented clique chain complex.
    edges = sorted({tuple(sorted((a, b))) for L in lines for a, b in itertools.combinations(L, 2)})
    tris = sorted({tuple(sorted(t)) for L in lines for t in itertools.combinations(L, 3)})
    assert (len(edges), len(tris)) == (240, 160)
    ei = {e: i for i, e in enumerate(edges)}

    d1 = np.zeros((40, 240), dtype=np.int64)
    for j, (a, b) in enumerate(edges):
        d1[a, j] = -1
        d1[b, j] = 1

    d2 = np.zeros((240, 160), dtype=np.int64)
    for j, (a, b, c) in enumerate(tris):
        d2[ei[(b, c)], j] += 1
        d2[ei[(a, c)], j] -= 1
        d2[ei[(a, b)], j] += 1

    assert np.all((d1 @ d2) % P == 0)
    r1 = rank_mod(d1, P)
    r2 = rank_mod(d2, P)
    assert (r1, r2) == (39, 120)
    ker_dim = 240 - r1
    assert ker_dim == 201 and ker_dim - r2 == 81

    # Type-preserving Levi building. Chambers are point-line incidences and are
    # oriented from point vertex to line vertex, so PSp action has no sign.
    chambers = [(p, ell) for ell, L in enumerate(lines) for p in L]
    assert len(chambers) == 160
    ci = {c: i for i, c in enumerate(chambers)}
    Z, Zden = integer_cycle_basis(40, 40, chambers)
    assert Zden == 1 and Z.shape == (160, 81) and rank_mod(Z, P) == 81

    # Phi(p,L) = sum_{q != p in L} oriented edge p->q.
    Phi = np.zeros((240, 160), dtype=np.int64)
    for s, (p, ell) in enumerate(chambers):
        for q in lines[ell]:
            if q == p:
                continue
            e = tuple(sorted((p, q)))
            Phi[ei[e], s] += 1 if p < q else -1

    Y = (Phi @ Z) % P
    assert np.all((d1 @ Y) % P == 0)
    image_rank = rank_mod(Y, P)
    combined_rank = rank_mod(np.concatenate([d2 % P, Y], axis=1), P)
    intersection_dim = r2 + image_rank - combined_rank
    assert image_rank == 81
    assert combined_rank == ker_dim == 201
    assert intersection_dim == 0

    # Strong chain-level equivariance.  A chamber is sent to another chamber
    # with coefficient +1. Clique edges acquire the orientation sign induced by
    # canonical increasing-vertex orientation.
    lidx = {frozenset(L): i for i, L in enumerate(lines)}
    g40s = D.get('g40')
    if g40s is None:
        # shell.G contains the exact group; recover the same deterministic four
        # generator actions from the obstruction scripts if the helper omits g40.
        import w33_20260901_obstruction_wedderburn_steinberg_projectors as obs
        acts, _charts, _lines = obs.build_action()
        # acts live on chart x line, so match them to exact G elements and take p40.
        g40s = []
        for a in acts:
            hit = next((z[0] for z in G if all((z[2][c] * 40 + lidx[frozenset(z[0][x] for x in lines[ell])]) == a[c * 40 + ell]
                                                for c, ell in ((0,0),(0,1),(1,0),(7,13),(26,39)))), None)
            assert hit is not None
            g40s.append(hit)
    assert len(g40s) >= 4

    equivariance_checks = 0
    for g in list(g40s)[:4]:
        lp = tuple(lidx[frozenset(g[x] for x in L)] for L in lines)
        sp = tuple(ci[(g[p], lp[ell])] for p, ell in chambers)
        ep = [signed_edge_image(g, e, ei) for e in edges]
        # Check target action * Phi == Phi * source action columnwise.
        for s in range(160):
            lhs = np.zeros(240, dtype=np.int64)
            nz = np.flatnonzero(Phi[:, s])
            for old in nz:
                new, sign = ep[int(old)]
                lhs[new] = (lhs[new] + sign * int(Phi[old, s])) % P
            rhs = Phi[:, sp[s]] % P
            assert np.array_equal(lhs % P, rhs)
            equivariance_checks += 1

    # Freeze a canonical quotient-coordinate certificate.  Since [d2|Y] has
    # rank 201 = dim ker d1, the 81 columns of Y are a concrete logical basis.
    ybytes = np.asarray(Y, dtype=np.int8).tobytes()
    zbytes = np.asarray(Z % P, dtype=np.int8).tobytes()
    out = {
        'schema': 'w33.20260902.ternary-css-building-steinberg.v1',
        'status': 'PASS',
        'field': 'F3',
        'cliqueComplex': {
            'C0': 40, 'C1': 240, 'C2': 160, 'C3': 40,
            'rank_d1': r1, 'rank_d2': r2, 'ker_d1_dimension': ker_dim,
            'H1_dimension': ker_dim - r2,
        },
        'building': {
            'pointVertices': 40, 'lineVertices': 40, 'chambers': 160,
            'H1_dimension': 81, 'cycleBasisRankMod3': rank_mod(Z, P),
        },
        'chainMap': {
            'formula': 'Phi(p,L)=sum_{q in L\\{p}} [p->q] over F3',
            'shape': [240, 160],
            'imageOnBuildingH1Rank': image_rank,
            'triangleBoundaryRank': r2,
            'combinedBoundaryPlusImageRank': combined_rank,
            'intersectionWithTriangleBoundaries': intersection_dim,
            'generatorEquivarianceChecks': equivariance_checks,
            'generatorEquivarianceVerified': True,
            'logicalBasisSHA256Int8Mod3': hashlib.sha256(ybytes).hexdigest(),
            'buildingCycleBasisSHA256Int8Mod3': hashlib.sha256(zbytes).hexdigest(),
        },
        'directSum': 'ker(d1) = im(d2) direct-sum Phi(H1_building) over F3',
        'theorem': (
            'The canonical [[240,81,3]]_3 W33 clique-chain CSS logical quotient is explicitly PSp4(3)-equivariantly isomorphic to the 81-dimensional H1 of the W(3,3) Levi building. The map sends each chamber (p,L) to the oriented three-edge star from p inside L. Thus the CSS logical module is the defining-characteristic modular Steinberg module, not merely an equal-dimensional 81-space.'
        ),
        'whyCharacteristicThreeMatters': (
            'The chain identity uses the vanishing of the coefficient 3 multiplying the chamber contribution at the source point. The same formula is not asserted to identify homology in other characteristics.'
        ),
        'boundary': (
            'This is an exact finite chain-complex and modular-representation statement. It does not by itself supply a fault-tolerance threshold, decoder, particle interpretation, or continuum field theory.'
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps({
        'status': 'PASS', 'rank_d2': r2, 'logical': image_rank,
        'combined': combined_rank, 'intersection': intersection_dim,
        'equivarianceChecks': equivariance_checks,
    }, sort_keys=True))


if __name__ == '__main__':
    main()
