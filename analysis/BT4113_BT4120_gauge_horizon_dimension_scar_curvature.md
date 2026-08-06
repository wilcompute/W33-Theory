# BT4113–BT4120 — Gauge-string pumping, an active horizon, dynamic dimension, local scar compilation, thermodynamic curvature, and three outside-box probes

## Evidence boundary

This packet promotes exact finite calculations only. It does **not** claim continuum QCD, observed Hawking radiation, a derivation of physical four-dimensional spacetime, a static local Hamiltonian that directly cycles the three bare CDW product states, a finite-size thermodynamic phase transition, exchanged non-Abelian anyons, gravitational or cosmological redshift, or a theory of everything.

The deterministic source is `analysis/w33_pass4113_4120_gauge_horizon_dimension_scar_curvature.py`; the frozen certificate is `data/PART_4113_4120_GAUGE_HORIZON_DIMENSION_SCAR_CURVATURE.json` with semantic SHA-256 `28391f98e03ec20cc688cc8692579ff0cf352930d085b2d33d979de7ef9a3e2a`.

## Pass 4113 — Gauge-string fractional pump

Tensor the three one-third-filled CDW branches from Pass 4097 with the unique local `SU(3)` Gauss singlet from the finite quantum-link truncation:

\[
|\mathcal M\rangle=\frac13\sum_{a,b=1}^{3}|\bar a\rangle\,|a,\bar b\rangle\,|b\rangle.
\]

The explicit eight Gell-Mann generators were used at both endpoints. The simultaneous left/right Gauss Casimir on the 81-dimensional endpoint–link–endpoint space has a one-dimensional kernel, and the displayed state has zero generator residual to machine precision.

The fractional pump translates matter occupation and the support of its attached fundamental–antifundamental flux string together. It therefore transports a **gauge-invariant meson/composite**, not an isolated color charge. Per branch cycle the polarization changes by one third of a composite pair; after three cycles one complete singlet pair and its flux string cross a cut.

The exact color result is:

- net transported `SU(3)` color charge: zero;
- zero-background-flux three-cycle Wilson holonomy: identity;
- normalized zero-flux Wilson loop: one;
- with a prescribed background center flux `k`, the holonomy is `exp(2 pi i k/3) I`.

Thus the minimal unique-singlet sector does **not** produce non-Abelian Wilson mixing. Such mixing requires a degenerate color multiplet, unpaired endpoints, or a nontrivial plaquette background. This is a useful negative theorem, not a failure: gauge invariance tightly determines what the fractional pump can carry.

The treatment of local singlet sectors follows the standard lattice Gauss-law viewpoint; see, for example, Anishetty and Sreeraj, *Addition of SU(3) generators and its Singlet Hilbert space*, arXiv:1903.07956.

## Pass 4114 — Active Floquet–Bogoliubov horizon

Pass 4099 proved that a static reciprocal hopping gradient has no one-way horizon and no particle-producing Bogoliubov block. The minimal extension here deliberately adds both missing ingredients:

1. a directed Floquet walk with quasienergy
   \[
   \Omega(k)=\frac{2}{\tau}\arcsin\!\left[v\sin\left(\frac{ka}{2}\right)\right],
   \]
2. a local two-mode Bogoliubov squeezer coupling the outside Hawking mode and the inside partner.

The group velocity is

\[
v_g(k)=\frac{a}{\tau}\frac{v\cos(ka/2)}{\sqrt{1-v^2\sin^2(ka/2)}}.
\]

At low momentum,

\[
\Omega(k)=\frac{va}{\tau}k+\frac{v^3-v}{24}\frac{a^3}{\tau}k^3+O(k^5a^5),
\]

which explicitly exposes the leading lattice ultraviolet correction.

A horizon occurs where the directed background flow satisfies `u(x_H)=c_eff`, with `c_eff=va/tau`. Define

\[
\kappa=|\partial_x(u-c_{\rm eff})|_{x_H},\qquad T_H=\frac{\kappa}{2\pi}.
\]

The Hawking/partner core is the exact two-mode squeeze transformation

\[
\tanh r=e^{-\pi\omega/\kappa},\qquad
n_\omega=\sinh^2r=\frac{1}{e^{2\pi\omega/\kappa}-1}.
\]

A greybody beam splitter of transmission `Gamma` gives

\[
n_{\rm out}=\Gamma n_\omega.
\]

The code constructs the full six-by-six Nambu scattering matrix: a two-mode squeezer on Hawking/partner channels followed by a passive beam splitter into an environment channel. It satisfies the bosonic paraunitary condition with residual

