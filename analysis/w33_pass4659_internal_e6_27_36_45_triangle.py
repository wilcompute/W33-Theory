#!/usr/bin/env python3
"""Pass 4659 — reconstruct the full 27–36–45 E6 incidence triangle internally.

Starting from the selected 135_6-270_3 geometry only:
  * its degree-27 maximal-singular orbit and the 36 minimum words of the
    intrinsic [135,16,30]_2 code reconstruct the 27x36 double-six matrix R;
  * the meeting graph recovered from RR^T has exactly 45 triangles, five
    through every line: these are an intrinsic 45-carrier;
  * each triangle meets each double-six in 0 or 2 lines, with census
    0^540,2^1080, giving T^T R = 2(J-D).

Action-level closure is supplied by the internal-triangle stabilizer: it has
order 576 and fixes exactly one of the 45 protected 16-line supports of
Pass4585. Thus the 45 triangles are PSp-equivariantly the protected 45, which
Pass4616 already intertwines explicitly with the center-quad/E6 tritangent
carrier. No classical labels are imported into the reconstruction itself.
"""
from __future__ import annotations
import itertools, json
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry, build_line_perm, nullspace2, perm_group, transvection_matrix
from w33_pass4587_w33_derived_d4_triality import rank_basis_int, span
from w33_pass4595_concrete_d4_triality_w33_lifts import max_generators
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4659_INTERNAL_E6_27_36_45_TRIANGLE_REGEN.json'

def pmask(mask,p):
    y=0; x=int(mask)
    while x:
        b=x&-x; i=b.bit_length()-1; x^=b; y|=1<<p[i]
    return y

