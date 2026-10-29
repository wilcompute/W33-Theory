#!/usr/bin/env python3
"""Independent 51840 Weyl double-cover verifier and 9-mode reference witness.
Finite generator data: data/w33_20261029_explicit_mod2_E8_isometry.json.
Outputs an exact integer certificate and ideal ordinary-optics calculation.
"""
from collections import Counter,defaultdict,deque
from pathlib import Path
import json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261029_e8_cover_photonic_sign.json'

def act(g,x):
    out=0
    while x:
        t=x&-x;out^=g[t.bit_length()-1];x^=t
    return out

def compose(g,h):return tuple(act(g,z) for z in h)

def rank(xs):
    base={}
    for x in xs:
        while x:
            k=x.bit_length()-1
            if k not in base:base[k]=x;break
            x^=base[k]
    return len(base)

def roots_by_residue(G):
    roots={tuple(int(i==j) for i in range(8)) for j in range(8)}
    roots|={tuple(-a for a in r) for r in roots}
    todo=deque(roots)
    while todo:
        r=todo.popleft()
        for j in range(8):
            v=list(r);v[j]-=int(G[j]@r);v=tuple(v)
            if v not in roots:roots.add(v);todo.append(v)
            assert len(roots)<=240
    assert len(roots)==240
    buckets=defaultdict(list)
    for r in roots:buckets[sum((x&1)<<j for j,x in enumerate(r))].append(r)
    assert len(buckets)==120 and all(len(b)==2 for b in buckets.values())
    return buckets

def lift(cols,G,edges,buckets):
    vectors=[np.array(sorted(buckets[c])[0],dtype=np.int64) for c in cols]
    signs={0:1};queue=deque([0])
    while queue:
        j=queue.popleft()
        for a,b in edges:
            if j not in (a,b):continue
            k=b if j==a else a
            if k in signs:continue
            dot=int(vectors[j]@G@vectors[k]);assert abs(dot)==1
            signs[k]=-signs[j]*dot;queue.append(k)
    M=np.column_stack([vectors[k]*signs[k] for k in range(8)])
    I=np.eye(8,dtype=np.int64)
    assert np.array_equal(M.T@G@M,G)
    assert tuple(sum((int(M[r,c])&1)<<r for r in range(8)) for c in range(8))==cols
    if np.array_equal(M@M@M,-I):M=-M
    assert np.array_equal(M@M@M,I)
    return M

def optical_mesh(U):
    R=U.astype(complex).copy();gates=[]
    for j in range(7):
        for k in range(7,j,-1):
            a,b=R[k-1,j],R[k,j];norm=np.hypot(abs(a),abs(b))
            if norm<1e-13:continue
            Z=np.array([[a.conjugate(),b.conjugate()],[-b,a]])/norm
            R[k-1:k+1]=Z@R[k-1:k+1]
            gates.append((k-1,Z.conj().T))
    assert np.max(abs(R-np.diag(np.diag(R))))<1e-11
    V=np.diag(np.diag(R))
    for k,Z in reversed(gates):V[k:k+2]=Z@V[k:k+2]
    err=float(np.max(abs(V-U)));assert err<1e-11
    return len(gates),err

def main():
    old=json.loads((ROOT/'data/w33_20261029_explicit_mod2_E8_isometry.json').read_text())
    edges=[tuple(x) for x in old['E8_Dynkin_edges']]
    G=2*np.eye(8,dtype=np.int64)
    for a,b in edges:G[a,b]=G[b,a]=-1
    buckets=roots_by_residue(G)
    gens=[tuple(g['E8_simple_root_mod2_columns']) for g in old['checked_group_generators']]
    matrices=[lift(g,G,edges,buckets) for g in gens]
    I=np.eye(8,dtype=np.int64);F=tuple(1<<j for j in range(8))
    W=I.copy();f=F
    for j in (0,1,5,4):W=W@matrices[j];f=compose(f,gens[j])
    assert compose(f,f)==F and f!=F and np.array_equal(W@W,-I)
    seen={F:(None,None)};queue=deque([F]);invol=[]
    while queue:
        g=queue.popleft()
        if g!=F and compose(g,g)==F:invol.append(g)
        for j,h in enumerate(gens):
            v=compose(g,h)
            if v not in seen:seen[v]=(g,j);queue.append(v)
    assert len(seen)==25920 and len(invol)==315
    counts=Counter(rank(g[j]^F[j] for j in range(8)) for g in invol)
    assert counts=={4:270,2:45}
    r2=next(g for g in invol if rank(g[j]^F[j] for j in range(8))==2)
    path=[];v=r2
    while v!=F:v,j=seen[v];path.append(j)
    K=I.copy()
    for j in reversed(path):K=K@matrices[j]
    assert np.array_equal(K@K,I)
    eig,Q=np.linalg.eigh(G.astype(float));assert eig.min()>0
    S=(Q*np.sqrt(eig))@Q.T;Sinv=(Q/np.sqrt(eig))@Q.T
    O=S@W@Sinv
    assert np.max(abs(O.T@O-I))<1e-11 and np.max(abs(O@O+I))<1e-11
    gates,err=optical_mesh(O)
    ref=np.r_[1.,np.zeros(8)];sig=np.r_[0.,np.eye(8)[0]]
    output=(ref+np.r_[0.,(O@O)@np.eye(8)[0]])/np.sqrt(2)
    p_plus=float(abs(np.vdot((ref+sig)/np.sqrt(2),output))**2)
    p_minus=float(abs(np.vdot((ref-sig)/np.sqrt(2),output))**2)
    assert p_plus<1e-22 and abs(p_minus-1)<1e-11
    data=dict(status='PASS',finite_order=len(seen),integral_cover_order=2*len(seen),
       roots=240,mod2_root_pairs=120,rank4_involutions_order4_lifts=counts[4],
       rank2_involutions_order2_lifts=counts[2],double_cover_kernel=['I','-I'],
       nonsplit_witness_word=[0,1,5,4],nonsplit_witness_integral_square='-I',
       rank2_witness_word=list(reversed(path)),rank2_witness_integral_square='I',
       integer_generator_columns=[m.T.tolist() for m in matrices],
       signal_modes=8,reference_modes=1,unitary_mesh_gates=gates,
       unitary_mesh_max_error=err,ideal_plus_port_probability=p_plus,
       ideal_minus_port_probability=p_minus,
       caveat='9-mode witness is standard phase-referenced quantum optics, not a demonstration of fundamental E8 physics')
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(data,indent=2)+'\n')
    print('PASS integral cover',data['integral_cover_order'],'optical gates',gates,'minus port',p_minus)
if __name__=='__main__':main()
