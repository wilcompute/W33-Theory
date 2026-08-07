#!/usr/bin/env python3
"""Deterministic verifier for Passes 4169-4176."""
from __future__ import annotations
import collections, hashlib, itertools, json, math
from itertools import combinations, product
from pathlib import Path
import numpy as np
from scipy.optimize import brentq, root

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/PART_4169_4176_DISCRETE_C2_HAWKING_BACKREACTION_GRAY_LEVI_CASIMIR_AXION.json"
CERT=json.loads(OUT.read_text())

def semantic_hash(c):
    x=dict(c); x.pop("semantic_sha256",None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def c2_degree(N,m=-3.0):
    ks=np.linspace(-math.pi,math.pi,N,endpoint=False); h=2*math.pi/N
    g=np.meshgrid(ks,ks,ks,ks,indexing="ij")
    d=np.stack([np.sin(g[0]),np.sin(g[1]),np.sin(g[2]),np.sin(g[3]),
                m+np.cos(g[0])+np.cos(g[1])+np.cos(g[2])+np.cos(g[3])],axis=-1)
    n=d/np.linalg.norm(d,axis=-1,keepdims=True)
    ds=[(np.roll(n,-1,axis=a)-np.roll(n,1,axis=a))/(2*h) for a in range(4)]
    det=np.linalg.det(np.stack([n]+ds,axis=-1))
    return float(det.sum()*h**4/(8*math.pi**2/3))

def squeezer(n,i,j,r):
    S=np.eye(2*n,dtype=complex); c=math.cosh(r); s=math.sinh(r)
    for row in (i,j,n+i,n+j): S[row,:]=0
    S[i,i]=c; S[i,n+j]=s; S[j,j]=c; S[j,n+i]=s
    S[n+i,n+i]=c; S[n+i,j]=s; S[n+j,n+j]=c; S[n+j,i]=s
    return S

def beamsplitter(n,i,j,g):
    g=min(1.,max(0.,float(g))); S=np.eye(2*n,dtype=complex)
    t=math.sqrt(g); q=math.sqrt(1-g)
    for row in (i,j,n+i,n+j): S[row,:]=0
    S[i,i]=t;S[i,j]=q;S[j,i]=-q;S[j,j]=t
    S[n+i,n+i]=t;S[n+i,n+j]=q;S[n+j,n+i]=-q;S[n+j,n+j]=t
    return S

def chain(rv,gv):
    n=19; S=np.eye(2*n,dtype=complex)
    for j,(r,g) in enumerate(zip(rv,gv)):
        S=beamsplitter(n,0,10+j,g)@squeezer(n,0,1+j,r)@S
    return S

def covariance(S,nth=0.0):
    n=S.shape[0]//2; K=np.zeros((2*n,2*n),complex)
    for i in range(n):
        K[i,2*i]=K[n+i,2*i]=1/math.sqrt(2)
        K[i,2*i+1]=1j/math.sqrt(2); K[n+i,2*i+1]=-1j/math.sqrt(2)
    Sq=np.real_if_close(np.linalg.inv(K)@S@K,tol=1e5).real
    return (nth+.5)*Sq@Sq.T

def symplectic_eigs(V):
    m=V.shape[0]//2; om=np.kron(np.eye(m),np.array([[0.,1.],[-1.,0.]]))
    return np.sort(np.abs(np.linalg.eigvals(1j*om@V)))[::2]

def logneg(S,nth=0.0):
    V=covariance(S,nth); modes=[0]+list(range(1,10))
    idx=[q for m in modes for q in (2*m,2*m+1)]
    W=V[np.ix_(idx,idx)]; pt=np.eye(20); pt[1,1]=-1
    nu=symplectic_eigs(pt@W@pt)
    return max(0.,-float(np.sum(np.log(2*nu[nu<.5])))),float(nu[0])

def occup(S):
    n=S.shape[0]//2; V=S[:n,n:]; occ=np.sum(np.abs(V)**2,axis=1)
    return float(occ[0]),float(occ[1:10].sum()),float(occ[10:].sum())

def symp_growth(S): return float(np.log(np.linalg.svd(S,compute_uv=False)[0])/9)
def sigmoid(x): return 1/(1+np.exp(-x))
def logit(x): return np.log(x/(1-x))

RB=np.array([.00979708977002,.0203649786239,.0410938074485,.0738588749836,.0950655772517,.0738588749836,.0410938074485,.0203649786239,.00979708977002])
GB=np.array([.931739737612,.916053718604,.87648655463,.805844961224,.76,.805844961224,.87648655463,.916053718604,.931739737612])
KAPPAS=-math.pi*.3/np.log(np.tanh(RB))

def r_of_omega(w): return np.arctanh(np.exp(-math.pi*w/KAPPAS))
def mobility_edge(nth):
    def f(w): return logneg(chain(r_of_omega(w),GB),nth)[1]-.5
    return brentq(f,.01,2.)

def norm_proj(v):
    v=tuple(x%3 for x in v); first=next(x for x in v if x); inv=1 if first==1 else 2
    return tuple((inv*x)%3 for x in v)
def symp(x,y): return (x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2])%3
def build_levi():
    pts=sorted({norm_proj(v) for v in product(range(3),repeat=4) if any(v)})
    pi={p:i for i,p in enumerate(pts)}; lines=set()
    for i,j in combinations(range(40),2):
        x,y=pts[i],pts[j]
        if symp(x,y): continue
        line=frozenset(pi[norm_proj(tuple((a*x[k]+b*y[k])%3 for k in range(4)))]
                       for a,b in product(range(3),repeat=2) if a or b)
        lines.add(line)
    lines=sorted(lines,key=lambda z:tuple(sorted(z))); edges=[]
    for li,line in enumerate(lines):
        for p in line: edges.append((p,40+li))
    return pts,lines,edges
