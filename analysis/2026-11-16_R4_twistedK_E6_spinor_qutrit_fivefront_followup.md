# Five-front follow-up: eight-derivative BF threshold, twisted K, spinor selection, E6 Hessian, and a four-MUB photonic discriminator

Date: 2026-11-16. Independently generated reproducible work. Research grade: mathematical calculations and conditional experimental design only. **No complete eleven-dimensional corrected solution, exact string spectrum, phenomenological SM vacuum, or laboratory data.**

## Evidence provenance and checked predecessors

The starting master was `331b48fb8f187a192a725a74fdb4265ef86a3315`. Read the existing `analysis/2026-11-16_fivefront_M_IIB_Ktheory_E6_temporal_controls.md` and its four producer scripts, the older `analysis/2026-11-16_D9_mtheory_uplift.md` and IIB circle dual draft, and preserved the substantial dirty worktree. The new calculations were checked against the specific prior producer functions instead of treating old results as novel.

External controls:
- Wulff, *All symmetric AdS_{n>2} solutions of eleven-dimensional supergravity*: https://arxiv.org/abs/1611.06139 .
- Higher-derivative eleven-dimensional curvature/flux terms and C3-X8: https://arxiv.org/abs/hep-th/9706175 ; the eight-derivative completion includes mixed G4-dependent terms, not a standalone pure R4 prescription.
- Twisted complex K-theory AHSS: https://ncatlab.org/nlab/show/Atiyah%E2%80%93Hirzebruch+spectral+sequence ; topology and T duality: https://doi.org/10.1103/PhysRevLett.92.181601 .
- MUB separable coincidence bound and qutrit witnesses: https://doi.org/10.1038/s41598-022-16225-z ; operational process-tensor memory: https://arxiv.org/abs/1801.09811 .

## I. What an R4-induced mass correction must achieve

Existing exact two-derivative mass and flux quantization give, for `(N1,N2,N0)=(N+1,N,N)`,
`m_-² L²=-4-45/N²+O(N^-3)` and `(L/lp)^3=(9 pi/2)N+O(1)`.

Assume for *coefficient bookkeeping only* that all eight-derivative terms, once evaluated on the **corrected** background and canonically normalized scalar fluctuation, shift the AdS-normalized eigenvalue by `C*(lp/L)^6`. The asymptotically necessary condition for removing this homogeneous BF violation is

`C >= 45*(9*pi/2)^2 = 3645*pi^2/4 = 8993.67701049...`.

The verifier computes exact finite-integer analogues `C_req(N)=gap(N)*(L/lp)^6` with 65-digit inputs and confirms convergence to that threshold. Since the coefficient, radius renormalization, and flux-dependent operators have NOT been calculated, neither stability nor instability of the fully corrected vacuum is concluded.

**Independent geometric check:** On the exact product constant-sectional-curvature background `AdS5 x S2 x S2 x T2`, every curvature two-form on a single factor is `R^a_b=K e^a wedge e^b` and each trace term `tr R^(2n)` vanishes pointwise because its wedge factors repeat basis one-forms. The flat torus adds zero curvature, hence `X8(background)=0`. This does NOT imply `delta X8` or `delta^2 (C3 X8)` vanishes; nor can one drop mixed curvature/flux terms when computing masses.

Producer `analysis/toe_20261116_R4_threshold_spinor_modes.py`, certificate `data/toe_20261116_R4_threshold_spinor_modes.json`.

## II. Twisted K-theory: actual zero-H vacuum versus optional H=k*z backgrounds

Let `Y(p,q)->S2 x S2` be the circle bundle with nonzero Chern class `p x+q y`; let `g=gcd(|p|,|q|)`. Prior Gysin calculations give
`H^0=Z, H^2=Z+Z_g, H^3=Z<z>, H^4=Z_g, H^5=Z`.
Choose a free degree-two class `t` with `<t cup z,[Y]>=1` and torsion degree-two class `u` with `u cup z=0`.

**Important:** The currently studied source-free Type IIB solution sets `H3=0`. The following `H=kz` is an *optional new background*, not a silent change to the physical vacuum.

For nonzero k, complex twisted-K AHSS has `d3=SqZ^3+H cup`. The integral third-square contributes zero on the relevant degrees because its possible targets `H^3` and `H^5` are torsion-free. Therefore `d3: H^0->H^3` is multiplication by k and `d3: H^2_free->H^5` is also multiplication by k; torsion u maps to zero. Higher differentials have no surviving nonzero source/target in dimension five. Thus the E_infinity filtration gives

`gr K_H^0=Z_g + Z_g,qquad gr K_H^1=Z_|k| + Z_|k|.`

For `g=1`, the total space is `S2 x S3` and Kunneth resolves `K_H^0=0, K_H^1=Z_|k|^2`. For `g>1`, the total orders are `|K_H^0|=g^2`, `|K_H^1|=k^2`, but additive extensions are **not determined** by this AHSS alone. An isolated spin D3 wrapping an oriented unit 3-cycle with nonzero H period is subject to the Freed-Witten obstruction; such a situation is not present at H=0.

Producer `analysis/toe_20261116_twisted_K_AHSS_extensions.py`, certificate `data/toe_20261116_twisted_K_AHSS_extensions.json`.

## III. Spinor and winding: exact selection rule, not a manufactured duality

In the equal-charge quotient `T11/Z_N`, a cover mode `exp(i k psi_std/2)` transforms under the deck generator `psi_std -> psi_std+4 pi/N` by `exp(2 pi i k/N)`. Ordinary spin lift retains `k == 0 (mod N)`; the alternative lift, present for even N, retains `k == N/2 (mod N)`.

