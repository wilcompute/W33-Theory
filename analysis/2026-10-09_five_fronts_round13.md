# W33 Theory of Everything — independent frontier experiments, Round 13
**Date:** 9 October 2026. **Status:** five prior proposals investigated plus three independent out-of-the-box constructions. Source and output certificates accompany all claims.

## Intake and provenance

Authorized local repo `C:\Repos\Theory of Everything` fast-forwarded to live GitHub `master` `57feb213c95debf9e68d749e8a7f28ccd921a19b` from prior research commit `623b6c8cb183f943aece1168af9d8ca466a7eb3a`. The intervening commit updated only Pass398's formula-universe JSON. Existing dirty source `.continuity/*`, agent instructions, Pass10956 and many unrelated scratch files are intentionally unchanged. All new files have unique Round13 names.

The carrier `W(3,3)` is SRG(40,12,2,4), 40 points, 40 lines, 160 point-line flags. `PSp(4,3)` has order 25,920. The 81D Levi cycle homology is the unique irreducible Steinberg module: **pre-existing BT1688 / September 2026 group-theory ownership**.

## 1. Full quantum Hamiltonian: dual estimates on all 160 codimension-one factor zeros

Earlier Pass11769 built the **actual quantum model** `H=sum_e (z_e(U_e.P+a))^2`, `z_e(q)=V_e.q+a`, `a=1/sqrt20` on `L²(R^78)`; Pass11778 proved qualitative ground energy >0 and compact resolvent, but no numerical global lower bound. Our prior Round12 proved the cycle-weighted pointwise scalar bound at a SINGLE `q_e=-a V_e/||V_e||²`, where the original naive harmonic-mean lower potential fails because `z_e=0`.

This pass **exhausts all 160** representatives. At each one:
- Remove edge `e` from the 80-vertex Levi graph and take a length-seven alternate path, returning an alternating signed 8-cycle `c`.
- The transport vectors satisfy `U^T c=0`, `ones^T U=0`, `sum c=0`.
- Then `w=ones-c` has `w_e=0`, `sum w=160`, `U^T w=0`.
- With exact rational `t_i=(3120-(40V_i).(40V_e))/3120`, weighted Cauchy certifies
```
V_opt(q_e)>= a^4*160^2 / sum_{i:w_i!=0} w_i^2/t_i^2.
```
Every **one of 160** independent exact rational calculations returns precisely
```
                  25600/77571 ≈ 0.330020239522502.
```
Thus the earlier coarse `V_CS(q_e)=0` is an artifact of a deliberately suboptimal dual vector, *not* a genuine local zero for any of the 160 ordinary factor-zero representatives. This does NOT cover arbitrary points on those hyperplanes, simultaneous vanishing factors, the known genuine classical zero, infinity or a quantitative global `E0` gap. No unsupported global mass-gap claim.

Producer: `analysis/w33_20261009_all160_single_factor_dual_bounds.py`; complete rational histogram in JSON.

## 2. Physical heterotic F-flatness: the 16 rank-three Yukawa candidates face many additional F-term risks

Prior Pass11797–11801 benchmark sources own the 176-sector field metadata, parity, corrected gamma-aware `R/nonR`, FI core and 13-field VEV invariant ring. Round11 found **sixteen distinct 3-singlet supports** admitting necessary integer-gauge and corrected-R up Yukawa rank3 and colored 7x10 matching rank7. Round12 checked the original WSL orbifolder finite C exports: only four n83 supports have ten exactly named finite colored couplings each; this was not an amplitude test.

