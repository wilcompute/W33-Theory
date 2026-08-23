#!/usr/bin/env python3
"""Pass7509-7516: the 9-sheet common S4 is the affine direction quotient.

Input: the two 9-point restricted permutations obtained from the hash-pinned
ATLAS Monster maximal-subgroup generators in Pass7501-7508.
Output: an exact AG(2,3) affine-plane reconstruction and the quotient
AGL(2,3)/(3^2:2) = PGL(2,3) = S4 acting on the four parallel classes.
"""
from collections import Counter, deque
import json
from pathlib import Path

G1=(0,2,4,5,3,7,1,8,6)
G2=(1,3,0,6,7,2,4,5,8)
OUT=Path('data/PART_W33_PASS7509_7516_MONSTER_HESSE_DIRECTION_COUPLING.json')

def comp(a,b): return tuple(a[b[i]] for i in range(len(a)))
def inv(a):
    z=[0]*len(a)
    for i,j in enumerate(a): z[j]=i
    return tuple(z)
def closure(gs):
    e=tuple(range(len(gs[0]))); S={e}; q=deque([e])
    while q:
        a=q.popleft()
        for b in gs:
            c=comp(b,a)
            if c not in S: S.add(c); q.append(c)
    return S
def order(a):
    e=tuple(range(len(a))); x=e
    for n in range(1,100):
        x=comp(a,x)
        if x==e:return n
    raise RuntimeError

def main():
    G=closure([G1,G2]); assert len(G)==432
    e=tuple(range(9))
    c3=[g for g in G if order(g)==3 and all(g[i]!=i for i in range(9))]
    T=None
    for a in c3:
        for b in c3:
            if a==b or comp(a,b)!=comp(b,a): continue
            H=closure([a,b])
            if len(H)==9 and len({h[0] for h in H})==9:
                if all(comp(comp(s,t),inv(s)) in H for s in [G1,G2] for t in H):
                    T=H;break
        if T is not None: break
    assert T is not None
    dirs=[]
    for t in T:
        if t==e: continue
        H=frozenset(closure([t]))
        if H not in dirs: dirs.append(H)
    assert len(dirs)==4 and all(len(D)==3 for D in dirs)
    didx={D:i for i,D in enumerate(dirs)}
    def dperm(s):
        si=inv(s)
        return tuple(didx[frozenset(comp(comp(s,t),si) for t in D)] for D in dirs)
    Dimg={dperm(s) for s in G}
    assert len(Dimg)==24
    assert Counter(order(x) for x in Dimg)==Counter({1:1,2:9,3:8,4:6})
    kernel=[s for s in G if dperm(s)==tuple(range(4))]
    assert len(kernel)==18 and T.issubset(set(kernel))
    classes=[]; all_lines=[]
    for D in dirs:
        unseen=set(range(9)); cls=[]
        while unseen:
            x=min(unseen); L=frozenset(t[x] for t in D)
            assert len(L)==3; cls.append(L); unseen-=L
        assert len(cls)==3 and set().union(*cls)==set(range(9))
        classes.append(cls); all_lines.extend(cls)
    assert len(set(all_lines))==12
    pair_count=Counter(); point_count=Counter()
    for L in all_lines:
        for x in L: point_count[x]+=1
        A=sorted(L)
        for i in range(3):
            for j in range(i+1,3): pair_count[(A[i],A[j])]+=1
    assert set(pair_count.values())=={1} and len(pair_count)==36
    assert set(point_count.values())=={4}
    line_set=set(all_lines)
    assert all(frozenset(s[x] for x in L) in line_set for s in G for L in all_lines)
    out={
      'schema':'w33.pass7509_7516.monster_hesse_direction_coupling.v1','status':'PASS',
      'input':{'source':'Pass7501-7508 restriction of hash-pinned ATLAS Monster H generators','degree':9,'group_order':432},
      'translation_socle':{'order':9,'structure':'C3^2','regular':True},
      'affine_plane':{'points':9,'lines':12,'line_size':3,'lines_through_point':4,'parallel_classes':4,'lines_per_parallel_class':3,'object':'AG(2,3) / Hesse (9_4,12_3) incidence'},
      'direction_action':{'image_order':24,'element_order_census':dict(sorted(Counter(order(x) for x in Dimg).items())),'identification':'S4 = PGL(2,3)','kernel_order':18,'kernel_structure':'3^2:2','meaning':'the four S4 letters are the four affine directions / parallel classes'},
      'monster_coupling':'The common S4 in (3^2:2 x O8+(3)).S4 couples the four AG(2,3) direction classes to the D4(3) outer/triality coordinate on the 3360-sheet.',
      'claim_boundary':'Exact finite permutation geometry; no physical identification follows.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
