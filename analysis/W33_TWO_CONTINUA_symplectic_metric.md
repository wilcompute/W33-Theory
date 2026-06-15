# The two continua of W(3,3): symplectic (architecture) vs metric (physics)

**Status: genuine continuum-structure result. Explains why R3 needs an external
metric seed, and unifies the architecture and the physics as the two continuum
limits of one substrate.** Witness
`analysis/w33_two_continua_symplectic_metric.py`, data
`data/w33_two_continua_symplectic_metric.json`.

## Why R3's spacetime continuum cannot be intrinsic (the arithmetic tower is rigid)

The natural "intrinsic" refinement of W(3,3) is the **arithmetic tower**
`W(3,3^n)` — the symplectic GQ over the field extensions `F_{3^n}`. Computing it
(exact SRG eigenvalue formulas, verified against W(3,3) at q=3):

| q | points | adjacency eigenvalues | Laplacian nonzero |
| --- | ---: | --- | --- |
| 3 | 40 | 12, 2⁽²⁴⁾, −4⁽¹⁵⁾ | 10, 16 |
| 9 | 820 | 90, 8⁽⁴⁵⁰⁾, −10⁽³⁶⁹⁾ | 82, 100 |
| 27 | 20440 | 756, 26, −28 | 730, 784 |
| 243 | 14.4M | 59292, 242, −244 | 59050, 59536 |

`W(3,q)` has **exactly three distinct eigenvalues at every q** (it is an SRG by
construction), with all nonzero Laplacian eigenvalues `~ q²`. **No Weyl law
`N(λ)~λ^{d/2}` ever emerges** — the arithmetic tower does *not* converge to a
Riemannian manifold. Therefore:

> The **spacetime (metric) continuum cannot be obtained by refining W(3,3)
> arithmetically.** It genuinely requires an *external* curved 4-geometry —
> canonically **K3** (`χ(K3)=24=f`, a W(3,3) invariant) — refined edgewise
> (R3). This is a positive vindication of the almost-commutative `M⁴×F`
> framing: the external seed is *necessary*, not a modelling choice.

## The intrinsic continuum that *does* exist: symplectic (Weil → oscillator)

The substrate carries a second, genuinely intrinsic continuum. Its matter shell
is the Heisenberg group `3^{1+2}` and `Aut(W(3,3))=Sp(4,3)` acts on it — exactly
a **Weil-representation** datum (Gurevich–Hadani: the functor `V ↦ H(V)`, the
Weil rep of `Sp(V)` over `F_q`). The `q→∞` / archimedean limit of that Weil
representation is the **metaplectic (oscillator) representation of `Sp(4,ℝ)` on
`L²(ℝ²)`** — the continuous-variable, Fock/oscillator quantum computation. This
is the substrate's intrinsic **phase-space** continuum.

## The unification: architecture and physics are the two continuum limits

> One finite geometry, two continuum limits:
> - **metric** (external K3, edgewise) → **spacetime physics** (Standard Model
>   + general relativity, via the spectral action — R3);
> - **symplectic** (intrinsic Weil → oscillator) → the **photonic architecture**
>   (the continuous-variable / Fock universal computer).

This directly ties the project's two goals together: the *theory of everything*
(metric continuum) and the *architecture* (symplectic continuum) are the two
faces of the same finite substrate's continuum limit. It also explains the
division of labour: the physics needs K3 because W(3,3) is spectrally rigid; the
computer needs no external seed because its continuum (the oscillator rep) is
intrinsic to the Heisenberg/symplectic structure.

## What this is (honest)

A structural result, not a closure of R3's K3 computation. It (i) *proves* the
arithmetic tower is not a metric continuum (computed, exact), (ii) identifies the
intrinsic symplectic continuum (Weil → oscillator), and (iii) draws the
architecture↔physics unification. The K3 spectral-action computation (the metric
continuum's quantitative output) remains the application task.

## Sources

- S. Gurevich, R. Hadani, *Quantization of symplectic vector spaces over finite
  fields*, [arXiv:0705.4556](https://arxiv.org/abs/0705.4556) — the Weil-rep
  functor over `F_q`.
- Payne–Thas, *Finite Generalized Quadrangles* — `W(q)` parameters and spectra.
