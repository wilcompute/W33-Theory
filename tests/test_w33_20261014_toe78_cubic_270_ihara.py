"""TOE78 regression for actual 27-octagon cubic-SRG Ramanujan and 270 cycles."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe78_cubic_270_ihara import certificate
def test_27_native_cubic_ramanujan_and_270_oriented_prime_triangles():
    c=certificate()
    assert c["status"]=="PASS_TOE78_W33_NATIVE_GQ27_IHARA_270_PRIME_TRIANGLE_INSTRUCTIONS"
    assert c["vertices_edges_degree"]==[27,135,10]
    assert c["strongly_regular_parameters"]==[27,10,1,5]
    assert c["adjacency_spectrum_multiplicities"]=={"10":1,"1":20,"-5":6}
    assert c["Ramanujan_regular_degree_10"]
    assert c["undirected_primitive_three_cycles"]==45
    assert c["based_oriented_length3_prime_nonbacktracking_geodesics"]==270
    assert c["E8_external_phase_labelled_cubic_supports"]==270
    assert all(c0["difference"]<2e-10 for c0 in c["independent_Bass_numerical_checks"])
