"""Exact FIXED-U interaction trace certificates on native five W33 PSp orbits.

Identity: R(t)=(I-U*t*G(t))^-1, G_n=P D^n P (doublon subspace).
Tr(H^N)-Tr(D^N)=[t^(N-1)] tr(R(t)*d/dt[U*t*G(t)]).
All operations modulo p in F_p[i]; nonzero reduction implies nonzero Q(i).
Original floating-point angles are NOT claimed to be covered.
"""
import sys, json, math, time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261009_round17_interaction_trace_certificate as prior
from w33_20261008_5state_ritz import geometry
NMAX=19
def zzero(n=80):
    z=np.zeros((n,n), dtype=np.int64)
    return z,z.copy()
def zadd(x,y,p):
    return ((x[0]+y[0])%p,(x[1]+y[1])%p)
def zscale(x,k,p):
    return (x[0]*k%p,x[1]*k%p)
def ztrace(x,p):
    return int(np.trace(x[0])%p)
def zprod(x,y,p):
    return ((x[0]@y[0]-x[1]@y[1])%p, (x[0]@y[1]+x[1]@y[0])%p)
def projected_returns(A,p,nmax=NMAX):
    n=A[0].shape[0]; ident=(np.eye(n,dtype=np.int64),np.zeros((n,n),dtype=np.int64))
    powers=[ident]
    for _ in range(nmax):
        powers.append(zprod(powers[-1],A,p))
    G=[]
    for k in range(nmax):
        if k%2:
            G.append(zzero(n));continue
        v=zzero(n)
        for a in range(k+1):
            x,y=powers[a],powers[k-a]
            had=((x[0]*y[0]-x[1]*y[1])%p,(x[0]*y[1]+x[1]*y[0])%p)
            v=zadd(v,zscale(had,math.comb(k,a)%p,p),p)
        G.append(v)
    return G

def interaction_deltas(G,U,p,NMAX=NMAX):
    # This is a coefficient-by-coefficient Neumann expansion of a rank-80 resolvent.
    size=G[0][0].shape[0]
    R=[(np.eye(size,dtype=np.int64),np.zeros((size,size),dtype=np.int64))]
    for n in range(1,NMAX):
        v=zzero(size)
        for j in range(0,n,2): # G_odd=0, by bipartiteness
            v=zadd(v,zprod(G[j],R[n-1-j],p),p)
        R.append(zscale(v,U%p,p))
    out={}
    for n in [15,17,19]:
        value=0
        for j in range(0,n,2):
            value+=(j+1)*ztrace(zprod(R[n-1-j],G[j],p),p)
        out[str(n)]=int(U*value%p)
    return out

def toy_check():
    from itertools import combinations_with_replacement
    from w33_20261009_round16_two_boson_hubbard_orbits import build
    # Direct 2-boson check with a 4-cycle and varying U, in modular arithmetic.
    n=4;p=1000003; A=(np.array([[0,1,0,1],[1,0,1,0],[0,1,0,1],[1,0,1,0]],dtype=np.int64),np.zeros((4,4),dtype=np.int64))
    G=projected_returns(A,p,11)
    states=list(combinations_with_replacement(range(n),2)); idx={s:i for i,s in enumerate(states)}
    D=np.zeros((len(states),len(states)),dtype=np.int64);P=np.zeros_like(D)
    # Entries sqrt(2) are avoided by using a nonorthonormal polynomial Fock basis:
    # instead use a complex-valued orthonormal direct Hamiltonian and round traces.
    H=np.zeros_like(D,dtype=np.float64)
    for col,(i,j) in enumerate(states):
        if i==j:P[col,col]=1
        occ={i:2} if i==j else {i:1,j:1}
        for x,nx in occ.items():
            for y in np.flatnonzero(A[0][:,x]):
                new=[i,j];new.remove(x);new.append(int(y))
                val=math.sqrt(nx*(occ.get(int(y),0)+1))
                H[idx[tuple(sorted(new))],col]+=val
    for U in (1,2,4):
        mat=H+U*P; base=H
        for moment in (3,5,7,9):
            raw=np.trace(np.linalg.matrix_power(mat,moment))-np.trace(np.linalg.matrix_power(base,moment))
            # float exact up to this size, integer trace
            expected=int(round(raw))%p
            computed=interaction_deltas_all(G,U,p,11)
            assert computed[str(moment)]==expected,(U,moment,computed[str(moment)],expected)
    return True

def interaction_deltas_all(G,U,p,nmax):
    size=G[0][0].shape[0]
    R=[(np.eye(size,dtype=np.int64),np.zeros((size,size),dtype=np.int64))]
    for n in range(1,nmax):
        v=zzero(size)
        for j in range(0,n,2):v=zadd(v,zprod(G[j],R[n-1-j],p),p)
        R.append(zscale(v,U%p,p))
    return {str(n):int(U*sum((j+1)*ztrace(zprod(R[n-1-j],G[j],p),p) for j in range(0,n,2))%p) for n in range(1,nmax,2)}

def main():
    assert toy_check()
    edges,*_=geometry()
    reps=json.loads((ROOT/"data/w33_20261009_PSp_orbits_isotropic_triplets.json").read_text())["orbits"]
    cert={}
    for p in (1000003,1000033):
        prior.MOD=p
        Gs=[]
        for orb in reps:
            Gs.append(projected_returns(prior.phased_adj(edges,orb["representative"]),p))
        by_U={}
        for U in (2,8,20):
            t=time.time()
            vs=[interaction_deltas(G,U,p) for G in Gs]
            distinct17=len({x["17"] for x in vs})
            distinct19=len({x["19"] for x in vs})
            distinctpair=len({(x["17"],x["19"]) for x in vs})
            assert distinct19==5 and distinctpair==5,(p,U,vs)
            by_U[str(U)]={"interacting_minus_free_trace":vs,"distinct_moment17":distinct17,"distinct_moment19":distinct19,"distinct_joint":distinctpair}
            print("FIXED U",p,U,"17",[x["17"] for x in vs],"19",[x["19"] for x in vs],"secs",round(time.time()-t,2),flush=True)
        cert[str(p)]=by_U
    out={"status":"PASS","method":"exact rank-80 projected resolvent coefficients","phase_gaussian_rationals":[[15,8,17],[4,-3,5],[5,12,13]],"moduli":list(map(int,cert)),"orbits":[o["representative"] for o in reps],"fixed_U":cert,"toy_direct_boson_check":True,"interpretation":"Every pair of specified rational-phase W33 two-boson Hubbard Hamiltonians at U=2,8,20 has inequivalent full spectra (joint trace moments 17,19), certified by a nonzero coefficient in the displayed modular reduction. This is not a statement about original floating-phase angles, all U, or physical realization."}
    f=ROOT/"data/w33_20261009_round18_fixedU_resolvent_certificate.json"
    f.write_text(json.dumps(out,indent=2)+"\n")
    print("PASS written",f,flush=True)
if __name__=="__main__":main()
