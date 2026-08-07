#!/usr/bin/env python3
"""Deterministic verifier for Passes 4185-4192."""
from __future__ import annotations
import collections, hashlib, itertools, json, math
from itertools import combinations, product
from pathlib import Path
import numpy as np
from scipy.optimize import brentq, minimize_scalar

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_4185_4192_ADAPTIVE_C2_HAWKING_HYSTERESIS_3LOCAL_COVER_HOLONOMY_IHARA_HEAT.json'
CERT=json.loads(OUT.read_text())

def semantic_hash(c):
    x=dict(c); x.pop('semantic_sha256',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def c2_midpoint(n,m=-3.0):
    xs=-math.pi+(np.arange(n)+.5)*(2*math.pi/n)
    g=np.meshgrid(xs,xs,xs,xs,indexing='ij'); K=np.stack(g,axis=-1)
    s=np.sin(K); c=np.cos(K)
    d=np.concatenate([s,(m+c.sum(axis=-1,keepdims=True))],axis=-1)
    norm=np.linalg.norm(d,axis=-1,keepdims=True); nh=d/norm
    D=np.zeros(K.shape[:-1]+(5,4))
    for j in range(4): D[...,j,j]=c[...,j]; D[...,4,j]=-s[...,j]
    P=np.eye(5)-nh[..., :,None]*nh[...,None,:]
    dn=np.einsum('...ab,...bj->...aj',P,D)/norm[...,None]
    det=np.linalg.det(np.concatenate([nh[..., :,None],dn],axis=-1))
    return float((3/(8*math.pi**2))*det.sum()*(2*math.pi/n)**4)

def r_of_omega(w,kappa=.4): return math.atanh(math.exp(-math.pi*w/kappa))

def nb(s): return 1/(math.exp(2*math.exp(-s))-1)
def flow(s,g,h=.004):
    n=nb(s); return math.log(80)-4*s+g*n-h*n*n

def deriv(f,x):
    e=1e-6; return (f(x+e)-f(x-e))/(2*e)

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
    lines=sorted(lines,key=lambda z:tuple(sorted(z)))
    edges=[(p,40+li) for li,line in enumerate(lines) for p in sorted(line)]
    adj=[[] for _ in range(80)]
    for u,v in edges: adj[u].append(v); adj[v].append(u)
    for a in adj: a.sort()
    return pts,lines,edges,adj

def simple_cycles_L(adj,L):
    cycles=[]
    for s in range(len(adj)):
        for first in adj[s]:
            if first<=s: continue
            stack=[(first,[s,first],{s,first})]
            while stack:
                u,path,seen=stack.pop()
                if len(path)==L:
                    if s in adj[u] and path[1]<path[-1]: cycles.append(tuple(path))
                    continue
                for v in adj[u]:
                    if v==s or v<=s or v in seen: continue
                    stack.append((v,path+[v],seen|{v}))
    return cycles

def cover_voltages():
    p=65537; vals=[]
    for i in range(160):
        h=hashlib.sha256(f'W33:COVER:1:{i}'.encode()).digest()
        vals.append(int.from_bytes(h[:8],'big')%p)
    return p,vals

def cycle_voltage(c,vals,edge_index,p):
    z=0
    for i in range(len(c)):
        u,v=c[i],c[(i+1)%len(c)]; e=edge_index[tuple(sorted((u,v)))]
        z=(z+(1 if u<40 else -1)*vals[e])%p
    return z

def verify():
    assert semantic_hash(CERT)==CERT['semantic_sha256']
    p=CERT['pass4185_adaptive_c2']
    for n in (7,9,13): assert abs(c2_midpoint(n)-p['midpoint_quadrature'][str(n)])<3e-12
    assert round(p['midpoint_quadrature']['7'])==1 and abs(p['midpoint_quadrature']['9']-1)<.05

    p=CERT['pass4186_hawking_critical_surface']
    for sw,row in p['omega_table'].items():
        r=r_of_omega(float(sw)); assert abs(r-row['r'])<1e-14
        assert abs((math.exp(2*r)-1)/2-row['n_ent'])<1e-14
        assert abs(math.sinh(r)**2-row['n_B_to_A'])<1e-14
    r=r_of_omega(.3); q=math.sinh(r)**2
    assert abs(.4*q-p['omega0p3_A_to_B_thresholds']['eta0p7'])<1e-15

    p=CERT['pass4187_hysteretic_backreaction']
    roots=[]
    xs=np.linspace(.2,5.5,10000); vals=[flow(x,.5) for x in xs]
    for a,b,fa,fb in zip(xs[:-1],xs[1:],vals[:-1],vals[1:]):
        if fa*fb<0: roots.append(brentq(lambda s:flow(s,.5),a,b))
    roots2=[]
    for r in roots:
        if not roots2 or abs(r-roots2[-1])>1e-5: roots2.append(r)
    assert len(roots2)==3
    for r,row in zip(roots2,p['g0p5_roots']):
        assert abs(r-row['s'])<2e-10 and (deriv(lambda s:flow(s,.5),r)<0)==row['stable']
    h=.004
    def gcurve(s):
        n=nb(s); return (4*s-math.log(80)+h*n*n)/n
    ext=[]; dg=[deriv(gcurve,x) for x in xs]
    for a,b,fa,fb in zip(xs[:-1],xs[1:],dg[:-1],dg[1:]):
        if fa*fb<0: ext.append(brentq(lambda s:deriv(gcurve,s),a,b))
    assert abs(gcurve(ext[0])-p['hysteresis_g_window'][1])<2e-9
    assert abs(gcurve(ext[1])-p['hysteresis_g_window'][0])<2e-9

    p=CERT['pass4188_exact_3local_clock']
    H=np.zeros((49,49))
    for j in range(48): H[j,j+1]=H[j+1,j]=math.sqrt((j+1)*(48-j))
    ev=np.linalg.eigvalsh(H)
    assert np.max(np.abs(ev-np.arange(-48,49,2)))<2e-10
    assert p['max_locality']==3 and p['total_auxiliary_ancillas']==96
    for x,y,z in product((0,1),repeat=3):
        pen=x*y-2*x*z-2*y*z+3*z
        assert (pen==0)==(z==x*y)

    p=CERT['pass4189_high_girth_levi_cover']; pts,lines,edges,adj=build_levi()
    assert len(pts)==40 and len(lines)==40 and len(edges)==160 and {len(a) for a in adj}=={4}
    C={L:simple_cycles_L(adj,L) for L in (8,10,12)}
    assert {str(L):len(C[L]) for L in C}==p['base']['cycle_counts']
    prime,volts=cover_voltages(); assert prime==65537
    assert hashlib.sha256(json.dumps(volts,separators=(',',':')).encode()).hexdigest()==p['voltage_vector_sha256']
    ei={tuple(sorted(e)):i for i,e in enumerate(edges)}
    for L in C: assert sum(cycle_voltage(c,volts,ei,prime)==0 for c in C[L])==0
    assert len(edges)-80+1==81

    p=CERT['pass4190_holonomic_universality']; rt=math.sqrt(3)
    Uy=np.array([[-.5,-rt/2],[rt/2,-.5]],complex); w=np.exp(2j*math.pi/3)
    Uz=np.diag([w.conjugate(),w]); Cc=Uy@Uz@Uy.conj().T@Uz.conj().T
    assert np.linalg.norm(np.linalg.matrix_power(Uy,3)-np.eye(2))<1e-14
    assert np.linalg.norm(np.linalg.matrix_power(Uz,3)-np.eye(2))<1e-14
    assert abs(np.trace(Cc).real+.25)<2e-14 and abs(math.cos(p['commutator_eigenphase'])+.125)<2e-14

    p=CERT['pass4191_ihara_factorization']; A=np.zeros((80,80))
    for u in range(80):
        for v in adj[u]: A[u,v]=1
    ae=np.linalg.eigvalsh(A)
    target=np.array([-4]+[-math.sqrt(6)]*24+[0]*30+[math.sqrt(6)]*24+[4])
    assert np.max(np.abs(ae-target))<2e-12
    assert max(abs(x) for x in ae[1:-1])<=2*math.sqrt(3)+1e-12

    p=CERT['pass4192_heat_dimension']; lam=np.array([0,8,4-math.sqrt(6),4+math.sqrt(6),4.]); mul=np.array([1,1,24,24,30.])
    def ds(t):
        e=np.exp(-lam*t); return 2*t*np.sum(mul*lam*e)/np.sum(mul*e)
    opt=minimize_scalar(lambda t:-ds(t),bounds=(1e-6,10),method='bounded',options={'xatol':1e-13})
    assert abs(opt.x-p['maximum_time'])<2e-6 and abs(-opt.fun-p['maximum_spectral_dimension'])<2e-10
    assert -opt.fun<4
    return True

def main():
    verify(); print('PASS_4185_4192',CERT['semantic_sha256']); return 0
if __name__=='__main__': raise SystemExit(main())
