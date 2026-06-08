# BT574 — Static Preprint Check Manifest

Target: `paper/w33_preprint.tex`

Purpose: verify that the BT572 section is structurally present and ready for a full TeX compile in a local build environment.

Checked items:

- Section title appears once.
- Section label appears once.
- The section is placed before the TOE Singularity section.
- Theorem, proof, and display-math delimiters are balanced in the inserted section.
- Existing local section inputs are referenced and checked by the verifier.
- Required formulas from BT564--BT573 are present in the inserted section.

Status: verifier script pushed in `analysis/bt574_latex_sanity_verifier.py`.

Boundary: this is a static repository check, not a substitute for running a full PDF build with an installed TeX toolchain.
