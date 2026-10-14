# TOE77 extension — A W33 spectral nuclear-norm principle and exterior-induced flux crossover

**Date:** 14 October 2026. **Original TOE77 proof packet:** \`analysis/2026-10-14_toe77_embed_11_into_80.md\`. **This extension gives a bridge from the established W33 Ramanujan singular values to a directly computed, embedding-sensitive fermionic flux energy.**

## 1. Exact half-filled free energy identity

Let \(M(t,\phi)\) be the 40×40 complex magnetic **point-line incidence block** of the 80×80 Hermitian bipartite hopping matrix \(H(t,\phi)=\left(\begin{smallmatrix}0&-M\\-M^\dagger&0\end{smallmatrix}\right)\). Its one-particle eigenvalues are the 40 opposite singular-value pairs \(\pm\sigma_i(M)\), including zeros. Consequently, for the canonical **40 spinless fermions** at half filling,
\[
\boxed{E_{N=40}(t,\phi)=-\sum_{i=1}^{40}\sigma_i[M(t,\phi)]=-\|M(t,\phi)\|_*}.
\]
Thus static magnetic flux selection becomes a **nuclear-norm maximization** problem. This is exact for any finite bipartite free hopping graph; it does not require a nonzero fermion gap.

For the *unphased* full native W33 Levi incidence, the proven singular spectrum is \(4^1,(\sqrt6)^{24},0^{15}\), so the half-filled ground energy has the exact algebraic value
\[
\boxed{E_{W33,\phi=0}=-(4+24\sqrt6)}.
\]
The two patch phase links change only two entries of \(M\), hence its rank remains at most 27. At least 13 singular values stay zero on each sublattice: \(\dim\ker H\ge26\). **This lower bound is an exact no-go for generating a fully gapped single-particle 80-site spectrum from these two local holonomies.** The bipartite index remains zero; it is not a model of 26 Weyl neutrinos, gauge anomalies, or physical chirality.

A further rigorous perturbation bound follows from the nuclear-norm triangle inequality. For unit hopping on exactly two independently phase-twisted links,
\[
\boxed{|E_{\phi}-E_0|
\le |e^{i\phi_1}-1|+|e^{i\phi_2}-1|\le4.}
\]
The source checks the exact baseline and this bound numerically at representative flux sectors.

## 2. W33 embedding can overturn the isolated theta flux theorem

There are 12 edges among the native 11-site theta patch and 148 outside-edge links. Set the patch hopping amplitudes to one and every other W33 Levi edge to a real parameter \(t\in[0,1]\). The \(t=0\) background is the isolated \(\Theta(4,4,4)\) plus 69 isolated vertices; \(t=1\) is the *full 80-site W33 Levi graph*. Only the two selected theta chords receive variable phases \(\phi_1,\phi_2\).

TOE75 mathematically proved that the isolated theta \(t=0\) free energy is globally minimized at the two 120° phase patterns. But the TOE77 verified 80×80 spectrum shows a different result when the exterior is reinstated:
- At \(t=0\), \(E_{120}-E_{\pi,\pi}=-0.0206931704210\).
- At \(t=\frac14\), the difference is \(-0.0154690506454\).
- At \(t=\frac12\), the difference is \(-0.0063616117564\).
- At \(t=1\), the difference is **\(+0.0182225316338\)**.

Thus **the sign of the fixed 120°-versus-\(\pi,\pi\) energy preference reverses** between the isolated motif and the restored W33 Levi model. Continuous 2D multistart optimization at \(t=1\) finds a minimum numerically at \((\pi,\pi)\). The full torus global minimum is not interval-certified.

The present extension evaluates the **continuous one-parameter symmetry line**
\[
(\phi_1,\phi_2)=(\pi+\delta,\pi-\delta),\qquad
\delta\in[0,\pi/2],
\]
with 14 environment couplings \(t\), and distinguishes two different numeric events:
1. The crossing \(E_{120}(t)=E_{\pi,\pi}(t)\) for *two fixed competing backgrounds*, evaluated by root finding.
2. The sign change of the local second derivative \(\partial_\delta^2 E(\pi+\delta,\pi-\delta)\vert_{\delta=0}\), which is a local stability threshold along that line.

These are **not necessarily the same \(t\)** and should not be labeled thermodynamic phase transitions: the graph is finite and its canonical half-filled ground may have protected zero-mode degeneracies. The reported root locations are numerical, not exact or rigorously bracketed with interval arithmetic.

## 3. Why this bridges spectral graph theory to model matter

The untwisted Levi graph's exact spectrum and graph-RH property determine the baseline singular values and thus the exact 40-fermion ground energy \(-(4+24\sqrt6)\). The **magnetically twisted** full incidence block no longer shares the untwisted Ramanujan eigenvalue multiplicities; nevertheless the rank constraint and graph girth-eight walk expansion remain rigorous.

At short times the first phase-sensitive spectral trace is the eighth:
\[
\operatorname{tr} H(t,\phi)^8-\operatorname{tr}H(t,0)^8
=16\sum_{C\in\mathrm{Octagons}(W33)}
 t^{d_C}\left[\cos(w_C\!\cdot\!\phi)-1\right].
\]
The exact native 1620-octagon winding polynomial and nine direct eigenvalue-trace tests were verified in the original TOE77 CI run. That is a finite graph **Ihara/geodesic-to-matter magnetic response bridge**, not a connection to zeros of the classical Riemann zeta function.

The physically useful next question is *whether any experimentally accessible embedding-dependent current or band observable distinguishes a W33 photonic circuit from a generic three-arm interferometer*. The 11-site free 120° theorem alone cannot.

## 4. Reproducibility

- \`analysis/w33_20261014_toe77_nuclear_norm_transition.py\`
- \`tests/test_w33_20261014_toe77_nuclear_norm.py\`
- \`.github/workflows/w33_toe77_nuclear_norm.yml\`
- \`data/w33_20261014_toe77_nuclear_norm_transition.json\` (regenerated in Actions)

**Scope and open problem:** The W33 embedding-sensitive flux reversal and spectral nuclear norm are finite **free**-fermion effects. No claim has been made that coupling a full interacting Gauss-constrained electric gauge sector selects the same phases, that the 26 zero modes are physical chiral particles, or that a physical Theory of Everything has been derived.
