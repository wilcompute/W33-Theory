# Passes 4089–4096 — implementation closure and three outside-box probes

## Evidence boundary

This packet executes the five implementation targets after Passes 4073–4080 while avoiding the completed Passes 4081–4088 overlap-chirality and Thouless-pump work. The promoted results are exact finite graph constructions, norm bounds, representation-ring identities, perturbative pulse identities, a deterministic full 160-mode simulation, and exact linear network calculations. No hardware, Standard Model, nonlinear pattern experiment, gravity, or TOE is claimed.

Certificate: `data/PART_4089_4096_IMPLEMENTATION_OUTSIDE_BOX.json`  
Semantic SHA-256: `598f80f12de4571824218228000fbfc874f339b59717009fb567e4268a5797dc`

## Pass 4089 — all 160 physical router assignments

The symplectic points and totally isotropic lines of `W(3,3)` are enumerated canonically over `F3`. Deterministic bipartite matching produces four perfect matchings of the 80-vertex Levi graph. Each matching contains forty disjoint point–line swaps, and the corrected frozen route table is

`data/w33_pass4089_four_router_layout.json`.

Its semantic hash is

`32e46ee39dde19ae936eb7334e79db5f083a75db9a9c4dafa6902f1190152556`.

With a balanced four-path selector and the four permutation routers,

\[
(\langle00|B^\dagger\otimes I)U_{\rm sel}(B|00\rangle\otimes I)=A_L/4.
\]

If router `j` has complex transmission `t_j exp(i theta_j)`,

\[
\eta_{\rm signal}\le {1\over4}\sum_j|t_j e^{i\theta_j}-1|,
\qquad
\|\delta U_{\rm QSP}\|\le5\eta_{\rm signal}+6\delta_\phi.
\]

A per-router complex error of `0.001` and phase-gate error `0.0005 rad` gives the conservative total operator bound `0.008`. Equal loss on all routes changes postselection success rather than the normalized block.

## Pass 4090 — optimal finite phase reference

The binomial reference of Pass 4074 is not optimal. For a reference supported on weights `0,...,K`, maximize the nearest-neighbour coherence

\[
S=\sum_{n=1}^{K}c_{n-1}c_n.
\]

The Rayleigh quotient of the path adjacency matrix gives the exact optimum

\[
c_n=\sqrt{2\over K+2}\sin{(n+1)\pi\over K+2},
\qquad
S_{\max}=\cos{\pi\over K+2}.
\]

For the cyclic processor,

\[
z_K=e^{i\phi}\cos{\pi\over K+2}
+{2\sin^2(\pi/(K+2))\over K+2}e^{-iK\phi}.
\]

Therefore

\[
\|\mathcal E_K-\mathcal U_\phi\|_\diamond
\le1-\cos{\pi\over K+2}
+{2\sin^2(\pi/(K+2))\over K+2}
={\pi^2\over2K^2}+O(K^{-3}).
\]

This improves the binomial `O(K^-1)` law to `O(K^-2)`. Actual single-use errors are `1.0963e-3` at `K=64` and `7.3647e-5` at `K=256`. Repeated-use degradation and preparation cost remain open.

## Pass 4091 — exterior algebra produces an anomaly-free generation pattern

The dimension-57 multiplicity extension supplies fundamental multiplicity spaces `C^3` and `C^2`. The determinant-one central charges are

\[
q_3=-{1\over3},\qquad q_2={1\over2}.
\]

Their tensor, conjugate, and exterior representations contain

\[
Q=(3,2)_{1/6},\quad
u^c=(\bar3,1)_{-2/3},\quad
d^c=(\bar3,1)_{1/3},\quad
L=(1,2)_{-1/2},\quad
e^c=(1,1)_1.
\]

Here `u^c=Lambda^2 3` and `e^c=Lambda^2 2`. Exact rational traces give

\[
SU(3)^3=SU(3)^2U(1)=SU(2)^2U(1)=\mathrm{grav}^2U(1)=U(1)^3=0,
\]

and the number of left-handed `SU(2)` doublets, including colour, is four, so the mod-two Witten obstruction vanishes.

