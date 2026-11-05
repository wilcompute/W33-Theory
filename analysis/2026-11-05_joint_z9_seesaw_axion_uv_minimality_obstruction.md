# 2026-11-05 — Proton-safe flavor \(U(1)\), generic neutrino masses, and the renormalizable axion-quality obstruction

**Status:** Two executable producers, two JSON certificates, and twelve independent tests. The framework of gauged flavor-nonuniversal baryon/lepton numbers and proton-protecting residual \(\mathbb Z_9\) already exists in Greljo–Ponce Díaz–Thomsen (arXiv:2505.18259, 2025) and the extension of Davighi–Greljo–Ponce Díaz (arXiv:2609.01712, 2026). **No priority or novel exact-stability theorem is claimed.** This experiment reconstructs a *specific minimal* charge/vev choice and subjects it to the simultaneous seesaw, discrete-baryon, axion-quality, and radiative-gauge requirements.

## Proven starting no-go in the stated generation-universal field inventory

For generation-universal extra \(U(1)_X\) charges \(q_X(Q)=q\), \(q_X(L)=\ell\) and **only** the three ordinary SM generations of chiral \(SU(2)_L\) doublets, the mixed \(SU(2)^2 U(1)_X\) anomaly condition is \(3(3q+\ell)=0\). Consequently,
\[
q_X(QQQL)=3q+\ell=0.
\]
The customary dimension-six \(QQQL\) proton-decay operator is not forbidden by this extra \(U(1)\) (or any residual subgroup of it). This proof does not require assumptions about the Higgs charge, singlet-neutrino masses or detailed cubic anomalies. It **does not apply** if lepton charges are generation dependent, new chiral doublets contribute to the anomaly, or anomaly inflow/Green–Schwarz terms intervene. An anomaly-free universally charged \(B-L\) seesaw cannot by itself supply exact proton stability.

## A specific family-dependent escape

Use the integer-normalized generator \(X=3(B-3L_e)\) and three LH SM generations with \(N_i^c\). Then:
- All quark doublets have \(X=+1\), all charge-conjugate right-handed quarks \(X=-1\).
- Electron-flavor \(L_e\) has \(X=-9\), with \(e^c,N_e^c\) carrying \(X=+9\).
- Muon/tau leptons and their singlet conjugates have \(X=0\).
- The ordinary Higgs has \(X=0\).
- Two complex singlet scalars \(T,S\) have \(X(T)=-9\), \(X(S)=-18\).

An independent generation/representation-level calculation gives precisely zero for the complete local anomaly list:
\[
[SU(3)]^2X,\quad[SU(2)]^2X,\quad Y^2X,\quad YX^2,\quad X^3,\quad \mathrm{grav}^2X.
\]
In the standard SM, the number of LH weak doublets remains twelve, avoiding a new \(SU(2)\) Witten global anomaly. This finite arithmetic is not a complete nonperturbative discrete-anomaly classification.

If **both** singlets acquire vevs, their charge gcd is \(\gcd(9,18)=9\) so the unbroken subgroup is an exact discrete gauge \(\mathbb Z_9\) (in the primitive normalization). Explicit familiar proton-decay operators have charges:
\[
q_X(QQQL_e)=-6,\quad
q_X(QQQL_{\mu,\tau})=3;
\]
\[
q_X(u^cu^cd^ce^c_e)=6,\quad
q_X(u^cu^cd^ce^c_{\mu,\tau})=-3,
\]
and similarly \(u^cd^cd^cN_i^c\). Each is **nonzero mod 9**.
The exact residual baryon-selection rule is \(\Delta B=0 \pmod3\); this forbids single and double proton/neutron decay in this field-content setting.

A schematic \((u^cd^cd^c)^3 N_e^c\) operator, with three anti-quark triples and one electron sterile LH neutrino, has **zero unbroken U(1) charge** \(-9+9=0\), hypercharge zero, triality zero, even Weyl count and canonical dimension \(15\). This is a **necessary-contraction** example; nonzero SU(3), Lorentz and Grassmann contractions and sufficient distinct flavors need explicit construction. Its existence at the level of charges is consistent with \(\Delta B=-3\) being allowed by the residual selection rule.

## A full-rank but *not predictive* type-I seesaw

