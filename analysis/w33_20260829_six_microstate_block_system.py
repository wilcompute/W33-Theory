#!/usr/bin/env python3
"""Exact local group action on the six optimal near-ovoid completions.

For one oriented collinear W33 pair (a,c), rebuild the six completions, their
high-release signatures, the PSp(4,3) oriented-edge stabilizer, and its induced
six-point action.  The migration 3+3 split is proved to be the unique block
system of that action and is identified with the two residual hinge points.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter,deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260829_SIX_MICROSTATE_BLOCK_SYSTEM.json'

def norm(v):
    i=next(k for k,x in enumerate(v) if x%3); z=pow(v[i]%3,-1,3)
    return tuple((z*x)%3 for x in v)
def form(u,v): return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%3
def compose(p,q): return tuple(p[q[i]] for i in range(len(q)))
def porder(p):
    seen=[False]*len(p);o=1
    for i in range(len(p)):
        if seen[i]: continue
        j=i;n=0
        while not seen[j]: seen[j]=True;n+=1;j=p[j]
        o=math.lcm(o,n)
    return o

def geometry():
    pts=sorted({norm(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    idx={v:i for i,v in enumerate(pts)}; lines=set()
    for a,b in itertools.combinations(range(40),2):
        if form(pts[a],pts[b]): continue
        S=set()
        for s,t in itertools.product(range(3),repeat=2):
            if s==t==0: continue
            S.add(idx[norm(tuple((s*pts[a][k]+t*pts[b][k])%3 for k in range(4)))])
        if len(S)==4: lines.add(tuple(sorted(S)))
    lines=sorted(lines); pls=[[] for _ in range(40)];adj=[set() for _ in range(40)]
    for li,L in enumerate(lines):
        for p in L: pls[p].append(li)
        for x,y in itertools.combinations(L,2): adj[x].add(y);adj[y].add(x)
    return pts,idx,lines,pls,adj

def solve(lines,pls,target):
    allowed={p for p in range(40) if all(target[l]>0 for l in pls[p])}
    cand=[[p for p in L if p in allowed] for L in lines];cnt=[0]*40;ch=[];inside=[False]*40;sol=set()
    def rec():
        if len(ch)>10:return
        unmet=[]
        for l,t in enumerate(target):
            if cnt[l]>t:return
            need=t-cnt[l]
            if need:
                F=[p for p in cand[l] if not inside[p] and all(cnt[j]<target[j] for j in pls[p])]
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
            for p in sub:ch.append(p);inside[p]=True
            for j,z in d.items():cnt[j]+=z
            rec()
            for j,z in d.items():cnt[j]-=z
            for _ in sub:inside[ch.pop()]=False
    rec();return sorted(sol)

def main():
    pts,idx,lines,pls,adj=geometry(); a=0;c=min(adj[a])
    hinge=next(iter(set(pls[a])&set(pls[c]))); residual=sorted(set(lines[hinge])-{a,c})
    target=[1]*40
    for l in set(pls[a])-{hinge}:target[l]=0
    for l in set(pls[c])-{hinge}:target[l]=2
    sols=solve(lines,pls,target);assert len(sols)==6
    def free(S):
        T=set(S);return [li for li,L in enumerate(lines) if not (T&set(L))]
    highs=[]
    for S in sols:
        H=tuple(sorted(y for y in S if len(free(set(S)-{y}))==7));assert len(H)==4
        assert len(set(H)&set(residual))==1;highs.append(H)
    blocks=[]
    for r in residual:
        I=tuple(i for i,H in enumerate(highs) if r in H);assert len(I)==3;blocks.append(I)
    assert set(blocks[0]).isdisjoint(blocks[1])

    gens=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for x in pts:
                z=alpha*form(x,v)%3;y=norm(tuple((x[k]+z*v[k])%3 for k in range(4)));p.append(idx[y])
            gens.append(tuple(p))
    ident=tuple(range(40));G={ident};Q=deque([ident])
    while Q:
        p=Q.popleft()
        for g in gens:
            h=compose(g,p)
            if h not in G:G.add(h);Q.append(h)
    assert len(G)==25920
    stab=[p for p in G if p[a]==a and p[c]==c];assert len(stab)==54
    si={S:i for i,S in enumerate(sols)};image=set()
    for p in stab:
        image.add(tuple(si[tuple(sorted(p[x] for x in S))] for S in sols))
    assert len(image)==18 and Counter(map(porder,image))==Counter({1:1,2:3,3:8,6:6})
    all6=set(range(6));systems=[]
    for A in itertools.combinations(range(6),3):
        A=set(A);B=all6-A
        if min(B)<min(A):continue
        if all(({p[i] for i in A}==A and {p[i] for i in B}==B) or ({p[i] for i in A}==B and {p[i] for i in B}==A) for p in image):
            systems.append((tuple(sorted(A)),tuple(sorted(B))))
    assert len(systems)==1 and {frozenset(x) for x in systems[0]}=={frozenset(x) for x in blocks}
    fix=[p for p in image if {p[i] for i in blocks[0]}==set(blocks[0])]
    assert len(fix)==9 and Counter(map(porder,fix))==Counter({1:1,3:8})

    out={'schema':'w33.20260829.six-microstate-block-system.v1','status':'PASS',
      'orientedDefectPair':[a,c],'hingeLine':hinge,'hingePoints':list(lines[hinge]),'residualHingePoints':residual,
      'localAction':{'orientedEdgeStabilizer':54,'sixStateImageOrder':18,'sixStateImage':'C3 x S3','kernelOrder':3,
                     'elementOrders':{'1':1,'2':3,'3':8,'6':6}},
      'blockSystem':{'uniqueNontrivialThreePlusThree':True,'blocks':[list(x) for x in blocks],
                     'blockFixingImageOrder':9,'blockFixingImage':'C3 x C3','fullPreimageOrder':27,'quotient':'C2'},
      'migrationGeometry':{'highReleaseSize':4,'hingeIntersectionSize':1,
        'rule':'the two 3-state blocks are exactly the states whose high-release set contains one or the other residual point of the hinge line'},
      'theorem':'The two K3 migration microstate halves are the unique system of imprimitivity of the exact C3xS3 six-completion action. The C2 quotient swaps both the two blocks and the two residual hinge points.',
      'boundary':'Finite group-action and scheduler-signature theorem only.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','stabilizer':54,'image':18,'blocks':'3+3','kernel':9,'quotient':'C2'}))
if __name__=='__main__':main()
