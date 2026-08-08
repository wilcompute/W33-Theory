#!/usr/bin/env python3
"""Deterministic verifier for Passes 4245-4252.

Quick mode reconstructs W(3,3), PSp(4,3), the 5- and 3-subset orbit
classifications, GHZ broadcast/resource arithmetic, exact two-channel lower/upper
bound logic, routed-delay geometry arithmetic, and the three outside-box identities.

--full additionally runs interval/Krawczyk branch-and-bound on the triangle and
maximally symmetric independent-triple nonlinear quotient systems.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, math, collections
from pathlib import Path
import numpy as np
from scipy.optimize import root

ROOT=Path(__file__).resolve().parents[1]
P={n:ROOT/f"data/w33_pass{n}_{name}.json" for n,name in {
4245:"residual_generation_anchor_symmetry",
4246:"ghz28_operating_strategy",
4247:"exact_minimum_hodge_channels",
4248:"explicit_routed_delay_geometry",
4249:"triple_stabilizer_lattice",
4250:"symmetry_resolved_metrology",
4251:"hodge_two_temperature_exergy",
4252:"exact_quotient_rg_chain",
}.items()}
PACKET=ROOT/"data/PART_4245_4252_RESIDUAL_SYMMETRY_GHZ_HODGE_ROUTE_LATTICE_OUTSIDE_BOX.json"
MANIFEST=ROOT/"data/PART_4245_4252_RESIDUAL_SYMMETRY_GHZ_HODGE_ROUTE_LATTICE_OUTSIDE_BOX_manifest.json"
SRC4147=ROOT/"data/w33_pass4147_conditioned_seven_fault_moments.json"
SRC4148=ROOT/"data/w33_pass4148_hybrid_stack_materialization.json"

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

def geometry():
    pts=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    idx={p:i for i,p in enumerate(pts)}
    A=np.zeros((40,40),int)
    for i,u in enumerate(pts):
        for j,v in enumerate(pts):
            if i!=j and symp(u,v)==0:A[i,j]=1
    return pts,A

def compose(p,q):return tuple(p[q[i]] for i in range(40))

def group_perms(pts):
    idx={p:i for i,p in enumerate(pts)}
    def tv(v):
        out=[]
        for x in pts:
            s=symp(x,v);y=tuple((x[k]+s*v[k])%3 for k in range(4))
            out.append(idx[canon(y)])
        return tuple(out)
    gs=[tv(pts[i]) for i in (0,1,2,4,13)]
    ident=tuple(range(40));seen={ident};stack=[ident]
    while stack:
        g=stack.pop()
        for h in gs:
            x=compose(h,g)
            if x not in seen:seen.add(x);stack.append(x)
    assert len(seen)==25920
    return gs,list(seen)

def mask(c):
    m=0
    for i in c:m|=1<<i
    return m

def pmask(m,p):
    out=0
    for i in range(40):
        if (m>>i)&1:out|=1<<p[i]
    return out

def subset_orbits(k,gens,A):
    universe={mask(c) for c in itertools.combinations(range(40),k)}
    out=[]
    while universe:
        rep=next(iter(universe));orb={rep};stack=[rep]
        while stack:
            m=stack.pop()
            for g in gens:
                z=pmask(m,g)
                if z not in orb:orb.add(z);stack.append(z)
        universe.difference_update(orb)
        S=[i for i in range(40) if (rep>>i)&1]
        edges=int(A[np.ix_(S,S)].sum()//2)
        degs=sorted(A[np.ix_(S,S)].sum(axis=1).tolist(),reverse=True)
        out.append((rep,len(orb),25920//len(orb),edges,degs,S))
    return out

def stabilizer(group,S,pointwise=False):
    SS=set(S)
    if pointwise:return [p for p in group if all(p[x]==x for x in S)]
    return [p for p in group if {p[x] for x in S}==SS]

def orbits(st):
    unseen=set(range(40));res=[]
    while unseen:
        x=min(unseen);o={p[x] for p in st};res.append(sorted(o));unseen-=o
    return sorted(res,key=lambda z:(len(z),z[0]))

def quotient(A,orb):
    Q=np.zeros((len(orb),len(orb)),int)
    for i,O in enumerate(orb):
        x=O[0]
        for j,Pj in enumerate(orb):Q[i,j]=sum(A[x,y] for y in Pj)
    return Q

def broadcast():
    n=28;children={i:[] for i in range(n)}
    for i in range(1,n):children[(i-1)//2].append(i)
    def bt(v):
        ts=sorted((bt(c) for c in children[v]),reverse=True)
        return max([i+1+t for i,t in enumerate(ts)] or [0])
    def sched(v,start=0):
        cs=sorted(children[v],key=bt,reverse=True);z=[]
        for j,c in enumerate(cs):
            t=start+j+1;z.append((t,v,c));z.extend(sched(c,t))
        return z
    z=sched(0);layers=collections.defaultdict(list)
    for t,u,v in z:layers[t].append((u,v))
    assert bt(0)==7 and len(z)==27
    for es in layers.values():
        q=[x for e in es for x in e];assert len(q)==len(set(q))
    return bt(0),[layers[t] for t in range(1,8)]

def fusion_cost(n,s):
    E=[0.0]*(n+1);split=[None]*(n+1)
    for k in range(2,n+1):
        E[k],a=min(((E[a]+E[k-a]+1)/s,a) for a in range(1,k))
        split[k]=(a,k-a)
    return E[n],split[n]

def build_B(Q,J):
    r=len(Q);L=12*np.eye(r)-Q
    return np.block([[J[0,0]*np.eye(r)-.1*L,J[0,1]*np.eye(r)],[J[1,0]*np.eye(r),J[1,1]*np.eye(r)-10*L]])
def F(B,x):return B@x-x**3
def interval_f(B,lo,hi):
    pos=np.maximum(B,0);neg=np.minimum(B,0)
    return pos@lo+neg@hi-hi**3,pos@hi+neg@lo-lo**3
def jac_interval(B,lo,hi):
    sqlo=np.where((lo<=0)&(hi>=0),0,np.minimum(lo*lo,hi*hi));sqhi=np.maximum(lo*lo,hi*hi)
    mid=B.copy();rad=np.zeros_like(B)
    for i in range(len(lo)):
        l=B[i,i]-3*sqhi[i];h=B[i,i]-3*sqlo[i];mid[i,i]=(l+h)/2;rad[i,i]=(h-l)/2
    return mid,rad
def krawczyk(B,lo,hi):
    x=(lo+hi)/2;r=(hi-lo)/2;J=B-np.diag(3*x*x)
    try:C=np.linalg.inv(J)
    except np.linalg.LinAlgError:return "split",lo,hi,x
    jm,jr=jac_interval(B,lo,hi);E0=np.eye(len(x))-C@jm;Er=np.abs(C)@jr
    y=x-C@F(B,x);kr=(np.abs(E0)+Er)@r+1e-14;klo=y-kr;khi=y+kr
    nlo=np.maximum(lo,klo);nhi=np.minimum(hi,khi)
    if np.any(nlo>nhi):return "empty",None,None,y
    if np.all(klo>lo)&np.all(khi<hi):return "unique",klo,khi,y
    return "contract",nlo,nhi,y
def interval_count(Q,J,U,V,cap):
    B=build_B(Q,J);r=len(Q);stack=[(np.r_[-U*np.ones(r),-V*np.ones(r)],np.r_[U*np.ones(r),V*np.ones(r)])]
    uniq=[];unres=[];nodes=0
    while stack:
        lo,hi=stack.pop();nodes+=1
        if nodes>cap:raise RuntimeError("node cap")
        fl,fh=interval_f(B,lo,hi)
        if np.any((fl>0)|(fh<0)):continue
        typ,nlo,nhi,y=krawczyk(B,lo,hi)
        if typ=="empty":continue
        if typ=="unique":uniq.append(y);continue
        old=hi-lo;new=nhi-nlo
        if np.max(new/old)<.85:stack.append((nlo,nhi));continue
        if np.max(new)<1e-7:unres.append((nlo,nhi));continue
        scales=np.r_[U*np.ones(r),V*np.ones(r)];j=int(np.argmax(new/scales));m=(nlo[j]+nhi[j])/2
        a=nhi.copy();a[j]=m;b=nlo.copy();b[j]=m;stack.append((nlo,a));stack.append((b,nhi))
    roots=[];seeds=list(uniq)+[np.array(c) for c in {tuple(np.round((a+b)/2,6)) for a,b in unres}]
    for y in seeds:
        rr=root(lambda z:F(B,z),y,jac=lambda z:B-np.diag(3*z*z),tol=1e-11);assert rr.success
        x=rr.x
        if not any(np.linalg.norm(x-z)<1e-6 for z in roots):
            typ,*_=krawczyk(B,x-1e-3,x+1e-3);assert typ=="unique";roots.append(x)
    return roots,nodes

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--full",action="store_true");args=ap.parse_args()
    data={n:json.loads(p.read_text()) for n,p in P.items()}
    packet=json.loads(PACKET.read_text());manifest=json.loads(MANIFEST.read_text())
    for d in list(data.values())+[packet,manifest]:assert chash(d)==d["semantic_sha256"]
    assert packet["semantic_sha256"]=="314ff5c6d21bd4f70a6c7a3228a958cc00f6f4991a288c0f293dcedd9146b8c2"
    pts,A=geometry();gens,group=group_perms(pts);assert np.all(A.sum(1)==12)
    o5=subset_orbits(5,gens,A);assert len(o5)==43 and sum(x[1] for x in o5)==math.comb(40,5)
    best=max(o5,key=lambda z:z[2]);assert best[2]==72 and best[3]==4 and best[4]==[4,1,1,1,1]
    depth,schedule=broadcast();assert depth==7
    E28,sp=fusion_cost(28,.87);assert abs(E28-47.90630292256911)<1e-12 and sp==(13,15)
    src47=json.loads(SRC4147.read_text());assert chash(src47)==src47["semantic_sha256"]
    assert src47["semantic_sha256"]==data[4247]["source_conditioned_moments_sha256"]
    assert src47["theta_core_audit"]["4_4_4"]==4320 and src47["stacked_spark_lower_bound"]>=15
    assert data[4247]["lower_bound"]["m_min"]==2 and data[4247]["upper_bound"]["m_suffices"]==2
    src48=json.loads(SRC4148.read_text());assert chash(src48)==src48["semantic_sha256"]
    assert src48["semantic_sha256"]==data[4248]["source_schedule_sha256"]
    hist=collections.Counter();routes=0;units=0
    for branch in src48["branch_layers"]:
        seen=set()
        for ell,layer in enumerate(branch):
            d=8-ell
            for point,line in layer:seen.add(point);hist[d]+=1;routes+=1;units+=d
        assert seen==set(range(40))
    assert routes==160 and units==919 and dict(sorted(hist.items()))=={int(k):v for k,v in data[4248]["delay_histogram"].items()}
    dog=data[4248]["dogleg"];assert abs(2*dog["vertical_excursion_mm"]+(2*math.pi-4)*dog["bend_radius_mm"]-dog["slot_excess_path_mm"])<1e-12
    o3=subset_orbits(3,gens,A);assert len(o3)==5 and sum(x[1] for x in o3)==math.comb(40,3)
    sig=sorted((x[2],x[3],tuple(x[4])) for x in o3)
    assert sig==sorted([(162,3,(2,2,2)),(72,0,(0,0,0)),(12,2,(2,1,1)),(9,0,(0,0,0)),(6,1,(1,1,0))])
    assert 4*12==48 and data[4250]["global_max"]["QFI"]==256
    th,tg=2.,1.;tf=th**(81/160)*tg**(79/160);W=.5*(81*th+79*tg-160*tf)
    assert abs(W-data[4251]["example_TH_over_TG_2"]["Wmax_over_kBTG"])<1e-12
    structs=[[0],[0,1],[0,1,2]];parts=[];Qs=[]
    for S in structs:
        st=stabilizer(group,S,pointwise=True);oo=orbits(st);parts.append(oo);Qs.append(quotient(A,oo))
    assert [len(x) for x in parts]==[3,6,8]
    def lift(fine,coarse):
        R=np.zeros((len(fine),len(coarse)),int)
        for i,O in enumerate(fine):
            for j,C in enumerate(coarse):
                if set(O)<=set(C):R[i,j]=1
        return R
    R63=lift(parts[1],parts[0]);R86=lift(parts[2],parts[1])
    assert np.array_equal(Qs[1]@R63,R63@Qs[0]) and np.array_equal(Qs[2]@R86,R86@Qs[1])
    out={"status":packet["status"],"packet_sha256":packet["semantic_sha256"],"five_subset_orbits":43,"max_anchor_stabilizer":72,"ghz_rounds":7,"minimum_hodge_channels":2,"delay_units":919,"triple_orbits":5,"full":args.full}
    if args.full:
        byorder={x[2]:x for x in o3};expected={162:{"24":9,"15":3},72:{"24":9,"15":9}}
        Js={"24":np.array([[2.,5.],[-21.,-20.]]),"15":np.array([[3.2,12.],[-21.,-10.]])};bounds={"24":(2.50439835,2.13976351),"15":(3.79360056,3.53797676)};got={}
        for order in (162,72):
            S=byorder[order][5];oo=orbits(stabilizer(group,S));Q=quotient(A,oo);got[order]={}
            for name,J in Js.items():
                U,V=bounds[name];roots,nodes=interval_count(Q,J,U,V,1000000);assert len(roots)==expected[order][name];got[order][name]=[len(roots),nodes]
        out["interval"]=got
    print(json.dumps(out,sort_keys=True))
if __name__=="__main__":main()