This is a representation-ring identity, not a derivation of particles. A one-particle carrier explicitly containing multiplicities `6,3,2` has minimum dimension

\[
6\cdot1+3\cdot15+2\cdot24=99.
\]

Masses, Yukawas, generations, dynamics, and observed couplings remain unbuilt.

## Pass 4092 — materialized four-notch waveform

Choose

\[
h(t)={218790\over T}x^8(1-x)^8,\qquad x=t/T,
\]

which has unit area and vanishing endpoint derivatives through order seven. Define

\[
f={h^{(8)}+124h^{(6)}+4644h^{(4)}+53056h''+102400h\over102400}.
\]

For `T=16/J`, the unit-area waveform has peak `0.1831411095 J` and L2 norm `0.3633439828 sqrt(J)`. It has exact spectral zeros at all four bright gaps.

A full 160-mode line-graph simulation starts from a projected local `H1` state and applies one local diagonal control. For amplitudes `eta=0.2,0.1,0.05,0.025`, square-pulse leakage scales with fitted exponent `2.0191183`, while the notched pulse scales with exponent `4.0191314`. At `eta=0.1`, leakage falls from `7.0078e-7` to `5.4699e-11`.

## Pass 4093 — tolerance-certified mechanical build sheet

The scalar mechanical dual uses 80 equal masses and 160 equal springs, four springs per node. Pin one node to remove the uniform mechanism. The target nonzero squared-frequency bands are

\[
(4-\sqrt6)^{24},\quad4^{30},\quad(4+\sqrt6)^{24},\quad8^1.
\]

For independent spring errors satisfying `|delta k_e|<=epsilon k`,

\[
\|\delta M\|\le8\epsilon k/m.
\]

A sufficient worst-case condition to keep adjacent bands separated by at least half their ideal gap is

\[
\epsilon<{4-\sqrt6\over16}=0.0969068911.
\]

The self-stress projector is measured by quasistatic bond-space relaxation:

\[
P_{\rm stress}=I-D^T(DD^T)^+D.
\]

## Pass 4094 — outside box: the self-stress space is a sparse-error code

The real cycle code

\[
\mathcal C=\ker D\subset\mathbb R^{160}
\]

has dimension 81. Every nonzero circulation contains a cycle, and the Levi graph has girth eight. Conversely every apartment supports an alternating circulation. Hence

\[
\boxed{[n,k,d]=[160,81,8]}.
\]

Every bond-tension error on at most seven springs is detectable by the nodal-force syndrome `De`. Any error on at most three springs is uniquely correctable in the noiseless sparse model, because two such errors cannot differ by a nonzero codeword of support at most six.

## Pass 4095 — outside box: exact Turing mode selectors

A two-species reaction–diffusion system sees only Laplacian values `0,10,16`, with multiplicities `1,24,15`.

For

\[
J=\begin{pmatrix}2&5\\-21&-20\end{pmatrix},\qquad(D_u,D_v)=(0.1,10),
\]

\[
\det(J-\lambda D)=(\lambda-5)(\lambda-13).
\]

The homogeneous mode and `lambda=16` sector are stable, while `lambda=10` has growth rate `0.125917182`; the unstable pattern space is exactly 24-dimensional.

For

\[
J=\begin{pmatrix}3.2&12\\-21&-10\end{pmatrix},
\]

\[
\det(J-\lambda D)=(\lambda-11)(\lambda-20).
\]

Now only the `lambda=16` sector is unstable, with growth rate `0.118681204`; the pattern space is exactly 15-dimensional.

## Pass 4096 — outside box: two-valued electrical geometry

Put a unit resistor on every W33 edge. The exact Laplacian pseudoinverse is

\[
L^+={7\over80}I+{1\over160}A-{13\over3200}J.
\]

Therefore

\[
R_{\rm adjacent}={13\over80},\qquad
R_{\rm nonadjacent}={7\over40},\qquad
{R_{\rm nonadjacent}\over R_{\rm adjacent}}={14\over13}.
\]

The 240 adjacent and 540 nonadjacent pairs give Kirchhoff index

\[
240{13\over80}+540{7\over40}={267\over2}.
\]

W33 is thus an exact two-distance resistance geometry. This is DC circuit geometry, not spacetime.
