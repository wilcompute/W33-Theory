## Passes 2682–2689 — the Kraft router built, the transceiver verified, and Pass 2642 laid to rest

---

## Pass 2682 — the Bell–compass router, in 9 logic cells

The paper's router theorem gives four Siegel-parabolic orbits on the 1296 compass pairs,
`162_L + 162_R + 324 + 648`, satisfying Kraft equality exactly and admitting the complete
prefix code `{0, 10, 110, 111}`.

Built as `rtl/w33_pass2682_kraft_router.sv` — encoder, self-delimiting constant-depth
decoder, and the four engineering actions the paper names.

```text
orbit sizes      : 648 324 162 162  (sum 1296)
Kraft sum        : 1.000000     (must be exactly 1)
expected length  : 1.750000     (paper: 7/4)
round-trip on all four classes, W(E6) fused view: 0 errors

ICESTORM_LC 9/5280      SB_IO 15/96
```

> **Nine logic cells for the entire routing decision**, with expected word length `7/4`
> reproduced to the digit.

The reason this is worth building rather than any other codec is the paper's own remark:
*"the code lengths were not optimized from assumed traffic probabilities: they were read
from exact group orbits."* A Huffman tree is fitted to measured statistics; this one is a
theorem about `PSp(4,3)` orbits, and the Kraft equality holding **exactly** rather than
`≤ 1` is what makes the decoder complete with no wasted branch.

The `chiral_resolved` input exposes the outer-Weyl fusion: dropping it collapses
`110/111` to a 2-bit `11`, which is the `W(E₆)` view, and only `PSp(4,3)` resolves the
chiral bit.

---

## Pass 2684 — the incidence transceiver: **the paper's theorem checks out**

`T = N − J/10` on the line–point incidence:

```text
rank(T) = 24                                      paper: 24        MATCH
eigenvalues of T^T T : {0 (x16), 6 (x24)}         so T^T T = 6 E_24 exactly
decoder x = N^T (N x)/6 on the 24-sector          max error 6.75e-16
```

> **Verified independently, from the repo's own geometry builder.** `T/√6` is a lossless
> transceiver on the shared 24-dimensional gauge sector, exactly as claimed.

RTL not built — a 40×40 integer datapath with a `/6` normalisation, larger than the
router and needing a fixed-point decision the paper does not make. It is the next
well-specified target.

*(I printed a row of `10T` and compared it to the paper's `{−3¹,−1⁹,0²⁰,1⁹,3¹}`
selector-word histogram. Those are different objects — the histogram is over the 480
local-axis selector vectors, not over rows of `T` — so the mismatch is my comparison, not
a discrepancy.)*

---

## Pass 2685 — Pass 218 read: it is the characteristic-2 shadow of my characteristic-0 work

```text
"the 24-dimensional irreducible F2 shadow has endomorphism field F4 and is the
 restriction of scalars of the AtlasRep/CTblLib 12a module"
"the q=7 48-dimensional shadow is the split hyperbolic sum U + U*"
"dimensions and transvection character values match the two modular Weil modules
 of degree (q^2-1)/2 described by Szechtman, arXiv math/0212378"
```

`(q²−1)/2` is precisely the **odd Weil half** whose Frobenius–Schur indicators I computed
in Passes 2458/2462 — `4, 12, 24` at `q = 3, 5, 7`. Pass 218 studies the same degree
family in **characteristic 2**; I studied it in characteristic 0.

> **Complementary, not duplicated — and it supplies a citation I did not have
> (Szechtman) for the modular side of exactly my family.**

---

## Pass 2686 — Pass 2642: what survives

Three independent strikes:

1. the holonet's fractal is **40-ary**, not 3-ary (Pass 2651);
2. the `E₆ × A₂ < E₈` branching action is **nonconjugate** to the substrate's W33-code
   action, with different root-orbit fingerprints (Pass 2674, quoting the paper);
3. and the paper calls using it *"a chamber calibration rather than a symmetry-forced
   device frame"*.

> **The mathematical claim is void.** `w33_pass2642_holonet_fractal_node.sv` does not
> model the holonet, does not model the substrate's action, and its branching factor is
> not the substrate's.

**What survives is the engineering only:** a working recursive SystemVerilog module with
an identical port signature at every depth, placed at depths 0–3, with a measured exact
law `LC(d) = 75·3^d − 2`. That is a correct fact about *that circuit* and about nothing
else.

Recorded as **relabelled, not retracted**: the file stays as a generic ternary-recursion
demonstrator and the `E₈`-branching justification is withdrawn. Leaving it in place with
the false rationale attached would be worse than either deleting it or renaming it.

---

## Pass 2687 — ledger

| claim | status |
|---|---|
| Kraft equality holds exactly | **verified, 1.000000** |
| expected word length `7/4` | **verified, 1.750000** |
| router fits 9 logic cells | measured |
| `rank(T) = 24`, `TᵀT = 6E₂₄` | **verified independently** |
| decoder `Nᵀ(Nx)/6` exact on the 24-sector | verified, `6.75e-16` |
| my `10T` row vs the selector histogram | **my comparison was wrong, not the paper** |
| Pass 218 is the char-2 shadow of my family | established |
| Pass 2642's `E₈` justification | **withdrawn; circuit relabelled** |
| transceiver RTL | not built |

---

## Prior art

- `photonic_holonet_body.tex` §"The parabolic router", §"The incidence transceiver" — own
  both theorems; this pass builds one and verifies the other.
- `analysis/w33_pass218_weil_shadow_split.g` and Szechtman `math/0212378` — the modular
  Weil modules.

## Still open

- Transceiver RTL, and the fixed-point choice it needs.
- Paper lines 720–2400 unread.
- Everything carried from earlier batches: `χ(H) ∈ {10,11}`, ranks 10–14, five
  certificates, the data-plane RTL.
