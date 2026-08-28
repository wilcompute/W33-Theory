#!/usr/bin/env python3
"""The 40 O_c subsets form a canonical W33 <-> GQ(4,2) tactical design.

This extends the near-ovoid quotient tower.  The forty 9-sets O_c inside the
45-point minimum-vector carrier are exactly one PSp(4,3)-orbit of ovoids of
GQ(4,2).  The full GQ(4,2) carrier has 200 ovoids, split into PSp orbits 40+160.

For the 40x45 incidence matrix B=[m in O_c]:

    B B^T = 8 I_40 + 2 A_W33 + J_40,
    B^T B = 8 I_45 + 2 A_nonorth,

so every row has size 9, every column has replication 8, orthogonal carrier
pairs occur together in zero rows and nonorthogonal pairs in exactly two.
The nonzero singular spectrum is 72^1 + 12^24, hence rank(B)=25.

Dually, the eight W33 centres containing any carrier point induce K4,4 in W33.
Thus the 45 carrier points may also be read as 45 canonical K4,4 subgraphs of
W33, while the 40 distinguished GQ ovoids recover the 40 W33 points.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260828_FORTY_GQ42_OVOID_DESIGN.json'
Q=3

def norm(v):
    i=next(k for k,x in enumerate(v) if x%Q);z=pow(v[i]%Q,-1,Q)
    return tuple((z*x)%Q for x in v)
def form(u,v):return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%Q

def geometry():
    pts=sorted({norm(v) for v in itertools.product(range(Q),repeat=4) if any(v)})
    idx={v:i for i,v in enumerate(pts)};lines=set()
    for a,b in itertools.combinations(range(40),2):
        if form(pts[a],pts[b]):continue
        S=set()
        for s,t in itertools.product(range(Q),repeat=2):
            if s==t==0:continue
            S.add(idx[norm(tuple((s*pts[a][k]+t*pts[b][k])%Q for k in range(4)))])
        if len(S)==4:lines.add(tuple(sorted(S)))
    return pts,idx,sorted(lines)

def solve_near(lines,pls,target):
    allowed={p for p in range(40) if all(target[l]>0 for l in pls[p])}
    cand=[[p for p in L if p in allowed] for L in lines];cnt=[0]*40;ch=[];sol=set()
    def rec():
        if len(ch)>10:return
        unmet=[]
        for l,t in enumerate(target):
            if cnt[l]>t:return
            need=t-cnt[l]
            if need:
                F=[p for p in cand[l] if p not in ch and all(cnt[j]<target[j] for j in pls[p])]
                if len(F)<need:return
                unmet.append((len(F),-need,l,F))
        if not unmet:
            if len(ch)==10:sol.add(tuple(sorted(ch)))
            return
        _,ng,_,F=min(unmet);need=-ng
        for sub in itertools.combinations(F,need):
            d=Counter()
            for p in sub:
                for j in pls[p]:d[j]+=1
            if any(cnt[j]+z>target[j] for j,z in d.items()):continue
            ch.extend(sub)
            for j,z in d.items():cnt[j]+=z
            rec()
            for j,z in d.items():cnt[j]-=z
            del ch[-len(sub):]
    rec();return sorted(sol)

def compose(p,q):return tuple(p[q[i]] for i in range(len(q)))

def main():
    pts,idx,lines=geometry();assert len(lines)==40
    N=[[0]*40 for _ in range(40)];pls=[[] for _ in range(40)]
    for l,L in enumerate(lines):
        for p in L:N[l][p]=1;pls[p].append(l)
    cols=[tuple(N[l][p] for l in range(40)) for p in range(40)]

    # 45 minimum-vector lines from the 4-subset signature collisions.
    sig=defaultdict(list)
    for S in itertools.combinations(range(40),4):
        z=tuple(sum(cols[p][l] for p in S) for l in range(40));sig[z].append(S)
    pairs=sorted(tuple(sorted((tuple(v[0]),tuple(v[1])))) for v in sig.values() if len(v)==2)
    assert len(pairs)==45
    mins=[tuple(1 if i in b else -1 if i in a else 0 for i in range(40)) for a,b in pairs]
    orth=[set() for _ in range(45)]
    for i,j in itertools.combinations(range(45),2):
        if sum(mins[i][k]*mins[j][k] for k in range(40))==0:orth[i].add(j);orth[j].add(i)
    assert {len(x) for x in orth}=={12}
    non=[set(range(45))-{i}-orth[i] for i in range(45)]

    # Every oriented dipole yields near-ovoids; adding the defect centre gives
    # the 360 minimum blockers, grouped nine per blocker centre.
    blockers=defaultdict(set)
    for a in range(40):
        for c in range(40):
            H=set(pls[a])&set(pls[c])
            if len(H)!=1:continue
            h=next(iter(H));target=[1]*40
            for l in set(pls[a])-{h}:target[l]=0
            for l in set(pls[c])-{h}:target[l]=2
            for S in solve_near(lines,pls,target):blockers[c].add(tuple(sorted(S+(a,))))
    assert Counter(map(len,blockers.values()))==Counter({9:40})

    # A blocker pair difference is a local trade and uniquely determines the
    # nonorthogonal edge between two minimum-vector lines.
    signed=[]
    for i,v in enumerate(mins):signed += [(i,v),(i,tuple(-z for z in v))]
    sumedge={}
    for ia,va in signed:
        for ib,vb in signed:
            if ia>=ib:continue
            s=tuple(va[k]+vb[k] for k in range(40))
            if sum(z*z for z in s)==12:sumedge[s]=(ia,ib)
    assert len(sumedge)==1440

    O=[]
    for c in range(40):
        bs=sorted(blockers[c]);labs=[]
        for i,B in enumerate(bs):
            SB=set(B);edges=[]
            for j,C in enumerate(bs):
                if i==j:continue
                SC=set(C);d=tuple(int(k in SC)-int(k in SB) for k in range(40))
                edges.append(sumedge[d])
            common=set(edges[0])
            for e in edges[1:]:common&=set(e)
            assert len(common)==1;labs.append(next(iter(common)))
        assert len(set(labs))==9;O.append(frozenset(labs))
    assert len(set(O))==40

    # Tactical design identities.
    rep=Counter(m for S in O for m in S);assert rep==Counter({m:8 for m in range(45)})
    inter=Counter();trip=defaultdict(Counter)
    padj=[set() for _ in range(40)]
    for L in lines:
        for a,b in itertools.combinations(L,2):padj[a].add(b);padj[b].add(a)
    for a,c in itertools.combinations(range(40),2):
        z=len(O[a]&O[c]);inter[(c in padj[a],z)]+=1
    assert inter==Counter({(True,3):240,(False,1):540})
    assert all(all(j in non[i] for i,j in itertools.combinations(S,2)) for S in O)

    pairco=Counter()
    for i,j in itertools.combinations(range(45),2):
        z=sum(i in S and j in S for S in O);pairco[(j in orth[i],z)]+=1
    assert pairco==Counter({(True,0):270,(False,2):720})

    # Columns are canonical K4,4 subgraphs of W33.
    columns=[]
    for m in range(45):
        C={c for c in range(40) if m in O[c]};assert len(C)==8
        deg={c:len(C&padj[c]) for c in C};assert set(deg.values())=={4}
        # Bipartite BFS, then all 16 cross edges must occur.
        side={next(iter(C)):0};front=list(side)
        while front:
            u=front.pop()
            for v in C&padj[u]:
                if v not in side:side[v]=1-side[u];front.append(v)
                else:assert side[v]!=side[u]
        assert Counter(side.values())==Counter({0:4,1:4})
        columns.append(tuple(sorted(C)))
    assert len(set(columns))==45

    # Triple intersections refine the W33 induced-edge type.
    for a,b,c in itertools.combinations(range(40),3):
        e=int(b in padj[a])+int(c in padj[a])+int(c in padj[b])
        trip[e][len(O[a]&O[b]&O[c])]+=1
    expected={0:Counter({0:2880,1:360}),1:Counter({0:4320}),2:Counter({1:2160}),3:Counter({0:160})}
    assert dict(trip)==expected

    # Enumerate every 9-clique in the nonorthogonality graph (= every ovoid of
    # GQ(4,2)) by Bron-Kerbosch with pivot.
    allovoids=set()
    def bron(R,P,X):
        if not P and not X:
            if len(R)==9:allovoids.add(frozenset(R))
            return
        if len(R)+len(P)<9:return
        U=P|X;u=max(U,key=lambda z:len(P&non[z])) if U else None
        for v in list(P-(non[u] if u is not None else set())):
            bron(R|{v},P&non[v],X&non[v]);P.remove(v);X.add(v)
    bron(set(),set(range(45)),set())
    assert len(allovoids)==200 and set(O)<=allovoids

    # PSp generators induce the ovoid orbit split 40+160.
    pairidx={p:i for i,p in enumerate(pairs)}
    gens=[]
    for v in pts:
        for a in (1,2):
            g=[]
            for x in pts:
                cc=a*form(x,v)%3;y=norm(tuple((x[k]+cc*v[k])%3 for k in range(4)));g.append(idx[y])
            h=[]
            for A,B in pairs:
                AA=tuple(sorted(g[i] for i in A));BB=tuple(sorted(g[i] for i in B));h.append(pairidx[tuple(sorted((AA,BB)))])
            gens.append(tuple(h))
    def orbit(S):
        seen={frozenset(S)};front=list(seen)
        while front:
            T=front.pop()
            for g in gens:
                U=frozenset(g[i] for i in T)
                if U not in seen:seen.add(U);front.append(U)
        return seen
    small=orbit(O[0]);assert len(small)==40 and small==set(O)
    other=next(S for S in allovoids if S not in small);large=orbit(other)
    assert len(large)==160 and not (small&large) and small|large==allovoids

    out={
      'schema':'w33.20260828.forty-gq42-ovoid-design.v1','status':'PASS',
      'tactical_configuration':{'rows':40,'columns':45,'row_size':9,'column_replication':8,
        'row_intersections':{'W33_adjacent':3,'W33_nonadjacent':1},
        'column_pair_cooccurrence':{'GQ42_orthogonal':0,'GQ42_nonorthogonal':2}},
      'matrix_identities':{'BBt':'8 I_40 + 2 A_W33 + J_40','BtB':'8 I_45 + 2 A_nonorth',
        'nonzero_singular_squares':{'72':1,'12':24},'rank':25},
      'GQ42_ovoids':{'total':200,'PSp_orbits':[40,160],'distinguished_orbit':40,
        'distinguished_stabilizer_order':648},
      'dual_W33_reading':{'carrier_points':45,'centres_per_carrier_point':8,'induced_graph':'K4,4'},
      'triple_intersections':{str(k):dict(sorted(v.items())) for k,v in sorted(trip.items())},
      'theorem':'The forty O_c are exactly the 40-element PSp(4,3) orbit among the 200 ovoids of GQ(4,2). Their 40x45 incidence matrix is a (40_9,45_8) tactical configuration satisfying BB^T=8I+2A_W33+J and B^TB=8I+2A_nonorth. Each GQ carrier point corresponds dually to a canonical K4,4 on eight W33 points.',
      'boundary':'Exact finite design/group-action statement only.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','ovoids':200,'orbits':[40,160],'rank':25,'columns':'45 K4,4'}))
if __name__=='__main__':main()
