"""Replay optimal Clifford linear compiler across all GL(3,3)."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_ccz_sum_optimal as O
def test_full_linear_group_dijkstra():
    x=O.verify()
    assert x["all_invertible_matrices_checked"]==11232
    assert x["target_minimum_SUM_cost"]==4
    assert x["full_chiral_clock_compiler"]=={
        "local_qutrit_fourier":6,"SUM":8,"CCZ":1,
        "formula":"U=F P_L^dag CCZ P_L F^dag with P_L and inverse each 4 SUM"}
    assert sum(x["cost_census"].values())==11232
if __name__=="__main__":
    test_full_linear_group_dijkstra()
    print("PASS exact GL3(F3) 11232-map minimal SUM cost")