def main():
    pts,pidx,lines,lidx,_,Astar,_,apartments,_=build_geometry(); Astar=np.asarray(Astar,dtype=np.uint8)
    apartments=sorted(tuple(map(int,a)) for a in apartments); n=40; j=(1<<n)-1
    cols=[]
    for c in range(n):
        m=0
        for r in np.flatnonzero(Astar[:,c]): m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i in range(n) for k in range(i+1,n) if Astar[i,k]])
    V=set(span(B9)); rep=lambda x:min(int(x),int(x)^j)
    q=lambda x:(rep(x).bit_count()//4)&1
    polar=lambda x,y:q(x)^q(y)^q(rep(x)^rep(y))
    singular=sorted(x for x in {rep(v) for v in V} if x and q(x)==0); assert len(singular)==135
    def ap_fiber(ap):
        x=0
        for i in ap: x^=cols[i]
        return rep(x)
    def ap_line(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]; assert len(opp)==2
        s=rep(cols[opp[0][0]]^cols[opp[0][1]]); t=rep(cols[opp[1][0]]^cols[opp[1][1]])
        return tuple(sorted((s,t,ap_fiber(ap))))
    selected=sorted({ap_line(a) for a in apartments}); assert len(selected)==270
    sing=sorted(set().union(*(set(L) for L in selected))); assert sing==singular; sidx={x:i for i,x in enumerate(sing)}
    N=np.zeros((135,270),dtype=np.uint8)
    for c,L in enumerate(selected):
        for x in L: N[sidx[x],c]=1

    # intrinsic code and its 36 minimum supports.
    B=nullspace2(N.T); assert len(B)==16
    bm=[]
    for b in B:
        m=0
        for i,z in enumerate(b):
            if int(z): m|=1<<i
        bm.append(m)
    words=[0]
    for b in bm: words += [x^b for x in words]
    minimum=sorted(w for w in words if w.bit_count()==30); assert len(minimum)==36
    min_support=[{sing[i] for i in range(135) if (w>>i)&1} for w in minimum]

    MG=max_generators(singular,rep,q,polar); assert len(MG)==270
    scount=Counter(sum(set(L).issubset(X) for L in selected) for X in MG)
    assert scount==Counter({6:135,0:72,15:36,10:27})
    O27=sorted([X for X in MG if sum(set(L).issubset(X) for L in selected)==10],key=lambda X:tuple(sorted(X))); assert len(O27)==27

    # R is reconstructed by zero intersection inside the selected 135 points.
    R=np.zeros((27,36),dtype=np.int64); ic=Counter()
    for i,X in enumerate(O27):
        S=set(X)-{0}
        assert len(S)==15
        for a,U in enumerate(min_support):
            z=len(S&U); ic[z]+=1; assert z in (0,6)
            if z==0: R[i,a]=1
    assert ic==Counter({6:540,0:432})
    assert set(map(int,R.sum(1)))=={16} and set(map(int,R.sum(0)))=={12} and np.linalg.matrix_rank(R)==21
    I=np.eye(27,dtype=np.int64); J=np.ones((27,27),dtype=np.int64)
    A27=(R@R.T-10*I-6*J)//2
    assert np.array_equal(R@R.T,10*I+2*A27+6*J) and set(map(int,A27.sum(1)))=={10}

    # The intrinsic 45 = triangles of the reconstructed meeting graph.
    tri=[]
    for a,b,c in itertools.combinations(range(27),3):
        if A27[a,b] and A27[a,c] and A27[b,c]: tri.append(frozenset((a,b,c)))
    assert len(tri)==45
    assert Counter(i for t in tri for i in t)==Counter({i:5 for i in range(27)})
    T=np.zeros((27,45),dtype=np.int64)
    for a,t in enumerate(tri):
        for i in t: T[i,a]=1
    assert set(map(int,T.sum(1)))=={5} and set(map(int,T.sum(0)))=={3}

    # 45x36 cross-incidence: triangle/double-six intersection is 0 or 2.
    X=T.T@R; xc=Counter(map(int,X.flat)); assert xc==Counter({2:1080,0:540})
    D=(X==0).astype(np.int64)
    assert set(map(int,D.sum(1)))=={12} and set(map(int,D.sum(0)))=={15}
    assert np.array_equal(X,2*(np.ones((45,36),dtype=np.int64)-D))

    # Exact PSp action and the action-level 45 -> protected-support intertwiner.
    candidates=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    gens=[]; G={tuple(range(40))}
    for p in candidates:
        trial=perm_group(gens+[p])
        if len(trial)>len(G): gens.append(p); G=trial
        if len(G)==25920: break
    assert len(G)==25920
    def act_v(x,g): return rep(pmask(rep(x),g))
    def act_X(X,g): return frozenset(act_v(x,g) for x in X)
    oidx={X:i for i,X in enumerate(O27)}
    tri0=tri[0]
    def act_tri(t,g): return frozenset(oidx[act_X(O27[i],g)] for i in t)
    tri_orbit={act_tri(tri0,g) for g in G}; assert len(tri_orbit)==45 and tri_orbit==set(tri)
    H=[g for g in G if act_tri(tri0,g)==tri0]; assert len(H)==576

    # Pass4585 protected 45 from apartment-fiber unions, constructed independently.
    fibers=defaultdict(list)
    for ap in apartments: fibers[ap_fiber(ap)].append(ap)
    supports=set()
    for _,F in fibers.items(): supports.add(frozenset().union(*(set(ap) for ap in F)))
    assert len(supports)==45 and all(len(U)==16 for U in supports)
    def act_U(U,g): return frozenset(g[i] for i in U)
    fixed=[U for U in supports if all(act_U(U,g)==U for g in H)]; assert len(fixed)==1
    U0=fixed[0]
    mapping={}
    for g in G:
        t=act_tri(tri0,g); U=act_U(U0,g)
        if t in mapping: assert mapping[t]==U
        mapping[t]=U
    assert len(mapping)==45 and set(mapping.values())==supports
    old=json.loads((ROOT/'data/PART_W33_PASS4616_EXPLICIT_45_E6_INTERTWINER.json').read_text())
    assert old['equivariant_bijection_size']==45 and old['common_stabilizer_order']==576

    out={'pass':4659,
      'internal_carriers':{'lines27':27,'double_sixes36':36,'tritangents45':45},
      '27x36':{'intersection_census':{'0':432,'6':540},'R_shape':[27,36],'row_degree':16,'column_degree':12,'rank_Q':21,'meeting_graph':'SRG(27,10,1,5)'},
      '27x45':{'tritangents_as_meeting_triangles':45,'tritangents_per_line':5,'lines_per_tritangent':3},
      '45x36':{'triangle_double_six_line_intersection_census':{'0':540,'2':1080},'disjointness_row_degree':12,'disjointness_column_degree':15,'identity':'T^T R = 2 (J-D)'},
      'action_level_45_bridge':{'internal_triangle_orbit':45,'stabilizer_order':576,'fixed_protected_supports':1,'PSp_equivariant_bijection_to_protected45':True,'composition_with_Pass4616':'protected45 = center-quad/E6-tritangent45'},
      'theorem':'The selected geometry internally reconstructs the complete 27-36-45 cubic-surface incidence triangle: its 27/36 carrier yields exactly 45 meeting triangles, and the three cross-incidences close with explicit matrices. The internal 45 is action-theoretically the previously certified protected/E6 tritangent carrier.',
      'boundary':'Exact finite incidence/G-set theorem; no physical E6 field is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps(out,indent=2,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
