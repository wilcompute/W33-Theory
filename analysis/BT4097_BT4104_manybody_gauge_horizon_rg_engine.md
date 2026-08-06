# Passes 4097–4104 — many-body pumping, quantum links, horizon falsifier, spectral RG, and three outside-box probes

## Status

`PASS_EXACT_EIGHT_FRONT_WITH_STRONG_COUPLING_TRUNCATION_HARDWARE_AND_EMERGENCE_BOUNDARIES`

Semantic certificate: `4687bd582e2d83c5bc0c168f905139edbab429bee37715398e4a7952cc3cf1ef`.

The deterministic source is `analysis/w33_pass4097_4104_manybody_gauge_horizon_rg_engine.py`; the frozen output is `data/PART_4097_4104_MANYBODY_GAUGE_HORIZON_RG_ENGINE.json`.

## Pass 4097 — exact fractional many-composite pump

Take a nine-cell ring with three hard-core composite pairs and

\[
H_0=U\sum_{i=0}^{8}(n_i+n_{i+1}+n_{i+2}-1)^2 .
\]

In the fixed-filling Hilbert space of dimension \(\binom93=84\), direct enumeration gives

\[
E/U=0^3+2^{18}+4^{36}+6^{18}+10^9.
\]

The three exact ground patterns are

\[
100100100,\qquad010010010,\qquad001001001,
\]

with Resta polarizations \(0,1/3,2/3\).  The many-body gap is exactly \(2U\).

Let \(T_3\) cyclically permute the three branches.  With boundary twist \(\phi\), choose the ground-space pump holonomy

\[
W(\phi)=e^{i\phi/3}T_3.
\]

Then

\[
\det W(\phi)=e^{i\phi},\qquad
C=\frac{1}{2\pi i}\int_0^{2\pi}d\phi\,\partial_\phi\log\det W=1.
\]

Each branch advances by polarization \(1/3\) per cycle and returns after three cycles.  Thus one cycle pumps \(1/3\) of a composite-pair charge, while three cycles pump one complete pair, or two photons.  This is the standard degenerate-ground-bundle mechanism underlying fractional Thouless pumping, here realized by an exact finite strong-coupling parent rather than inferred from a plateau.

**Boundary.** Finite hopping, disorder, finite-time adiabaticity, branch preparation, and loss are not certified.

## Pass 4098 — finite dynamical \(SU(3)\) quantum-link sector

Use a link Hilbert space

\[
\mathcal H_\ell=\mathbf 1\oplus(\mathbf3\otimes\bar{\mathbf3}),
\qquad \dim\mathcal H_\ell=10.
\]

The flux sector has left fundamental and right antifundamental color indices.  For one link terminated by antifundamental matter on the left and fundamental matter on the right,

\[
G_L^a=T^a_{\bar3,\mathrm{matter}}+T^a_{3,\mathrm{link}},\qquad
G_R^a=T^a_{\bar3,\mathrm{link}}+T^a_{3,\mathrm{matter}}.
\]

The exact 81-dimensional endpoint/link Hilbert space has a one-dimensional simultaneous Gauss-law kernel.  Its normalized state is

\[
|\mathrm{string}\rangle=\frac13\sum_{a,b=1}^3
|\bar a\rangle\,|a,\bar b\rangle\,|b\rangle.
\]

Since \(C_2(\mathbf3)=4/3\),

\[
H_E=\frac{g^2}{2}\sum_\ell L_\ell^2
\quad\Longrightarrow\quad
E_{\rm string}(R)=\frac{2g^2R}{3},
\]

so the exact truncation has string tension

\[
\sigma=\frac{2g^2}{3a}.
\]

The smallest gauge-invariant plaquette sector consists of the vacuum and one oriented color-contracted loop.  With magnetic amplitude \(J\),

\[
H_\square=
\begin{pmatrix}
0&-J\\
-J&8g^2/3
\end{pmatrix},
\]

and

\[
E_\pm=\frac{4g^2}{3}\pm\sqrt{\frac{16g^4}{9}+J^2},
\qquad
\Delta_\square=2\sqrt{\frac{16g^4}{9}+J^2}.
\]

