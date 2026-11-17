# Five-front TOE verification: proton lifetime, four-mode KK min-max theorem, linear X8 no-go, IIB torsion linking, event-ready time-bin test

**Date:** 2026-11-16. **Repository:** `wilcompute/W33-Theory` `master`. **Baseline read:** `ee98cc6e300ded7d510c2f19eaad5c35bb3d74f2`. **Worktree:** parallel untracked and staged E6 filter `analysis/2026-11-16_E6_triplet_exchange_filter.md` and corresponding code/certificate were present and deliberately untouched. **Status labels:** mathematical theorem / numerical verifier / conditional EFT / synthetic photon experiment. This packet does **not** establish a TOE or quantum hardware demonstration.

## 1 — E6 proton decay: quantitative, experimentally grounded bound AND triplet filter robustness

The prior E6 tree-level Higgs sector and cubic Yukawa family leave heavy color triplets permitting `QQQL` and `u^c u^c d^c e^c`. Parallel research staged an exact Higgs-leg polynomial **F(Y)=(Y²−4)/5**, with `F(-3)=1` for the weak doublet and `F(±2)=0` for the dangerous color-triplet states. The other agent proves a tree-level filter in that specified messenger superpotential, while acknowledging the separate gauge-mediated dimension-six channel and unknown radiative stability. This report **does not re-stage or duplicate** that parallel filter.

### Lifetime constraint

Super-Kamiokande reports `tau/B(p -> anti-nu K+) > 8.2e33 years` at 90% CL with 365 kt-years. The conservative user-independent effective-operator *parametrization* is (one coherent chirality/flavor amplitude, in the standard W0 convention)

`Gamma = m_p/(32pi) * (1 - m_K²/m_p²)² * |W_K C6|²,`

where `W_K` has units GeV² and `C6` has units GeV^-2. For illustrative `|W_K|=0.10 GeV²`, the current lifetime limit gives

**`|C6| < 2.282836781959541e-31 GeV^-2`**, equivalent to a single unit-amplitude effective cutoff `1/sqrt(|C6|)>2.09e15 GeV`.

The matrix element is **not** universal: lattice calculations report channel, chirality and renormalization dependent values. A complete decay prediction must sum coherently over all operators, neutrino flavors and physical hadronic form factors, and include full RG, color and spinor normalization. This is explicitly a **single-operator conditional bound**.

A simple wino-like dressing ansatz is

`C6 = [A_RG * (g2²/16pi²) * (m_Wino/m_squark²) * f_loop] * [(y_u y_d)/M_triplet]`.

Reference values `A_RG=2, g2=.65, f_loop=1, m_Wino=1 TeV, m_squark=10 TeV, M_triplet=5e16 GeV` and `|y_u y_d|=1e-6` give **`tau=3.731e32 years`**, below the benchmark SK limit; `|y_u y_d|=1e-8` gives a lifetime larger by a factor `10^4`. Varying the squark mass by a factor two increases lifetime by `2^4=16` in this approximation. None of these masses or Yukawas have been predicted by our E6 vacuum.

### An independent robustness test of the parallel filter (new)

The interpolation matrix for `F(-3)=1,F(-2)=0,F(+2)=0` has determinant **20**, so `F(t)=(t²−4)/5` is the **unique quadratic** implementing those conditions. If either triplet eigenvalue is displaced from `±2` to `±2+δ` by commuting adjoint-VEV detuning, then

`F(±2+δ)=(±4δ+δ²)/5`.

The worst-case leakage factor is `s(δ)=(4|δ|+δ²)/5` if the light-doublet normalization remains fixed. A single triplet-mediated decay amplitude increases linearly in `|δ|`, so its rate grows as `δ²`. Under the high-Yukawa illustrative benchmark above, the experiment requires `s < sqrt(tau_unsuppressed/tau_limit)`, hence **`|δ| < 0.250898...`** in this specific normalization. Other flavor/loop choices or the distinct gauge contribution change this threshold. The exact filter is a chosen coefficient relation with **no demonstrated radiative or symmetry protection**: a broader adjoint perturbation, threshold corrections or an allowed contact operator can regenerate proton decay. This is a quantified tuning-sensitivity diagnostic, not an exclusion.

Reproducers:
- `analysis/toe_20261116_proton_Knu_dressing_bounds.py`, `data/toe_20261116_proton_Knu_conditional_bound.json`
- `analysis/toe_20261116_E6_triplet_filter_tolerance.py`, `data/toe_20261116_E6_triplet_filter_misalignment_tolerance.json`

