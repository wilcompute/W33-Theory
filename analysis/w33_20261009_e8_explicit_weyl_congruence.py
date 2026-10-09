"""Explicit E8 Weyl/lattice witness for benchmark 1 versus W33 Z6II_34 1558.

The allowed *gauge* matching is rigorous after selecting generators
(-V,-W2,+W3). Whether their sign inversions are physically admissible
space-group automorphisms is a separate geometric question.
"""
from pathlib import Path
import json,sys
import sympy as S
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_e8_colored_root_isomorphism as iso
import w33_20261009_heterotic_benchmark_full_roots as B
import w33_20261008_heterotic_benchmark_shift_screen as screen
def wmat(permutation):
    roots=[S.Matrix(1,8,list(x)) for x in B.ROOTS]
    chosen=[]
    for i,r in enumerate(roots):
        if S.Matrix.vstack(*(chosen+[r])).rank()>len(chosen):chosen.append(r);chosen_idx=locals().get('chosen_idx',[])+[i]
        if len(chosen)==8:break
    R=S.Matrix.vstack(*chosen)
    R2=S.Matrix.vstack(*[roots[permutation[i]] for i in chosen_idx])
    W=R.inv()*R2
    assert W*W.T==S.eye(8)
    assert all(roots[i]*W==roots[permutation[i]] for i in range(240))
    return W
def certify():
    graph=iso.graph()
    candidate='Z6II_34__SM_20260917_1558'
    rows=B.source_model(B.SCAN/(candidate+'.model'))
    mine=[tuple(-x for x in rows[0]),tuple(-x for x in rows[7]),rows[4]]
    data=B.BENCH['model1']
    target=[B.vector(B.BENCH_V),B.vector(data['W2']),B.vector(data['W3'])]
    witnesses=[]
    for side in (0,8):
        u,v=iso.encode_color_sets(iso.colours(mine,side),iso.colours(target,side))
        ok,p,_=graph.isomorphic_vf2(graph,color1=u,color2=v,return_mapping_12=True)
        assert ok and sorted(p)==list(range(240))
        W=wmat(p)
        congruences=[]
        for left,right in zip(mine,target):
            lhs=S.Matrix([S.Rational(str(x)) for x in left[side:side+8]])
            rhs=S.Matrix([S.Rational(str(x)) for x in right[side:side+8]])
            delta=lhs-W*rhs
            delta_tuple=tuple(screen.F(str(x)) for x in delta)
            assert screen.e8_lattice(delta_tuple)
            congruences.append([str(x) for x in delta])
        witnesses.append(dict(E8_factor=side//8,
             mapped_root_index_permutation=p,
             orthogonal_weyl_matrix=[[str(W[i,j]) for j in range(8)] for i in range(8)],
             benchmark_to_candidate_lattice_offsets=congruences))
    return dict(status='PASS',candidate=candidate,benchmark='Lebedev et al 0708.2691 model1',
        generator_transform='(-V,-W2,+W3)',gauge_isometry=2,
        root_graph='240 E8 roots, dot product 1 edges, all 240 maps checked and E8 lattice offsets certified',
        witnesses=witnesses,
        physical_boundary='Fixed generator transform candidate only; must prove inversion(s) lift to a genuine Z6-II space-group equivalence and compare spectrum/vacuum.')
if __name__=='__main__':
    x=certify()
    (ROOT/'data/w33_20261009_e8_explicit_weyl_congruence.json').write_text(json.dumps(x,indent=2)+'\n')
    print('PASS factors',len(x['witnesses']))
    for w in x['witnesses']:
        print('factor',w['E8_factor'],'Weyl',w['orthogonal_weyl_matrix'],'shift',w['benchmark_to_candidate_lattice_offsets'])
