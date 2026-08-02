# Passes 2516–2523 — completeness is settled, the labelling hunt is dead, and `M` is in hand

---

## Pass 2516 — frontier completeness: **settled**, and my Pass 2505 is retracted

Pass 2505 declared frontier completeness "the load-bearing question". The parallel track
points at Pass 1821, and Pass 1821's own text is unambiguous:

> *"A compiled Algorithm-X search **exhausts** every exact cover through frame zero:
> 394200 … The previous Pass-1505 lower bound was therefore **the exact global count** …
> This upgrades Pass 1505 from an exact lower-bound frontier to a **complete
> classification count**."*

> **`3,547,800` covers in exactly `327` `PSp(4,3)`-orbits is a complete classification,
> not a frontier. Pass 2505's framing is withdrawn.**

Consequence for my own Pass 2496: the `K₈` criterion is therefore **unconditional**, not
frontier-relative. If every one of the 327 links has clique number `< 8`, `χ(H) = 9` is
**refuted outright** — no completeness caveat needed. That makes the computation more
valuable than I described it, not less.

---

## Pass 2517 — the labelling hunt is dead: a **fourth** gate

Pass 2511 found the frozen representatives have trivial stabilisers under my GAP frame
labelling. The obvious fix was to use the repo's own canonical construction,
`w33_pass1801_1805_common.build_geometry()`, which supplies exactly the right objects:

```text
points 40   edges 240   lines 40   frames 540   octets 45
M : 540 x 240   row sums {4}   col sums {9}
frame action from acts[i][3], closure order 25920 = |PSp(4,3)|
```

Everything about that geometry is correct. But:

```text
first 60 frozen reps, measured orbit sizes : {25920: 60}
first 60 frozen reps, frozen   orbit sizes : {12960: 60}
```

and the decisive test:

```text
rep 0 : 60 frames -> column sums  min 0  max 5   all ones? FALSE
rep 1 : 60 frames -> column sums  min 0  max 3   all ones? FALSE
rep 2 : 60 frames -> column sums  min 0  max 4   all ones? FALSE
```

> **The frozen Pass-1511 representatives are not exact covers under the
> `pass1801_1805_common` labelling either.** They use a third ordering, belonging to the
> `pass1505/1511` construction specifically, and it is recorded nowhere on disk.

Four gates now: wrong generators (order 192), wrong form convention, labelling mismatch
against my GAP ordering, and labelling mismatch against the repo's own common ordering.
**No link number has been published from any of them.**

---

## Pass 2518 — `M` is in hand, and that kills the dependency

The labelling problem is now moot, because the object that actually matters is available:

```text
M = 540 x 240 frame/edge incidence, row sums 4, column sums 9
```

This confirms the structure derived in Pass 2504 from counting alone — a frame covers the
**4 transversal edges** of the perfect matching between its two disjoint lines, and each
edge lies in **9** frames. With `M` and the frame action both in hand:

> **The whole computation can be done self-contained: run exact cover on `M` directly,
> obtain my own 3,547,800 covers and 327 orbits, and run the `K₈` test in my own
> labelling.** Reproducing `394,200` through frame 0 is then an independent confirmation
> of Pass 1821 rather than a dependency on it.

Nothing from `pass1511` is needed. The C++ worker committed at Pass 2511 takes cover
masks, so only the cover generation changes.

**Not executed this pass.** The remaining work is one DLX run (Pass 1821 reports 477M
nodes, ~508 s compiled) plus the existing clique search.

---

## Pass 2519 — the parallel track confirms Pass 2468, and sharpens it

Their Pass 2474 independently reaches my Pass 2468 result and goes further:

```text
N_{Sp(4,3)}(C5) = 5:8, NONSPLIT          (my Pass 2468: 0 order-20 complements)
element orders  : 1^1 2^1 4^10 5^4 8^20 10^4
every order-8 lift T satisfies  T^4 = z
z acts as -I on the 144, so  T^4 = -I,  minimal polynomial x^4 + 1
Hom_{5:8}(E8, 90) = 0
144 = 36 copies of the faithful 4-dimensional irreducible
```

The last line is my Pass 2476 exactly; the `T⁴ = −I` mechanism is theirs and is the
sharper form. **Their result and mine agree and neither needed the other**, which is the
best kind of cross-track outcome.

---

## Pass 2520 — outside the box (1): `x⁴ + 1` puts `√2` in the controller

Their `T⁴ = −I` with minimal polynomial `x⁴ + 1 = Φ₈` means the lifted normaliser's
eigenvalues are **primitive 8th roots of unity**, so its splitting field is