External references:
- Super-K 2025 talk displaying `p -> anti-nu K+` lifetime: https://www-sk.icrr.u-tokyo.ac.jp/~nakahata_s/kakenhi-kibanS/talk/Nakahata_SuperK_KMI2025_250305.pdf .
- Hadronic transition form factors near the physical pion mass: https://pos.sissa.it/466/435/pdf .
- SUSY GUT superpartner-dressing phenomenology: https://arxiv.org/abs/2012.14411 .

## 2 — Four independent torus KK instabilities protected by a min–max theorem

At exact equal flux on a square torus, the previously certified sphere-exchange-odd, constrained scalar/Maxwell physical KK branch has eigenvalue

`m0² L²=3pi-2-sqrt(4+48pi)=-5.0169440813078374...`,

thus **BF gap `delta0=1.0169440813078374...`**. The shell `(m,n)=(±1,0),(0,±1)` contains four independent **real** sine/cosine modes; the next shell `|k|²=2` has `lambda=6pi>12` and is stable *within this branch*. A real four-dimensional subspace therefore has Rayleigh quotient `m0²`.

**Rigorous conditional theorem:** If the complete physical, canonical gauge-constrained unequal-flux operator `H_N` acts self-adjointly on the identified physical Hilbert space and `||H_N-H_equal||_op < delta0`, the Courant–Fischer min–max theorem places **at least four physical real modes below the AdS5 BF bound**. This avoids assuming their detailed splitting or any special mixing pattern. The background preserves the square torus Fourier labels; continuity of the relevant physical subspace must still be proved.

For diagnostics only, parameterize the unknown physical norm by

`||H_N-H_equal|| <= K*|eta(N)-1/2| + C*(lp/L)^6`.

Both `K` and `C` are **not calculated** from 11D physics. For a hypothetical `C=100`, sufficient thresholds are `N>=6` for `K=5`, `N>=14` for `K=10`, `N>=29` for `K=20`, `N>=74` for `K=50` (the finite-N inequalities here are merely controlled examples of the theorem, not physical thresholds). A random self-adjoint four-mode perturbation validates min–max numerically; when the hypothetical bound is exceeded the test rightly cannot guarantee instability.

The actual unequal-flux eleven-dimensional metric/`C3` fluctuation matrix, gauge elimination, kinetic inner product and operator derivative bound are **unsolved**. This packet does not claim they have been diagonalized.

Reproducer `analysis/toe_20261116_KK_four_mode_minmax_protection.py`, certificate `data/toe_20261116_KK_four_mode_minmax_certificate.json`.

## 3 — Eight-derivative curvature: an exact FIRST-ORDER vanishing theorem for X8

The unwarped eleven-dimensional background `AdS5 x S² x S² x T²` is a product of constant-sectional-curvature blocks. In an orthonormal frame, the curvature two-form matrix has

`(R0)^a_b=K_i e^a wedge e^b` for `a,b` in the same block, and zero otherwise.

**Stronger identity:** It is nilpotent under **matrix multiplication using exterior wedge**:

`(R0 wedge R0)^a_c = sum_b K_i² (e^a wedge e^b wedge e^b wedge e^c)=0.`

Consequently `tr(R0²)=tr(R0⁴)=0` and, **for any first curvature variation `deltaR`**,

`delta tr R⁴ =4 tr(R0³ deltaR)=0`,
`delta [(tr R²)²] = 2 tr(R0²) delta tr(R²)=0`.

Since `X8` is a linear combination of those degree-eight Pontryagin polynomials, both **`X8(R0)=0` and `delta X8(R0)=0`**. The verifier implements exact 11-dimensional integer bitmask exterior algebra and shows `R0²=0` *entry by entry*, not merely after taking traces.

**Crucial limitation:** `delta²X8` need not vanish! The code constructs an algebraic perturbation with `delta tr R² !=0` and nonzero `(delta tr R²) wedge (delta tr R²)`. The example perturbation is a general curvature-form variation, not claimed to solve linearized Levi-Civita constraints. The `C3 wedge X8` term has no local `deltaC3 wedge deltaX8` mixed term at quadratic order around this product, but a background `C3 wedge delta²X8` term can remain (and its non-global background potential requires differential refinement). The separate `t8t8R4`, `epsilon epsilon R4`, `G4` curvature-mixed completion, and **the physical corrected mass** are still not calculated. A vanishing `X8` or first variation never justifies discarding the complete eight-derivative correction.

