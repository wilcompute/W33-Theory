#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, sys
from collections import Counter, deque
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_hermitian_s6_tetracode_c3.json"

from analysis.w33_20260924_history_bigcell_q43_compactification import (
    all_points, all_lagrangian_lines, wedge5, canon, gl2_projective_reps,
)
from analysis.w33_20260924_hermitian_3p1_spread_bridge import (
    projective4, projective5, hyperplane_points, qh, enumerate_spreads,
)
from analysis.w33_20260924_null_hesse_4a2_s4_intertwiner import direction_perm

P=3
J=np.block([
    [np.zeros((2,2),dtype=int),np.eye(2,dtype=int)],
    [-np.eye(2,dtype=int),np.zeros((2,2),dtype=int)],
])%3

def canon_matrix(M):
    a=tuple(map(int,(M%3).reshape(-1)))
    b=tuple(map(int,((-M)%3).reshape(-1)))
    return min(a,b)

def transvection(v):
    v=np.array(v,dtype=int).reshape(4,1)%3
    return (np.eye(4,dtype=int)+v@((J@v).T))%3

def mat_from_key(k):
    return np.array(k,dtype=int).reshape(4,4)%3
def inv_mod(A):
    A=np.array(A,dtype=int)%3
    n=A.shape[0]
    X=np.hstack([A,np.eye(n,dtype=int)])%3
    r=0
    for c in range(n):
        piv=next(i for i in range(r,n) if X[i,c])
        X[[r,piv]]=X[[piv,r]]
        X[r]=(X[r]*pow(int(X[r,c]),-1,3))%3
        for i in range(n):
            if i!=r and X[i,c]:
                X[i]=(X[i]-X[i,c]*X[r])%3
        r+=1
    assert np.array_equal(X[:,:n],np.eye(n,dtype=int)%3)
    return X[:,n:]%3

def psp_matrices():
    pts=all_points()
    gens=[transvection(v) for v in pts]
    ident=canon_matrix(np.eye(4,dtype=int))
    seen={ident}
    Q=deque([ident])
    while Q:
        k=Q.popleft()
        M=mat_from_key(k)
        for G in gens:
            z=canon_matrix((G@M)%3)
            if z not in seen:
                seen.add(z);Q.append(z)
    assert len(seen)==25920
    return [mat_from_key(k) for k in sorted(seen)]

def line_perm(M,lines,lidx):
    out=[]
    for L in lines:
        image=frozenset(
            canon(tuple(map(int,(M@np.array(v,dtype=int))%3)))
            for v in L
        )
        out.append(lidx[image])
    return tuple(out)
def order_perm(p):
    q=tuple(range(len(p)))
    for n in range(1,100):
        q=tuple(p[q[i]] for i in range(len(p)))
        if q==tuple(range(len(p))):
            return n
    raise AssertionError

def orbit_sizes(items,p):
    items=set(items);seen=set();sizes=[]
    for x in sorted(items):
        if x in seen: continue
        y=x;O=[]
        while y not in O:
            O.append(y);seen.add(y);y=p[y]
        assert set(O)<=items
        sizes.append(len(O))
    return sorted(sizes)

def exterior5(M):
    pairs=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    W6=np.zeros((6,6),dtype=int)
    for r,(i,j) in enumerate(pairs):
        for c,(a,b) in enumerate(pairs):
            W6[r,c]=(M[i,a]*M[j,b]-M[i,b]*M[j,a])%3
    # p6=[p01,p02,p03,p12,p13,p23]
    # x5=[p23,p03,p13,-p12,p01], with p02=-p13.
    P65=np.array([
      [0,0,0,0,1],
      [0,0,-1,0,0],
      [0,1,0,0,0],
      [0,0,0,-1,0],
      [0,0,1,0,0],
      [1,0,0,0,0],
    ],dtype=int)%3
    E56=np.array([
      [0,0,0,0,0,1],
      [0,0,1,0,0,0],
      [0,0,0,0,1,0],
      [0,0,0,-1,0,0],
      [1,0,0,0,0,0],
    ],dtype=int)%3
    return (E56@W6@P65)%3
