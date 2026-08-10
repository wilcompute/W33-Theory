#!/usr/bin/env python3
"""Pass 4661 (outside box) — the 120 nonsingular shell carries the dual 40x3 scheme.

Enumerate all anisotropic F2 two-planes in the W33-derived O^+(8,2) quotient.
There are 1120, split by PSp(4,3) into orbits 40+1080.  The 40-orbit partitions
all 120 nonsingular vectors into 40 triples.  Four intrinsic relations on the
120 vectors have valencies 2,36,27,54:
  R1 same anisotropic plane;
  R2 different planes that are totally polar-orthogonal;
  R3 nonadjacent planes, polar-orthogonal vector pair;
  R4 nonadjacent planes, nonorthogonal vector pair.
Their complete intersection tensor equals the historical Pass1355 selector
matching association algebra exactly.

Crucially, this is NOT promoted as the same PSp G-set.  Pass4654 identifies the
40-plane quotient with W33 points and proves its stabilizer fixes no W33 line,
whereas Pass1355's selector fibers are indexed by the 40 isotropic W33 lines.
Since R1 is intrinsic, any PSp-equivariant scheme isomorphism would induce a
point/line quotient isomorphism, which is impossible.  The result is an exact
point-side/line-side dual pair of association algebras, not a count-only merge.
"""
from __future__ import annotations
import itertools, json
from collections import Counter, deque
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry, build_line_perm, perm_group, transvection_matrix
from w33_pass4587_w33_derived_d4_triality import rank_basis_int, span
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4661_ANISOTROPIC_120_SCHEME_DUALITY_REGEN.json'

def pmask(mask,p):
    y=0; x=int(mask)
    while x:
        b=x&-x; i=b.bit_length()-1; x^=b; y|=1<<p[i]
    return y

def main():
    pts,pidx,lines,lidx,_,Astar,_,_,_=build_geometry(); Astar=np.asarray(Astar,dtype=np.uint8); n=40; j=(1<<n)-1
    cols=[]
    for c in range(n):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i in range(n) for k in range(i+1,n) if Astar[i,k]])
    V=set(span(B9)); rep=lambda x:min(int(x),int(x)^j); reps={rep(x) for x in V}
    q=lambda x:(rep(x).bit_count()//4)&1; pol=lambda x,y:q(x)^q(y)^q(rep(x)^rep(y))
    nons=sorted(x for x in reps if x and q(x)==1); assert len(nons)==120
    planes=set()
    for a,b in itertools.combinations(nons,2):
        c=rep(a^b)
        if c in set(nons): planes.add(frozenset((a,b,c)))
    assert len(planes)==1120

    candidates=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    gens=[]; G={tuple(range(40))}
    for p in candidates:
        trial=perm_group(gens+[p])
        if len(trial)>len(G): gens.append(p); G=trial
        if len(G)==25920:break
    assert len(G)==25920 and len(gens)==5
    def act_v(x,g):return rep(pmask(rep(x),g))
    def act_P(P,g):return frozenset(act_v(x,g) for x in P)
    def orbit(seed):
        S={seed};Q=deque([seed])
        while Q:
            P=Q.popleft()
            for g in gens:
                Z=act_P(P,g)
                if Z not in S:S.add(Z);Q.append(Z)
        return S
    rem=set(planes); orbits=[]
    while rem:
        O=orbit(next(iter(rem)));orbits.append(O);rem-=O
    assert sorted(map(len,orbits))==[40,1080]
    P40=sorted(next(O for O in orbits if len(O)==40),key=lambda P:tuple(sorted(P)))
    assert len(set().union(*P40))==120 and all(len(A&B)==0 for A,B in itertools.combinations(P40,2))
    pof={x:i for i,P in enumerate(P40) for x in P}; nidx={x:i for i,x in enumerate(nons)}

    Q40=np.zeros((40,40),dtype=np.uint8); cross=Counter()
    for a,b in itertools.combinations(range(40),2):
        z=sum(pol(x,y)==0 for x in P40[a] for y in P40[b]);cross[z]+=1
        assert z in (3,9)
        if z==9:Q40[a,b]=Q40[b,a]=1
    assert cross==Counter({3:540,9:240}) and set(map(int,Q40.sum(1)))=={12}

    R=[np.zeros((120,120),dtype=np.uint8) for _ in range(5)];R[0]=np.eye(120,dtype=np.uint8)
    for i,x in enumerate(nons):
        for k,y in enumerate(nons):
            if i==k:continue
            a,b=pof[x],pof[y]
            if a==b:r=1
            elif Q40[a,b]:r=2
            elif pol(x,y)==0:r=3
            else:r=4
            R[r][i,k]=1
    val=[int(M.sum(1)[0]) for M in R]; assert val==[1,2,36,27,54]
    assert all(set(map(int,M.sum(1)))=={val[i]} for i,M in enumerate(R))

    # Exact intersection tensor p_{ij}^k, verified constant on every relation.
    tensor=[]
    for i in range(5):
        block=[]
        P=R[i].astype(np.int64)
        for jj in range(5):
            M=P@R[jj].astype(np.int64); vals=[]
            for k in range(5):
                loc=np.argwhere(R[k])
                z={int(M[a,b]) for a,b in loc}; assert len(z)==1; vals.append(next(iter(z)))
            block.append(vals)
        tensor.append(block)
    old=json.loads((ROOT/'data/w33_pass1355_1359_selector_matching_scheme.json').read_text())
    assert tensor==old['intersection_numbers']
    assert val==old['relations']['valencies']
    assert old['construction']['selectors']==120 and old['construction']['isotropic_lines']==40
    p4654=json.loads((ROOT/'data/PART_W33_PASS4654_TRIALITY_PLANE_W33_POINT_INTERTWINER.json').read_text())
    assert p4654['target_carrier']=='W33 point carrier' and p4654['fixed_W33_lines']==[]

    out={'pass':4661,'anisotropic_planes':{'total':1120,'PSp_orbits':[40,1080],'small_orbit_partitions_nonsingular120':'40 x 3'},
      'scheme':{'vertices':120,'valencies':val,'relations':['identity','same_anisotropic_plane','totally_orthogonal_plane_pair','nonadjacent_plane_orthogonal_pair','nonadjacent_plane_nonorthogonal_pair'],'intersection_tensor_equals_Pass1355':True,'quotient':'SRG(40,12,2,4) W33 point carrier'},
      'comparison_to_Pass1355':{'same_Bose_Mesner_intersection_algebra':True,'Pass1355_quotient':'40 isotropic W33 lines','new_quotient':'40 W33 points','PSp_equivariant_isomorphism':False,'obstruction':'intrinsic 3-fiber quotient would force the inequivalent W33 point and line G-sets to be isomorphic'},
      'theorem':'The 120 nonsingular vectors carry a 40x3 four-class association scheme with exactly the Pass1355 selector intersection algebra, but on the dual PSp action type: its quotient is W33 points rather than W33 lines. The equality is algebraic while the G-set identification is explicitly obstructed.',
      'boundary':'Finite association-scheme/action duality; no physical selector interpretation.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
