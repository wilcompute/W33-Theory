#!/usr/bin/env python3
"""Passes 2808-2812: migrate and verify the executable Holonet blueprint."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "holonet_machine_blueprint.tex"
INSERT = ROOT / "analysis" / "BT2808_BT2812_blueprint_evidence_insert.tex"
OUT = ROOT / "data" / "PART_BT2808_BT2812_BLUEPRINT_HARDENING_results.json"
INPUT = r"\input{analysis/BT2808_BT2812_blueprint_evidence_insert}"
LEDGER = "% =====================================================================================\n\\section{The complete ledger}"


def literal(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"{label}: expected one legacy block, found {count}")
    return text.replace(old, new, 1)


def replace_item(text: str, start: str, end: str, replacement: str, label: str) -> str:
    if replacement.strip() in text:
        return text
    i = text.find(start)
    if i < 0:
        raise AssertionError(f"{label}: start marker missing")
    j = text.find(end, i + len(start))
    if j < 0:
        raise AssertionError(f"{label}: end marker missing")
    return text[:i] + replacement + text[j:]


ABSTRACT = r"""\begin{abstract}
\noindent
This is an executable design document for a computer that does not yet exist. Every
promoted statement is classified as \emph{proved}, \emph{simulated}, \emph{synthesized},
\emph{placed}, \emph{published}, \emph{modelled}, or \emph{open}; component evidence is
never silently promoted into an end-to-end machine claim. The logic substrate is the
$40$-point geometry $W(3,3)$. A minimal frame-control core uses \textbf{four operations
encoded by two opcode bits}, while the public eight-opcode three-bit ISA remains a
convenience shell. The measured convenience frame unit occupies \textbf{72 iCE40 logic
cells} and closes at \textbf{60.8\,MHz}; the minimal unit has its own independent hardware
gate. The deep $M_{36}$ grade is proved two-copy fidelity-distillable under full logical
Clifford decoding, with an explicit branch improving throughout its complete
magic-witness interval. That theorem is not an asymptotic-yield result or a
fault-tolerant injection threshold. A published photonic qutrit \textsc{sum} component
reaches $0.92\pm0.01$ fidelity, but that is not a measured Holonet. This document gives
the semantics, datapath, resource evidence, release gates, and the exact record of claims
that failed under stronger tests.
\end{abstract}"""


def upgrade(text: str) -> str:
    text = re.sub(
        r"\\date\{\\normalsize 3 August 2026 \\quad\$\\cdot\$\\quad Passes 2700--\d+\}",
        r"\\date{\\normalsize 3 August 2026 \\quad$\\cdot$\\quad Passes 2700--2812}",
        text,
        count=1,
    )
    if "This is an executable design document" not in text:
        text, count = re.subn(
            r"\\begin\{abstract\}.*?\\end\{abstract\}",
            lambda _m: ABSTRACT,
            text,
            count=1,
            flags=re.DOTALL,
        )
        if count != 1:
            raise AssertionError("abstract migration did not match exactly once")

    text = literal(text, "There are eleven of them. They are not", "There are twelve of them. They are not", "errata count")
    text = literal(
        text,
        "\\textbf{Instruction set}      & $\\mathcal{I}_{\\mathrm{holo}}$, eight opcodes, three bits. \\\\",
        "\\textbf{Minimal frame core}   & Four operations, two opcode bits: $F_p$, both\\n"
        "                                controlled-add directions, and one translation. \\\\\n"
        "\\textbf{Public ISA}           & $\\mathcal{I}_{\\mathrm{holo}}$, eight three-bit opcodes;\\n"
        "                                the extras are scheduling conveniences, not additional\\n"
        "                                frame expressivity. \\\\",
        "front-page ISA table",
    )
    text = literal(
        text,
        "\\textbf{Arithmetic unit}      & $72$ iCE40 logic cells, $60.80$\\,MHz (measured, \\S\\ref{sec:budget}). \\\\",
        "\\textbf{Arithmetic unit}      & Public convenience frame unit: $72$ iCE40 logic cells,\\n"
        "                                $60.80$\\,MHz (measured, \\S\\ref{sec:budget}); the minimal\\n"
        "                                two-bit unit has an independent hardware gate. \\\\",
        "front-page arithmetic row",
    )
    text = literal(
        text,
        "\\textbf{Physical layer}       & Time-bin $\\times$ frequency-bin photonic qutrits; the\\n"
        "                                two-qutrit \\textsc{sum} gate is experimentally\\n"
        "                                demonstrated at fidelity $0.92\\pm0.01$. \\\\",
        "\\textbf{Physical layer}       & Time-bin $\\times$ frequency-bin photonic qutrits; a\\n"
        "                                two-qutrit \\textsc{sum} component is published at\\n"
        "                                fidelity $0.92\\pm0.01$, not as an end-to-end Holonet. \\\\\n"
        "\\textbf{Evidence firewall}    & Proved $\\neq$ simulated $\\neq$ synthesized $\\neq$ placed;\\n"
        "                                promotion requires every gate in \\S\\ref{sec:evidence}. \\\\",
        "front-page physical row",
    )
    text = literal(
        text,
        "eight opcodes; generates $\\mathrm{ASp}(4,3)$, order $4{,}199{,}040$",
        "four-operation two-bit core; eight-opcode public shell; same $\\mathrm{ASp}(4,3)$",
        "stack ISA label",
    )

    if INPUT not in text:
        if text.count(LEDGER) != 1:
            raise AssertionError("ledger insertion marker missing or duplicated")
        text = text.replace(LEDGER, INPUT + "\n\n" + LEDGER, 1)

    text = literal(
        text,
        "$\\mu_{12}$ at $n{=}1$ by exact enumeration ($2592=12\\cdot216$) & proved & Pass 2791\\\\\n"
        "Minimal exponent $=3^n\\bmod 12$: $3$ odd, $9$ even & derived & Pass 2791\\\\",
        "Standard finite Clifford lift has scalar group $\\mu_{12}$ for all $n$ & proved & Pass 2805\\\\\n"
        "Minimal finite-lift exponent: $3$ odd $n$, $9$ even $n$ & proved & Pass 2805\\\\\n"
        "Arbitrary $U(1)$ representative phase requires exponent $3^n$ & proved & Pass 2805\\\\",
        "sensor ledger",
    )
    text = literal(
        text,
        "$M_{36}$ two-copy no-go, $5355$ codes $\\times$ $4$ syndromes & \\textbf{prior art} & parallel track, Pass 2784\\\\",
        "$M_{36}$ full decoder search: $11{,}520$ Cliffords, $48$ deep improvements & proved & Pass 2804\\\\\n"
        "Explicit deep branch improves for $0<p<2/3$ & proved & Pass 2804\\\\",
        "M36 ledger",
    )
    text = literal(
        text,
        "py -3 analysis/w33\\_pass2778\\_2779\\_affine\\_group\\_and\\_sensor\\_exponent.py\\\\[4pt]",
        "py -3 analysis/w33\\_pass2778\\_2779\\_affine\\_group\\_and\\_sensor\\_exponent.py\\\\\n"
        "py -3 analysis/bt2804\\_m36\\_clifford\\_decoder\\_distillation.py\\\\\n"
        "py -3 analysis/bt2805\\_n\\_qutrit\\_sensor\\_exponent.py\\\\\n"
        "py -3 analysis/bt2808\\_2812\\_blueprint\\_truth\\_gate.py -{}-check\\\\[4pt]",
        "reproduction commands",
    )

    magic = r"""\item \textbf{State-fidelity distillation is built; fault-tolerant injection is not.}
      Pass 2804 gives an explicit two-copy deep-grade protocol and proves exactly $48$
      improving branches under full logical Clifford decoding. The open work is now
      asymptotic yield, physical preparation cost, logical-noise propagation, injection
      into the selected non-Clifford operation, and an end-to-end threshold. The RTL
      controller continues to require a separately validated preparation handshake.
