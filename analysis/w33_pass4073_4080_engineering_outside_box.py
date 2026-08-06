#!/usr/bin/env python3
"""Deterministic verifier for Passes 4073-4080."""
from __future__ import annotations
import cmath, hashlib, itertools, json, math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data/PART_4073_4080_ENGINEERING_OUTSIDE_BOX.json"

def canonical_sha(obj):
    x=dict(obj); x.pop("semantic_sha256",None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def build_w33():
    pts=[]
    for v in itertools.product(range(3),repeat=4):
        if not any(v): continue
        for x in v:
            if x:
                inv=1 if x==1 else 2
                w=tuple((inv*y)%3 for y in v)
                if w not in pts: pts.append(w)
                break
    pts=sorted(pts); idx={v:i for i,v in enumerate(pts)}
    def symp(u,v):
        return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%3
    lines=set()
    for i,u in enumerate(pts):
        for j in range(i+1,len(pts)):
            v=pts[j]
            if symp(u,v): continue
            members=set()
            for a,b in itertools.product(range(3),repeat=2):
                if not (a or b): continue
                w=tuple((a*u[k]+b*v[k])%3 for k in range(4))
                for x in w:
                    if x:
                        inv=1 if x==1 else 2
                        wc=tuple((inv*y)%3 for y in w)
                        break
                members.add(idx[wc])
            if len(members)==4: lines.add(tuple(sorted(members)))
    lines=sorted(lines)
    B=np.zeros((40,40),dtype=int)
    for j,L in enumerate(lines):
        for i in L: B[i,j]=1
    return pts,lines,B

def perfect_matching(B):
    n=B.shape[0]; matchR=[-1]*n
    def dfs(u,seen):
        for v in range(n):
            if B[u,v] and not seen[v]:
                seen[v]=True
                if matchR[v] < 0 or dfs(matchR[v],seen):
                    matchR[v]=u; return True
        return False
    for u in range(n): assert dfs(u,[False]*n)
    return sorted((u,v) for v,u in enumerate(matchR))

def factorize(B):
    C=B.copy(); out=[]
    for _ in range(4):
        m=perfect_matching(C); out.append(m)
        for u,v in m: C[u,v]=0
    assert C.sum()==0
    return out

def binom_overlap(K):
    return sum(math.sqrt(float(math.comb(K,n-1))*float(math.comb(K,n)))
               for n in range(1,K+1))/(2.0**K)

def main():
    data=json.loads(DATA.read_text())
    assert canonical_sha(data)==data["semantic_sha256"]
    pts,lines,B=build_w33()
    assert len(pts)==len(lines)==40
    assert np.all(B.sum(0)==4) and np.all(B.sum(1)==4)
    matchings=factorize(B)
    fsha=hashlib.sha256(json.dumps(matchings,separators=(",",":")).encode()).hexdigest()
    assert fsha==data["pass4073_physical_four_router_block_encoding"]["factorization_sha256"]
    A=np.block([[np.zeros((40,40),int),B],[B.T,np.zeros((40,40),int)]])
    Ps=[]
    for matching in matchings:
        P=np.zeros((80,80),dtype=int)
        for i,j in matching: P[i,40+j]=P[40+j,i]=1
        assert np.array_equal(P@P,np.eye(80,dtype=int))
        Ps.append(P)
    assert np.array_equal(sum(Ps),A)
    vals=np.linalg.eigvalsh(A/4.0)
    targets=np.array([-1]+[-math.sqrt(6)/4]*24+[0]*30+[math.sqrt(6)/4]*24+[1])
    assert np.max(np.abs(vals-targets))<2e-12

    phi=math.atan2(3,-4)
    for sample in data["pass4074_binomial_phase_reference"]["samples"]:
        K=sample["K"]; S=binom_overlap(K)
        z=cmath.exp(1j*phi)*S+2.0**(-K)*cmath.exp(-1j*K*phi)
        assert abs(S-sample["S_K"])<2e-15
        assert abs(z.real-sample["coherence_multiplier"][0])<2e-15
        assert abs(z.imag-sample["coherence_multiplier"][1])<2e-15
        assert abs(abs(z-cmath.exp(1j*phi))-sample["channel_error_to_ideal"])<2e-15
        assert abs(1-abs(z)**2-sample["reference_branch_infidelity"])<2e-15

    ext=data["pass4075_minimal_nonabelian_multiplicity_extension"]
    assert ext["minimum_exact_factor_extension"]["dimension"]==3+24+2*15
    assert ext["minimum_bifundamental_carrier"]["dimension"]==6+24+15
    assert 30%2==0

    gaps=np.array([4-math.sqrt(6),4,4+math.sqrt(6),8],float)
    coeff=np.poly(-gaps*gaps)
    assert np.max(np.abs(coeff-np.array([1,124,4644,53056,102400],float)))<1e-9
    for d in gaps: assert abs(np.prod(gaps*gaps-d*d))<2e-9

    edges=list(zip(*np.where(B)))
    D=np.zeros((80,160),float)
    for e,(i,j) in enumerate(edges): D[i,e]=-1; D[40+j,e]=1
    rank=np.linalg.matrix_rank(D,tol=1e-10)
    assert rank==79 and 160-rank==81
    lv=np.linalg.eigvalsh(D@D.T)
    ltarget=np.array([0]+[4-math.sqrt(6)]*24+[4]*30+[4+math.sqrt(6)]*24+[8])
    assert np.max(np.abs(lv-ltarget))<3e-11

    q=data["pass4079_bonkers_quantum_quench_work"]["sample"]
    beta=q["beta"]; g0=q["g0"]; g1=q["g1"]
    Z0=1+24*math.exp(-10*beta*g0)+15*math.exp(-16*beta*g0)
    Z1=1+24*math.exp(-10*beta*g1)+15*math.exp(-16*beta*g1)
    ps=[1/Z0,24*math.exp(-10*beta*g0)/Z0,15*math.exp(-16*beta*g0)/Z0]
    ws=[0,10*(g1-g0),16*(g1-g0)]
    jar=sum(p*math.exp(-beta*w) for p,w in zip(ps,ws))
    assert abs(jar-Z1/Z0)<2e-15 and abs(jar-q["Jarzynski_average"])<2e-15

    assert data["pass4080_bonkers_Kuramoto_synchronization"]["timescale_ratio"]=="tau_slow/tau_fast=8/5"
    assert len(data["pass4077_experimental_falsification_suite"]["contracts"])==6
    print("PASS_4073_4080",data["semantic_sha256"],fsha)
if __name__=="__main__": main()
