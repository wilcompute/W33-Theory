"""Exact five-event order/dual audit: undirected Hasse spectrum cannot
recover causal time orientation. No proposed Lorentzian quantum-gravity action.
"""
from itertools import combinations,permutations,product
from collections import defaultdict,Counter
from pathlib import Path
import json
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/toe_20261119_causal_Hasse_oriented_spectral_obstruction.json'
N=5
EDGES=list(combinations(range(N),2));PERMS=list(permutations(range(N)))

def closure(A):
    A=A.copy()
    for k in range(len(A)):
        A|=(A[:,k,None]&A[None,k,:])
    return A

def canonical(A):return min(A[np.ix_(p,p)].tobytes() for p in PERMS)

def cover(A):
    H=A.copy()
    for i,j in product(range(N),repeat=2):
        if A[i,j] and any(A[i,k] and A[k,j] for k in range(N)):
            H[i,j]=False
    return H

def charpoly_laplace(H):
    U=(H|H.T).astype(int)
    L=s.diag(*np.sum(U,axis=0).tolist())-s.Matrix(U)
    return tuple(int(x) for x in L.charpoly().all_coeffs())

def run():
    raw={}
    for bits in range(1<<len(EDGES)):
        A=np.zeros((N,N),bool)
        for k,(i,j) in enumerate(EDGES):A[i,j]=(bits>>k)&1!=0
        A=closure(A)
        raw[A.tobytes()]=A
    assert len(raw)==357
    bycanon={}
    for A in raw.values():bycanon.setdefault(canonical(A),A)
    assert len(bycanon)==63
    dual_count=0;nondual=[]
    buckets=defaultdict(list)
    signatures={}
    for key,A in bycanon.items():
        H=cover(A)
        dualkey=canonical(A.T)
        if key==dualkey:dual_count+=1
        else:nondual.append(key)
        interval=[0]*4
        for i,j in product(range(N),repeat=2):
            if A[i,j]:interval[int(np.sum(A[i,:]&A[:,j]))]+=1
        bideg=tuple(sorted((int(np.sum(A[:,i])),int(np.sum(A[i,:]))) for i in range(N)))
        poly=charpoly_laplace(H)
        sig=(tuple(interval),bideg,poly)
        signatures[key]=sig
        buckets[poly].append(key)
        assert poly==charpoly_laplace(cover(A.T))
    assert len(nondual)%2==0
    # Hasse directed adjacency itself records the order exactly by
    # transitive closure, whereas L=Degree-(H+H.T) does not.
    maxspec=max(map(len,buckets.values()))
    undirected_graph_types={canonical((cover(A)|cover(A).T)) for A in bycanon.values()}
    # A directed inverse-response based only on Frobenius norm is also
    # orientation-blind: ||(mI-alpha H)^-1||_F = ||transpose(...)||_F.
    response_diff=0.
    for A in bycanon.values():
        H=cover(A).astype(float)
        r=lambda M:float(np.linalg.norm(np.linalg.inv(1.3*np.eye(N)-.6*M))**2)
        response_diff=max(response_diff,abs(r(H)-r(H.T)))
    assert response_diff<1e-12
    # Explicit simplest non-self-dual example as a directed star.
    A=np.zeros((N,N),bool);A[0,1]=A[0,2]=True
    B=A.T.copy()
    assert canonical(A)!=canonical(B)
    H=cover(A);Hb=cover(B)
    assert np.array_equal(H|H.T,Hb|Hb.T)
    lap=charpoly_laplace(H)
    nrootA=int(sum(np.sum(A,axis=0)==0));nrootB=int(sum(np.sum(B,axis=0)==0))
    assert nrootA==3 and nrootB==4
    # For nonselfdual pairs, any invariant that ignores orientation
    # assigns the same score, not merely this Laplacian spectrum.
    nonself_count=len(nondual)
    out={'forward_graph_presentations':1024,'naturally_labeled_relations':357,
       'unlabeled_poset_classes':63,
       'self_dual_isomorphism_classes':dual_count,
       'nonselfdual_isomorphism_classes':nonself_count,
       'distinct_dual_pairs':nonself_count//2,
       'undirected_Hasse_laplacian_spectral_classes':len(buckets),
       'undirected_Hasse_graph_isomorphism_types':len(undirected_graph_types),
       'inverse_propagator_Frobenius_response_dual_max_difference':response_diff,
       'largest_cospectral_class':maxspec,
       'nonselfdual_example':{'P_covers':[[0,1],[0,2]],
           'P_dual_covers':[[1,0],[2,0]],
           'minimal_points_P':nrootA,'minimal_points_dual':nrootB,
           'identical_undirected_Hasse_laplacian_charpoly':lap},
       'theorem':'The undirected Hasse graph and every graph spectrum computed from it are identical for P and P^op. For non-self-dual P this loses causal time orientation, even though directed Hasse transitive closure recovers the poset.',
       'physical_caveat':'A time-reversal-invariant gravity action may deliberately assign equal weights; extra oriented data/operators are needed if chirality or directed propagators must distinguish past and future. No Einstein action inferred.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2)+'\n')
    print('CAUSAL 5 SELF-DUAL',dual_count,'NONS',nonself_count,'SPECTRAL CLASSES',len(buckets))
    return out
if __name__=='__main__':run()
