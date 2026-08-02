# Passes 2059–2063 — why `q + 1 = 4`, and 3 is a primitive root mod 7

Five items. Two give the selection principle a *reason* rather than an identity;
one is a fact I dismissed too quickly last batch and should not have; one is
still running.

---

## Pass 2059 — why `q + 1 = 4`, at the right level

Pass 2054 reduced the selection to `q + 1 = 4` but left it as an arithmetic
identity. The reason is a compatibility between the substrate's **two
involutions**:

- `σ_S` pairs the `q+1` points of a line into `(q+1)/2` edges — its orbits are
  **2-subsets**.
- The star acts by **complementation** — a 2-subset goes to a `(q−1)`-subset.

Those coincide iff `q − 1 = 2`.

> **`σ_S`'s orbits are star-stable if and only if `q = 3`.**

So it is not a numerical accident about the number 4. It is the statement that
the involution generating the spread obstruction and the involution realising the
Hodge star act on **the same degree** — and they can only do that at `q = 3`.
That is a structural reason, and it is the form the claim should take.

---

## Pass 2060 — 3 is a primitive root mod 7, and I dismissed it too fast

Last batch I filed `ord₃(7) = 6` as "a count match, different objects" and moved
on. That was wrong to do so quickly. The right reading is the other order:

```text
3^1..3^6 mod 7 = 3, 2, 6, 4, 5, 1
```

> **`3` is a primitive root modulo `7`.** The substrate's characteristic
> generates the *entire* multiplicative group of its own Heawood number
> `2q + 1 = 7`.

Unlike the base-10 material this is base-independent and relates `q` to a quantity
derived from `q`, so it is not the kind of coincidence the count-match rule was
written for. Testing how special it is — `q` Sophie Germain (so `2q+1` prime) and
`q` a primitive root mod `2q+1`:

```text
q :   2    3    5   11   23   29   41   53   83
2q+1: 5    7   11   23   47   59   83  107  167
prim: T    T    F    T    T    F    F    F    T
```

`q ∈ {2, 3, 11, 23, 83}` in this range. **Every one of them is also in the
genus-ladder reachable set** (`q ≡ 2, 3, 11 mod 12`, Pass 2024).

**Flagged, not claimed.** Both lists are sparse, and small-list overlap is not
evidence — it is exactly the reasoning that produced three withdrawn claims in
this arc. Recorded as a question with a stated test: whether the primitive-root
condition and the mod-12 reachability condition are related, or agree by accident
on small values.

---

## Pass 2061 — the double-count audit

Pass 2054 found one place where I counted a single identity twice. Sweeping the
arc's other `q`-selection claims:

| claim | reduces to | distinct? |
|---|---|---|
| star acts on edges of `K_{q+1}` | `q + 1 = 4` | — |
| Heawood `= ` one past mod-12 midpoint | `q + 1 = 4` | **same** (Pass 2054) |
| `σ_S` orbits are star-stable | `q − 1 = 2` | **same again** (Pass 2059) |
| genus-ladder reachability | `q ≡ 2, 3, 11 (mod 12)` | **different** — a family, not a point |
| 3 a primitive root mod 7 | `ord_{2q+1}(q) = 2q` | **different** |

So the arc has **one** point-selection (`q + 1 = 4`, now with three equivalent
statements) and **two** genuinely different conditions that `q = 3` also
satisfies. The correction from last batch generalises: three of my "principles"
are one, and I should have noticed at the second.

---

## Pass 2062 — the corrected statement, for the draft

> **`W(3,3)` is distinguished among the `W(q,q)` by `q + 1 = 4`.** Its totally
> isotropic lines are tetrahedra; the tetrahedron is the unique simplex whose
> Hodge star acts in middle degree; and consequently `σ_S`'s selection of a
> 1-factor of each line is simultaneously a selection of a star-orbit. The
> obstruction generator and the star are the same choice, and only at `q = 3`.

One principle, three equivalent forms, one reason.

---

## Pass 2063 — reconstructing the `D₈` parallel class: **still running**

The parallel track's Pass 2012 built a 60-frame parallel class from twelve orbits
of a `D₈` inside the four-line-pair stabiliser. Reconstructing it independently —
build the stabiliser `H ≅ S₄ × D₈` (the size-270 centraliser, Pass 1996),
enumerate its subgroup classes of order 2, 4 and 8, take frame orbits, discard
internally overlapping ones, and subset-sum to 60 edges-disjointly.

**Launched and still running after ten minutes; no result.** Reported as in
flight, not as a negative — this is the fourth time this construction has been
attempted from this side and the first with the right subgroup band, so a
timeout is not evidence either way.

---

## Prior art

- Passes 2011–2015 (parallel track) — **own** the `D₈` witness and the subgroup
  census; Pass 2002 — the diagnosis of why random generators fail.
- Pass 2042/2047/2054 — the selection principle and its first correction.
- `dccxxiii` — the Heawood number and the clocks.

## Still open

- `χ(H) = 9`.
- Whether the primitive-root condition and mod-12 reachability are related.
- The `D₈` reconstruction.
