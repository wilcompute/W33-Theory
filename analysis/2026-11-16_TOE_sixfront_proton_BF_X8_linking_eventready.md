# Six-front TOE continuation: quantitative proton-decay falsifier, four KK modes, exact X8 variation, IIB torsion linking, and event-ready qutrit trials

**Prepared 2026-11-16 in W33-Theory, using the authorized local machine.** Starting GitHub HEAD: `ee98cc6e300ded7d510c2f19eaad5c35bb3d74f2`. The user's other local research is frequently dirty/staged; **preserve it** and commit only the six new verifiers, six deterministic JSON certificates, this report and focused unittest.

**Scientific scope:** We are quantifying necessary constraints and exact low-dimensional algebra. This packet does **not** constitute an eleven-dimensional corrected supergravity spectrum, complete supersymmetric E6 phenomenology, global physical M-theory Page charge calculation, or experimental quantum-memory demonstration.

## 1. Proton decay: experimental coefficient constraints and a stringent E6 filter stability test

The Super-Kamiokande `p -> anti-nu K+` lifetime lower bound `8.2e33 yr` at 90% confidence (365 kt yr) appears in the publicly posted collaboration results ([Super-Kamiokande presentation](https://www-sk.icrr.u-tokyo.ac.jp/~nakahata_s/kakenhi-kibanS/talk/Nakahata_SuperK_KMI2025_250305.pdf)). This is a **reported experimental bound**, not a computed prediction of the E6 Higgs vacuum. In a conventional **single effective operator** normalization

`Gamma(p->K nu) = [m_p/(32pi)]*(1-m_K²/m_p²)² * |W0*C6|²`,

we take `m_p=.9382720813 GeV, m_K=.493677 GeV` and an illustrative `|W0|=.10 GeV²` (actual hadronic matrix elements are chirality- and channel-dependent). Converting the lifetime bound with `hbar=6.582119569e-25 GeV*s` gives `|C6| < 2.282836781959541e-31 GeV^-2`, equivalent to an effective single-operator scale `1/sqrt(C6)`, about `2.09e15 GeV`.

For a **toy** wino dressing, not a full supersymmetric computation,

`C6 = A_RG *(g2²/16pi²)*(M_wino/M_sfermion²)*f_loop*(y_u*y_d)/M_triplet.`

With `g2=.65, A_RG=2, f_loop=1, M_wino=1000 GeV, M_sfermion=10000 GeV, M_triplet=5e16 GeV, y_u*y_d=1e-6` the predicted one-channel lifetime is `3.731037569386319e32 yr`, below the stated limit. At Yukawa product `1e-8` it is 10,000 times longer, and the illustrative model satisfies the bound. Exact comparison requires all flavor matrices, chiralities, soft terms, RG running, sparticle dressing and coherent hadronic interference. No E6 model is excluded by this simplified benchmark.

**Parallel-agent connection and new stress test:** The staged (not ours) E6 filter uses `F(t)=(t²-4)/5` on the Higgs leg; this exactly satisfies `F(-3)=1,F(-2)=F(2)=0`, removing the triplet holomorphic couplings while leaving the up-type weak doublet. Our independent interpolating-polynomial verifier proves the filter is the **unique quadratic** meeting those three conditions. A commuting diagonal VEV detuning `t_triplet = ±2+delta` gives an unavoidable first-order leakage `F= (±4 delta+delta²)/5`. In the stated high-Yukawa illustrative benchmark, both triplet weights remain below the single-channel proton bound provided the worst-case detuning magnitude is **less than ~0.250898**, under the assumption that the light doublet normalization and other parameters are fixed. There is **no derived all-orders protection** of that interpolation under radiative corrections, no complete E6 flavor structure and no gauge-mediated proton-lifetime prediction.

Verifiers: `analysis/toe_20261116_proton_Knu_dressing_bounds.py`, `analysis/toe_20261116_E6_triplet_filter_tolerance.py`.
Data: `data/toe_20261116_proton_Knu_conditional_bound.json`, `data/toe_20261116_E6_triplet_filter_misalignment_tolerance.json`.

## 2. Four-mode BF min–max protection on the square torus, with explicit physical hypotheses

Our previously verified **equal-flux** constrained sphere-exchange-odd scalar + 11D three-form KK block has `m_-²L²=lambda-2-sqrt(4+16lambda)` with `lambda=3pi*(m²+n²)` for a square torus. The BF threshold `m²L²>=-4` is violated for `0<lambda<12`. Among nonzero square-lattice vectors, **exactly** `(±1,0),(0,±1)` lie in that interval; the next shell `lambda=6pi>12` is stable **in that specific branch**. These four signed momenta yield four independent real cos/sin harmonics. At `lambda=3pi`, the BF deficit is `Delta0=1.0169440813078374...`.

This gives a strengthened **conditional min–max theorem**: if `H_N` and `H_equal` are canonically normalized self-adjoint **physical** (all metric and C3 constraints eliminated) fluctuations on a common Hilbert space, with a four-dimensional subspace of quadratic form `<=-4-Delta0`, then
`||H_N-H_equal|| < Delta0`
implies **at least four** BF-violating physical eigenvalues, by Courant–Fischer/Weyl. Numerical examples illustrate a hypothetical **unproven** Lipschitz bound

`||H_N-H_equal|| <= K*|eta_N-1/2| + C*(lp/L)^6.`

For purely illustrative numbers `K=5,C=100`, the sufficient inequality is met at `N>=6` in the provided sample. **Neither K nor C is a calculated physical value**. Do not quote `N=6` as a real M-theory stability threshold; the rigorous output is the min–max implication conditional on an actual full operator norm bound.

Verifier: `analysis/toe_20261116_KK_four_mode_minmax_protection.py`. Certificate: `data/toe_20261116_KK_four_mode_minmax_certificate.json`.

## 3. Eight derivatives: exact nilpotency and linearized cancellation for the gravitational X8 polynomial

On the background `AdS5 x S2 x S2 x T2` with each factor of constant sectional curvature and direct-product connection, choose an orthonormal frame `e^a`. The curvature two-form matrix is `R^a_b=K_i e^a ∧ e^b` within each constant-curvature factor. The matrix square is **exactly zero as a four-form matrix**:

`(R∧R)^a_c = Σ_b K² e^a∧e^b∧e^b∧e^c =0.`

Thus `tr R²=tr R⁴=0` and the standard M-theory eight-form `X8 ∝ tr R⁴ - (tr R²)²/4` vanishes **pointwise**. More surprisingly, the first variation with respect to **arbitrary algebraic curvature variations** `delta R` also vanishes:
`delta tr R⁴ =4 tr (R³∧delta R)=0` and `delta (tr R²)²=2 tr R²∧delta tr R²=0`. This is an exact linearized identity, verified by explicit bitset exterior algebra in eleven tangent dimensions; it does not assume numerical curvature approximations.

**But the second variation need not vanish.** The verifier constructs an algebraic `delta R` with `delta tr R² !=0` and `(delta tr R²)² !=0`. Therefore the local **mixed** quadratic term `delta C3 ∧ delta X8` vanishes in this background, while `C3_bg∧delta²X8` and the full supersymmetric scalar `t8t8R4`, `epsilon epsilon R4`, flux/curvature couplings, corrected radii and fluctuation kinetic operator may still contribute. Since the background C3 is not global, this statement is only about local differential-form expansion. No eight-derivative BF eigenvalue or physical coefficient has been computed.

Verifier: `analysis/toe_20261116_11D_X8_nilpotent_variation.py`. Certificate: `data/toe_20261116_11D_X8_linear_variation_nilpotent.json`.

## 4. IIB torsion linking: genuine topological input beyond a numerical gcd

Consider the oriented principal circle bundle `Y(p,q)->S²×S²` with Euler class `e=p x+q y`, `g=gcd(|p|,|q|)>0`. An integral Gysin calculation yields `H0=Z,H1=0,H2=Z+Z_g,H3=Z,H4=Z_g,H5=Z` (with `Z_1=0`), and `pi1(Y)=Z_g`. The free generator `z∈H3(Y)` pushes to `(p/g)x - (q/g)y` in `H2(base)`.

We additionally derive an explicit **perfect torsion-linking form**
`Tor H²(Y) × Tor H⁴(Y) -> Q/Z`
with generator pair `L(t,u)= ±1/g (mod 1)`, where `t=pi*((p/g)x+(q/g)y)` and `u=pi*(x y)`. Choose a fiber angular cochain `theta` with `dtheta=g t` and normalized fiber integral one; the cochain formula gives `(1/g) ∫_Y theta ∧ pi*(x y) =1/g` up to orientation. It is a nondegenerate linking pairing for **every nontrivial** `p,q`, checked for 360 signed integer pairs. At `(6,6)` the linking unit is `1/6`; at coprime `(7,6)` it is trivial.

**Important physical separation:** This proves a topological invariant of IIB geometry. It does not identify an eleven-dimensional differential C-field, an actual Page-charge group, a twisted K-theory extension, or a propagating wound string. Global C-field quantization and electric charge refinements must be treated as in Diaconescu–Freed–Moore, [arXiv:hep-th/0312069](https://arxiv.org/abs/hep-th/0312069).

Verifier: `analysis/toe_20261116_IIB_circle_Gysin_linking.py`. Certificate: `data/toe_20261116_IIB_circle_Gysin_torsion_linking.json`.

## 5. Experiment-ready three-time-bin qutrit: synthetic time-tag and sequential statistics

The previously proven four-MUB witness requires a 3-port Fourier optical analyzer **plus coherent temporal routing**, and a pair-source herald independent of later randomly selected measurement settings. Count **every pre-setting heralded attempt**; no-click is a mismatch. Let source visibility `v=.75`, time-bin phase sigma `.15` radians, reference/signal detector efficiencies `.9`, memory/path throughput `.95` each, two spatial time routers `f_R,f_S`, calibration `epsilon=.01`, setting leakage TV 0. Under a trusted isotropic/noise model:

`F=v(1+2e^-sigma²)/3+(1-v)/9,`
`q=(1+3F)/4,`
`eta_pair=(.9)²(.95)² f_R f_S,`
`p_gross=eta_pair*q+(1-eta_pair)*p_dark/3,`
`p_null=.5+epsilon+TV=.51.`

A reference configuration with **95% routing efficiency per arm** exceeds the witness threshold; **90% each** falls short. An asymmetric pair `f_R=.99,f_S=.90` passes. To exercise the sequential inference we simulated 16 seeded, 12,000-herald trial datasets including random basis labels, detector losses and dark counts. The predeclared fixed-alternative e-process (not a postselected coincidence test) crosses the one-percent evidence threshold in **all 16 synthetic runs**, with expected KL evidence scale roughly **1,953 gross trials** for e-value 100 in the nominal model. This is **not an estimate of actual experimental performance** and cannot replace the e-process's analytic non-IID false-positive guarantee, which relies on hidden settings and calibrated device-level bounds. Also, the raw simulation does not construct a time-resolved electromagnetic pulse or implement a physical quantum SWAP; hardware remains to be built.

Verifier: `analysis/toe_20261116_qutrit_eventready_timetag_sequential.py`. Certificate: `data/toe_20261116_qutrit_eventready_full_timetag_acceptance.json`.

## 6. Unifying falsification: a rare cross-domain methodological lesson

Three distinct nonuniformities obstruct naive "TOE" interpretations:
- **Supersymmetric E6 algebra vs experimentally viable flavor:** exact Higgs symmetry breaking and even exact triplet *tree* filtering do not prove suppression of loop-mediated baryon violation; the filter has calculable sensitivity to off-target adjoint eigenvalues.
- **Uniform classical BF instability vs controlled higher derivatives:** four classical KK harmonics provide a robust min–max test only after the full physical operator is constructed and bounded. The exact X8 linear cancellation helps isolate particular terms, but does not eliminate other eight-derivative couplings.
- **Exact topology and optics vs physical charge/measurement:** a perfect torsion-linking form is not a quantum Page-charge spectrum, just as a three-port unitary is not a time-bin analyzer and a coincidence-selected sample is not an event-ready entanglement test.

## Reproducibility and limitations

Run each of the six source files independently:
`python analysis/toe_20261116_proton_Knu_dressing_bounds.py`
`python analysis/toe_20261116_E6_triplet_filter_tolerance.py`
`python analysis/toe_20261116_KK_four_mode_minmax_protection.py`
`python analysis/toe_20261116_11D_X8_nilpotent_variation.py`
`python analysis/toe_20261116_IIB_circle_Gysin_linking.py`
`python analysis/toe_20261116_qutrit_eventready_timetag_sequential.py`

Then:
`python -m unittest discover -s tests -p test_toe_20261116_sixfront_proton_KK_X8_linking_photon.py -v`

Run at least two prior-targeted test suites as regression controls. Commit **only** these six new scripts, six data JSONs, the report and this test module; preserve the other parallel agent's **preexisting staged E6 triplet-filter** and all dirty files. All results are conditional or exact at their stated mathematical level; no complete Theory of Everything or unmeasured photonic hardware achievement is claimed.
