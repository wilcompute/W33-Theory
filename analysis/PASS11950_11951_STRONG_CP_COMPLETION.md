# Passes 11950–11951: the missing gauge factor and a parity-safe vectorlike alternative

Codex track, 12 October 2026. Reservation `b9e607ea9` was pushed before computation.
Producer: `analysis/w33_pass11950_11951_strong_cp_divisor_and_vectorlike.py`.
Certificate: `data/w33_pass11950_11951_strong_cp_divisor_and_vectorlike.json`.
Independent controls: `tests/test_w33_pass11950_11951_strong_cp_completion.py`.

## What changed, and what was actually reviewed

GitKraken intake from our last receipt `9039660bf` to `f8a2e0071` contains **330 commits and 916 changed paths**.
The complete current-file intake is hash-bound in `data/w33_pass11950_intervening_material_intake.json`:
108,332,684 bytes, 434 parsed Python files, all JSON nodes traversed, no parse errors.
That is **machine intake, not a claim that every file or individual patch received human semantic review**.
Close reading for this attack follows the reports on the finite Lorentz/chirality firewall, Siegel and Hermitian
moduli, the E8/SU9 vacuum and chiral-spectrum failures, magnetized fluxes and normalization, flavour qutrits,
Witting displacement and soft supertraces, Weber spectra, CKM/PMNS and the axiflavon correction. Source-level
dependencies include TOE38/39 theta kernels, Pass11942's actual fitted matrices, Pass11947/49 phase probes and
the certified Qpsi parity. The broader independent code/cover/hardware material is inventoried; it is not all
independently validated by this packet.

The user explicitly replaced the old singlet-support route. No old singlet mass-mask pass was extended here.
The forty-points manuscript was refreshed through its updated physics/ledger dependencies; its new CP sentence
already records the Pass11949 retraction. Neither that manuscript nor its PDF is modified by this packet.

**The key intake result:** Pass11949's quality failure stands. An approximate up-phase rephasing cannot function
as a QCD axion when the ordinary Yukawa loop potential dominates QCD. Instead of trying to make that same phase
an axion, this packet examines the full strong-CP invariant and a different mass architecture.

## 11950: local divisor matching is a necessary condition on the gauge sector

In the stated supersymmetric, real-Higgs-VEV convention, the physical quantity is

\[
A(\Omega)=e^{-8\pi^2 f_3(\Omega)}\det Y_u(\Omega)\det Y_d(\Omega),
\qquad \bar\theta=\arg A.
\]