The renormalizable Dirac Yukawa selection matrix is
\[
Y_{\nu}\sim
\begin{pmatrix} *&0&0\\0&*&*\\0&*&*\end{pmatrix},
\]
while the symmetric Majorana matrix has entries sourced as
\[
M_R\sim
\begin{pmatrix}
S&T&T\\T&M&M\\T&M&M
\end{pmatrix}.
\]
Here the \(S\) entry represents \(S N_e^cN_e^c\), the \(T\) entries represent \(T N_e^cN_{\mu,\tau}^c\), and \(M\) denotes allowed bare sterile Majorana masses for the neutral \(\mu,\tau\) entries. The numerical producer selects arbitrary nonsingular \(m_D,M_R\) matrices satisfying these patterns, and verifies that \(-m_D M_R^{-1}m_D^T\) is *symmetric, full rank, and has nonzero electron–other-flavor mixing*. It does not fit measured neutrino angles or derive a mass scale. Additional choices of charged-lepton textures are unrestricted within allowed charges.

This explicitly answers an integration question: one can maintain proton-protecting \(\mathbb Z_9\) and allow neutrino flavor mixing, instead of the previous universally charged \(B-L\) model's absence of proton protection. This choice however **sacrifices the earlier rank-two/massless-neutrino ansatz**, because the generic seesaw has rank three. Physics must select one, not conflate them.

## The decisive new *minimality obstruction*: renormalizable axion breaking

The same scalar charges permit
\[
S^\dagger T^2+\mathrm{h.c.},\qquad
q_X(S^\dagger T^2)=+18+2(-9)=0.
\]
This is a **dimension-three**, renormalizable, gauge-invariant operator. Full enumeration of phase-sensitive scalar monomials confirms there are none of degree 1 or 2, but \(S^\dagger T^2\) and its conjugate occur already at degree 3. With both vevs, its scalar potential contains a term proportional to \(\cos(2\theta_T-\theta_S)\), where that relative phase is invariant under the gauged \(U(1)_X\).

The gauge boson eats only **one** combination of scalar phases. The other relative phase becomes massive from a generic nonzero cubic coefficient: it is **not** a protected high-quality Peccei–Quinn axion. The cubic could be set to zero as a choice, but it is *not forbidden by this gauge symmetry*, so a technical naturalness/extra-selection-rule analysis is obligatory.

Thus the elementary model achieves **anomaly freedom + exact proton protection + full-rank seesaw** while **failing high-quality axion protection**. The 2026 axion-quality paper uses **additional deliberate charge/fermion structures** and analyzes mixed fermion operators; we cannot assume its successes transfer to this pared-down two-scalar realization.

## An additional same-action UV pressure: the \(Y\)--\(X\) gauge kinetic matrix

Add the previous candidate vectorlike \((3,2,Y=1/6)\) quark and its Dirac conjugate, with vectorlike \(X\) charges \(\pm1\). In *raw physical* hypercharge units and primitive \(X=3(B-3L_e)\), the full one-loop inverse kinetic matrix beta coefficient above the vectorlike threshold is
\[
B_{Y,X} =
\begin{pmatrix}
127/18 & 52/3\\
52/3 & 383
\end{pmatrix}.
\]
Here \(B_{YX}=52/3\) is large in the chosen charge normalization; a rescaling of \(X\) must be accompanied by inverse gauge-coupling rescaling. **A large raw coefficient by itself is not a physical bound.**

For the deliberately chosen unbroken-basis matching benchmark
\(\mu_0=10^{10}\,\mathrm{GeV}\), \(\mu_U=1.3163\times10^{15}\,\mathrm{GeV}\), \(g_Y(\mu_0)=0.36\), a one-loop necessary condition from keeping the \(K_{XX}\) diagonal positive at \(\mu_U\) is
\[
g_X(\mu_0)<
\sqrt{\frac{8\pi^2}{383\ln(\mu_U/\mu_0)}}
\simeq0.132245.
\]
A *full positive* \(2\times2\) kinetic matrix is a stronger condition; the producer checks eigenvalues for eight benchmark couplings. A small coupling \(g_X=0.05\) remains positive at this one-loop benchmark while \(g_X=0.20\) does not. The matrix-current observable \(q^T K^{-1}q\) is unchanged under a nontrivial diagonal basis rescaling.

