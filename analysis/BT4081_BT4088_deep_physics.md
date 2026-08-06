# Passes 4081–4088 — deep physics closure

## Scope and evidence boundary

This packet executes the five physics targets after Passes 4057–4072 and adds three deliberately different probes. Every promoted statement is an exact finite group, effective-Hamiltonian, Bloch-band, overlap-operator, subgroup-commutant, resolvent, information-thermodynamic, or short-time propagator result. Nothing here is a fabricated device, a measured pump, a chiral Standard Model, physical non-Abelian gauge bosons, gravity, cosmology, or a theory of everything.

Frozen certificate: `data/PART_4081_4088_DEEP_PHYSICS.json`  
Semantic SHA-256: `2f545b68de78b2cc7ab9844834ba5d9275841fce4e8aefa156c0f5388c9a5c9a`

## Pass 4081 — canonical resolution of every contact-dark irrep

The exact `PSp(4,3)=U4(2)` computation from Pass 4058 was continued from grouped dimensions to individual ordinary characters.

1. Four projective symplectic transvections generate all 25,920 group elements.
2. Conjugation gives 20 conjugacy classes.
3. An ATLAS-standard generator pair maps the internally reconstructed classes to
   `1A,2A,2B,3A,3B,3C,3D,4A,4B,5A,6A,6B,6C,6D,6E,6F,9A,9B,12A,12B`.
4. The 20-dimensional class algebra reconstructs all ordinary characters.
5. Every character value lies in `Q(sqrt(-3))`; the certificate stores it exactly as `[p,q]=(p+q i sqrt(3))/2` in ATLAS class order.

The dark module has no trivial constituent. Its individual multiplicities are

- `5a:1`, `5b:1`, `6:2`;
- the two 10-dimensional characters: `1,1`;
- `15a:1`, `15b:3`;
- the three 30-dimensional characters: `6,6,3`;
- `20:5`, `24:2`, `64:8`, `60:9`, `81:9`;
- the two 40-dimensional characters: `4,4`;
- the two 45-dimensional characters: `4,4`.

The weighted dimension is exactly 3,161. The exact central idempotent is

\[
e_\chi={\chi(1)\over25920}\sum_C \overline{\chi(C)}K_C,
\]

so the stored fingerprints specify every isotypic projector coefficient. Official suffixes are certified where an official representation trace fixes the orientation (`5a/5b` and `15a/15b`). Remaining Galois/table-automorphism pairs use an explicit plus/minus orientation instead of guessing an ATLAS suffix.

## Pass 4082 — mobile composite dark matter, conditionally and exactly

The bare repulsive contact-dark manifold has zero first-order contact motion. To ask a physically well-posed mobility question, introduce an explicit same-cell dark-pair binding energy `-Delta` and symmetry-preserving single-photon intercell tunnelling `t`.

Second-order Schrieffer–Wolff elimination gives

\[
J_{\rm pair}={2t^2\over\Delta},\qquad
E(k)=-\Delta-{4t^2\over\Delta}-{4t^2\over\Delta}\cos k.
\]

Therefore

\[
W={8t^2\over\Delta},\qquad
m^*={\Delta\over4t^2a^2}\quad(\hbar=1).
\]

Because the tunnelling is identity on the internal `H1` label, it is identity on all 19 contact-dark isotypic sectors. They do not mix and share the same clean pair dispersion.

A single pair-energy defect `nu` produces the exact bound-state offset and localization length

\[
E_{\rm b}-E_{\rm center}=\operatorname{sgn}(\nu)\sqrt{\nu^2+4J_{\rm pair}^2},
\qquad
\xi^{-1}=\operatorname{asinh}{|\nu|\over2|J_{\rm pair}|}.
\]

The result is conditional but sharp: mobile composites require an explicit binding scale. The original repulsive contact-dark degeneracy alone is neither bound nor mobile.

## Pass 4083 — a genuine two-parameter pair pump

Dimerize the effective pair hopping and cycle a staggered pair energy:

\[
J_1=J+R\cos\theta,\quad J_2=J-R\cos\theta,\quad m=2R\sin\theta,
\quad 0<R<J.
\]

The pair-center Bloch Hamiltonian is

\[
h(k,\theta)=(J_1+J_2\cos k)\sigma_x+J_2\sin k\,\sigma_y+m\sigma_z.
\]

At `k=pi`, the control loop is `(2R cos theta,0,2R sin theta)`, which encloses the unique gap closing once. The minimum band gap is exactly `4R`. A 41×41 Fukui–Hatsugai–Suzuki computation gives

\[
C_-=1.0000000000000009,
\]

hence one composite pair is pumped per clean filled-band cycle: two photons of number transport. This is the two-parameter structure absent from the one-clock static-port no-pump theorem of Pass 4061.

## Pass 4084 — exact overlap chirality on the W33 tower

For the four-dimensional external lattice, define

