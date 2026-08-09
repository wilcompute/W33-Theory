#!/usr/bin/env python3
"""Pass 4539 -- exact local linear decoder for the full protected H10 space.

Pass 4534 gave a nine-spoke basis for the edge-accessible V9. Pass 4536 proves
one line-star supplies the missing coefficient-parity direction. Together these
ten local vectors form a basis of H10=im(A_*).

This pass finds ten ambient readout coordinates on which that basis restricts to
an invertible 10x10 matrix, freezes its inverse, and exhausts all 1024 protected
vectors.  Thus ten sampled bits reconstruct the full 40-bit protected vector;
the first decoded coordinate is exactly the missing parity bit and the remaining
nine are local spoke coordinates.

The separate eight-state Borel equitable quotient is intentionally not called a
decoder: it preserves orbit-constant transfer/spectral information but collapses
240 edge identities to eight states.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from w33_apartment_section_core import build_geometry,rank2

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4539_EXACT_LOCAL_H10_DECODER.json'
SPOKES=[1,2,3,4,5,7,8,28,32]
EXPECTED_ROWS=[0,1,2,3,4,5,7,8,10,11]
EXPECTED_INV=[
 [1,1,1,1,0,0,0,0,0,0],
 [0,1,1,1,0,0,0,1,0,1],
 [0,0,0,1,0,0,0,1,0,1],
 [0,0,1,0,0,0,0,1,0,1],
 [0,1,1,1,0,1,0,0,0,0],
 [0,1,1,1,1,0,0,0,0,0],
 [0,1,1,1,0,0,0,1,0,0],
 [0,1,1,1,0,0,1,0,0,0],
 [0,1,1,1,1,0,1,1,1,1],
 [1,0,1,1,0,1,0,1,1,0],
]

def inv2(M):
    M=np.asarray(M,dtype=np.uint8);n=M.shape[0]
    X=np.hstack((M.copy(),np.eye(n,dtype=np.uint8)))
    for c in range(n):
        r=next(i for i in range(c,n) if X[i,c]);X[[c,r]]=X[[r,c]]
        for i in range(n):
            if i!=c and X[i,c]:X[i]^=X[c]
    return X[:,n:]

def greedy_rows(M):
    rows=[];cur=np.zeros((0,M.shape[1]),dtype=np.uint8);r=0
    for i in range(M.shape[0]):
        T=np.vstack((cur,M[i]));rr=rank2(T)
        if rr>r:rows.append(i);cur=T;r=rr
        if r==M.shape[1]:break
    return rows

def main():
    *_x,A=build_geometry()[:6]
    center=A[:,0]
    spoke=[A[:,0]^A[:,j] for j in SPOKES]
    M=np.column_stack([center]+spoke).astype(np.uint8)
    assert rank2(M)==10
    rows=greedy_rows(M);assert rows==EXPECTED_ROWS
    S=M[rows,:];Sinv=inv2(S)
    assert Sinv.tolist()==EXPECTED_INV
    assert np.array_equal((Sinv@S)%2,np.eye(10,dtype=np.uint8))
    for mask in range(1<<10):
        c=np.array([(mask>>i)&1 for i in range(10)],dtype=np.uint8)
        y=(M@c)%2; dec=(Sinv@y[rows])%2
        assert np.array_equal(dec,c)
        assert np.array_equal((M@dec)%2,y)
        # Only the first basis vector has odd coefficient parity.
        assert int(dec[0])==int(c[0])
    c4535=json.loads((ROOT/'data/PART_W33_PASS4535_BOREL_EDGE_TRANSFER_QUOTIENT.json').read_text())
    orbit_sizes=c4535['orbit_sizes']
    assert len(orbit_sizes)==8 and sum(orbit_sizes)==240 and max(orbit_sizes)>1
    out={
      'pass':4539,'protected_dimension':10,
      'local_basis':{'parity_line_star':[0],'nine_spokes':[[0,j] for j in SPOKES]},
      'sample_rows':rows,'sample_count':10,
      'restricted_basis_matrix':S.astype(int).tolist(),
      'decoder_inverse':Sinv.astype(int).tolist(),
      'decoder_xor_fanins':Sinv.sum(axis=1).astype(int).tolist(),
      'decoder_total_xor_inputs':int(Sinv.sum()),
      'exhausted_protected_vectors':1024,
      'first_decoded_bit':'coefficient parity pi from Pass 4536',
      'remaining_decoded_bits':'nine local Borel-cell spoke coordinates spanning V9',
      'eight_state_boundary':{'edge_states':240,'borel_orbits':8,'orbit_sizes':orbit_sizes,
        'statement':'The equitable quotient preserves orbit-constant spectral transfer but loses within-orbit identity; it is not the full linear decoder.'},
      'theorem':'Ten ambient protected bits decode all of H10 exactly in a basis consisting of one local line-star plus nine local spokes; the parity/spoke split is explicit and exhaustive.',
      'boundary':'This is a GF(2) linear readout circuit, not a physical syndrome-extraction, noise, threshold, or hardware timing theorem.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
