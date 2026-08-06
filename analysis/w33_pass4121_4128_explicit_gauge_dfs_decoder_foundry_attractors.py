#!/usr/bin/env python3
"""Deterministic verifier for Passes 4121-4128."""
from __future__ import annotations
import hashlib, itertools, json, math
from collections import deque
from fractions import Fraction
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/"data/PART_4121_4128_EXPLICIT_GAUGE_DFS_DECODER_FOUNDRY_ATTRACTORS_BONKERS.json"
GAUGE=ROOT/"data/w33_pass4121_explicit_145_gauge_action.json"
FOUNDRY=ROOT/"data/w33_pass4124_cornerstone_floorplan_audit.json"
ATTR=ROOT/"data/w33_pass4125_attractor_orbit_census.json"
ROUTER=ROOT/"data/w33_pass4089_four_router_layout.json"

def chash(d):
    x=dict(d); x.pop("semantic_sha256",None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def points_f3():
    out=set()
    for v in itertools.product(range(3),repeat=4):
        if not any(v): continue
        i=next(i for i,x in enumerate(v) if x)
        z=1 if v[i]==1 else 2
        out.add(tuple((z*x)%3 for x in v))
    return sorted(out)

def symp(u,v):
    return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%3

def w33():
    pts=points_f3(); A=np.zeros((40,40),dtype=int)
    for i,u in enumerate(pts):
        for j,v in enumerate(pts):
            if i!=j and symp(u,v)==0: A[i,j]=1
    return pts,A

def levi(A):
    r=json.loads(ROUTER.read_text()); E=[]
    for L in r["lines"]:
        for p in L["point_ids"]: E.append((p,40+L["id"]))
    D=np.zeros((80,160)); adj=[[] for _ in range(80)]
    for e,(u,v) in enumerate(E):
        D[u,e]=1; D[v,e]=-1
        adj[u].append((v,e)); adj[v].append((u,e))
    return E,D,adj

def gauge_matrices():
    rt=math.sqrt
    lam=[np.array([[0,1,0],[1,0,0],[0,0,0]],complex),np.array([[0,-1j,0],[1j,0,0],[0,0,0]],complex),np.array([[1,0,0],[0,-1,0],[0,0,0]],complex),np.array([[0,0,1],[0,0,0],[1,0,0]],complex),np.array([[0,0,-1j],[0,0,0],[1j,0,0]],complex),np.array([[0,0,0],[0,0,1],[0,1,0]],complex),np.array([[0,0,0],[0,0,-1j],[0,1j,0]],complex),np.diag([1,1,-2])/rt(3)]
    T=[x/2 for x in lam]
    p=[np.array([[0,1],[1,0]],complex)/2,np.array([[0,-1j],[1j,0]],complex)/2,np.array([[1,0],[0,-1]],complex)/2]
    G3=[np.zeros((145,145),complex) for _ in range(8)]; G2=[np.zeros((145,145),complex) for _ in range(3)]; Y=np.zeros((145,145),complex)
    for a in range(8): G3[a][:6,:6]=np.kron(T[a],np.eye(2))
    for a in range(3): G2[a][:6,:6]=np.kron(np.eye(3),p[a])
    Y[:6,:6]=np.eye(6)/6; Y[6,6]=1
    off=7
    for orb in range(15):
        base=off+6*orb
        for a in range(8):
            G3[a][base:base+3,base:base+3]=-T[a].conj(); G3[a][base+3:base+6,base+3:base+6]=-T[a].conj()
        Y[base:base+3,base:base+3]=-2*np.eye(3)/3; Y[base+3:base+6,base+3:base+6]=np.eye(3)/3
    off=97
    for orb in range(24):
        base=off+2*orb
        for a in range(3): G2[a][base:base+2,base:base+2]=p[a]
        Y[base:base+2,base:base+2]=-np.eye(2)/2
    return G3,G2,Y

def phase_error(K,m,phi):
    th=math.pi/(K+2); c=np.array([math.sqrt(2/(K+2))*math.sin((n+1)*th) for n in range(K+1)])
    C=float(c[:K+1-m]@c[m:]); B=sum(c[n]*c[m-1-n] for n in range(m))
    z=np.exp(1j*m*phi)*C+np.exp(-1j*(K+1-m)*phi)*B
    return abs(z-np.exp(1j*m*phi))

def candidate_edges(adj,E,support):
    y=np.zeros(80)
    for e in support:
        u,v=E[e]; y[u]+=1; y[v]-=1
    S=[i for i,x in enumerate(y) if abs(x)>0.5]; out=set()
    for a,b in itertools.combinations(S,2):
        q=deque([(a,[])]); seen={a}; found=None
        while q:
            u,path=q.popleft()
            if len(path)>=3: continue
            for v,e in adj[u]:
                if v in seen: continue
                npth=path+[e]
                if v==b: found=npth; q.clear(); break
                seen.add(v); q.append((v,npth))
        if found is not None: out.update(found)
    return out

def inversion_count(perm):
    return sum(perm[i]>perm[j] for i in range(len(perm)) for j in range(i+1,len(perm)))

def main():
    cert=json.loads(CERT.read_text()); gauge=json.loads(GAUGE.read_text()); foundry=json.loads(FOUNDRY.read_text()); attr=json.loads(ATTR.read_text())
    assert chash(cert)==cert["semantic_sha256"] and chash(gauge)==gauge["semantic_sha256"] and chash(foundry)==foundry["semantic_sha256"] and chash(attr)==attr["semantic_sha256"]
    pts,A=w33(); assert A.sum(axis=1).tolist()==[12]*40; assert np.allclose(np.linalg.eigvalsh(A),[-4]*15+[2]*24+[12])
    G3,G2,Y=gauge_matrices(); assert all(np.max(abs(g-g.conj().T))<1e-14 for g in G3+G2+[Y]); assert max(np.max(abs(a@b-b@a)) for a in G3 for b in G2+[Y])<1e-14
    q,u,d,l,e=1,15,15,24,1
    assert 2*q-u-d==-28 and Fraction(q-2*u+d,3)==Fraction(-7,3) and Fraction(3*q-l,4)==Fraction(-23,4) and q-2*u+d-l+e==-37
    M=np.array([[2,-1,-1,0,0],[1,-2,1,0,0],[1,0,0,-1,0],[1,-2,1,-1,1]],float); ns=np.linalg.svd(M)[2][-1]; assert np.allclose(ns/ns[0],np.ones(5))
    phi=math.atan2(3,-4)
    for row in cert["pass4122_relational_phase_subsystem"]["rows"]:
        assert abs(row["K256_encoded_clock_error"]-phase_error(256,1,phi))<2e-13
        assert abs(row["K256_direct_worst_error"]-phase_error(256,row["total_logical_qubits"],phi))<2e-13
        assert row["paired_sector_dimension"]==math.comb(row["physical_modes"],row["weights"][0])
    E,D,adj=levi(A); assert np.linalg.matrix_rank(D)==79
    maxc=0; worst=None
    for r in range(4):
        for supp in itertools.combinations(range(160),r):
            c=candidate_edges(adj,E,supp)
            if len(c)>maxc: maxc=len(c); worst=(supp,sorted(c))
    assert maxc==20 and worst[0]==tuple(cert["pass4123_graph_aware_decoder"]["worst_case_support_edge_ids"]) and worst[1]==cert["pass4123_graph_aware_decoder"]["worst_case_candidate_edge_ids"]
    assert 1+20+math.comb(20,2)+math.comb(20,3)==1351
    router=json.loads(ROUTER.read_text()); po=foundry["balanced_ordering"]["point_order"]; lo=foundry["balanced_ordering"]["line_order"]; ppos={x:i for i,x in enumerate(po)}; lpos={x:i for i,x in enumerate(lo)}
    inv=[]; max_path=0
    for R in router["routers"]:
        perm=[None]*40
        for p,l in R["pairs"]: perm[ppos[p]]=lpos[l]
        inv.append(inversion_count(perm))
        for i in range(40): max_path=max(max_path,sum((i-j)*(perm[i]-perm[j])<0 for j in range(40)))
    assert inv==foundry["balanced_ordering"]["one_direction_inversions"] and 2*sum(inv)==1934 and max_path==21
    plus=cert["pass4126_bonkers_antiferromagnetic_Ising"]["witness_plus_vertices"]; s=-np.ones(40); s[plus]=1
    assert np.allclose(A@s,-4*s); cut=sum(s[i]!=s[j] for i in range(40) for j in range(i+1,40) if A[i,j]); assert cut==160
    I=np.eye(40); J=np.ones((40,40)); P2=-(A-12*I)@(A+4*I)/60; U=I-2*P2
    assert np.allclose(U@U,I) and np.allclose(U,-(I+A)/3+2*J/15)
    col=U[:,0]**2; assert abs(col[0]-Fraction(1,25))<1e-14 and abs(col[A[0]==1].sum()-Fraction(12,25))<1e-14 and abs(col[A[0]==0].sum()-col[0]-Fraction(12,25))<1e-14
    g=1.0; B=np.array([[1j*g,g],[g,-1j*g]],complex); H=np.kron(np.eye(15),B)
    assert np.linalg.matrix_rank(H,tol=1e-10)==15 and np.max(abs(H@H))<1e-12
    print(json.dumps({"status":cert["status"],"semantic_sha256":cert["semantic_sha256"],"decoder_max_candidate_edges":maxc,"crossings":1934,"maxcut":cut,"simultaneous_EP2":15},sort_keys=True))

if __name__=="__main__": main()
