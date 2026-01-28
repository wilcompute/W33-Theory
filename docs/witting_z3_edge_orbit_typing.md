# Monomial Edge Orbit Typing (Family Structure)

We typed each monomial edge orbit (12 total) by its **family-pair composition**
(Basis vs Families F0–F3). This reveals the orbit structure is entirely governed
by family blocks.

## Orbit structure summary
- **12 orbits**: 8 of size 27, 4 of size 81
- All **basis-containing edges** live in size‑27 orbits.
- All **non‑basis edges** split into size‑27 and size‑81 orbits depending on
  whether they are same‑family or cross‑family.

## Orbit types (representative)
- **B–F0/F1/F2** edges: size‑27 orbits (each orbit contains 9 of each BF0,BF1,BF2).
- **B–F3** edges: a dedicated size‑27 orbit (all BF3).
- **F0–F0 / F1–F1 / F2–F2**: size‑27 orbits (each orbit has 9 of each).
- **F3–F3**: a dedicated size‑27 orbit.
- **F0–F1 / F0–F2 / F1–F2**: size‑81 orbits (each contains 27 of each cross‑pair).
- **F0–F3 / F1–F3 / F2–F3**: size‑81 orbits (each contains 27 of each cross‑pair).

This shows the monomial symmetry orbits are **exactly the family block decomposition**
of the 40‑ray set. The Z3 edge potential therefore lives on a rigid family‑orbit
stratification, not on finer local features.

Script: `tools/witting_z3_edge_orbit_typing.py`
Full listing: `docs/witting_z3_edge_orbit_typing.txt`
