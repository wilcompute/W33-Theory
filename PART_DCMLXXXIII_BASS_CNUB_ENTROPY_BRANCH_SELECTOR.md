# Part DCMLXXXIII (983) - Bass/CnuB Entropy Branch Selector

**Date:** 2026-05-18
**Series:** W(3,3) Theory of Everything
**Status:** VERIFIED BRANCH-SELECTOR AUDIT

---

## Why this part exists

DCMLXXXII separated the live W(3,3) Ihara-Bass determinant from the
coefficient-12 shadow.  Reading that result against the CnuB/CMB temperature
ratio exposes a sharper selector:

\[
\boxed{\text{live Bass-11} \Longleftrightarrow 4/11.}
\]

The coefficient-12 branch is still useful arithmetic structure, but it gives
the wrong entropy denominator.

---

## Standard entropy packet

In the instantaneous-decoupling limit, electron-positron annihilation heats the
photon bath after neutrino decoupling.  The electromagnetic entropy degrees of
freedom are
\[
g_{\rm before}=2+\frac78\cdot 4=\frac{11}{2},
\qquad
g_{\rm after}=2.
\]

Therefore
\[
\left(\frac{T_\gamma}{T_\nu}\right)^3
=\frac{g_{\rm before}}{g_{\rm after}}
=\frac{11}{4},
\qquad
\boxed{
\left(\frac{T_\nu}{T_\gamma}\right)^3=\frac{4}{11}.
}
\]

This is the standard CnuB/CMB entropy ratio.  Precision neutrino-decoupling
calculations then package the small spectral distortions as \(N_{\rm eff}=3.044\),
but the denominator selector remains \(11\).

---

## W(3,3) branch comparison

For W(3,3),
\[
k=12,\qquad \mu=4,\qquad q_{\rm Bass}=k-1=11.
\]

The live nonbacktracking branch gives
\[
\boxed{\frac{\mu}{k-1}=\frac{4}{11}},
\]
exactly matching the standard entropy ratio.

The coefficient-12 shadow gives
\[
\boxed{\frac{\mu}{k}=\frac{4}{12}=\frac13}.
\]

The exact branch gap is
\[
\frac{4}{11}-\frac13=\frac{1}{33}.
\]

Equivalently, on the photon-heating side,
\[
3-\frac{11}{4}=\frac14.
\]

Thus coefficient 12 is the wrong CnuB entropy branch for the same reason it is
the wrong live graph-zeta coefficient: it keeps the immediate return channel
that Ihara-Bass removes.

---

## Interpretation

This part promotes a branch selector, not a new continuum proof:

- Ihara-Bass deletes one immediate-return channel from the 12-regular graph,
  leaving the live nonbacktracking denominator \(11\).
- Standard CnuB reheating uses the reciprocal denominator \(11/4\), hence
  \((T_\nu/T_\gamma)^3=4/11\).
- The coefficient-12 shadow predicts \(1/3\), so it fails the entropy branch
  test exactly.

The new theorem target is therefore not another finite graph-RH claim.  The
next target is a functorial entropy-decoupling bridge explaining why the W(3,3)
return-channel deletion is the finite shadow of the CnuB reheating denominator.

---

## Boundaries

This audit does not claim:

- direct CnuB detection;
- a full derivation of neutrino decoupling dynamics from W(3,3) alone;
- the classical Riemann Hypothesis.

It verifies the exact arithmetic selector that the live Bass-11 branch, and not
the coefficient-12 shadow, is compatible with the standard \(4/11\) CnuB
temperature-cube ratio.

---

## Static external references

- PDG 2025, *Neutrinos in Cosmology*: standard
  \(T_\nu/T_\gamma=(4/11)^{1/3}\) and \(N_{\rm eff}=3.044\) correction packet.
- Rangarajan 2017, *A Combinatorial Proof of Ihara-Bass's Formula for Regular
  Graphs*: Ihara zeta is built from prime nonbacktracking cycles and the
  regular determinant carries the \(d-1\) term.

The verifier records these as static source facts; it has no runtime internet
dependency.

---

## Executable artifact

- Verifier: `verify_dcmlxxxiii_bass_cnub_entropy_branch_selector.py`
- Tests: `tests/test_dcmlxxxiii_bass_cnub_entropy_branch_selector.py`
- Data: `data/dcmlxxxiii_bass_cnub_entropy_branch_selector.json`
- Result: `PART_DCMLXXXIII_BASS_CNUB_ENTROPY_BRANCH_SELECTOR_results.json`
