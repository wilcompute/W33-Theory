# BT1031 — The spectral propinquity closes R3's spectral-action convergence

**Status: novel rigorous route to R3, absent from the corpus. The hard
"does the action converge" step is reduced to an existing theorem.**
Script `analysis/bt1031_spectral_propinquity_route.py`, data
`data/bt1031_spectral_propinquity_route.json`.

## The idea (internet-sourced, repo-absent)

The corpus's R3 program (BT983–BT1029) proves the curved-4D continuum lift via
*classical* tools — Cheeger–Müller–Schrader (curvature) and FEEC/Dodziuk–Patodi
(eigenvalues) on a shape-regular edgewise tower. There is a **modern NCG
convergence framework** built for exactly "finite spectral triples → continuum
spectral triple," which the corpus does not use (a single literature mention of
van Suijlekom; zero of *propinquity*):

> **Latrémolière's spectral propinquity** is a metric, up to unitary
> equivalence, on metric spectral triples. If a sequence converges for the
> propinquity then (i) the **Dirac spectra converge**, and crucially
> (ii) **action functionals — the spectral action `Tr f(D²/Λ²)` — are
> continuous** (Math. Ann. 2023, arXiv:2112.11000).

## The R3 reduction

The Einstein–Hilbert + matter action *is* the spectral action, which is a
continuous functional for the spectral propinquity. Therefore:

> **R3 reduces to:** does the sequence of spectral triples
> `W(3,3) × (edgewise K3 refinement tower)` converge to the continuum triple
> `W(3,3) × K3` in the spectral propinquity?
>
> If yes, the spectral action — hence Einstein–Hilbert + matter — converges
> **by Latrémolière's theorem**. The hard "does the action converge" step is
> no longer an open analysis problem; it is a citation. Only the propinquity
> convergence of the tower remains.

This is strictly stronger than the classical route: FEEC gives convergence of
*each fixed eigenvalue*; the propinquity gives convergence of the *whole
functional calculus* (hence the spectral action, a sum over the full spectrum
with a cutoff), which is exactly what the spectral action needs and what
per-eigenvalue convergence did not supply.

## Concrete W(3,3) verification (the two prerequisites)

- **T1 — W(3,3) is a metric spectral triple.** The Connes/graph metric on the
  40 substrate points has distances `{0,1,2}` (collinear pairs = 1, matter
  shell = 2 — the generalized-quadrangle "resolution-0" emergent metric),
  satisfying symmetry, identity, and the triangle inequality. Off-diagonal
  distribution `{1: 480, 2: 1080}` (= 40×12 collinear, 40×27 matter).
- **T2 — the spectral action is well-defined.** From the exact Dirac square
  spectrum `{0¹²², 4²⁴⁰, 10⁴⁸, 16³⁰}`, `S(Λ)=Tr f(D²/Λ²)` is computable for any
  cutoff; its Λ→∞ moments are the substrate invariants
  `{M₀=dim H_F=440, M₁=Tr D_F²=1920, M₂=Tr D_F⁴=16320}` (the cosmological/EH
  and Yang–Mills/Higgs coefficients).

So W(3,3) supplies both ingredients the propinquity framework needs.

## How this fits the existing program

- The FEEC/Dodziuk–Patodi eigenvalue convergence (BT994/BT984) and the CMS
  Regge curvature convergence (BT986) are **necessary** for propinquity
  convergence — they are the spectral and metric data converging.
- The propinquity packages them into convergence in the *space of spectral
  triples* and adds the decisive output: continuity of the spectral action.
- Dual finite-approximation picture: **spatial** refinement (edgewise/FEEC,
  mesh→0) and **spectral/UV** truncation (Connes–van Suijlekom operator
  systems, Λ→∞) are the two faces of the same convergence; the spectral action
  lives most naturally on the UV-truncation side (its cutoff Λ *is* a spectral
  truncation), and the propinquity is the common metric.

## Open (sharpened, with the tool named)

Establish (or cite) **propinquity convergence of the shape-regular edgewise
Whitney/FEEC tower** of `W(3,3) × K3` to the continuum spectral triple. The
2025 result that a polynomial path of Riemannian metrics on a closed spin
manifold is continuous in the spectral propinquity (arXiv:2504.11715), and the
operator-system truncation convergence (arXiv:2005.08544), are the directly
applicable building blocks. With propinquity convergence in hand, R3's
spectral-action (Einstein–Hilbert + matter) convergence follows from the
continuity theorem — closing the analytic core.

## Sources

- F. Latrémolière, *Continuity of the Spectrum of Dirac Operators of Spectral
  Triples for the Spectral Propinquity*, Math. Ann. (2023),
  [arXiv:2112.11000](https://arxiv.org/abs/2112.11000) — spectral + action
  functional continuity.
- F. Latrémolière, *Continuity for the spectral propinquity of Dirac operators
  associated with an analytic path of Riemannian metrics* (2025),
  [arXiv:2504.11715](https://arxiv.org/abs/2504.11715).
- Connes–van Suijlekom, *Gromov–Hausdorff convergence of state spaces for
  spectral truncations*, [arXiv:2005.08544](https://arxiv.org/abs/2005.08544).
