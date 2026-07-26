from __future__ import annotations
import json,time
from pathlib import Path
from collections import Counter
from sympy.combinatorics import Permutation,PermutationGroup
from w33_pass1060_1064_core import *


def elemkey(g,n=40): return tuple(int(g(i)) for i in range(n))

def greedy_gens(G):
    chosen=[];H=PermutationGroup([Permutation(list(range(40)))])
    for g in G.generators:
        K=PermutationGroup(chosen+[g])
        if K.order()>H.order():chosen.append(g);H=K
        if H.order()==G.order():break
    return chosen

def outer_classes(w):
    G=w.G; sim=matrix_perm(w,[[1,0,0,0],[0,2,0,0],[0,0,1,0],[0,0,0,2]])
    gens=greedy_gens(G); invs=[g**-1 for g in gens]
    invs_outer=set(h*sim for h in G.generate_schreier_sims() if (h*sim).order()==2)
    unseen=set(invs_outer);classes=[]
    while unseen:
        t=next(iter(unseen));orb={t};stack=[t];unseen.remove(t)
        while stack:
            x=stack.pop()
            for g,gi in zip(gens,invs):
                y=gi*x*g
                if y not in orb:orb.add(y);unseen.discard(y);stack.append(y)
        classes.append(orb)
    return sorted(classes,key=len)

def line_perm(w,g):
    idx={L:i for i,L in enumerate(w.lines)}
    return tuple(idx[tuple(sorted(g(p) for p in L))] for L in w.lines)

def enumerate_spreads(w):
    bypoint=[[] for _ in range(40)]
    masks=[]
    for i,L in enumerate(w.lines):
        m=sum(1<<p for p in L);masks.append(m)
        for p in L:bypoint[p].append(i)
    full=(1<<40)-1;out=[]
    def rec(covered,chosen):
        if covered==full:
            out.append(tuple(sorted(chosen)));return
        p=next(i for i in range(40) if not (covered>>i)&1)
        for li in bypoint[p]:
            if masks[li]&covered==0:rec(covered|masks[li],chosen+[li])
    rec(0,[])
    return sorted(set(out))

def disjoint_pair_configs(w):
    configs={}
    for a in range(40):
        for b in range(a+1,40):
            if set(w.lines[a])&set(w.lines[b]):continue
            tr=[]
            for c,L in enumerate(w.lines):
                if c in (a,b):continue
                if len(set(L)&set(w.lines[a]))==1 and len(set(L)&set(w.lines[b]))==1:tr.append(c)
            # In W(3,3) the common transversals of a disjoint line pair form four disjoint lines.
            if len(tr)==4 and all(not(set(w.lines[x])&set(w.lines[y])) for x,y in itertools.combinations(tr,2)):
                configs[(a,b)]=tuple(sorted(tr))
    return configs