The two known covering conifold Killing-spinor phases are `k=+1,-1`. They survive only for `N=1` with ordinary lift, and `N=2` with alternative lift. This repeats and strengthens the auditability of a prior repo claim through explicit residues for N=1..16. `pi1(Y)=Z_N` supplies a separate **topological fiber winding** classification, not an automatic identification between a IIB winding excitation and an 11D fermionic KK mode. The latter would require explicit spin-dependent duality of physical operators and worldsheet sectors. We do not claim an 11D supersymmetry restoration.

The charge table is in the R4/spin verifier above.

## IV. E6: renormalizable single-27 obstruction with a flat singlet Hessian

Under `SU3^3`, three 3x3 bifundamental sectors `A,B,C` have center charges `(1,-1,0),(0,1,-1),(-1,0,1)` mod 3. Enumerating all nine ordered bilinear sector pairs, **none** has net zero center charge. Hence a single chiral 27 has **no gauge-invariant quadratic superpotential term**, even under this subgroup. The center criterion is necessary, not a complete enumeration of invariant tensors.

The established cubic `W=det A+det B+det C-Tr(ABC)`, restricted to `A=a I3,B=b I3,C=c I3`, becomes `W=a³+b³+c³-3abc`. At `a=b=c=s`, the Hessian in raw coordinates is `3s*(3 I3-J3)`, with eigenvalues `(0,9s,9s)`. Because the kinetic norm is `3(|da|²+|db|²+|dc|²)`, canonical superpotential mass eigenvalues are `(0,3s,3s)`, corresponding to F-term scalar mass squares `(0,9|s|²,9|s|²)` along these complex singlet directions. The exactly massless radial modulus makes scale selection impossible with only this homogeneous cubic; the unbroken group is diagonal SU3 rather than the observed SM.

Nothing here proves a no-go for models with 27bar fields, extra generations, soft terms, higher-dimensional operators, supergravity, or other gauge-breaking sectors.

Producer `analysis/toe_20261116_E6_cubic_hessian_center.py`, certificate `data/toe_20261116_E6_cubic_hessian_center.json`.

## V. Four-setting optical qutrit entanglement protocol and conditional statistical power

Take time-bin/rail qutrits `R,S,E` with reference/system initially in `|Phi3>=(|00>+|11>+|22>)/sqrt3`. Coherently SWAP `S` with memory `E`, causally break the system via a fresh `|0>` re-preparation, then SWAP back. A memoryless or computational-classical storage reference returns separable `rho_RS`; the ideal coherent process returns `Phi3`. This is an ideal circuit specification, not a claim that a deterministic optical memory device was fabricated.

**Four measurement settings:** take eigenbases of `Z,X,XZ,XZ²` on reference, and the complex-conjugate basis on the system, using calibrated phase masks and Fourier multiports. Record matching outcomes independently for each of the four basis settings, with probabilities `C_b`. The exact 9x9 operator identity is

`sum_(b=1)^4 P_match(b)=I9+3 |Phi3><Phi3|`.

This was checked independently with server-side NumPy and local standard-library complex matrix multiplication. Therefore, **for arbitrary two-qutrit density matrices**,
`F_Bell=(sum_b C_b -1)/3`. Every separable state obeys `F<=1/3`, i.e. `S=sum_b C_b<=2`. The four-setting witness detects more noise than a two-MUB witness, with a clean, general fidelity reconstruction.

For the explicitly assumed isotropic noise model `rho(v)=v Phi3+(1-v)I9/9`, each C is `(1+2v)/3`. Four-MUB entanglement detection occurs for `v>1/4`, and two-MUB detection requires `v>1/2`.

**Fixed-shot power planning:** Let n independent, accepted trials be collected for each of the four settings. Hoeffding gives the conservative separability rejection rule `S_hat>2+sqrt(2 ln(1/alpha)/n)` with false-positive target alpha. Under fixed isotropic v, failure-to-reject probability is <=beta when
`n >= [sqrt(2 ln(1/alpha))+sqrt(2 ln(1/beta))]^2/(E[S]-2)^2`.
At alpha=.01,beta=.1, the ideal-model requirements are n=31 per setting for v=.6, n=16 for v=.75, and n=9 for v=.9. **These are accepted/heralded pair counts**, not gross optical attempts. Detector efficiency, basis calibration, multipair errors, phase drift, memory loss, stationarity and a detection-loophole audit must be added for any practical laboratory claim.

Producer `analysis/toe_20261116_qutrit_four_MUB_experiment.py`, certificate `data/toe_20261116_qutrit_four_MUB_experiment.json`.

## VI. What remains genuinely open

1. **Eight-derivative M mass sign:** the threshold is mathematically exact given the hypothesized correction form, but no physical `C` was calculated.
2. **Physical RR charge groups:** twisted associated-graded extensions (especially nonprimitive g), self-dual five-form flux and differential refinements are unresolved.
3. **M/IIB fermionic equivalence:** quotient selection is exact; identification of actual winding fermions, their spin structures and masses has not been derived.
4. **An isolated realistic E6 vacuum:** the cubic branch remains scale-flat and has the wrong residual gauge group.
5. **Optical hardware demonstration:** four-MUB fidelity reconstruction is exact, but all shot claims are synthetic and device-dependent.

## Regression and change ownership

`python -m unittest discover -s tests -p test_toe_20261116_fivefront_followup_R4_K_E6_MUB.py -v` — 15 focused cross-front tests against the older programs. Each standalone analysis program writes one deterministic certificate. This work owns only the 4 new producer files, the 4 certificate JSON files, this report, and the targeted test suite; no unrelated dirty worktree content should be staged or rewritten.
