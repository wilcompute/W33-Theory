"""One-photon reduced-density ranks of two W33->E6 quartic orbital
coisometry row resources; falsifies deterministic passive-only preparation
from any four occupied input modes.

A passive number-conserving interferometer acts as U on one-body density
gamma and preserves its eigenvalues and rank. A 4-photon Fock input in
<=4 occupied orthogonal source modes has rank(gamma)<=4. Both ideal output
row states have larger one-body rank, so passive interferometry alone
cannot prepare them from such inputs. Postselection, non-Gaussian
resources, or other initial entanglement are NOT excluded.
"""
from collections import defaultdict,deque
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import sys,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_W33_symmetry_minimal_fourcopy import build_geometry,generators
from toe_20261116_W33_quartic_orbital_sparse_compilers import compose,inverse,closure

OUT=ROOT/"data"/"toe_20261116_W33_quartic_60_960_onebody_resource.json"
def stabilizer():
    geom=build_geometry();gen=generators(geom)
    reps={0:(tuple(range(40)),tuple(range(27)))}
    queue=deque([0])
    while queue:
        i=queue.popleft(); p,l=reps[i]
        for pp,ll in gen:
            j=ll[i]; nxt=(compose(pp,p),compose(ll,l))
            if j not in reps:
                reps[j]=nxt;queue.append(j)
    assert len(reps)==27
    hgen=[];H={tuple(range(40))}
    for i,(p,l) in reps.items():
        for pp,ll in gen:
            j=ll[i]
            hp=compose(inverse(reps[j][0]),compose(pp,p))
            if hp in H:continue
            hgen.append(hp);H=closure(hgen)
            if len(H)==960:return hgen,H
    assert False
def orbit(seed,generators):
    seen={tuple(seed)};queue=deque([tuple(seed)])
    while queue:
        q=queue.popleft()
        for g in generators:
            z=tuple(sorted(g[i] for i in q))
            if z not in seen:
                seen.add(z);queue.append(z)
    return sorted(seen)
def onebody(quartets):
    N=len(quartets)
    triples=defaultdict(list)
    for q in quartets:
        assert len(q)==4 and len(set(q))==4
        for i in q:
            triple=tuple(k for k in q if k!=i)
            triples[triple].append(i)
    M=np.zeros((40,40),dtype=np.int64)
    for points in triples.values():
        for i in points:
            for j in points:M[i,j]+=1
    assert int(np.trace(M))==4*N
    assert np.all(M==M.T)
    eig=np.linalg.eigvalsh(M.astype(float))/(4*N)
    assert eig.min()>-1e-11
    assert abs(eig.sum()-1)<1e-10
    purity=F(int(np.sum(M*M)),16*N*N)
    return dict(fourphoton_kets=N,
                onebody_integer_diagonal_multiset=sorted(set(np.diag(M).tolist())),
                onebody_integer_offdiagonal_nonzero_pairs=int(np.count_nonzero(M-np.diag(np.diag(M)))//2),
                onebody_integer_matrix_sha256=__import__("hashlib").sha256(M.tobytes()).hexdigest(),
                onebody_purity=str(purity),
                onebody_rank=int(np.sum(eig>1e-9)),
                onebody_min_eigenvalue=float(eig[0]),
                onebody_max_eigenvalue=float(eig[-1]),
                onebody_max_identical_product_overlap_upper=float(eig[-1]),
                onebody_is_maximally_mixed=bool(np.array_equal(M,np.eye(40,dtype=np.int64)*(N//10))) )
def run():
    gen,H=stabilizer()
    assert len(H)==960
    choices={"sparse60":[0,1,4,13],"best_uniform960":[0,1,4,17]}
    cases={}
    for name,seed in choices.items():
        Q=orbit(seed,gen)
        assert len(Q)==(60 if name=="sparse60" else 960)
        cases[name]=onebody(Q)
        assert cases[name]["onebody_rank"]>4
    result={
      "status":"W33_TWO_QUARTIC_ORBITAL_RESOURCE_ONEBODY_RANK_PASSIVE_NO_GO",
      "stabilizer_order":len(H),
      "cases":cases,
      "passive_LO_no_heralding_no_go":"Passive single-particle U acts as gamma->U gamma U^dagger, preserving the rank and spectrum. Any four-photon Fock source occupying <=4 input modes has rank(gamma)<=4. Both row resource states have rank>4.",
      "input_reference":"data/toe_20261116_W33_quartic_164_orbital_sparse_compilers.json",
      "limits":"Exact one-body integer correlation enumeration; eigenvalue and rank numeric with margin. Does not exclude photon counting, nonlinear resources, entangled sources or heralded optical preparation."
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    return result
if __name__=="__main__":
    x=run()
    print("PASS",x["status"],{k:v["onebody_rank"] for k,v in x["cases"].items()})