def adj_from_edges(n,edges):
    a=[set() for _ in range(n)]
    for u,v in edges: a[u].add(v);a[v].add(u)
    return a
def girth(adj):
    best=10**9
    for s in range(len(adj)):
        d=[-1]*len(adj); par=[-1]*len(adj); q=collections.deque([s]); d[s]=0
        while q:
            u=q.popleft()
            for v in adj[u]:
                if d[v]<0: d[v]=d[u]+1;par[v]=u;q.append(v)
                elif par[u]!=v: best=min(best,d[u]+d[v]+1)
    return best
def canon_cycle(c):
    rr=[]
    for s in (c,list(reversed(c))):
        for i in range(8): rr.append(tuple(s[i:]+s[:i]))
    return min(rr)
def cycles8(adj):
    C=set()
    for s in range(len(adj)):
        stack=[(s,[s])]
        while stack:
            u,p=stack.pop()
            if len(p)==8:
                if s in adj[u]: C.add(canon_cycle(p))
                continue
            for v in adj[u]:
                if v in p: continue
                stack.append((v,p+[v]))
    return C
def gf2_rank(masks):
    basis={}
    for x in masks:
        while x:
            p=x.bit_length()-1
            if p in basis:x^=basis[p]
            else:basis[p]=x;break
    return len(basis)
def two_lift(n,edges,bits):
    E=[]
    for (u,v),s in zip(edges,bits):
        E.append((2*u,2*v+s)); E.append((2*u+1,2*v+(1^s)))
    return 2*n,E
def det_bits(level,n):
    return [hashlib.sha256(f"W33LEVIlift:{level}:{i}".encode()).digest()[0]&1 for i in range(n)]