"""
    if "State-fidelity distillation is built; fault-tolerant injection is not" not in text:
        text = replace_item(text, "\\item \\textbf{The magic-state route is the universality gap.}", "\\item \\textbf{No physical power figure exists.}", magic, "M36 open item")

    transpose = r"""\item \textbf{(Closed at Pass 2806.)} The transpose is checked objectwise at
      $q=5$ and $q=7$: $T^2=I$, $T^{\mathsf T}JT=-J$, controlled-add directions are
      conjugate, and the reverse gate is obtained by local Fourier conjugacy. The broader
      eight-prime modular check remains in Pass 2792.
"""
    if "Closed at Pass 2806" not in text:
        text = replace_item(text, "\\item \\textbf{(Closed at Pass 2792.)}", "\\item \\textbf{One original module is unparseable}", transpose, "transpose item")

    mixer = r"""\item \textbf{The rejected mixer source is removed from the active tree.}
      Verification and workflow triggers now target
      \cmd{rtl/w33\_pass2773\_spread\_mixer36\_synth.sv}. The packed-bus replacement is
      exact and parseable, but its parallel area exceeds the iCE40 target; the serial
      mixer remains the deployable architecture.
"""
    if "rejected mixer source is removed from the active tree" not in text:
        text = replace_item(text, "\\item \\textbf{One original module is unparseable}", "\\end{enumerate}", mixer, "mixer item")
    return text


def truth_checks(text: str) -> dict[str, bool]:
    insert = INSERT.read_text(encoding="utf-8")
    combined = text + "\n" + insert
    return {
        "pass_range_2812": "Passes 2700--2812" in text,
        "minimal_four_operation_core": "four operations encoded by two opcode bits" in combined,
        "public_shell": "public eight-opcode three-bit ISA remains a" in text,
        "evidence_input": INPUT in text,
        "promotion_firewall": "Evidence-state contract" in insert,
        "m36_full_decoder_count": "$11{,}520$-element projective two-qubit" in insert,
        "m36_48_branches": "exactly $48$ improving branches" in combined,
        "m36_explicit_interval": "improves for $0<p<2/3$" in combined,
        "m36_threshold_boundary": "not yet provide asymptotic" in insert,
        "sensor_all_n_mu12": "is $\\mu_{12}$ for every register width" in insert,
        "sensor_u1_boundary": "$U(1)$ phases rather than the standard finite lift" in insert,
        "transpose_direction": "T\\,\\mathrm{CX}_{p\\to f}\\,T^{-1}=\\mathrm{CX}_{f\\to p}" in insert,
        "mixer_removed": "removed\nfrom the active tree" in insert,
        "component_not_system": "not a measured Holonet" in text,
        "stale_broad_no_go_removed": "two-copy no-go" not in text,
        "stale_no_protocol_removed": "does \\emph{not} supply a distillation protocol" not in text,
    }


def write_certificate(text: str, checks: dict[str, bool]) -> None:
    insert = INSERT.read_text(encoding="utf-8")
    payload = {
        "schema": "w33.pass2808_2812.blueprint_hardening.v1",
        "canonical_pass_range": "2808-2812",
        "depends_on": "w33.pass2803_2807.five_deep_frontiers.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "check_count": len(checks),
        "checks": checks,
        "blueprint_sha256": hashlib.sha256(text.encode()).hexdigest(),
        "insert_sha256": hashlib.sha256(insert.encode()).hexdigest(),
        "boundaries": {
            "m36": "state-fidelity distillation, not asymptotic yield or fault-tolerant injection",
            "sensor": "3/9 law for standard finite mu_12 lift; arbitrary U(1) uses 3^n",
            "hardware": "synthesis and P&R require observed clean-run evidence",
            "photonic": "published component evidence is not an end-to-end Holonet",
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    original = TEX.read_text(encoding="utf-8")
    migrated = upgrade(original)
    if args.write and migrated != original:
        TEX.write_text(migrated, encoding="utf-8")
    current = TEX.read_text(encoding="utf-8")
    checks = truth_checks(current)
    write_certificate(current, checks)

    if args.check and migrated != original:
        raise AssertionError("migration not applied; run --write and commit the result")
    missing = [name for name, ok in checks.items() if not ok]
    if missing:
        raise AssertionError(f"blueprint truth-gate failures: {missing}")
    if upgrade(current) != current:
        raise AssertionError("migration is not idempotent")
    print(f"PASS {len(checks)}/{len(checks)}; {TEX}")


if __name__ == "__main__":
    main()
