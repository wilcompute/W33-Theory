#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, math, hashlib
from pathlib import Path
import numpy as np
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
FILES={
"p":ROOT/"data/PART_4177_4184_AF_NOGO_TWOBODY_HODGE_PDK_INTERVAL_BONKERS.json",
"a":ROOT/"data/w33_pass4177_fixed_carrier_af_nogo.json",
"g":ROOT/"data/w33_pass4178_strict_two_mode_relational_compiler.json",
"h":ROOT/"data/w33_pass4179_hodge_complete_real_decoder.json",
"d":ROOT/"data/w33_pass4180_pdk_grounded_tapped_delay_layout.json",
"n":ROOT/"data/w33_pass4181_symmetry_stratified_interval_mixed_push.json",
}
def chash(d):
    x=dict(d);x.pop("semantic_sha256",None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def canon(v):
    v=tuple(x%3 for x in v)
    for x in v:
        if x:
            z=1 if x==1 else 2
            return tuple(z*y%3 for y in v)
def symp(u,v):
    return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%3
def geom():
    pts=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    idx={p:i for i,p in enumerate(pts)}
    A=np.zeros((40,40),int)
    for i,u in enumerate(pts):
        for j,v in enumerate(pts):
            if i!=j and symp(u,v)==0:A[i,j]=1
    lines=set()
    for i,u in enumerate(pts):
        for j,v in enumerate(pts):
            if j<=i or symp(u,v):continue
            S={idx[canon(tuple(a*u[k]+b*v[k] for k in range(4)))]
               for a,b in itertools.product(range(3),repeat=2) if a or b}
            if len(S)==4:lines.add(tuple(sorted(S)))
    lines=sorted(lines);E=[]
    D=np.zeros((80,160),float);e=0
    for l,L in enumerate(lines):
        for p in L:
            E.append((p,40+l));D[p,e]=1;D[40+l,e]=-1;e+=1
    return A,lines,E,D
def eq_rhs(z,Q,J):
    m=len(Q);L=12*np.eye(m)-Q;u=z[:m];v=z[m:];a,b=J[0];c,d=J[1]
    return np.r_[a*u+b*v-u**3-.1*(L@u),c*u+d*v-v**3-10*(L@v)]
def eq_jac(z,Q,J):
    m=len(Q);L=12*np.eye(m)-Q;u=z[:m];v=z[m:];a,b=J[0];c,d=J[1]
    return np.block([[a*np.eye(m)-np.diag(3*u*u)-.1*L,b*np.eye(m)],
                     [c*np.eye(m),d*np.eye(m)-np.diag(3*v*v)-10*L]])
def main():
    ds={k:json.loads(p.read_text()) for k,p in FILES.items()}
    for k,d in ds.items():assert chash(d)==d["semantic_sha256"],k
    A,lines,E,D=geom()
    assert len(lines)==40 and len(E)==160
    assert np.allclose(np.linalg.eigvalsh(A),[-4]*15+[2]*24+[12])
    assert ds["a"]["original_carrier"]["SU3_Dynkin_load"]==16
    assert ds["a"]["original_carrier"]["SU3_cubed_anomaly"]==-28
    assert 11-(2/3)*(16+.5)==0
    G=nx.Graph();G.add_nodes_from(range(58));G.add_edges_from(ds["g"]["physical_edges"])
    assert G.number_of_edges()==84 and max(dict(G.degree()).values())==4 and nx.diameter(G)==9
    H=np.array([[1,1],[1,-1]],complex)/math.sqrt(2);I=np.eye(2)
    CZ=np.diag([1,1,1,-1]);CNOT=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],complex)
    assert np.allclose(np.kron(I,H)@CZ@np.kron(I,H),CNOT)
    assert np.linalg.matrix_rank(D)==79
    U,s,Vh=np.linalg.svd(D,full_matrices=True);Z=Vh[79:,:]
    M=np.vstack([D,Z]);sv=np.linalg.svd(M,compute_uv=False)
    assert abs(sv.min()-1)<1e-10 and abs(sv.max()-math.sqrt(8))<1e-10
    sizes=[[12,5,6,3,9,3,1,1],[10,9,4,8,3,2,2,2],[10,7,7,4,4,4,2,1,1],[13,6,6,5,2,5,1,2]]
    hist={i:0 for i in range(9)};units=0
    for br in sizes:
        for slot,n in enumerate(br):
            u=8-slot;hist[u]+=n;units+=u*n
    assert units==919 and hist=={0:1,1:6,2:6,3:14,4:18,5:20,6:23,7:27,8:45}
    slot=299792458*5e-12/2
    assert abs(units*slot-ds["d"]["exact_schedule_materialization"]["aggregate_delay_length_m"])<1e-15
    Q=np.array([[0,12,0],[1,2,9],[0,4,8]],float)
    for name,J in [("selector24",np.array([[2.,5.],[-21.,-20.]])),
                   ("selector15",np.array([[3.2,12.],[-21.,-10.]]))]:
        block=ds["n"]["point_stabilizer"][name];assert block["exhaustive_root_count"]==3
        for r in block["roots"]:assert np.linalg.norm(eq_rhs(np.array(r,float),Q,J))<1e-8
        eig=np.linalg.eigvals(eq_jac(np.array(block["roots"][1],float),Q,J));assert eig.real.max()<0
    I40=np.eye(40);J40=np.ones((40,40))
    S=(-1/3+2j/3)*I40+(1/6+1j/6)*A+(-1/60-1j/15)*J40
    assert np.allclose(S.conj().T@S,I40)
    assert (10**24)*(16**15)//40==28823037615171174400000000000000000000000
    assert (11**24)*(17**15)==28194101862441165313701387046733006325904913
    K=(I40+A)/3-(13/120)*J40;P0=J40/40
    assert np.allclose(K@K,I40-P0) and np.allclose(K@K@K,K)
    print(json.dumps({"status":ds["p"]["status"],"semantic_sha256":ds["p"]["semantic_sha256"],"couplers":84,"hodge_sigma_min":float(sv.min()),"delay_units":units,"point_roots":[3,3]},sort_keys=True))
if __name__=="__main__":main()
