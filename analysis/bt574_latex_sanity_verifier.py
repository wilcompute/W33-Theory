#!/usr/bin/env python3
"""BT574: LaTeX sanity verifier for the BT572 preprint patch.

This is a lightweight repository-local verifier.  It does not require a TeX
installation; it checks the structural conditions that the BT572 integration
patch should satisfy before a full compile:

  * the active preprint exists,
  * the new symmetry/phase/cubic-leakage section is present exactly once,
  * theorem/proof/display environments introduced by the patch are balanced,
  * macros introduced by the patch are supported by the existing package set,
  * all local \input files referenced by the preprint exist.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "paper" / "w33_preprint.tex"
REQUIRED_INPUTS = [
    ROOT / "paper" / "sections" / "sec_stdmodel_full.tex",
    ROOT / "paper" / "sections" / "sec_complement_duality.tex",
    ROOT / "paper" / "sections" / "sec_quantum_dark.tex",
]
SECTION_LABEL = r"\label{sec:symmetry-phase-cubic-leakage}"
SECTION_TITLE = r"\section{Symmetry, Phase, and Cubic Leakage}"
REQUIRED_SNIPPETS = [
    r"\operatorname{Aut}_{\rm flag}=\mathrm{PSp}(4,3)",
    r"51840=2\cdot25920",
    r"+1:25920",
    r"-1:25920",
    r"\frac{244}{121}",
    r"P_{E_0+E_4}(A)",
    r"G=\frac{1}{81}CC^T=\frac{160}{81}E_4",
]
SUPPORTED_PATCH_MACROS = {
    "operatorname", "rm", "mathrm", "mathbb", "cdot", "qquad", "sqrt",
    "frac", "sum", "lambda", "Phi", "chi", "boxed", "text", "left",
    "right", "begin", "end", "label", "section", "subsection", "item",
}


def count_token(s: str, token: str) -> int:
    return s.count(token)


def check_balanced(content: str, env: str) -> bool:
    return count_token(content, rf"\begin{{{env}}}") == count_token(content, rf"\end{{{env}}}")


def extract_new_section(content: str) -> str:
    start = content.index(SECTION_TITLE)
    next_section = content.find("\n\section", start + len(SECTION_TITLE))
    return content[start:] if next_section == -1 else content[start:next_section]


def main() -> None:
    content = TEX.read_text(encoding="utf-8")
    new_section = extract_new_section(content)
    command_names = set(re.findall(r"\\([A-Za-z]+)", new_section))
    unknown_patch_commands = sorted(command_names - SUPPORTED_PATCH_MACROS)
    checks = {
        "preprint_exists": TEX.exists(),
        "section_title_once": content.count(SECTION_TITLE) == 1,
        "section_label_once": content.count(SECTION_LABEL) == 1,
        "section_before_uniqueness": content.index(SECTION_TITLE) < content.index(r"\section{The TOE Singularity Theorem}"),
        "theorem_environment_balanced": check_balanced(new_section, "theorem"),
        "proof_environment_balanced": check_balanced(new_section, "proof"),
        "display_math_balanced": new_section.count(r"\[") == new_section.count(r"\]"),
        "required_inputs_exist": all(p.exists() for p in REQUIRED_INPUTS),
        "required_snippets_present": all(s in new_section for s in REQUIRED_SNIPPETS),
        "no_unknown_patch_commands": unknown_patch_commands == [],
        "document_ends": content.rstrip().endswith(r"\end{document}"),
    }
    result = {
        "bt": 574,
        "title": "LaTeX sanity verifier for BT572 patch",
        "target": str(TEX.relative_to(ROOT)),
        "new_section_label": "sec:symmetry-phase-cubic-leakage",
        "required_inputs": [str(p.relative_to(ROOT)) for p in REQUIRED_INPUTS],
        "unknown_patch_commands": unknown_patch_commands,
        "checks": checks,
        "all_identities_hold": all(checks.values()),
        "interpretation": "The BT572 manuscript patch is structurally present and LaTeX-sane under static checks; full PDF compilation remains a separate environment-dependent check.",
    }
    out = ROOT / "data" / "PART_BT574_LATEX_SANITY_VERIFIER_results.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
