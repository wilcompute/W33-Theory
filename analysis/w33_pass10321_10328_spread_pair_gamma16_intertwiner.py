#!/usr/bin/env python3
"""Pass10321-10328: explicit objectwise bridge from four-intersection spread pairs to Gamma16.

This pass closes the strongest open bridge from Pass10169-10176.

Starting from W(3,3) in F3^4 it independently reconstructs:
* 40 projective points and 40 totally isotropic lines;
* all 36 spreads (10 disjoint lines covering all 40 points);
* all 630 spread pairs, with intersection distribution 360 pairs sharing 1 line
  and 270 pairs sharing 4 lines;
* PSp4(3) of order 25920 from four symplectic transvections, and the full
  point-collinearity group PGSp4(3)=PSp4(3):2 of order 51840 after adding a
  nonsquare similitude.

For one pair of spreads sharing four lines, the four common lines contain 16
points.  The W33 induced collinearity graph on those points is explicitly
identified with the Pass10169 graph

  Gamma16 = Cay(C4 x C4,{(0,1),(0,2),(0,3),(1,2),(2,2),(3,2)}).

The common spread lines are exactly its four K4 fibres.  The full unordered
spread-pair stabilizer in PGSp4(3) has order 192 (the PSp half has order 96).
Its restriction to the 16 common points is faithful and has 192 distinct
permutations.  Pass10169 proved |Aut(Gamma16)|=192, so the restriction is an
ISOMORPHISM onto the entire graph automorphism group S4 x D8.

Thus the old spread-intersection 192-group and the new Hermitian-residue
192-group are the same permutation geometry, not merely equal orders.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10321_10328_SPREAD_PAIR_GAMMA16_INTERTWINER.json'
P=3

def canon(v):
    v=tuple(int(x)%P for x in v)
    for x in v:
        if x:
            u=pow(x,-1,P);return tuple(u*y%P for y in v)
    raise ValueError

def omega(u,v):return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%P

def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))

def gen_group(gens,n,limit):
    ident=tuple(range(n));seen={ident};Q=deque([ident])
    while Q:
        g=Q.popleft()
        for h in gens:
            z=comp(h,g)
            if z not in seen:
                seen.add(z);Q.append(z)
                if len(seen)>limit:raise RuntimeError('group limit exceeded')
    return seen

def main():
    pts=sorted({canon(v) for v in itertools.product(range(P),repeat=4) if any(v)})
    assert len(pts)==40;pidx={p:i for i,p in enumerate(pts)}

    # W33 point collinearity and 40 isotropic lines.
    A=np.zeros((40,40),dtype=np.uint8);lines=set()
    coeff=((1,0),(0,1),(1,1),(1,2))
    for i,p in enumerate(pts):
        for j in range(i+1,40):
            q=pts[j]
            if omega(p,q)==0:
                A[i,j]=A[j,i]=1
                L=frozenset(canon(tuple((a*p[k]+b*q[k])%P for k in range(4))) for a,b in coeff)
                if len(L)==4:lines.add(L)
    lines=sorted(lines,key=lambda L:sorted(L));assert len(lines)==40
    lpidx=[frozenset(pidx[p] for p in L) for L in lines]
    line_by_pts={L:i for i,L in enumerate(lpidx)}

    # Enumerate all spreads as exact covers by 10 disjoint lines.
    masks=[];through=[[] for _ in range(40)]
    for li,L in enumerate(lpidx):
        m=0
        for x in L:m|=1<<x;through[x].append(li)
        masks.append(m)
    FULL=(1<<40)-1;spreads=[]
    def rec(mask,chosen):
        if mask==FULL:
            spreads.append(tuple(sorted(chosen)));return
        unc=[i for i in range(40) if not ((mask>>i)&1)]
        x=min(unc,key=lambda i:sum(1 for li in through[i] if not (masks[li]&mask)))
        for li in through[x]:
            if not (masks[li]&mask):rec(mask|masks[li],chosen+[li])
    rec(0,[])
    spreads=sorted(set(spreads));assert len(spreads)==36 and all(len(s)==10 for s in spreads)
    spread_index={frozenset(s):i for i,s in enumerate(spreads)}

    pairdist=Counter();pairs4=[]
    for a,b in itertools.combinations(range(36),2):
        inter=tuple(sorted(set(spreads[a])&set(spreads[b])))
        pairdist[len(inter)]+=1
        if len(inter)==4:pairs4.append((a,b,inter))
    assert pairdist==Counter({1:360,4:270})

    # Generate PSp4(3) efficiently from four transvections.
    def trans_perm(v):
        out=[]
        for x in pts:
            s=omega(x,v);y=tuple((x[k]+s*v[k])%P for k in range(4));out.append(pidx[canon(y)])
        return tuple(out)
    seed_vectors=[(0,1,1,1),(1,2,1,2),(0,1,0,0),(1,0,1,0)]
    trans=[trans_perm(v) for v in seed_vectors]
    PSp=gen_group(trans,40,30000);assert len(PSp)==25920

    # Nonsquare similitude diag(2,2,1,1) has multiplier 2 and doubles to PGSp.
    D=np.diag([2,2,1,1])%P
    def mat_perm(M):return tuple(pidx[canon(tuple((M@np.array(x,dtype=int))%P))] for x in pts)
    sim=mat_perm(D)
    PGSp=gen_group(trans+[sim],40,60000);assert len(PGSp)==51840

    def line_perm(g):return tuple(line_by_pts[frozenset(g[x] for x in L)] for L in lpidx)

    # Choose deterministic representative of the 270 orbit.
    sa,sb,common=pairs4[0];S0=set(spreads[sa]);S1=set(spreads[sb])
    common_lines=[lpidx[i] for i in common]
    common_points=sorted(set().union(*common_lines));assert len(common_points)==16

    # Target Gamma16.
    V=[(a,b) for a in range(4) for b in range(4)];vidx={v:i for i,v in enumerate(V)}
    conn={(0,1),(0,2),(0,3),(1,2),(2,2),(3,2)}
    def gadj(x,y):return ((y[0]-x[0])%4,(y[1]-x[1])%4) in conn

    # Find explicit fibre-preserving isomorphism: common lines -> four K4 fibres.
    fibres=[sorted(L) for L in common_lines];iso=None
    for order in itertools.permutations(range(4)):
        F=[fibres[i] for i in order]
        for lab0 in itertools.permutations(F[0]):
            labels=[list(lab0)];ok=True
            for j in range(1,4):
                lab=[None]*4
                for b in range(4):
                    neigh=[q for q in F[j] if A[lab0[b],q]]
                    if len(neigh)!=1:ok=False;break
                    lab[(b+2)%4]=neigh[0]
                if not ok:break
                labels.append(lab)
            if not ok:continue
            mp={(a,b):labels[a][b] for a in range(4) for b in range(4)}
            if all(bool(A[mp[x],mp[y]])==gadj(x,y) for x,y in itertools.combinations(V,2)):
                iso=(order,labels,mp);break
        if iso:break
    assert iso is not None
    order,labels,mp=iso

    # Full group orbit of the selected pair is exactly all 270 four-intersection pairs.
    orbit=set();stab_full=[];stab_psp=[]
    for group,is_psp in ((PGSp,False),(PSp,True)):
        for g in group:
            lp=line_perm(g);im0=frozenset(lp[i] for i in S0);im1=frozenset(lp[i] for i in S1)
            if not is_psp:
                orbit.add(tuple(sorted((spread_index[im0],spread_index[im1]))))
            if (im0==frozenset(S0) and im1==frozenset(S1)) or (im0==frozenset(S1) and im1==frozenset(S0)):
                (stab_psp if is_psp else stab_full).append(g)
    assert len(orbit)==270 and set(orbit)=={tuple(sorted((a,b))) for a,b,_ in pairs4}
    assert len(stab_psp)==96 and len(stab_full)==192

    # Restrict the 192 stabilizer elements to the common 16 points.  Faithful image order 192.
    loc={x:i for i,x in enumerate(common_points)};restr=set()
    for g in stab_full:
        assert {g[x] for x in common_points}==set(common_points)
        p=tuple(loc[g[x]] for x in common_points)
        assert all(bool(A[common_points[i],common_points[j]])==bool(A[common_points[p[i]],common_points[p[j]]]) for i in range(16) for j in range(16))
        restr.add(p)
    assert len(restr)==192

    # Pass10169 independently proved the target graph full Aut order 192.
    old=json.loads((ROOT/'data/PART_W33_PASS10169_10176_ISOTROPIC16_CAYLEY_GRAPH.json').read_text())
    assert old['automorphisms']['full_order']==192 and old['automorphisms']['structure']=='S4 x D8'

    out={
      'schema':'w33.pass10321_10328.spread_pair_gamma16_intertwiner.v1','status':'PASS','passes':'10321-10328',
      'W33':{'points':40,'lines':40,'spreads':36,'spread_size':10,'spread_pair_intersections':{'1':360,'4':270}},
      'groups':{'PSp4_3_order':len(PSp),'PGSp4_3_order':len(PGSp),'four_intersection_pair_stabilizer_PSp':len(stab_psp),'four_intersection_pair_stabilizer_PGSp':len(stab_full)},
      'representative_pair':{'spread_indices':[sa,sb],'common_line_indices':list(common),'common_points':common_points,
                             'explicit_gamma16_labels':{f'{a},{b}':int(mp[(a,b)]) for a,b in V},
                             'common_lines_become_K4_fibres':True},
      'orbit':{'PGSp_orbit_size':len(orbit),'equals_all_four_intersection_pairs':True},
      'stabilizer_action':{'common_16_point_restriction_order':len(restr),'faithful':True,'target_graph_Aut_order':192,'isomorphism':'Stab_PGSp({S,T}) ~= Aut(Gamma16) ~= S4 x D8'},
      'theorem':'For every pair of W33 spreads sharing four lines, the 16 points on those common lines induce exactly the Hermitian-isotropic Gamma16 graph from Pass10169. The full PGSp4(3) stabilizer of the unordered spread pair has order 192 and acts faithfully as the entire automorphism group Aut(Gamma16)=S4 x D8. The four shared spread lines are precisely the four K4 fibres. Thus the spread-pair and Hermitian-residue constructions are objectwise the same 16-point permutation geometry.',
      'consequence':'The earlier S4 x D8 coincidence is upgraded to an explicit transporter. The local Hermitian W33 selector is canonically realized inside the global spread geometry as the common-point geometry of a four-intersection spread pair.',
      'boundary':'Exact exhaustive finite computation. The isomorphism is at the W33 incidence/permutation level; no claim is made yet that the local-field chamber itself canonically selects a unique global spread pair.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','spreads':36,'pairs4':270,'stabilizer':192,'restriction':192,'bridge':'OBJECTWISE'}))
    return 0
if __name__=='__main__':raise SystemExit(main())
