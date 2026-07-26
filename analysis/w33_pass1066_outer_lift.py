from __future__ import annotations
import json, time
from pathlib import Path
from collections import Counter
from sympy.combinatorics import Permutation, PermutationGroup
from w33_pass1060_1064_core import *
from w33_pass1060_minimal_signed_cover import lift_signs, signed_perm
from w33_pass1061_springer_embedding_decision import arbitrary_actions

GENERATOR_POINT_INDICES = [0, 1, 4, 5, 13]


def elemkey(g, n=40):
    return tuple(int(g(i)) for i in range(n))


def greedy_gens(G):
    chosen=[]; H=PermutationGroup([Permutation(list(range(40)))])
    for g in G.generators:
        K=PermutationGroup(chosen+[g])
        if K.order()>H.order(): chosen.append(g); H=K
        if H.order()==G.order(): break
    return chosen


def conjugacy_orbit(seed, gens):
    invs=[g**-1 for g in gens]
    orb={seed}; stack=[seed]
    while stack:
        x=stack.pop()
        for g,gi in zip(gens,invs):
            y=gi*x*g
            if y not in orb:
                orb.add(y); stack.append(y)
    return orb


def cycles(g, n):
    out=Counter(len(c) for c in g.cyclic_form)
    out[1]+=n-sum(k*v for k,v in out.items())
    return dict(sorted(out.items()))


def main():
    w=build_w33(); q=build_quot(w); a=build_axes(w,q); e=build_e8(); F=isometry(q,e)
    reps=[e.positive[F[c]] for c in a.coords]

    inner_axis=[a.axis_gens[i] for i in GENERATOR_POINT_INDICES]
    inner_signed=[signed_perm(p,lift_signs(p,reps)) for p in inner_axis]
    L=PermutationGroup(inner_signed)
    neg=Permutation([2*i+(b^1) for i in range(120) for b in (0,1)])
    ident=Permutation(list(range(240)))
    assert L.order()==51840 and L.contains(neg)

    G=w.G
    sim=matrix_perm(w,[[1,0,0,0],[0,2,0,0],[0,0,1,0],[0,0,0,2]])
    pgens=greedy_gens(G); pinvs=[g**-1 for g in pgens]
    outer=[h*sim for h in G.generate_schreier_sims()]
    involutions=set(t for t in outer if t.order()==2)
    unvisited=set(involutions); classes=[]
    while unvisited:
        t=next(iter(unvisited)); orb={t}; stack=[t]; unvisited.remove(t)
        while stack:
            x=stack.pop()
            for g,gi in zip(pgens,pinvs):
                y=gi*x*g
                if y not in orb:
                    orb.add(y); unvisited.discard(y); stack.append(y)
        classes.append(orb)
    classes=sorted(classes,key=len)
    assert [len(c) for c in classes]==[36,540]

    records={}; lifted={}; extensions={}
    for orb in classes:
        n=len(orb); t=min(orb,key=elemkey)
        _,ap=arbitrary_actions(w,q,a,t)
        T=signed_perm(ap,lift_signs(ap,reps))
        E=PermutationGroup(inner_signed+[T])
        sorb=conjugacy_orbit(T,inner_signed)
        H=G.subgroup_search(lambda x:x*t==t*x)
        rec={
            'unsigned_class_size':n,
            'inner_centralizer_order':int(H.order()),
            'lift_order':int(T.order()),
            'lift_square':'identity' if T*T==ident else ('global_negation' if T*T==neg else 'other'),
            'signed_cycle_profile':cycles(T,240),
            'signed_conjugacy_class_size_under_Sp43':len(sorb),
            'negative_lift_in_same_signed_class':neg*T in sorb,
            'extension_order':int(E.order()),
            'extension_center_order':int(E.center().order()),
            'extension_derived_order':int(E.derived_subgroup().order()),
            'normalizes_signed_cover':all(L.contains((T**-1)*g*T) for g in inner_signed),
            'fixed_signed_roots':sum(T(i)==i for i in range(240)),
            'representative_point_images':elemkey(t),
        }
        records[str(n)]=rec; lifted[n]=T; extensions[n]=E

    E36,E540=extensions[36],extensions[540]
    T36,T540=lifted[36],lifted[540]
    same_extension=(E36.order()==E540.order()==103680 and E36.contains(T540) and E540.contains(T36))
    split_section=(T540.order()==2 and T540 not in L and E540.order()==2*L.order())

    checks={
        'signed_cover_order_51840':L.order()==51840,
        'unsigned_outer_involution_classes_are_36_and_540':[len(c) for c in classes]==[36,540],
        'class36_lifts_have_order4_and_square_to_center':T36.order()==4 and T36*T36==neg,
        'class540_lifts_are_involutions':T540.order()==2 and T540*T540==ident,
        'both_lifts_normalize_signed_cover':records['36']['normalizes_signed_cover'] and records['540']['normalizes_signed_cover'],
        'both_generate_order103680_extension':E36.order()==E540.order()==103680,
        'both_generate_the_same_extension':same_extension,
        'extension_center_is_global_C2':E540.center().order()==2 and E540.center().contains(neg),
        'extension_derived_subgroup_is_Sp43':E540.derived_subgroup().order()==51840,
        'extension_splits_over_outer_C2_via_540_lift':split_section,
        'class36_signed_preimage_is_72_order4_elements':records['36']['signed_conjugacy_class_size_under_Sp43']==72 and records['36']['negative_lift_in_same_signed_class'],
        'class540_signed_preimage_is_1080_involutions':records['540']['signed_conjugacy_class_size_under_Sp43']==1080 and records['540']['negative_lift_in_same_signed_class'],
        'class36_has_no_fixed_roots':records['36']['fixed_signed_roots']==0,
        'class540_has_eight_fixed_roots':records['540']['fixed_signed_roots']==8,
    }
    assert all(checks.values()),checks

    return {
      'schema':'w33.pass1066.outer_lift.v1','status':'PASS',
      'headline':'The outer W(E6) involution lifts to a split order-103680 extension Sp(4,3) semidirect C2, but its two unsigned outer-involution classes lift differently: the 36-class becomes order 4 with square equal to global root negation, while the 540-class has genuine involutory lifts.',
      'signed_cover_order':51840,
      'full_extension_order':103680,
      'abstract_extension':'Sp(4,3) semidirect C2 (split over the outer quotient, witnessed by a 540-class involutory lift)',
      'outer_class_lifts':records,
      'structural_decision':{
        'globally_split':True,
        'splitting_witness':'any signed lift of a 540-class outer involution',
        'localized_pin_like_behavior':'the 36-class has no involutory lift; both preimages have order 4 and square to the central antipode',
        'same_group_from_either_class':same_extension,
      },
      'check_count':len(checks),'checks':checks,
      'scope':'Exact signed permutations on the 240 E8 roots. The result fingerprints the explicit extension without assigning an unverified ATLAS suffix to the double cover.'
    }

if __name__=='__main__':
    started=time.time(); result=main()
    output=Path(__file__).resolve().parents[1]/'data'/'w33_pass1066_outer_lift.json'
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'check_count':result['check_count'],'seconds':round(time.time()-started,3),'output':str(output)},indent=2))
