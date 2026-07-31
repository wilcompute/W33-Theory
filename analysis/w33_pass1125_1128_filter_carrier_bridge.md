# Passes 1125–1128 — the tree filter's generators, a 5× smaller carrier, and a bridge that cannot exist

Four exact results and one CI wiring. Two of them close standing open questions, and
one hands the parallel track a strictly better carrier than its own minimum.

---

## Pass 1125 — the tree filter has exactly 8 minimal generators

Pass 1122 showed the subgroups with `b₁(Δ/H) = dim St^H = 0` form an upward-closed
family (a filter), because `St^K ⊆ St^H` whenever `H ≤ K`. A filter is determined by
its minimal members. Computing them over all 116 conjugacy classes:

```text
tree-quotient classes : 23
MINIMAL ones          :  8
```

| index | \|H\| | structure | SmallGroup |
|---|---|---|---|
| 810 | 32 | (C₂)³ : (C₂)² | [32, 49] |
| 270 | 96 | (A₄ : C₄) : C₂ | [96, 195] |
| 240 | 108 | (C₃)³ : (C₂)² | [108, 40] |
| 240 | 108 | (C₃)³ : C₄ | [108, 37] |
| 216 | 120 | S₅ | [120, 34] |
| 162 | 160 | ((C₂)⁴ : C₅) : C₂ | [160, 234] |
| 120 | 216 | ((C₃×C₃) : C₃) : Q₈ | [216, 88] |
| 72 | 360 | A₆ | [360, 118] |

That is a complete characterisation: **a subgroup of PSp(4,3) kills the Steinberg
exactly when it contains a conjugate of one of these eight.** The list is
strikingly mixed — a 2-group of order 32, two 3-groups-with-complement of order
108, and the alternating and symmetric groups A₆ and S₅ — so there is no single
structural feature ("contains a Sylow", "is a p-group") that explains it, and I do
not claim one.

The frame stabiliser `C₂ × S₄` of order 48 contains none of the eight, which is
now *forced* rather than observed: it has `b₁ = 2`, so by the filter property it
cannot contain any tree subgroup.

---

## Pass 1126 — the 3×81 lives in three orbits of size 432, not in the 2240

Pass 1124 showed W(E6) is intransitive on the 2240 A₂ root triples: 14 orbits.
Decomposing each orbit separately:

```text
orbit | 81_a | 81_b | rank
   1  |  0   |  0   |  1
   1  |  0   |  0   |  1
  27  |  0   |  0   |  3      (x6 such orbits, all zero)
 240  |  0   |  0   |  7
 270  |  0   |  0   |  21     (x2, both zero)
 432  |  1   |  0   |  26
 432  |  1   |  0   |  26
 432  |  1   |  0   |  26
totals = [3, 0]                (matches the whole 2240)
```

**Every one of the three 81s sits in a distinct 432-orbit, and every other orbit
contributes exactly zero.** The 2240 is not a carrier of the 81; 1296 of it is, and
that 1296 is three independent copies of a 432.

This matters for the parallel track's carrier hierarchy `2240 : 3·81₋`,
`3360 : 4·81₋`, `15120 : 81₊ ⊕ 26·81₋`. The smallest **tested** carrier of a single
81 is not 2240 — it is a **432-orbit**, a factor 5.2 smaller, and it is transitive
where the 2240 is not. The hierarchy should read

```text
432 (transitive, one 81)  <  2240 (intransitive, three 81s in three 432s)  <  3360  <  15120
```

The 432-orbit has point stabiliser of order 51840/432 = 120. No claim is made about
which group of order 120 that is, or about any relation to the S₅ appearing in Pass
1125's minimal list — two order-120 objects in one session is exactly the coincidence
this corpus has been burned by.

---

## Pass 1127 — BT781's bridge functor cannot exist

> **PRIOR ART, FOUND LATE (2026-07-31). BT783 owns this obstruction.** BT781's
> "Next experiment" was answered by the two adjacent files: `BT782` writes the
> bridge as the exact sequence `1 -> C2_chiral -> Gamma(T)' -> Aut+(Q3) -> 1`,
> and `BT783` refutes it — "centre order 1, abelianization order 3, normal C2
> subgroup none, index-2 subgroup none, order-24 quotient none". Everything
> below was computed without citing them, so the *headline* of this pass is a
> rediscovery and is withdrawn as a first result.
>
> What survives is strictly stronger and is not in BT783: BT783 refutes ONE
> route (the central-C2 extension). The quotient-lattice computation below shows
> there is **no nontrivial common quotient of any kind**, so *every* bridge
> factoring through a quotient fails, not just that one — and it identifies the
> largest common subgroup, `A4`, which BT783 does not compute. Pass 1376 then
> shows that `A4` is the derived subgroup of the frame stabiliser itself.
>
> This is the seventh failure mode firing on its own author, one batch after
> being written down. The cause was measured rather than guessed: the guard's
> token grammar extracted **zero** tokens from BT781's boundary, because it had
> no rule for group notation like `2^3:S3`. `group_tokens()` in
> `scripts/check_rediscovery.py` fixes that; it now yields four shared tokens
> between BT781's boundary and BT782.


