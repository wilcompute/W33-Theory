from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VERIFIER = load(
    ROOT / "analysis/bt3363_minimum_gauge_defect_generation.py", "bt3363_verifier"
)
INTEGRATOR = load(
    ROOT / "tools/integrate_bt3363_minimum_gauge_defect.py", "bt3363_integrator"
)


def test_certificate_matches_frozen_result() -> None:
    observed = VERIFIER.certificate()
    frozen = json.loads(
        (ROOT / "data/PART_BT3363_MINIMUM_GAUGE_DEFECT_GENERATION_results.json").read_text(
            encoding="utf-8"
        )
    )
    assert observed == frozen
    assert observed["global"]["C3_5_flat_rank"] == 2400
    assert observed["global"]["cohomology_rank"] == 2180


def test_minimum_vectors_span_local_flat_plane() -> None:
    vectors = VERIFIER.certificate()["local"]["minimum_vectors"]
    assert VERIFIER.rank_mod3(vectors) == 2
    assert all(sum(row) % 3 == 0 for row in vectors)
    assert all(sum(x != 0 for x in row) == 2 for row in vectors)


def test_wrapper_integrator_is_idempotent() -> None:
    wrapper = (
        "\\AtBeginDocument{%\n"
        "  \\renewcommand{\\tableofcontents}{%\n"
        "    OLD\n"
        "  }%\n"
        "}\n"
        "\\input{body.tex}\n"
    )
    first = INTEGRATOR.integrate_tex(wrapper)
    second = INTEGRATOR.integrate_tex(first)
    assert first == second
    assert first.count(INTEGRATOR.TEX_INPUT) == 1


def test_live_front_doors_reference_bt3363_once() -> None:
    for name in INTEGRATOR.TARGETS:
        text = (ROOT / name).read_text(encoding="utf-8")
        assert text.count(INTEGRATOR.TEX_INPUT) == 1