\[
2.282836126979115\times10^{-16}.
\]

For the frozen demonstration `kappa=0.4`, `omega=0.3`, `Gamma=0.7`:

- `T_H = 0.06366197723675814`;
- `r = 0.09506557725167403`;
- thermal partner occupation `0.009064722057396675`;
- transmitted outside occupation `0.006345305440177674`;
- reflected environment occupation `0.0027194166172190034`;
- logarithmic negativity after greybody loss `0.15624263179344325`.

This is an exactly checked active horizon **cell**. A complete spatial device still needs a resolved flow profile, mode matching over many sites, state preparation, detector response, and loss/error analysis. The design is consistent with the known need for directed Floquet or quench dynamics and Bogoliubov mode conversion in lattice Hawking constructions; see Maertens, Bultinck, and Van Acoleyen, arXiv:2204.06583, and Coutant and Weinfurtner, arXiv:1707.09664.

## Pass 4115 — Dynamically selected four-dimensional scaling

The previous hierarchy obtained spectral dimension four by supplying `b=80^(1/4)`. Here the scale is instead selected by an explicit information-balance dynamics grounded in two exact finite quantities:

- branching number `B=80`;
- Levi edge connectivity `chi=4`, interpreted as four independent transport channels.

Let `s=ln b` and define the mismatch potential

\[
\Phi(s)=\frac12[\ln80-4s]^2.
\]

Choose the scale flow

\[
\frac{ds}{d\tau}=\gamma[\ln80-4s].
\]

Then

\[
\frac{d\Phi}{d\tau}=-4\gamma[\ln80-4s]^2\le0,
\]

so the fixed point is globally Lyapunov-stable:

\[
s_*=\frac{\ln80}{4},\qquad b_*=80^{1/4}=2.9906975624424406.
\]

Linear perturbations decay with exponent `-4 gamma`. The discrete update

\[
s_{n+1}=s_n+\eta(\ln80-4s_n)
\]

is stable for `0<eta<1/2`; at `eta=1/8`, deviations contract by exactly one half per iteration.

The resulting spectral dimension is no longer inserted independently:

\[
d_s=\frac{\ln80}{\ln b_*}=4.
\]

The exact statement is conditional on the channel-balance potential. It is a concrete dynamical selection principle tied to the finite graph’s edge connectivity, not proof that physical spacetime must obey this RG law.

## Pass 4116 — Local scar compiler and static no-go

The three CDW branches are

`100100100`, `010010010`, and `001001001`.

Every pair differs on six sites. Consequently, any operator supported on fewer than six sites has zero direct matrix element between distinct branches. Therefore, if the bare three-dimensional span is required to be exactly invariant, a strictly finite-range static Hamiltonian cannot generate the desired nontrivial branch cycle. This prevents a misleading claim that a nearest-neighbor static term directly realizes the earlier global trimer.

The exact local resolution is Floquet compilation. Apply the eight nearest-neighbor swaps `(0,1),(1,2),...,(7,8)` sequentially. Each swap is generated for time `tau` by

\[
H_i=\frac{\pi}{2\tau}(I-\mathrm{SWAP}_{i,i+1}).
\]

The resulting shift maps

- `100100100 -> 001001001`,
- `001001001 -> 010010010`,
- `010010010 -> 100100100`.

Thus one shift takes `T_shift=8 tau`, and

\[
U_{\rm shift}^3=I
\]

on the CDW tower at

\[
T_{\rm rev}=24\tau.
\]

The Floquet quasienergies are `0` and `+/- 2 pi/(3 T_shift)`. Every pulse is two-local and nearest-neighbor, with instantaneous norm `pi/tau`.

A telescoping robustness bound is immediate: if each pulse has operator-norm error at most `epsilon`, one compiled shift differs from ideal by at most `8 epsilon`, and the three-cycle revival differs by at most `24 epsilon`.

This separates two statements that should not be conflated: a static local bare-subspace Hamiltonian is ruled out, while an exact time-dependent local circuit exists.

## Pass 4117 — Two-parameter thermodynamic curvature

Introduce a sector-size splitting field by assigning each dark isotypic block of dimension `n_j` the charge

\[
q_j=\ln n_j.
\]

The five bright groups retain their exact contact energies and carry `q=0`. The partition function is

\[
Z(\beta,h)=\sum_{j\in\mathrm{dark}}n_j e^{-h\ln n_j}
+\sum_{a\in\mathrm{bright}}g_a e^{-\beta E_a}.
\]