```text
Q(zeta_8) = Q(i, sqrt(2))
```

My Pass 2440 censused every word of length ≤ 7 in `⟨R₄,U₆⟩ = SL₃(ℤ)` and found the
reducible ones land in exactly **two** quadratic fields:

```text
Q(sqrt 5)   golden phi, phi^2
Q(sqrt 2)   silver 1 + sqrt 2, first at word length 7
```

> **`ℚ(√2)` enters the arithmetic controller through `Φ₈`, and `Φ₈` enters the group
> theory through the double cover** — the `C₄` of `5:4` lifting to the `C₈` of `5:8`.
> The silver ratio's field and the lifted normaliser's field are the same field.

**Scope: this is a field coincidence with a plausible mechanism, not a proved link.** Two
objects both landing in `ℚ(√2)` is exactly the count-match pattern this repo rejects
unless a map is named, and no map is named here. Recorded as a **test to run**: does the
`SL₃(ℤ)` word whose growth rate is `1+√2` have any relation to the order-8 lift, or is
`ℚ(√2)` simply the second-smallest real quadratic field and therefore cheap to hit?

---

## Pass 2521 — outside the box (2): are the rank-9 multiplicities the 540-frame permutation character?

Their Pass 2472 decodes the rank-9 fusion of the rank-22 shell algebra:

```text
valencies      1, 256, 24, 128, 48, 48, 8, 3, 24     (sum 540)
multiplicities 1,  15, 15,  20, 162, 135, 108, 24, 60 (sum 540)
```

The multiplicities of an association scheme on 540 points are the **dimensions of the
common eigenspaces**, i.e. the multiplicities of irreducible constituents in the
permutation representation on the 540 frames. And `1, 15, 15, 20, 24, 60` are all
**degrees of `U₄(2)` irreducibles** (its degree list is `1,5,5,6,10,10,15,15,20,24,30,30,
30,40,40,45,45,60,64,81`).

> **Conjecture with a one-command test:** the rank-9 multiplicities are exactly the
> constituent degrees of `Ind_{Stab}^{PSp(4,3)} 1` on the 540 frames, with `162 = 2×81`,
> `135 = 3×45`, and `108 = 2×54?` requiring the actual decomposition to check.

The frame stabiliser has order **48** (Pass 2510), so the permutation character is
`Ind` from an order-48 subgroup, and GAP decomposes it in one call. If the multiset
matches, their combinatorial scheme and this session's representation-theoretic work are
descriptions of one object — and `162`, `135`, `108` acquire names.

**Not computed.** Stated because it is cheap, falsifiable, and would connect two threads
that have run in parallel all session.

---

## Pass 2522 — the remaining items, honestly

- **Pentagon zero mode vs the `C₃` orientation** — not tested. Still well-posed.
- **The eight pentagons simultaneously** — not tested.
- **Certificate value index** — still not built. Fourth report.

---

## Pass 2523 — ledger

| claim | discharged by | status |
|---|---|---|
| frontier completeness | Pass 1821 exhaustive Algorithm X | **settled; Pass 2505 retracted** |
| `K₈` criterion is unconditional | the above + Pass 2496 | upgraded |
| frozen reps are covers in the common labelling | column sums 0–5 | **refuted; 4th gate** |
| `M` is 540×240, degrees 4 and 9 | `build_geometry()` | confirmed |
| self-contained route is unblocked | `M` + frame action in hand | **ready, not run** |
| `5:8` nonsplit | Pass 2468 (mine) and 2474 (theirs) | agreed independently |
| `ℚ(√2)` link between `Φ₈` and the silver word | — | **coincidence, test named** |
| rank-9 multiplicities = permutation character | — | **conjecture, test named** |

---

## Prior art

- Pass 1821 — **owns** the complete cover classification; supersedes my Pass 2505.
- Pass 2474 (parallel track) — **owns** the `T⁴ = −I` mechanism.
- Pass 2472 (parallel track) — **owns** the rank-9 scheme and its multiplicities.
- `w33_pass1801_1805_common.build_geometry()` — **owns** the canonical `M`.
- Passes 2468/2476/2496/2510 (mine) — the normaliser, the module, the criterion, the action.

## Still open

- The `K₈` run, now self-contained and needing only a DLX pass over `M`.
- Whether `ℚ(√2)` is a real link or a cheap coincidence.
- Whether the rank-9 multiplicities are the 540-frame permutation character.
