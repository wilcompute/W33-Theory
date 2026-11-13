"""Reproduce/validate exact compact E6, Fermat sixer, clock and MUB packets.
Run: python tests/test_toe_20261113_e6_fermat_clock_full.py
Producers write their scoped deterministic JSON certificates.
"""
import json,sys
from pathlib import Path
from fractions import Fraction
from collections import Counter
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
import toe_20261113_e6_c4_translation_holography as C
import toe_20261113_albert_six_coordinate_sections as S
import toe_20261113_fermat_cubic_h27_sixers as F
import toe_20261113_e6_biaxial_address_compatibility_erratum as E
import toe_20261113_chiral_e6_cubic_compatibility as corrected

def test_36_packets_and_projection():
    cert,terms,D,mapi,roots=R.load()
    keys,Ks=R.pack_roots(roots)
    assert len(Ks)==36 and len(keys)==36
    edges={(i,j) for k in keys for i,j,v in k}
    assert len(edges)==216 and len(set(edges))==216
    assert all(np.array_equal(K@K@K,-K) for K in Ks)
    null={(i,j) for i in range(27) for j in range(i+1,27) if D[i,j]}
    assert len(null)==108
    overlap=[sum(int(D[i,j])*v for i,j,v in key) for key in keys]
    assert sum(a*a for a in overlap)==46
    assert Fraction(sum(a*a for a in overlap),3)==Fraction(46,3)
    assert Counter(sum((i,j) in null for i,j,v in k) for k in keys)==Counter({0:12,2:18,3:6})

def test_root_packet_finite_cubic_preservation():
    _,terms,D,mapi,roots=R.load()
    keys,Ks=R.pack_roots(roots)
    chosen=next(k for k in Ks if len({(i,j) for i,j in zip(*np.triu_indices(27,1)) if k[i,j] and D[i,j]})==3)
    R.inf_check(chosen,terms)
    V,control=R.cubic_finite(chosen,terms)
    assert control["45_monomials_exactly_preserved"]
    assert control["order_three"]
    assert np.max(abs(V@V@V-np.eye(27)))<1e-12

def test_all_729_torus_points_exact():
    cert,*_=R.load()
    x=R.torus(cert)
    assert x["torus_3_torsion_points_checked"]==729
    assert x["spectral_multiplicity_census"]["15,6,6"]==72
    assert "19,4,4" not in x["spectral_multiplicity_census"]

def test_compact_C4_and_translation_full_rank():
    x=C.main()
    assert x["lie_type"]["root_system"]=="C4"
    assert x["lie_type"]["full_exact_integer_charpoly_match"]
    assert x["translation"]["modular_ranks"]=={"101":36,"103":36}
    assert x["translation"]["rational_kernel_dimension"]==0
    assert x["clock_frontier"]["proven_minimum_new_edges_for_any_nonzero_compatible_skew_generator"]==3
    assert Counter((z["new_edges"],z["choi_perfect_3by3_cuts"]) for z in x["clock_frontier"]["all_root_clock_candidates"])==Counter({(3,4):6,(4,2):18,(6,8):12})

def test_72_sections():
    x=S.main()
    assert x["number_of_maximal_six_coordinate_sections"]==72
    assert x["maximal_clique_sizes"]=={"5":216,"6":72}
    assert x["unordered_b_fibre_composition"]=={"(0, 3, 3)":18,"(2, 2, 2)":54}

def test_fermat_648_automorphisms_two_orbits():
    x=F.main()
    assert x["fermat_linear_automorphism_group_order"]==648
    assert x["sixer_orbit_sizes"]==[18,54]
    assert x["canonical_E6_45_triple_graph_isomorphic"] and x["iso_preserves_three_b_sectors"]

def test_corrected_biaxial_source():
    x=E.main()
    y=corrected.run()
    assert x["first_seven_corrected_cubic_numerators"]==[z["signed_norm_of_9Ue_cubed"] for z in y["nonzero_examples"][:7]]
    assert y["nonzero_examples"][1]["signed_norm_of_9Ue_cubed"]==28
    assert y["nonzero_examples"][1]["input_history"]==[0,1,2]
    assert x["corrected_test_still_disproves_cubic_preservation"]

def test_independent_mub_bitset_timeout_is_not_unsat():
    x=json.loads((ROOT/"data/toe_20261113_fivequbit_two_s3_classes_bitset_search.json").read_text())
    assert x["two_S3_orbit_representatives"]==[692,694]
    assert x["status"]=="undecided"
    assert all(z["status"]=="undecided" and z["timeout"] for z in x["states"])
    assert sum(z["nodes"] for z in x["states"])>=10000000
    assert all(z["lowest_uncovered_count_seen"]>=1 for z in x["states"])

if __name__=="__main__":
    tests=[v for k,v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for t in tests:
        t()
        print("PASS",t.__name__,flush=True)
    print("PASS",len(tests),"/",len(tests),flush=True)