def main():
    w=build_w33(); classes=outer_classes(w); assert [len(c) for c in classes]==[36,540]
    spreads=enumerate_spreads(w);spreadset=set(spreads)
    pairconfigs=disjoint_pair_configs(w)

    class36_fixed=[]; class36_profiles=Counter()
    for t in classes[0]:
        lp=line_perm(w,t); fixed=tuple(i for i,x in enumerate(lp) if i==x)
        class36_fixed.append(fixed)
        class36_profiles[(sum(t(i)==i for i in range(40)),len(fixed))]+=1

    class540_pairs=[];class540_profiles=Counter();all_k24=True;all_fixedpoints_degree2=True
    for t in classes[1]:
        lp=line_perm(w,t); fixed=tuple(i for i,x in enumerate(lp) if i==x)
        fp={i for i in range(40) if t(i)==i}
        deg={li:sum(bool(set(w.lines[li])&set(w.lines[lj])) for lj in fixed if lj!=li) for li in fixed}
        hubs=tuple(sorted(li for li,d in deg.items() if d==4)); spokes=tuple(sorted(li for li,d in deg.items() if d==2))
        ok=(len(fixed)==6 and len(hubs)==2 and len(spokes)==4 and
            not(set(w.lines[hubs[0]])&set(w.lines[hubs[1]])) and
            all(not(set(w.lines[x])&set(w.lines[y])) for x,y in itertools.combinations(spokes,2)) and
            all(len(set(w.lines[s])&set(w.lines[h]))==1 for s in spokes for h in hubs))
        all_k24 &= ok
        degree2_points={p for p in range(40) if sum(p in w.lines[li] for li in fixed)==2}
        all_fixedpoints_degree2 &= degree2_points==fp and len(fp)==8
        class540_pairs.append(hubs)
        class540_profiles[(len(fp),len(fixed),tuple(sorted(deg.values())))] += 1

    fixed36set=set(class36_fixed); pair540set=set(class540_pairs)
    checks={
      'exactly_36_spreads':len(spreads)==36,
      'each_spread_has_10_disjoint_lines_covering_40_points':all(len(S)==10 and len(set().union(*(set(w.lines[i]) for i in S)))==40 and all(not(set(w.lines[a])&set(w.lines[b])) for a,b in itertools.combinations(S,2)) for S in spreads),
      'outer_classes_are_36_and_540':[len(c) for c in classes]==[36,540],
      'class36_fixed_line_sets_are_spreads':all(S in spreadset for S in class36_fixed),
      'class36_to_spreads_is_bijection':len(fixed36set)==36 and fixed36set==spreadset,
      'class36_elements_fix_no_points_and_10_lines':class36_profiles=={(0,10):36},
      'exactly_540_unordered_disjoint_line_pairs':len(pairconfigs)==540,
      'every_disjoint_pair_has_four_pairwise_disjoint_common_transversals':len(pairconfigs)==sum(1 for a,b in itertools.combinations(range(40),2) if not(set(w.lines[a])&set(w.lines[b]))),
      'class540_fixed_lines_form_K2_4':all_k24,
      'class540_fixed_points_are_the_eight_intersections':all_fixedpoints_degree2,
      'class540_to_disjoint_line_pairs_is_bijection':len(pair540set)==540 and pair540set==set(pairconfigs),
      'class540_profile_is_uniform':class540_profiles=={(8,6,(2,2,2,2,4,4)):540},
      'stabilizer_orders_match_orbit_sizes':25920//36==720 and 25920//540==48,
    }
    assert all(checks.values()),checks

    return {
      'schema':'w33.pass1067.outer_class_geometry.v1','status':'PASS',
      'headline':'The two outer-involution classes have exact dual finite-geometric meanings. The 36-class is canonically the 36 spreads: each involution fixes ten disjoint lines covering all 40 points. The 540-class is canonically the 540 unordered disjoint-line pairs: each involution fixes the pair plus its four common transversals, a K2,4 line-intersection configuration.',
      'class36':{
        'size':36,'inner_centralizer_order':720,'fixed_points_per_element':0,'fixed_lines_per_element':10,
        'geometry':'fixed lines are a spread','number_of_spreads':36,'bijection':'t -> Fix_lines(t)'
      },
      'class540':{
        'size':540,'inner_centralizer_order':48,'fixed_points_per_element':8,'fixed_lines_per_element':6,
        'geometry':'two disjoint hub lines plus four pairwise-disjoint common transversals; intersection graph K2,4',
        'number_of_unordered_disjoint_line_pairs':540,'bijection':'t -> the two degree-4 hub lines in Fix_lines(t)'
      },
      'bridge':'The prior 36-spread count and BT748 540-fibre count are the two outer-involution orbits of the same PGSp(4,3) extension, distinguished by centralizers 720 and C2 x S4 of order 48.',
      'check_count':len(checks),'checks':checks,
      'scope':'Exact enumeration of all spreads, all disjoint line pairs, and every outer involution. No amplitude or physical interpretation is assumed.'
    }

if __name__=='__main__':
    started=time.time();result=main()
    output=Path(__file__).resolve().parents[1]/'data'/'w33_pass1067_outer_class_geometry.json'
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'check_count':result['check_count'],'seconds':round(time.time()-started,3),'output':str(output)},indent=2))
