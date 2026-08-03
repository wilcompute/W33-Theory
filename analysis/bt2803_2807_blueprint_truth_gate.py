#!/usr/bin/env python3
"""Passes 2803-2807: idempotently harden holonet_machine_blueprint.tex.

The script deliberately treats the blueprint as an executable specification.  It repairs
stale front-page claims, inserts an evidence/promotion firewall, narrows the M36 census to
the decoder gauge actually enumerated, separates exact n=1,2 sensor results from the
conditional n-qutrit extension, and records the retired mixer migration contract.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "holonet_machine_blueprint.tex"
OUT = ROOT / "data" / "PART_BT2803_BT2807_BLUEPRINT_HARDENING_results.json"

SECTION_MARKER = "% =====================================================================================\n\\section{The complete ledger}"
NEW_SECTION_TOKEN = "\\section{Evidence states and release gates}\\label{sec:evidence}"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"{label}: expected one old block, found {count}")
    return text.replace(old, new, 1)


def replace_delimited(text: str, start: str, end: str, replacement: str, label: str) -> str:
    if replacement in text:
        return text
    i = text.find(start)
    if i < 0:
        raise AssertionError(f"{label}: start marker missing")
    j = text.find(end, i + len(start))
    if j < 0:
        raise AssertionError(f"{label}: end marker missing")
    return text[:i] + replacement + text[j:]


def upgrade(text: str) -> str:
    text = re.sub(
        r"\\date\{\\normalsize 3 August 2026 \\quad\$\\cdot\$\\quad Passes 2700--\d+\}",
        r"\\date{\\normalsize 3 August 2026 \\quad$\\cdot$\\quad Passes 2700--2807}",
        text,
        count=1,
    )

    text = replace_once(
        text,
        "There are eleven of them. They are not",
        "There are twelve of them. They are not",
        "errata-box count",
    )

    abstract = r"""\begin{abstract}
\noindent
This is an executable design document for a computer that does not yet exist. Every
promoted statement is classified as \emph{proved}, \emph{measured}, \emph{published},
\emph{modelled}, or \emph{open}; a component result is never silently promoted into an
end-to-end machine claim. The logic substrate is the $40$-point geometry $W(3,3)$. A
minimal frame-control core uses \textbf{four instructions encoded by two opcode bits},
while the eight-opcode three-bit ISA remains a convenience shell; both generate the same
full affine symplectic action once one translation is present. The measured convenience
frame unit occupies \textbf{72 iCE40 logic cells} and closes at \textbf{60.8\,MHz}. A
published photonic qutrit \textsc{sum} gate reaches $0.92\pm0.01$ fidelity, but that is
component evidence rather than a measured Holonet. The remaining universality gap is a
proved, decoder-independent $M_{36}$ injection or distillation protocol. This document
gives the instruction semantics, datapath, resource evidence, network protocol, release
gates, and an itemised record of the claims that failed under stronger tests.
\end{abstract}"""
    if "Every\npromoted statement is classified" not in text:
        text = replace_delimited(
            text,
            "\\begin{abstract}",
            "\\end{abstract}",
            abstract,
            "abstract truth repair",
        )

    text = replace_once(
        text,
        "\\textbf{Instruction set}      & $\\mathcal{I}_{\\mathrm{holo}}$, eight opcodes, three bits. \\\\",
        "\\textbf{Minimal frame core}   & Four instructions, two opcode bits: one of six exact\\n"
        "                                three-Clifford generating triples plus one translation. \\\\\n"
        "\\textbf{Convenience ISA}      & $\\mathcal{I}_{\\mathrm{holo}}$, eight three-bit opcodes;\\n"
        "                                the extra operations are scheduling conveniences, not\\n"
        "                                additional frame expressivity. \\\\",
        "one-page ISA table",
    )
    text = replace_once(
        text,
        "\\textbf{Arithmetic unit}      & $72$ iCE40 logic cells, $60.80$\\,MHz (measured, \\S\\ref{sec:budget}). \\\\",
        "\\textbf{Arithmetic unit}      & Full convenience frame unit: $72$ iCE40 logic cells,\\n"
        "                                $60.80$\\,MHz (measured, \\S\\ref{sec:budget}); the minimal\\n"
        "                                two-bit implementation is measured separately. \\\\",
        "one-page arithmetic row",
    )
    text = replace_once(
        text,
        "\\textbf{Physical layer}       & Time-bin $\\times$ frequency-bin photonic qutrits; the\\n"
        "                                two-qutrit \\textsc{sum} gate is experimentally\\n"
        "                                demonstrated at fidelity $0.92\\pm0.01$. \\\\",
        "\\textbf{Physical layer}       & Time-bin $\\times$ frequency-bin photonic qutrits; a\\n"
        "                                two-qutrit \\textsc{sum} component is published at\\n"
        "                                fidelity $0.92\\pm0.01$, not yet as an end-to-end Holonet. \\\\\n"
        "\\textbf{Evidence firewall}    & Proved $\\neq$ measured $\\neq$ published $\\neq$ modelled;\\n"
        "                                promotion requires every gate in \\S\\ref{sec:evidence}. \\\\",
        "one-page physical/evidence rows",
    )
    text = replace_once(
        text,
        "eight opcodes; generates $\\mathrm{ASp}(4,3)$, order $4{,}199{,}040$",
        "four-instruction, two-bit core; eight-opcode convenience shell; same $\\mathrm{ASp}(4,3)$",
        "stack diagram ISA label",
    )

    section = r"""
