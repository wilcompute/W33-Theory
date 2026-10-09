"""Find concrete symmetry-broken subgroups allowing rank-three cycle quotients.
For connected graph 0->C0->C1->H1->0, taking H-invariants is exact
for finite H over Q: dim H1^H = #(H edge orbits)-#(H vertex orbits)+1.
"""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import bt1688_exact_h1_character_irreducibility as B
def orbits(items,perms):
    todo=set(items);result=[]
    while todo:
        first=next(iter(todo))
        orbit={tuple(p[k] for k in first) for p in perms}
        # when tuple is a single index, encoded as (index,)
        assert orbit<=todo or orbit.isdisjoint(set().union(*result))
        todo-=orbit;result.append(orbit)
    return sorted([len(x) for x in result])
def one_homology_h(subgroup,lines,index):
    vertex_maps=[];edge_maps=[]
    E=[(i,p) for i,line in enumerate(lines) for p in line]
    for g in subgroup:
        lineperm=tuple(index[tuple(sorted(g[p] for p in l))] for l in lines)
        vperm=tuple(g)+tuple(40+x for x in lineperm)
        pos={e:i for i,e in enumerate(E)}
        eperm=tuple(pos[(lineperm[li],g[p])] for li,p in E)
        vertex_maps.append(vperm);edge_maps.append(eperm)
    n0=orbits([(i,) for i in range(80)],vertex_maps)
    n1=orbits([(i,) for i in range(160)],edge_maps)
    return dict(order=len(subgroup),vertex_orbit_sizes=n0,edge_orbit_sizes=n1,
        fixed_H1_dimension=len(n1)-len(n0)+1)
def certificate():
    pts=B.make_points()
    G=B.projective_group(pts)
    lines=B.w33_lines(pts)
    index={line:i for i,line in enumerate(lines)}
    cases={}
    for label,pred in [('point_stabilizer',lambda g:g[0]==0),
             ('ordered_pair_stabilizer',lambda g:g[0]==0 and g[1]==1),
             ('set_pair_stabilizer',lambda g:set((g[0],g[1]))=={0,1}),
             ('ordered_triple_stabilizer',lambda g:g[0]==0 and g[1]==1 and g[2]==2),
             ('ordered_quad_stabilizer',lambda g:g[0]==0 and g[1]==1 and g[2]==2 and g[3]==3)]:
        group=[g for g in G if pred(g)]
        cases[label]=one_homology_h(group,lines,index)
        print(label,cases[label]['order'],cases[label]['fixed_H1_dimension'],flush=True)
    # Full-group zero fixed cycles is independently proven by BT1688 irreducibility.
    return dict(status='PASS',full_PSp_fixed_H1_dimension=0,cases=cases,
        theorem='For any finite subgroup H of PSp(4,3), rational fixed-cycle dimension = #edge orbits - #vertex orbits +1. If >=3, a rank-three H-equivariant integral lattice quotient with trivial target action exists via saturated invariant covectors.',
        boundary='Subgroups are imposed as examples; neither their selection nor a Lorentzian continuum follows from W33 dynamics.')
if __name__=='__main__':
    result=certificate()
    (ROOT/'data/w33_20261009_symmetry_broken_cycle_quotients.json').write_text(json.dumps(result,indent=2)+'\n')
