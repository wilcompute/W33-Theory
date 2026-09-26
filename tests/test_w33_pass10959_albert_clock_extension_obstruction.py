import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis/w33_pass10959_albert_clock_extension_obstruction.py"
CERT = ROOT / "data/w33_pass10959_albert_clock_extension_obstruction.json"
JOUT = ROOT / "data/w33_pass10959_doubled_albert_gl23_intertwiner.json"


def load():
    return json.loads(CERT.read_text(encoding="utf-8"))


def test_producer_replays():
    subprocess.run(
        [sys.executable, str(PRODUCER)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert load()["status"] == "PASS_16D_NOGO_AND_MINIMAL_32D_GL23_COMPLETION"
def test_character_restriction_law():
    g = load()["gap_character_restriction"]
    assert g["group"] == "GL(2,3)"
    assert g["order"] == 48
    assert g["clock_order"] == 8
    assert g["irrep_degrees"] == [1,1,2,2,2,3,3,4]
    assert [x["exponents"] for x in g["center_minus_irreps"]] == [
        [1,3], [5,7], [1,3,5,7]
    ]
    assert "m1=m3 and m5=m7" in g["central_minus_restriction_law"]


def test_single_albert_16_is_obstructed():
    n = load()["dimension16_no_go"]
    assert n["central_minus_degree16_combinations"] == 25
    assert n["all_exhausted"] is True
    assert n["target_15_extension_exists"] is False
    assert n["target_37_extension_exists"] is False
    assert "m1=m3 and m5=m7" in n["obstruction"]
def test_minimal_completion_is_32():
    m = load()["minimal_completion"]
    assert m["dimension"] == 32
    assert m["extra_dimension"] == 16
    assert m["combined_C8_multiplicities"] == {
        "1": 8, "3": 8, "5": 8, "7": 8
    }
    assert "8 copies" in m["realization"]
    assert m["faithful"] is True


def test_exact_32d_extension():
    e = load()["explicit_32D_extension"]
    assert e["field"] == "Q(zeta8)=Q(i,sqrt(2))"
    assert e["intertwiner_rank"] == 32
    assert e["clock_intertwining_exact"] is True
    assert e["center_maps_to"] == "-I32"
    assert "transport" in e["homomorphism_reason"]
def test_intertwiner_certificate_shape_and_relation():
    d = json.loads(JOUT.read_text(encoding="utf-8"))
    assert d["field"] == "Q(zeta8)=Q(i,sqrt(2))"
    assert d["formula"] == "J = S32 T32^-1"
    assert len(d["intertwiner_J"]) == 32
    assert all(len(row) == 32 for row in d["intertwiner_J"])
    assert d["relation"] == "G_A J = J R32(g)"
    assert len(d["sha256"]) == 64


def test_gap_script_is_frozen():
    p = ROOT / "analysis/w33_pass10959_gl23_character_restriction.g"
    text = p.read_text(encoding="utf-8")
    assert "irrG:=Irr(G)" in text
    assert "RestrictedClassFunction" in text
    assert "ScalarProduct" in text
def test_visible_surfaces_are_unique():
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    tail = (ROOT / "analysis/W33_SHARED_FRONTIER_TAIL.tex").read_text(
        encoding="utf-8"
    )
    assert docs.count('id="pass10959-albert-clock-extension"') == 1
    assert tail.count(
        "PASS10959_ALBERT_CLOCK_EXTENSION_OBSTRUCTION_INSERT}%"
    ) == 1
