#!/usr/bin/env python3
"""Deterministic verifier for Passes 4089--4096."""
from __future__ import annotations
import hashlib, itertools, json, math
from fractions import Fraction
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data/PART_4089_4096_IMPLEMENTATION_OUTSIDE_BOX.json'
LAYOUT=ROOT/'data/w33_pass4089_four_router_layout.json'
P=3

def canon(v):
    v=[x%P for x in v]
    for x in v:
        if x:
            inv=pow(x,-1,P); return tuple(inv*y%P for y in v)
    raise ValueError

def symp(u,v): return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%P

def geometry():
    pts=sorted({canon(v) for v in itertools.product(range(P),repeat=4) if any(v)})
    idx={v:i for i,v in enumerate(pts)}; lines=set()
    for i,u in enumerate(pts):
        for j in range(i+1,len(pts)):
            v=pts[j]
            if symp(u,v): continue
            s={idx[canon(tuple((a*u[k]+b*v[k])%P for k in range(4)))]
               for a,b in itertools.product(range(P),repeat=2) if a or b}
            if len(s)==4: lines.add(tuple(sorted(s)))
    return pts,sorted(lines)

def semantic_sha(x):
    y=dict(x); y.pop('semantic_sha256',None)
    return hashlib.sha256(json.dumps(y,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def verify_layout():
    x=json.loads(LAYOUT.read_text()); pts,lines=geometry()
    assert [tuple(q['vector']) for q in x['points']]==pts
    assert [tuple(q['point_ids']) for q in x['lines']]==lines
    assert semantic_sha(x)==x['semantic_sha256']
    incidence={(p,l) for l,line in enumerate(lines) for p in line}
    seen=set(); mats=[]
    for router in x['routers']:
        pairs=[tuple(z) for z in router['pairs']]
        assert len(pairs)==40 and len({p for p,_ in pairs})==40 and len({l for _,l in pairs})==40
        assert all(z in incidence for z in pairs); seen.update(pairs)
        M=np.zeros((80,80))
        for p,l in pairs: M[p,40+l]=M[40+l,p]=1
        assert np.array_equal(M@M,np.eye(80)); mats.append(M)
    assert seen==incidence and len(seen)==160
    A=sum(mats); vals=np.linalg.eigvalsh(A/4)
    target=np.array([-1]+[-math.sqrt(6)/4]*24+[0]*30+[math.sqrt(6)/4]*24+[1])
    assert np.max(np.abs(vals-target))<1e-12

def verify_reference():
    phi=math.atan2(3,-4)
    for K in (32,64,128,256):
        a=math.pi/(K+2); c=np.sqrt(2/(K+2))*np.sin((np.arange(K+1)+1)*a)
        overlap=float(c[:-1]@c[1:]); wrap=float(c[0]*c[-1])
        assert abs(overlap-math.cos(a))<1e-14
        z=np.exp(1j*phi)*overlap+np.exp(-1j*K*phi)*wrap
        bound=1-math.cos(a)+2*math.sin(a)**2/(K+2)
        assert abs(z-np.exp(1j*phi))<=bound+1e-14

def verify_anomalies():
    assert 2*Fraction(1,2)*Fraction(1,6)+Fraction(1,2)*Fraction(-2,3)+Fraction(1,2)*Fraction(1,3)==0
    assert 3*Fraction(1,2)*Fraction(1,6)+Fraction(1,2)*Fraction(-1,2)==0
    assert 6*Fraction(1,6)+3*Fraction(-2,3)+3*Fraction(1,3)+2*Fraction(-1,2)+1==0
    assert 6*Fraction(1,6)**3+3*Fraction(-2,3)**3+3*Fraction(1,3)**3+2*Fraction(-1,2)**3+1==0
    assert 6*1+3*15+2*24==99

def matrices():
    _,lines=geometry(); edges=sorted((p,l) for l,line in enumerate(lines) for p in line)
    D=np.zeros((80,160))
    for e,(p,l) in enumerate(edges): D[p,e]=1; D[40+l,e]=-1
    return D,D.T@D-2*np.eye(160)

def verify_spectra_and_notch():
    D,A=matrices(); vals=np.linalg.eigvalsh(A)
    target=np.array([-2]*81+[-math.sqrt(6)+2]*24+[2]*30+[math.sqrt(6)+2]*24+[6])
    assert np.max(np.abs(vals-target))<1e-11
    gaps=np.array([4-math.sqrt(6),4,4+math.sqrt(6),8])
    poly=np.poly(-gaps*gaps)
    assert np.max(np.abs(poly-np.array([1,124,4644,53056,102400])))<1e-9
    c=json.loads(CERT.read_text())['pass4092_materialized_notch']
    es=np.array(c['etas']); sq=np.array(c['square_leakage']); nt=np.array(c['notched_leakage'])
    assert 1.95<np.polyfit(np.log(es),np.log(sq),1)[0]<2.1
    assert 3.95<np.polyfit(np.log(es),np.log(nt),1)[0]<4.1
    assert np.linalg.matrix_rank(D)==79 and round(np.trace(np.eye(160)-D.T@np.linalg.pinv(D@D.T)@D))==81

def verify_turing_and_resistance():
    for J,roots,unstable in [
        (np.array([[2.,5.],[-21.,-20.]]),(5,13),10),
        (np.array([[3.2,12.],[-21.,-10.]]),(11,20),16)]:
        for lam in (0,10,16):
            det=np.linalg.det(J-lam*np.diag([.1,10.]))
            assert abs(det-(lam-roots[0])*(lam-roots[1]))<1e-9
        assert max(np.linalg.eigvals(J-unstable*np.diag([.1,10.])).real)>0
    # SRG identity and pseudoinverse formula.
    pts,_=geometry(); A=np.zeros((40,40))
    for i,u in enumerate(pts):
        for j,v in enumerate(pts):
            if i!=j and symp(u,v)==0: A[i,j]=1
    J=np.ones((40,40)); L=12*np.eye(40)-A
    Lp=Fraction(7,80)*np.eye(40)+Fraction(1,160)*A-Fraction(13,3200)*J
    assert np.linalg.norm(L@Lp-(np.eye(40)-J/40))<1e-11
    r_adj=2*(Lp[0,0]-Lp[np.where(A[0]==1)[0][0],0])
    r_non=2*(Lp[0,0]-Lp[np.where((A[0]==0)&(np.arange(40)!=0))[0][0],0])
    assert abs(r_adj-13/80)<1e-12 and abs(r_non-7/40)<1e-12

def main():
    c=json.loads(CERT.read_text()); assert semantic_sha(c)==c['semantic_sha256']
    verify_layout(); verify_reference(); verify_anomalies(); verify_spectra_and_notch(); verify_turing_and_resistance()
    print('PASS_4089_4096',c['semantic_sha256'])

if __name__=='__main__': main()
