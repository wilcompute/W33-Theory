#!/usr/bin/env python3
"""BT574/BT607/BT610: LaTeX sanity verifier for W33 preprint inserts.

This is a lightweight repository-local verifier.  It does not require a TeX
installation; it checks the structural conditions that the symmetry/phase,
cubic-leakage, Ihara-shadow, master-evolution, and cubic-lock-reviewer inserts
should satisfy before a full compile:

  * the active preprint exists,
  * the symmetry/phase/cubic-leakage section is present exactly once,
  * theorem/proof/display environments introduced by the patch are balanced,
  * local \input files referenced by the managed insert pipeline exist,
  * the BT588/BT589/BT597/BT601/BT606 snippets are visible either directly in
    the section or through its managed \input files.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "paper" / "w33_preprint.tex"
BASE_REQUIRED_INPUTS = [
    ROOT / "paper" / "sections" / "sec_stdmodel_full.tex",
    ROOT / "paper" / "sections" / "sec_complement_duality.tex",
    ROOT / "paper" / "sections" / "sec_quantum_dark.tex",
]
MANAGED_INSERT_INPUTS = [
    ROOT / "paper" / "sections" / "sec_bt588_raw_cubic_leakage_ratios.tex",
    ROOT / "paper" / "sections" / "sec_bt589_levi_vs_fiber_homology.tex",
    ROOT / "paper" / "sections" / "sec_bt597_cubic_leakage_ihara_shadow.tex",
    ROOT / "paper" / "sections" / "sec_bt601_master_evolution_axiom.tex",
    ROOT / "paper" / "sections" / "sec_bt606_cubic_lock_reviewer_lemma.tex",
]
REQUIRED_INPUT_LINES = [
    r"\input{sections/sec_bt588_raw_cubic_leakage_ratios}",
    r"\input{sections/sec_bt589_levi_vs_fiber_homology}",
    r"\input{sections/sec_bt597_cubic_leakage_ihara_shadow}",
    r"\input{sections/sec_bt601_master_evolution_axiom}",
    r"\input{sections/sec_bt606_cubic_lock_reviewer_lemma}",
]
SECTION_LABEL = r"\label{sec:symmetry-phase-cubic-leakage}"
SECTION_TITLE = r"\section{Symmetry, Phase, and Cubic Leakage}"
REQUIRED_SNIPPETS = [
    # BT572/BT574 base section snippets.
    r"\operatorname{Aut}_{\rm flag}=\mathrm{PSp}(4,3)",
    r"51840=2\cdot25920",
    r"+1:25920",
    r"-1:25920",
    r"\frac{244}{121}",
    r"P_{E_0+E_4}(A)",
    r"G=\frac{1}{81}CC^T=\frac{160}{81}E_4",
    # BT588/BT589 insert snippets.
    r"Raw Cubic Leakage Ratios",
    r"Levi Homology versus Phase-Cover Fiber Homology",
    r"\beta_1(L)=81",
    r"\beta_1^{\rm fiber}=12960",
    # BT597/BT601 insert snippets.
    r"Cubic leakage as an Ihara shadow",
    r"\frac{M_5/M_3}{(k-1)^2}",
    r"244=v\Phi_6-\chi q^2",
    r"Master Evolution Axiom",
    r"Physical evolution on the protected W33 cycle frame",
    r"Hodge projection of Ihara/nonbacktracking propagation",
    # BT606 insert snippets.
    r"Reviewer Lemma: why the cubic lock is $M_5/M_3$",
    r"M_1=0",
    r"\frac{M_3}{6}=160",
    r"M_5=234240",
    r"\text{cubic leakage}=\text{normalized }M_5/M_3",
]
SUPPORTED_PATCH_MACROS = {
    "operatorname", "rm", "mathrm", "mathbb", "cdot", "qquad", "sqrt",
    "frac", "sum", "lambda", "Phi", "chi", "boxed", "text", "textbf",
    "left", "right", "begin", "end", "label", "section", "subsection",
    "item", "beta", "leadsto", "longmapsto", "mapsto", "to", "neq", "in",
    "operatorname", "Tr", "rm", "mid", "times", "quad", "dots",
}


def count_token(s: str, token: str) -> int:
    return s.count(token)


def check_balanced(content: str, env: str) -> bool:
    return count_token(content, rf"\begin{{{env}}}") == count_token(content, rf"\end{{{env}}}")


def extract_new_section(content: str) -> str:
    start = content.index(SECTION_TITLE)
    next_section = content.find("\n\section", start + len(SECTION_TITLE))
    return content[start:] if next_section == -1 else content[start:next_section]


def path_for_input(input_name: str) -> Path:
    normalized = input_name.strip()
    if normalized.endswith(".tex"):
        rel = normalized
    else:
        rel = normalized + ".tex"
    return ROOT / "paper" / rel


def verification_scope(section_text: str) -> tuple[str, list[str]]:
    """Return section text plus contents of section-local managed inputs."""
    chunks = [section_text]
    loaded = []
    for input_name in re.findall(r"\\input\{([^}]+)\}", section_text):
        path = path_for_input(input_name)
        if path.exists() and path in MANAGED_INSERT_INPUTS:
            chunks.append(path.read_text(encoding="utf-8"))
            loaded.append(str(path.relative_to(ROOT)))
    return "\n".join(chunks), loaded


def main() -> None:
    content = TEX.read_text(encoding="utf-8")
    new_section = extract_new_section(content)
    scope, loaded_managed_inputs = verification_scope(new_section)
    command_names = set(re.findall(r"\\([A-Za-z]+)", scope))
    unknown_patch_commands = sorted(command_names - SUPPORTED_PATCH_MACROS)
    all_required_inputs = BASE_REQUIRED_INPUTS + MANAGED_INSERT_INPUTS
    checks = {
        "preprint_exists": TEX.exists(),
        "section_title_once": content.count(SECTION_TITLE) == 1,
        "section_label_once": content.count(SECTION_LABEL) == 1,
        "section_before_uniqueness": content.index(SECTION_TITLE) < content.index(r"\section{The TOE Singularity Theorem}"),
        "theorem_environment_balanced": check_balanced(scope, "theorem"),
        "proof_environment_balanced": check_balanced(scope, "proof"),
        "quote_environment_balanced": check_balanced(scope, "quote"),
        "display_math_balanced": scope.count(r"\[") == scope.count(r"\]"),
        "required_inputs_exist": all(p.exists() for p in all_required_inputs),
        "managed_input_lines_present": all(s in content for s in REQUIRED_INPUT_LINES),
        "managed_inputs_loaded": sorted(loaded_managed_inputs) == sorted(str(p.relative_to(ROOT)) for p in MANAGED_INSERT_INPUTS if p.exists()),
        "required_snippets_present": all(s in scope for s in REQUIRED_SNIPPETS),
        "no_unknown_patch_commands": unknown_patch_commands == [],
        "document_ends": content.rstrip().endswith(r"\end{document}"),
    }
    result = {
        "bt": 610,
        "title": "LaTeX sanity verifier for W33 preprint insert pipeline",
        "target": str(TEX.relative_to(ROOT)),
        "new_section_label": "sec:symmetry-phase-cubic-leakage",
        "required_inputs": [str(p.relative_to(ROOT)) for p in all_required_inputs],
        "required_input_lines": REQUIRED_INPUT_LINES,
        "managed_inputs_loaded": loaded_managed_inputs,
        "unknown_patch_commands": unknown_patch_commands,
        "checks": checks,
        "all_identities_hold": all(checks.values()),
        "interpretation": "The W33 manuscript insert pipeline is structurally present and LaTeX-sane under static checks; full PDF compilation remains a separate environment-dependent check.",
    }
    out = ROOT / "data" / "PART_BT610_LATEX_SANITY_VERIFIER_results.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
