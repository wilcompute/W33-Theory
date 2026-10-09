# W33 TOE research round 12 — five independent fronts (9 October 2026)

## Intake, provenance and strict scope

The authorized Windows repo `C:\Repos\Theory of Everything` was fast-forwarded from our prior `9a2968cc503bfa2c71f1be965657be1d1fca49a2` to the next parallel Pass398-only master `7d496373cb4069bd039a576217681bf64e302e4f`. Pre-existing modified `.continuity/*`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `analysis/w33_pass10956_*` and untracked `.research_*` are preserved; do not stage unrelated files.

This pass executes, with explicit research limitations, the five independent proposals from round11:

1. quantitative full-H lower form: exact nonvanishing local certificate on a zero set of the previous simple scalar potential; **not a global (E_0) enclosure**.
2. string spectrum/F flatness: direct original WSL orbifolder exports with SHA fingerprints and named finite-coupling matches for sixteen candidate supports; **not a complete CFT selection or F-flatness proof**.
3. true infinite-H ground symmetry: an exact finite-field *magnetic-curvature obstruction* to a naive scalar positivity-improving proof; **not an actual irrep determination**.
4. optical full-path monitoring: mathematically justified per-shot clipping before randomized frame averaging, synthetic power and falsification stress.
5. geometric continuum: exhaustive 85,320 native quotient choices on an explicit universal Abelian W33 cover, demonstrating chosen rank-three heat diffusion without a unique emergent space.

Pre-existing ownership: Pass11769 built the 160-current (L^2(\mathbb R^{78})) quantum Hamiltonian; Pass11778 proved a *qualitative* discrete compact spectrum and positive ground excitation gap; Pass11797–11801 own the recovered heterotic (Z_6)-II source and corrected (R/\mathrm{nonR}) metadata; BT1688 owns the complex irreducibility of (H_1\cong\mathbb Z^{81}); BT548 / Pass4019–4024 own the original degree-six line-graph -2 flat band; our previous rounds own the degree-30 triple graph, optical shams, named 16 three-singlet candidate filters and their integer corrected-R necessary witnesses. The previous `analysis/w33_20261009_universal_abelian_cover.py` already materialized the deck group (\mathbb Z^{81}): do not claim to rediscover it.

### External physics literature checked