\[
H_W(k)=\gamma_5[D_W(k)-m_0],\qquad
D_{\rm ov}=a^{-1}[I+\gamma_5\operatorname{sign}(H_W)].
\]

The overlap operator obeys

\[
\gamma_5D+D\gamma_5=aD\gamma_5D.
\]

Independent momentum tests give a maximum residual `2.404473386885297e-15`. In the window `0<m0<2r`, the Wilson corner audit leaves one light external species and makes the other 15 corners heavy. Tensoring with the rank-81 harmonic fiber therefore gives 81 light vectorlike Dirac species.

The modified chirality operator is

\[
\widehat\gamma_5=\gamma_5(1-aD).
\]

A finite fifth-dimensional domain wall approximates the sign function exponentially; the exact overlap expression is the explicit-sign/infinite-wall limit. This closes exact lattice chirality, not chiral gauge anomaly cancellation.

## Pass 4085 — one marked incidence edge exposes exact SU(3) and SU(2) blocks

Full `PSp(4,3)` symmetry acts irreducibly on `H1`, so its commutant is scalar. Mark one incidence edge. Its stabilizer has order

\[
25920/160=162
\]

and 22 conjugacy classes. Restricting the 81-dimensional harmonic representation to this stabilizer gives commutant dimension

\[
\sum_\rho m_\rho^2=45.
\]

The key blocks are:

- a six-dimensional stabilizer irrep with multiplicity three, giving `U(3)` and an exact `SU(3)` subalgebra;
- several three-dimensional stabilizer irreps with multiplicity two, giving `U(2)` and exact `SU(2)` subalgebras.

This is minimal in number of marked incidence edges: zero marks leave only scalar `U(1)`, while one mark already produces `U(3)`. It is a control/symmetry commutant, not a claim that these are QCD or electroweak gauge bosons.

## Pass 4086 — one-port inverse spectral scattering

At any Levi vertex, vertex transitivity fixes the exact local resolvent

\[
G_{00}(s)=\frac{s^4+16s^3+78s^2+112s+4}
{s(s+4)(s+8)(s^2+8s+10)}.
\]

Equivalently,

\[
G_{00}(s)={1\over80}\left[\frac1s+\frac{24}{s+4-\sqrt6}
+\frac{30}{s+4}+\frac{24}{s+4+\sqrt6}+\frac1{s+8}\right].
\]

Thus a single ideal vertex port recovers the complete Levi Laplacian spectrum and multiplicities from poles and residues. The corresponding impulse response is

\[
h(t)={1\over80}\left[1+24e^{-(4-\sqrt6)t}+30e^{-4t}
+24e^{-(4+\sqrt6)t}+e^{-8t}\right].
\]

Adding the four shell-differential transfer functions from Pass 4044 recovers the graph-distance shell as well. This is an exact inverse problem, not a noise-conditioned laboratory reconstruction.

## Pass 4087 — Landauer cost of the dark information reservoir

Erasing a maximally mixed state on the 3,161-dimensional dark manifold requires at least

\[
W_{\min}=k_BT\ln3161=8.058643712215618\,k_BT.
\]

Resolve the state first into its 19 exact isotypic sectors. If the sector label is retained, the conditional erasure cost is

\[
5.730777383999303\,k_BT.
\]

The label contains

\[
H(\text{label})=2.3278663282163152\ \text{nats},
\]

and exactly

\[
\ln3161=H(\text{label})+\sum_jp_j\ln n_j.
\]

Keeping the representation label can lower the immediate data-erasure cost, but erasing the label record costs at least the same amount. The symmetry resolution creates no Maxwell-demon loophole.

## Pass 4088 — a defect-operational causal metric

For hopping Hamiltonian `H=J A_line`, define

\[
d(u,v)=\min\left\{n:\left.{d^n\over dt^n}
\langle u|e^{-iHt}|v\rangle\right|_{t=0}\neq0\right\}.
\]

Because `(A^n)_{uv}=0` below shortest-path length, this operational response order equals line-graph distance exactly. From any link, the shells are

\[
1,6,18,54,81
\]

at distances `0,1,2,3,4`. The first nonzero geodesic multiplicities are

\[
1,1,1,2.
\]

The leading amplitudes are therefore

\[
-iJt,\quad {(-iJt)^2\over2!},\quad {(-iJt)^3\over3!},
\quad 2{(-iJt)^4\over4!}.
\]

Short-time response reconstructs both distance and shortest-path degeneracy. Removing couplers changes this operational metric. This is finite graph causality, not emergent gravitational spacetime.

## Primary foundations used

- ATLAS of Finite Group Representations, `U4(2)=PSp(4,3)` class and representation data.
- Bravyi, DiVincenzo, and Loss, rigorous Schrieffer–Wolff transformation.
- Thouless, *Quantization of particle transport*; and the TKNN Chern-number formulation.
- Neuberger, overlap Dirac operator and exact lattice chiral symmetry.
- Landauer erasure principle and modern information-thermodynamic formulations.