def cycle_type_on_projective(points,T):
    idx={v:i for i,v in enumerate(points)}
    p=[]
    for v in points:
        y=canon(tuple(map(int,(T@np.array(v,dtype=int))%3)))
        p.append(idx[y])
    return tuple(p)

def duad_orbits(p6):
    duads=list(itertools.combinations(range(6),2))
    did={d:i for i,d in enumerate(duads)}
    p=tuple(did[tuple(sorted((p6[a],p6[b])))] for a,b in duads)
    return orbit_sizes(range(15),p)

def main():
    lines=all_lagrangian_lines()
    lidx={L:i for i,L in enumerate(lines)}
    coords={wedge5(L):L for L in lines}
    qpts=sorted(coords)
    H=(0,1,0,1,0)
    sec=hyperplane_points(H,qpts)
    herm_spread=set(lidx[coords[x]] for x in sec)
    assert len(herm_spread)==10

    # Tetracode C3 in the common P1(F3) action.
    G=next(A for A in gl2_projective_reps()
           if direction_perm(A)==(0,2,3,1))
    GiT=inv_mod(G).T%3
    C=np.block([[G,np.zeros((2,2),dtype=int)],
                [np.zeros((2,2),dtype=int),GiT]])%3
    cp=line_perm(C,lines,lidx)
    assert order_perm(cp)==3

    spreads=enumerate_spreads(lines,all_points())
    assert len(spreads)==36
    fixed=[set(S) for S in spreads if {cp[i] for i in S}==set(S)]
    assert len(fixed)==3
    assert all(orbit_sizes(S,cp)==[1,3,3,3] for S in fixed)

    # Build PSp(4,3) and conjugate C into the stabilizer of the Hermitian spread.
    group=psp_matrices()
    spread_stabilizer=[]
    transporter=None
    target=min(fixed,key=lambda S:tuple(sorted(S)))
    for M in group:
        p=line_perm(M,lines,lidx)
        image={p[i] for i in herm_spread}
        if image==herm_spread:
            spread_stabilizer.append(M)
        if transporter is None and image==target:
            transporter=M
    assert len(spread_stabilizer)==720
    assert transporter is not None

    Hm=transporter
    C_H=(inv_mod(Hm)@C@Hm)%3
    cperm=line_perm(C_H,lines,lidx)
    assert order_perm(cperm)==3
    assert {cperm[i] for i in herm_spread}==herm_spread
    assert orbit_sizes(herm_spread,cperm)==[1,3,3,3]

    # Restrict the induced exterior-square action to the Hermitian hyperplane.
    W5=exterior5(C_H)
    h=np.array(H,dtype=int).reshape(1,5)%3
    hw=(h@W5)%3
    assert any(hw[0])
    scalar=next(
        (int(hw[0,i])*pow(int(h[0,i]),-1,3))%3
        for i in range(5) if h[0,i]
    )
    assert np.array_equal(hw,(scalar*h)%3)

    P54=np.array([
      [1,0,0,0],
      [0,0,1,0],
      [0,0,0,1],
      [0,0,-1,0],
      [0,-1,0,0],
    ],dtype=int)%3
    Q45=np.array([
      [1,0,0,0,0],
      [0,0,0,0,-1],
      [0,1,0,0,0],
      [0,0,1,0,0],
    ],dtype=int)%3
    T4=(Q45@W5@P54)%3
    assert np.array_equal((P54@T4)%3,(W5@P54)%3)
    pts4=projective4()
    p4=cycle_type_on_projective(pts4,T4)
    assert order_perm(p4)==3
    classes={q:[i for i,v in enumerate(pts4) if qh(v)==q] for q in (0,1,2)}
    assert [len(classes[q]) for q in (0,1,2)]==[10,15,15]
    class_orbits={str(q):orbit_sizes(classes[q],p4) for q in (0,1,2)}

    # Exceptional-S6 fingerprint on the two inequivalent degree-15 shells.
    # A single 3-cycle and a double 3-cycle have different duad orbit structures.
    s6_single3=(1,2,0,3,4,5)
    s6_double3=(1,2,0,4,5,3)
    single3_duads=duad_orbits(s6_single3)
    double3_duads=duad_orbits(s6_double3)
    assert single3_duads==[1,1,1,3,3,3,3]
    assert double3_duads==[3,3,3,3,3]
    assert class_orbits["2"]==single3_duads
    assert class_orbits["1"]==double3_duads

    # Orthogonal action check on every projective vector.
    mults=set()
    for v in pts4:
        y=tuple(map(int,(T4@np.array(v,dtype=int))%3))
        if qh(v):
            mults.add((qh(y)*pow(qh(v),-1,3))%3)
        else:
            assert qh(y)==0
    assert len(mults)==1
    multiplier=next(iter(mults))
    assert multiplier==1

    out={
      "schema":"w33.20260924.hermitian_s6_tetracode_c3.v1",
      "status":"PASS_TETRACODE_C3_CONJUGATES_INTO_HERMITIAN_SPREAD_S6",
      "groups":{
        "PSp4_3_order":len(group),
        "Hermitian_spread_stabilizer_order":len(spread_stabilizer),
        "Hermitian_spread_stabilizer_identification":"S6 = PO^-(4,3)",
        "tetracode_C3_order":order_perm(cperm),
        "C3_fixed_spreads_before_conjugation":len(fixed),
      },
      "embedding":{
        "Bell_C3_PGL2_matrix":G.astype(int).tolist(),
        "transporter_PSp4_matrix":Hm.astype(int).tolist(),
        "conjugated_C3_matrix":C_H.astype(int).tolist(),
        "Hermitian_4D_matrix":T4.astype(int).tolist(),
        "orthogonal_multiplier":multiplier,
      },
      "orbit_decomposition":{
        "null_QH0_10":class_orbits["0"],
        "norm1_QH1_15":class_orbits["1"],
        "norm2_QH2_15":class_orbits["2"],
        "spread_null_lines":orbit_sizes(herm_spread,cperm),
      },
      "exceptional_S6_class_fingerprint":{
        "single_3cycle_on_6_duad_orbits":single3_duads,
        "double_3cycle_on_6_duad_orbits":double3_duads,
        "QH2_matches_single_3cycle_class":True,
        "QH1_matches_double_3cycle_class":True,
        "reading":(
          "the two 15-point anisotropic shells realize the two outer-related "
          "degree-15 S6 actions: the same C3 is seen as 3*1^3 on one shell and "
          "3^2 on the other"
        ),
      },
      "theorem":(
        "The tetracode-selected C3 from the common four-direction S4 does not "
        "stabilize the initial Hermitian spread in its Bell gauge, but it fixes "
        "exactly three of the 36 W33 spreads. A concrete PSp(4,3) transporter "
        "conjugates it into the order-720 stabilizer of the representative "
        "Hermitian spread. The induced four-dimensional action is an exact "
        "orthogonal isometry of Q_H=ac-x^2-y^2, so its orbit decomposition can "
        "be read simultaneously on the 10 null and two 15-point anisotropic "
        "projective shells. Those two degree-15 actions fingerprint the two "
        "order-three S6 classes exchanged by the exceptional outer automorphism."
      ),
      "boundary":(
        "The Q_H=1 and Q_H=2 shells are algebraically distinct finite anisotropic "
        "classes. Calling them timelike and spacelike requires an additional "
        "continuum/signature convention; the finite theorem itself does not make "
        "that physical assignment."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "stabilizer":out["groups"]["Hermitian_spread_stabilizer_order"],
      "orbits":out["orbit_decomposition"],
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
