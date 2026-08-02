# Passes 2099–2103 — `ψ` is confined to the arithmetic group, and the cross-track note is finally written

Three clean negatives that scope the supergolden result properly, plus the note
I had deferred four times.

---

## Pass 2099 — no substrate count obeys the Narayana recursion

If `ψ` were structural rather than confined to the arithmetic group, some natural
counting sequence should satisfy `a(n) = a(n−1) + a(n−3)`. Checked:

```text
PG(n-1,3) points [n,1]_3   1, 4, 13, 40, 121, 364, 1093     Narayana? False
t.i. lines of W(q,q)       15, 40, 85, 156, 259, 400, 585    False
genus oscillator v         4, 7, 10, 13, 16, 19, 22          False
genus oscillator E         6, 21, 36, 51, 66, 81, 96         False
K_{q+1} edges              3, 6, 10, 15, 21, 28, 36          False
frames of W(q,q)           60, 540, 2720, 9750, 27972        False
```

> **None.** The `101`-forbidden / Narayana structure does not appear in the
> substrate's combinatorics. `ψ` enters **only** through the infinite arithmetic
> group `SL₃(ℤ)`, exactly as Pass 2093 stated.

A clean negative, and it keeps the supergolden result honest: it is a fact about
the phase carrier's arithmetic, not about the geometry.

---

## Pass 2100 — `ψ` is not distinguished by minimality

```text
plastic number (smallest Pisot)  t^3 - t - 1        1.3247180
supergolden psi                  t^3 - t^2 - 1      1.4655712
tribonacci                       t^3 - t^2 - t - 1  1.8392868
```

`SL₃(ℤ)` characteristic polynomials are `t³ − at² + bt − 1` for integers `a, b` —
an infinite family. **`ψ` is not the smallest Pisot number**, so `t³ − t² − 1` is
not singled out by minimality.

If it is distinguished, it is because the `R₄`/`U₆` relations force it — which is
the parallel track's result to establish, not a property of the polynomial.
Recorded so the supergolden finding is not over-read as "the substrate selects
`ψ`" when what is shown is "one witness element has growth rate `ψ`".

---

## Pass 2101 — the degree-5 invariant lives on a module the substrate does not contain

`W(E₆)` has basic invariant degrees `2, 5, 6, 8, 9, 12`, and the degree-5 one is
a quintic on the **6-dimensional reflection representation**.

```text
V_signed = 15 + 24 + 30 + 81 + 90     over PGSp(4,3)
degree 6 among the constituents ?  NO
```

> The reflection representation is **not** a constituent of the signed edge
> module. So the degree-5 basic invariant — the one place `Φ₅` genuinely lives in
> `W(E₆)` — sits on a space the substrate's edge module does not contain.

That completes the three-way split of "is the 5 there": **invariant theory** yes
(degree-5 invariant, on the reflection rep), **permutation action** yes (eight
pentagons on the 40 points), **arithmetic** no (`ℚ(ζ₅)` in no character field) —
and now, **edge module** no.

---

## Pass 2102 — their Pass 2050, read rather than reconstructed

Six attempts at reconstructing the `D₈` parallel class from this side; the last
reproduced the search space (116 subgroup classes of order 2/4/8 in
`H ≅ D₈ × S₄`) but hit GAP's recursion trap.

Their Pass 2050 has since transported all 33 local classes through the full group
and fused them into **14 full-group subgroup types** and **12 schedule orbits**,
with `|N_G(K)| · |K^G| = 51840` checked for each. That supersedes independent
reconstruction: the useful move now is to read their fusion, not to repeat the
search.

**Recorded as superseded, not as failed** — and as the sixth and final report of
this item.

---

## Pass 2103 — the cross-track note

`analysis/CROSS_TRACK_FIVE_RESULTS_FOR_THE_DRAFT.md`, deferred four times, now
written. It carries: the `q + 1 = 4` selection principle with its reason; the
`q ≡ 3 (mod 4)` unification of Gow's theorem, `σ_S`-is-`i`, and the primitive-root
property, with the short genus-reachability proof; the total incompatibility of
the two complex structures; the cubic-at-every-level result with `φ` located at
rank 5; the degree-safety table; and a list of what I got wrong.

---

## Prior art

- Passes 1942/1953, 2050–2053, 2064 (parallel track) — **own** the `SL₃(ℤ)`
  witness, the subgroup fusion, the graph identification and the `1 or q+1`
  census.
- Pass 2093 — the supergolden identification this pass scopes.

## Still open

- `χ(H) = 9` — best attacked from their 12 schedule orbits.
- Whether the `R₄`/`U₆` relations force `t³ − t² − 1`.
