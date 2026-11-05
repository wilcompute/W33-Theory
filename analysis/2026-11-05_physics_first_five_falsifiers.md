# November 5, 2026 — Physics-first TOE: Five independent necessary consistency tests

**Scope:** Five model-independent screens and reproducible calculations in
\`analysis/toe_20261105_physics_first_consistency_filters.py\`.
Machine-readable output:
\`data/toe_20261105_physics_first_consistency_filters.json\`.
Regression tests:
\`tests/test_toe_20261105_physics_first_consistency_filters.py\`.

The aim is **not** to infer field equations from finite-geometry numerology.
The question is: what actually must a candidate microscopic Theory of
Everything *derive* rather than merely describe?

## I. Chirality, hypercharge and the neutrino branch: a precise underdetermination

Assume one SM-like generation of *left-handed* Weyl fields
\[
Q:(3,2)_q,\quad u^c:(\bar3,1)_u,\quad d^c:(\bar3,1)_d,\quad
L:(1,2)_\ell,\quad e^c:(1,1)_e,\quad N^c:(1,1)_n,
\]
and one Higgs doublet of charge \(h\). Gauge-invariant Yukawa
couplings imply \(u=-q-h\), \(d=-q+h\),
\(e=-\ell+h\), \(n=-\ell-h\).

The exact \(SU(3)^2U(1)\), \(SU(2)^2U(1)\), mixed gravitational and
\(U(1)^3\) conditions simplify to
\[
2q+u+d=0,\qquad 3q+\ell=0,
\]
\[
6q+3u+3d+2\ell+e+n=0,\quad
6q^3+3u^3+3d^3+2\ell^3+e^3+n^3
=-6h^2(3q+\ell).
\]
Therefore all local polynomial anomalies vanish for **two independent
charge parameters** \(q,h\) once \(\ell=-3q\). Explicitly
\[
X=\alpha Y_{\rm SM}+\beta(B-L),\quad
\alpha=2h,\quad\beta=3q-h.
\]
The one-generation \(SU(2)\) doublet count is
\(3Q+L=4\), even as required to avoid the usual Witten \(SU(2)\)
mod-two anomaly.

If \(N^c\) is absent, the gravitational and cubic anomalies are
respectively \(h-3q\) and \((h-3q)^3\); they force \(h=3q\).
If \(N^c\) has a gauge-invariant bare Majorana mass, then
\(n=3q-h=0\) forces the same relation. Under those stated model
assumptions the usual hypercharge direction is singled out, up to
normalization. **Anomaly cancellation alone does not predict neutrino
mass generation, flavor or the charge normalization.**

The code checks all 49 integral \((q,h)\) grid points in \([-3,3]^2\)
and the rational Standard Model and B-minus-L bases.

### Minimal purely Abelian chiral anomaly control

For \(n\) left-handed \(U(1)\) Weyl fermions, local anomaly
conditions \(\sum_iq_i=\sum_iq_i^3=0\) have no strictly chiral
nonzero-charge solution for \(n\le4\). For \(n=3\),
\(\sum q_i^3=3q_1q_2q_3\) when the sum vanishes; for \(n=4\),
the cubic sum factorizes into three sums of opposite-pair charges.
A complete integer enumeration of primitive five-charge solutions
with \(|q_i|\le9\), modulo sign and ordering, finds exactly one:
\[
(-9,-5,-1,7,8),\quad \sum q_i=0,\quad\sum q_i^3=0.
\]
This is a **known elementary anomaly-free toy example**. It neither
proves a consistent lattice Weyl fermion measure by itself nor
constructs SM matter.

Sources: Minahan/Ramond/Warner, Phys Rev D41 715 (1990);
Gripaios/Nguyen, JHEP01(2026)055;
Lüscher, Nucl Phys B549 (1999) 295, DOI
10.1016/S0550-3213(99)00115-7.

## II. Reconstruct dimension from causal order; distinguish input from emergence

Independent causal-set control on Minkowski Alexandrov intervals.
For dimension \(d\), the Myrheim–Meyer order fraction is
\[
\mathbb E[r_d]=\frac{\Gamma(d+1)\Gamma(d/2)}
 {2\Gamma(3d/2)},\quad
r_d=\frac{\#\{\text{causally related unordered pairs}\}}
            {\binom N2}.
\]
The exact values for \(d=2,3,4\) are \(1/2,8/35,1/10\).
The simulator samples points uniformly by the volume form of each
diamond, counts all timelike pair relations, and inverts the formula.

For N=360 events and 16 independent replications per dimension
(seed 20261105+23d), reconstructed estimates are approximately
\(2.0129,3.0031,4.0670\).

**Critical distinction:** the Minkowski causal cones and integer \(d\)
were *inputs to the random sampler*. This is a successful *recovery*
of geometric dimension from event relations, **not** a theory
selecting four dimensions or generating gravitational dynamics.
Compare the established causal-set dimension literature:
Surya, Living Reviews in Relativity 22 (2019),
DOI 10.1007/s41114-019-0023-1.

## III. Single-excitation versus independent multiparticle locality

Take the bosonic Fock subspace \(\mathcal H_1\) of exactly one quantum
distributed among six spatial modes. The local number operators for
two disjoint mode groups \(A,B\) satisfy identically on this sector:
\[
n_An_B\big|_{\mathcal H_1}=0,\quad
\langle n_A\rangle+\langle n_B\rangle=1,\quad
G^{(2)}_{AB}=\langle:n_A n_B:\rangle=0.
\]
The numerical test uses a random normalized one-excitation wavefunction.
A two-excitation state with one quantum in each region instead has
\(\langle n_An_B\rangle=1\).

Consequently **a literal globally conserved one-excitation passive
model cannot account for two independent local excitation-counting
events in the same trial**. Encoding many logical qubits in many
time/frequency/path modes is a different statement: a high-dimensional
single photon can encode information but is not thereby a physically
independent multiparticle Fock sector. Possible model extensions
include genuine excitation-number changes, ancillas/matter, nonlinear
interactions, and a precisely specified operational encoding.

This is a conditional Hilbert/Fock-space fact, not a no-go for every
speculative single-photon cosmology.

## IV. Why universal limiting light speed needs a mechanism

For each of two independent local discrete scalar fields the
stable wave equation gives
\[
\frac4{\Delta t^2}\sin^2\left(\frac{\omega\Delta t}{2}\right)
=\frac{4v_i^2}{a^2}\sin^2\left(\frac{ka}{2}\right).
\]
The code uses common \(a=1/40,\Delta t=a/2\) but independent
\(v_A=1,v_B=1.2\). Both theories are local/stable and have
\(\partial_k\omega_i\to v_i\) as \(k\to0\). Therefore no
theorem that *local discrete dynamics alone* yields a **universal**
\(c\) can be valid. A candidate TOE needs a shared effective metric,
restored Lorentz symmetry, coupling-flow mechanism, or additional
symmetry fixing common light cones. Nothing here implies measured
Lorentz violations.

## V. The Standard Model gauge couplings do not simply meet

In SU(5)-normalized hypercharge convention, the minimal
three-generation/one-Higgs Standard Model has one-loop coefficients
\[
(b_1,b_2,b_3)=(41/10,-19/6,-7),\quad
\alpha_i^{-1}(\mu)=\alpha_i^{-1}(M_Z)
-\frac{b_i}{2\pi}\log(\mu/M_Z).
\]
For illustrative MSbar Z-scale values
\(M_Z=91.1876\mathrm{\,GeV}\),
\(\alpha^{-1}_{EM}=127.955\),
\(\sin^2\theta_W=0.23122\),
\(\alpha_s=0.1180\), the three **pairwise** crossing scales are:

| Pair | One-loop crossing scale (GeV) | Third inverse coupling mismatch |
|---|---:|---:|
| 1–2 | \(1.0317\cdot10^{13}\) | 5.583 |
| 1–3 | \(2.4326\cdot10^{14}\) | 3.655 |
| 2–3 | \(9.7252\cdot10^{16}\) | 10.584 |

There is no triple intersection in this minimal one-loop model.
A fundamental unified gauge prediction must specify any additional
particles and masses, thresholds, and two-loop terms; it must confront
proton decay and low-energy coupling measurements. Simply noting
that an exceptional Lie group contains suitable subgroups is
insufficient.

References: PDG 2025 QCD (\(\alpha_s=0.1180\pm0.0009\));
PDG 2025 Electroweak Review (\(\sin^2\hat\theta_Z=0.23122\));
PTEP 2025 113B04 (beta coefficients, nonunification). The
electromagnetic normalization above is a common illustrative
Z-scale MSbar reference; quoted scales are *not* precision fits.

## Where this leaves a legitimate TOE programme

These five independent screens locate five genuine missing
*dynamical or physical* derivations: (a) chiral representation and
charge selection, (b) Lorentzian 3+1-dimensional
spacetime and Einstein limit without assuming them at generation,
(c) true multiparticle local operations,
(d) universal effective light cones and equivalence principle,
(e) measured coupling evolution with thresholds and spectrum.

The results are established theories/controls reimplemented as a
common reproducible consistency suite. They are not new experimentally
supported physics. Any proposed TOE must **simultaneously** meet
these requirements and predict at least one parameter or observable
not fitted as input before claiming a genuine breakthrough.


---

## VI. Inverse one-loop GUT-matching as a *falsifiable model-building screen*

The fifth control establishes that *minimal* SM one-loop couplings do not
triple-intersect. Instead of stopping there, solve for a common added
multiplet threshold \(M_X\) and unification scale \(M_U\) under specified
matter quantum numbers. This adds two unknowns to two independently
measured coupling differences:
\[
2\pi(\alpha_1^{-1}-\alpha_2^{-1})_{M_Z}
=(b_1-b_2)t+(\Delta b_1-\Delta b_2)s,
\]
\[
2\pi(\alpha_2^{-1}-\alpha_3^{-1})_{M_Z}
=(b_2-b_3)t+(\Delta b_2-\Delta b_3)s,
\]
where \(t=\log(M_U/M_Z)\) and \(s=\log(M_U/M_X)\).
Require \(0<s<t\), \(1\ {\rm TeV}<M_X<M_U<10^{19}\) GeV.

The executable
\`analysis/toe_20261105_inverse_gauge_threshold_witnesses.py\`
defines nine textbook vectorlike/real-fermion/complex-scalar
representations, exactly derives their rational one-loop
\(\Delta b=(\Delta b_1,\Delta b_2,\Delta b_3)\),
and searches 1-, 2-, and 3-multiplet combinations under *one common
mass threshold*. This limited, declared candidate space yields
2 one-multiplet, 11 two-multiplet, and 46 three-multiplet solutions.

The two single-multiplet one-loop mathematical witnesses are:

| Extra state | Exact \(\Delta b\) | Solved \(M_X\) (GeV) | Solved \(M_U\) (GeV) |
|---|---|---:|---:|
| One vectorlike \((3,2)_{1/6}\) Dirac quark doublet | \((2/15,2,4/3)\) | \(1.43822\cdot10^6\) | \(2.41792\cdot10^{15}\) |
| One \((1,3)_0\) Majorana SU2 triplet | \((0,4/3,0)\) | \(8.05098\cdot10^6\) | \(2.43264\cdot10^{14}\) |

The unified inverse couplings are 38.4017 and 40.3510,
respectively. Exact pairwise residuals are below \(2\cdot10^{-12}\).
The code varies \(\alpha_s\) by \(\pm0.0009\),
\(\sin^2\theta_W\) by \(\pm0.00006\), and
\(\alpha^{-1}_{EM}\) by \(\pm0.01\) over eight corner cases.
Both remain mathematically valid step-threshold fits.

**Do not mistake inverse fits for actual particle predictions.** Their
masses are determined using measured couplings, not computed from a
microscopic mechanism; the selected multiplet catalog is not an
exhaustive classification. No threshold splitting, two-loop analysis,
coupled Yukawa RG, unified representation or proton decay branching
calculation was included. The relatively low convergence scales can
make ordinary GUT proton-decay constraints especially important. For
orientation, Super-Kamiokande's established \(p\to e^+\pi^0\) partial
lifetime lower bound is \(2.4\cdot10^{34}\) years at 90% CL
(Phys Rev D102 112011, 2020); translating it into a limit on this
model requires specifying the heavy baryon-number violating mediators.

This is a useful falsifier scaffold: it converts "unification should
happen" into named candidate representations with calculable
precision-RG and proton-decay confrontations. It does not uniquely
select a UV theory, and it supplies **no evidence** that either
hypothetical multiplet exists.
