#!/usr/bin/env python3
"""Do all 1620 minimal W33 octagon Wilson loops determine flat U1 gauge?

Take a BFS-tree gauge: 79 vertex phases removed, 81 chords physical.
Construct 1620 octagon ×81 integer signed-chord matrix. Compute exact
GFp rank and search for an 81-octagon submatrix with determinant ±1.
Such a certificate proves no invisible finite-order U1 local-holonomy
sectors remain if all 1620 shortest loops have Wilson flux zero.
"""
import json,sys
from pathlib import Path
import numpy as np,networkx as nx
from sympy import Matrix
from w33_20261109_octagon_gauge_matter_tradeoff import loops_length8
from w33_20261109_flux_dark_mode_fragility import build

def rankmod(mat,p):
    A=np.asarray(mat,dtype=np.int64).copy()%p
    m,n=A.shape
    rows=[];rr=0
    for j in range(n):
        nz=np.nonzero(A[rr:,j])[0]
        if len(nz)==0:continue
        k=rr+int(nz[0]);A[[rr,k]]=A[[k,rr]]
        A[rr,:]=(A[rr,:]*pow(int(A[rr,j]),-1,p))%p
        for z in range(rr+1,m):
            a=int(A[z,j])
            if a:A[z,:]=(A[z,:]-a*A[rr,:])%p
        rr+=1
        if rr>=min(n,m):break
    return rr

def pivot_mod2(mat):
    basis={};picked=[]
    for i,row in enumerate(mat):
        bits=0
        for j,x in enumerate(row):
            if int(x)&1:bits|=1<<j
        reduced=bits
        for k,v in sorted(basis.items(),reverse=True):
            if (reduced>>k)&1:reduced^=v
        if reduced:
            p=reduced.bit_length()-1
            basis[p]=reduced
            picked.append(i)
            if len(picked)==mat.shape[1]:break
    return picked

def main(path=None):
    B,edges,G=build()
    tree=nx.bfs_tree(G,0).to_undirected()
    chords=sorted(set(tuple(sorted(e)) for e in G.edges())-
                  set(tuple(sorted(e)) for e in tree.edges()))
    assert len(chords)==81
    ids={frozenset(e):i for i,e in enumerate(chords)}
    loops=loops_length8(G)
    assert len(loops)==1620
    W=np.zeros((len(loops),81),dtype=np.int8)
    for i,ring in enumerate(loops):
        for a,b in zip(ring,ring[1:]+ring[:1]):
            j=ids.get(frozenset((a,b)))
            if j is not None:
                W[i,j]+=1 if a<40 else -1
    ranks={str(p):rankmod(W,p) for p in (2,3,5,7,11)}
    assert ranks=={"2":81,"3":81,"5":81,"7":81,"11":81},ranks
    picked=pivot_mod2(W)
    assert len(picked)==81
    det=int(Matrix(W[picked].tolist()).det(method="domain-ge"))
    assert det%2==1
    # If det ±1, these 81 true local octagons themselves supply
    # a unimodular basis for EVERY U1 flux degree.
    cert=abs(det)==1
    output={
     "status":"PASS_ALL_W33_OCTAGON_CHORD_RANK_MOD_2_3_5_7_11",
     "native_graph":[80,160],
     "fundamental_cycle_dimension":81,
     "shortest_8cycle_count":len(loops),
     "all_octagon_chord_matrix_shape":list(W.shape),
     "all_octagon_chord_matrix_rank_over_each_prime":ranks,
     "GF2_selected_81_octagon_row_ids":picked,
     "exact_integer_determinant_of_selected_81_octagon_minor":str(det),
     "selected_integer_minor_unimodular":bool(cert),
     "local_wilson_ground_saturation_conclusion":("These 81 shortest octagons form an EXACT Z-basis for gauge-invariant U1 cycle angles. Their all-zero Wilson flux forces all81 chord fluxes zero modulo2pi, hence pure gauge." if cert else "The selected mod2-independent 81 rows have odd nonzero determinant but may not be unimodular. Full U1 discrete-torsion uniqueness requires an explicit unimodular minor or full integer Smith normal form; rank over small primes is not enough."),
     "scope":"Full set of all 1620 shortest octagons on the native W33 Levi graph, not the 1382 zero-three-deck-winding local plaquettes of the prior TOE38 quotient 2-complex. Fixing every shortest loop is a DIFFERENT gauge action with potentially different physical locality/embedding and removes TOE38's deck-sector freedom. Flat-connection theorem is finite graph lattice topology only, not a dynamics selection of a nontrivial flux or a continuum TOE."
    }
    if path:Path(path).write_text(json.dumps(output,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("OCTAGON_INTEGER",json.dumps({"ranks":ranks,"chosen_minor_det":str(det),
         "unimodular":cert,"full_octagons":len(loops)}))
    return output
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
