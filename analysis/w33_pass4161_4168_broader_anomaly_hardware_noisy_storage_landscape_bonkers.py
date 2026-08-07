#!/usr/bin/env python3
"""Deterministic verifier for Passes 4161-4168."""
from __future__ import annotations
import collections, hashlib, itertools, json, math
from pathlib import Path
import networkx as nx
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import Bounds, LinearConstraint, milp, root

ROOT=Path(__file__).resolve().parents[1]
ANOM=ROOT/"data/w33_pass4161_broader_rep_anomaly_optimization.json"
HW=ROOT/"data/w33_pass4162_relational_hardware_graph.json"
DEC=ROOT/"data/w33_pass4163_quantized_noisy_t7_decoder.json"
STORAGE=ROOT/"data/w33_pass4164_storage_primitive_comparison.json"
LAND=ROOT/"data/w33_pass4165_global_mixed_landscape_push.json"
CERT=ROOT/"data/PART_4161_4168_BROADER_ANOMALY_HARDWARE_NOISY_STORAGE_LANDSCAPE_BONKERS.json"

def chash(d):
    x=dict(d); x.pop("semantic_sha256",None)
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
    lines=set()
    for i,u in enumerate(pts):
        for j,v in enumerate(pts):
            if j<=i or symp(u,v):continue
            S={idx[canon(tuple(a*u[k]+b*v[k] for k in range(4)))]
               for a,b in itertools.product(range(3),repeat=2) if a or b}
            if len(S)==4:lines.add(tuple(sorted(S)))
    lines=sorted(lines)
    G=nx.Graph();G.add_nodes_from(range(80));E=[]
    for l,L in enumerate(lines):
        for p in L:E.append((p,40+l));G.add_edge(p,40+l)
    D=np.zeros((80,160),int)
    for e,(p,l) in enumerate(E):D[p,e]=1;D[l,e]=-1
    return pts,A,lines,E,D,G

SU3={"1":(1,0,0),"3":(3,1,1),"3bar":(3,1,-1),"6":(6,5,7),"6bar":(6,5,-7),"8":(8,6,0)}
SU2={1:(1,0,False),2:(2,1,True),3:(3,4,False)}
def avec(r3,r2,n):
    d3,t3,a3=SU3[r3];d2,t2,_=SU2[r2]
    return np.array([a3*d2,t3*d2*n,t2*d3*n,d3*d2*n,d3*d2*n**3],int)

def anomaly_audit(d):
    orig=[("3",2,1,1),("3bar",1,-4,15),("3bar",1,2,15),("1",2,-3,24),("1",1,6,1)]
    Aorig=sum((w*avec(r3,r2,n) for r3,r2,n,w in orig),np.zeros(5,dtype=int))
    assert Aorig.tolist()==[-28,-28,-69,-222,-3594]
    species=[]
    for r3 in SU3:
        for r2 in SU2:
            for n in range(-6,7):
                v=avec(r3,r2,n)
                if not np.any(v):continue
                d3,t3,_=SU3[r3];d2,t2,_=SU2[r2]
                species.append((r3,r2,n,d3*d2,d3%2 if r2==2 else 0,(t3/2)*d2,(t2/2)*d3,v))
    assert len(species)==228
    m=len(species);A=np.column_stack([s[7] for s in species]).astype(float)
    par=np.array([s[4] for s in species],float);dims=np.array([s[3] for s in species],float)
    Aeq=np.zeros((6,m+1));Aeq[:5,:m]=A;Aeq[5,:m]=par;Aeq[5,m]=-2
    beq=np.r_[-Aorig,1.0]
    bounds=Bounds(np.zeros(m+1),np.r_[np.full(m,100.),10000.])
    integ=np.ones(m+1)
    res=milp(np.r_[dims,0.],integrality=integ,bounds=bounds,constraints=LinearConstraint(Aeq,beq,beq))
    assert res.success and abs(res.fun-68)<1e-8
    t3=np.array([s[5] for s in species],float)
    r3=milp(np.r_[t3,0.],integrality=integ,bounds=bounds,constraints=LinearConstraint(Aeq,beq,beq))
    assert r3.success and abs(r3.fun-11)<1e-8
    total=np.zeros(5,dtype=int);dim=0;mult=0;parity=0;t3load=t2load=0.0
    for row in d["solution"]:
        q=row["multiplicity"];r3n=row["SU3"];r2=row["SU2_dimension"];n=row["n"]
        total+=q*avec(r3n,r2,n);dim+=q*row["state_dimension"];mult+=q
        d3,t3i,_=SU3[r3n];d2,t2i,_=SU2[r2]
        parity+=q*(d3%2 if r2==2 else 0)
        t3load+=q*(t3i/2)*d2;t2load+=q*(t2i/2)*d3
    assert total.tolist()==[28,28,69,222,3594] and dim==68 and mult==35 and parity%2==1
    assert abs(t3load-11)<1e-12 and abs(t2load-7.5)<1e-12

