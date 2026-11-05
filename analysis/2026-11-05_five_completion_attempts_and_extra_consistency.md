# Five concrete TOE completion attempts and additional cross-checks

November5,2026. Continues science191e18a5d/receipt78b092bcc. All five investigations were executed as named mathematical/model calculations. None establishes a complete quantum-gravity UV completion, a full Standard-Model RG calculation, an all-configuration local chiral measure, or a nonlinear first-class gravity algebra. The distinction between executing a test and solving its physical target is essential.

## Incoming work and ownership

Read the complete incoming analysis/PASS12613_12615_ORBIFOLD_ROUTE.md at eaf9911c8. It owns the finite SU5 missing-partner search, the orbifold fragment construction and its axion-quality caveat. Its zero-result covers the specified representation catalogue, not every possible splitting mechanism. [Agrawal-Nee-Reig](https://arxiv.org/abs/2511.21830), revised October2026, supplies the primary orbifold axion argument. This packet does not override that construction with an uncited rediscovery.

Read the complete prior12026-12033 report, particularly12030's actual native-compatible4D determinant torus, charge-cubic sum, coarse-mesh failures and Lipschitz gap bound. That prior calculation is broader than this packet's opposite-charge toron control; it already checks the10+bar5 anomaly sum. The new calculation is an independently assembled isotropic2^4 four-torus using our previously published overlap source. Neither is an all-configuration local measure.

The previous45-report reading and PDF pages1-53 coverage remains as recorded in data/toe_20261105_change_reading_coverage.json. This continuation does not claim full-PDF or full-history reading. Result searches and prior-source citations are recorded separately; search counts never establish semantic priority.

## 1. A concrete anomaly-free protection variant, including its cost

Producer: analysis/toe_20261105_five_fronts_model_completion.py; matching data certificate.

Add a gauged U1_X, scalars S,T with integer charges2,2n, and the following LH fermions. D denotes the SM vectorlike representation(3,1,-1/3) with its conjugate.

| Copies of Dirac pair | LH X charges | Mass term |
|---|---|---|
| n colored D pairs |(-1,-1)|S D Dbar|
| one colored D pair |(n,n)|Tdag Dprime Dprimebar|
|3n SM-singlet pairs |(1,1)|Sdag N Nbar|
|three SM-singlet pairs |(-n,-n)|T Nprime Nprimebar|

SM fields have X0. SU3²X and Y²X cancel between the colored blocks; YX² cancels inside each conjugate-hypercharge pair. There are no extra weak doublets. The singlets cancel the remaining gravitational and cubic anomalies exactly. The tests independently sum the explicit Weyl inventory, not just the producer's aggregate formula.

The physical gauge-invariant phase is psi=n thetaS-thetaT. Its primitive integer coefficient vector(n,-1) gives period2pi after quotient by gauge orbits; QCD couples once to psi, so NDW1. E/N remains2/3 because all colored representations are D singlets. These anomaly/phase statements do not establish realistic cosmology.

The first phase-sensitive pure scalar invariant is S^n Tdag, dimension n+1. For scalar kinetic normalization S=FS/sqrt2 exp(i thetaS),T=FT/sqrt2 exp(i thetaT), the physical axion constant is

    fa=FS FT/sqrt(n² FT²+FS²).

With equal FS=FT=F and fa input1e11GeV, F=fa sqrt(n²+1); it cannot be identified with fa. At supplied coefficient magnitude1 and reduced Planck suppression, n13 is the first tested value whose leading scalar operator passes the phase-uniform quality bound. It has dimension14, F1.30384e12GeV and sufficient theta bound2.67846e-12. The higher protection requirement than the earlier one-scalar table follows from the larger actual vevs.

This provides an explicit escape from the unchanged-inventory obstruction by CHANGING the inventory:14 colored Dirac pairs and42 singlet pairs replace D+2Q. It is not the old candidate repaired for free. With all Yukawas assumed1 at one common threshold, delta b=(3.73333,0,9.33333) in SU5-normalized gauge convention. The12 crossing occurs near4.45e12GeV, but the third inverse coupling misses by-8.44946. It fails that restricted unification screen. A different spectrum or threshold fit is additional model-building work.

The general gauged accidental-PQ approach is established in [Babu-Dutta-Mohapatra](https://arxiv.org/abs/2412.21157); this transparent mirrored-singlet variant and its explicit resource cost are controls, not a claim to invent protected axions.

### An additional obstruction: complete SU5 multiplets do not repair the unchanged candidate

One might try preserving one-loop unification differences by adding only complete SU5 multiplets. Define C=A_Y²X+A_SU2²X-(8/3)A_SU3²X. In any complete SU5 irrep with a uniform X charge, invariant traces give A_SU2=A_SU3 and A_Y²=(5/3)A_SU3, hence C0. This is true in arbitrary representations; exact5,10,24weight controls verify the normalization. The single-Higgs SM Yukawa assumptions likewise give C_SM0. But the original D+Q+Q mass signs require C=qSigma. Thus ANY number of complete SU5 representations with X commuting with SU5 cannot cancel that candidate's anomalies while charging Sigma. Incomplete/split-X multiplets, changed mass generation, altered SM Yukawas or inflow are needed. This connects the prior PQ obstruction to the incoming GUT completion, rather than assuming that extra unified matter automatically fixes it. The invariant-trace method is classical, not a new general theorem of SU5.

### Extra checks: residual symmetry, decays and a Landau cost

For odd n13 the scalar condensates preserve gauge Z2; all new fermions are odd and SM fields are even. Ordinary heavy-SM mixing is forbidden; the lightest odd particle is stable. A dimension6 Lorentz scalar(D N)(uc ec) has X0 and Y0 and can mediate colored decay with suitable masses and Wilson coefficient. Decay kinematics, lifetime, thermal production and dark relic abundance have not been calculated.

Tr(YX)=0, so one-loop kinetic mixing vanishes for this inventory. The positive U1 coefficient is bX=1682.6667 in the printed integer-charge normalization. A common-threshold formal pole screen gives initial gX below about0.07489 to avoid a pole before the supplied MU. At gX0.1 the formal pole is only about109threshold units away. These are necessary perturbative diagnostics with supplied masses; they are not a coupled running solution of this new protection model.

## 2. Derive the Yukawa equation before performing the coupled flow

For three disjoint heavy Dirac species with dimensions D_i=(3,6,6), explicitly form both symmetric real-scalar Yukawa matrices, including the Sigma/Sigma-dagger signs. Apply the one-loop real-scalar tensor expression. The matrix result is

    16pi² beta_yi=yi[yi²+sum_j D_j yj²-6sum_a C_a(i)g_a²].

In the equal-y limit the cubic coefficient is1+15=16, not the old parent's3+15=18. For one color triplet it gives4, agreeing with the explicit one-loop term in AppendixB of [SMASH](https://arxiv.org/html/1610.01639), beta_y. This is a substantive correction to the approximate parent equations; the previous normalization-only audit intentionally held those equations fixed. Its mathematical controls of that old system remain valid, but its numeric flow is not silently reused as the corrected physical model.

The numerical producer now evolves ten independent coordinates: gY,g2,g3,yt,lambdaH,lambdaS,lambdaHS,yD,yQ1,yQ2. It uses the original D+2Q spectrum, separate activation thresholds, distinct EW terms in the heavy Yukawas, scalar-portal backreaction and canonical yi(Mi)=sqrt2 Mi/f. The potential convention is

    V=lambdaH(HdagH)^2+lambdaS(SdagS)^2+lambdaHS HdagH SdagS.

Tree elimination gives lambdaH_low=lambdaH_high-lambdaHS²/(4lambdaS), verified by independent symbolic elimination. This makes the portal convention explicit instead of copying a threshold formula with a different factor of2.

Eighteen supplied boundary points cover f5e10,1e11,2e11GeV, lambdaS .003,.03,.3 and common versus(1,.7,1.4) mass splitting, with threshold uplift delta_lambdaH .02. A final EFT-ordering audit rejects nine points before integration because a heavy fermion would activate below the radial scalar; that regime requires broken-phase axion/mass operators and matching, not the full complex-scalar beta functions. Among the nine supported orderings, five integrate through MU and four stop early. An earlier numerical18point sweep was therefore narrowed rather than passed off as a complete EFT calculation. Successful integration is NOT vacuum viability: all supported points sample negative lambdaH for the illustrative one-loop SM inputs, and some lambdaS trajectories also cross zero. None is labelled an absolutely stable viable model. The known sensitivity of the Higgs instability scale to higher loops remains material.

This is a closed one-loop top-only SM and diagonal-heavy-Yukawa truncation with tree step matching. Full SM flavor, sterile or heavy-SM mixing matrices, finite scheme/mass matching, two-loop equations and a UV vacuum are not computed. The request for a COMPLETE physical running calculation remains open beyond this explicit implementation; no precise axion-mass ceiling is claimed.

## 3. A gravity repair can raise M5 while destroying the original KK spectrum

Try a flat positive brane Einstein term first:

    M4²=M5³ L+Mbrane².

For fixed M4,L and nonnegative Mbrane², this cannot raise M5. Substituting M5=the fitted MU requires a negative brane coefficient; that is rejected as a healthy repair.

Next introduce a conventional5D Einstein-AdS interval with warp factor exp(-ky), tuned Randall-Sundrum boundary tensions and supplied length L. Its Planck relation is

    M4²=M5³[1-exp(-2kL)]/(2k).

Setting M5=MU gives k/M5=1.32563e-6, weak curvature relative to M5. But for the8-15micron inputs, kL exceeds1e19. The warped IR KK scale behaves as3.83k exp(-kL), exponentially different from1/L. Thus this explicit action repairs the Planck-scale inequality only by abandoning the approximately flat micron KK spectrum used by the cosmology model. The certificate exports logarithms to avoid numerical underflow. Radius stabilization, vacuum selection and quantum UV completion are not supplied.

Warped gravity is established [Randall-Sundrum](https://arxiv.org/abs/hep-ph/9905221); [dark-dimension GUT constraints](https://arxiv.org/abs/2409.01405) motivate the compatibility test. Neither literature nor this finite scale calculation licenses declaring one shared TOE action complete.

## 4. Actual4D determinant-line topology, with a resolution firewall

Producer: analysis/toe_20261105_global_measure_and_lorentz_branches.py; matching data certificate.

Use the published4D Wilson-overlap regulator on2^4sites with flux in plane34 and two periodic boundary-link torons in directions1,2. Positive-kernel eigenvectors supply local chiral frames. Determinant overlaps and parameter plaquettes give Chern sums-1 for charge+1 and+1 for charge-1 at meshes8 and12. Frame ranks are32; minimum sampled kernel gap is0.1939366; all neighboring overlaps are nonsingular.

A refined40mesh charge+1 run adds the standard12030 Lipschitz control: each toron derivative has norm at most|q|, hence the whole-torus gap is bounded below by sampled_gap-2pi|q|/N, with numerical rounding caveat. This controls rank continuity, not by itself the Chern integer. Mesh convergence and determinant overlap diagnostics are stored; an interval-certified topological computation is not claimed.

The opposite-charge sum cancels on this tested two-cycle. That is a vectorlike control, not a newly constructed anomaly-free chiral measure. The actual native12030 predecessor already treats the10+bar5 charge-cubic cancellation and demonstrates coarse-mesh false integers despite a positive gap. The higher charges(-9,-5,-1,7,8) are NOT certified on our coarse spatial lattice. A local reconstruction current, all noncontractible configuration loops, full non-Abelian anomalies and volume-uniform locality remain open. This investigation names and executes the obstruction test rather than presenting a determinant or anomaly sum as the missing measure.

Primary framework: [Lüscher](https://arxiv.org/abs/hep-lat/9811032). No blanket claim that the literature lacks a construction is made.

## 5. Boundary-complete complex continuation repairs the flat-action failure

Construct a4D simplex with time-axis length2, insert its barycenter and perform1to5 refinement. Continue the FULL Regge-plus-boundary action from Euclidean signature along diag(exp(-i alpha),1,1,1), alpha0to pi-epsilon, tracking individual normal and area square roots and dihedral angle sheets. Include actual boundary exterior angles. No reference-action subtraction is used.

The flat internal deficits are below2.3e-15; the direct finite-difference action gradient has norm4.75e-9. Three actual internal-vertex motions preserve the boundary action to about5.4e-15. Doubling160continuation steps to320 gives the same endpoint action at printed precision. The independent Schlaefli hinge gradient agrees with action differences to4.76e-9.

At the flat point the five-by-five Hessian has one singular value about6.25 and four below1e-7, as four internal vertex motions require. A supplied.001off-shell squared-edge perturbation produces deficit.00806 and Hessian singular values approximately6.146,.01179,.003071,.003071,.000997. This quantifies the loss of the flat Hessian nulls in that off-shell diagnostic. It is not by itself a proof about a field-dependent nonlinear gauge algebra.

This is progress beyond the prior nine-simplex principal-product-square-root diagnostic with nonzero flat gradient, on a DIFFERENT one-interior-vertex triangulation. It does not yet repair the nine-simplex model, define a causal quantum path integral, establish branch uniqueness for arbitrary triangulations or construct canonical lapse/shift brackets. The action is complex with boundary-joint contributions; no unjustified reality/positivity claim is made. The explicit analytic-continuation approach is established in [Borissova-Dittrich](https://arxiv.org/abs/2303.07367).

## Reproduction and validation

Run both producers and analysis/toe_20261105_five_completion_validation.py. Nine independent focused tests cover explicit anomaly sums, primitive axion phase and metric, protection-spectrum cost, complete-SU5 repair obstruction, tensor Yukawas, portal elimination, canonical threshold activation, warped scaling and actual geometry certificates. The initial combined suite passed40tests; the extended final suite has41tests, whose actual status and hashes are recorded in the final validation receipt. Server V8 separately checks39integer anomaly cases, the first quality dimension, beta coefficient and warp relation. Remote Desktop Commander executes PC work while server checks and literature/repo searches proceed.

The initial new-test run had6PASS,2FAIL: a symbolic test incorrectly required the signed radial fluctuation to be positive, and another demanded exact equality of a floating Chern sum with1. Both test errors were repaired, with the failure history retained. No physical coefficient or result was changed to satisfy them.

## Five independent next investigations

1. Classify mixed fermion PQ-breaking operators and actual relic decays in the protected spectrum before claiming full axion quality/cosmological viability.
2. Generate complete multi-loop matrix RG equations and finite matching, including allowed mixing/sterile interactions and measured-input uncertainties.
3. Construct a stabilized gravity sector preserving an acceptable KK spectrum and demonstrate the gauge sector's UV validity.
4. Build a local integrable chiral measure on the actual native configuration space, checking every global loop and a uniform locality bound.
5. Extend the continued Lorentzian boundary action to the existing two-interior-vertex complex and derive canonical nonlinear constraints.
