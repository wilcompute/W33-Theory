# Passes 1816–1820 — the sign is a local observable, and there are four bits, not one

Five items following Passes 1612–1616. Two upgrade the chirality result
substantially; one produces a new counting theorem; one is a correction to my own
framing from two passes ago.

---

## Pass 1816 (physics) — the handedness is readable from a **single frame**

Pass 1615 found the sign detected on the 540 frames and the 36 spreads, but as a
*character* fact — a statement about the whole group. The sharper question is
whether one frame's own symmetry already sees it. A frame's stabiliser in
`PGSp(4,3)` has order `51840/540 = 96`; restrict both degree-81 extensions to it:

```text
frame stabiliser order        : 96      contained in PSp? false
  Res(81a) = Res(81b) ?       : FALSE   -> the sign IS visible locally
spread stabiliser order       : 1440    contained in PSp? false
  Res(81a) = Res(81b) ?       : FALSE   -> visible here too
control: frame stab cap PSp   : 48
  Res(81a) = Res(81b) ?       : TRUE    -> invisible, as it must be
```

> **The two Steinberg extensions are already inequivalent as modules for the
> order-96 stabiliser of one frame.** The handedness is a local observable, not a
> global bookkeeping choice.

The control is what makes this a mechanism rather than a coincidence. The frame
stabiliser is `C₂ × S₄ = O_h`, order 48 inside `PSp` and 96 in the full group.
Intersecting back down to the `PSp` half makes the two restrictions **equal**. So
the sign lives precisely on the *outer half of one frame's own octahedral
group* — the extra factor of 2 that the frame acquires in the full collineation
group is exactly the thing that reads the chirality.

---

## Pass 1817 — a new free-cut family, and a correction to my own framing

Pass 1613's generator says: any frame-subset `T` with `χ_T ⊥ E₋₄(H)` is met by
every colour class of every resolution in exactly `|T|/9`. Testing every natural
`PGSp`-orbit of frame-subsets:

| family | count | \|T\| | \|T\|/9 | max ‖P₋₄ χ_T‖ | verdict |
|---|---|---|---|---|---|
| octet neighbourhood | 45 | 72 | 8 | 4.7e−15 | FREE |
| edge (matching ∋ e) | 240 | 9 | 1 | 2.9e−15 | FREE |
| **point (some line ∋ p)** | **40** | **108** | **12** | **8.8e−15** | **FREE — new** |
| line (L in the frame) | 40 | 27 | 3 | 2.12 | constrains |
| spread (both lines in S) | 36 | 45 | 5 | 6.12 | constrains |
| spread (some line in S) | 36 | 225 | 25 | 6.12 | constrains |
| H-neighbourhood of a frame | — | 32 | 3.56 | 3.06 | constrains |

> **New counting theorem.** In any resolution of `W(3,3)`'s frames, every colour
> class contains exactly **12** of the 108 frames having a line through any given
> point. Forty such identities, one per point.

Note the asymmetry: **points are free, lines are not.** `W(3,3)` is **not self-dual (q=3 odd; W(3,q) is self-dual iff q even -- Pass 4563/4755)**, so
this cannot come from the geometry alone — it comes from the frame construction,
which is built from pairs of *lines* and therefore breaks the point/line duality.

### The correction

My Pass 1613 write-up invited the reading that the 225-dimensional free space is
a reservoir of new constraints to export. It is not, and two measurements say so:

```text
rank_Q col(M) = 225, and the 240 edge columns already span it
   -> as RATIONAL constraints the 225 add nothing to the edge equations

rank_F2(M^T)              = 195
   + 45 octet vectors     = 225      <- the octets add 30
   + 40 point vectors     = 195      <- the points add NOTHING
   + both                 = 225
```

So freeness over ℚ does **not** imply usefulness over `F₂`, and the point family
is the counterexample: a genuine new counting theorem that is nonetheless already
implied mod 2. The octets are not one instance of a general family — so far they
are the **only** family that adds mod-2 rank, and that is what makes them
special. I should have measured this before framing the generator as a source of
new constraints.

---

## Pass 1818 — the spreads are the strongest branching family

Ranking the same families by relative `(−4)`-mass
`‖P₋₄ χ_T‖ / ‖χ_T − (|T|/540)·1‖` — the fraction of a subset's variation that
the free-constraint space cannot see, hence the fraction a solver must decide:

