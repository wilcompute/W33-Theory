from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
from functools import lru_cache

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass1330_1334_modular_triality_cycle_atlas.py"


def load_module():
    spec = importlib.util.spec_from_file_location("pass1330_1334", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def payload():
    return load_module().main(write=False)


def test_radical_classification():
    records = payload()["pass1330_modular_jacobson_radicals"]["records"]
    assert records["2"]["jacobson_radical_dimension"] == 21
    assert records["2"]["loewy_power_dimensions"] == [21,17,13,7,2,0]
    assert records["3"]["jacobson_radical_dimension"] == 22
    assert records["3"]["loewy_power_dimensions"] == [22,16,10,4,0]
    assert records["5"]["jacobson_radical_dimension"] == 6
    assert records["5"]["loewy_power_dimensions"] == [6,2,0]


def test_semisimple_quotients():
    records = payload()["pass1330_modular_jacobson_radicals"]["records"]
    assert records["2"]["semisimple_quotient"] == "M_2(F_2) + F_2"
    assert records["3"]["semisimple_quotient"] == "F_3^4"
    assert records["5"]["semisimple_quotient"] == "M_3(F_5) + M_2(F_5) + F_5^7"


def test_nine_axis_scheme():
    scheme = payload()["pass1331_nine_axis_triality_scheme"]
    assert scheme["relation_valencies"] == [1,2,2,4]
    assert scheme["primitive_idempotent_ranks"] == [1,2,2,4]
    assert scheme["coordinate_swap_fusion"]["relation_valencies"] == [1,4,4]


def test_literal_cycles():
    cycles = payload()["pass1332_selected_cycle_representatives"]["cycles"]
    assert cycles["7"]["dihedral_stabilizer_order"] == 2
    assert cycles["7"]["dihedral_orbit_size"] == 25920
    assert cycles["7"]["support_set_stabilizer_order"] == 12
    assert cycles["7"]["support_chord_count"] == 5
    assert cycles["8"]["dihedral_stabilizer_order"] == 1
    assert cycles["8"]["dihedral_orbit_size"] == 51840


def test_copy_selector_boundary():
    record = payload()["pass1332_selected_cycle_representatives"]
    assert record["species20_copy_idempotent_orbit_size"] == 3
    assert record["combined_W_E6_times_S3"]["length7_cycle_plus_copy_orbit"] == 77760
    assert record["combined_W_E6_times_S3"]["length8_cycle_plus_copy_orbit"] == 155520


def test_json_certificate_matches_execution():
    frozen = json.loads((ROOT / "data" / "w33_pass1330_1334_modular_triality_cycle_atlas.json").read_text(encoding="utf-8"))
    assert frozen == payload()


def test_central_blocks_are_executably_reconstructed():
    records = payload()["pass1330_modular_jacobson_radicals"]["records"]
    assert records["2"]["central_block_dimensions"] == [4, 22]
    assert records["3"]["central_block_dimensions"] == [1, 25]
    assert records["5"]["central_block_dimensions"] == [1, 1, 1, 1, 4, 9, 9]
    assert records["2"]["primitive_central_idempotent_count"] == 2
    assert records["3"]["primitive_central_idempotent_count"] == 2
    assert records["5"]["primitive_central_idempotent_count"] == 7


def test_gap_atlasrep_certificate():
    certificate = json.loads(
        (ROOT / "data" / "w33_pass1333_atlasrep_species20.json").read_text(encoding="utf-8")
    )
    assert certificate["status"] == "PASS"
    assert certificate["group_order"] == 51840
    assert [record["image_size"] for record in
            certificate["degree20_representation_records"]] == [51840] * 3
    assert any(
        sorted(record["degree20_multiplicities"]) == [0, 0, 3]
        for record in certificate["tom_432_records"]
    )
    assert any(
        sorted(record["degree20_multiplicities"]) == [0, 0, 1]
        for record in certificate["tom_480_records"]
    )


def test_integrator_is_idempotent(tmp_path):
    insert = ROOT / "analysis" / "BT1330_BT1334_modular_triality_cycle_atlas.tex"
    analysis = tmp_path / "analysis"
    tools = tmp_path / "tools"
    analysis.mkdir(); tools.mkdir()
    shutil.copy(insert, analysis / insert.name)
    shutil.copy(ROOT / "tools" / "integrate_pass1330_1334.py", tools / "integrate_pass1330_1334.py")
    for name in ("w33_paper.tex", "photonic_holonet.tex"):
        (tmp_path / name).write_text("\\documentclass{article}\n\\begin{document}\nX\n\\end{document}\n", encoding="utf-8")
    subprocess.run([sys.executable, str(tools / "integrate_pass1330_1334.py")], cwd=tmp_path, check=True)
    subprocess.run([sys.executable, str(tools / "integrate_pass1330_1334.py")], cwd=tmp_path, check=True)
    for name in ("w33_paper.tex", "photonic_holonet.tex"):
        text = (tmp_path / name).read_text(encoding="utf-8")
        assert text.count(r"\input{analysis/BT1330_BT1334_modular_triality_cycle_atlas}") == 1


def test_insert_compiles_minimally(tmp_path):
    if shutil.which("pdflatex") is None:
        return
    shutil.copy(
        ROOT / "analysis" / "BT1330_BT1334_modular_triality_cycle_atlas.tex",
        tmp_path / "insert.tex",
    )
    (tmp_path / "main.tex").write_text("\\documentclass{article}\n\\begin{document}\n\\input{insert}\n\\end{document}\n", encoding="utf-8")
    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
        cwd=tmp_path,
        check=True,
        stdout=subprocess.DEVNULL,
    )