Reproducer `analysis/toe_20261116_11D_X8_nilpotent_variation.py`, certificate `data/toe_20261116_11D_X8_linear_variation_nilpotent.json`.

Background: the eight-derivative action includes more than `X8` and `R4`; e.g. https://research-portal.uu.nl/files/74820878/thesismayercomplete_5f2a73fd792ea.pdf .

## 4 — An exact IIB circle-bundle torsion LINKING invariant

Let `Y(p,q) -> B=S²xS²` be the oriented circle bundle with nonzero `e=p*x+q*y`, `g=gcd(|p|,|q|)`, `a=p/g,b=q/g`. The integral Gysin sequence, not a guess at a finite charge group, gives

`H^0(Y)=Z; H^1(Y)=0; H^2(Y)=Z ⊕ Z_g; H^3(Y)=Z; H^4(Y)=Z_g; H^5(Y)=Z,`
`pi1(Y)=Z_g`.

The primitive torsion generator of `H²` is `t=pi*(a x+b y)` (order g). The `H⁴` torsion generator is `u=pi*(x y)` (order g). The integral `H³` generator has fiber pushforward `pi_*z=a x-b y`. Choosing an angular connection with `d theta=pi*e=g t`, normalized `integral_{fiber}theta=1`, yields an exact **cohomological torsion linking** pairing

`L(t,u)= ±(1/g) mod 1`.

For `g>1`, this is a **perfect pairing** of the two cyclic torsion sectors; for coprime `p,q` it vanishes because the torsion is absent. Examples: `Y(6,6)` has linking `1/6`; `Y(7,6)` is torsion-free; `Y(12,18)` has linking `1/6`. The code computes Smith forms and tests signed pairs `|p|,|q|<=9`.

**Distinction from physical charge:** This is an unambiguous global invariant of the topological five-manifold. It does not by itself quantify RR Page charges, M2/M5 endpoint screening, a twisting by `H3`, nor an M/IIB differential-field duality. It provides a better mathematical benchmark than identifying every flux gcd with the IIB winding group.

Reproducer `analysis/toe_20261116_IIB_circle_Gysin_linking.py`, certificate `data/toe_20261116_IIB_circle_Gysin_torsion_linking.json`. C-field global context: https://arxiv.org/abs/hep-th/0312069 .

## 5 — Executable event-ready qutrit experiment acceptance protocol

Combine prior full 27-dimensional SWAP–causal-reset–SWAP-back simulation, proven four-MUB identity `sum_b P_match(b)=I9+3|Phi3><Phi3|`, and non-IID anytime-valid e-process with an actual hardware accounting interface.

Each heralded attempt follows this strict timing:
1. Source herald and both pair carriers prepared; log pre-basis attempt ID and timestamp.
2. Random secret one-of-four MUB basis drawn independently of preparation; log independent choice timestamp after herald.
3. Route time-bin superpositions **coherently** into three simultaneous spatial rails (or calibrated programmable temporal projector); phase-modulate and perform U3 Fourier analysis on reference and signal conjugate bases.
4. Record **all** heralded time-tag windows, including lost photons, missed detections and no clicks. Count a matched valid pair as `Y=1`, everything else `Y=0`.
5. Apply a predeclared, predictable e-process with null `p0=0.5+calibration_error+setting_leakage_TV`, retaining all event-ready trial counts.

In a specific trusted-device noise model, with isotropic visibility `v=.75`, Gaussian dephasing `sigma=.15`, both detector efficiencies `.90`, memory/path each `.95`, router efficiencies `fR,fS`, and accidental no-pair match probability `dark/3`, the expected **gross** match probability is

`p = eta*q+(1-eta)*dark/3`, `eta=.9²*.95²*fR*fS`,
`F=v*(1+2exp(-sigma²))/3+(1-v)/9`, `q=(1+3F)/4`.

The separable null is `p0=.51` (with eps=.01, setting TV 0). The route asymmetry matters only through `fR*fS` within the uniform trusted-loss model. Both routers at `.95` yield a positive witness gap; both at `.90` do not; `fR=.99,fS=.90` is feasible under the same assumptions.

For a **predeclared fixed alternative** `q=p_model>p0`, sequential log-likelihood factors form a nonnegative supermartingale under any separable conditional Bernoulli response `p_t<=p0`. The information scale is `n ~ log(100)/D_KL(p_model||p0)`: **about 1,953 heralded trials** for the 95%-routing model, not a rigorous fixed-sample guarantee. A deterministic 16-seed synthetic 12,000-trial simulation crossed the anytime 1% threshold in **16/16 runs**; the exact false-alarm control comes from the supermartingale theorem, not those simulations. This does not certify a real photon memory, real detector POVM or physical loophole closure.

