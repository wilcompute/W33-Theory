# Frozen S8: nonlinear interaction and symmetric power/geometry attribution

> **WITHDRAWN AS PHYSICAL SHEAR EVIDENCE — PASS12632, 2026-11-08.** A CLASS/Halofit scalar-field nonlinear-power bug invalidated the original fading/KLT power spectra. The arithmetic Shapley decomposition below is internally reproducible for its original inputs but has NO valid model-comparison or empirical standing. Do not cite its DES/KiDS rankings or fractions until independent patched likelihood reruns. Source: `analysis/PASS12632_HALOFIT_SCF_BUG.md`.

**Date:** 2026-11-08. **Source:** analysis/w33_20261108_s8_hybrid_shapley_audit.py. **Tests:** tests/test_w33_20261108_s8_hybrid_shapley_audit.py (13/13 desktop pass). **CI:** .github/workflows/w33_20261108_s8_shapley.yml. **Certificate:** data/w33_20261108_S8_hybrid_shapley_audit.json.

**Protocol boundary:** The previously frozen forward prediction analysis/toe_uv/prereg_highz.json was **not edited or re-frozen**. This is arithmetic reconstruction of previously computed fixed-background survey models. It is not new observational evidence, a calibrated p-value or a causal cosmological parameter isolation.

## Prior owners and the question

Pass12631 and latest parallel S8 commits corrected the previously mistaken S7 mechanism: the CPL shear penalty occurs mainly in DES high-redshift tomographic blocks and KiDS high plus mixed blocks, **not** the previously claimed low-z bins. analysis/toe_uv/shear_hybrid.py already computes two-factor hybrid cell chi-squares and prints a nonlinear interaction correction. The new work supplies a reproducible **order-independent** interaction allocation and a complete frozen-data cross-check, without claiming prior ownership of those input chi-squares.

Four conditional hybrid constructions were read from both committed DES and KiDS files:

- F: fading matter power, fading geometry.
- C: CPL matter power, CPL geometry.
- P: CPL power, fading geometry.
- G: fading power, CPL geometry.

Define Delta=C-F, p=P-F, g=G-F. The nonadditive interaction is I=C-P-G+F, so Delta=p+g+I exactly. The frequently repeated contributions p and g *share a fading baseline* and cannot be simply added unless I vanishes.

The symmetric two-factor Shapley decomposition assigns half the interaction to each mechanism:

\[
\boxed{S_{\mathrm{power}}=\tfrac12[(P-F)+(C-G)]=p+I/2,\qquad
S_{\mathrm{geometry}}=\tfrac12[(G-F)+(C-P)]=g+I/2.}
\]

The two values sum exactly to Delta, regardless of the chosen order in which model factors are switched. This is a conventional counterfactual attribution, not independent causal identification.

| Model benchmark | CPL minus fading chi2 | One-factor power | One-factor geometry | Interaction | Shapley power | Shapley geometry |
|---|---:|---:|---:|---:|---:|---:|
| DES Y3, all bins | +2.884483 | +2.201317 | +1.931405 | **-1.248239** | **+1.577197 (54.68%)** | **+1.307285 (45.32%)** |
| KiDS Legacy, all bins | +4.503429 | +3.195358 | +2.038892 | **-0.730821** | **+2.829948 (62.84%)** | **+1.673481 (37.16%)** |

The negative interaction cancels approximately 30.2% of the sum of DES one-factor effects and 14.0% of the KiDS sum. Both power and geometry contribute positive Shapley shares in these full-bin summaries, but their relative attribution is survey-dependent. A universal 55-60% power ratio is **not supported by these two conditional hybrids**.

## Preservation of frozen S8

The new program validates the original frozen preregistration's total, power and geometry numbers against the 4-by-4 cells in both already committed hybrid JSONs, across all low/high/mixed/all tomography blocks. Neither code nor tests overwrite any frozen input.

DES high-bin CPL-minus-fading chi2 is +4.9436 and low-bin is -0.9506. KiDS high is +1.0806 and mixed is +1.8067. These are current benchmark model diagnostics, not outcomes from future DES Y6, Euclid or HSC data. The frozen high-z claim is unchanged and still faces future falsification.

This audit does **not** rerun raw DES/KiDS likelihoods, include independent nuisance/posterior uncertainties, correct overlapping survey covariances, validate baryonic or intrinsic-alignment priors, or establish statistical model preference. Interchanging which model supplies P and geometry is a constructed diagnostic, not a unique split prescribed by physical dynamics.

## Verification and five independent next directions

All **13/13** focused tests passed on the authorized desktop from a separate temporary source copy. An independent GitHub workflow is provided but its outcome must be checked separately.

1. Test frozen S8 directly against a genuinely untouched future high-z shear release, preserving its existing nuisance and covariance scoring contract.
2. Estimate Shapley uncertainty under posterior draws, alternative baryonic/IA priors, and correlated survey sky overlap; avoid interpreting point contributions as significance.
3. Repair the KLT small-f root-bracketing solver with an independently validated boundary-value method and compare against the full scalar dynamics.
4. Construct a physically motivated invariant native Wilson scalar-mass term and measure which compactification subgroup it breaks, as established by the separate H27 orbit theorem.
5. Audit the radiative, discrete-anomaly and mass-generation constraints that must coexist for the dark-sector completion to count as a genuine UV candidate.
