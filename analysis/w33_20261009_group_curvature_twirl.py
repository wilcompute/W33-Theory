"""Full PSp(4,3) symmetry averaging kills each adjacent current curvature.

For each orbit type (shared point or shared line), locate an actual
group element swapping the two incidence edges. Since U_g J_e U_g^-1
= J_ge, this maps C_ef=i[J_e,J_f] to -C_ef.
Thus full-group twirling of C_ef is zero, without using antiunitarity.
"""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import bt1688_exact_h1_character_irreducibility as h
def main():
    pts=h.make_points();lines=h.w33_lines(pts)
    gp=h.projective_group(pts)
    li={tuple(z):i for i,z in enumerate(lines)}
    edges=[(p,i) for i,line in enumerate(lines) for p in line]
    assert len(gp)==25920 and len(edges)==160
    p0=[(j,e) for j,e in enumerate(edges) if e[0]==edges[0][0] and e!=edges[0]][0]
    l0=[(j,e) for j,e in enumerate(edges) if e[1]==edges[0][1] and e!=edges[0]][0]
    examples={}
    for kind,(j,f) in [('shared_point',p0),('shared_line',l0)]:
        e=edges[0]
        a,b=(e[0],e[1]),f
        swap=None
        for g in gp:
            img={old:li[tuple(sorted(g[p] for p in line))] for old,line in enumerate(lines)}
            if (g[a[0]],img[a[1]])==b and (g[b[0]],img[b[1]])==a:
                swap=g;break
        assert swap is not None
        examples[kind]=dict(current_indices=[0,j],incidences=[list(a),list(b)],
            permutation=list(swap),mapped_pair='reversed',T_odd_not_needed=True)
    orbit_sizes={}
    for kind,(j,f) in [('shared_point',p0),('shared_line',l0)]:
        e=edges[0]
        orbit=set()
        for g in gp:
            lidx={old:li[tuple(sorted(g[p] for p in line))] for old,line in enumerate(lines)}
            mapped=tuple(sorted(((g[e[0]],lidx[e[1]]),(g[f[0]],lidx[f[1]]))))
            orbit.add(mapped)
        orbit_sizes[kind]=len(orbit)
        assert len(orbit)==240,(kind,len(orbit))
    dist=json.loads((ROOT/'data/PART_BT1688_EXACT_H1_CHARACTER_IRREDUCIBILITY_results.json').read_text())
    assert dist['character_square_sum']==25920
    return dict(status='PASS',projective_group_size=len(gp),
        point_line_preserving_current_orbits=2,adjacent_current_pairs=480,adjacent_pair_orbit_sizes=orbit_sizes,
        edge_swap_witnesses=examples,
        theorem='Every adjacent pair lies in one of two PSp(4,3) orbits. A reversing symmetry exists for a representative in each, hence group twirl of each Hermitian curvature i[J_e,J_f] is identically zero as an operator.',
        scope='A G-invariant ground/thermal state has zero curvature expectation; non-G-invariant states can have nonzero curvature. Does not classify true ground-state multiplicity or spontaneous symmetry breaking.')
if __name__=='__main__':
    r=main()
    (ROOT/'data/w33_20261009_group_curvature_twirl.json').write_text(json.dumps(r,indent=2)+'\n')
    print('PASS orbit swaps',list(r['edge_swap_witnesses']))
