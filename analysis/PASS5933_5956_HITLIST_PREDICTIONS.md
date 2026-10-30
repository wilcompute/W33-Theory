# PASS 5933–5956 — SUPERSEDED PREDICTION-DERIVATION CLAIMS

**Status:** `ANSATZ/COMPARISON-ONLY` after Pass5957–5964 evidence audit.

The original version of this file claimed derivations of a Yang–Mills mass gap at
1818 MeV, a 0.0500 eV neutrino mass, inflationary `r=1/45`, and a scalar resonance
near 3.2 TeV. The producer scripts do not establish those claims as predictions.

Canonical correction:

- `analysis/PASS5957_5964_prediction_evidence_audit.md`
- `data/PART_W33_PASS5957_5964_PREDICTION_EVIDENCE_AUDIT.json`
- `analysis/PASS5957_5964_prediction_evidence_audit_insert.tex`

What remains valid:

1. The cubic-surface count of 45 tritangent planes may be retained where independently
   certified.
2. The octahedron graph `K_{2,2,2}` has exactly 384 spanning trees.
3. The integer identity `6*480*13*273 = 10,221,120` is exact.
4. The coefficient `12*sqrt(13/40)` is exact arithmetic from the chosen W33 constants.

Why prediction status was withdrawn:

- the Yang–Mills producer explicitly solves `Lambda_QCD_eff` from the target
  `1818 MeV`;
- the neutrino producer first obtains a factor four too large, notices the mismatch,
  then replaces 24 by 6 to obtain the desired denominator;
- the inflation producer simply defines `r = 1/N_tritangent` without deriving an
  inflationary potential or perturbation spectrum;
- the scalar producer simply multiplies the measured Higgs mass by `384/15` without
  a mass operator, pole equation, coupling, or self-energy theorem.

These finite quantities may remain as ansätze worth exploring, but numerical agreement
cannot upgrade them to predictions without an independent dynamics theorem.

The original content remains recoverable in Git history at commit
`2326c04067f6e239f2d97a033e1a96365dda47a2`.
