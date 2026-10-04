#!/usr/bin/env python3
"""Pass 3159: fail-closed rank-three M36 promotion and monotone analysis.

No candidate is inferred from an empty search.  Every discovered object must first pass the
independent rank-three projector checks.  Accepted candidates then receive a Pauli spectrum,
a fixed-frame qubit Wigner-negativity witness, an exact product-stabilizer fidelity lower
bound, a logical symplectic frame, and first/second-order accepted-error coefficients.
The full 4,922,775-Lagrangian stabilizer-fidelity census and up-to-92,897,280-element logical
Clifford orbit are emitted as separate exhaustive gates rather than silently approximated.
"""
from __future__ import annotations
import glob,itertools,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_BT3159_RANK3_MONOTONE_PIPELINE_results.json'
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
LOCAL={(0,0):I,(1,0):X,(0,1):Z,(1,1):Y}

def rank_f2(rows):
    a=[list(map(int,r)) for r in rows];rank=0
    if not a:return 0
    for c in range(len(a[0])):
        p=next((i for i in range(rank,len(a)) if a[i][c]),None)
        if p is None:continue
        a[rank],a[p]=a[p],a[rank]
        for i in range(len(a)):
            if i!=rank and a[i][c]:a[i]=[x^y for x,y in zip(a[i],a[rank])]
        rank+=1
    return rank

def symp(u,v,n=6):return sum(u[i]*v[n+i]+u[n+i]*v[i] for i in range(n))&1

def pmatrix(v,n=6):
    out=np.array([[1]],complex)
    for i in range(n):out=np.kron(out,LOCAL[(v[i],v[n+i])])
    return out

def m36_basis():
    m=np.array([0,1,-1,1],complex);m/=np.linalg.norm(m)
    cols=[m]+[np.eye(4,dtype=complex)[:,i] for i in range(4)]
    q,_=np.linalg.qr(np.column_stack(cols));e=[q[:,i] for i in range(1,4)]
    clean=np.kron(np.kron(m,m),m);singles=[];doubles=[]
    for site in range(3):
        for a in range(3):
            fs=[m,m,m];fs[site]=e[a];singles.append(np.kron(np.kron(*fs[:2]),fs[2]))
    for i,j in itertools.combinations(range(3),2):
        for a in range(3):
            for b in range(3):
                fs=[m,m,m];fs[i]=e[a];fs[j]=e[b]
                doubles.append(np.kron(np.kron(*fs[:2]),fs[2]))
    return clean,singles,doubles

def pexpect(psi,v,n=6):
    x=v[:n];z=v[n:];mask=sum(int(x[i])<<(n-1-i) for i in range(n))
    phase=(1j)**(sum(x[i]*z[i] for i in range(n))%4);ans=0j
    for b,a in enumerate(psi):
        parity=sum(z[i]*((b>>(n-1-i))&1) for i in range(n))&1
        ans+=np.conj(psi[b^mask])*phase*((-1)**parity)*a
    return ans

def fwht(a):
    a=np.array(a,dtype=float,copy=True);h=1
    while h<len(a):
        for i in range(0,len(a),2*h):
            x=a[i:i+h].copy();y=a[i+h:i+2*h].copy();a[i:i+h]=x+y;a[i+h:i+2*h]=x-y
        h*=2
    return a

def f2_nullspace(rows,ncols):
    a=[list(map(int,r)) for r in rows];piv=[];r=0
    for c in range(ncols):
        p=next((i for i in range(r,len(a)) if a[i][c]),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r]
        for i in range(len(a)):
            if i!=r and a[i][c]:a[i]=[x^y for x,y in zip(a[i],a[r])]
        piv.append(c);r+=1
    free=[c for c in range(ncols) if c not in piv];basis=[]
    for f in free:
        v=[0]*ncols;v[f]=1
        for i,c in enumerate(piv):v[c]=a[i][f]
        basis.append(tuple(v))
    return basis

def logical_frame(stabs):
    # S^perp constraints are (z|x) dot v = 0.
    rows=[tuple(g[6:]+g[:6]) for g in stabs];comp=f2_nullspace(rows,12)
    span=[tuple(g) for g in stabs];quot=[]
    for v in comp:
        if rank_f2(span+[v])>rank_f2(span):span.append(v);quot.append(v)
    assert len(quot)==6
    rem=list(quot);pairs=[]
    while rem:
        x=rem.pop(0);j=next(i for i,z in enumerate(rem) if symp(x,z));z=rem.pop(j)
        new=[]
        for v in rem:
            w=list(v)
            if symp(v,z):w=[a^b for a,b in zip(w,x)]
            if symp(v,x):w=[a^b for a,b in zip(w,z)]
            new.append(tuple(w))
        rem=new;pairs.append({'X':list(x),'Z':list(z)})
    return pairs

def product_stabilizer_bound(psi):
    eig=[]
    for P in (X,Y,Z):
        w,v=np.linalg.eigh(P)
        eig.extend([v[:,0],v[:,1]])
    best=0.0
    for choice in itertools.product(range(6),repeat=6):
        s=np.array([1],complex)
        for i in choice:s=np.kron(s,eig[i])
        best=max(best,float(abs(np.vdot(s,psi))**2))
    return best

