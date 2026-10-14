"""Native W33 octagon association scheme and 6 irreducible symmetry sectors."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe78_octagon_bose_mesner import certificate

def test_exact_symmetric_six_class_orbital_algebra():
    c=certificate()
    assert c["status"]=="PASS_TOE78_W33_OCTAGON_6_SECTOR_ASSOCIATION_SCHEME"
    assert c["rank_of_commutative_orbital_adjacency_algebra"]==6
    assert c["all_five_orbital_matrices_pairwise_commute_exactly"]
    assert c["undirected_pair_orbital_valencies"]==[2,4,4,8,8]
    assert c["multiplicity_free_27_representation_dimensions"]==[1,4,4,6,6,6]
    assert c["H27_center_trivial_isotypic_total_dimension"]==9
    assert c["nontrivial_H27_center_isotypic_total_dimension"]==18
    assert c["GQ_27_line_spectrum"]=={"10":1,"1":20,"-5":6}
    assert sum(r["dimension"] for r in c["six_irreducible_symmetry_sector_controls"] if r["GQ24_cubic_surface_eigenvalue"]==-5)==6
