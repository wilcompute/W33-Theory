# W33 Round 7: anomaly-safe matter, negative interaction region, calibrated optics, E8(-24), conditional RG scale
**19 October 2026.** Worktree isolated from modified user checkout. Sources: prior W33 passes 10949 (E8 real forms), 11681 (tensor bracket), 11687-91 (matter), and October 19 round 6 exact heptad polynomials. **No physical TOE, new measured physics, real optical hardware, or parameter-free mass scale is claimed.**

## 1. Matter and anomaly consistency
The conventional E6 trinification 27 under SU3_C x SU3_L x SU3_R is (3,bar3,1)+(bar3,1,3)+(1,3,bar3). Its three SU3 cubic anomaly contributions are (3,-3,0),(-3,0,3),(0,3,-3): each gauge factor is anomaly-free. Each SU3 factor sees six Weyl triplets or three Dirac-flavor equivalents; restriction to the standard SU2 in that SU3 gives an even six doublets, passing the mod-two Witten test.

This is standard E6 algebra, NOT a 9 fundamental of SU9 inside E8 adjoint. Since SU9->E8 factors through SU9/mu3, a lone chiral SU9 fundamental 9 is not an E8 adjoint submodule and in a separate gauged SU9 theory would have nonzero cubic anomaly +1. Adding a vectorlike 9+bar9 repairs SU9 gauge anomaly but doubles degrees of freedom and does not derive the earlier special 9-mode Hamiltonian or chemical potential. Gauge anomalies of a global, nongauged symmetry are not at issue. The anomaly-safe trinification 27 does not itself supply a chiral Standard Model or explain observed masses.

## 2. Analytic outer bracket of the negative-kappa global phase boundary
The exact inequality from the earlier packet is F_T(w)-F_T(single)>=a(T) C(w), where a(T)=3T[1-(1+1/T)exp(-1/T)]/[3+6exp(-1/T)], for all normalized nonnegative 120-rate w and T>0. Therefore a single tick remains a global minimum for kappa>=-a(T).

The five EXACT integer characteristic-polynomial families for uniform seven-point noncommuting heptads determine five algebraic spectra. For each T choose the lowest Gibbs energy F_h(T) among them. Its interaction C=4/7. If
\[
\kappa<-\frac74\big(F_h(T)-F_{\rm single}(T)\big),
\]
the explicit heptad competitor beats ALL single ticks and ALL configurations with C=0, since F_T(w)>=F_T(single). Hence a region in which every global minimizer must have positive noncommutation is mathematically proven to EXIST. This does NOT certify a heptad is globally optimal there.

At T=.5: global singleton sufficient condition kappa>=-0.2337325527; explicit noncommuting competitor excludes a singleton for kappa<-0.3578835141. The intermediate region is unsolved. Threshold expressions use exact algebraic spectra, but quoted decimals are floating evaluations, NOT rigorous outward-rounded interval enclosures. Continuous 40-point mass optimization remains open.

## 3. Actual component controls for the 18-mode single-photon trace circuit
The 2-path x 9-mode circuit from round 5 uses four projector phase masks, four G/Gdag blocks, and two path Hadamards; round 6 decomposed each G via complex Givens mixers. New test adds heterogeneous internal **output-mode amplitude** transmission ell_j in [0.68,0.96] AFTER the nontrivial signal W. With a photon input in basis j, the raw detector path difference obeys p0(j)-p1(j)=ell_j Re W_jj. A W=I reference measurement gives ell_j exactly, enabling mode-by-mode correction:
\[
\delta_{\rm calibrated}
=1-\frac19\sum_{j=0}^8
\frac{p_{0,\rm signal}(j)-p_{1,\rm signal}(j)}
{p_{0,\rm reference}(j)-p_{1,\rm reference}(j)}.
\]
It recovers the exact ideal delta=8/27 and commuting null zero. A SINGLE GLOBAL visibility correction instead produces bias -0.00948509485 for this loss profile.

