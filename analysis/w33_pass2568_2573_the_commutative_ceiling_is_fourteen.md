# Passes 2568–2573 — the commutative ceiling is **14**, `√2` is closed, and the index is finally built

---

## Pass 2568 — the 22 orbitals, computed independently

Union–find on all `540² = 291,600` ordered frame pairs under the exported `PGSp(4,3)`
frame action (order 51840, three generators):

```text
ORBITALS (rank) : 22          matches the parallel track's rank-22 shell algebra
valencies       : 96, 48,48,48,48, 24x7, 16, 12,12,12, 8,8, 6,6, 3, 1     (sum 540)
symmetric       : 14 of 22    (so four antisymmetric pairs)
```

Third independent confirmation of rank 22 in this arc — once as `⟨pc,pc⟩`, once as
`Σ m_χ²`, and now by direct orbital enumeration.

---

## Pass 2569 — the commutative ceiling is `Σ m = 14`, and it is new

The isotypic multiplicities of the 540-frame permutation representation under `PGSp` are
`[1,1,2,2,2,1,2,1,1,1]` (Pass 2535). Two dimensions follow:

```text
centraliser algebra dimension = sum m^2 = 22     (the rank)
MAXIMUM commutative subalgebra = sum m   = 14
```

because the centraliser is `⊕ M_{m_i}(ℂ)` and a maximal commutative subalgebra of
`M_2(ℂ)` is 2-dimensional.

> **No commutative fusion of the 540-frame configuration can have rank above 14.**

The parallel track's Pass 2433 exhausted all `65,535` binary symmetric seeds and found
commutative fusions of ranks `3³ 4⁵ 5³ 6 7 8 9` — topping out at 9 — while noting that
"arbitrary non-binary partitions remain outside the classification".

> **`14` is the exact ceiling for that open region.** Their search reached 9; ranks
> `10`–`14` are the precise remaining window, and `15` and above are impossible.

### The fusion structure, derived rather than matched

The 14 finest possible eigenspaces (every multiplicity-2 block split) are

```text
[1, 15,15,15, 20,20, 24,24, 60,60,60, 64, 81,81]        sum 540
```

Reaching their rank-9 multiplicities `[1,15,15,20,24,60,108,135,162]` means merging
14 parts into 9 — saving exactly 5 — and there is one consistent way:

```text
135 = 15 + 60 + 60      3 parts -> 1, saves 2
108 = 20 + 24 + 64      3 parts -> 1, saves 2
162 = 81 + 81           2 parts -> 1, saves 1
unchanged : 1, 15, 15, 20, 24, 60
```

This supersedes both earlier attempts: Pass 2528 grouped from the `PSp` decomposition and
mis-attributed `135`, and Pass 2536 wrote `135 = 15 + 120`. The `120` is the
multiplicity-2 block `[60,2]`, which the fusion may or may not split internally — either
way it sits whole inside `135`, so `15 + 60 + 60` is the structurally correct reading.

**Still not done:** matching individual primitive idempotents of `Q` to individual
constituents. The dimension bookkeeping is now forced; the assignment is not.

---

## Pass 2570 — the certificate value index, **built**

Six reports as "proposed, not built". `scripts/build_certificate_index.py` now exists.

```text
wrote CERTIFICATE_INDEX.md: 30,907 values from 3,967 certificates
```

Calibrated the same way as `check_rediscovery.py` and `check_certificates.py`: values in
`[100, 10^12]` appearing in at most 12 files. Indexing every integer would reproduce the
noise problem both of those had to be calibrated away from.

The test is the seven answers that hid in plain sight this session:

```text
3547800 -> w33_pass1505_..._frontier.json/certified_cover_lower_bound
394200  -> w33_pass1821_1825_....json/pass1821_complete_cover_census/fixed_frame_covers
13648   -> w33_pass1511_1515_....json/pass1512_disjoint_partner_frontier/...
25920   -> ...
51840   -> ...
```

> **`394200` now resolves in one command to the certificate that proves it** — the answer
> this arc spent several passes failing to find, because certificates are prose-free and
> no topic search reaches them.

`py -3 scripts/build_certificate_index.py <value>` looks a number up. **Do that before
opening a question about it.**

---

## Pass 2571 — `√2`: closed as a coincidence, and it is the *same* coincidence as `φ`

Pass 2520 flagged that `ℚ(√2)` appears twice: as the real subfield of `ℚ(ζ₈)` from the
order-8 lift `T` (`T⁴ = −I`, minimal polynomial `Φ₈ = x⁴+1`), and as the field of the
silver ratio `1+√2`, a growth rate in `⟨R₄,U₆⟩ = SL₃(ℤ)`.

They cannot be related:

```text
T           order 8, FINITE       eigenvalues are primitive 8th ROOTS OF UNITY, modulus 1
silver word infinite order        1 + sqrt2 is a real quadratic UNIT, modulus > 1
```

> **One `√2` comes from a cyclotomic field of roots of unity; the other from a
> unit-growth field. No map can carry a finite-order element to a hyperbolic one.
> Coincidence — closed.**

And it is the *same* coincidence the arc already diagnosed for `φ`: Pass 2083 showed
Gaussian binomials are products of cyclotomics so their roots are roots of unity, while
Pass 2439 found `φ` as the growth rate of an infinite-order word. **Roots of unity versus
units is the recurring trap in this project**, and `√2` is its third instance.

---

## Pass 2572 — `χ(H)`, and what this arc contributed

```text
chi(H) >= 10    their Pass 2551, global, unconditional since Pass 2516
chi(H) <= 11    their verified colouring
```

One bit remains. The `K₈` reduction (Pass 2496) supplied the lower bound and is now spent
— it says nothing about 10 versus 11. The `45 × (A₄/V₄)` symmetry-breaking is the right
instrument for the last bit and is theirs.

---

## Pass 2573 — ledger

| claim | discharged by | status |
|---|---|---|
| 22 orbitals, valencies summing to 540 | union–find on 291,600 pairs | reproduced |
| commutative fusion rank ≤ 14 | `Σ m` and `M_2` maximal commutative | **proved, new** |
| ranks 10–14 are the open window | above + their exhausted binary search | proved |
| `135 = 15 + 60 + 60` | merge arithmetic, forced | supersedes 2528 and 2536 |
| idempotent-level assignment | — | still open |
| certificate value index | 30,907 values, 3,967 files | **built** |
| `√2` link | finite vs infinite order | **closed as coincidence** |

---

## Prior art

- Pass 2433 / 2472 (parallel track) — own the binary-generated fusion classification and
  the rank-9 scheme.
- Pass 2551 / 2556 (parallel track) — the global refutation and the chromatic interval.
- Passes 2083 / 2439 (mine) — the roots-of-unity versus units distinction this reuses.
- Passes 2528 / 2536 (mine) — superseded here.

## Still open

- `χ(H) ∈ {10, 11}`.
- Whether any commutative fusion of rank 10–14 exists (non-binary partitions).
- Idempotent-level confirmation of the rank-9 assignment.
