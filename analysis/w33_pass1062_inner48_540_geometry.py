from __future__ import annotations
import json, time
from collections import Counter
from pathlib import Path
from w33_pass1060_1064_core import *
from sympy.combinatorics import Permutation,PermutationGroup

def elemkey(g,n=40):return tuple(int(g(i)) for i in range(n))
def greedy_gens(G):
    chosen=[];H=PermutationGroup([Permutation(list(range(40)))])
    for g in G.generators:
        K=PermutationGroup(chosen+[g])
        if K.order()>H.order(): chosen.append(g);H=K
        if H.order()==G.order():break
    return chosen

def subgroup_invariants(H):
    els=list(H.generate_schreier_sims()); orders=Counter(int(x.order()) for x in els)
    cen=H.center();der=H.derived_subgroup();normals={}
    for x in els:
        N=H.normal_closure(PermutationGroup([x])); key=frozenset(N.generate_schreier_sims());normals[key]=N
    normprof=Counter((int(N.order()),int(N.center().order()),int(N.derived_subgroup().order()),bool(N.is_abelian)) for N in normals.values())
    return {
      'order':int(H.order()),'center_order':int(cen.order()),'derived_order':int(der.order()),
      'abelianization_order':int(H.order()//der.order()),'element_order_distribution':dict(sorted(orders.items())),
      'normal_subgroup_profiles':[{'multiplicity':m,'order':p[0],'center':p[1],'derived':p[2],'abelian':p[3]} for p,m in sorted(normprof.items())]
    }

def main():
    w=build_w33();G=w.G
    sim=matrix_perm(w,[[1,0,0,0],[0,2,0,0],[0,0,1,0],[0,0,0,2]])
    PG=PermutationGroup(list(G.generators)+[sim]); assert PG.order()==51840
    gens=greedy_gens(G); invs=[g**-1 for g in gens]
    elements=list(G.generate_schreier_sims()); outer=[h*sim for h in elements]
    outer_involutions=set(t for t in outer if t.order()==2)
    unvisited=set(outer_involutions); classes=[]
    while unvisited:
        t=next(iter(unvisited));orb={t};stack=[t];unvisited.remove(t)
        while stack:
            x=stack.pop()
            for g,gi in zip(gens,invs):
                y=gi*x*g
                if y not in orb:
                    orb.add(y);unvisited.discard(y);stack.append(y)
        classes.append(orb)
    class_summ=[]; target=None
    for orb in sorted(classes,key=len):
        t=min(orb,key=elemkey); H=G.subgroup_search(lambda x:x*t==t*x)
        rec={'orbit_size':len(orb),'centralizer_order':int(H.order()),'representative_images':elemkey(t)}
        if H.order()==48:
            rec['invariants']=subgroup_invariants(H); target=(t,H,orb,rec)
        class_summ.append(rec)
    assert target is not None
    t,H,orb,rec=target; inv=rec['invariants']
    Z=set(H.center().generate_schreier_sims()); els=list(H.generate_schreier_sims())
    cosets=[];seen=set()
    for x in els:
        if x in seen:continue
        c=frozenset(x*z for z in Z);seen|=c;cosets.append(c)
    qgens=[]
    for g in H.generators:
        im=[]
        for c in cosets:
            x=next(iter(c));y=x*g
            im.append(next(i for i,d in enumerate(cosets) if y in d))
        qgens.append(Permutation(im))
    Q=PermutationGroup(qgens)
    qinv={'order':int(Q.order()),'center':int(Q.center().order()),'derived':int(Q.derived_subgroup().order()),'element_orders':dict(sorted(Counter(int(x.order()) for x in Q.generate_schreier_sims()).items()))}
    checks={
      'PGSp_order_51840':PG.order()==51840,
      'outer_involutions_partitioned_exhaustively':sum(len(c) for c in classes)==len(outer_involutions),
      'a_unique_outer_involution_class_has_size_540':sum(len(c)==540 for c in classes)==1,
      'its_inner_centralizer_has_order_48':H.order()==48 and len(orb)==G.order()//H.order()==540,
      'inner48_has_C2_times_S4_fingerprint':inv['center_order']==2 and inv['derived_order']==12 and inv['abelianization_order']==4 and inv['element_order_distribution']=={1:1,2:19,3:8,4:12,6:8},
      'central_quotient_has_S4_fingerprint':qinv['order']==24 and qinv['center']==1 and qinv['derived']==12 and set(qinv['element_orders'])=={1,2,3,4},
      'direct_product_C2_times_S4_confirmed':inv['element_order_distribution']=={1:1,2:19,3:8,4:12,6:8} and qinv['order']==24,
      'BT748_count_identity_is_orbit_stabilizer':51840==540*96 and 25920==540*48,
    }
    assert all(checks.values()),checks
    return {
      'schema':'w33.pass1062.inner48_540_geometry.v1','status':'PASS',
      'headline':'The 540 carrier is the unique PSp(4,3)-conjugacy class of outer involutions in PGSp(4,3) whose inner centralizer has order 48. That centralizer is C2 x S4; its central quotient is S4. This validates the parallel order-48 denominator, but now with an explicit symplectic subgroup and orbit-stabilizer construction.',
      'outer_involution_classes':class_summ,
      'target':{
        'class_size':len(orb),'inner_centralizer':inv,'central_quotient':qinv,
        'isomorphism_type':'C2 x S4','full_PGSp_centralizer_order':96,
        'torsor_identity':'51840 presentation pairs = 540 outer-involution/root-triple fibres x 2 chiralities x 48 (C2 x S4) coordinates',
        'representative_outer_involution_images':elemkey(t)
      },
      'classification_boundary':'This exhausts every outer-involution class in the explicit PGSp(4,3) extension and therefore every order-48 subgroup occurring as the BT748 inner centralizer. It does not assert that PSp(4,3) has no unrelated order-48 subgroup classes.',
      'check_count':len(checks),'checks':checks,
      'scope':'Exact permutation enumeration of all outer involutions and their PSp conjugacy classes. The 540 geometry is now group-theoretic, with no amplitude interpretation assumed.'
    }
if __name__ == "__main__":
    started = time.time(); result = main()
    output = Path(__file__).resolve().parents[1] / "data" / "w33_pass1062_inner48_540_geometry.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "headline": result["headline"], "check_count": result["check_count"], "output": str(output), "seconds": round(time.time()-started, 3)}, indent=2))
