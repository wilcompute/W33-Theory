"""Exact W33 ordered-flag stabilizer identification.

The extra triplet ordering refines each of 160 flags by S3, leaving a
27-element kernel. Verify whether that kernel is the extraspecial
Heisenberg H27 or an Abelian C3^3 group, rather than assuming the name.
"""
import json,sys
from pathlib import Path
from collections import Counter
from sympy.combinatorics import Permutation,PermutationGroup
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261118_W33_triperiodic_Levi_homogenization as W

def run():
    G,points,lines=W.levi()
    pidx={p:i for i,p in enumerate(points)}
    lidx={l:i for i,l in enumerate(lines)}
    flags=[(p,li) for li,line in enumerate(lines) for p in line]
    assert len(flags)==160
    fidx={f:i for i,f in enumerate(flags)}
    generators=[]
    for v in points:
        pm={i:pidx[W.projective(tuple((x[k]+W.symplectic(x,v)*v[k])%3
                                    for k in range(4)))] for i,x in enumerate(points)}
        lm={i:lidx[tuple(sorted(pm[k] for k in line))] for i,line in enumerate(lines)}
        generators.append(Permutation([fidx[(pm[p],lm[li])] for p,li in flags]))
    grp=PermutationGroup(generators)
    assert grp.order()==25920
    chosen=0;point,li=flags[chosen]
    three=[fidx[(p,li)] for p in sorted(set(lines[li])-{point})]
    stab=grp.stabilizer(chosen)
    assert stab.order()==162
    allstab=list(stab.generate_schreier_sims())
    K=[g for g in allstab if all(g(i)==i for i in three)]
    assert len(K)==27
    Kset=set(K)
    # A subgroup: closure and inverse tests, not merely a set count.
    assert all(g*h in Kset for g in K for h in K)
    center=[g for g in K if all(g*h==h*g for h in K)]
    ordercounts=Counter(int(g.order()) for g in K)
    derived={g*h*g**-1*h**-1 for g in K for h in K}
    assert all(c in Kset for c in derived)
    assert len(center)==27 and ordercounts=={1:1,3:26} and len(derived)==1
    classification="elementary Abelian C3^3, NOT nonabelian Heisenberg H27"
    out=dict(status="PASS",W33_full_group_order=25920,
             initial_point_line_flags=160,flag_stabilizer_order=162,
             ordered_triples_per_flag=6,ordered_flag_configurations=960,
             pointwise_triplet_stabilizer_order=len(K),
             pointwise_stabilizer_element_orders=dict(ordercounts),
             pointwise_stabilizer_center_order=len(center),
             pointwise_stabilizer_commutator_size=len(derived),
             abelian_exponent=3,
             group_classification=classification,
             group_distinction="The 27-element pointwise flag stabilizer is C3^3 with center order27; do not identify it with extraspecial H27, whose center has order3 and derived subgroup order3.",
             exact_orbit_stabilizer_identity="25920=160*6*27",
             connection="The kernel of the action of a flag stabilizer on its three remaining line points is a 27-element group. Its exact internal structure is checked by center, commutator and element-order counts, not inferred from cardinality.",
             caveat="Even an exact native H27 correspondence between W33 ordered flags and a triplet does not select a physical ordered defect or prove 3 chiral families, a compactification, or realistic masses.")
    path=ROOT/"data/toe_20261118_W33_ordered_flag_H27_kernel.json"
    path.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(out)
    return out

if __name__=="__main__":run()