With sufficient statistics `T=(-E,-q)`, the Fisher metric is

\[
g_{ab}=\operatorname{Cov}(T_a,T_b).
\]

For a two-dimensional Hessian metric, the scalar curvature is evaluated from second and third derivatives of `psi=ln Z`:

\[
R=-\frac{1}{2\det(g)^2}
\det\begin{pmatrix}
\psi_{11}&\psi_{12}&\psi_{22}\\
\psi_{111}&\psi_{112}&\psi_{122}\\
\psi_{112}&\psi_{122}&\psi_{222}
\end{pmatrix}.
\]

Frozen values along `h=0` are:

- `R(0,0) = -0.6460278596846867`, `det g = 0.002770098686766183`;
- curvature zero at `beta U = 14.579166757087052`;
- `R(20,0) = 0.20080335722980544`, `det g = 1.901209288045885e-05`.

The curvature changes sign, giving a sharp finite information-geometric crossover. However, `Z` is a finite sum of positive exponentials and is analytic for all finite `beta,h`; while the metric is nondegenerate there is no true thermodynamic singularity. This explicitly avoids equating every curvature feature with a phase transition. Finite-system information geometry and the subtle relation between curvature and condensation are discussed, for example, in Pessoa, arXiv:2302.03182.

## Pass 4118 — Outside-box: qutrit projective-holonomy memory

Use the three CDW branches as a logical qutrit. One fractional-pump cycle supplies

\[
X|q\rangle=|q+1\bmod3\rangle,
\]

while a branch-dependent twist supplies

\[
Z|q\rangle=\omega^q|q\rangle,
\qquad \omega=e^{2\pi i/3}.
\]

The exact relation is

\[
ZX=\omega XZ,
\]

with numerical residual `2.482534153247273e-16`. Hence

\[
ZXZ^\dagger X^\dagger=\omega I,
\]

and the nine displacement operators `X^a Z^b` furnish the qutrit Heisenberg–Weyl logical algebra up to center phases.

This is noncommuting projective holonomy on a degenerate ground bundle. It is **not** evidence that spatially exchanged non-Abelian anyons have been constructed.

## Pass 4119 — Outside-box: exact transport quantum speed limit

The qutrit branch shift has eigenvalues `1,omega,omega^2`, so its principal logarithm has eigenphases

\[
0,\quad +\frac{2\pi}{3},\quad -\frac{2\pi}{3}.
\]

Therefore

\[
\|\log X\|=\frac{2\pi}{3}.
\]

For any time-independent generator with centered operator norm `||H-cI|| <= Lambda`, implementing the full branch shift requires

\[
T\ge\frac{2\pi}{3\Lambda}.
\]

For transfer between two orthogonal branch states, the Mandelstam–Tamm form separately gives

\[
T\ge\frac{\pi}{2\Delta H}.
\]

The local SWAP compiler takes `8 tau` per shift and `24 tau` per three-cycle revival, intentionally exceeding the unconstrained norm-only geodesic bound because locality and translation structure impose additional resources.

This is a finite control-theory speed limit, not a relativistic universal velocity.

## Pass 4120 — Outside-box: spectral redshift

At the dynamically selected hierarchy scale

\[
b_*=80^{1/4},
\]

successive spectral levels obey

\[
\lambda_{n+m}=\lambda_n b_*^{-2m},
\qquad
\omega_{n+m}=\omega_n b_*^{-m}.
\]

The corresponding discrete spectral redshift is

\[
1+z_m=b_*^m=80^{m/4}.
\]

For `m=1,2,3,4`:

\[
z_m=(1.9906975624424406,\;7.944271909999156,\;25.749612199056866,\;79).
\]

Diffusive relaxation times dilate as

\[
\frac{t_{n+m}}{t_n}=b_*^{2m}=80^{m/2},
\]

while `omega_n ell_n` remains invariant if length scales as `ell_n proportional to b_*^n`.

This is a precise redshift analogue of a discrete spectral hierarchy. It is not cosmological expansion, gravitational redshift, or a measured spacetime geometry.

## Verification summary

- all eight pass checks hold;
- focused regression: nine tests pass locally;
- semantic certificate SHA-256: `28391f98e03ec20cc688cc8692579ff0cf352930d085b2d33d979de7ef9a3e2a`;
- `docs/index.html` was not edited;
- remote GitHub Actions and manuscript compilation remain separate evidence and must not be inferred from local verification.