New all-support F-term necessary-rule scan: for each of sixteen 13+3 VEV supports, enumerate every **parity-even, hypercharge-zero, fully non-Abelian-singlet outsider** `X` and seek a holomorphic integer charge-neutral, gamma-corrected R/nonR-allowed term `W ~ X * VEV monomial`, with the same <=72 exponent bound and neutral meson powers as the published previous screen. The exact source `Pass11797.selection` is called for each positive witness. The counts of potential outsider `F_X`-tadpole monomials across sixteen supports are
```
2 supports: 13 outsiders; 2 supports: 15;
6 supports: 19 outsiders; 6 supports: 21.
```
For priority `(n51,n79,n83)`, **15 of 24** checked parity-even SM/non-Abelian singlet outsiders admit necessary-rule integer monomials; `(n65,n79,n83)` yields **13 of 24**. The leading candidate is the *previously known* `n81*n17*n82` with just TWO old FI insertions. Since `n17,n82` are nonzero on all sixteen candidate supports, **IF** a nonzero worldsheet coefficient of this cubic exists, every candidate must arrange cancellations in `F81` (or in other condensate derivatives when `n81` itself condenses).

This is a **conditional F-flatness hazard**, not proof any selected candidate fails. Our test enforces exact gauge and recovered corrected discrete-charge **necessary** constraints; fixed-point space-group, Rule4/5/6, oscillators, instanton existence, nonzero amplitudes, all-order cancellation and nonsinglet outsider F terms remain unresolved. Existing `C` export absence is not a zero-amplitude theorem. Full physical vacua and masses are **not established**.

Producer: `analysis/w33_20261009_all16_heterotic_F_tadpoles.py`, all 16 source-backed positive monomials JSON. The two top choices additionally have independent focused source audit in `...selected_heterotic_F_tadpole_screen.py`.