**Important domain condition:** \(\mu_0\) is chosen above the assumed \(X\)-breaking vevs and full fermion thresholds. This is *not* the previous high-scale seesaw spectrum—heavy-neutrino masses, vevs and matching would have to be set accordingly. There is no coupled two-loop non-Abelian U(1) matrix RGE here, no kinetic matching below the vevs, and no GUT completion. Consequently the upper bound is only a **conditional, one-loop, chosen-particle-spectrum test**, not an experimentally excluded value of \(g_X\).

## Source ownership / validation / next falsifiers

- \`analysis/toe_20261105_joint_flavor_u1_z9_seesaw_scalar_quality.py\`
- \`analysis/toe_20261105_joint_flavor_u1_uv_coupling_cost.py\`
- \`data/toe_20261105_new_joint_symmetry_z9_seesaw_pq_obstruction.json\`
- \`data/toe_20261105_new_joint_flavor_u1_uv_gauge_cost.json\`
- \`tests/test_toe_20261105_joint_z9_proton_seesaw_pq_uv.py\`

Re-run: \`python -m pytest -q --noconftest tests/test_toe_20261105_joint_z9_proton_seesaw_pq_uv.py\`. This suite regenerates both exact certificates and checks independent charge identities, phase-invariant monomials, textures, anomalies, Dirac/Majorana rank, full matrix eigenvalues, and basis-covariant current couplings.

**Next independent scientific requirements:** (i) genuinely high-dimensional axion selection rule that eliminates \(S^\dagger T^2\) and mixed fermion violations without spoiling the neutrino texture; (ii) full two-loop coupled gauge/Yukawa/scalar RG and precision LFV constraints; (iii) nonperturbative exact discrete-gauge anomaly and higher-dimension ΔB=3 operator matching; (iv) natural light-neutrino/PMNS prediction rather than an existence construction; (v) tests of the symmetry sector together with the causal/gravitational dynamics.

**Literature and provenance:** Greljo, Ponce Díaz and Thomsen, *Insights on the Cosmic Origin of Matter from Proton Stability*, arXiv:2505.18259; Davighi, Greljo and Ponce Díaz, *Axion Quality from Exact Proton Stability*, arXiv:2609.01712; Holdom, *Two U(1)'s and epsilon charge shifts*, Phys Lett B166 (1986) 196; previous local note \`analysis/2026-11-05_latest_five_plus_three_physics_swing_report.md\`. The paper's \(\mathbb Z_9\) proton-selection idea is not novel; the exact two-scalar cubic obstruction is a straightforward charge check for **this** supplied pared-down inventory.


## Quantitative axion-quality stress test (conditional, not an axion solution)

Set purely illustrative scalar vevs \(v_T=v_S=10^{11}\) GeV, and **suppose** the relative phase were intended to act as a QCD axion with unit QCD anomaly number. Normalize the physical gauge-invariant phase \(\varphi=2\theta_T-\theta_S\):
\[
f_\varphi=\left(4/v_T^2+1/v_S^2\right)^{-1/2}
=v/\sqrt5=4.472136\cdot10^{10}\ \mathrm{GeV}.
\]
For a dimensionful coefficient \(\mu\) of \(S^\dagger T^2+\mathrm{h.c.}\), the phase-sensitive potential height is
\[
\Lambda_{\rm break}^4=\frac{|\mu|\,v_Sv_T^2}{\sqrt2}.
\]
Using the conventional QCD susceptibility \(\chi_{\mathrm QCD}\simeq(0.0756\,\mathrm{GeV})^4\), a *sufficient* all-phase quality condition \(\Lambda_{\rm break}^4 <10^{-10}\chi_{\mathrm QCD}\) then demands
\[
|\mu|<4.61958\times10^{-48}\ \mathrm{GeV}.
\]
For the opposite benchmark \(|\mu|=v_T\), the relative-phase tree mass is \(m_\varphi\approx1.8803\times10^{11}\) GeV—entirely unlike a light QCD axion. This illustrates the extreme fine-tuning cost of **trying to repurpose** the bare two-scalar remnant phase as an axion.

**Crucial limitations:** this minimal model has not supplied the heavy QCD-anomalous PQ fermion sector, so it does **not actually contain** an established QCD axion. The quality inequality is only a hypothetical stress test if the missing anomaly were added with unit phase charge. Absolute scalar vevs, phase conventions, QCD anomaly normalization and the cubic coupling are supplied inputs. Suppressing the cubic requires a further actual symmetry, not simply asserting that its coefficient is small.