- [Kobayashi et al., *Revisiting Coupling Selection Rules in Heterotic Orbifold Models* (2011)](https://arxiv.org/abs/1107.2137): gauge invariance, space-group and (R) are not a complete selection test. Extra torus-lattice and worldsheet-instanton constraints exist.
- [Cabo Bizet et al., *R-charge Conservation and More...* (2013)](https://arxiv.org/abs/1301.2322): the non-prime orbifold \(\gamma\) correction, Rules 4 and 6 and instanton sensitivities.
- [Parameswaran and Zavala, *Worldsheet instantons and coupling selection rules* (2014)](https://arxiv.org/abs/1401.6162): broader CFT context.

**No measured photonic device, physical mass, true F-flat vacuum, experimentally tested scattering process, global numeric quantum spectral lower bound, unique emergent Einstein geometry, or completed Theory of Everything is asserted.**

## 1. Full quantum Hamiltonian: an exact cycle-dual **positive local lower bound** on a former scalar-bound zero

Recall the exact 78-dimensional Hamiltonian
```
H=sum_{e=1}^{160} [(V_e.q+a)(U_e.P+a)]²,    a=1/sqrt20,
h[psi]=sum_e ||(V_e.q+a)(U_e.P+a)psi||².
```
The previous scalar local lower-form bound `V_CS(q)=(160a)^2/sum_e (V_e.q+a)^(-2)` was defined as zero on the union of all 160 hyperplanes `V_e.q+a=0`. A zero *bound* at a hyperplane does not imply the quantum kinetic form is locally zero.

Choose one edge `e0=0` and the explicit real configuration
```
q_*=-a V_{e0}/||V_{e0}||².
```
Exactly one of the 160 factors `z_e=V_e.q_*+a` vanishes, namely `z_{e0}=0`. Construct the shortest **eight-edge Levi cycle** containing `e0`, with alternating signed edge indicator `c_e=+1,-1,+1,...,-1`. The integer 160×80 transport incidence obeys `c^T U=0` and `sum c_e=0`; likewise `ones^T U=0`. Therefore the integer dual vector `w=ones-c` has
```
w[e0]=0,   U^T w=0,  sum_e w_e=160,
distribution w_e: 0×4, 1×152, 2×4.
```
For any such left-null `w`, Cauchy-Schwarz yields the exact local sharp quadratic-form certificate
```
V_opt(q) >= a² (sum_e w_e)^2 /
                sum_{e:z_e!=0} w_e²/z_e².
```
At the chosen `q_*\), the factors are `z_e=a*t_e` with `t_e=(3120-(40V_e).(40V_e0))/3120` EXACT rational numbers, and `a^4=1/400`. The resulting *exact Fraction calculation* proves
```
V_opt(q_*) >= 0.330020239522502... > 0.
```
An independent numerical optimization over the actual 78 momentum directions gave `V_opt(q_*)≈0.347075766157703`, consistent with the certified lower bound. Meanwhile the prior coarse `V_CS(q_*)=0`.

This is a genuinely useful weighted dual witness: the eight-cycle algebra repairs one artificial zero of the earlier harmonic-mean barrier. **It does not cure the known classical zero** with 156 vanishing factors, prove a uniform global E0 or control exterior IMS error. The global lower spectral enclosure remains open; Pass11778's qualitative positivity is separate and prior.

Producer `analysis/w33_20261009_weighted_cycle_local_quantum_bound.py` + exact integer/Fraction output.

## 2. Full model: original orbifolder exported **named couplings** versus sixteen tri-singlet candidates

We read these files **directly and read-only** from the authorized connected WSL installation, with SHA-256 per file:

```
/home/wiljd/orb/scan/cp2/out/Z6II_34__SM_20260917_1558.dbd
/home/wiljd/orb/scan/cp2/out/Z6II_34__SM_20260917_1558.mu
/home/wiljd/orb/scan/cp2/out/Z6II_34__SM_20260917_1558.ch
/home/wiljd/orb/scan/cp2/out/Z6II_34__SM_20260917_1558.w
/home/wiljd/orb/scan/cp2/out/Z6II_34__SM_20260917_1558.model
/home/wiljd/orb/scan/cp2/sp/Z6II_34__SM_20260917_1558.sp
```

The file-type grammar matters: `.dbd` has **170** finite `C <degree> <names>` records, `.mu` has **51**. The `.ch` file comprises `F <state> <charges>` rows, `.w` comprises `W` state-weight records, `.sp` comprises `S` state/spectrum rows with twist `k`, constructing coordinates `n`, gauge dimensions and charges. The latter are **not comprehensive superpotential amplitude catalogs**. In total, 221 finite, distinct named C couplings were enumerated (source hashes retained in JSON).

For each of sixteen earlier tri-singlet candidate VEV supports, compare the EXACT MULTISET of fields in each previously verified corrected-`R/nonR` necessary monomial to the finite C records, without reordering or renaming field content beyond sort equality.

- Four candidates containing `n83` in the previously selected combinations have **ten direct exact named colored-sector matches** each. These are `(n51,n79,n83)`, `(n65,n79,n83)`, `(n51,n83,n86)`, `(n65,n83,n86)`.
- The ten finite matched candidates span **a colored 7×10 structural matching rank of five**, not seven, within this **incomplete finite exported subset**. Actual permitted but unexported higher-order couplings remain possible. A catalog matching graph, even when full, is *not* a proof of nonzero CFT numerical coefficients or actual mass-matrix rank.
- Other twelve tri-singlet candidates have no exact complete-monomial match **in this particular limited finite export**. This does NOT veto their higher-degree couplings.
- The known necessary-rule candidate `n81*n17*n82`, which conditionally contributes the outsider (F_{n81}\) derivative if its physical coefficient is nonzero, is **absent in these limited exported C records**. Absence is **NOT** evidence the term vanishes in the exact CFT.
- The finite C records do not independently give a complete F-term superpotential. No F-flatness result follows.

The source record for several matching colored terms is explicitly `C 5 d_1 bd_7 n_17 n_82 n_83`, rather than an invented model-independent coupling. This cross-check strengthens provenance and also narrows what is currently known: full structural rank seven after charge/R screening is still a **necessary possibility**, not yet supported by a complete named CFT coefficient catalog.

This is the first pass here to cross-check the newly identified 16 candidate monomials **against the real original WSL export files** and classify exactly which files actually contain couplings.

Producer `analysis/w33_20261009_heterotic_wsl_catalog_F_audit.py`, original WSL SHA fingerprints and all 16 masks in JSON. External selection-rule literature above explains why these files cannot substitute for fixed-point instanton evaluation.

## 3. True quantum vacuum irrep: an exact **magnetic curvature** obstruction to a naive uniqueness theorem

The first-order terms of the true full-H differential quadratic form are naturally a variable kinetic metric and a one-form connection:
```
z_e(q)=V_e.q+a,
K(q)=U^T diag(z²)U,
b(q)=a U^T(z²),  A(q)=K(q)^(-1)b(q).
```
On any chart with full-rank (K), the scalar minimum is `V_opt=a² sum z² - b^T K^-1 b`. A scalar positivity-improving Schrödinger ground-state uniqueness argument might be tempting **if** a phase `exp(i phi(q))` could globally remove (A(q)). It cannot whenever `dA\ne0`.

We first tested the analytic derivative formula
```
partial_j A_i =
  [2 K^-1 U^T diag(z*(a-U A)) V]_{ij}
```
in an orthonormal 78-dimensional coordinate chart; numerical antisymmetry is zero at the maximally symmetric origin but nonzero at generic small displacements. We then strengthened this to an **EXACT finite-field certificate**, avoiding any reliance on a nonzero floating point number as a theorem.

Choose the configuration (q=a(e_0-e_{39})/10) and the explicit 80×78 integer zero-sum coordinate basis (D). **Crucial cotangent detail**: for (q=D x), the differential vectors transform as `U D(D^T D)^(-1)`, whereas (V) position gradients transform as `V D`; omitting this dual metric gives incorrect curvature values. Construct the corresponding integer numerator matrices `u,v`, integer slopes `t=400+v[:,0]`, and the exact rational curvature formula
```
C=32000*T^-1 * u^T diag(t*(1-u*T^-1*b))*v,
T=u^T diag(t²)u, b=u^T(t²).
```

An exact modular Gauss–Jordan solve of (T) and the selected derivative columns at primes **10007 and 10009** proved a nonzero antisymmetric curvature entry indexed **(35,46)**, with residues **5309 and 44**, respectively; the denominator matrices are invertible modulo both primes. A rational quantity whose modular residues are nonzero cannot vanish.

Thus **no local scalar U(1) phase removes the effective first-order connection at this point**. This blocks a naive application of a scalar Perron–Frobenius positivity argument to certify a simple trivial vacuum. It does NOT imply the full-H ground is degenerate, that its PSp representation is nontrivial, or give a numerical ground-energy lower enclosure.

Producer `analysis/w33_20261009_quantum_curl_exact_modular.py`, two modular exact certificates and carefully distinguished derivative/cotangent coordinates, alongside `analysis/w33_20261009_quantum_connection_curl_audit.py` for independent numerical probes. The exact modular code is the stronger certificate.

## 4. Photonic fault tolerance: clip **each shot before** taking independently randomized frame means

The earlier robust null test tolerated at most (m) **entire compromised frames**. That premise was hard to certify against a burst of isolated arbitrarily large spikes, especially because a partial sentinel cannot catch every individual fault.

We derive a stronger hardware-relevant *clipped score* inequality. Independently draw a Rademacher sign (r_b=\pm1) for each frame (b\), with (L) raw homodyne weighted samples per frame. Let (y_{0,b,i}) be clean sharp-null observations, potentially arbitrarily temporally correlated but independent of the randomized signs, and (Q^2_{b,i}\ge0) trusted. For good shots:
```
yobs[b,i]=y0[b,i]+r[b]*delta[b]*Q²[b,i],  |delta[b]|<=d.
```
Up to (M) raw shots may instead be **arbitrarily corrupted after seeing r**. Clip raw readings to `[-T,T]` **before averaging each frame**, producing the observed vector `zobs_b`. Since clipping is 1-Lipschitz and changes at most `2T` per bad shot,
```
||zobs-z0||_1 <= e1 = d*sum_b Qbar²_b+2*T*M/L,
||zobs-z0||_2 <= e2 = d*||Qbar²||_2+2*T*M/L.
```
The second e2 bound uses `||bad_frame_mean_errors||_2<=||...||_1`; it remains valid even when ALL bad shots concentrate in one frame. A conditional Rademacher Hoeffding bound plus the triangle inequality gives a uniform level-α sharp-null test:
```
REJECT if
|sum_b r_b*zobs_b| >
  e1 + sqrt(2 log(2/alpha))*(||zobs||_2+e2).
```
Unlike the previous frame-only guard, an arbitrarily huge raw fault now costs at most `2T/L` in score, so **no assumption of bounded raw fault magnitude is needed**. However, a credible total bad-**shot** count (M), trusted (Q^2) weights and setting-independent clean outcomes are still necessary. There is no inference if corruption remains unbounded in **number**, or if all good outcomes are sign-dependent.

Simulated **36 null and 36 quartic-proxy** runs with `B=1200`, `L=200`, `N=240000`, `M=40`, `T=.15`, `d=.001`, serial AR(1) drift `rho=.85` and forty (10^8 r_b) malicious samples:
- null false detections **0/36**;
- injected modeled quartic-proxy detections **36/36**.

These counts demonstrate code behavior for synthetic assumptions, **not** optical hardware or physical quartic nonlinearity.

Producer `analysis/w33_20261009_shot_clipped_frame_optics.py` plus JSON.

## 5. Native infinite geometry: exhaustive 85,320 coordinate-three-chord quotients

The previous `analysis/w33_20261009_universal_abelian_cover.py` already showed the *canonical* universal Abelian covering group for the W33 80-vertex,160-edge Levi graph is `H1=Z^81`. A spanning-tree voltage representation has 81 independent graph chords, one coordinate for each integer deck direction.

If we choose **any three distinct chord coordinates** and project the deck `Z^81 -> Z^3`, we get a connected infinite periodic **rank-three by construction** quotient, but that choice is extra external structure. For the projected 3×3 phase-diffusion tensor,
```
K_3=(E_3^T Pi_cycle E_3)/80,
Pi_cycle=I-Divergence^T (Div Div^T)^+ Divergence,
lambda0(k)=k^T K_3 k+O(|k|^3).
```
Every chosen triple has positive definite (K_3). We exhaustively evaluated all
```
binomial(81,3)=85,320
```
three-chord coordinate projections in a fixed deterministic spanning-tree basis, computing all (3\times3) eigenvalues.

The **eigenvalue anisotropy ratios** (largest/smallest stiffness eigenvalue) vary from **1.0375** (near isotropic) to **4.0**. Thus native W33 supports nearly isotropic **ENGINEERED** three-periodic quotients, but not a unique physical 3D geometry: the choice of deck quotient and its Euclidean coordinate norm is not invariant under changes of spanning tree or integer basis. Each selected `Z^3` cover has expected long-time heat scaling `t^(-3/2)` *because rank three was deliberately imposed*, not because general relativity or three spatial dimensions were spontaneously derived.

Prior BT1688 irreducibility of the 81-dimensional cycle representation already obstructs a PSp-equivariant rank-three quotient of the full native 81D module; not our discovery here. This pass adds the **complete 85,320-choice anisotropy census** and explicit extreme voltage choices.

Producer `analysis/w33_20261009_all_coordinate_3D_quotients.py` and 3×3 tensor extrema/quantiles JSON.

## Reproduce and verification

From the Windows repository root:
```powershell
python -m pytest -q tests/test_w33_20261009_five_fronts_round12.py
```
The seven checks regenerate the five fronts, a previous IMS local-bound regression, and a portable committed source-fingerprint check. The live original-export heterotic audit runs on the authorized Windows WSL computer; in CI environments without `wsl.exe`, that live-audit test is explicitly skipped and the frozen source SHA-256 metadata and record counts are still checked. Other scripts use only committed repository inputs.

The named finite F catalog contains actual export **field combinations**, not a CFT amplitude table. The magnetic certificate is an **exact modular algebraic nonzero** proof, stronger than its separate floating probe. The rank-three quotient tensor is a **numerical exhaustive census in a fixed basis**, not an invariant rank-selection mechanism.

## Five best independent follow-on tasks

1. **Global quantum lower enclosure:** exploit the new eight-cycle dual weighting on every hyperplane stratum, then combine with genuine exterior Hörmander/IMS estimates. A numerical `E0` lower bound and quantitative first gap remain open.
2. **Actual tri-singlet heterotic coupling/F-flatness:** recover the full constructing-element fixed point, oscillator and gamma data for all 16 supports, run orbifolder CFT selection Rules4/5/6 beyond corrected R, and calculate the superpotential plus coupled F/D flatness and physical exotic mass matrices. Prioritize the four `n83` supports with named finite C records, but do not assume other twelve are forbidden.
3. **Ground-state irrep lower enclosures:** incorporate the exact nonzero magnetic curvature into sector-resolved full-H lower estimates; do not invoke scalar positivity uniqueness without a valid nonmagnetic gauge. Prove or disprove actual unique PSp-trivial vacuum.
4. **Physical clipped-shot optical interlock:** implement and calibrate trusted hardware clipping before frame aggregation, bound total corrupted shots independently of sign assignments, monitor Q² integrity, and test correlated sham-route detector artifacts in real optics.
5. **Search for non-imposed 3D geometry:** test native group-equivariant graph covering constructions beyond coordinate projections, identify possible symmetry-breaking dynamics selecting a physical rank-three quotient, and derive Lorentzian dispersion rather than calling every chosen `Z^3` cover gravity.

**Research boundary:** No physical Theory of Everything has been established.
