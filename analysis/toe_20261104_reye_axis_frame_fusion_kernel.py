#!/usr/bin/env python3
"""Exact 25 packet -> 60 icosian-axis frame fusion: rank 17 and 8 blind modes.

Use 25 tangent-plane Reye packets (inscribed 24cells) vs 60 600cell
antipodal axes. Each axis meets five packet sites one-per-row/column,
a literal A5 permutation pattern. The 25x60 incidence M has
M M^T spectrum 60^(1),15^(16),0^(8) and exact row/column
zero-sum 8D kernel. Orbit of 600 3-cell triples sharing a single axis
is 60*C(5,3), in one-to-one correspondence with axis/3-subset data.

These are finite algebra/combinatorics, not a physically realized E8
H1, self-entanglement, gravity, or 8 independent gauge photons.
"""
from __future__ import annotations
import collections,itertools,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT/"analysis") not in sys.path:sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261104_pg34_icosian_quadric import geometry
OUT=ROOT/"data"/"toe_20261104_reye_axis_frame_fusion_kernel.json"
def main():
    pg=geometry()
    rows=pg["reye_tangent_plane_records_25"]
    M=np.zeros((25,60),dtype=np.int64)
    for rec in rows:
        for a in rec["incidence_axes"]:M[rec["cell_id"],a]=1
    assert np.all(M.sum(axis=0)==5)
    assert np.all(M.sum(axis=1)==12)
    K=M@M.T
    assert np.all(np.diag(K)==12)
    assert collections.Counter(K[i,j] for i in range(25) for j in range(i+1,25))=={0:100,3:200}
    e=np.eye(25,dtype=np.int64)
    assert not np.any(K@(K-15*e)@(K-60*e))
    from sympy import Matrix
    rank=Matrix(M).rank()
    assert rank==17
    assert Matrix(K).rank()==17
    eig=np.linalg.eigvalsh(K)
    assert sum(abs(v)<1e-8 for v in eig)==8
    assert sum(abs(v-15)<1e-8 for v in eig)==16
    assert sum(abs(v-60)<1e-8 for v in eig)==1
    coords=[tuple(x) for x in pg["cell_grid_locations_25"]]
    assert set(coords)==set(itertools.product(range(5),repeat=2))
    B=np.zeros((25,8),dtype=np.int64)
    for idx,(r,c) in enumerate(coords):
        for k in range(4):
            B[idx,k]=(int(r==k+1)-int(r==0))
            B[idx,k+4]=(int(c==k+1)-int(c==0))
    assert Matrix(B).rank()==8
    assert not np.any(M.T@B)
    assert not np.any(K@B)
    triple_axes=collections.Counter()
    for axis in range(60):
        cells=tuple(np.flatnonzero(M[:,axis]).tolist())
        assert len(cells)==5
        assert len({coords[i][0] for i in cells})==5
        assert len({coords[i][1] for i in cells})==5
        for combo in itertools.combinations(cells,3):
            triple_axes[combo]+=1
    assert len(triple_axes)==600 and set(triple_axes.values())=={1}
    # The 600 triple-patterns are exactly those threefold intersections
    # of at least one 600-cell antipodal axis (2 vertices).
    assert all(sum(M[i,axis] for i in tri)==3 for axis in range(60)
             for tri in itertools.combinations(np.flatnonzero(M[:,axis]),3))
    out=dict(status="PASS_REYE_25_X_60_FRAME_FUSION_EIGHT_BLIND_DIRECTIONS",
        packet_rows=25,icosian_axis_columns=60,incidences=300,
        packet_degree12=True,axis_degree5=True,
        exact_integer_Gram_eigen_polynomial="K(K-15I)(K-60I)=0, K=M M^T",
        Gram_eigenvalues={"0":8,"15":16,"60":1},
        binary_matrix_rank_over_Q=rank,
        eight_dimensional_nullspace_from_row_col_zero_sum=True,
        nullspace_dimension=8,
        all_8_explicit_kernel_vectors_25_entries=B.T.tolist(),
        invariant_uniform_mode_eigenvalue=60,
        other_16_active_modes_eigenvalue=15,
        active_singular_values=[float(np.sqrt(15)),float(np.sqrt(60))],
        condition_on_nonzero_singular_values=2,
        triple_intersections_on_one_axis=600,
        exactly_one_axis_per_shared_triple=True,
        correspondence="600 triples = 60 axes x choose(5,3) ten triples for each axis; all 600 distinct. Every axis picks one 24cell in each 5x5 row/column.",
        interpretation="The naive 25 packet amplitude ->60 axis co-occurrence M^T is not injective; its kernel is exactly four zero-sum row potentials plus four zero-sum column potentials. This is a geometric frame-fusion no-go. The number 8 matches E8 rank but no canonical E8 isomorphism/physical gauge is established.",
        predecessor="Denney et al 2020 25x5x5 H4 incidence (prior art), current 2026-11-04 exact PG34/25 Reye producer. This is independent integer singular-spectrum and explicit kernel certificate.",
        physics_limit="No physical photonic Hamiltonian, no numerical chiral generation selection, no natural-to-W33 C3 equivariant map.")
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(out["status"],"rank",rank,"kernel",8,"triples",len(triple_axes),flush=True)
    return out
if __name__=="__main__":main()