% =====================================================================================
\section{Evidence states and release gates}\label{sec:evidence}
% =====================================================================================

\begin{plain}
A mathematical proof, a synthesized netlist, a placed design, a laboratory component and
an end-to-end machine are five different kinds of evidence. Earlier drafts occasionally
put them in one sentence and allowed the strongest-sounding phrase to colour the rest.
This section is the promotion firewall: it says exactly what must be true before a claim
moves upward.
\end{plain}

\begin{spec}[Evidence-state contract]
\begin{center}
\begin{tabular}{@{}p{2.4cm}p{5.2cm}p{6.2cm}@{}}
\toprule
\textbf{State} & \textbf{Meaning} & \textbf{Promotion gate}\\
\midrule
Proved & Exact finite or symbolic statement & Deterministic rebuild and an independent
falsifier both pass.\\
Simulated & RTL behaviour under a stated bench & Both frontends parse; the bench observes
state change and illegal-input failure.\\
Synthesized & Technology-mapped netlist exists & Sequential state survives optimization;
cell and DFF floors reject folded designs.\\
Placed/timed & Routed design on a named part & nextpnr completes, utilization is recorded,
and the requested clock has non-negative slack.\\
Published component & External laboratory result & The cited device implements the same
operation and encoding, with its own assumptions preserved.\\
Modelled system & End-to-end engineering scenario & Every rate, loss, memory and latency
assumption is explicit; it is never called measured.\\
Built system & Physical Holonet & Requires a reproducible end-to-end experiment. This row
is currently open.\\
\bottomrule
\end{tabular}
\end{center}
\end{spec}

\subsection{Minimal core versus convenience shell}

The frame-control theorem has two interfaces that must not be conflated. The convenience
ISA contains eight three-bit opcodes because that is a useful scheduling surface. The
minimal generating interface contains three Clifford operations and one translation, so
it fits in two opcode bits. Exhaustive subset closure finds no one- or two-Clifford
solution and exactly six three-Clifford generating triples. Every valid triple contains a
Fourier operation and an entangling controlled-add operation. One translation generator
then produces the full affine group because $\mathrm{Sp}(4,3)$ is transitive on the $80$
nonzero frame vectors.

\headline{Four instructions are sufficient for expressivity. Eight instructions are
convenient for scheduling. Cell counts must always say which interface was synthesized.}

\subsection{The $M_{36}$ decoder-gauge firewall}

The Pass-2784 census is exhaustive over all $5{,}355$ binary rank-two isotropic
$[[4,2]]$ projectors and all four syndromes, but only after freezing a canonical logical
Pauli decoder gauge. The first implementation diagonalized commuting Paulis numerically;
arbitrary eigensolver column phases changed the logical decoder while leaving the
projector unchanged. A clean-run CI rebuild exposed the error because the claimed branch
counts moved. The repaired implementation constructs each logical basis state from
rank-one Pauli projectors and freezes the surviving phase.

\begin{gotwrong}[The no-go was broader than the enumerated object]
The earlier sentence said that an arbitrary logical Clifford decoder was ``absorbed by
the $M_{36}$ orbit.'' The remote clean rebuild falsified that wording. What is proved is:
no improving branch exists in the frozen canonical logical Pauli decoder gauge over the
stated witness intervals. Arbitrary logical Clifford decoders, nonidentical inputs,
three-copy blocks, catalytic resources, adaptive rounds and non-stabilizer assistance
remain open.
\end{gotwrong}

