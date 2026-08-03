# Passes 2674–2681 — reading §sec:parabolic-router properly: the paper had already warned me three times

Reading `photonic_holonet_body.tex` lines 340–720 in full. Four passages bear directly on
work I published in this session, and three of them are warnings I violated.

---

## Pass 2674 — the `E₈ ⊃ A₂ ⊕ E₆` branching is **explicitly warned against**

Line 680:

> *"Moreover **the transitive W33-code action and the standard `E₆ × A₂ < E₈` branching
> action are nonconjugate and have different root-orbit fingerprints**, so choosing
> rational `E₈` coordinates remains a chamber calibration rather than a symmetry-forced
> device frame."*

My Pass 2642 built the fractal holonet node from exactly that branching and wrote *"the
self-similarity is not a design choice — it is the branching rule of the tower"*.

> **The paper says that branching action is nonconjugate to the substrate's own, with
> different root-orbit fingerprints, and that using it is a calibration choice rather
> than something the symmetry forces.** That is the precise negation of what Pass 2642
> claimed.

Pass 2651 already withdrew that pass's framing on the grounds that the holonet's fractal
is 40-ary. This is a second, independent, and stronger reason: **the branching I used is
not the substrate's action at all.** Third strike on Pass 2642.

---

## Pass 2675 — my Pass 2442 spread/ovoid alignment is in the paper

Line 685:

> *"Incidence duality also changes the schedule type. `W(3,3)` has `36` spreads and no
> ovoids, while `Q(4,3)` has no spreads and `36` ovoids; the duality-odd checksum is
> therefore `Δ_SO = #spreads − #ovoids = ±36`, not an Euler characteristic."*

Pass 2442 recounted exactly this (0 ovoids / 36 ovoids, max partial ovoid 7) and cited
`w33_pass1021_corollary_ovoid_orientation.py`. It is **also** in the manuscript, with a
name (`Δ_SO`) and a caution I did not have (it is *not* an Euler characteristic).

The chirality/contextuality *alignment* I drew on top of it remains mine and remains
scoped as a two-point co-occurrence. The underlying duality fact is doubly prior art.

---

## Pass 2676 — there is prior Weil work at `q = 5, 7`

Lines 695–702:

> *"The construction is also **special to field order three**. At the tested odd anchors
> the regular-spread owner router covers the path carrier with degree `(q−1)/2`: `1, 2, 3`
> at `q = 3, 5, 7`, so only `q = 3` is lookup-free and bijective. The module backend
> changes at the same anchors: **the `q = 5` binary `24` is the `𝔽₂` restriction of an
> `𝔽₄` Weil `12`, while the `q = 7` `48` is the split dual pair `24 ⊕ 24*`**."*
>
> Witness: `analysis/w33_pass218_weil_shadow_split.g`

My Passes 2441/2458/2462 studied Weil constituents at `q = 3, 5, 7` and cited Gow,
Vinroot and Pass 353/355 — **but not Pass 218**, which is the repo's own `q = 5, 7` Weil
work and reaches conclusions about the same anchors from the module side.

Not a rediscovery — Pass 218's objects are `𝔽₂`/`𝔽₄` module restrictions, mine were
Frobenius–Schur indicators over `ℂ`. But it is the fourth Weil-adjacent file in this repo
that I found only after publishing, and it should have been cited.

**And there is a genuinely useful fact in it:** the router degree `(q−1)/2` equals `1, 2, 3`
at `q = 3, 5, 7`, so **`q = 3` is the unique lookup-free case.** That is a new reason for
`q = 3` beyond the ones I had catalogued (`q! = 2q`, minimal magic, `c = 24`).

---

## Pass 2677 — the size-six warning, which I came close to violating

Lines 598–603:

> *"The line stabilizer satisfies `1 → C₃³ → H_line → S₄ → 1`: its six signed states carry
> the tetrahedral-edge `S₄` action, while complement-pairing gives the unframed `S₃/C₂`
> axis action. **Firmware must therefore not identify the six edge states with a regular
> `S₃` clock merely because both sets have size six.**"*

My Pass 2437 found an `S₃` acting on a six-element fibre. That one **survives**: it was
measured as the induced action of the setwise stabiliser, with order and regularity
computed in GAP, not inferred from `|set| = 6`. But the warning is exactly aimed at the
inference I would have made a batch earlier, and Pass 2437 should cite it.

---

## Pass 2678 — what else is in this section that nothing of mine touched

Recorded because it is the part of the architecture I have no hardware for:

- **The Kraft-equality router.** The Bell-line parabolic's four orbits on 1296 compass
  pairs are `162+162+324+648`, whose normalised sizes satisfy
  `2⁻³+2⁻³+2⁻²+2⁻¹ = 1` exactly, giving a **complete prefix code** `{110, 111, 10, 0}`
  with expected word length `7/4`. *"the code lengths were not optimized from assumed
  traffic probabilities: they were read from exact group orbits."*
- **The incidence transceiver.** `T = N − J/10` has rank 24 with `TᵀT = 6E₂₄`, so
  `T/√6` is lossless on the shared gauge sector, and the address and route dark lattices
  are `[40,15,8]` and `[40,15,10]` — *different codes*, first separating at the third
  shell (`5085` vs `3645`).
- **The `4320 → 240 → 120` tower**, `18:1` then `2:1`, with the deck operation central in
  the order-`103680` action — the same group my Pass 2461 analysed for the `C₅`
  normaliser lift.

> **A prefix router with `7/4` expected word length and a rank-24 lossless transceiver are
> both fully specified and have no RTL.** They are better-defined hardware targets than
> anything I built this session, because the paper states their exact orbit structure.

---

## Pass 2679 — ledger

| claim | status |
|---|---|
| Pass 2642's `E₈ ⊃ A₂⊕E₆` branching is the substrate's | **refuted by the paper — nonconjugate actions** |
| Pass 2442's spread/ovoid fact | **prior art, twice (`Δ_SO = ±36`)** |
| Passes 2441/2458/2462 cite the relevant `q=5,7` work | **no — Pass 218 missed** |
| `q = 3` is the unique lookup-free router degree | **new to me; the paper's** |
| Pass 2437's `S₃` is a size-6 inference | **no — measured; but should cite the warning** |
| the Kraft router and transceiver have RTL | **no — best-specified unbuilt targets** |

---

## Prior art

- `photonic_holonet_body.tex` §"The parabolic router" and §"The incidence transceiver" —
  own all four passages above.
- `analysis/w33_pass218_weil_shadow_split.g` — owns the `q = 5, 7` module backends.
- `analysis/w33_pass1021_corollary_ovoid_orientation.py` — the spread/ovoid count.

## Still open

- Every one of the previous batch's five items.
- RTL for the Kraft prefix router and the rank-24 transceiver.
- Whether Pass 2642 retains any value now that its branching is known nonconjugate.
