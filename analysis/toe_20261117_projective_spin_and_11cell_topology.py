"""Spin-lift and locally-projective topology checks relevant to 11D use.

Reuses the preceding exact Witting action and BT839 incidence counts.
Distinguishes face-number alternating sums from order-complex Euler numbers.
"""
import json
from collections import deque
from pathlib import Path

import numpy as np
import sympy as sp

from toe_20261117_witting_CP3_invariant_modes import generators, modular
from bt839_gc_operation_euler_flag_audit import BASE, OPERATIONS, totals


def spin_lifts():
    prime = 7
    matrices = [modular(u, prime=prime, root=2) for u in generators()]
    identity = np.eye(4, dtype=np.int64)
    key = lambda m: tuple(int(x) for x in m.flat)
    seen, queue = {key(identity)}, deque([identity])
    while queue:
        current = queue.popleft()
        for generator in matrices:
            following = generator@current % prime
            label = key(following)
            if label not in seen:
                seen.add(label)
                queue.append(following)
    scalars = [a for a in range(1, prime) if key(a*identity % prime) in seen]
    assert len(seen) == 51840 and scalars == [1, 6]
    # Exact upper bound: the preceding ray-action computation has25920
    # projective elements. Scalar SU4 matrices lying in Q(omega) are only +/-I.
    # Reduction has51840 distinct matrices, so both bounds coincide.
    assert len(seen)//len(scalars) == 25920
    cone = []
    for n in range(2, 13):
        # Spin(2) lifts are +/-exp(pi i/n). The nth powers are
        # -1 and (-1)^(n+1), respectively.
        powers = (-1, (-1)**(n+1))
        cone.append(dict(order=n, lift_nth_powers=list(powers),
                         honest_cyclic_spin_lifts=sum(x == 1 for x in powers)))
    assert [r['honest_cyclic_spin_lifts'] for r in cone] == [0, 1]*5+[0]
    return dict(mod7_SU4_closure_order=len(seen), scalar_kernel=['+I', '-I'],
                projective_order=25920,
                Witting_CP3_spin_lift=True,
                global_reason='CP3 has K^(1/2)=O(-2). The SU4 lifts have scalar kernel +/-I, '
                  'which acts trivially on O(-2). Their equivariant spin bundle descends.',
                S5_mirror_spin_obstruction=True,
                S5_reason='A projective transposition rotates one real normal plane by pi. '
                  'Both Spin lifts square to-1, so no order2 lift exists at the generic mirror.',
                cone_controls=cone,
                caveat='Spin compatibility does not resolve the branch singularities or provide their localized dynamics.')


def flag_topology():
    # Incidence counts come from the actual local facets, not an assumption
    # that every facet boundary is S2. Pair ordering is01,02,03,12,13,23.
    data = {
        '11_cell': dict(pair_counts=[110, 165, 66, 165, 165, 110], flags=660,
                        projective_facets=11, projective_vertex_links=11),
        '57_cell': dict(pair_counts=[342, 855, 570, 855, 855, 342], flags=3420,
                        projective_facets=57, projective_vertex_links=57),
        'tomotope_partial_b': dict(pair_counts=[24, 48, 28, 48, 48, 32], flags=192,
                                  projective_facets=4, projective_vertex_links=4)}
    rows = {}
    for name, item in data.items():
        face_vector = totals(BASE[name]['rank_classes'])
        naive = sum((-1)**i*x for i, x in enumerate(face_vector))
        flag_vector = [sum(face_vector), sum(item['pair_counts']), 2*item['flags'], item['flags']]
        euler = sum((-1)**i*x for i, x in enumerate(flag_vector))
        # A cone on RP2 attaches with relative Euler1-1=0, not1-2=-1.
        assert euler == naive+item['projective_facets']
        singular = item['projective_facets']+item['projective_vertex_links']
        assert singular == 2*euler
        omni = totals(OPERATIONS[name]['omnitruncated'])
        if name != 'tomotope_partial_b':
            assert flag_vector == omni[::-1]
        rows[name] = dict(face_numbers=face_vector, face_number_alternating_sum=naive,
                          order_complex_f_vector=flag_vector, order_complex_Euler=euler,
                          RP2_link_singular_vertices=singular, omnitruncated_table_counts=omni,
                          omnitruncated_face_number_alternating_sum=sum((-1)**i*x for i, x in enumerate(omni)),
                          flags=item['flags'])
    assert [rows[k]['order_complex_Euler'] for k in data] == [11, 57, 4]
    return dict(objects=rows,
                topology='The order complexes are3-dimensional. RP2 links obstruct ordinary '
                    '3-manifold neighborhoods and orientability of the regular part adjacent to those links.',
                correction='The BT839 sums0 and-11/-57/-4 are face-table arithmetic, not the '
                    'topological Euler characteristic of a regular CW decomposition with ball cells.',
                tomotope_correction='The tomotope itself is an abstract uniform4-polytope, Aut order96, '
                    '192 flags. Its monodromy group order18432 fails the intersection property; '
                    'that failure does not make the tomotope a non-polytope.',
                dimensions='11 cells do not determine11 spacetime dimensions; a smooth spin '
                    'internal geometry and a dynamical action are additional requirements.')


if __name__ == '__main__':
    result = dict(status='PASS', spin=spin_lifts(), locally_projective_topology=flag_topology())
    output = Path(__file__).resolve().parents[1]/'data/toe_20261117_projective_spin_and_11cell_topology.json'
    output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(status=result['status'], SU4_group=result['spin']['mod7_SU4_closure_order'],
                          euler={k:v['order_complex_Euler'] for k,v in result['locally_projective_topology']['objects'].items()})))
