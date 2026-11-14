"""Exact quaternionic flag fibration in the E6 Pauli attractor."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261114_quaternionic_flag_HP3_attractor_fibration as F

def test_flag_to_projective_rank_and_stu_kernel():
    r=F.main()
    assert r["status"].startswith("PASS_EXACT")
    assert r["generic_quaternionic_flag_orbit_dimension"]==24
    assert r["balanced_top_eigenline_orbit_dimension"]==12
    assert r["exact_fiber_image_rank"]==12
    assert r["kernel_decomposition"].startswith("14 = 12")

if __name__=="__main__":
    test_flag_to_projective_rank_and_stu_kernel()
    print("PASS 1/1",flush=True)
