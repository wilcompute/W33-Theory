#!/usr/bin/env python3
from collections import deque
from pathlib import Path
import hashlib,json
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/PART_W33_PASS11614_HESSE_COXETER_DISCRIMINANT.json"
RES="1be1b367f"

def ph(p):
    p=Path(p)
    raw=(json.dumps(json.loads(p.read_text()),sort_keys=True,separators=(",",":")).encode()
         if p.suffix==".json" else p.read_bytes().replace(b"\r\n",b"\n"))
    return hashlib.sha256(raw).hexdigest()

def k(M): return tuple(int(a) for a in list(M))
def refl(a):
    v=s.Matrix(a); assert (v.T*v)[0]==2
    return s.eye(3)-v*v.T
def gen(gs):
    I=s.eye(3); d={k(I):I}; q=deque([I])
    while q:
        A=q.popleft()
        for g in gs:
            B=A*g
            if k(B) not in d: d[k(B)]=B; q.append(B)
    return list(d.values())

def result():
    x,y,z=s.symbols("x y z", real=True); v=s.Matrix([x,y,z])
    W=s.expand((x*x-y*y)*(y*y-z*z)*(z*z-x*x))
    roots=[s.Matrix(a) for a in [(1,-1,0),(1,1,0),(1,0,-1),(1,0,1),(0,1,-1),(0,1,1)]]
    delta=s.prod((r.T*v)[0] for r in roots); assert s.expand(W+delta)==0
    simples=[(1,-1,0),(0,1,-1),(0,1,1)]; gs=[refl(a) for a in simples]; G=gen(gs)
    assert len(G)==24 and sum(g.det()==1 for g in G)==12
    for g in G:
        q=g*v
        assert s.expand(W.subs({x:q[0],y:q[1],z:q[2]},simultaneous=True)-g.det()*W)==0
    b=s.Matrix([1,2,3]); sigs=set(); signs=[]; orbit=set()
    for g in G:
        q=g*b; orbit.add(tuple(int(a) for a in q))
        sig=tuple(int(s.sign((r.T*q)[0])) for r in roots); assert 0 not in sig; sigs.add(sig)
        w=int(W.subs({x:q[0],y:q[1],z:q[2]})); signs.append(1 if w>0 else -1)
        assert signs[-1]==int(g.det())
    assert len(orbit)==len(sigs)==24 and signs.count(1)==signs.count(-1)==12
    W0=s.factor(W.subs({x:1/s.sqrt(14),y:2/s.sqrt(14),z:3/s.sqrt(14)})); assert W0==s.Rational(15,343)
    idx={k(g):i for i,g in enumerate(G)}; edges=set(); deg=[0]*24
    for i,g in enumerate(G):
        for R in gs:
            j=idx[k(g*R)]; edges.add(tuple(sorted((i,j))))
    assert len(edges)==36
    for a,b2 in edges:
        deg[a]+=1;deg[b2]+=1;assert G[a].det()==-G[b2].det()
    assert set(deg)=={3}
    po=[len(gen([gs[0],gs[1]])),len(gen([gs[0],gs[2]])),len(gen([gs[1],gs[2]]))]
    assert sorted(po)==[4,6,6]
    sq=sum(24//o for o in po if o==4); hx=sum(24//o for o in po if o==6)
    assert (sq,hx,24-36+sq+hx)==(6,8,2)
    p2=x*x+y*y+z*z;p3=x*y*z;p4=x**4+y**4+z**4;e2=(p2**2-p4)/2;e3=p3**2
    disc=s.expand(p2**2*e2**2-4*e2**3-4*p2**3*e3-27*e3**2+18*p2*e2*e3)
    compact=s.expand(s.Rational(1,4)*(p2**2-p4)**2*(2*p4-p2**2)+p2*(5*p2**2-9*p4)*p3**2-27*p3**4)
    assert s.expand(W**2-disc)==0 and s.expand(W**2-compact)==0
    return {
      "status":"PASS_HESSE_CP_ORDER_PARAMETER_IS_D3_COXETER_DISCRIMINANT",
      "coxeter":{"group":"W(D3)~=W(A3)~=S4","order":24,"positive_root_count":6,
        "W_factorization":"W=-(x-y)(x+y)(x-z)(x+z)(y-z)(y+z)",
        "reflection_arrangement":"W=0 iff x=+/-y or x=+/-z or y=+/-z","anti_invariant":"W(gx)=det(g)W(x)"},
      "vacuum_chambers":{"base_ray":"(1,2,3)/sqrt(14)","normalized_W":"15/343","orbit_size":24,
        "distinct_root_signatures":24,"W_sign_multiplicities":{"+":12,"-":12},
        "theorem":"The generic Hesse orbit has one point in every D3 chamber; sign(W) is its orientation class."},
      "wall_graph":{"vertices":24,"edges":36,"degree":3,"bipartition":[12,12],"rank2_parabolic_orders":po,
        "square_faces":sq,"hexagonal_faces":hx,"faces_total":sq+hx,"euler":2,
        "identification":"simple-reflection Cayley graph of S4: order-4 permutohedron, combinatorially truncated octahedron"},
      "discriminant":{"roots":"x^2,y^2,z^2",
        "cubic":"t^3-p2 t^2+((p2^2-p4)/2)t-p3^2",
        "identity":"W^2=(1/4)(p2^2-p4)^2(2p4-p2^2)+p2(5p2^2-9p4)p3^2-27p3^4"},
      "physics_weld":{"selector":"Passes11607/11609 leave Chi=-sign(W) and E8 shell C=-sign(W).",
        "wall":"Every simple reflection crosses W=0 and flips both selected signs.",
        "native_mass":"Pass11610/11557 supply native Gamma_* for an anticommuting Gamma_* W Chi wall, conditional on that physical coupling."},
      "boundary":"Exact chamber/order-parameter theorem only; no spacetime texture, tension, anomaly inflow or cosmological chamber selection is derived."}

def main():
    r=result(); o={"pass_number":11614,"reservation":RES,"status":r["status"],"result":r}
    src=["analysis/w33_pass11557_pin_equivariant_event_dirac.py","analysis/w33_pass11600_dynamical_hesse_flavor.py",
         "data/w33_pass11600_dynamical_hesse_flavor.json","analysis/PASS11608_11613_CHIRAL_UNIFICATION.md",
         "data/PART_W33_PASS11608_11613_CHIRAL_UNIFICATION.json"]
    o["source_sha256"]={p:ph(ROOT/p) for p in src};o["producer_sha256"]=ph(Path(__file__))
    OUT.write_text(json.dumps(o,indent=2,sort_keys=True)+"\n");print(json.dumps(o,indent=2,sort_keys=True))
if __name__=="__main__":main()