Reproducer `analysis/toe_20261116_qutrit_eventready_timetag_sequential.py`, certificate `data/toe_20261116_qutrit_eventready_full_timetag_acceptance.json`. Current 2026 temporal measurement research: https://opg.optica.org/abstract.cfm?uri=QUANTUM-2026-QM3A.4 and https://opg.optica.org/abstract.cfm?uri=QUANTUM-2026-QW4C.6 .

## Sixfront outside-box falsifier synthesis

The test suite also compares **tree-level fine-tuning versus robust protection**: the exceptional Higgs vacuum and polynomial filter can obey exact algebraic identities yet remain unprotected against small operator changes; the M-theory constant-curvature `X8` identity removes certain terms exactly but cannot be substituted for the higher-derivative theory; and a time-bin experiment can pass ideal unitary checks while failing strict event-ready statistics once routing loss is introduced. The meaningful next milestone across these fronts is a derived *stability margin* from a fully specified physical operator, not another correspondence of raw counts.

## Verification commands and limitations

`python analysis/toe_20261116_proton_Knu_dressing_bounds.py`
`python analysis/toe_20261116_E6_triplet_filter_tolerance.py`
`python analysis/toe_20261116_KK_four_mode_minmax_protection.py`
`python analysis/toe_20261116_11D_X8_nilpotent_variation.py`
`python analysis/toe_20261116_IIB_circle_Gysin_linking.py`
`python analysis/toe_20261116_qutrit_eventready_timetag_sequential.py`
`python -m unittest discover -s tests -p test_toe_20261116_sixfront_proton_KK_X8_linking_photon.py -v`

No full unequal-flux 11D physical KK matrix, no corrected supersymmetric eight-derivative mass, no genuinely quantized differential Page charge algebra, no realistic full E6 proton lifetime, and no laboratory qutrit photon experiment have been obtained. Treat the quantified models as conditional experimental design or falsification targets.


## 1B — Independent gauge-boson proton decay survives the exact triplet filter

The staged parallel color-triplet filter removes the specified **dimension-five holomorphic** tree exchange but explicitly leaves a `Y`-charge-five E6 gauge-boson sector. The complete charged block's exact trace-metric projector contains a nonzero component `-1/6` connecting light `Q†e^c` and `(u^c)†Q` currents, and the reduced adjoint gauge-mass formula is `M_X²=25*g_GUT²*v_Y²`. These are prior parallel-source results (`analysis/toe_20261116_E6_triplet_exchange_filter.py`); our NEW independent step is the **conditional experimental constraint** on that channel.

For a single dimension-six operator (neglecting all uncomputed interference, CKM/flavor, RG and chirality factors), assume `C6=κ*g_GUT²/M_X²=κ/(25*v_Y²)`, with `κ=1/6` interpreted as the magnitude of the prior current projector coefficient. Super-K's `p→e+π0` limit is `tau>2.4e34 years` with 450 kt-years. In the same standard two-body form-factor normalization, an **illustrative** hadronic `Wπ=.10 GeV²` gives

`|C6| < 9.8535513e-32 GeV^-2` and therefore **`v_Y > 2.6011057e14 GeV`**, assuming `A_RG=1` and the above normalized single current saturates the decay channel. At `v_Y=1e14 GeV` this benchmark violates the limit; at `v_Y=1e15 GeV` it passes. The gauge coupling cancels algebraically because the boson mass is proportional to `g_GUT v_Y`. A different effective group coefficient or RG factor simply rescales the threshold by its square root.

This is NOT a model-independent lower bound on the E6 breaking scale: the current projector is not a complete low-energy proton-decay Wilson coefficient. The physical answer requires all six heavy gauge generators, fermion mixing, field normalization, operator matching, RG evolution, hadronic matrix elements, and interference. Nevertheless, it is a quantitatively useful **second independent decay channel** to carry alongside the filtered dimension-five triplet interaction.

Reproducer: `analysis/toe_20261116_E6_charge5_gauge_proton_bound.py`; certificate `data/toe_20261116_E6_X_gauge_proton_pion_bound.json`; 7 focused tests in `tests/test_toe_20261116_E6_X_gauge_proton_bound.py`. Super-K presentation: https://www-sk.icrr.u-tokyo.ac.jp/~nakahata_s/kakenhi-kibanS/talk/Nakahata_SuperK_KMI2025_250305.pdf .
