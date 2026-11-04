from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis"/"2026_11_03_optimal_5load_apartment_hamiltonian.py"
spec=importlib.util.spec_from_file_location("five_load",SRC)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def test_exact_optimal_load_and_GF2_spanning():
    c=mod.verify()
    assert c["status"].startswith("PASS_EXACT")
    assert c["flags"]==160 and c["apartments_all"]==1620
    assert c["apartments_selected"]==81
    assert c["GF2_independent"] and c["Q_independent"]
    assert c["max_flag_load"]==5
    assert sum(int(k)*v for k,v in c["load_histogram"].items())==648

def test_local_H_protects_cycle_space_but_splits_band():
    c=mod.verify()
    assert c["boundary_zero"]
    assert c["A_H_equals_minus2_H"]
    assert c["H_non_scalar_in_H1"]
    assert c["H_max_offdiagonal_neighbors"]<=35
    assert c["H_numerical_active_eigenvalue_range"][0]>0