This is a finite quantum-link realization of exact non-Abelian Gauss constraints, confinement energy, and plaquette dynamics.

**Boundary.** It is not a continuum Yang–Mills limit, QCD spectrum, or fabricated gauge simulator.

## Pass 4099 — decisive passive-horizon and Hawking no-go

Consider a reciprocal number-conserving chain

\[
H=\sum_n J_n a_n^\dagger a_{n+1}+\mathrm{h.c.}
\]

with real \(J_n\).  On an open chain, recursive local \(\pi\)-phase choices transform every nonzero \(J_n\) to \(|J_n|\).  A sign-changing hopping profile is therefore gauge-equivalent to a positive profile; if a hopping reaches zero, it creates a cut rather than a horizon.

Because the single-particle matrix is real symmetric,

\[
U(t)=e^{-iht}=U(t)^T,
\]

so propagation is reciprocal.  In Nambu space,

\[
S(t)=\operatorname{diag}(U,U^*),
\]

and the Bogoliubov creation block obeys

\[
\boxed{\beta=0},\qquad
\langle N\rangle_{\rm vacuum}=\operatorname{tr}(\beta\beta^\dagger)=0.
\]

Hence a static reciprocal \(J(x)\) gradient alone creates neither a one-way causal horizon nor spontaneous Hawking particles.  Lattice Hawking constructions require an additional directed-flow/Floquet or quench structure, and particle creation requires positive/negative-norm or particle/hole mixing.

**Boundary.** This is a no-go for the passive proposal only, not for flowing condensates, Floquet horizons, filled fermion seas, or Bogoliubov systems.

## Pass 4100 — discrete-scale spectral renormalization fixed cycle

Use the exact nonzero Levi spectrum

\[
(4-\sqrt6)^{24}+4^{30}+(4+\sqrt6)^{24}+8^1.
\]

Define an \(n\)-level hierarchy with one zero mode and, for \(j=0,\ldots,n-1\), eigenvalues

\[
\lambda_\alpha b^{-2(n-1-j)}
\]

with multiplicities \(m_\alpha80^j\).  Its dimension is exactly

\[
1+79\sum_{j=0}^{n-1}80^j=80^n.
\]

The normalized heat return has a discrete log-time period \(2\log b\).  Its log-period-average spectral dimension is

\[
\bar d_s=\frac{\log80}{\log b}.
\]

Choosing

\[
b=80^{1/4}
\]

gives

\[
\boxed{\bar d_s=4}.
\]

For \(n=14\), the central scaling window gives

\[
\langle d_s\rangle=3.99987084247,
\]

with persistent log-periodic excursions from \(2.97765560\) to \(5.14402331\).  The result is therefore a nontrivial discrete-scale fixed cycle, not a smooth continuum fixed point.

**Boundary.** Four is obtained only after the rescaling \(b=80^{1/4}\) is supplied.  The cell does not independently choose this scaling or establish physical spacetime.

## Pass 4101 — closed topological information–heat engine

The 19 nonzero dark isotypic dimensions are

\[
5,5,12,10,10,15,45,180,100,180,512,180,180,540,160,160,90,729,48,
\]

summing to 3161.  With \(p_j=n_j/3161\),

\[
H(J)=2.327866328216315,
\]

\[
\sum_jp_j\log n_j=5.730777383999302,
\]

and exactly

\[
H(J)+\sum_jp_j\log n_j=\log3161=8.058643712215618.
\]

A reversible cycle may:

1. isothermally expand a pure reference into the uniform dark reservoir and extract \(k_BT\log3161\);
2. measure and store the irrep label reversibly;
3. use the label to control a \(C_j=\pm1\) topological pair pump, routing one pair or two photons;
4. erase the conditional microstate at cost \(k_BT\sum p_j\log n_j\);
5. erase the label at cost \(k_BTH(J)\).

The closed-cycle work is therefore

\[
\boxed{W_{\rm net}^{\max}=0}
\]

in the reversible limit.  Topology can protect transport and routing, but not evade Landauer accounting or the second law.

## Pass 4102 — bonkers: exact three-state many-body scar clock

Project the three CDW ground states into an invariant subspace and take