\subsection{Metaplectic sensor scope}

For a $d$-dimensional representative, the ratio
\[
 \Theta_k^{(e)}(U)=\frac{\operatorname{Tr}(U^k)^e}{\det(U^k)}
\]
is invariant under $U\mapsto\lambda U$ when $e\equiv d$ modulo the scalar-phase order.
The scalar subgroup is verified as $\mu_{12}$ for one qutrit by exact enumeration and for
two qutrits by the independent collision certificate. Thus the minimal exponents are
exactly $3$ at $n=1$ and $9$ at $n=2$. The alternating rule
$e_n\equiv3^n\pmod{12}$ gives $3,9,3,9,\ldots$ provided the $\mu_{12}$ scalar subgroup
persists for general $n$; the all-$n$ persistence proof is a separate obligation and is
not smuggled in by the arithmetic congruence alone.

\subsection{Transpose scope and mixer retirement}

The anti-symplectic transpose construction is checked at
$q=3,5,7,11,13,17,19,23$, with $T^2=I$ and $T^{\mathsf T}JT=-J$ in every case; the
outer/inner congruence criterion follows from whether $-1$ is a square. The original
\cmd{rtl/w33\_spread\_mixer36.sv} is retained only as an archaeological artifact. It is
not an admissible build source: neither Icarus nor Yosys accepts it. New manifests must
use \cmd{rtl/w33\_pass2773\_spread\_mixer36\_synth.sv} for the exact parallel port or the
serial mixer for an iCE40 target, because the measured parallel implementation requires
$13{,}965$ LUT4s and does not fit the target part.

\subsection{Release-state matrix}

\begin{center}
\begin{tabular}{@{}p{4.1cm}p{3.0cm}p{7.0cm}@{}}
\toprule
\textbf{Packet} & \textbf{Promoted state} & \textbf{Remaining gate}\\
\midrule
Minimal/convenience ISA & proved; full shell measured & Measure every chosen two-bit core
in the same loadable harness before quoting its area.\\
$M_{36}$ two-copy census & proved in canonical gauge & Enumerate logical Clifford gauges,
then larger/nonidentical/catalytic protocols.\\
Metaplectic sensor & exact codebook and shot model & Add visibility, phase-diffusion,
loss and detector-imbalance confusion matrices.\\
Passes 2784--2788 hardware & local exact rebuild & Promote RTL/synthesis/P\&R only after
the dedicated clean GitHub runner reaches every hardware stage.\\
Photonic remote \textsc{sum} & recurrence and scheduler model & Demonstrate the stated
encoding, heralding and memory assumptions end to end.\\
\bottomrule
\end{tabular}
\end{center}

"""
    if NEW_SECTION_TOKEN not in text:
        if SECTION_MARKER not in text:
            raise AssertionError("complete-ledger insertion marker missing")
        text = text.replace(SECTION_MARKER, section + SECTION_MARKER, 1)

    text = replace_once(
        text,
        "$\\mu_{12}$ at $n{=}1$ by exact enumeration ($2592=12\\cdot216$) & proved & Pass 2791\\\\\n"
        "Minimal exponent $=3^n\\bmod 12$: $3$ odd, $9$ even & derived & Pass 2791\\\\",
        "$\\mu_{12}$ at $n{=}1$ exact and $n{=}2$ independently certified & proved & Passes 2779, 2791\\\\\n"
        "Minimal exponents $3$ ($n{=}1$) and $9$ ($n{=}2$) & proved & Passes 2779, 2791\\\\\n"
        "Odd/even $3,9$ cycle for general $n$ & conditional & requires all-$n$ $\\mu_{12}$ persistence\\\\",
        "sensor ledger scope",
    )
    text = replace_once(
        text,
        "$M_{36}$ two-copy no-go, $5355$ codes $\\times$ $4$ syndromes & \\textbf{prior art} & parallel track, Pass 2784\\\\",
        "$M_{36}$ canonical-gauge census, $5355$ codes $\\times$ $4$ syndromes & proved & Pass 2784 v2\\\\\n"
        "Arbitrary logical Clifford decoder gauges & \\textcolor{bad}{OPEN} & clean-run failure exposed scope\\\\",
        "M36 ledger scope",
    )

    text = replace_once(
        text,
        "py -3 analysis/w33\\_pass2778\\_2779\\_affine\\_group\\_and\\_sensor\\_exponent.py\\\\[4pt]",
        "py -3 analysis/w33\\_pass2778\\_2779\\_affine\\_group\\_and\\_sensor\\_exponent.py\\\\\n"
        "py -3 analysis/bt2803\\_2807\\_blueprint\\_truth\\_gate.py -{}-check\\\\[4pt]",
        "reproduction truth-gate command",
    )

    magic_replacement = r"""\item \textbf{The magic-state route is the universality gap.} The substrate identifies
      $36$ distinguished Witting rays and the Pass-2784 packet proves a finite no-go only
      in its frozen canonical logical Pauli decoder gauge. It does not yet cover arbitrary
      logical Clifford gauges, nonidentical inputs, three-copy blocks, catalysts, adaptive
      protocols or non-stabilizer assistance. The controller therefore refuses injection
      until a separately proved protocol asserts validity.
