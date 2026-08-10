#!/usr/bin/env python3
"""Pass 4768 -- the support-12 even-cycle parity and apartment deck classes are parallel characteristic-two invariants, but not the same cohomology object.

Pass4761 gives C_even as the even-weight hyperplane in the cycle space of the
40-vertex W33 line-intersection graph X.  Its missing quotient character is the
all-edge mod-2 cohomology class [1_E]: it evaluates one on every triangle, hence
is nonzero, and is fixed by PGSp.  An edge stabilizer contains endpoint reversers,
so this invariant has no invariant characteristic-zero oriented lift.

Pass4745/4752's apartment deck line has the same characteristic-two/no-rational-lift
phenomenon, but it descends to a different 270-vertex homogeneous PSp base.  The
40-vertex and 270-vertex bases have stabilizers of orders 648 and 96.  Neither
order divides the other, so there is no PSp-equivariant map between the transitive
bases in either direction.  Thus a canonical pullback/pushforward identification
of the two classes is obstructed even though both are abstract trivial F2 lines.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,perm_group,transvection_matrix
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4768_DECK_VS_EVEN_CYCLE_PARITY_BOUNDARY.json'

def main()->int:
    pts,pidx,lines,lidx,_,A,_,apartments,_=build_geometry();A=np.asarray(A,dtype=np.uint8)
    edges=[(i,j) for i,j in itertools.combinations(range(40),2) if A[i,j]];assert len(edges)==240
    # A triangle witnesses that the all-edge F2 cochain is not a coboundary.
    tri=[]
    for C in itertools.combinations(range(40),3):
        if all(A[i,j] for i,j in itertools.combinations(C,2)):tri.append(C)
    assert tri and len(tri)==160  # four choose three in each of 40 point pencils

    cand=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    gens=[];G={tuple(range(40))}
    for p in cand:
        trial=perm_group(gens+[p])
        if len(trial)>len(G):gens.append(p);G=trial
        if len(G)==25920:break
    assert len(G)==25920
    H40=[g for g in G if g[0]==0];assert len(H40)==648
    e0=edges[0];He=[g for g in G if tuple(sorted((g[e0[0]],g[e0[1]])))==e0];assert len(He)==108
    reversers=sum(g[e0[0]]==e0[1] and g[e0[1]]==e0[0] for g in He);assert reversers==54

    p4745=json.loads((ROOT/'data/PART_W33_PASS4745_INVARIANT_H1_CHARACTER.json').read_text(encoding='utf-8'))
    p4752=json.loads((ROOT/'data/PART_W33_PASS4752_DECK_NORMALIZER_TWIST_COMPARISON.json').read_text(encoding='utf-8'))
    assert p4745['characteristic_two_boundary']['H1_Q_PGSp_invariants']==0
    assert p4745['characteristic_two_boundary']['H1_F2_has_PGSp_fixed_deck_line'] is True
    assert p4752['equivariant_projection']['selected_lines_or_residues']==270
    H270=p4752['local_stabilizer']['H_order'];assert H270==96 and 25920//H270==270
    assert 648%96!=0 and 96%648!=0

    out={'pass':4768,
      'support12_parity_class':{'base':'40-vertex W33 line-intersection graph','edges':240,'cycle_dimension':201,'even_cycle_dimension':200,
        'cohomology_representative':'all-edge F2 cochain','nonzero_triangle_witness':True,'PSp_vertex_stabilizer':648,'edge_stabilizer':108,'endpoint_reversers':54,
        'invariant_characteristic_zero_oriented_lift':False},
      'apartment_deck_class':{'descended_base_vertices':270,'PSp_vertex_stabilizer':96,'PGSp_fixed_F2_line':True,'PGSp_invariant_Q_lift':False},
      'equivariant_base_map_test':{'40_to_270':False,'270_to_40':False,'reason':'transitive G-map requires stabilizer inclusion; 648 and 96 are mutually nondivisible'},
      'comparison':{'shared_feature':'nonzero characteristic-two invariant with no invariant rational oriented lift','same_cohomology_object':False,'abstract_1D_F2_module_isomorphism_not_promoted':True},
      'theorem':'The even-cycle parity quotient and the apartment deck line are parallel characteristic-two orientation-collapse invariants, but they live on inequivalent homogeneous bases. Stabilizer orders 648 and 96 forbid any PSp-equivariant base map in either direction, so there is no canonical cohomological identification.',
      'boundary':'Exact obstruction to the natural equivariant pullback/pushforward route. It does not forbid unrelated nonlinear correspondences.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
