import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"analysis/bt3528_3534_borel_star_moore_functor_transplant.py"

def load():
    spec=importlib.util.spec_from_file_location("packet3528",SOURCE)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test_exact_packet():
    mod=load()
    result=mod.build_certificate()
    assert result["status"]=="PASS_7_FRONTS"
    assert result["semantic_sha256"]=="1ec126887cd1f09b8cdc074872567dd4962c2a399c1b14db8b035a8ea50dc591"
    borel=result["front_3528_perkel_borel_restriction"]
    assert borel["fixed_dimensions"]=={"C19":2,"C9":2,"C3":8,"Borel_19:9":0}
    assert borel["full_permutation_rational_decomposition"]=="Q^57 = 1 + 3*V18 + V2"
    star=result["front_3529_star_complement_firewall"]
    assert star["independent_candidate_census"]["spectral_survivors"]==3720
    assert star["largest_clique"]==31 < star["required_clique"]==38
    moore=result["front_3530_m57_dual_tracks"]
    assert moore["only_admissible_fibre_sizes"]==[1,2,6,56]
    functor=result["front_3531_typed_quotient_reconstruct"]
    assert functor["uniform_fibre_functor_equivalence"] is False
    audit=result["front_3532_spectral_transplant_audit"]
    assert audit["hits"]==34
    factor=result["front_3534_bonkers_factorization_curvature"]
    assert factor["M57_involutive_branch"]["edges_covered_once_per_pencil"]==1540