\[
H_{\rm scar}=\Omega(T_3+T_3^\dagger).
\]

Its spectrum is

\[
-\Omega,-\Omega,2\Omega.
\]

An initial CDW branch has exact return probability

\[
P_A(t)=\frac{5+4\cos(3\Omega t)}9,
\]

with first perfect revival

\[
T_{\rm rev}=\frac{2\pi}{3\Omega}.
\]

At \(L=9,N=3\), the invariant scar subspace has dimension 3 inside a fixed-filling Hilbert space of dimension 84, a fraction \(1/28\).  The Fourier scar eigenstates are qutrit cats with entropy \(\log3\) across cuts distinguishing the patterns.

**Boundary.** This is an exact projector-embedded scar construction with a global translation term, not a generic local scar phase.

## Pass 4103 — bonkers: fractional-pump qutrit-cat metrology

For \(L=3N_p\), the three CDW branches have pair-position eigenvalues

\[
X_0,\quad X_0+N_p,\quad X_0+2N_p.
\]

For

\[
|\mathrm{cat}\rangle=\frac{|A\rangle+|B\rangle+|C\rangle}{\sqrt3},
\]

the pure-state quantum Fisher information for a pair-position phase is

\[
\boxed{F_Q=4\operatorname{Var}X=\frac{8N_p^2}{3}}.
\]

Because each composite contains two photons, the corresponding photon-gradient generator gives

\[
\boxed{F_Q^{(\gamma)}=\frac{32N_p^2}{3}}.
\]

For \(N_p=3\), these are 24 and 96.  An inverse qutrit Fourier transform followed by branch measurement is the natural readout.

**Boundary.** Preparation, dephasing, loss, and estimator saturation remain open.

## Pass 4104 — bonkers: thermodynamic geometry of the dark reservoir

For the exact projected contact spectrum, the canonical Fisher metric is

\[
g_{\beta\beta}=\operatorname{Var}_\beta(E)=\frac{C}{k_B\beta^2}.
\]

The canonical thermal path from \(\beta=0\) to \(\infty\) has length

\[
\mathcal L_{\rm can}=0.4530018812338062.
\]

The infinite-temperature distribution is uniform on 3321 states, while the zero-temperature endpoint is uniform on the 3161-dimensional dark manifold.  Their Bhattacharyya coefficient is

\[
B=\sqrt{\frac{3161}{3321}}=0.9756135200168286,
\]

so the Fisher–Rao geodesic distance is

\[
d_{\rm FR}=2\arccos B=0.4425945899021065.
\]

The canonical path is only

\[
2.351427597\% 
\]

longer than the geodesic.  The huge dark manifold makes the thermal endpoints information-geometrically close despite the temperature range being infinite.

**Boundary.** This is thermodynamic information geometry, not a spacetime metric.

## Evidence boundary

Every promoted statement is an exact finite strong-coupling, group-generator, Gauss-law, passive-Bogoliubov, hierarchical-spectrum, information-themodynamic, invariant-subspace, Fisher-information, or canonical-geometry result.  No fractional-pump experiment, continuum QCD, Hawking observation, physical four-dimensional spacetime, positive-work engine, generic scar phase, fabricated sensor, gravity, cosmology, or theory of everything is claimed.

## Primary external context

- Zeng, Zhu, and Sheng, *Fractional charge pumping of interacting bosons in one-dimensional superlattices*, arXiv:1607.06151.
- Hayward et al., *Topological charge pumping in the interacting bosonic Rice–Mele model*, Phys. Rev. B **98**, 245148 (2018).
- Baer, Brower, Schlittgen, and Wiese, *Quantum Link Models with Many Rishon Flavors and with Many Colors*, arXiv:hep-lat/0110148.
- Maertens, Bultinck, and Van Acoleyen, *Hawking radiation on the lattice from Floquet and local Hamiltonian quench dynamics*, arXiv:2204.06583.
- Schmidt, Caccioli, and Aste, *Spectral Coarse-Graining and Rescaling for Preserving Structural and Dynamical Properties in Graphs*, arXiv:2411.11991.
- Turner et al., *Quantum many-body scars*, arXiv:1711.03528.