Relevant prior-art CFT constraints, not discoveries of this pass:
- Kobayashi et al., *Revisiting Coupling Selection Rules in Heterotic Orbifold Models*, [arXiv:1107.2137](https://arxiv.org/abs/1107.2137);
- Cabo Bizet et al., *R-charge conservation and more*, JHEP05(2013)076, [DOI](https://doi.org/10.1007/JHEP05(2013)076).

## 3. True ground-state symmetry: exact 16-dimensional curvature lower-rank certificate

The actual quantum ground-state irrep remains an open problem, with only restricted variational bounds and Pass11778's qualitative spectral theorem. Round12 established an exact **single nonzero** effective magnetic curvature component of the full 78D quantum kinetic connection at the rational symmetry-breaking configuration
```
q = (e0-e39)/(10 sqrt20).
```
The connection `A(q)=K(q)^-1 b(q)` enters first-order terms; a scalar phase can remove it locally only if the 2-form `dA` vanishes.

This pass calculates the **entire 78×78 antisymmetric curvature matrix** in exact modular arithmetic, using the corrected cotangent-coordinate Jacobian and exact inverses modulo primes **10007, 10009, 10037**. The rank is **16 at all three primes**, which rigorously proves *rational rank >=16*. Real SVD independently also gives numerical rank16. We have NOT produced an exact upper bound rank<=16 over rational numbers, so the currently rigorous assertion is `rank_Q(dA)>=16`, numerical evidence suggests equality at this configuration.

This strengthens the no-scalar-gauge obstruction and tells future vacuum calculations that the effective connection has multiple nontrivial 2D magnetic planes. It does **not** demonstrate ground-state degeneracy, identify its PSp representation, compute a numerical E0 lower enclosure or describe an actual electromagnetic field.

Producer: `analysis/w33_20261009_quantum_curvature_fullrank_modp.py`.

## 4. Photonic sham design: exact observational-identifiability no-go

Round12 proved a level-alpha clipped-shot/frame-Rademacher statistical test robust to bounded shot faults, with numerical shams; the new independent question is whether statistics alone can distinguish real photon nonlinearity from detector corruption.

Construct two causal mechanisms using identical randomized pump sign `S`, gate sign `G`, route sign `R`, centered intensity proxy `Q` and clean reference noise:
```
A: optical real nonlinear term theta*S*G*R*Q, electronics clean;
B: optical nonlinear term exactly ZERO, downstream electronics injects
   the identical theta*S*G*R*Q.
```
For *every* joint distribution of all randomized inputs and noise, the observed detectors are identical in the two mechanisms, before and after arbitrary deterministic shot clipping; their **total-variation distance is zero**. Thus for equal prior odds the Bayes discrimination error is exactly 1/2 even with infinite samples. A 240,000-sample paired seeded array verifies the exact identity and a strong artificial lock-in statistic in both models.

This falsifies the idea that randomized triple-sign lock-in plus a huge signal-to-noise ratio ALONE identifies physical optical nonlinearity. A separately calibrated upstream optical intervention, sensor swap, matched dummy path or another experimentally justified causal exclusion restriction is necessary. We did not implement or measure real sensors.

Producer: `analysis/w33_20261009_optical_threeway_identifiability_nogo.py`.

## 5. The creative geometry result: exact PSp-equivariant **86,400** optimal three-mode selectors and their FIVE symmetry orbits

The previous rank81 universal Abelian cover belongs to `analysis/w33_20261009_universal_abelian_cover.py` (prior). In Round12 we exhaustively measured 85,320 arbitrary spanning-tree *chord* triples and found minimum anisotropy 83/80; that was a BASIS-DEPENDENT family.

This pass removes the spanning tree entirely. For the canonical signed 80×160 Levi incidence matrix `B`, let `L=BB^T`, and `Pi=I-B^T L^+ B` the orthogonal projector onto the **81D cycle space**. We constructed an exact polynomial in the 80D integer Laplacian,
```
12800 L^+ = -47 L^4 +900 L^3 -5686 L^2 +12152 L.
```
It gives a surprising exact **q=3 hierarchy** of matrix coefficients:
```
160 Pi_ii=81,
160 Pi_ij in {-27,-3,1,9} for any i!=j.
```
Exhaustive exact integer checks verify symmetry, idempotency, annihilation by B, and off-diagonal multiplicities.

For each of the `C(160,3)=669920` unordered flag triples form the 3×3 principal Gram matrix `K=Pi[T,T]`. Because its integer-scaled diagonal entries are 81 and each nonzero off-diagonal has magnitude>=1, an elementary **trace + Frobenius spectral spread** proof gives a *global analytic optimum over ALL triples*:
```
cond(K) = lambda_max/lambda_min >= 83/80.
```
The ratio is attained whenever every one of the three off-diagonal elements equals **+1**; then `160K=80I_3+J_3`, so eigenvalues are `80,80,83`. The `Pi_ij=+1/160` graph is exactly 81-regular on 160 flag vertices and has **86,400 triangles** (= optimal selectors), counted by integer `tr(A^3)/6`.

A second **full-group 25,920-element orbit calculation**, checked by explicit symplectic projective permutations on points, lines and flags, partitions all 86,400 selectors into EXACTLY FIVE PSp(4,3) orbits:
```
  orbit sizes:  4320, 4320, 25920, 25920, 25920.
  stabilizers:  6,    6,      1,     1,     1.
```
For each 4320 orbit, the stabilizer action on the three chosen flags has image a 3-cycle group C3 (3 distinct permutations, each twice) and a 2-element pointwise kernel; an order6 group with normal C2 kernel and quotient C3 must be **C6**, not S3. Thus there are **two C6-stabilized isotropic families** and three generic trivial-stabilizer families.

**Physics interpretation (strictly conditional):** the entire optimal triple collection is symmetry-invariant, but no individual rank3 subspace is fixed by the full group. A future PSp-invariant interacting order parameter energy could *spontaneously* select one of five orbit families and thereby break symmetry. We have NOT derived such dynamics, an Einstein-Hilbert action, a physical 3D continuum or Lorentzian metric. The number86,400 is a pure finite combinatorial count; its coincidence with seconds per day supplies no physical relationship.

Producers:
- `analysis/w33_20261009_canonical_triplet_isotropy_theorem.py`;
- `analysis/w33_20261009_PSp_orbits_isotropic_triplets.py`;
- exact integer projector, isotropy extremum, and full orbit stabilizer JSON.

## Independent out-of-the-box extra: exact point–line polarization band Hamiltonian

Define 40×160 flag indicator matrices `M` (missing/incident W33 point) and `D` (parent W33 line), and the `PSp`-equivariant weighted positive-semidefinite Hamiltonian
```
K(t) = t M^T M + (1-t) D^T D,   0<=t<=1.
```
Using exact singular values of 40×40 point–line incidence `R=MD^T`, namely `4^1, sqrt6^24, 0^15`, one obtains the complete **algebraic exact spectrum** for `0<t<1`:
```
0^81,
4^1,
[2 + sqrt(4(2t-1)^2+6t(1-t))]^24,
[2 - sqrt(4(2t-1)^2+6t(1-t))]^24,
(4t)^15, [4(1-t)]^15.
```
At either endpoint `t=0,1`, rank collapses to40, with **120 zero modes**; throughout the open interval the exact protected cycle kernel is 81D. The point/line 15-dimensional irreducibles become degenerate at (t=1/2) in a **positive-energy sector**. This is a mathematically tunable duality and a useful hardware architecture comparison, not the same as the previous A6/A30 crossing, nor a physical quantum-gravity theory.

Eleven full 160×160 diagonalizations independently matched the exact spectrum to better than `5e-9`.

Producer: `analysis/w33_20261009_weighted_flag_polarization_spectrum.py`.

## Reproducibility, numerical status and epistemic firewall

Each script has standalone `certificate()`, prints key counts and stores a frozen `data/w33_20261009_*.json` witness. Source-backed files are never overwritten. Added `tests/test_w33_20261009_five_fronts_round13.py` exercises all independent results and audits exact/conditional boundaries. Run from repo root:

```powershell
python -m pytest -q tests/test_w33_20261009_five_fronts_round13.py
```

Everything involving mass/coupling ranks or CFT amplitude is **necessary screening** only. The full-H magnetic-curvature ranks are rigorously **lower** bounds over Q. The anisotropy theorem and optimal orbit decomposition, by contrast, are exact finite combinatorics. Photonic signals are synthetic and the causal indistinguishability theorem prevents claiming actual hardware nonlinearity.

## Top five INDEPENDENT next research actions

1. **Quantitative global quantum mass-gapped spectrum:** propagate dual eight-cycle lower witnesses through simultaneous vanishing-factor strata, then combine genuine subelliptic localization with interval spectral Galerkin enclosures for actual global (E_0) and first excitation. Do not confuse the pointwise `25600/77571` with spectral E0.
2. **True heterotic F-flat support validation:** determine worldsheet coefficient of the `n81*n17*n82` cubic and each nearest n83 coupling from constructing-element fixed points and Rules4–6, then test all 16 supports for exact F/D flatness and nonzero Yukawa matrices.
3. **Actual PSp vacuum representation:** certify rational curvature rank upper bound using exact rational column space, use curvature-aware coercive operators and group projectors to enclose full-H sector bottoms. Either prove unique trivial ground or exhibit rigorous degeneracy.
4. **Causally identified photonic experiment:** build blinded independent optical path and two detector paths, constrain direct electronic cross-talk with measured interventions, then apply shot-clipped randomized-frame test with a trustworthy maximum corruption bound.
5. **A real selection Hamiltonian for the five isotropic orbits:** use explicit invariant local interactions on triples of 160 flag selectors, find the exact or numerical energy minimizers, exhibit robust order parameters choosing the two C6 or three trivial stabilizers, and check whether any infinite native cover has Lorentzian/acoustic dynamics.

**There is no empirically validated Theory of Everything or solved Standard Model vacuum here.** The finite exact PSp orbit landscape is the strongest new theorem from this round; its physical role is a falsifiable conjecture.
