# Passes 1928–1933 — the substrate has exactly one phase, and it is quantized in sixths

Six items. The last one is the physics, and it is the first dimensionful anchor
this arc has produced.

---

## Pass 1933 (physics) — one non-rational block, and its field is Eisenstein

Every result in this arc so far has been dimensionless: groups, graphs, counts.
A physical map needs one anchor. Here it is.

Computing the **character field** of each block of the signed 240-edge module:

```text
degree 15 : Rationals
degree 24 : Rationals
degree 30 : Rationals
degree 81 : Rationals
degree 90 (over the full group PGSp) : Rationals

degree 90 restricted to PSp(4,3) = 45 + 45,  character field CF(3)
    = Q(zeta_3) = Q(sqrt(-3)) = Q(omega),  degree 2 over Q,  conductor 3
```

> **Exactly one block of the substrate has a non-rational character field, and
> that field is the Eisenstein field `ℚ(ω)`.** Its conductor is 3 — the same `q`.

The chain to a unit is then forced:

1. `End_PSp(90) ≅ ℂ` with `J` unique up to sign (Pass 1895).
2. The character field is `ℚ(ω)`, so any `ℤ`-form of the module is a module over
   an order in `ℤ[ω]`, the Eisenstein integers.
3. `ℤ[ω]^× = ⟨−ω⟩ ≅ ℤ₆` — the **sixth** roots of unity. This is classical.
4. Hence the integral automorphisms of the phase form a cyclic group of order 6,
   and the elementary phase step is `2π/6`.

> **The substrate carries exactly one phase, and it is quantized in sixths of a
> turn.**

### The physical reading — stated as a reading, not a derivation

A `U(1)` whose integral automorphisms are `ℤ₆` has charge labels
`q ∈ {0, ±1/3, ±2/3, ±1}` under `e^{2πiq}` — sixth roots of unity are exactly the
phases of charges quantized **in thirds, with both signs**. That is the observed
electric-charge spectrum of one Standard Model generation.

If that identification is made, it is the anchor the whole structure lacked: fix
`e`, and every other charge in the model is a `ℤ₆` label rather than a free
parameter. Everything else in this arc — the Hodge blocks, the chirality bits,
`σ_S` — is dimensionless and would hang off that one unit.

**Scope, explicitly.** Items 1–4 are computed or classical. The charge reading is
an *identification*, not a theorem: nothing here derives electromagnetism, and the
`ℤ₆` is a statement about integral automorphisms of a 90-dimensional module of
`PSp(4,3)`. What is established is that the substrate admits exactly one phase and
that its quantization is sixfold. Whether that phase *is* electric charge is the
identification to be argued, and this pass does not argue it.

**Prior art checked before claiming.** `ℚ(ω)` as the character field is already in
the corpus for the **Weil representation** — Pass 353 states it verbatim
("The character field of `U` is `Q(√(-3)) = Q(ω)`"), and Pass 350 builds the
Eisenstein trace form. What is new here is that (a) the *edge module's coexact
block* has this field, (b) it is the **only** non-rational block of the five, and
(c) the step from field to `ℤ₆` phase quantum. Charge quantization appears
nowhere in the corpus (checked: `docs/index.html` and all of `analysis/`).

---

## Pass 1929 — dogfooding found a hole in my own index

The alias index built last batch scored **`Eisenstein: 0`**. The Pass 350 prior
art that motivated the whole tool would not have been caught by it — I found that
file by plain grep. The `named:` class only fires before
*theorem/indicator/bound*, so eponymous **object** names were invisible.

Fixed with a curated eponym list — not a regex over capitalised words, because
Passes 1107/1483 measured that widening a token vocabulary without calibration
turns these guards into noise. Then the calibration itself failed informatively:

```text
object tokens surviving the <=12-file cut : 7 of 34
```

Eponyms are common by nature, so the discriminating-power rule filtered every one
— re-hiding exactly what the index exists to surface. The design fix is to keep
object tokens but list **only the topically opaque files** for them, since those
are the ones no topic search can reach:

```text
object:Eisenstein ⚠ (opaque-named only) -> 2026-05-18_toroidal_...,
                                           2026-07-15_pass348_weil_q3_anatomy, ...
object:Weil       ⚠ (opaque-named only) -> 2026-07-15_pass348, pass352, pass353, ...
```

Both retraction sources are now reachable by name. 3,133 files, 608 tokens, 34
object tokens, `--check` green.

---

## Pass 1928 — the check is wired into pre-commit

An index only prevents rediscovery if it is current, and last batch it was built
but not enforced — the same gap between *instruction exists* and *instruction
works* that cost two retractions. `build_topical_aliases.py --check` now runs as a
local pre-commit hook on any change under `analysis/`, `docs/` or `manuscripts/`.

---

## Pass 1931 — cross-track audit through the index

Running the tokens that matter through the new index:

```text
Gow        3 entries      Vinroot   1      Weil      13
Eisenstein now indexed    Kantor    0
```

`Kantor: 0` is worth recording — the symplectic-spread literature's central name
appears nowhere in this corpus, which is a gap for the `σ_S` work rather than a
collision.

---

## Pass 1932 — `σ_S` for general odd `q`: existence yes, uniqueness only at `q = 3`

The similitude construction gives **existence** for every odd `q` directly: pick
`μ` a non-square in `F_q^×` and `g ∈ GSp(4,q)` with `g² = μI`; then `g` is
fixed-point-free (a fixed point needs `λ² = μ`), outer (non-square multiplier),
and `x² − μ` irreducible gives `F_q⁴` the `F_{q²}`-structure whose lines are the
spread. In characteristic 2 no non-square exists and the construction fails —
both branches, as before.

**Uniqueness** — that the kernel of `Stab(S) → Sym(lines of S)` is exactly `C₂` —
was verified by enumeration at `q = 3` only, and is *not* upgraded here. The note
records it as `q = 3`, and this pass does not widen it.

---

## Pass 1930 — the colour-free encoding

Not run. Pass 1924 showed the clique-0 colour fixing is incompatible with any
geometric lex-leader break; dropping the fixing and breaking on the group alone is
the untried combination, and it is not attempted here. Recorded as not done
rather than implied.

---

## Prior art

- Pass 353 — **owns** `ℚ(ω)` as the Weil representation's character field;
  Pass 350 — **owns** the Eisenstein trace form.
- Pass 1895 — `End_PSp(90) ≅ ℂ`, `J` unique up to sign.
- Passes 1107/1483 — **own** the token-calibration discipline Pass 1929 follows.
- Passes 1912/1917 — the two retractions this tooling exists to prevent.

## Still open

- Whether the `ℤ₆` phase *is* electric charge. An identification, not a theorem.
- `χ(H) = 9`.
- Uniqueness of `σ_S` for odd `q > 3`.
