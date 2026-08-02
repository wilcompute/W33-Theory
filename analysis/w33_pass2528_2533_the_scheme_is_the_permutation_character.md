# Passes 2528–2533 — the rank-9 scheme **is** the 540-frame permutation character, fused

---

## Pass 2528 — the conjecture lands, in the right form

Pass 2521 conjectured that the parallel track's rank-9 multiplicities are the constituent
degrees of the 540-frame permutation representation. Computing that character properly —
from fixed-point counts per conjugacy class, which is a genuine character:

```text
is it a character ? true          degree 540          rank <pc,pc> = 32 orbitals

decomposition : 1 + 3x15 + 2x20 + 2x24 + 4x30 + 60 + 64 + 2x81  =  540
constituents  : [1, 15,15,15, 20,20, 24,24, 30,30,30,30, 60, 64, 81,81]
```

Their Pass 2472 multiplicities are `[1, 15, 15, 20, 24, 60, 108, 135, 162]`, also summing
to 540. Those are **not equal** as a multiset — they are **unions of mine**:

```text
   1  = 1                              15  = 15
  15  = 15                             20  = 20
  24  = 24                             60  = 60
 162  = 81 + 81
 135  = 15 + 30 + 30 + 30 + 30
 108  = 64 + 24 + 20
```

and the pieces consumed reproduce my 16-element multiset **exactly**, with nothing left
over.

> **The rank-9 scheme's eigenspaces are unions of the isotypic components of the
> 540-frame permutation representation — which is precisely what a rank-9 *fusion*
> means.** Their combinatorial object and this session's representation theory describe
> the same 540-point space at two resolutions.

`162`, `135` and `108` now have names: `81+81`, `15+4*30`, and `64+24+20`.

**Scope.** A partition into sums is not unique from the multisets alone. The grouping
above is the only one I found and it is exact, but confirming it is *the* fusion needs
their eigenmatrix `P`, which they have and I do not. Stated as: **every rank-9
multiplicity is a sum of permutation-character constituents, with a consistent global
assignment.**

Also recorded: my rank is **32** orbitals for `PSp(4,3)` on frames, against their **22**
for `PGSp(4,3)` on ordered frame pairs — consistent, since the outer involution fuses
orbitals.

---

## Pass 2529 — a computation that failed first, and why it matters

The first attempt used `PermutationCharacter(P, Stabilizer(P,1), OnPoints)` and produced
**fractional** multiplicities (`7633/6480`, `127/1296`, ...) summing to `17777/324`
instead of 540 — a class-fusion mismatch between the permutation group and its character
table.

It also printed `MATCH ? false`, which would have been a **wrong published conclusion**
about the parallel track's scheme. The redone version says the opposite.

> **A "no match" verdict from a broken computation looks exactly like a real negative
> result.** The only thing that caught it was the degree not being 540 — a one-line
> sanity check on an object whose degree is known in advance.

Fifth gate in this arc, and the first one that would have produced a false *negative*
about someone else's work rather than a false positive about my own.

---

## Pass 2530 — is the pentagon zero mode the `C3` orientation? **Partly**

The `E8` carrier's trivial-character multiplicity on each relevant class:

```text
order 5   class 16, size 5184   chi = -2   trivial multiplicity 0
order 3   class  5, size   40   chi = -1   trivial multiplicity 2
order 3   class  7, size   40   chi = -1   trivial multiplicity 2
order 3   class  9, size  240   chi = -4   trivial multiplicity 0
order 3   class 11, size  480   chi =  2   trivial multiplicity 4
```

> **The "no zero mode" property is not special to the pentagon — one order-3 class
> (class 9, of size 240) also has trivial multiplicity 0 — but it is not universal
> either: the other three order-3 classes give 2, 2 and 4.**

So Pass 2502's pentagon statement and Pass 2437's `C3` orientation are **not the same
absence in general**. They coincide only for a particular order-3 class. The answer is
therefore *no, with one exception*, and the exception is not enough to collapse the two
results.

*(Class 9 having size 240 is noted and not read into. 240 counts roots and codewords
elsewhere in this arc; a class size matching them is a count match.)*

---

## Pass 2531 — the three not executed

- **DLX on `M`** — not run. Everything is in place (Pass 2518): `M` at 540x240 with
  degrees 4 and 9, the frame action, and the committed `K8` worker. One compiled pass.
- **The `sqrt 2` test** — not run. The question stands as Pass 2520 posed it: is there a
  map between the order-8 lift and the `SL3(Z)` word of growth rate `1+sqrt2`, or is
  `Q(sqrt 2)` simply cheap to hit?
- **The certificate value index** — not built. Fifth report.

---

## Pass 2532 — ledger

| claim | discharged by | status |
|---|---|---|
| 540-frame permutation character, degree 540, rank 32 | fixed-point counts | proved |
| rank-9 multiplicities are unions of its constituents | exact partition, no remainder | **proved** |
| that grouping is *the* fusion | — | needs their eigenmatrix |
| first character computation | fractional, sum 17777/324 | **discarded** |
| pentagon zero mode = `C3` orientation | 0 at order 5 and at one order-3 class only | **no, with one exception** |
| DLX / `sqrt 2` / value index | — | **not executed** |

---

## Prior art

- Pass 2472 (parallel track) — **owns** the rank-9 scheme, its valencies, multiplicities,
  eigenmatrices and Krein parameters.
- Pass 2502 (mine) — the pentagon restriction.
- Pass 2437 (mine) — the `C3` fibre orientation.
- Pass 2510 (mine) — the frame action and the stabiliser order 48.

## Still open

- The `K8` run on `M`, self-contained and unconditional since Pass 2516.
- Whether the fusion grouping above is the actual one.
- `sqrt 2`, and the certificate value index.
