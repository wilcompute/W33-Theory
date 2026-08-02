# Passes 2000–2004 — spreads meet in one line or four, and degree 40 is ambiguous too

Five items. One completes the spread-pair picture; one finds a second place where
count-matching is unsafe; one is a third failure of the same approach, now with a
structural explanation rather than a compute excuse.

---

## Pass 2000 — the intersection of two spreads is **1 or 4**, never anything else

```text
intersection sizes over all C(36,2) = 630 spread pairs : {1: 360, 4: 270}
```

> **Two distinct spreads of `W(3,3)` share exactly one line or exactly four
> lines.** No pair is disjoint, and no other intersection size occurs.

The disjointness half independently reconfirms Pass 1828's measurement (0
disjoint pairs of 630), reached there by a different computation. The rigidity —
only two values from a possible `0..9` — was not known.

---

## Pass 2001 — the 270 is a class, the 360 is not

```text
orbit 270 : shared lines 4, stabiliser 192 = S4 x D8
            matches a conjugacy class as a G-set?  YES (size 270, order 2)
orbit 360 : shared lines 1, stabiliser 144 = C2 x ((S3 x S3) : C2)
            matches a conjugacy class as a G-set?  NO
```

The 270-orbit ↔ class correspondence is confirmed by a second, independent route
(Pass 1996 came at it from the centraliser's orbit structure; this from the
orbit's stabiliser). The 360-orbit has stabiliser of order 144 and `|G|/144 =
360`, but **no conjugacy class of size 360 has its character** — so it is a
genuine `G`-set with no class counterpart.

Recorded as a negative rather than left implied: not every natural orbit is a
class, and the 270 was not typical.

---

## Pass 2003 — degree 40 is ambiguous too

The Pass 1875 failure was that degree 270 admits **eight** conjugacy classes of
index-270 subgroups, so matching the count proved nothing. Sweeping the degrees
this arc has used:

| index | subgroup classes | count-matching safe? |
|---|---|---|
| 27 | 1 | yes |
| 36 | 1 | yes |
| **40** | **2** | **NO** |
| 45 | 1 | yes |
| **270** | **8** | **NO** |

> **Degree 40 is ambiguous.** That is the point/line duality: `W(3,3)` has 40
> points and 40 lines, and they are *non-isomorphic* `G`-sets — exactly what Pass
> 1874 found when the point and line permutation modules turned out to carry
> different degree-15 constituents.

And a useful positive: **degree 45 has a single class**, so the parallel track's
"these 45 are those 45" identifications are safe at the `G` level on count alone.
Degrees 27 and 36 likewise.

---

## Pass 2004 — five classes whose centralisers fix nothing

Pass 1995's negative ("`C` fixes no point, line, frame or spread") was the clue
that named the 270. Sweeping for the same signature:

```text
class 45,   order 2 : smallest spread-orbit 12, line-orbit 16
class 270,  order 2 : smallest spread-orbit  2, line-orbit  4   <- named (Pass 1996)
class 1620, order 4 : smallest spread-orbit  2, line-orbit  4
class 540,  order 4 : smallest spread-orbit 12, line-orbit 16
class 540,  order 4 : smallest spread-orbit  2, line-orbit  4
```

Three classes share the 270's exact signature — smallest spread-orbit 2, smallest
line-orbit 4. Those are the candidates for the same style of naming, and the
method that worked once is now a stated procedure: **when a centraliser fixes
nothing, look at its smallest orbit, not its fixed points.**

---

## Pass 2002 — orbit-built parallel classes fail for a structural reason

Third attempt, this time on non-cyclic subgroups: it did not complete, and the
reason is not compute budget.

Two random transvections almost always generate a **large** subgroup. A large
subgroup has few, large orbits on the 540 frames — and a parallel class needs a
union of orbits totalling exactly 60. Once the smallest orbit exceeds 60, no
union can work at all; when orbits are few, the subset-sum has almost nothing to
choose from.

> The approach needs subgroups **large enough to be useful and small enough to
> have orbits under 60** — a narrow band that random 2-generator subgroups miss
> almost surely. Enumerating subgroup classes by order and filtering on maximum
> orbit length is the version worth trying; sampling generators is not.

Recorded as a diagnosed failure rather than a fourth "no verdict".

---

## Prior art

- Pass 1828 — **owns** the 0-disjoint-spread-pairs measurement Pass 2000
  reconfirms.
- Pass 1996 — the 270 naming Pass 2001 independently reconfirms.
- Pass 1874 — the point/line module difference Pass 2003 explains group-theoretically.
- Pass 1875/1984 — the count-matching failure Pass 2003 generalises.

## Still open

- What the 360-orbit corresponds to, given it is not a class.
- Whether the size-1620 and size-540 classes with the 270's signature name
  spread-pair-like configurations.
- `χ(H) = 9`.
