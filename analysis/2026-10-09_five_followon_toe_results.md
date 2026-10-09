# 2026-10-09 — Five follow-on TOE falsification/certification passes (spectra, all-order FI, curvature twirling, finite-shot optics, symmetry of intrinsic space)

## Intake, provenance and boundaries

Checked GitHub master (including parallel Pass11786–11793 and Pass398 formula-search commits), the local checkout, the amended Pass10960 FI no-go and exact support ledger, the corrected eleven-state current-quadrature Wick certificate, the two-mode optical gate, the native Levi Abelian cover, and the old BT1688 **exact H1 irreducibility certificate**. All new outputs are independent reproducible scripts and JSON certificates. No unrelated files or parallel agent changes are to be overwritten.

**Physical scope:** This is a candidate 78-mode quantum Hamiltonian, one specified heterotic model, a single-edge quartic CV optical toy, and one exact graph-cover family. It does NOT derive the measured Standard Model, a full positive *numerical* quantum gap, a string-theory F-flat vacuum, a physical optical gate, or 3+1D Einstein gravity.

## 1. Certified upper enclosure for the second ordered energy, not the excitation gap

Inputs: `analysis/w33_20261009_certified11_wick.py` and its complete outward-rounded `10^-36` rational interval 11x11 Hermitian matrix. Previous work gave `E0<127.595507`. To obtain an independently defensible *ordered second eigenvalue* certificate, diagonalize only the matrix midpoints to **select** two independent trial vectors, rationalize each real/imaginary coefficient to 13 decimals, recompute their bilinear quadratic form using exact rational intervals, and use the elementary Gram-matrix Gershgorin inequality. In exact arithmetic:

```
E_1(H) <= lambda_max(H restricted span{v0,v1})
       <= [max(H2_00^upper,H2_11^upper)+|Re H2_01|^upper+|Im H2_01|^upper]
          /[min(G2_00,G2_11)-|Re G2_01|-|Im G2_01|].
```

The output `data/w33_20261009_second_ordered_upper_certificate.json` records all 22 rational complex vector coefficients, the exact Gram lower and interval quadratic upper. This proves **`E_1(H)<139.665320`** (counting multiplicity); its computed rational value is approximately `139.66531963083764`. A floating eigenvector is only a trial *selector*, not part of the proof. The Hamiltonian is compact with discrete spectrum by the parallel Pass11778 result.

**Strict firewall:** Both this number and `E0<127.595507` are **upper** bounds. Subtraction gives no true gap interval. If the ground is degenerate, `E_1` is not even the first *distinct* excitation. Computing a numerical positive lower gap is an unsolved part of the requested task, not a delivered result.

## 2. Exactly eleven possible one-outsider F-terms, at EVERY polynomial degree

The previous Pass Oct9 degree≤9 enumerator returned 11 gauge-neutral type-B terms and zero type-A terms built entirely from the six FI-cancelling VEV support singlets `n_1,n_19,n_54,n_56,n_80,n_82`.

New theorem: their full exact rational `9x6` U1 charge matrix has **rank six**, hence its kernel is zero. For any of the 170 outside fields `X`, the neutrality equation `Qsupport*n=-Q(X)` has **at most one** rational exponent vector. Compute it with exact SymPy elimination; a solution is an admissible holomorphic one-outsider monomial precisely when all six exponents are nonnegative integers.

The exhaustive list across **all total polynomial degrees** contains **exactly 11 candidate monomials**, with degrees **2:5, 3:2, 4:2, 5:2**, and **zero at degree>5**. All 11 have the necessary point-group sector sum zero. This is **much stronger than an arbitrary degree-9 cutoff**, but still only the nine-U1 gauge-invariance + twist-sector filter. Full Z6-II fixed-point space-group/gamma/H-momentum/discrete R/oscillator rules, superpotential coefficients and phase cancellations remain unresolved. Type-A terms are excluded to all orders by the common negative anomalous charge of all six VEV singlets.

Producer `analysis/w33_20261009_all_order_one_outsider_F_gate.py`; JSON lists each candidate and exact integer exponents.
## 3. Actual-current symmetry twirl kills all 480 local curvature observables

The actual 160 W33 incidence currents satisfy `PSp(4,3)` relabeling covariance. For a current pair e,f sharing a point or a line, `C_ef=i[J_e,J_f]` changes sign when the two currents are swapped. Using BT1688's full explicit list of 25,920 permutations, we found a group element interchanging representative current pairs in **both** orbit types and verified their two complete unordered-pair orbits each contain exactly **240 pairs**. Thus every one of the **480** noncommuting adjacent current-pair curvatures has identically zero *group average* as an operator:

```
(1/25920) sum_{g in PSp(4,3)} U_g C_ef U_g^-1 = 0.
```

