"""TOE68: exact-Gauss reconstruction and coupled gauge-matter octagon.

One ACTUAL W33 Levi 8-cycle; 4 dynamical spinless fermions, one integer
electric-flux coordinate, eight link electric energies, dynamical gauge
hopping and all eight native fermion hops. Finite-dimensional Galerkin.
"""
from pathlib import Path
import sys,json
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_pass1081_1086_core import build_w33

def native_octagon():
    *_,point_lines,frames,fidx,flags,flagidx=build_w33()
    edges=[(p,40+l) for p,l in flags]
    adj=[[] for _ in range(80)]
    for e,(a,b) in enumerate(edges):
        adj[a].append((b,e));adj[b].append((a,e))
    root=0
    def recurse(path,es):
        a=path[-1]
        if len(path)==8:
            for b,e in adj[a]:
                if b==root and path[1]<a:return path,es+[e]
            return None
        for b,e in adj[a]:
            if b<=root or b in path:continue
            got=recurse(path+[b],es+[e])
            if got:return got
        return None
    for b,e in adj[root]:
        if b>root:
            got=recurse([root,b],[e])
            if got:return got
    raise RuntimeError("W33 has no 8-cycle")

def sector(L,magnetic=.25,g=.9,kappa=.6):
    nodes,links=native_octagon()
    assert nodes==[0,40,4,44,1,45,13,41]
    assert links==[0,16,17,4,5,53,52,1]
    background=np.asarray([1,0]*4,dtype=int)
    occs=[x for x in range(256) if x.bit_count()==4]
    states=[(bits,m) for bits in occs for m in range(-L,L+1)]
    lookup={s:i for i,s in enumerate(states)}
    rows=[];cols=[];vv=[];Gauss=0
    for i,(bits,m) in enumerate(states):
        occ=np.asarray([(bits>>j)&1 for j in range(8)],int)
        electric=np.asarray([m+int(sum(occ[:j+1]-background[:j+1])) for j in range(8)],int)
        assert electric[-1]==m
        for j in range(8):
            assert electric[(j-1)%8]-electric[j]+occ[j]-background[j]==0
            Gauss+=1
        rows.append(i);cols.append(i);vv.append(.5*g*g*float(electric@electric)+magnetic)
        for e in range(8):
            a,b=e,(e+1)%8
            if occ[a]==occ[b]:continue
            target=bits^(1<<a)^(1<<b)
            direction=1 if occ[a] else -1
            newm=m-direction if e==7 else m
            destination=lookup.get((target,newm))
            if destination is not None:
                fermions_between=sum((bits>>j)&1 for j in range(min(a,b)+1,max(a,b)))
                rows.append(i);cols.append(destination);vv.append(-kappa*(-1)**fermions_between)
        if magnetic:
            for dm in (-1,1):
                destination=lookup.get((bits,m+dm))
                if destination is not None:
                    rows.append(i);cols.append(destination);vv.append(-magnetic/2)
    dim=len(states)
    H=coo_matrix((vv,(rows,cols)),shape=(dim,dim)).tocsr()
    assert (H-H.T).nnz==0
    energies,vec=eigsh(H,k=2,which="SA",tol=1e-11,maxiter=10000)
    order=np.argsort(energies)
    u=vec[:,order[0]]
    assert np.linalg.norm(H@u-energies[order[0]]*u)<1e-7
    boundary=float(sum(abs(u[j])**2 for j,(_,m) in enumerate(states) if abs(m)==L))
    return {"L":L,"magnetic":magnetic,"dimension":dim,
            "ground_energy":float(energies[order[0]]),
            "first_excitation_gap":float(energies[order[1]]-energies[order[0]]),
            "flux_boundary_probability":boundary,
            "Gauss_equalities_checked":Gauss}

def certificate():
    sweep=[sector(L) for L in (1,2,3)]
    control=sector(2,magnetic=0)
    assert [r["dimension"] for r in sweep]==[210,350,490]
    assert all(sweep[i+1]["ground_energy"]<sweep[i]["ground_energy"] for i in range(2))
    assert sweep[2]["flux_boundary_probability"]<1e-7
    return {
        "status":"PASS_TOE68_NATIVE_OCTAGON_COUPLED_GAUSS_MATTER",
        "octagon_vertices":native_octagon()[0],"native_link_indices":native_octagon()[1],
        "couplings":{"electric_g":.9,"fermion_hopping":.6,"magnetic":.25},
        "sectors":sweep,"zero_magnetic_control":control,
        "theorem":"Every represented state satisfies all eight Gauss equalities exactly and the explicitly generated Hermitian hopping/magnetic Hamiltonian preserves this Hilbert sector.",
        "scope":"Finite one-octagon 4-fermion gauge-invariant quantum Hamiltonian, not full W33 80-site lattice, no certified infinite-flux truncation bound, no continuum or physical CP selection."}
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe68_native_octagon_gauss.json").write_text(json.dumps(c,indent=2)+"\n")
    print(c["status"],[round(x["ground_energy"],8) for x in c["sectors"]])
