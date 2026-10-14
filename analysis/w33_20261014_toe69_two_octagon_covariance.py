"""TOE69: two overlapping native W33 octagons, mobile gauge-dressed fermions.

Fully occupied 5-fermion Fock sector on an 11-site / 12-edge patch; both
Gauss-law electric integers and all 3 native supported Wilson cycles.
Sparse Galerkin comparison at L=1 and L=2, including flux covariance.
"""
from __future__ import annotations
import itertools,json,sys
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_five_fronts import graph,octagons

def patch():
    ed,adj,cycles=octagons()
    chosen=(cycles[0],cycles[1])
    support=sorted(set(chosen[0])|set(chosen[1]))
    nodes=sorted({vertex for e in support for vertex in ed[e]})
    assert support==[0,1,2,4,5,6,16,17,52,53,88,89]
    assert len(nodes)==11 and len(support)==12
    idx={v:i for i,v in enumerate(nodes)}
    p_ed=[(idx[ed[e][0]],idx[ed[e][1]]) for e in support]
    B=np.zeros((12,11),int)
    for i,(a,b) in enumerate(p_ed):
        B[i,a]=-1
        B[i,b]=1
    emap={e:i for i,e in enumerate(support)}
    faces=[]
    for c in cycles:
        if not set(c).issubset(support):
            continue
        sub={}
        for e in c:
            a,b=ed[e]
            sub.setdefault(a,[]).append((b,e,1))
            sub.setdefault(b,[]).append((a,e,-1))
        v=min(sub);before=None;row=np.zeros(12,int)
        for _ in range(8):
            nxt,e,sg=next(z for z in sub[v] if z[0]!=before)
            row[emap[e]]+=sg
            before,v=v,nxt
        assert v==min(sub)
        assert not np.any(row@B)
        faces.append(row)
    P=np.unique(np.array(faces),axis=0)
    assert P.shape==(3,12)
    adj2=[[] for _ in nodes]
    for e,(a,b) in enumerate(p_ed):
        adj2[a].append((b,e,1))
        adj2[b].append((a,e,-1))
    order=[0]
    parents={0:None}
    parent_edges={}
    for a in order:
        for b,e,sg in adj2[a]:
            if b not in parents:
                parents[b]=a
                parent_edges[b]=(a,e,sg)
                order.append(b)
    assert len(order)==11
    tree={value[1] for value in parent_edges.values()}
    chords=[e for e in range(12) if e not in tree]
    assert len(chords)==2
    assert {tuple(x) for x in P[:,chords]}=={(-1,1),(1,0),(0,1)}
    bg=np.asarray([int(v<40) for v in nodes])
    return dict(nodes=nodes,support=support,p_ed=p_ed,
                B=B,P=P,order=order,parent_edges=parent_edges,
                chords=chords,background=bg)

def exact_gauss_electric(occupancy,flux,patch):
    B=patch["B"];order=patch["order"]
    acc=occupancy-patch["background"]
    n=np.zeros(12,int)
    n[patch["chords"]]=flux
    acc=acc+B.T@n
    for b in reversed(order[1:]):
        a,e,sg=patch["parent_edges"][b]
        n[e]=-sg*acc[b]
        acc[a]+=acc[b]
    assert not np.any(B.T@n+occupancy-patch["background"])
    return n