```text
spread (both lines in S)      0.9535   strong
H-neighbourhood of a frame    0.5568   strong
spread (some line in S)       0.5345   strong
line (L in the frame)         0.4189   weak
point / edge / octet          0.0000   FREE - no branching value
```

The spread-pair family at **0.954** is almost entirely invisible to the free
constraints, making it the best branching family available.

That family is not new as an object: [BT795](analysis/BT795_spread_envelope_routing_cell.md)
**owns** it, identifying each spread's `C(10,2) = 45` skew pairs as a complete
`K₁₀` in the skew-pair graph — and those 45 skew pairs are exactly 45 frames.
What is new here is its spectral property, that this `K₁₀` is the frame-subset
family least visible to the free constraints.

And that is the same object twice. The 36 spreads carry the *maximal* sign
separation (`∓9` for the Steinberg, `−20` for the whole edge module, Pass
1485/1615) **and** the maximal branching value for the resolution. The
combinatorial hardness and the chirality concentrate on the same 36 objects.

---

## Pass 1819 (physics) — four independent handedness bits, not one

Four of `V`'s five blocks are chiral. Are their signs one bit repeated, or
independent? The difference functions `δ_B = (χ_B − χ_B·ε)/2`:

```text
degree 15 : nonzero on 8 classes
degree 24 : nonzero on 6 classes
degree 30 : nonzero on 7 classes
degree 81 : nonzero on 6 classes
rank of the 4 x 25 matrix : 4
no two delta_B are equal
```

> **The four chiral blocks carry four independent sign bits.** `V`'s handedness
> is a point in a 4-bit space, not a single scalar.

This is a real upgrade to Pass 1615. The gauge sector (15 and 24), the physical
sector (81) and the constraint sector (30) can each be signed separately, and the
substrate selects one of **16** combinations. Pass 1616's six cancelling classes
are now explained: they are where independent bits happen to sum to zero, not
where a single bit is absent.

---

## Pass 1820 — there are three classes of size 540, and the order-4 one is not a square root

Pass 1616 noted two size-540 classes behaving oppositely. There are in fact
three, and all three have centraliser order 96:

| order | inner | fixed points | fixed lines | fixed frames | g² lies in a class of size |
|---|---|---|---|---|---|
| 2 | no | 8 | 6 | 16 | 1 (identity) |
| 4 | no | 0 | 4 | 6 | **270** |
| 4 | yes | 4 | 0 | 0 | 45 |

The order-2 outer class is BT773's — 8 fixed points, 6 fixed lines, 16 fixed
frames. The order-4 **outer** class is the one whose sign cancels in Pass 1616,
and the answer to "is it a square root of the frame involution" is **no**: it
squares into a class of size 270, not into the 540-class. So the frames do not
carry a `C₄` refining BT773's involution; the two size-540 outer classes are
independent objects that happen to share a centraliser order.

The inner order-4 class fixes no lines and no frames at all, which is why it
never appears in any of this.

> **Method note.** GAP's conjugacy-class *indices* are not stable across
> invocations — the same three classes came out numbered (4, 18, 20) and
> (5, 12, 18) in two runs of the same script. Identify these classes by
> `(order, size, inner, fixed-point/line/frame counts)`, never by index. Pass
> 1616's table used indices and should be read the same way.

---

## Prior art

- [BT795](analysis/BT795_spread_envelope_routing_cell.md) — **owns** the 36
  spreads as routing envelopes and their `K₁₀` of 45 skew pairs, the family Pass
  1818 measures. BT790 owns the maximum-clique-10 computation behind it.
- [BT773](analysis/BT773_involution_cube_theorem.md) — **owns** the order-2
  size-540 class ↔ frames bijection.
- Pass 1541 / 1536 (parallel track) — **own** the 45 octets and the 405 cuts;
  Passes 1606/1607 — **own** the `195 → 225` gain. Pass 1817 measures that the
  point family does *not* reproduce it.
- Pass 1613 — the spectral generator, whose scope this pass corrects.
- Pass 1615/1616 — the chirality and the cancellation table, upgraded here from
  one bit to four and from global to local.
- Pass 1485 — the 36 spreads and their maximal sign separation.

## Still open

The resolution. Pass 1818 names the best branching family; nothing here decides
`χ(H) = 9`. And the mod-2 question is now sharper: is there any family other
than the octets that adds `F₂` rank to the frame system?
