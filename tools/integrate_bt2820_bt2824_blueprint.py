#!/usr/bin/env python3
"""Idempotently integrate Passes 2820--2824 into the public artifacts."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSERT = r"\input{analysis/BT2820_BT2824_blueprint_hardening_insert}%"


def write_if_changed(path: Path, text: str) -> bool:
    old = path.read_text(encoding="utf-8")
    if old == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def add_wrapper_insert(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if INSERT in text:
        return False
    anchor = r"\input{analysis/BT2808_pg32_tetrahedral_support_lift_insert}%"
    if anchor in text:
        text = text.replace(anchor, anchor + "\n" + INSERT, 1)
    else:
        body = r"\input{w33_paper_body.tex}"
        if body not in text:
            raise RuntimeError(f"cannot locate insertion anchor in {path}")
        text = text.replace(body, INSERT + "\n" + body, 1)
    return write_if_changed(path, text)


def patch_blueprint(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    text = text.replace("Passes 2700--2795", "Passes 2700--2824")

    old_abstract = """The machine's logic is a $40$-point finite geometry called $W(3,3)$; its instruction set
has eight opcodes and generates a group of order $4{,}199{,}040$ exactly; its arithmetic
unit fits in \\textbf{72 logic cells} on a \\$25 FPGA and runs at \\textbf{60.8\\,MHz}; and
its physical layer is a photonic gate that a laboratory has already demonstrated with
$0.92$ fidelity."""
    new_abstract = """The machine's logic is a $40$-point finite geometry called $W(3,3)$.  Its public
three-bit ISA exposes eight opcodes, while its internal two-bit frame micro-ISA uses four
operations; both generate the affine group of order $4{,}199{,}040$ exactly.  The measured
loadable public frame unit fits in \\textbf{72 logic cells} on a \\$25 FPGA and runs at
\\textbf{60.8\\,MHz}; the minimal four-operation engine awaits separately observed
synthesis and place-and-route evidence.  The physical layer is a photonic gate that a
laboratory has already demonstrated with $0.92$ fidelity."""
    if old_abstract in text:
        text = text.replace(old_abstract, new_abstract, 1)

    text = text.replace(
        r"\textbf{Instruction set}      & $\mathcal{I}_{\mathrm{holo}}$, eight opcodes, three bits. \\",
        r"""\textbf{Public instruction set} & $\mathcal{I}_{\mathrm{holo}}$, eight opcodes, three bits. \\
\textbf{Internal micro-ISA}    & $F_p$, $\mathrm{CX}_{p\to f}$, $\mathrm{CX}_{f\to p}$, $Z_p$: four operations, two bits. \\""",
    )
    text = text.replace(
        r"\textbf{Arithmetic unit}      & $72$ iCE40 logic cells, $60.80$\,MHz (measured, \S\ref{sec:budget}). \\",
        r"\textbf{Arithmetic unit}      & Public loadable unit: $72$ iCE40 logic cells, $60.80$\,MHz (measured, \S\ref{sec:budget}); minimal-engine P\&R remains separate. \\",
    )
    text = text.replace(
        "eight opcodes; generates $\\mathrm{ASp}(4,3)$, order $4{,}199{,}040$",
        "public eight-opcode ISA / internal four-operation micro-ISA; generates $\\mathrm{ASp}(4,3)$, order $4{,}199{,}040$",
    )

    text = text.replace(
        r"\section{The magic states, and the one thing the machine cannot yet do}\label{sec:magic}",
        r"\section{The magic states, and the deep-grade protocol now known}\label{sec:magic}",
    )
    old_plain = r"""\begin{plain}
That is the practical payoff. The known result in this area is a \emph{no-go}: an
exhaustive search over $5{,}355$ small stabilizer codes and $21{,}420$ branches found no
two-copy protocol that improves fidelity anywhere it applies. The natural next move is to
search bigger protocols, and that search is expensive. Knowing there are only three
inequivalent starting materials shrinks it by a factor of twelve before it begins.
\end{plain}

\begin{spec}[Evidence boundary, stated as bluntly as possible]
No distillation protocol for $M_{36}$ is known. The controller types the resource
\cmd{M36\_Q4\_RAW} and \emph{refuses} injection in RTL until a proved protocol asserts
validity. \textbf{Until that assertion exists, this machine is not universal.} Everything
else in this blueprint is built or proved; this is not.
\end{spec}"""
    new_plain = r"""\begin{gotwrong}[The arbitrary-decoder no-go was false]
The earlier search fixed the logical decoder too narrowly.  Pass 2804 exhausts all
$5{,}355$ binary $[[4,2]]$ stabilizer projectors, all four syndromes, and the full
$11{,}520$-element logical Clifford decoder group.  The shallow and two middle grades
still have zero improving branches, but the deep eight-ray grade has exactly $48$
improving deep-grade branches.
\end{gotwrong}

