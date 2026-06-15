# The heterotic-on-K3 kinematic dictionary from W(3,3)

**Status: synthesis. Every *kinematic* input of an `E8 x E8` heterotic
compactification on `K3` is a `W(3,3)` invariant.** It assembles the new
KO-dimension derivation of `4D` (`W33_SPACETIME_DIMENSION_FROM_KO.md`) with the
established lattice/spectral corpus, and adds one standard string-theory link
(the anomaly instanton number) that was not previously recorded here. See
`w33_paper.tex`, Cor. "The heterotic--on--K3 kinematic dictionary".

## The dictionary

| Heterotic-on-K3 datum | Value | W(3,3) invariant | Source |
|---|---|---|---|
| Spacetime dimension `dim M` | `4` | `KO(F)=2q=6` + Connes–Barrett total `=2` | NEW (KO derivation) |
| Internal seed | `K3` | `chi(K3)=24=f`; intersection form sig `(3,19)=(q, g+mu)` | corpus (K3 lattice on seed) |
| Gauge lattice | `E8(-1) (+) E8(-1)` | rank-16 complement of `3U`; Laplacian energy `E+E=480=vk`, `E=240=f*Theta=g*lambda^mu=|E8|` | corpus (Phase 32; complement = E8^2, not D16+) |
| The single `E8` | canonical | mod-2 homology lift `H=ker A2/im A2 ~ F2^8` -> E8 (R1) | corpus + R1 |
| Instanton number | `n1+n2 = 24` | `= integral_{K3} c2(TK3) = chi(K3) = 24 = f` | NEW link |

## The new link (instanton number)

For the `E8 x E8` heterotic string on `K3`, the Green–Schwarz / Bianchi identity
`dH = tr R^R - tr F^F` integrates (with `c1(K3)=0`) to the anomaly condition

```text
n1 + n2  =  integral_{K3} c2(TK3)  =  chi(K3)  =  24,
```

the total instanton number carried by the two `E8` factors (the textbook
"24 instantons", commonly split `(12,12)`). Since `chi(K3)=24=f` is the `W(3,3)`
matter count, the number of heterotic instantons on the spacetime seed equals
the substrate matter count `f`. (Corpus uses "instanton" elsewhere only in the
Stokes/saddle sense — `240` Stokes types — so this anomaly link is new here;
`w33_paper.tex` had no occurrence of the word.)

## Honest scope

A structural **dictionary**, not a dynamical proof that the physical string is
heterotic-on-`K3`. Its content: every datum such a compactification must specify
by hand — dimension, seed, gauge group, instanton number — is, in the `W(3,3)`
substrate, pinned to a finite-geometry invariant (`dim=4` from `KO=2q`; seed and
instanton number from `chi=f=24`; gauge group from the Laplacian equipartition
`E+E=vk` with the `E8` the R1 homology lift). The dimension and instanton-number
entries are the new contributions; the seed and gauge-lattice entries are cited
from the existing corpus.

## Sources

- KO/4D: `W33_SPACETIME_DIMENSION_FROM_KO.md` (this repo).
- K3 lattice on the seed, `E8(-1)^2` complement, Laplacian `E+E=vk`: `docs/index.html`
  (Phase 32; explicit-complement identification).
- Heterotic anomaly / instanton number on K3: Green–Schwarz; the standard
  `n1+n2=c2(K3)=24` of heterotic/F-theory duality (e.g. the `(12,12)` heterotic
  string on K3).