def error_series(P,psi0,clean,singles,doubles):
    def sums(vs):
        return (sum(float(np.vdot(v,P@v).real) for v in vs),
                sum(float(abs(np.vdot(psi0,v))**2) for v in vs))
    s0=float(np.vdot(clean,P@clean).real);n0=float(abs(np.vdot(psi0,clean))**2)
    ss,ns=sums(singles);sd,nd=sums(doubles)
    S=[s0,-3*s0+ss/3,3*s0-2*ss/3+sd/9]
    N=[n0,-3*n0+ns/3,3*n0-2*ns/3+nd/9]
    f0=N[0]/S[0];f1=(N[1]*S[0]-N[0]*S[1])/S[0]**2
    f2=N[2]/S[0]-N[1]*S[1]/S[0]**2+N[0]*(S[1]**2/S[0]**3-S[2]/S[0]**2)
    return {'success_coefficients_p0_p1_p2':S,'fidelity_coefficients_p0_p1_p2':[f0,f1,f2],
            'infidelity_linear_slope':-f1,'infidelity_quadratic_coefficient':-f2}

def certify(c):
    gens=[tuple(map(int,g['vector'])) for g in c.get('generators',[])]
    signs=[int(g.get('sign',1)) for g in c.get('generators',[])]
    reasons=[]
    if len(gens)!=3 or any(len(g)!=12 for g in gens):reasons.append('need three 12-bit generators')
    if reasons:return {'name':c.get('name','unnamed'),'accepted':False,'reasons':reasons}
    if rank_f2(gens)!=3:reasons.append('binary rank is not three')
    if any(symp(gens[i],gens[j]) for i in range(3) for j in range(i)):reasons.append('noncommuting')
    P=np.eye(64,dtype=complex)
    for g,s in zip(gens,signs):P=P@(np.eye(64)+s*pmatrix(g))/2
    clean,singles,doubles=m36_basis();s=float(np.vdot(clean,P@clean).real)
    killed=max(float(np.linalg.norm(P@v)) for v in singles)
    if np.max(np.abs(P-P.conj().T))>1e-9 or np.max(np.abs(P@P-P))>1e-9:reasons.append('invalid projector')
    if abs(np.trace(P).real-8)>1e-8:reasons.append('projector trace is not eight')
    if killed>1e-8:reasons.append('single errors not annihilated')
    if s<=1e-12:reasons.append('zero clean success')
    if reasons:return {'name':c.get('name','unnamed'),'accepted':False,'reasons':reasons,
      'clean_success_probability':s,'max_single_error_projection_norm':killed}
    psi=P@clean/math.sqrt(s)
    paulis=list(itertools.product((0,1),repeat=12));ex=np.array([pexpect(psi,v).real for v in paulis])
    unit=int(np.sum(np.abs(np.abs(ex)-1)<1e-8))
    if unit==64:return {'name':c.get('name','unnamed'),'accepted':False,'reasons':['accepted output is stabilizer']}
    W=fwht(ex)/4096
    return {'name':c.get('name','unnamed'),'accepted':True,'reasons':[],
      'clean_success_probability':s,'pauli_unit_count':unit,
      'pauli_l1':float(np.sum(np.abs(ex))),'pauli_l2_squared':float(np.sum(ex*ex)),
      'weyl_frame_negativity':float((np.sum(np.abs(W))-1)/2),
      'product_stabilizer_fidelity_lower_bound':product_stabilizer_bound(psi),
      'logical_symplectic_frame':logical_frame(gens),
      'logical_clifford_group_order_mod_phase':92897280,
      'exact_stabilizer_lagrangian_count':4922775,
      'error_series':error_series(P,psi,clean,singles,doubles)}

def extract(obj):
    out=[]
    if isinstance(obj,dict):
        if 'generators' in obj:out.append(obj)
        for v in obj.values():out.extend(extract(v))
    elif isinstance(obj,list):
        for v in obj:out.extend(extract(v))
    return out

def main():
    paths=[]
    for pat in ('data/*3125*.json','evidence/**/*3125*.json'):
        paths.extend(Path(p) for p in glob.glob(str(ROOT/pat),recursive=True))
    candidates=[]
    for p in sorted(set(paths)):
        try:candidates.extend(extract(json.loads(p.read_text())))
        except Exception:continue
    results=[certify(c) for c in candidates]
    out={'schema':'w33.pass3159.rank3_monotone_pipeline.v1','files_scanned':[str(p.relative_to(ROOT)) for p in paths],
      'candidate_count':len(results),'accepted_count':sum(r['accepted'] for r in results),'results':results,
      'status':'ANALYZED_ACCEPTED_CANDIDATES' if results else 'NO_CANDIDATE_INPUTS',
      'exhaustive_followups':{'stabilizer_fidelity':'4,922,775 Lagrangian shards','logical_clifford_orbit':'up to 92,897,280 projective Clifford elements'},
      'boundary':'No input is not a no-go. Qubit Wigner negativity is explicitly tied to the frozen Weyl frame; product-stabilizer fidelity is a certified lower bound until the exhaustive Lagrangian gate completes.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