In 800 simulated repetitions, each using 3,500 photons per input j per condition (identity calibration, signal, commuting null), the total per repetition was 94,500 photons. At a preselected half-ideal threshold the synthetic detection fraction was 100% and null false alarm fraction 0%. No real photon observations were collected. Mode cross-talk, loss INTERNAL to W, phase drift, detector noise, afterpulsing and correlated errors are not corrected by the diagonal stationary-loss model. Actual fabrication and process tomography remain necessary.

Prior art: 2026 intensity-only local variance calibration https://arxiv.org/abs/2607.14759 ; an 8x8 Clements programmable photonic mesh https://www.nature.com/articles/s41566-026-01997-x.

## 4. E8(-24) as an explicit SU9 tensor real structure, plus Clifford firewall
**Prior art alert:** repo Pass 10949 ALREADY certifies E8(-24) using clock-root parity and 56-dimensional Freudenthal geometry. The present contribution is a simple explicit implementable realization in the existing 9x9 + 84 + 84 SU9 tensor bracket, and a test of its Clifford stabilizer.

Take compact conjugation sigma_c(A,x,y)=(-A dagger, conjugate y, conjugate x) and D=diag(1,1,1,1,1,1,1,-1,-1) in SU9. Let theta=Ad_D on all three tensor grades and sigma_24=theta∘sigma_c. The Pass11681 complex E8 bracket is compatible with this conjugate-linear involution. The compact even sector has dim136 (52 from sl9 and 84 from exterior pair); odd sector has dim112 (28+84). Thus the fixed real form is E8(-24) with Killing signature (112 positive,136 negative), maximal compact E7_compact+su2. The node6 E8 root parity count independently gives 128 compact roots plus 8 Cartans. Maximum random mixed-bracket/real-structure residual ~1.36e-14.

**Unexpected Clifford restriction:** among five SU9 Cliffords tested, only S1 and CZ preserve this PARTICULAR D-defined E8(-24) real form. F1, SUM, SWAP preserve the complex E8 but change its selected real-form involution. A theory requiring the full Clifford as a PHYSICAL vacuum symmetry must address this incompatibility or alter the vacuum/representation. This is not a no-go for all alternative conjugate real structures.

External mathematical context: E8(-24) maximal compact E7 x SU2 and noncompact (56,2), https://msp.org/agt/2015/15-5/agt-v15-n5-p05-s.pdf.

## 5. Dimensional transmutation: consistent conditional route, not a fixed mass
For an SU3 gauge factor with the three effective Dirac-flavor equivalents in the specified trinification 27, ignoring all scalars and thresholds, one-loop b0=11N/3-2Nf/3=9. Then
\[
\mu dg/d\mu=-b_0g^3/(16\pi^2),\qquad
\Lambda=\mu\exp[-8\pi^2/(b_0 g(\mu)^2)].
\]
The second expression is an RG-invariant integration constant in the given one-loop toy theory; four scale-separated samples confirm it numerically. Assuming mu=10^12 GeV and arbitrary UV g=.35,.5,.65 yields Lambda respectively ~7.90e-20 GeV, 5.75e-4 GeV, and 9.60e2 GeV. W33 counts do not determine UV g or mu, so do NOT predict absolute scale or a measured particle mass. Scalar contributions, thresholds, high-loop effects, symmetry breaking, gravity and UV completion remain missing.

## Reproduction
- analysis/w33_20261019_round7_matter_rg.py => data/w33_20261019_round7_matter_rg.json
- analysis/w33_20261019_round7_competing_phase.py => data/w33_20261019_round7_competing_phase.json
- analysis/w33_20261019_round7_optical_mode_loss.py => data/w33_20261019_round7_optical_mode_loss.json
- analysis/w33_20261019_round7_e8m24_involution.py => data/w33_20261019_round7_e8m24_involution.json
- tests/test_w33_20261019_round7.py

**Evidence firewall:** proof of a real form and standard representation anomaly cancellation; exact variational exclusion formula but incomplete phase diagram; purely synthetic optical loss protocol; RG integration with free UV coupling; no unique TOE prediction.
