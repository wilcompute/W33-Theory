# 2026-11-05 — Beyond Separate TOE Toys: Five Physical Fronts, Three Orthogonal Guards, One Cross-Sector Obstruction

**Research status:** Executed numerical and symbolic consistency tests. The individual effects are established mathematics/physics; the contribution here is their exact *shared falsification workflow* and model-specific numerical benchmarks. No microscopic Theory of Everything, quantum gravity, observed particle spectrum, derived universal light speed, or new particle has been experimentally established.

**Implementation:** Seven executable generators, seven regenerated JSON certificates, and executable regression tests.

| Front | Executable | Output certificate |
|---|---|---|
| 1. Coupling unification + conditional proton decay | \`analysis/toe_20261105_twoloop_proton_consistency.py\` | \`data/toe_20261105_two_loop_threshold_proton_guard.json\` |
| 2. Metric-free causal growth | \`analysis/toe_20261105_causal_growth_without_background.py\` | \`data/toe_20261105_causal_growth_no_embedded_dimension.json\` |
| 3. Two-body locality and scattering | \`analysis/toe_20261105_multiparticle_local_scattering.py\` | \`data/toe_20261105_multiparticle_scattering_locality.json\` |
| 4. Anomaly-free chiral B−L and seesaw | \`analysis/toe_20261105_anomalyfree_bl_seesaw_degeneracy.py\` | \`data/toe_20261105_bl_gauge_seesaw_flavour_degeneracy.json\` |
| 5. Common light cone and one-loop self-energy | \`analysis/toe_20261105_universal_speed_radiative_guard.py\` | \`data/toe_20261105_universal_lightcone_radiative_guard.json\` |
| 6–8. Three independent UV/clock/entanglement controls | \`analysis/toe_20261105_three_orthogonal_quantum_gravity_controls.py\` | \`data/toe_20261105_three_independent_toe_controls.json\` |
| 9. Attempted combined action / gauge kinetic mixing | \`analysis/toe_20261105_crossfront_bl_kinetic_mixing.py\` | \`data/toe_20261105_bl_sm_threshold_kinetic_mixing_no_go.json\` |

Run targeted combined tests from the repository root:

\`\`\`powershell
python -m pytest -q --noconftest tests/test_toe_20261105_eight_physics_fronts.py tests/test_toe_20261105_physics_first_consistency_filters.py tests/test_toe_20261105_inverse_gauge_threshold_witnesses.py
\`\`\`

These independent screens are deliberately not assumed to derive from any particular finite graph. The repo's geometry is not a premise.

## 1 — Actual two-loop gauge running: previously fitted thresholds move by an order of magnitude

Begin with *explicit* minimal-SM beta coefficients (SU5 hypercharge normalization)

\[
b=(41/10,-19/6,-7),\quad
B=\begin{pmatrix}199/50&27/10&44/5\\9/10&35/6&12\\11/10&9/2&-26\end{pmatrix},
\quad d_t=(17/10,3/2,2),
\]
and evolve the **inverse gauge couplings** \(\alpha_i^{-1}=4\pi/g_i^2\):
\[
\frac{d\,\alpha_i^{-1}}{dt}
=-\frac{b_i}{2\pi}
-\frac{\sum_j B_{ij}g_j^2-d_{t,i}y_t^2}{32\pi^3}.
\]
Top Yukawa is evolved at ONE LOOP via
\[
\frac{dy_t}{dt}=\frac{y_t}{16\pi^2}
\left[\tfrac92y_t^2-\tfrac{17}{20}g_1^2-\tfrac94g_2^2-8g_3^2\right],
\quad y_t(M_Z)=0.936.
\]
Bottom/tau/BSM Yukawas, finite matching, heavy threshold splitting,
three-loop gauge effects and two-loop top-Yukawa corrections are excluded.

For each proposed extra fermion, calculate its Dynkin/Casimir matter
contribution above a sharp common threshold. In a product group, a
Dirac/Weyl fermion with group factors \(S_2^i\), \(C_2^j\) contributes
\[
\Delta b_i=\tfrac43\kappa S_2^i,\quad
\Delta B_{ij}=4\kappa S_2^i C_2^j
+\delta_{ij}\tfrac{20}3\kappa S_2^i C_2(G_i),
\quad\kappa=1\text{ (Dirac)},\,\tfrac12\text{ (Weyl/Majorana)}.
\]
For the vectorlike quark \((3,2)_{1/6}\),
\(\Delta b=(2/15,2,4/3)\); for a real adjoint SU2 Majorana,
\(\Delta b=(0,4/3,0)\), \(\Delta B_{22}=64/3\).

Numerically solve two coupled nonlinear crossing equations for
\((M_{\rm threshold},M_U)\).

| Matter content | One-loop threshold (GeV) | Two-loop threshold (GeV) | Two-loop \(M_U\) (GeV) | \(1/\alpha_U\) |
|---|---:|---:|---:|---:|
| 1 vectorlike quark doublet | \(1.43822\,10^6\) | \(2.11891\,10^7\) | \(1.31630\,10^{15}\) | 38.6581 |
| 1 Majorana weak triplet | \(8.05098\,10^6\) | \(8.40613\,10^7\) | \(1.71870\,10^{14}\) | 40.3867 |

The component beta formula and the standard SM B-matrix are from
Jones, Phys Rev D25 581 (1982) and Phys Rev D90 075006, appendix B.
Two-loop *gauge* running is not a complete two-loop threshold EFT.

**Conditional proton partial lifetime filter.** Use only the known
experimental lower bound \(\tau/B(p\to e^+\pi^0)>2.4\cdot10^{34}\)
years (Super-Kamiokande, Phys Rev D102 112011, 2020).
A purely parametric dimension-6 reference scaling is
\[
\tau = K\left(\frac{M_V}{10^{16}\,\mathrm{GeV}}\right)^4
\left(\frac{0.025}{\alpha_U}\right)^2.
\]
For the **illustrative extra hypothesis** \(M_V=M_U\), the minimum
*unspecified* reference normalization \(K\) to satisfy this mode's
bound is \(8.56\cdot10^{37}\) years for the quark, and
\(2.70\cdot10^{41}\) years for the triplet. These are enormous
relative to the **arbitrary reference value** \(K=10^{35}\) years.
This is a serious caution *if* the theory has unsuppressed
baryon-violating vectors at \(M_U\), but is **not a model-independent
exclusion**: their mass \(M_V\), flavor tensors, baryon selection rules,
hadronic matrix elements and hence \(K\) are not derived.
No tree-level baryon-violating amplitude was computed.

## 2 — Generate order without preassigning dimension

The previous experiment reconstructed an input 4D Minkowski interval.
This one genuinely begins with **only** a birth order and intrinsic
stochastic causal precursors: at each new vertex, each earlier vertex
is independently selected as a causal parent with probability \(p\);
their ancestral closures are inherited exactly using integer bitsets.
This is **transitive percolation**, a classical sequential growth toy
known from Rideout and Sorkin, PRD61 024002 (1999/2000).

Run \(n=160,320\), \(p=.025,.065,.15\), three seeded replicates each
(18 generated posets). For intrinsic intervals \([a,b]\) containing
17–180 causally related events, compute the related-pair fraction,
invert the Myrheim–Meyer function
\[
r(d)=\frac{\Gamma(d+1)\Gamma(d/2)}{2\Gamma(3d/2)}.
\]
**Never** apply this Minkowski-interval inversion formula to an
arbitrary entire growth poset and claim its value is a spacetime
dimension; use actual causal intervals and expose both selection and
finite-size biases.

For \(n=320\) the representative three-replicate medians are:
- \(p=.025:\) about \(2.05\)–\(2.23\);
- \(p=.065:\) about \(2.02\)–\(2.09\);
- \(p=.15:\) about \(1.41\)–\(1.53\).

The very sparse \(n=160,p=.025\) ensemble barely produces eligible
intervals. No robust \(d=4\) is selected; not even interval
homogeneity is guaranteed.

This tests a crucial idea without *assuming* a 4D ambient geometry,
but it does not yet derive manifoldlike local 3+1D dynamics,
continuum Einstein equations, or quantum amplitudes.

## 3 — Actual independent local two-particle events require a multiparticle sector

On two sites, exact Bose–Hubbard Hamiltonian in the
\(\{|20\rangle,|11\rangle,|02\rangle\}\) two-boson sector:
\[
H=\begin{pmatrix}
U&-\sqrt2J&0\\
-\sqrt2J&0&-\sqrt2J\\
0&-\sqrt2J&U
\end{pmatrix}.
\]
Evolve \(|11\rangle\) to \(Jt=\pi/4\). Coincidence probability:

| \(U/J\) | \(P_{11}\) |
|---:|---:|
| 0 | 0 |
| .5 | .015532 |
| 2 | .227187 |
| 5 | .865629 |
| 20 | .962461 |

At \(U=0\), the output has perfect bosonic Hong–Ou–Mandel bunching
and mode-entanglement negativity \(1/2\). On a four-site nearest
neighbor chain, the exact two-particle model has nonzero
\(P(n_0>0,n_3>0)\) at finite time, whereas *every*
state in the one-excitation sector obeys
\(\langle n_0n_3\rangle=0\) identically.

The model provides genuine local occupation-number events and
interaction-dependent two-body dynamics. No Lorentz-invariant
scattering matrix, Standard Model QFT or field creation mechanism
was derived. It is a conditional obstacle for a literal
single-excitation universe, not a no-go for all informational
single-photon encodings.

## 4 — One anomaly-free action; neutrino masses still underdetermined

Take the three SM chiral families with
\(3N^c\) (B−L=+1 in LH conjugate notation), Higgs \(H\)
(B−L=0) and one complex scalar \(S\) (B−L=-2):
\[
\mathcal L\supset -\frac14F_{BL}^{\mu\nu}F_{BL,\mu\nu}
+|D_\mu H|^2+|D_\mu S|^2
-\left(Y_\nu LHN^c+\frac12fSN^cN^c+\mathrm{h.c.}\right)-V.
\]
The code explicitly verifies
\(U(1)_{B-L}^3\), mixed gravitational-B−L,
\(Y^2(B-L)\), \(Y(B-L)^2\),
\(SU(3)^2(B-L)\), \(SU(2)^2(B-L)\),
and ordinary hypercharge anomalies **per generation**.
If \(N^c\) is removed, B−L cubic and gravitational
anomalies are both \(-1\) per family.

Choose illustrative heavy masses \(10^{10},\,2\cdot10^{11},
\,5\cdot10^{12}\) GeV. The type-I seesaw,
\(m_\nu=-m_DM^{-1}m_D^T\), is evaluated for an externally
specified approximate PMNS matrix
\((\theta_{12},\theta_{23},\theta_{13},\delta)=
(33.44^\circ,49.2^\circ,8.57^\circ,195^\circ)\),
\(\Delta m^2_{21}=7.42\cdot10^{-5}\mathrm{eV}^2\),
\(\Delta m^2_{31}=2.515\cdot10^{-3}\mathrm{eV}^2\).
The resulting singular masses are
\((0,0.008614,0.050150)\) eV, up to machine epsilon.

With one vanishing column of \(Y_\nu\), its rank is two even
though the **three anomaly-cancelling** right-handed Weyl fields
are present. Three distinct \(SO(2)\) Casas–Ibarra rotations give
different Dirac matrices reproducing *exactly the same* light mass
matrix; changing the heavy mass of the decoupled sterile state
does not affect it.

This proves **existence and nonuniqueness**, NOT the measured
masses, the family count or CP phase from first principles.
The Lagrangian, flavor choices and spacetime metric are
introduced as input. See two-right-handed-neutrino type-I
seesaw literature, PRD97 115016 (2018).

## 5 — Interaction may gap a relative field rather than select universal \(c\)

Two local scalar fields with independent spatial-gradient
coefficients \(c_A=1,c_B=1.2\) and local spring
\(g(\phi_A-\phi_B)^2/2\) have squared-frequency matrix
\[
K(k)=\begin{pmatrix}
4c_A^2\sin^2(ka/2)/a^2+g&-g\\
-g&4c_B^2\sin^2(ka/2)/a^2+g
\end{pmatrix}.
\]
At \(g=0\) there are **two gapless branches** with
different limiting velocities. At any \(g>0\) in this model,
there is only *one* gapless acoustic branch:
\(c_{\rm eff}=\sqrt{(c_A^2+c_B^2)/2}\simeq1.104536\);
the relative branch has an optical gap \(\sqrt{2g}\).

Therefore a common *surviving* acoustic cone is not a
demonstration of a universal cone **for both matter species**.

For separate quartic \(\phi^4\) and a mixed
\(\phi_A^2\phi_B^2\) interaction, the simple one-loop
self-energies are tadpoles independent of **external** momentum.
Numerical finite-cutoff shell integrals give nonzero mass
corrections but zero one-loop wavefunction/velocity corrections.
No one-loop speed-attraction has been demonstrated in this
restricted scalar system; the real task is an interacting,
3+1D, multiple gapless matter theory with a stable common
Lorentz group.

## Three orthogonal physical controls

### A. Anomaly freedom is not UV completion
The strictly chiral, anomaly-free five-Weyl charge set
\((-9,-5,-1,7,8)\) has \(\sum q_i=\sum q_i^3=0\), but
its positive Abelian gauge coefficient is
\[
b=\frac23\sum q_i^2=\frac{440}{3}.
\]
If \(g(1\mathrm{\,TeV})=0.2\), the formal one-loop pole occurs
at \(7.0\cdot10^8\) GeV and the convention
\(\max_q(qg)^2/(4\pi)=1\) is crossed already at
\(2.18\cdot10^7\) GeV. Choosing smaller \(g\) moves the
threshold dramatically, revealing another free parameter,
not a universal physical prediction.

### B. Two-clock redshift is operational time, not mere tick counting
For a weak-field potential difference \(\Delta\Phi/c^2=10^{-15}\)
and optical frequency \(f_0=10^{15}\) Hz,
\(\Delta\varphi=2\pi f_0 t\,\Delta\Phi/c^2\).
A path-superposed clock loses Ramsey visibility
\(|\cos(\Delta\varphi/2)|\); at \(t=0.5\) s the internal-clock/path
entanglement is **one ebit** in this ideal model, and
at 1 s the two phases rephase. Relating "time = exchanges"
to physical proper time requires trajectory-dependent
local rates and quantum coherence, not a universal integer counter.
Gravitational redshift **was an input**, not an emergent result.

### C. Entanglement scaling does not automatically imply gravity
A 128-site periodic harmonic chain has exact Gaussian
ground-state reduced covariance entropies. For block lengths
4,8,16,32,48,64 and mass gap \(m\):
- nearly critical \(m=.001\): chord-log fitted slope \(\simeq0.314\),
  close to but not exactly the \(c/3\) CFT expectation due to
  finite size and a regularized zero mode;
- gapped \(m=.5\): slope \(0.000498\),
  and entanglement saturates with block length
  (1D area-law behavior).

Such scaling is necessary in many entanglement-gravity approaches,
but is **not** a derivation of the Einstein equations or a 3+1D
black-hole area law.

## A single-action **integration** obstruction: induced Y–B−L mixing

The previous eight fronts are deliberately not independent
successes of one microscopic action. Put the three-generation
anomaly-free \(B-L\) seesaw next to the single vectorlike
\((3,2)_{1/6}\) quark of the two-loop gauge fitting test;
assign it physical B−L=1/3 and include its conjugate Weyl
partner. All polynomial chiral anomaly checks still vanish.

However **gauge-kinetic mixing is radiatively generated**.
In left-handed Weyl and complex-scalar notation,
\[
b_{Y,BL}=
\frac23\sum_{\rm Weyl}n_fY_f(B-L)_f
+\frac13\sum_{\rm complex~scalar}n_sY_s(B-L)_s.
\]
For 3 SM families + 3 sterile conjugates,
\(\operatorname{Tr}[Y(B-L)]=8\);
the vectorlike quark pair adds \(2/3\).
Hence
\[
\operatorname{Tr}[Y(B-L)]=\frac{26}{3},\qquad
b_{Y,BL}=\frac{52}{9}\ne0.
\]
Including the \(S(-2)\) scalar, the diagonal
\(B-L\) one-loop coefficient is \(b_{BL}=116/9\).
Thus setting \(\chi_{Y,BL}=0\) at one renormalization scale
is **not radiatively stable** without another symmetry or
additional matter cancellation.

For illustration only, fixed
\(g_Y\simeq0.357,g_{BL}=0.2\), a zero mixing boundary
at \(10^{10}\) GeV and the quark candidate's
\(M_U=1.3163\cdot10^{15}\) GeV produce leading-log
\(\Delta\chi\simeq0.03083\).
This is NOT a full U1xU1 kinetic-mixing RGE:
couplings run, broken-phase thresholds and off-diagonal
couplings must be evolved together, and mass matching depends
on the symmetry-breaking scheme.

**This is the sharpest cross-domain lesson this round**:
the separate "successful" two-loop diagonal gauge fit and
anomaly-free gauged B-L neutrino model **do not simply combine
as one radiatively closed theory**. A unified TOE must pass
cross-sector beta functions and renormalized field dynamics.
See standard B-L kinetic mixing treatments:
https://inspirehep.net/files/34cfe7040a800f05c22593d549d9ffaa ;
https://doi.org/10.1103/PhysRevD.25.581 .

## Scientific disclosure and next decisive model-selection gates

- No particle threshold above has been measured; all new masses
  come from *inverse fits* to known gauge data.
- No observed light-speed equality, curved Lorentzian spacetime,
  general relativity, or quantum measurement statistics are
  independently derived from the same microscopic dynamics.
- Models are explicitly finite, perturbative or phenomenological;
  their validity domains must not be conflated.
- The cross-sector \(Y\)--\(B-L\) kinetic mixing is *a necessary
  additional equation*, not evidence that a specific E8, W33,
  lattice or causal-set microscopic description is uniquely right.
- The most useful next steps are full coupled two-loop
  \(U(1)_Y\times U(1)_{B-L}\) matrix RG,
  a dynamical Lorentzian causal-set matter action with no
  preinstalled dimension, and a genuinely parameter-reducing
  chiral/flavor vacuum-selection mechanism.

**Citations / verified sources:** Jones, PRD25 581 (1982);
SM two-loop coefficients, PRD90 075006, Appendix B;
Rideout & Sorkin, PRD61 024002 (2000);
two-right-handed-neutrino seesaw, PRD97 115016 (2018);
Super-Kamiokande, PRD102 112011 (2020);
classic B-L kinetic mixing treatment
https://inspirehep.net/files/34cfe7040a800f05c22593d549d9ffaa.


## Parallel-work calibration after completion (same-day incoming commit)

While these independent producers were running, the master branch advanced to
\`5c033ec6724c6ee381aa31e6a1203f8f47e8c609\`,
\`analysis/PASS12603_12608_PQ_ASSISTED_UNIFICATION.md\`.
That track independently derived the **same single vectorlike (3,2,1/6)
two-loop threshold** near \(2.12\cdot10^7\) GeV and confirmed
the original Q-assisted unification has prior art in
Di Luzio–Mescia–Nardi (arXiv:1705.05370). This is a useful cross-check,
**not a second independent novel prediction**.

The parallel track additionally identifies a three-vectorlike-fermion
model with common scale near \(2.7\cdot10^{10}\) GeV and a **conditional**
proton lifetime around \(3.5\cdot10^{34}\) years, with its GUT completion,
threshold and strong-CP quality caveats. These results are distinct
from the intentionally limited *single-multiplet* two-loop scan here.
The conditional proton lifetime it uses has a fixed model-reference
normalization, while the present scan transparently exposes its
unknown normalization \(K\) rather than assuming a GUT model.
Neither calculation experimentally establishes a new particle or a
completed unified action.

The new work in **this** note is instead the cross-front audit
and directly executable no-go/consistency tests for causal dimension,
multiparticle Fock locality, anomaly-free seesaw degeneracy,
common limiting-speed dynamics and nonzero radiative
hypercharge–B−L mixing. Even those constituent physical principles
are known; no claim of mathematical or physical priority is made.
