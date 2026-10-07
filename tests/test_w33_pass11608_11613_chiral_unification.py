import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("p11608_13",ROOT/"analysis/w33_pass11608_11613_chiral_unification.py")
M=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(M)


def test_11608_exact_decoupling():
    r=M.pass11608_local_decoupling()
    assert r["status"].startswith("PASS_")
    assert "^16" in r["determinant_factorization"]


def test_11609_shell_selector():
    r=M.pass11609_e8_shell_selector()
    for row in r["vacuum_rows"]:
        assert "gauge_86" in row["zero_blocks"]
        assert len([x for x in row["zero_blocks"] if x.startswith("matter_")])==1


def test_11610_domain_wall_no_go_and_repair():
    r=M.pass11610_domain_wall()
    assert "gapless" in r["no_go"]
    assert "sqrt" in r["repaired_bulk"]
    assert "Gamma_*" in r["native_beta"]
    assert "one normalizable zero mode" in r["zero_modes"]


def test_11611_cp_sign_lock():
    r=M.pass11611_cp_chirality_lock()
    assert all(x["selected_Chi"]==x["J_sign"] for x in r["rows"])
    assert r["dynamic_alignment_11606"]["selected_Chi"]==r["dynamic_alignment_11606"]["CP_sign"]==-1


def test_11612_anti_invariant_ideal():
    r=M.pass11612_portal_ideal()
    assert r["table"][5]["anti_dim"]==0
    assert r["table"][6]["anti_dim"]==1
    for row in r["table"]:
        assert row["anti_dim"]==row["anti_expected_from_degree_minus6"]


def test_11613_anomaly_closure():
    r=M.pass11613_anomaly_closure()
    assert r["total_anomaly"]=="0"
    assert r["total_Weyl_dimension"]==91
    assert "already owned" in r["prior_owner"]