The gauge kinetic function matters: `arg det(Yu Yd)` alone assumes a corresponding gauge-angle convention.
In an actual supersymmetry-breaking completion, gluino and other phases must also be tracked. This is standard
modular strong-CP theory, not a new mechanism. See Feruglio–Marrone–Strumia–Titov,
[arXiv:2505.20395](https://arxiv.org/abs/2505.20395), especially equations 2, 18 and the regularity assumptions.

### The separating divisor is already known; the completion requirement is new here

TOE38 owns the moment-determinant coefficient; TOE39 owns its odd parity and fifth-order remainder;
Pass11947 owns the phase winding in the flavour chain. In a **fixed physical sector marking**,

\[
\det Y_u=C(\tau_1,\tau_2)\varepsilon^3+O(\varepsilon^5),\quad
C=\frac{(6\pi i)^3}{2}\det[f_0,f_1,f_2]\det[g_0,g_1,g_2].
\]

We cite those results rather than claiming the cubic determinant as new. The coefficient is nonzero at both
current Pass11942 quark fits. Independent theta evaluation gives winding **3** around a small epsilon circle.

Suppose the down determinant is nonzero and `f3` is finite and holomorphic near `epsilon=0`.
Its exponential is nonzero, so **A also has a zero of order three**. If A were real positive throughout a complex
open neighbourhood away from the divisor, the open mapping theorem would force it to be constant. Analytic
continuation to the divisor would then force that nonzero constant to be zero, a contradiction.

Thus this marked theta family has **no identically protected, zero-strong-CP completion with a regular gauge
kinetic function across the separating divisor**. This does not exclude an isolated CP-safe selected vacuum,
a different Yukawa architecture or a singular threshold completion.

For a constant nonzero A one necessarily needs

\[
e^{-8\pi^2 f_3}\sim\varepsilon^{-3},\qquad
f_3=\frac3{8\pi^2}\log\varepsilon+\text{regular}.
\]

One loop around epsilon shifts `f3` by `3i/(4pi)` and the gauge theta by `-6pi`, compensating the Yukawa winding.
This is a local matching condition, **not a calculation of a string threshold**.

### A concrete genus-two threshold target

The Igusa form `chi10` is, up to a constant, the product of squares of the ten even half-characteristic theta
constants on **Omega**, whereas our Yukawa theta series uses **3 Omega**. At a generic product torus nine
constants are nonzero; the odd-odd one has a simple separating zero. Hence

\[
\chi_{10}=D(\tau_1,\tau_2)\varepsilon^2+O(\varepsilon^4).
\]

The required pole can therefore be locally represented by

\[
f_3=\frac3{16\pi^2}\log\chi_{10}+\text{regular},\qquad
\frac{(\det Y_u)^2}{\chi_{10}^3}\longrightarrow \frac{C^2}{D^3}\ne0.
\]

The squared ratio avoids choosing a square-root branch. The coefficient **3/2** multiplying `log chi10` in
`8pi² f3` is a falsifiable target for an actual colored threshold inventory. Igusa forms already occur in
heterotic gauge thresholds: Kawai [hep-th/9512046](https://arxiv.org/abs/hep-th/9512046), and
Datta–David–Lüst [arXiv:1510.05425](https://arxiv.org/abs/1510.05425). Those are different compactifications;
their existence does not fix this coefficient for W33.

Both fitted factor moduli give convergent nonzero squared ratios. The ratios differ and have generic complex
phases: **divisor cancellation alone is not a strong-CP solution**. It fixes neither the regular part of f3 nor
the global modular law. TOE38's marking firewall remains essential; the reshaped determinant is not automatically
a scalar under entangling modular transformations.

With `K=-log det Im Omega` the separating locus is at finite metric distance for fixed elliptic factors,
`K_epsilon,epsilonbar=1/(2 Im tau1 Im tau2)`. It is not the decompactification cusp. A threshold singularity there
therefore requires independently identified new physics; it cannot be justified just by calling it a cusp.
The logarithmic formula drives the real part of f3 downward arbitrarily close to the divisor, so one weakly
coupled EFT cannot be extrapolated all the way there with a finite constant dilaton.

Positive Hermitian canonical-normalization matrices multiply determinants by positive real numbers.
They cannot erase this holomorphic phase/winding. Their flavour effects and physical loop amplitudes still matter.

## 11951: a different determinant architecture, with the E6 parity gate checked

Nelson–Barr is standard prior art, including an E6 implementation:
Schwichtenberg–Tremper–Ziegler [arXiv:1802.08109](https://arxiv.org/abs/1802.08109).
Their model assumes a scalar sector; it is not a completed W33 vacuum.

For real nonsingular m, positive real mu and a complex row B, declare

\[
\mathcal M=\begin{pmatrix}m&0\\B&\mu\end{pmatrix}.
\]

Its full determinant is exactly `mu det m`, independent of B, although its light left-handed Hermitian matrix
in the heavy-decoupling limit is complex:

\[
H_d=mm^T-\frac{mB^\dagger Bm^T}{\mu^2+|B|^2}.
\]

### Exact witness and a constructive inverse

Take

\[
m=\begin{pmatrix}1&1&0\\0&2&1\\1&0&3\end{pmatrix},\quad
B=(1+i,2-i,1+2i),\quad\mu=2.
\]

Then

\[
\det\mathcal M=14>0,\qquad
\operatorname{Im}(H_{12}H_{23}H_{31})=\frac{119}{64}\ne0.
\]

With a distinct real diagonal up sector this is physical weak CP violation at tree level, while the declared
full colored determinant is real. It is not the false implication “Z3-neutral determinant means real” in the
old `test_strong_cp_axionless_cccix.py`; that historical file is left untouched, not endorsed.

An inverse construction avoids another free-parameter optimizer. For any positive Hermitian 3x3 target H,
write `Im H=a b^T-b a^T` (every real antisymmetric 3x3 matrix is decomposable). Let `u=a+i b`; then
`S=H+u u†` is real positive. Choose real Cholesky `m m^T=S`, and `c=m^-1 u`. Positivity of H gives `|c|²<1`.
Setting `mu=1`, `B†=c/sqrt(1-|c|²)` reproduces H exactly by the displayed Schur form.

Using the repo's supplied quark comparator, this reconstructs all down masses and the mass-labelled CKM with
`J=3.080000000000401e-5`; the Hermitian reconstruction residual is `6.17e-19`. This is **input reconstruction,
not prediction**. Full finite 4x4 singular-value controls at heavy scales 100, 1000, 10000 retain the target light
masses to better than `1e-8` relative and give the expected suppressed weak-unitarity defect. The supplied up
sector may be a real diagonal matrix with the desired positive masses; neither its entries nor m are derived.

The raw reconstructed `|B/mu|` reaches about61. The common scaling `(B,mu)->(B/64,mu/64)` leaves the light Schur
matrix unchanged and puts every B component below1. It introduces a supplied small mu, not a predicted scale.

### Why the existing E6 exotics cannot simply be reused

The committed parity certificate says

\[
27=16_1+10_{-2}+1_4,\qquad P=(-1)^{Q_\psi}.
\]

Ordinary `d^c` in16 is odd; the vectorlike D in10 is even. Their mixing bilinear is odd. **Every product of
parity-even condensates keeps that bilinear forbidden, to all orders.** In the native 27³ cubic its mixing needs
an odd16 background; the certified 40 `(16,16,10)` and five `(10,10,1)` triads verify the representation gate.
This obstruction is specific to the standard stored parity; it says nothing universal about the alternative
full-field orbifold parities or adding a vectorlike16 pair.

### Explicit parity-compatible SM-level alternative

Add `D=(3,1,-1/3)` and `Dc=(bar3,1,+1/3)` **both matter-parity odd**, two even singlets S1,S2 and two even
spectators T1,T2. Under an additional local U1_X assign

| fields | Q, dc, Hd | D | Dc | S1,S2 | T1,T2 |
|---|---:|---:|---:|---:|---:|
| X | 0 | +1 | -1 | -1 | +1 |

The new chiral inventory has exactly zero SU3²X, Y²X, YX², gravitational-X and X³ anomaly sums.
Its declared holomorphic superpotential is

\[
W=Qm d^cH_d+\mu DD^c+\lambda_{ij}S_iD d^c_j
  +c_{ijkl}S_iS_jT_kT_l/\Lambda,
\]

with CP-real coefficients. At `T1=T2=0`, the unwanted `Q Hd Dc` has charge -1 and no nonnegative S-only dressing
can neutralize it. The zero upper block is thus protected to all orders in **this holomorphic S-only EFT**.
The light m and mu have charge0 and cannot acquire S-only holomorphic corrections either. This is not a statement
about arbitrary nonholomorphic operators, soft loops or a gravity completion.

A declared rigid FI term `xi=2` allows the D-flat background `S1=1,S2=i,T1=T2=0`. The spectator F derivatives
of `(S1 T1)^2+(S2 T2)^2` vanish there. A supplied positive CP-invariant alignment potential

\[
V=\lambda_r(|S_1|^2+|S_2|^2-2)^2+\lambda_a(|S_1|^2-|S_2|^2)^2
 +\kappa[\operatorname{Re}(\bar S_1S_2)]^2
\]

has minima with relative phase ±pi/2. At unit coefficients the exact real Hessian spectrum is
`0,4,16,16`: the zero mode is the gauged common phase. Real lambda coefficients can then produce the explicit
complex B through the physical relative phase. The origin of this additional alignment potential is **not
derived from the supersymmetric part**. Constant FI is a rigid EFT assumption; no supergravity/string realization
or E6 embedding of this added field content is supplied.

### Radiative stability is the decisive next gate

An upper-right leakage `c=eta(1,0,0)^T` changes the exact witness determinant to

\[
\det\mathcal M=14-(6+i)\eta.
\]

For real small eta, `delta theta=-eta/14+O(eta²)`. A tree triangular block alone therefore proves no all-loop
strong-CP solution. Actual portals, scalar/spectator masses, soft terms, gluino phase and higher operators must
be specified before claiming an EDM-safe model. The U1 holomorphic zero is a structural starting point, not a
replacement for that computation.

## Validation and practical consequence

**14 tests PASS in17.48s**: twelve new independent checks plus the prior TOE39 parity and Pass11949 quality
replays. Controls include 25 independent positive Hermitian inverse targets, exact symbolic determinant/CP and
upper-block leakage, all mixed anomaly sums, the physical mass ordering, alignment Hessian/gauge mode,
spectator F terms, theta cutoffs and positive Kähler phase controls. Initial failures were an expanded-versus-
factored Sympy comparison and JSON integer serialization; both were corrected without changing any theorem.

The new architecture choice is explicit: either derive an actual **colored genus-two threshold with the
required divisor and phase**, or move CP transmission into a **parity-compatible vectorlike mass sector** whose
full determinant is protected. Neither route is licensed by the bare finite geometry alone. The new calculations
name the objects, coefficients and failures that the physical completion must settle.

Masses and mixing still require derived coefficients/vacuum selection; chirality, Einstein dynamics and the
cosmological constant are not solved by this packet. No new manuscript-level TOE claim is made.

Five independent next investigations:

1. Compute an actual color-charged threshold inventory and test the required `3/2 log chi10` coefficient and global marking law.
2. Construct the parity-safe vectorlike sector in an explicit E6/orbifold field inventory, including its U1/FI completion.
3. Calculate the resulting radiative theta with a declared scalar/soft spectrum and the exact upper-block leakage diagnostic.
4. Test the same vectorlike mixing on charged leptons and neutrinos, against the newly established PMNS obstruction.
5. Derive metric dynamics for the native two-polarization Maxwell construction, then test gravitational constraint closure rather than identifying a graph spectrum with gravity.