Any PSp-invariant state therefore has zero expectation for every such curvature observable, irrespective of whether that state is invariant under the separately discovered dressed antiunitary. This is consistent with the preceding nonzero `+/-1/10` curvature in deliberately momentum-displaced non-invariant coherent Gaussian states. It **does not** establish that the actual ground sector consists only of group-invariant rays or determine spontaneous symmetry breaking.

Producer `analysis/w33_20261009_group_curvature_twirl.py`; exact orbit and reversal permutations preserved in JSON.

## 4. Finite-sample optical inference despite temporally correlated pump-even drift

In the prior single-edge CV toy, independently randomized pump sign `s_i` and two-channel homodyne output define `W_i=P_X,i*(P_Y,i²-v_Y)`; test statistic `S=sum_i s_i W_i`. Under the **sharp randomized null** that pump sign cannot affect any measured readout, the `W_i` are *arbitrary fixed numbers when conditioned on the observed readouts*, and independent balanced Rademacher signs give a nonasymptotic Hoeffding bound

```
P_null[ |S| >= sqrt(2 log(2/alpha) sum_i W_i²) | all W ] <= alpha.
```

Unlike asymptotic kurtosis or third-cumulant z tests, this conditional type-I guarantee holds at **any finite shot count**, with even arbitrarily temporally correlated classical outcomes, *provided pump signs are independently randomized and there is no sign-dependent detector influence under the null*.

A seeded simulation with independent signs, AR(1) electronic drift rho=0.98, pump-even nonlinear quadratic detector crosstalk=0.08 and detector noise tests null, alternative and deliberate pump-sign-dependent detector bias. With alpha=0.01, null trials400 at N3000 gave **1** rejection; alternative160 trials at N24000 gave **159** rejections; the deliberately false pump-odd detector contamination gave **160** apparent detections. These Monte Carlo frequencies are illustrative, not guaranteed detection power or laboratory results. The last case is a deliberately demonstrated *fundamental instrumental loophole*: pump-sign randomization alone cannot distinguish optical physics from pump-odd detector artifacts.

Producer `analysis/w33_20261009_finite_shot_homodyne_randomization.py`, stored seeds/parameters/results in JSON.

## 5. Full-symmetry no-go for a 3D quotient of the native W33 Abelian cover

Existing BT1688, independently rerun in this pass, already proved the **81-dimensional cycle-space H1 representation of PSp(4,3) is complex-irreducible**, from explicit enumeration of all 25920 group elements and the exact graph-chain character formula:

```
chi_H1(g) = fixed_incidence_edges(g)-fixed_vertices(g)+1;
<chi_H1,chi_H1> = (sum_g chi(g)²)/25920 = 25920/25920=1.
```

The October9 intrinsic graph cover is the universal Abelian cover of the same 80-vertex, 160-edge Levi graph, with deck lattice `H1(G,Z)=Z^81`. **NEW application of the existing theorem:** a `PSp(4,3)`-equivariant rank-three deck quotient `Z^81 -> Z^3` cannot exist. Tensoring any surjective Z-linear equivariant map with C would create a nonzero quotient of the irreducible complex 81-dimensional representation of dimension3, a contradiction. In fact no nonzero equivariant quotient of any rank less than81 exists.

This is a clean **negative selection rule**. The full Sp(4,3) symmetry (or its projective quotient) must be broken/restricted to a proper subgroup, or one must change the geometric/dynamical construction, before a 3D lattice quotient becomes possible. This does not forbid an emergent 3D spacetime by wholly different, nonlinear, interacting or symmetry-broken mechanisms.

Producer `analysis/w33_20261009_no_equivariant_three_space.py`, which verifies and **credits** the existing BT1688 result rather than reinventing its irreducibility claim.

## Research conclusion and validation

The new results offer: a **second ordered upper spectral bound, not a numerical gap**; an **all-orders exact F-term candidate enumeration, not a superpotential**; a **full unitary-group selection rule, not a vacuum symmetry classification**; an **exact finite-N randomization null, not a hardware demo**; and a **specific symmetry-theoretic 3D quotient obstruction, not a theory of space-time**. Producers preserve raw sources and use isolated output paths. The original 5-front correction from Pass11786 and the parallel Pass11793 order-four matter parity results remain intact.

Strong next independent tests: (1) derive computable full-H lower spectral/gap bounds from an explicit coercive sum-of-squares; (2) obtain each outsider's fixed-point/H-momentum/R-charge data from original orbifolder and test actual string couplings; (3) determine the actual finite ground-sector representation and PSp/T breaking susceptibility; (4) calibrate detector sign-dependent bias using pump-off/witness-off controls; (5) classify rank-three quotients after explicit minimal symmetry breaking and test their dynamical stability.