def hardware_audit(d):
    G=nx.Graph();G.add_nodes_from(range(58))
    for a,b in d["physical_edges"]:G.add_edge(a,b)
    assert G.number_of_edges()==139 and max(dict(G.degree()).values())==7
    assert collections.Counter(dict(G.degree()).values())=={1:1,3:29,5:2,6:2,7:24}
    T=nx.Graph();T.add_nodes_from(range(28));T.add_edges_from(d["logical_edges"])
    assert nx.is_tree(T) and nx.diameter(T)==8 and nx.eccentricity(T,0)==4
    assert d["routing"]["arbitrary_payload_CNOT_depth_upper_bound"]==2*(8-1)+1
    assert d["routing"]["clock_controlled_payload_depth_upper_bound"]==2*4+1
    assert d["GHZ28"]["total_depth"]==5

def decoder_audit(d):
    assert d["inherits_conditioned_measurement_certificate"]=="ab02380ad1973a6155d99d479768c036435157a203c16aa7c792975024bb26dd"
    W=d["conditioning_inherited"]["maximum_coefficient"]
    assert W==11992
    for K,bits in ((1,18),(3,19),(15,22)):
        M=7*K*W
        assert math.ceil(math.log2(2*M+1))==bits
    assert d["modular_mode"]["prime"]==24001 and math.ceil(math.log2(24001))==15
    Delta=0.25
    z=np.array([3,-2,1],float);eta=np.array([.49,-.49,.1])*Delta
    assert np.array_equal(np.rint((Delta*z+eta)/Delta).astype(int),z.astype(int))

def storage_audit(d):
    c=299792458.0;lam=1550e-9;f=c/lam;omega=2*math.pi*f;t=40e-12
    taps=[k*c*5e-12/2*1e3 for k in range(9)]
    assert np.allclose(taps,d["design_point"]["tap_lengths_mm"])
    assert abs(taps[-1]-5.99584916)<1e-8
    Qreq=4.343*omega*t
    assert abs(Qreq-d["single_pole_resonator"]["Q_required_for_40ps_storage_below_1dB"])<1e-6
    BW=.44/5e-12;Qbw=f/BW
    loss=4.343*omega*t/Qbw
    assert loss>90 and d["single_pole_resonator"]["storage_loss_dB_if_Q_meets_5ps_bandwidth"]>90
    assert d["fixed_delay_bank"]["five_use_delay_propagation_loss_dB_upper"]==0.15

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
    return np.array(list(seen),dtype=np.int16)
def lexmin(arr):
    ids=np.arange(arr.shape[0])
    for j in range(arr.shape[1]):
        v=arr[ids,j];m=v.min();ids=ids[v==m]
        if len(ids)==1:break
    return tuple(arr[ids[0]].tolist())
def field_hash(y,perms):
    u=np.rint(y[:40]*1e6).astype(np.int64);v=np.rint(y[40:]*1e6).astype(np.int64)
    arr=np.hstack([u[perms],v[perms]])
    key=min(lexmin(arr),lexmin(-arr))
    return hashlib.sha256(np.array(key,dtype=np.int64).tobytes()).hexdigest()
def dyn(A,J):
    L=12*np.eye(40)-A;a,b=J[0];c,d=J[1]
    def rhs(y):
        u=y[:40];v=y[40:]
        return np.r_[a*u+b*v-u**3-.1*(L@u),c*u+d*v-v**3-10*(L@v)]
    def jac(y):
        u=y[:40];v=y[40:]
        return np.block([[a*np.eye(40)-np.diag(3*u*u)-.1*L,b*np.eye(40)],
                         [c*np.eye(40),d*np.eye(40)-np.diag(3*v*v)-10*L]])
    return rhs,jac
def corpus(A,perms,J,nseeds,base,amp,tmax,small=False):
    rhs,jac=dyn(A,J);out={}
    macro_rng=np.random.default_rng(base) if not small else None
    for s in range(nseeds):
        if small:
            rng=np.random.default_rng(s)
            y0=amp*rng.normal(size=80);y0[:40]-=y0[:40].mean();y0[40:]-=y0[40:].mean()
        else:
            y0=macro_rng.uniform(-amp,amp,80)
        sol=solve_ivp(lambda t,y:rhs(y),(0,tmax),y0,method="BDF",rtol=2e-7 if not small else 1e-8,atol=2e-9 if not small else 1e-10)
        rr=root(rhs,sol.y[:,-1],jac=jac,tol=1e-10)
        if np.linalg.norm(rhs(rr.x))>=1e-7: continue
        y=rr.x;h=field_hash(y,perms)
        if h not in out:
            eig=np.linalg.eigvals(jac(y));u=y[:40];v=y[40:]
            pure=np.std(np.abs(u))<1e-5 and np.std(np.abs(v))<1e-5 and np.min(np.abs(u))>1e-4
            out[h]={"seed":s,"count":0,"morse_index":int(np.sum(eig.real>1e-8)),
                    "pure_bivalent":bool(pure) if not small else bool(pure)}
        out[h]["count"]+=1
    return out
