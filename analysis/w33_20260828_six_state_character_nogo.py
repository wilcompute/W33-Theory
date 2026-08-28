#!/usr/bin/env python3
"""Exact six-state permutation-character no-go.

Compare two canonical six-state actions:
A) the six optimal near-ovoid completions over one oriented W33 defect dipole;
B) the six orbits of the split involution j:z->-z on P^1(F_9), acted on by
   its PGL(2,9) centralizer.

The first action has image C3 x S3 of order18 and is transitive.
The second has image D8 of order8 and has orbits 2+4.
Their permutation characters, element orders, and orbit structures differ, so
there is no equivariant bijection. This sharpens the parallel HJ10 weight
obstruction: even after forgetting fibre weights, the canonical six-state
actions are inequivalent.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter
from pathlib import Path
Q=3
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"PART_W33_20260828_SIX_STATE_CHARACTER_NOGO.json"

def compose(a,b): return tuple(a[b[i]] for i in range(len(b)))
def order(p):
    seen=set();o=1
    for i in range(len(p)):
        if i in seen:continue
        j=i;n=0
        while j not in seen:seen.add(j);n+=1;j=p[j]
        o=math.lcm(o,n)
    return o
def closure(gens,n):
    e=tuple(range(n));G={e};front=[e]
    while front:
        h=front.pop()
        for g in gens:
            z=compose(g,h)
            if z not in G:G.add(z);front.append(z)
    return G

# ---------- W33 local six ----------
def norm(v):
    i=next(k for k,x in enumerate(v) if x%3);z=pow(v[i]%3,-1,3)
    return tuple((z*x)%3 for x in v)
def form(u,v):return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%3
def geom():
    pts=sorted({norm(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    idx={v:i for i,v in enumerate(pts)};lines=set()
    for a,b in itertools.combinations(range(40),2):
        if form(pts[a],pts[b]):continue
        S=set()
        for s,t in itertools.product(range(3),repeat=2):
            if s==t==0:continue
            S.add(idx[norm(tuple((s*pts[a][k]+t*pts[b][k])%3 for k in range(4)))])
        if len(S)==4:lines.add(tuple(sorted(S)))
    return pts,sorted(lines)
def solve(lines,pls,target):
    allowed={p for p in range(40) if all(target[l]>0 for l in pls[p])}
    cand=[[p for p in L if p in allowed] for L in lines];cnt=[0]*40;chosen=[];sol=set()
    def rec():
        if len(chosen)>10:return
        unmet=[]
        for l,t in enumerate(target):
            if cnt[l]>t:return
            need=t-cnt[l]
            if need:
                F=[p for p in cand[l] if p not in chosen and all(cnt[j]<target[j] for j in pls[p])]
                if len(F)<need:return
                unmet.append((len(F),-need,l,F))
        if not unmet:
            if len(chosen)==10:sol.add(tuple(sorted(chosen)))
            return
        _,ng,_,F=min(unmet);need=-ng
        for sub in itertools.combinations(F,need):
            d=Counter()
            for p in sub:
                for j in pls[p]:d[j]+=1
            if any(cnt[j]+z>target[j] for j,z in d.items()):continue
            chosen.extend(sub)
            for j,z in d.items():cnt[j]+=z
            rec()
            for j,z in d.items():cnt[j]-=z
            del chosen[-len(sub):]
    rec();return sorted(sol)
def transvection(pts,idx,v):
    out=[]
    for x in pts:
        s=form(x,v);y=tuple((x[k]+s*v[k])%3 for k in range(4))
        out.append(idx[norm(y)])
    return tuple(out)

def local_action():
    pts,lines=geom();idx={v:i for i,v in enumerate(pts)}
    pls=[[] for _ in range(40)]
    for li,L in enumerate(lines):
        for p in L:pls[p].append(li)
    a=0;b=next(x for x in range(1,40) if len(set(pls[a])&set(pls[x]))==1)
    h=next(iter(set(pls[a])&set(pls[b])))
    target=[1]*40
    for l in set(pls[a])-{h}:target[l]=0
    for l in set(pls[b])-{h}:target[l]=2
    sols=solve(lines,pls,target);assert len(sols)==6
    trans=[transvection(pts,idx,v) for v in pts]
    G=closure([trans[i] for i in (17,26,23,2)],40);assert len(G)==25920
    stab=[g for g in G if g[a]==a and g[b]==b];assert len(stab)==54
    SS=[frozenset(s) for s in sols];image=set()
    for g in stab:
        image.add(tuple(SS.index(frozenset(g[p] for p in S)) for S in SS))
    assert len(image)==18
    return image

# ---------- F9 and PGL2(9) ----------
# a+bu, u^2=2
F=[(a,b) for a in range(3) for b in range(3)]
def add(x,y):return ((x[0]+y[0])%3,(x[1]+y[1])%3)
def neg(x):return ((-x[0])%3,(-x[1])%3)
def sub(x,y):return add(x,neg(y))
def mul(x,y):return ((x[0]*y[0]+2*x[1]*y[1])%3,(x[0]*y[1]+x[1]*y[0])%3)
def inv(x):
    if x==(0,0):raise ZeroDivisionError
    for y in F:
        if mul(x,y)==(1,0):return y
    raise AssertionError
def div(x,y):return mul(x,inv(y))
INF=None
P=F+[INF]
def mob(M,z):
    a,b,c,d=M
    if z is INF:
        if c==(0,0):return INF
        return div(a,c)
    num=add(mul(a,z),b);den=add(mul(c,z),d)
    return INF if den==(0,0) else div(num,den)
def canon_matrix(M):
    for z in M:
        if z!=(0,0):
            u=inv(z);return tuple(mul(u,x) for x in M)
def pgl():
    mats=set()
    for a,b,c,d in itertools.product(F,repeat=4):
        if sub(mul(a,d),mul(b,c))==(0,0):continue
        mats.add(canon_matrix((a,b,c,d)))
    assert len(mats)==720
    perms=set()
    for M in mats:
        pm=tuple(P.index(mob(M,z)) for z in P)
        perms.add(pm)
    assert len(perms)==720
    return perms
def quotient_action():
    G=pgl()
    j=tuple(P.index(INF if z is INF else neg(z)) for z in P)
    assert order(j)==2
    C=[g for g in G if compose(g,j)==compose(j,g)];assert len(C)==16
    unseen=set(range(10));orbs=[]
    while unseen:
        x=min(unseen);O={x,j[x]};orbs.append(tuple(sorted(O)));unseen-=O
    orbs=sorted(orbs,key=lambda z:(len(z),z))
    assert sorted(map(len,orbs))==[1,1,2,2,2,2]
    oi={x:i for i,O in enumerate(orbs) for x in O}
    image=set()
    for g in C:
        image.add(tuple(oi[g[O[0]]] for O in orbs))
    assert len(image)==8
    return image,orbs

def profile(G):
    return {
      "order":len(G),
      "element_orders":dict(sorted(Counter(order(g) for g in G).items())),
      "fixed_points":dict(sorted(Counter(sum(g[i]==i for i in range(len(g))) for g in G).items())),
      "order_fixed":{f"{a},{b}":n for (a,b),n in sorted(Counter((order(g),sum(g[i]==i for i in range(len(g)))) for g in G).items())}
    }
def orbits(G,n):
    unseen=set(range(n));out=[]
    while unseen:
        x=min(unseen);O={g[x] for g in G};out.append(sorted(O));unseen-=O
    return sorted(out,key=lambda z:(len(z),z))

def main():
    A=local_action();B,qorbs=quotient_action()
    pa,pb=profile(A),profile(B)
    oa,ob=orbits(A,6),orbits(B,6)
    assert list(map(len,oa))==[6]
    assert list(map(len,ob))==[2,4]
    assert pa["element_orders"]=={1:1,2:3,3:8,6:6}
    assert pa["fixed_points"]=={0:13,3:4,6:1}
    assert pb["element_orders"]=={1:1,2:5,4:2}
    assert pb["fixed_points"]=={0:2,2:5,6:1}
    out={
      "schema":"w33.20260828.six-state-character-nogo.v1","status":"PASS",
      "near_ovoid_local_action":{"group_image":"C3 x S3","profile":pa,"orbits":oa,"transitive":True},
      "P1F9_split_involution_quotient":{"centralizer":"D16 in PGL(2,9)","quotient_image":"D8","profile":pb,
                                        "j_orbit_sizes":sorted(map(len,qorbs)),"orbits":ob,"transitive":False},
      "invariants_separating_actions":["image order 18 vs 8","transitive 6 vs orbits 2+4",
                                      "order-3 and order-6 elements exist only on near-ovoid side",
                                      "permutation fixed-point characters differ"],
      "equivariant_bijection_exists":False,
      "parallel_HJ10_weight_obstruction":"Pass10917-10924 is stronger when canonical HJ fibre weights are retained: fixed weights 1,3 and moving-pair weights 2,3,3,6 obstruct D16/C4 already.",
      "theorem":"The six completions of a W33 optimal defect dipole and the six split-involution orbits of P1(F9) are not isomorphic permutation G-sets under their canonical local symmetry actions. The former is a transitive C3xS3 action; the latter is an intransitive D8 action with orbit sizes 2+4.",
      "boundary":"A bare set bijection exists because both sets have six elements. This theorem rules out the canonical equivariant identification; it does not rule out a new bridge after deliberately forgetting or replacing the local symmetry."
    }
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","near_image":18,"p1_image":8,"equivariant":False}))

if __name__=="__main__":main()
