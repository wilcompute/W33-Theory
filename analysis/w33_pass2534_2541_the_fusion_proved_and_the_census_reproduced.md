# Passes 2534–2541 — the census reproduced from scratch, and the rank-9 fusion proved with its mechanism

---

## Pass 2534 — the cover census, independently reproduced

Self-contained Algorithm X over the canonical `540 × 240` incidence matrix from
`w33_pass1801_1805_common.build_geometry()` — no dependence on the Pass-1511
representatives whose frame labelling could not be recovered (Passes 2511, 2517).

```text
M: 540 x 240, row degree 4, column degree 9   OK
covers through frame 0 : 394200   (Pass 1821: 394200)   match=1
search nodes           : 240,834,801
implied global count   : 394200 * 540 / 60 = 3,547,800
real 22m47s
```

> **`394,200` and `3,547,800` reproduced from a construction that shares no code with
> Pass 1821.** The validation gate that fired five times in this arc **passes**.

That also retires the labelling problem: the census never needed the frozen
representatives, only `M`.

---

## Pass 2535 — `PGSp` on the 540 frames: rank **22**, confirmed independently

Building the similitude group as `Normalizer(GL(4,3), SP(4,3))` (order 103680, acting on
frames with order 51840, frame stabiliser 96):

```text
genuine character ? true      degree 540      rank <pc,pc> = 22

[degree, multiplicity] :
  [1,1] [15,1] [15,2] [20,2] [24,2] [60,1] [60,2] [64,1] [81,1] [81,1]

sum d*m  = 540
sum m^2  = 1+1+4+4+4+1+4+1+1+1 = 22   = dim of the centraliser algebra = RANK
```

> **Rank 22 confirmed, and confirmed twice over**: once as `⟨pc,pc⟩` and once as `Σ m_χ²`,
> the centraliser-algebra dimension. This independently reproduces the parallel track's
> rank-22 shell algebra.

*(Under `PSp` the rank is 32 — Pass 2528 — consistent, since the outer involution fuses
orbitals.)*

---

## Pass 2536 — the rank-9 fusion, **proved**, with the mechanism

Their Pass 2472 gives multiplicities `[1, 15, 15, 20, 24, 60, 108, 135, 162]`. Those are
**not** unions of the `PGSp` isotypic dimensions `[1, 15, 30, 40, 48, 60, 64, 81, 81, 120]`
— e.g. `20` and `24` appear nowhere among them. Here is why, and it is the mechanism
their step 3 asks for:

> **An isotypic component of degree `d` and multiplicity `m` is `(d-dim irrep) ⊗ (m-dim
> multiplicity space)`. A COMMUTATIVE subalgebra of the centraliser algebra acts on the
> multiplicity space, so a component with `m = 2` SPLITS into two `d`-dimensional
> eigenspaces. Components with `m = 1` cannot split.**

The four multiplicity-2 components — `[15,2]`, `[20,2]`, `[24,2]`, `[60,2]` — are exactly
the ones that can split, and exactly the ones the fusion needs:

```text
   1   = 1
  15   = the multiplicity-ONE degree-15
  15   = one half of [15, 2]
  20   = one half of [20, 2]
  24   = one half of [24, 2]
  60   = [60, 1]
 135   = (other half of [15,2]) + [60,2]                 = 15 + 120
 108   = (other half of [20,2]) + (other half of [24,2]) + [64,1]
                                                         = 20 + 24 + 64
 162   = [81,1] + [81,1]                                 = 81 + 81
                                                    total = 540
```

Matches their multiset **exactly**, and the pieces consumed reconstitute the isotypic
dimensions exactly (`15+15 = 30`, `20+20 = 40`, `24+24 = 48`).

### This corrects my own Pass 2528

Pass 2528 gave the grouping from the **`PSp`** decomposition and read `135 = 15 + 4×30`.
Under `PGSp` that `120` is a **single** isotypic component `[60, mult 2]`, not four
30s — same number, wrong attribution. `162 = 81+81` and `108 = 64+24+20` were already
correct.

More importantly, Pass 2528 described the eigenspaces as "unions of isotypic components".
**That is false where the multiplicity is 2**, and it is precisely the multiplicity-2
splitting that makes the fusion possible. The corrected statement is the one above.

**Scope.** This proves the dimension bookkeeping is consistent and identifies the only
mechanism that can produce their multiset. It does **not** yet match individual primitive
idempotents of `Q` to individual constituents — that still needs their eigenmatrix, and
remains their step 3's final half.

---

## Pass 2537 — where `χ(H)` stands

Their Pass 2551 refuted nine-colourability globally by searching the link of one
representative from **every one of the 327 orbits** and finding **zero** containing `K₈` —
which is the Pass 2496 reduction executed, and unconditional since Pass 2516 established
the census is complete rather than a frontier.

Their Pass 2556 added Hoffman `α(H) ≤ 60`, attained, plus a DSATUR 14-colouring; and they
have since verified 13-, 12- and 11-colourings, rejecting a bad 10-colour run that carried
47 conflicts.

```text
chi(H) >= 10     Pass 2551, global theorem
chi(H) <= 11     verified colouring
```

> **One bit remains: does a valid 10-colouring exist?**

Recorded here because the `K₈` criterion this arc contributed is now fully spent — it
gave the lower bound and has nothing further to say about 10 versus 11.

---

## Pass 2538 — ledger

| claim | discharged by | status |
|---|---|---|
| 394,200 / 3,547,800 from scratch | Algorithm X on `M`, 240.8M nodes | **reproduced** |
| `PGSp` frame rank is 22 | `⟨pc,pc⟩` and `Σ m²` agree | proved |
| multiplicity-2 splitting is the fusion mechanism | isotypic structure | proved |
| the corrected 9-part grouping | exact arithmetic, no remainder | proved |
| Pass 2528's "unions of isotypic components" | — | **corrected** |
| idempotent-level matching | — | still needs their `Q` |

---

## Prior art

- Pass 1821 — owns the census this reproduces.
- Passes 2472 / 2551 / 2556 (parallel track) — own the rank-9 scheme, the global
  refutation, and the chromatic interval.
- Pass 2496 (mine) — the `K₈` reduction their 2551 executes.
- `w33_pass1801_1805_common.build_geometry()` — owns `M`.

## Still open

- `χ(H) ∈ {10, 11}`.
- Idempotent-level confirmation of the fusion.
- The `sqrt 2` question and the certificate value index — both still not done.