def diagonalize(L,patch,g=.8,kappa=.7,beta=.4,mass=.3):
    ed=patch["p_ed"];chords=patch["chords"]
    nferm=int(sum(patch["background"]))
    fock=[x for x in range(1<<11) if x.bit_count()==nferm]
    fidx={x:i for i,x in enumerate(fock)}
    fluxes=list(itertools.product(range(-L,L+1),repeat=2))
    fluxidx={x:i for i,x in enumerate(fluxes)}
    nflux=len(fluxes);dim=len(fock)*nflux
    row=[];col=[];val=[]
    for oi,bits in enumerate(fock):
        occ=np.asarray([(bits>>j)&1 for j in range(11)],int)
        stagger=mass*float((1-2*patch["background"])@occ)
        hops=[]
        for e,(a,b) in enumerate(ed):
            oa=(bits>>a)&1;ob=(bits>>b)&1
            if oa==ob:continue
            dest=bits^(1<<a)^(1<<b)
            direction=1 if oa else -1
            sign=(-1)**sum((bits>>j)&1 for j in range(min(a,b)+1,max(a,b)))
            hops.append((fidx[dest],e,direction,sign))
        for mi,f in enumerate(fluxes):
            j=oi*nflux+mi
            el=exact_gauss_electric(occ,np.asarray(f),patch)
            row.append(j);col.append(j)
            val.append(g*g*(el@el)/2+stagger+len(patch["P"])*beta/g**2)
            for di,e,dr,sign in hops:
                new=list(f)
                if e in chords:new[chords.index(e)]-=dr
                k=fluxidx.get(tuple(new))
                if k is not None:
                    row.append(j);col.append(di*nflux+k)
                    val.append(-kappa*sign)
            for delta in patch["P"][:,chords]:
                for sg in (-1,1):
                    k=fluxidx.get(tuple(np.asarray(f)+sg*delta))
                    if k is not None:
                        row.append(j);col.append(oi*nflux+k)
                        val.append(-beta/(2*g*g))
    H=coo_matrix((val,(row,col)),shape=(dim,dim)).tocsr()
    assert (H-H.T).nnz==0
    ev,vec=eigsh(H,k=2,which="SA",tol=1e-9,maxiter=8000)
    order=np.argsort(ev)
    u=vec[:,order[0]]
    residual=float(np.linalg.norm(H@u-ev[order[0]]*u))
    assert residual<1e-7
    prob=(abs(u.reshape(len(fock),nflux))**2).sum(axis=0)
    ints=np.asarray(fluxes,dtype=float)
    mean=prob@ints
    centered=ints-mean
    covariance=centered.T@(centered*prob[:,None])
    boundary=float(sum(prob[i] for i,f in enumerate(fluxes)
                       if max(abs(x) for x in f)==L))
    return {"L":L,"dimension":dim,"ground":float(ev[order[0]]),
        "first_gap":float(ev[order[1]]-ev[order[0]]),
        "flux_means":mean.tolist(),"flux_covariance":covariance.tolist(),
        "flux_boundary_probability":boundary,"numerical_ritz_residual":residual}

def certificate():
    p=patch()
    runs=[diagonalize(L,p) for L in (1,2)]
    assert [r["dimension"] for r in runs]==[4158,11550]
    assert runs[1]["ground"]<runs[0]["ground"]
    assert all(r["flux_covariance"][0][1]<0 for r in runs)
    assert runs[1]["flux_boundary_probability"]<.006
    return {"status":"PASS_TOE69_TWO_OVERLAPPING_NATIVE_OCTAGONS",
       "original_cycle_indices":[0,1],
       "native_edge_ids":p["support"],"native_vertex_ids":p["nodes"],
       "n_vertices":11,"n_edges":12,"n_fermions":int(sum(p["background"])),
       "fixed_number_fock_states":462,"independent_electric_coordinates":2,
       "native_supported_plaquettes":3,"chord_cycle_shifts":p["P"][:,p["chords"]].tolist(),
       "Hamiltonian_parameters":{"g":.8,"kappa":.7,"beta":.4,"mass":.3},
       "runs":runs,
       "scope":"Exact Gauss-law reconstruction in a native two-loop finite patch, numerical Ritz eigenstates and negative covariance at two truncations. Prior Pass11974 studied the same patch class; observable covariance and its cutoff comparison are the additional measured quantity. Not a certified untruncated, thermodynamic, or continuum gauge theory."}

if __name__=="__main__":
    out=certificate()
    (ROOT/"data/w33_20261014_toe69_two_octagon_flux_covariance.json").write_text(
        json.dumps(out,indent=2)+"\n")
    print(out["status"],[r["flux_covariance"][0][1] for r in out["runs"]])