def verify():
    assert semantic_hash(CERT)==CERT["semantic_sha256"]
    p=CERT["pass4169_discrete_c2_compiler"]
    masses=[-3+4-2*N for N in range(5)]
    weights=[math.comb(4,N)*((-1)**N) for N in range(5)]
    assert masses==p["trim_masses"] and weights==p["trim_chiral_weights"]
    assert sum(w*(1 if m>0 else -1) for w,m in zip(weights,masses))//2==1
    for N in (9,29): assert abs(c2_degree(N)-p["quadrature"][str(N)])<2e-12
    p=CERT["pass4170_continuous_hawking_disorder"]; rng=np.random.default_rng(20260807)
    idx=np.arange(9); C=np.exp(-np.abs(idx[:,None]-idx[None,:])/2.0); chol=np.linalg.cholesky(C)
    logs=[];outs=[]
    for _ in range(512):
        x=chol@rng.standard_normal(9); rv=RB*np.exp(.35*x); gv=sigmoid(logit(GB)+.25*x); S=chain(rv,gv)
        l,_=logneg(S);o,_,_=occup(S);logs.append(l);outs.append(o);symp_growth(S)
    assert abs(min(logs)-p["gaussian_logneg_min"])<3e-11 and abs(max(outs)-p["gaussian_outside_max"])<3e-11
    alpha=(math.sqrt(5)-1)/2; qlogs=[]
    for phi in np.linspace(0,2*math.pi,721,endpoint=False):
        x=np.cos(2*math.pi*alpha*np.arange(9)+phi)
        qlogs.append(logneg(chain(RB*np.exp(.7*x),sigmoid(logit(GB)+.5*x)))[0])
    assert abs(min(qlogs)-p["qp_logneg_min"])<3e-11 and abs(max(qlogs)-p["qp_logneg_max"])<3e-11
    assert abs(mobility_edge(.01)-p["baseline_thermal_mobility_edges"]["0.01"])<2e-10
    p=CERT["pass4171_scale_geometry_backreaction"]; ln80=math.log(80)
    nb=lambda s:1/(math.exp(2*math.exp(-s))-1)
    nbp=lambda s:(2*math.exp(-s))*math.exp(2*math.exp(-s))/(math.exp(2*math.exp(-s))-1)**2
    F=lambda s,g:ln80-4*s+g*nb(s); Fp=lambda s,g:-4+g*nbp(s)
    r1=brentq(lambda s:F(s,1),1,2);r2=brentq(lambda s:F(s,1),2,3)
    assert abs(r1-p["g1_roots"][0])<1e-12 and Fp(r1,1)<0<Fp(r2,1)
    cr=root(lambda z:[F(z[0],z[1]),Fp(z[0],z[1])],[1.97,1.125]).x
    assert np.linalg.norm(cr-[p["critical_s"],p["critical_g"]])<2e-10
    p=CERT["pass4172_locality_reduced_gray_clock"]; codes=[t^(t>>1) for t in range(25)]
    assert all((codes[i]^codes[i+1]).bit_count()==1 for i in range(24))
    for x,y,z in product((0,1),repeat=3):
        pen=x*y-2*x*z-2*y*z+3*z
        assert (pen==0)==(z==x*y)
    H=np.zeros((25,25))
    for t in range(24): H[t,t+1]=H[t+1,t]=math.sqrt((t+1)*(24-t))
    ev=np.linalg.eigvalsh(H); assert np.max(np.abs(ev-np.arange(-24,25,2)))<1e-10
    assert p["exact_reduced_locality"]==4 and p["total_and_ancillas"]==72
    p=CERT["pass4173_levi_cover_critical_sequence"]; pts,lines,edges=build_levi(); adj=adj_from_edges(80,edges)
    assert len(pts)==len(lines)==40 and len(edges)==160 and {len(x) for x in adj}=={4} and girth(adj)==8
    C8=cycles8(adj); assert len(C8)==1620
    ei={tuple(sorted(e)):i for i,e in enumerate(edges)}; masks=[]
    for c in C8:
        m=0
        for i in range(8): m^=1<<ei[tuple(sorted((c[i],c[(i+1)%8])))]
        masks.append(m)
    assert gf2_rank(masks)==81 and gf2_rank([m|(1<<160) for m in masks])==82
    n=80;E=edges; seq=[]
    for level in range(4):
        seq.append([n,len(E),girth(adj_from_edges(n,E))])
        if level<3:n,E=two_lift(n,E,det_bits(level,len(E)))
    assert seq==p["deterministic_cover_sequence"]
    assert abs(math.atanh(1/3)-p["beta_c_J"])<1e-15
    p=CERT["pass4174_hawking_erasure_channel"]; et=[]
    for bits in itertools.product((-1.,1.),repeat=9):
        z=np.array(bits); rv=RB*(1+.5*z); gv=GB+.05*z
        out=occup(chain(rv,gv))[0]; lossless=occup(chain(rv,np.ones(9)))[0]; et.append(out/lossless)
    assert sum(x>.5 for x in et)==261 and sum(x<.5 for x in et)==251
    assert abs(max(et)-p["eta_max"])<2e-12
    p=CERT["pass4175_spectral_casimir"]; A=np.zeros((80,80))
    for u in range(80):
        for v in adj[u]: A[u,v]=1
    G=np.linalg.inv(5*np.eye(80)-A)
    assert abs(G[0,0]-211/855)<2e-14
    d=[-1]*80;d[0]=0;q=collections.deque([0])
    while q:
        u=q.popleft()
        for v in adj[u]:
            if d[v]<0:d[v]=d[u]+1;q.append(v)
    expected={1:10/171,2:13/855,3:1/171,4:4/855}
    for dist,g in expected.items():
        for v in range(80):
            if d[v]==dist: assert abs(G[0,v]-g)<2e-14
    p=CERT["pass4176_axion_dimensional_reduction"]
    assert p["parent_second_chern"]==1 and p["chern_simons_level_shift"]==1 and p["theta_winding"]=="2pi"
    return True

def main():
    verify()
    frozen=json.loads(OUT.read_text()); assert frozen==CERT
    print("PASS_4169_4176",CERT["semantic_sha256"])
    return 0

if __name__=="__main__": raise SystemExit(main())
