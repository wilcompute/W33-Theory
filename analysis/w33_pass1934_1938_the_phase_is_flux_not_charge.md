# Passes 1934–1938 — the phase sits on the **flux** sector, and its `ℤ₆` is internal

Five items. The first two sharpen last batch's physics considerably, and in a
direction that makes it *more* defensible rather than less.

---

## Pass 1934 (physics) — the `ℤ₆` is on the flux sector, not the charge sector

Pass 1933 found the substrate's unique phase on the degree-90, inside the coexact
block, and read it as charge quantization. Testing *which* Hodge sector that
actually is, by building the boundary maps explicitly:

```text
2-cells (triangles)                          : 160
dim im(d0)   = exact,   GRADIENT sector      :  39
dim im(d1^T) = coexact, CURVATURE sector     : 120
harmonic (ker d1 ∩ ker d0^T)                 :  81
```

The exact block is `im(d₀)` — gradients, i.e. **pure gauge**. The coexact block is
`im(d₁ᵀ)` — the image of the 2-cells, i.e. **curvature**. The `ℤ₆` phase lives in
the 120.

> **The substrate's one phase is a phase of the curvature sector. It is flux
> quantization, not charge quantization.**

That is a correction to Pass 1933's reading, and it strengthens the argument. A
`U(1)` on a curvature sector is exactly what a magnetic flux is; a `U(1)` on the
gradient sector would have been Gauss law. Charge quantization in thirds is then
the *Dirac dual* of a sixfold flux quantum rather than a direct identification —
which is a derivation with a known name attached instead of a numerical
coincidence.

The gauge sector (39, gradients) and the physical sector (81) are both rational,
so neither carries any phase at all.

---

## Pass 1935 (physics) — the `ℤ₆` is **internal**, and chirality inverts it

`ℤ[ω]^× = ⟨−ω⟩ ≅ ℤ₆` consists of *scalars* in `End_PSp(90) ≅ ℂ`. Scalars commute
with the group action by definition, so:

> **The `ℤ₆` is an internal symmetry of the flux sector — it commutes with
> `PSp(4,3)` entirely.** It is not a subgroup of the substrate's symmetry group;
> it is a symmetry *of the module over* that group.

And the outer involution acts on it. The outer element is complex conjugation on
`Irr(PSp(4,3))` (Pass 1900) and swaps the two degree-45s, so on scalars it sends
`ω ↦ ω̄ = ω⁻¹`. Hence:

```text
Z6 = <-omega>, internal, commuting with PSp(4,3)
  containing Z3 = <omega>
  with the OUTER involution acting by INVERSION
```

An internal `ℤ₃` on which conjugation acts by inversion, sitting inside a `ℤ₆`
whose extra `ℤ₂` is `−1`, is structurally the shape of **the centre of `SU(3)`
with charge conjugation acting on it** — and the correlation between that `ℤ₃` and
third-integer charge is the standard colour–charge correlation, not a new claim.

Stated at the scope earned: what is computed is that the flux sector's internal
automorphisms are `ℤ₆`, that `ℤ₃ ⊂ ℤ₆` is inner-commuting, and that the outer
involution inverts them. The reading as colour-centre-plus-conjugation is an
identification, and this pass does not argue it.

---

## Pass 1936 (physics) — the physical sector is structurally neutral

Pass 1880 showed the 81 admits no invariant complex structure at *any* subgroup,
because 81 is odd and a real vector space carries `J` with `J² = −1` only in even
dimension. Pass 1933 adds that its character field is rational.

> **The harmonic/physical sector can carry no `U(1)` of any kind, at any
> subgroup, for any group.** Whatever it describes is uncharged — not as a fit,
> but as a parity obstruction.

That is a falsifiable structural statement rather than a numerical one: it says
the physical sector cannot be given a phase by *any* symmetry breaking whatever.
If the sector is later identified with something charged, the identification is
wrong, not the sector.

---

## Pass 1937 — the cross-track eponym audit is clean

Running the parallel track's characteristic names through the new index:

```text
Hashimoto 19 files   Ihara 40   MacWilliams 6   Gaussian 20
Bockstein 16 files   Mackey 5   Brauer 5       Kantor 3
```

**None are hidden** — every one appears in at least one topically-named file. So
their corpus is reachable by topic search, and the July 15 chirality arc was the
anomaly rather than the rule. That is worth knowing before generalising the
indexing problem: it is a *localised* defect in the mid-2026 dated files, not a
corpus-wide one.

---

## Pass 1938 — dropping the pinned clique costs far more than it saves

Pass 1924 showed the clique-0 colour pinning is incompatible with any geometric
lex-leader break. The obvious response is to drop the pinning and break on the
group instead. Measuring the first half of that:

```text
spread-variable encoding, clique pinned (Pass 1892) :    60,909 branches
no pinning, symmetry_level=3                         : 7,415,101 branches, UNKNOWN
```

**A 122× blow-up.** The colour symmetry is `9! = 362,880` and pinning one clique
removes all of it, which is worth far more than the geometric group would be.

**Scope, stated plainly:** the geometric lex constraints were *not* implemented in
this run — the loop that would have added them is a placeholder. So this measures
the **cost of dropping the pinning**, not the benefit of geometric breaking, and
the combination remains untested. Reported that way rather than as a test of the
idea, because presenting a placeholder run as a negative result would be exactly
the kind of thing Pass 1896 and Pass 1910 were about.

---

## Prior art

- Pass 1933 — the character-field computation this pass re-reads; Pass 353/355 —
  **own** `ℚ(ω)` for the Weil representation.
- Pass 1900 — the outer involution as complex conjugation.
- Pass 1880 — the parity obstruction on the 81.
- Pass 1892/1924 — the encoding and the incompatibility Pass 1938 quantifies.
- Passes 1907–1911 (parallel track) — **own** the 56-class phase poset and the
  `A₆` `𝖘𝖔(3)` reconciliation of the two complex structures; they also adopted
  the `σ_S` similitude correction and the mean-vs-maximum correction from this
  track, and issued their own provenance correction against Passes 353/355.

## Still open

- Whether the sixfold flux quantum is physical. Dirac duality gives the charge
  reading a name, but the identification is still an identification.
- `χ(H) = 9`. The pinning-plus-geometry combination is the one untested encoding.
- Where a threefold generation index would live, if anywhere. The `ℤ₃` found here
  is a colour-centre shape, not a generation index, and nothing in the substrate
  has yet produced a 3 of the right kind.
