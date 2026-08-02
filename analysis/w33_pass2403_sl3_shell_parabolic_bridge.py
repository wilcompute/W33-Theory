#!/usr/bin/env python3
from __future__ import annotations
import argparse,collections,hashlib,itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];CERT=ROOT/'data/w33_pass2403_sl3_shell_parabolic_bridge.json'
R=((0,-1,0),(1,0,0),(0,0,1));U=((1,0,0),(0,0,1),(0,-1,1))
def digest(d):
    x=dict(d);x.pop('sha256_without_hash_field',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def mm(A,B,p):return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(3))%p for j in range(3)) for i in range(3))
def ident(p):return ((1,0,0),(0,1,0),(0,0,1))
def group(p):
    gens=[tuple(tuple(x%p for x in row) for row in M) for M in (R,U)];G={ident(p)};q=collections.deque([ident(p)])
    while q:
        A=q.popleft()
        for g in gens:
            B=mm(A,g,p)
            if B not in G:G.add(B);q.append(B)
    return G,gens
def norm(v,p):
    for x in v:
        if x%p:
            z=pow(x%p,-1,p);return tuple(z*y%p for y in v)
    raise ValueError
def points(p):return sorted({norm(v,p) for v in itertools.product(range(p),repeat=3) if any(v)})
def act(A,v,p):return norm(tuple(sum(A[i][j]*v[j] for j in range(3))%p for i in range(3)),p)
def order(A,p):
    X=ident(p)
    for n in range(1,100):
        X=mm(X,A,p)
        if X==ident(p):return n
    raise AssertionError
def cyc_orbits(A,P,p):
    unseen=set(P);out=[]
    while unseen:
        x=min(unseen);o=[];y=x
        while y not in o:o.append(y);y=act(A,y,p)
        unseen-=set(o);out.append(len(o))
    return sorted(out)
def audit(p):
    G,gens=group(p);P=points(p);e=P[0];par=[g for g in G if act(g,e,p)==e]
    return {'order':len(G),'points':len(P),'parabolic':len(par),'R_order':order(gens[0],p),'U_order':order(gens[1],p),'R_orbits':cyc_orbits(gens[0],P,p),'U_orbits':cyc_orbits(gens[1],P,p)}
def verify(d):
    assert d['sha256_without_hash_field']==digest(d)
    assert d['mod2']['order']==168 and d['mod2']['point_parabolic_order']==24
    assert d['mod3']['order']==5616 and d['mod3']['point_parabolic_order']==432
    return d
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true');ap.add_argument('--verify-frozen',action='store_true');a=ap.parse_args();d=verify(json.loads(CERT.read_text()))
    if a.full:
        a2,a3=audit(2),audit(3)
        assert a2=={'order':168,'points':7,'parabolic':24,'R_order':2,'U_order':3,'R_orbits':[1,1,1,2,2],'U_orbits':[1,3,3]}
        assert a3=={'order':5616,'points':13,'parabolic':432,'R_order':4,'U_order':6,'R_orbits':[1,2,2,4,4],'U_orbits':[1,1,2,3,6]}
    print(json.dumps({'status':d['status'],'sha256':d['sha256_without_hash_field']},indent=2))
if __name__=='__main__':main()