def landscape_audit(A,pts,d):
    for key,J,guess in (("selector24",np.array([[2.,5.],[-21.,-20.]]),(2.5,2.1)),
                        ("selector15",np.array([[3.2,12.],[-21.,-10.]]),(3.8,3.5))):
        a,b=J[0];c,dd=J[1]
        rr=root(lambda z:[z[0]**3-a*z[0]-abs(b)*z[1],z[1]**3+abs(dd)*z[1]-abs(c)*z[0]],guess)
        assert rr.success
        stored=d["global_maximum_principle_boxes"][key]
        assert abs(rr.x[0]-stored["U_abs_upper"])<1e-7 and abs(rr.x[1]-stored["V_abs_upper"])<1e-7
    perms=group_perms(pts)
    m24=corpus(A,perms,np.array([[2.,5.],[-21.,-20.]]),64,20260901,.5,160,False)
    frozen24={r["hash"]:r for r in d["selector24"]["representatives"]}
    assert set(m24)==set(frozen24)
    assert len(m24)==29
    mixed24={h for h,v in m24.items() if not v["pure_bivalent"]}
    assert len(mixed24)==24 and sum(m24[h]["morse_index"]==0 for h in mixed24)==23
    small24=corpus(A,perms,np.array([[2.,5.],[-21.,-20.]]),64,0,1e-3,500,True)
    smallmix={h for h,v in small24.items() if not v["pure_bivalent"]}
    assert len(smallmix)==18 and len(mixed24&smallmix)==4 and len(mixed24-smallmix)==20
    m15=corpus(A,perms,np.array([[3.2,12.],[-21.,-10.]]),64,20260902,.5,160,False)
    frozen15={r["hash"]:r for r in d["selector15"]["representatives"]}
    assert set(m15)==set(frozen15)
    mixed15={h for h,v in m15.items() if not v["pure_bivalent"]}
    assert len(m15)==4 and len(mixed15)==3 and sum(m15[h]["morse_index"]==0 for h in mixed15)==2

def bonkers_audit(A,G,cert):
    I=np.eye(40);J=np.ones((40,40))
    P0=(A@A+2*A-8*I)/160
    assert np.allclose(P0,J/40)
    R=2*P0-I
    assert np.allclose(R@R,I)
    theta=math.asin(1/math.sqrt(40))
    p4=math.sin(9*theta)**2
    assert abs(p4-3920137321/4000000000)<1e-14
    L=12*I-A;Lp=(7/80)*I+(1/160)*A-(13/3200)*J
    assert np.allclose(L@Lp,I-J/40)
    adj=[];non=[]
    for i in range(40):
        for j in range(i+1,40):
            r=Lp[i,i]+Lp[j,j]-2*Lp[i,j]
            (adj if A[i,j] else non).append(r)
    assert len(adj)==240 and len(non)==540
    assert max(abs(x-13/80) for x in adj)<1e-12 and max(abs(x-7/40) for x in non)<1e-12
    assert abs(40*np.trace(Lp)-267/2)<1e-12
    dist=dict(nx.all_pairs_shortest_path_length(G));stats=collections.Counter()
    for u in range(80):
        for v in range(u+1,80):
            dd=dist[u][v]
            interval=[x for x in G if dist[u][x]+dist[x][v]==dd]
            layers=tuple(sum(1 for x in interval if dist[u][x]==k) for k in range(dd+1))
            layer=[x for x in G if dist[u][x]<=dd and dist[u][x]+dist[x][v]==dd]
            ways={u:1}
            for k in range(dd):
                for x in [q for q in layer if dist[u][q]==k]:
                    for y in G.neighbors(x):
                        if y in layer and dist[u][y]==k+1:ways[y]=ways.get(y,0)+ways[x]
            stats[(dd,len(interval),ways[v],layers)]+=1
    expected={(1,2,1,(1,1)):160,(2,3,1,(1,1,1)):480,
      (3,4,1,(1,1,1,1)):1440,(4,14,4,(1,4,4,4,1)):1080}
    assert stats==expected

def main():
    docs=[json.loads(p.read_text()) for p in (ANOM,HW,DEC,STORAGE,LAND,CERT)]
    an,hw,de,st,la,cert=docs
    for x in (an,hw,de,st,la,cert):assert chash(x)==x["semantic_sha256"]
    pts,A,lines,E,D,G=geometry()
    assert len(pts)==len(lines)==40 and len(E)==160 and nx.diameter(G)==4
    anomaly_audit(an);hardware_audit(hw);decoder_audit(de);storage_audit(st)
    landscape_audit(A,pts,la);bonkers_audit(A,G,cert)
    print(json.dumps({"status":cert["status"],"semantic_sha256":cert["semantic_sha256"],
      "anomaly_total":213,"hardware_max_degree":7,"quantized_noise_margin":"Delta/2",
      "storage_five_use_delay_dB":0.15,"selector24_new_macro_mixed":20,
      "grover_k4":3920137321/4000000000,"Kirchhoff_index":267/2,
      "diameter4_diamonds":1080},sort_keys=True))
if __name__=="__main__":main()
