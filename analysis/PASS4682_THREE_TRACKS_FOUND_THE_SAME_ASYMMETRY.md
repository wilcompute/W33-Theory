# Pass 4682 — three tracks reached the point/line asymmetry independently, by three methods

Three lanes are running on this repository. Within one day all three produced a version of
the same structural fact, none citing the others, and each of the three would be weak alone.
Together they are strong. This file exists so the next grep finds all three from any of
them.

## The fact

**The point carrier and the line carrier of a generalised quadrangle are inequivalent
objects, except when the quadrangle is self-dual — and `W(3,q)` is self-dual only for even
`q`.**

## Three arrivals

### Track A (this lane) — signing densities, Passes 4562–4563

Random `±1` line-signings reaching the Ramanujan bound, measured on two dual pairs built
from scratch over different fields:

| pair | field | carrier A | carrier B |
|---|---|---:|---:|
| 1 | GF(3)/GF(9) | Q(5,3) **7.2%** | H(3,9) **0.0%** |
| 2 | GF(2)/GF(4) | Q(5,2) **85.2%** | H(3,4) **0.0%** |

And the clean control at **fixed block size**: `W(3,3)` versus its dual `Q(4,3)`, both
SRG(40,12,2,4) with 6 edges per gauge block — **26.9% vs 27.8%, z = −0.39**, no difference.
That is what showed the driver is block size and not duality, and it required knowing
`W(3,3)` is *not* self-dual.

### Track B — association schemes

> *"same Bose–Mesner algebra ... but inequivalent point/line actions"*

The 120 nonsingular vectors give a 40-orbit whose intersection tensor **equals** the earlier
120-selector scheme — yet the new quotient is the 40 W(3,3) **points** while the old is the
40 **lines**. Identical scheme parameters, inequivalent `PSp`-sets.

This is the `G`-set rule of `CLAUDE.md` in its sharpest form: equal parameters are not an
equivalent action. It is also exactly the trap Track A fell into at Pass 4560, reading
40 points and 40 lines as self-duality — a claim Pass 4563 then had to withdraw.

### Track C — walk masses on the `C₈` selector

Six local non-backtracking walk species, with the apartment/star cancellation holding at
**GQ(2,2)** and failing everywhere else:

```
GQ(2,2):  224 + 64 = 96 + 192 = 288      ← equality
GQ(2,4):   60 ≠ 36
GQ(4,2): 2812 ≠ 792
GQ(3,3):  712 ≠ 180
```

## Why the three together are more than any one

**GQ(2,2) is `W(3,2)`, and `q = 2` is even — so it is precisely the self-dual member.**
Track C's "exceptional cancellation" is therefore not an unexplained coincidence at all; it
is the one quadrangle in the list whose two carriers are the same object, so a quantity
computed on points and a quantity computed on lines *must* agree.

And Track C's `GQ(2,4)` / `GQ(4,2)` are `Q(5,2)` and `H(3,4)` — **the exact dual pair Track A
constructed at Pass 4562**. Both tracks measured that pair and both found it wildly
asymmetric:

| pair member | Track A: % Ramanujan | Track C: walk mass |
|---|---:|---:|
| GQ(2,4) = Q(5,2) | 85.2% | 60 |
| GQ(4,2) = H(3,4) | 0.0% | 2812 |

Two unrelated observables, one geometry, the same asymmetry.

## What this makes newly answerable

Track C lists *"closed formulas for all six masses for arbitrary (s,t)"* as open. The
duality reading supplies a constraint that any such formula must satisfy and that can be
checked before deriving it:

> Under `(s,t) → (t,s)` the point-side and line-side masses must **exchange**, so the
> cancellation equation is symmetric under that swap and can only hold identically when
> `s = t`. Any candidate closed form failing that exchange is wrong without further
> calculation.

That does not derive the formulas. It does mean GQ(2,2) needs no special explanation, and
that the search for others should be restricted to `s = t` — which, with Higman's `t ≤ s²`,
is a very short list.

## Evidence boundary

Track A's densities are 600–1000 samples per carrier with constructed and verified GQ
parameters. Tracks B and C are quoted from their own reports and **not re-derived here** —
in particular the six walk masses and the Bose–Mesner equality are taken as stated. The
claim that GQ(2,2) is self-dual is standard (`W(3,q) ≅ Q(4,q)` iff `q` even) and is cited,
not reproved. The proposed exchange constraint is a necessary condition, not a derivation,
and is offered as a check rather than a result.