"""
    if "finite no-go only\n      in its frozen canonical logical Pauli decoder gauge" not in text:
        text = replace_delimited(
            text,
            "\\item \\textbf{The magic-state route is the universality gap.}",
            "\\item \\textbf{No physical power figure exists.}",
            magic_replacement,
            "what-is-not-built M36 item",
        )

    mixer_replacement = r"""\item \textbf{One original module is retired from every build manifest} ---
      \cmd{rtl/w33\_spread\_mixer36.sv}, rejected by both frontends. It remains only as a
      labelled historical artifact. Builds must use the exact packed-port replacement or
      the serial mixer; CI treats any new synthesis reference to the retired source as an
      error. The measured parallel replacement also exceeds the iCE40 target, so parsing
      successfully does not imply deployability.
"""
    if "retired from every build manifest" not in text:
        text = replace_delimited(
            text,
            "\\item \\textbf{One original module is unparseable}",
            "\\end{enumerate}",
            mixer_replacement,
            "retired mixer item",
        )

    return text


def checks(text: str) -> dict[str, bool]:
    required = {
        "pass_range_2807": "Passes 2700--2807" in text,
        "four_instruction_core": "four instructions encoded by two opcode bits" in text,
        "convenience_shell_named": "eight-opcode three-bit ISA remains a convenience shell" in text,
        "evidence_section": NEW_SECTION_TOKEN in text,
        "evidence_firewall": "Proved $\\neq$ measured $\\neq$ published $\\neq$ modelled" in text,
        "m36_gauge_boundary": "frozen canonical logical Pauli decoder gauge" in text,
        "arbitrary_decoder_open": "Arbitrary logical Clifford decoders" in text,
        "sensor_exact_n1_n2": "exactly $3$ at $n=1$ and $9$ at $n=2$" in text,
        "sensor_all_n_conditional": "all-$n$ persistence proof is a separate obligation" in text,
        "transpose_eight_primes": "q=3,5,7,11,13,17,19,23" in text,
        "retired_mixer": "retired from every build manifest" in text,
        "old_abstract_removed": "its instruction set\nhas eight opcodes" not in text,
        "old_m36_scope_removed": "complete only for identical two-copy binary" not in text,
    }
    return required


def write_certificate(text: str, result_checks: dict[str, bool]) -> None:
    payload = {
        "schema": "w33.pass2803_2807.blueprint_hardening.v1",
        "canonical_pass_range": "2803-2807",
        "status": "PASS" if all(result_checks.values()) else "FAIL",
        "check_count": len(result_checks),
        "checks": result_checks,
        "blueprint_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "boundaries": {
            "m36": "canonical logical Pauli decoder gauge only",
            "sensor": "all-n exponent cycle remains conditional on mu_12 persistence",
            "hardware": "RTL/synthesis/P&R promoted only after clean remote observation",
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
    upgraded = upgrade(original)
    if args.write and upgraded != original:
        TEX.write_text(upgraded, encoding="utf-8")
    current = TEX.read_text(encoding="utf-8") if args.write else original
    result_checks = checks(current)
    write_certificate(current, result_checks)

    if args.check:
        if upgraded != original:
            raise AssertionError("blueprint migration has not been applied; run with --write")
        missing = [name for name, ok in result_checks.items() if not ok]
        if missing:
            raise AssertionError(f"blueprint truth-gate failures: {missing}")
    elif not all(result_checks.values()):
        missing = [name for name, ok in result_checks.items() if not ok]
        raise AssertionError(f"post-write truth-gate failures: {missing}")

    print(f"PASS {sum(result_checks.values())}/{len(result_checks)}; {TEX}")


if __name__ == "__main__":
    main()
