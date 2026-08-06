#!/usr/bin/env python3
"""Deterministic verifier for Passes 4057-4064."""
from __future__ import annotations
import hashlib,itertools,json,math
from collections import defaultdict,deque
from pathlib import Path
import networkx as nx
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data/PART_4057_4064_ADVANCED_PHYSICS.json'

def norm(v):
    v=tuple(x%3 for x in v)
    for a in v:
        if a:return tuple((1 if a==1 else 2)*x%3 for x in v)
    raise ValueError

def form(u,v):return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%3

def geometry():
    pts=sorted({norm(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    W=nx.Graph();W.add_nodes_from(range(40))
    for i,u in enumerate(pts):
        for j in range(i+1,40):
            if form(u,pts[j])==0:W.add_edge(i,j)
    lines=sorted(tuple(sorted(c)) for c in nx.find_cliques(W) if len(c)==4)
    L=nx.Graph();L.add_nodes_from(range(80))
    for j,line in enumerate(lines):
        for p in line:L.add_edge(p,40+j)
    edges=sorted(tuple(sorted(e)) for e in L.edges())
    D=np.zeros((80,160))
    for k,(a,b) in enumerate(edges):D[a,k]=-1;D[b,k]=1
    X=nx.line_graph(L);A=nx.to_numpy_array(X,nodelist=edges);I=np.eye(160)
    P=((A-6*I)@(A-2*I)@(A@A-4*A-2*I))/320
    assert (len(pts),len(lines),len(edges),np.linalg.matrix_rank(D),round(np.trace(P)))==(40,40,160,79,81)
    return pts,lines,L,edges,D,P

def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))
def invperm(p):
    q=[0]*len(p)
    for i,j in enumerate(p):q[j]=i
    return tuple(q)

def dark_irreps(pts,lines,edges):
    idx={p:i for i,p in enumerate(pts)};ID=tuple(range(40))
    def tr(v):
        out=[]
        for x in pts:
            a=form(x,v);out.append(idx[norm(tuple((x[i]+a*v[i])%3 for i in range(4)))])
        return tuple(out)
    T=[tr(v) for v in pts];gens=[T[i] for i in (24,26,2,16)]
    G={ID};q=deque([ID])
    while q:
        g=q.popleft()
        for s in gens:
            h=compose(s,g)
            if h not in G:G.add(h);q.append(h)
    assert len(G)==25920
    gp=gens+[invperm(s) for s in gens];unseen=set(G);classes=[]
    while unseen:
        r=next(iter(unseen));C={r};q=deque([r])
        while q:
            g=q.popleft()
            for s in gp:
                h=compose(compose(s,g),invperm(s))
                if h not in C:C.add(h);q.append(h)
        classes.append(list(C));unseen-=C
    def order(g):
        h=ID
        for n in range(1,50):
            h=compose(g,h)
            if h==ID:return n
        raise AssertionError
    classes=sorted(classes,key=lambda C:(0 if ID in C else 1,order(C[0]),len(C)))
    cof={g:i for i,C in enumerate(classes) for g in C};li={l:i for i,l in enumerate(lines)}
    def counts(g):
        lp=tuple(li[tuple(sorted(g[p] for p in l))] for l in lines)
        fv=sum(g[i]==i for i in range(40))+sum(lp[i]==i for i in range(40))
        fe=sum(g[p]==p and lp[l-40]==l-40 for p,l in edges)
        return fv,fe
    dark=[]
    for C in classes:
        g=C[0];fv,fe=counts(g);h=fe-fv+1;fv2,fe2=counts(compose(g,g));h2=fe2-fv2+1
        dark.append((h*h+h2)//2-fe)
    K=len(classes);N=np.zeros((K,K,K),int);inv={g:invperm(g) for g in G};reps=[C[0] for C in classes]
    for i,C in enumerate(classes):
        for k,r in enumerate(reps):
            cnt=np.zeros(K,int)
            for a in C:cnt[cof[compose(inv[a],r)]]+=1
            N[i,:,k]=cnt
    M=[N[i].T.astype(float) for i in range(K)];rng=np.random.default_rng(20260806);a=rng.normal(size=K)
    _,V=np.linalg.eig(sum(a[i]*M[i] for i in range(K)));Vi=np.linalg.inv(V);sizes=np.array([len(C) for C in classes],float)
    omega=np.array([np.diag(Vi@m@V) for m in M]).T;rat=omega/sizes[None,:]
    bydeg=defaultdict(list)
    for r in rat:
        d=round(math.sqrt(25920/np.sum(sizes*np.abs(r)**2)));ch=r*d
        mult=round(float(np.real(np.sum(sizes*np.array(dark)*np.conj(ch))/25920)))
        bydeg[d].append(mult)
    return {str(d):sorted(v) for d,v in sorted(bydeg.items())},len(classes)

def semantic_sha(cert):
    raw={k:v for k,v in cert.items() if k!='semantic_sha256'}
    return hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def verify():
    cert=json.loads(CERT.read_text());pts,lines,L,edges,D,P=geometry()
    assert cert['all_checks_hold'] and semantic_sha(cert)==cert['semantic_sha256']
    LX=2*sp.acos(sp.Rational(1,4))+sp.pi*sp.sqrt(15)/2;LZ=sp.pi/3+sp.pi*sp.sqrt(3)/2
    assert abs(float(LX)-cert['pass4057_counterdiabatic_holonomy']['X_numeric'])<1e-12
    assert abs(float(LZ)-cert['pass4057_counterdiabatic_holonomy']['Z_numeric'])<1e-12
    dec,nclass=dark_irreps(pts,lines,edges)
    assert nclass==20 and dec==cert['pass4058_dark_pair_irreducibles']['irreducible_multiplicities_grouped_by_degree']
    assert sum(int(d)*sum(v) for d,v in dec.items())==3161 and np.linalg.matrix_rank(P*P)==160
    x=sp.symbols('x');lam=[4-sp.sqrt(6),4,4+sp.sqrt(6),8];poly=sp.interpolate([(z,1/sp.sqrt(z)) for z in lam],x)
    assert max(abs(float(sp.N(poly.subs(x,z)-1/sp.sqrt(z)))) for z in lam)<1e-12
    coeff=[float(sp.N(sp.expand(poly).coeff(x,i))) for i in range(4)];L0=D@D.T
    Q=D.T@sum(coeff[i]*np.linalg.matrix_power(L0,i) for i in range(4))
    assert np.linalg.norm(Q.T@Q-(np.eye(80)-np.ones((80,80))/80),2)<1e-10
    assert np.linalg.norm(Q@Q.T-(np.eye(160)-P),2)<1e-10
    I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1])
    gam=[np.kron(X,X),np.kron(X,Y),np.kron(X,Z),np.kron(Y,I)];g5=np.kron(Z,I)
    for i in range(4):
        for j in range(4):assert np.linalg.norm(gam[i]@gam[j]+gam[j]@gam[i]-(2*np.eye(4) if i==j else 0))<1e-12
        assert np.linalg.norm(gam[i]@g5+g5@gam[i])<1e-12
    assert sum(2*sum(b)==0 for b in itertools.product([0,1],repeat=4))==1
    phi=math.acos(1/80);z=complex(math.cos(phi),math.sin(phi));bound=2/abs(1-z)
    assert max(abs((1-z**N)/(1-z)) for N in range(1,10000))<=bound+1e-12
    for d in range(1,5):
        theta=2*math.acos(3**(-d));assert 0<theta<math.pi
    assert 3161+81+24+30+24+1==3321 and nx.edge_connectivity(L)==4
    return {'all_checks_hold':True,'semantic_sha256':cert['semantic_sha256'],'dark_irreps':dec}

if __name__=='__main__':print(json.dumps(verify(),indent=2,sort_keys=True))
