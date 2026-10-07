import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location("p11614",ROOT/"analysis/w33_pass11614_hesse_coxeter_discriminant.py")
M=importlib.util.module_from_spec(S);S.loader.exec_module(M)
R=M.result()

def test_discriminant():
    assert R["coxeter"]["order"]==24
    assert R["coxeter"]["positive_root_count"]==6
    assert "det(g)" in R["coxeter"]["anti_invariant"]

def test_chambers():
    V=R["vacuum_chambers"]
    assert V["orbit_size"]==V["distinct_root_signatures"]==24
    assert V["W_sign_multiplicities"]=={"+":12,"-":12}
    assert V["normalized_W"]=="15/343"

def test_wall_graph():
    G=R["wall_graph"]
    assert (G["vertices"],G["edges"],G["degree"])==(24,36,3)
    assert G["bipartition"]==[12,12]
    assert (G["square_faces"],G["hexagonal_faces"],G["euler"])==(6,8,2)

def test_cubic_discriminant():
    assert R["discriminant"]["roots"]=="x^2,y^2,z^2"
    assert "W^2" in R["discriminant"]["identity"]
