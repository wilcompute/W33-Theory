# Paper Directory Review — May 2026

**Purpose:** prevent confusion between the root-level arXiv manuscripts, `w33_paper_v2.tex`, and the `paper/` directory manuscript.

## Active paper surfaces observed

1. **`paper/main.tex`**
   - Added in commit `5163fb7` with `paper/references.bib` and three figure scripts.
   - Current title: `W(3,3): Arithmetic Uniqueness, Ramanujan Tau Bridge, Neutrino Mass, and Spectral Moment Identities`.
   - Current focus: Ramanujan/LPS uniqueness, tau bridge, spectral moments, neutrino mass, seesaw cascade, and exact-boundary layer.
   - This is the actual `paper/` directory manuscript and should be checked first when the user says "the paper directory".

2. **`w33_paper_v2.tex` / `w33_paper_v2.pdf`**
   - Updated in commit `c049e02`, labeled `PAPER v2.3 (30 pages)`.
   - Includes broad physics claims: Hubble tension theorem, muon g-2 anomaly absence, baryogenesis, strong CP, 33rd prime theorem, and new-particle claims.
   - This is a root-level paper surface, not the `paper/` directory manuscript.

3. **`PART_LXIII_ARXIV_COMPLETE_PAPER.tex`**
   - Updated in commit `6e416e3`, integrating Langlands/Frobenius Section 5 and Yukawa RG Section 6.
   - This is the full arXiv manuscript surface, distinct from both `paper/main.tex` and `w33_paper_v2.tex`.

## Latest structural update to integrate

Parts CXLIV--CL refine the paper architecture into a two-layer observable algebra:

- Mixer layer:
  \[
  C=8/13,\quad T=5/13,\quad D=C-T=3/13.
  \]

- Projection layer:
  \[
  P(A)=A/\Phi_3.
  \]

- Unique bridge:
  \[
  1-D=P(\Phi_4)=10/13.
  \]

This should eventually be integrated into the paper spine as the replacement for one-off ratio claims.  In particular:

- QCD uses mixer-only carrier `qC=24/13` plus the `Phi6` polar threshold.
- Pure field diagnostics use projection-only tokens such as `Phi6/Phi3=7/13`.
- The bridge token `10/13` is both a mixer complement and the direct projection of the `Q(sqrt(-10))` carrier field.

## Local PDF compile note

A local PDF was compiled from the current `paper/main.tex` content fetched from `master`.  It rendered cleanly in 3 pages.  Since the GitHub connector does not expose a direct directory checkout, the local compile used a reconstructed file from the fetched source plus a minimal `references.bib` stub; the manuscript body matches the fetched `paper/main.tex` content.