\begin{spec}[One exact deep-grade branch]
Input ray $5$, stabilizers $\mathrm{IYZY}$ and $\mathrm{YZXY}$, syndrome $(-1,+1)$,
Hadamard on the second logical coordinate, and output ray $7$ give
\[
P_{\rm succ}=\frac{p^2-2p+2}{4},\qquad
F_{\rm out}=\frac{5p^2-12p+8}{4(p^2-2p+2)},
\]
\[
F_{\rm out}-F_{\rm in}=\frac{p(p-1)(3p-2)}{4(p^2-2p+2)}.
\]
Hence the branch improves state fidelity for $0<p<2/3$, covering the deep magic interval.
This is state-fidelity distillation, not a fault-tolerant injection threshold or an
asymptotic-yield theorem; the RTL injection gate remains evidence-gated.
\end{spec}"""
    if old_plain in text:
        text = text.replace(old_plain, new_plain, 1)
    else:
        text = text.replace(
            "No distillation protocol for $M_{36}$ is known.",
            "Pass 2804 proves a deep-grade state-fidelity distillation branch; no fault-tolerant injection threshold is claimed.",
        )

    old_ledger_magic = r"""\item \textbf{The magic-state route is the universality gap.} The substrate identifies
      $36$ distinguished Witting rays and computes exact non-stabilizer witness
      boundaries for them. It does \emph{not} supply a distillation protocol; the
      published qutrit protocols act on a different space (ququart versus qutrit) and do
      not transfer."""
    new_ledger_magic = r"""\item \textbf{(Corrected at Pass 2804.)} The earlier arbitrary-decoder no-go was false.
      The exhaustive $5{,}355\times4\times11{,}520$ search finds $48$ improving branches,
      all in the deep eight-ray grade.  The result is a state-fidelity protocol, not a
      fault-tolerant injection threshold or asymptotic-yield theorem."""
    text = text.replace(old_ledger_magic, new_ledger_magic)

    old_ledger_mixer = r"""\item \textbf{One original module is unparseable} ---
      \cmd{rtl/w33\_spread\_mixer36.sv}, rejected by both frontends. It now carries a
      deprecation banner naming its replacement and quoting both errors; the bytes are
      kept as the historical record, since it compiles nowhere and deleting another
      track's file is not ours to do."""
    new_ledger_mixer = r"""\item \textbf{(Closed at Pass 2805.)} The historical dead source was removed:
      \cmd{rtl/w33\_spread\_mixer36.sv}.  The only live mixer is
      \cmd{rtl/w33\_pass2773\_spread\_mixer36\_synth.sv}; provenance is retained in Git
      history rather than in an unparseable source file."""
    text = text.replace(old_ledger_mixer, new_ledger_mixer)

    if INSERT not in text:
        anchor = "% =====================================================================================\n\\section{The network}\\label{sec:network}"
        if anchor not in text:
            raise RuntimeError("cannot locate blueprint hardening insertion anchor")
        text = text.replace(anchor, INSERT + "\n\n" + anchor, 1)

    return write_if_changed(path, text) if text != original else False


def patch_index(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if 'id="pass-2820-2824-blueprint-hardening"' in text:
        return False
    section = r'''
<section id="pass-2820-2824-blueprint-hardening" class="section theorem-section">
  <div class="section-number">Passes 2820--2824</div>
  <h2>Blueprint hardening: support for readout, phase for execution</h2>
  <p>The public machine keeps its eight-opcode, three-bit interface, while the exact internal frame micro-ISA uses four operations and two bits. The measured 72-LC / 60.80-MHz result remains attached to the public loadable unit until the minimal engine receives its own synthesis and place-and-route certificate.</p>
  <p>The corrected M36 search exhausts 5,355 stabilizer projectors, four syndromes, and 11,520 logical Clifford decoders. It finds exactly 48 improving branches, all in the deep eight-ray grade, with an explicit fidelity-improving interval <span class="math">0 &lt; p &lt; 2/3</span>.</p>
  <p>The PG(3,2) support shell is an exact geometric codec, but deterministic refinement under the four-operation engine runs <span class="math">16 &rarr; 40 &rarr; 78 &rarr; 81</span>. The support mask is therefore a readout/routing layer, not a replacement for ternary execution phase.</p>
</section>
'''
    marker = "</body>"
    if marker in text:
        text = text.replace(marker, section + "\n" + marker, 1)
    else:
        text += "\n" + section
    return write_if_changed(path, text)


def close_registry(path: Path) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("status") == "complete":
        return False
    data["status"] = "complete"
    data["completed_at_utc"] = "2026-08-03T00:00:00Z"
    data["completion"] = {
        "verifier": "analysis/bt2820_2824_blueprint_hardening.py",
        "certificate": "data/PART_BT2820_BT2824_BLUEPRINT_HARDENING_results.json",
        "insert": "analysis/BT2820_BT2824_blueprint_hardening_insert.tex",
        "workflow": ".github/workflows/w33_pass2820_2824_blueprint_hardening.yml",
    }
    return write_if_changed(path, json.dumps(data, indent=2, sort_keys=True) + "\n")


def main() -> None:
    changed = []
    for name in ("w33_paper.tex", "photonic_holonet.tex"):
        if add_wrapper_insert(ROOT / name):
            changed.append(name)
    if patch_blueprint(ROOT / "holonet_machine_blueprint.tex"):
        changed.append("holonet_machine_blueprint.tex")
    if patch_index(ROOT / "docs" / "index.html"):
        changed.append("docs/index.html")
    registry = ROOT / "data" / "w33_pass_namespace_registry_v2.d" / "2820-2824.json"
    if close_registry(registry):
        changed.append(str(registry.relative_to(ROOT)))
    print("changed:", ", ".join(changed) if changed else "none (already integrated)")


if __name__ == "__main__":
    main()
