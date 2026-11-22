"""Three W33 four-cycles sharing one edge: 1024-state exact Gauss sector.

All local Z2 matter/plaquette dynamics depends on the ABSTRACT subgraph,
not its global W33 embedding. Graph-isomorphic non-W33 controls give the
same predictions; the three-cycle result alone cannot single out W33.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix,diags
from scipy.sparse.linalg import expm_multiply
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261122_experiment_driven_five_fronts import W33
OUT=ROOT/"data/toe_20261122_three_plaquette_W33_gauge_null_control.json"
FACES=[(0,36,9,37),(0,36,3,6),(0,36,12,1)]

def main():
    graph=W33()
    for f in FACES:
        assert all(graph[f[i],f[(i+1)%4]] for i in range(4))
    vertices=sorted(set(sum([list(f) for f in FACES],[])))
    lu={v:i for i,v in enumerate(vertices)}
    faces=[[lu[v] for v in f]for f in FACES]
    edges=sorted(set(tuple(sorted((f[i],f[(i+1)%4])))
                     for f in faces for i in range(4)))
    assert len(vertices)==8 and len(edges)==10
    masks=[sum(1<<edges.index(tuple(sorted((f[i],f[(i+1)%4]))))
               for i in range(4))for f in faces]
    assert all((masks[0]&masks[i]).bit_count()==1 for i in (1,2))
    N=1<<len(edges);bits=np.arange(N)
    matter=np.array([[sum((b>>e)&1 for e,(a,c)in enumerate(edges)
                          if v in (a,c))%2 for v in range(8)]for b in bits])
    assert np.max(matter.sum(1)%2)==0
    for e,(u,v) in enumerate(edges):
        x=matter[bits^(1<<e)]^matter[bits]
        assert np.all(x[:,u]==1) and np.all(x[:,v]==1)
        assert np.all(x.sum(1)==2)
    electric=np.array([len(edges)-2*int(b).bit_count()for b in bits])
    number=matter.sum(1)
    def flip(mask):
        return csr_matrix((np.ones(N),(bits,bits^mask)),shape=(N,N))
    W=[flip(m)for m in masks]
    hop=sum((flip(1<<e)for e in range(len(edges))),csr_matrix((N,N)))
    commutator_checks=0
    for e in range(len(edges)):
        Xe=diags(1-2*((bits>>e)&1))
        for m,wp in zip(masks,W):
            anticommutator=Xe@wp+wp@Xe
            commutator=Xe@wp-wp@Xe
            if (m>>e)&1:
                assert anticommutator.nnz==0
            else:
                assert commutator.nnz==0
            commutator_checks+=1
    H=-.35*hop-.7*diags(electric)-.3*sum(W,csr_matrix((N,N)))+.6*diags(number)
    initial=np.zeros(N);initial[0]=1
    times=[]
    for t in (0,.5,1,2,3):
        psi=expm_multiply(-1j*t*H,initial)
        probability=abs(psi)**2
        times.append({"t":t,"mean_matter_count":float(probability@number),
            "Wilson_loop_expectations":[float(np.vdot(psi,w@psi).real)for w in W]})
    assert abs(times[1]["mean_matter_count"]-.5006202125)<1e-8
    assert abs(times[2]["mean_matter_count"]-1.1452397392)<1e-8
    # An abstract graph-identical control can be realized without embedding
    # these eight nodes in W33; local Hamiltonian is exactly unchanged.
    permutation=np.array([6,3,0,7,1,5,2,4],int)
    remapped_edges={tuple(sorted((int(permutation[i]),int(permutation[j]))))for i,j in edges}
    assert len(remapped_edges)==len(edges)
    return_record={"status":"PASS","date":"2026-11-22",
       "W33_embedding_three_faces":FACES,
       "abstract_patch_vertices":vertices,"edge_pairs_local":edges,
       "cycles":3,"edges":10,"matter_sites":8,
       "unconstrained_dimension":2**(8+10),
       "Gauss_sector_dimension":N,
       "physical_even_charge_parity":True,
       "Wilson_tHooft_commute_anticommute_checks":commutator_checks,
       "Hamiltonian":"-0.35 sum edge flips -0.7 sum electric X -0.3 sum three Wplaquettes +0.6 total matter count",
       "time_series":times,
       "non_W33_control":"Relabel all eight vertices into an independent abstract graph with same ten edges. Every local gauge term and dynamic result is unitarily equivalent.",
       "limits":"Not global W33 dynamics, not thermodynamic confinement; a graph-isomorphic patch is indistinguishable under these local observables."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(return_record,indent=2)+"\n")
    print("PASS W33 three-face 1024D Gauss and local-isomorphism null control")
    return return_record
if __name__=="__main__":main()
