# W(3,3)–E₈ Theory of Everything

A computational mathematical‑physics program built from the finite symplectic polar space **W(3,3)**.  The core object is a strongly regular graph on 40 vertices whose adjacency spectrum and incidence geometry generate the Standard Model couplings, mass hierarchies, mixing angles, gauge groups and cosmological parameters from *zero* free parameters.  As of **Phase 39**, the project has completed **3091 independent checks across 39 computation phases with zero failures**.

## Start here

* **Read the one‑minute summary** in the next section to understand the basic claim and why a finite graph can fix Standard‑Model physics.
* **Reproduce one result locally** by running `python SOLVE_OPEN.py` (see `tools/` for scripts) – this verifies a sample identity in under two minutes on a laptop.
* **View the latest paper**: the complete Phase 39 synthesis is in `docs/w33_paper_phase39.pdf` (also available via the GitHub Pages site).  It contains the full derivations, proofs and numeric tables.
* **Check the release notes for Phase 39** to see what changed in the latest milestone.

## What this repository claims

Starting from the graph **W(3,3)** (the symplectic polar space on 40 points with 240 edges), this program builds a chain complex and Dirac operator whose spectral and combinatorial properties reproduce known physics.  Coupling constants such as the fine‑structure constant α, weak mixing angle sin²θ_W, Higgs mass m_H, fermion mass ratios, neutrino mixing angles and cosmological densities all appear as algebraic functions of the same finite‑graph invariants.  The proofs are constructive and computational: every identity is verified by Python scripts that can be run locally, and the full ledger of checks is published.

## Latest milestone: Phase 39 (March 2026)

Phase 39 introduces several major advances and brings the total to **3091 verified identities**:

* **Grand Unification closure** – the finite‑geometry framework now reproduces the GUT gauge group structure and unification of couplings.
* **Seesaw neutrino structure** – the PMNS mixing matrix and seesaw coefficients emerge exactly from projective incidence over F₃.
* **String landscape & swampland links** – the combinatorial identities now connect to heterotic/F‑theory critical dimensions and Swampland constraints.
* **QCD confinement identities** – new spectral packets explain β₀ (Φ₆) and QCD string tension ratios.
* **Higgs and cosmological‑constant refinements** – the Higgs mass and dark‑energy density are sharpened with updated experimental values.

This milestone also reorganises the paper into a navigable “live” format (see the GitHub Pages site) and adds a reproducible `phase_ledger.json` summarising every check.

## Reproducibility

All results in this repository are **exact and reproducible**.  Each claimed identity is accompanied by:

1. **Plain‑English statement** – a short description of the physical quantity being computed.
2. **Mathematical expression** – the explicit finite‑geometry formula used to derive it.
3. **Python script** – code that computes both sides of the equation and checks that they match.
4. **Unit tests** – test files in `tests/` that automatically verify the identities with `pytest`.

To run the full verification suite, install the requirements in `requirements.txt` and execute `pytest`.  To reproduce a single result, open one of the scripts in `scripts/` (for example, `run_alpha_check.py`) and run it – the outputs will show the exact combinatorial values alongside the experimental constants.

## Contributing & outreach

If you are a physicist, mathematician or programmer interested in independent verification, please see `docs/verification.md` for instructions on how to run the proofs and how to contribute new cross‑checks.  For a non‑technical overview, `docs/summary.md` provides a short narrative description of the theory’s motivation and implications.  We welcome issues, pull requests and external critiques – every comment helps sharpen the argument.

## License

This project is licensed under the MIT License.  See `LICENSE` for more information.