BT781 ends with a proposed next experiment:

> BT782 should build the explicit bridge functor `Aut(Q3)=2³:S₃ → Γ(T)′=2⁴:C₃`
> by quotienting the cube reflection bit and adding the missing tomotope binary bit.

That route is **impossible**, and the obstruction is complete:

```text
O_h        = SmallGroup[48, 48]  = C2 x S4
Gamma(T)'  = SmallGroup[48, 50]  = 2^4 : C3
isomorphic : false                                    (BT781's result, confirmed)

O_h quotient types        : 1, C2, (C2)^2, S3, [12,4], [24,12], [48,48]
Gamma(T)' quotient types  : 1, C3, A4 = [12,3], [48,50]
COMMON quotient types     : 1  only
largest common QUOTIENT   : trivial

largest common SUBGROUP   : order 12, type [12,3] = A4
```

There is **no nontrivial common quotient at all**, so a construction that factors
through "quotient one, then extend to the other" has nothing to factor through.
Both groups do have an order-12 quotient, but they are different ones — `[12,4]`
versus `A₄ = [12,3]`.

What survives is a **common subgroup**, not a common quotient: `A₄`, which is
exactly the group BT781 itself identified as the cube half's derived subgroup
("cube-derived order distribution: {1:1, 2:3, 3:8}"), and which sits inside `2⁴:C₃`
as `2²:C₃`. So the shared structure is a core, approached from below by both, and
the numerical identity `2³·6 = 2⁴·3` is a coincidence of orders rather than the
shadow of a functor.

BT781's "one tomotope binary bit = one cube reflection bit" reading should be kept
as the arithmetic observation it is, and not upgraded.

---

## Pass 1128 — the 540 factorization identifies neither object

Pass 1121 found 133 files whose use of 540 is mechanically ambiguous. Reading the
densest cluster (`bt1187`–`bt1212`) explains why, and the reason is not sloppiness:

```text
bt1203:  mu_distribution == {4: 540}
```

W(3,3)'s collinearity graph is `SRG(40, 12, 2, 4)`, so its non-adjacent **point**
pairs number `40·27/2 = 540`, each with μ = 4. That file is definitively about the
**point**-nonedge 540.

But every other file in the cluster cites only

```text
51840 = 540 * 2 * 48
```

and **that identity holds for both 540s**, because both stabilisers have order 96 in
PGSp(4,3). The line-nonedges also number `40·27/2 = 540` (each line is disjoint from
exactly `q³ = 27` others). So the factorization is true of two different objects and
therefore identifies neither.

**The disambiguation rule is therefore not "write more carefully" but "cite the
object, never the factorization":** cube / skew pair / frame / 3A₁ involution for
the line side, noncollinear point pair for the point side.

One further alias found in the cluster: `bt1205` calls its 540 `"root_triples"`,
which matches neither vocabulary and is a **sixth** name for something in this
family. It is flagged, not resolved.

---

## CI

`.github/workflows/stale-boundaries.yml` runs the Pass 1120 sweep on every
`analysis/**.md` change plus weekly. The **self-test is gated** (it pins the
BT810/BT811 case at exactly two shared tokens, so narrowing the token grammar
becomes a build failure); the sweep itself is **advisory**, because a shared token
is a candidate and gating on candidates trains people to ignore the signal.

## Prior art

- [BT781](analysis/BT781_cube_tomotope_48_split.md) — owns the 48-split and posed the bridge question closed above.
- [Pass 1122](analysis/w33_pass1120_1124_boundaries_aliases_trees.md) — the filter property and the 23 classes.
- [Pass 1124](analysis/w33_pass1120_1124_boundaries_aliases_trees.md) — W(E6) intransitive on the 2240.
- Pass 1113 (parallel track) — the carrier hierarchy sharpened above.
- Monson, Pellicer, Williams, *The Tomotope*, Ars Math. Contemp. 5 (2012).
