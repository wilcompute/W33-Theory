from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "bt3320_integrator", ROOT / "tools/integrate_bt3320_bt3331.py"
)
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def test_wrapper_insertion_is_idempotent() -> None:
    wrapper = (
        "\\AtBeginDocument{%\n"
        "  \\renewcommand{\\tableofcontents}{%\n"
        "    OLD\n"
        "  }%\n"
        "}\n"
        "\\input{body.tex}\n"
    )
    insert = "\\section{X}\n\\label{sec:global-cover-quantum-hypercube}\n"
    first, mode = MOD.integrate_tex(wrapper, insert)
    assert mode == "wrapper_input"
    assert first.count(MOD.TEX_INPUT) == 1
    second, mode = MOD.integrate_tex(first, insert)
    assert mode == "already_present"
    assert second == first


def test_monolithic_insertion_is_idempotent() -> None:
    paper = "\\documentclass{article}\n\\begin{document}\nA\n\\end{document}\n"
    insert = "\\section{X}\n\\label{sec:global-cover-quantum-hypercube}\n"
    first, mode = MOD.integrate_tex(paper, insert)
    assert mode == "monolithic_insert"
    assert first.count(MOD.TEX_LABEL) == 1
    second, mode = MOD.integrate_tex(first, insert)
    assert mode == "already_present"
    assert second == first


def test_html_insertion_is_idempotent() -> None:
    page = "<html><main>A</main></html>"
    insert = '<section id="bt3320-3331-global-cover-quantum-hypercube">X</section>'
    first, mode = MOD.integrate_html(page, insert)
    assert mode == "html_insert"
    assert first.count(MOD.HTML_ID) == 1
    second, mode = MOD.integrate_html(first, insert)
    assert mode == "already_present"
    assert second == first


def test_live_tex_front_doors_reference_packet_once() -> None:
    for name in MOD.TARGETS:
        text = (ROOT / name).read_text(encoding="utf-8")
        assert text.count(MOD.TEX_INPUT) == 1
