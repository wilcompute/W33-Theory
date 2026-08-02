# Passes 2488–2495 — `73` is solved, the whole ladder is one Gauss sum, and Pass 355 needs a dimension correction

---

## Pass 2488 — `73` is **solved**, and the answer was committed in the repo all along

`data/w33_pass1510_bidirectional_cover_saturation.json` carries the orbit census:

```text
PSp(4,3) order 25920,  327 orbit types
   |stab| = 2   228 orbits   size 12960   ->  2,954,880 covers
   |stab| = 4    84 orbits   size  6480   ->    544,320
   |stab| = 8    15 orbits   size  3240   ->     48,600
                                     total   3,547,800
```

Factoring the total by the smallest orbit size:

```text
3,547,800 = 3240 * (4*228 + 2*84 + 1*15) = 3240 * 1095
1095 = 3 * 5 * 73
```

> **`73` comes from the weighted orbit count `1095 = 4·228 + 2·84 + 15`. It divides no
> orbit size and no orbit count — only the combination.**

Pass 2471 argued this was "probably an artifact" from sibling evidence. It **is** an
artifact, now proved. (`327 = 3 × 109` carries another sporadic prime by the same
mechanism.)

**And this closes a self-inflicted loop.** I spent Passes 2455, 2460 and 2471 on "why
73" while the histogram sat in a committed certificate. That is the repo's first rule —
*search for the RESULT* — failing on my own work for the third time this session.
Pass 2485 already recorded the same lesson about the frame graph `H`.

---

## Pass 2489 — the best known cover packing is **4**, and 9 is needed

The same frontier file carries a much stronger fact than the orbit census:

```text
disjoint partners of the canonical cover : 13,648
frozen disjointness graph clique number  :      3
four_packing_exact                       :   true
all 327 orbits have a disjoint partner   :   true
```

> **The canonical cover's link has clique number 3, so the largest packing exhibited is
> 4 pairwise disjoint covers. `χ(H) = 9` needs 9.**

The file's own quantifier audit is scrupulous and I repeat it rather than sharpening it:

> *"The 327 orbits are not proved to be all global cover orbits, and clique number three
> in the canonical-cover link is not the global packing number."*

So this is **not** a refutation. It is the honest frontier: `4 of 9`, with the gap
unexplained. Combined with Pass 2450 (no equivariant colouring) and the parallel track's
Pass 2432 (the selected nine-signature tuple is exactly impossible), the evidence
against `χ(H) = 9` is now substantial and still not conclusive.

---

## Pass 2490 — the entire ladder collapses to **one Gauss sum**

Measured directly:

```text
q= 3   g = 0.0000 +1.7321i = i*sqrt(3)    REAL: no    q mod 4 = 3
q= 5   g = 2.2361 -0.0000i =   sqrt(5)    REAL: yes   q mod 4 = 1
q= 7   g = 0.0000 +2.6458i = i*sqrt(7)    REAL: no    q mod 4 = 3
q=11   g = 0.0000 +3.3166i = i*sqrt(11)   REAL: no    q mod 4 = 3
q=13   g = 3.6056 +0.0000i =   sqrt(13)   REAL: yes   q mod 4 = 1
```

Gauss: `g(q) = √q` when `q ≡ 1 (mod 4)` and `i√q` when `q ≡ 3 (mod 4)`. The Weil
representation's character is built from the Gauss sum, so it is real exactly when
`q ≡ 1 (mod 4)`.

> **Everything this arc has accumulated is one congruence, and the mechanism is the
> quadratic Gauss sum being imaginary:**
>
> ```text
> q = 3 (mod 4)  <=>  -1 is a non-square in F_q
>                <=>  the quadratic Gauss sum is IMAGINARY
>                <=>  the Weil halves are non-self-dual (FS = 0), so they must be GLUED
>                <=>  PSp(4,q) has complex characters          (Gow 1985)
>                <=>  sigma_S is multiplication by i           (Pass 1908)
>                <=>  q primitive root mod 2q+1, Sophie Germain q  (Pass 2065)
> ```

The Gauss-sum *sign law* is classical and cited, not claimed. What this pass adds is that
it is the **common mechanism** under items the repo had been tracking as separate
conditions.

---

## Pass 2491 — a dimension correction to Pass 355

`analysis/2026-07-15_pass355_sp43_frobenius_schur.md` gives the Weil split at `q = 3` as

```text
dim W_+ = (q^2 + q)/2 = 6      dim W_- = (q^2 - q)/2 = 3
```

The character table of `2.U₄(2) = Sp(4,3)` contradicts the second:

```text
inflated degrees (z -> +I) : 1, 5, 5, 6, 10, 10, 15, 15, 20, 24, 30, 30, 30, 40, 40,
                             45, 45, 60, 64, 81
faithful degrees (z -> -I) : 4, 4, 20, 20, 20, 20, 20, 36, 36, 60, 60, 60, 64, 80
```

> **`Sp(4,3)` has no irreducible of degree 3.** The standard parity split of the Weil
> representation of `Sp(2n,q)` on functions over `𝔽_qⁿ` has degrees `(qⁿ+1)/2` and
> `(qⁿ−1)/2`, which at `q = 3, n = 2` is **`5 + 4`**, not `6 + 3`. Both sum to 9, but only
> `5 + 4` corresponds to representations that exist.

**What survives in Pass 355, and it is the substantive part:** the pieces are an `FS = 0`
complex-conjugate pair, each not self-dual, and *a choice is required*. That reading is
theirs, with Gow (1985) and Vinroot (2005, 2010) already cited there, and it is not
re-derived here.

**Scoping this session's work against Pass 353/355.** Per my own
`analysis/CROSS_TRACK_NOTICE_pass355_collision.md` (2026-08-01), which retracted glue-track
Passes 1900/1907/1914 as novel: the `q ≡ 3 (mod 4)` chirality content is **Pass 353/355
territory and is cited, not claimed**. What Passes 2444–2462 add on top is the
**central-character organisation** — the faithful/inflated partition of `Irr(2.U₄(2))`
(14 vs 20), the two non-isomorphic order-51840 doublings, the Weil halves landing on
**opposite** sides of the centre, and the `q ≡ 1 (mod 4)` behaviour (quaternionic vs
orthogonal) which Pass 355 does not treat.

---

## Pass 2492 — the Frobenius–Schur indicator **is** a KO-dimension statement

`analysis/W33_SPACETIME_DIMENSION_FROM_KO.md` already derives `KO-dim(F) = 6` with sign
triple `(ε, ε', ε'') = (+, +, −)`.

The FS indicator is exactly the classification of real structures:

```text
FS = +1  ->  real structure with J^2 = +1   (orthogonal)
FS = -1  ->  real structure with J^2 = -1   (quaternionic)
FS =  0  ->  NO real structure              (complex)
```

and `ε = J²`. So Pass 2462's table reads directly as a KO-dimension constraint:

| | chiral (faithful) | achiral (inflated) |
|---|---|---|
| `q ≡ 1 (mod 4)` | `FS = −1` → `ε = −1` → KO-dim ∈ {2,3,4,5} | `FS = +1` → `ε = +1` → KO-dim ∈ {0,1,6,7} |
| `q ≡ 3 (mod 4)` | `FS = 0` → no real structure until glued | `FS = 0` → same |

> **`KO-dim 6` requires `ε = +1`, an orthogonal real structure. That is the ACHIRAL
> (inflated, even-Weil) side. The chiral side is quaternionic and lands in {2,3,4,5},
> never 6.**

If that holds up, the repo's 4-dimensional-spacetime derivation runs through the
**achiral** tower, and the chiral tower — the one carrying the `E₈` roots — is excluded
from it by its real structure.

**Scope, and it is a large caveat.** This is an alignment of two sign conventions, not a
constructed spectral triple. `ε` in Connes' axioms is a property of the *specific* `J` on
the *specific* finite geometry, and the FS indicator is a property of an abstract
representation; identifying them requires exhibiting `J` as the FS real structure, which
is **not done here**. The repo has extensive Connes material (`BT921`, `BT1031`–`BT1039`,
`W33_TWO_CONTINUA`, `W33_HETEROTIC_K3_DICTIONARY`, and more in the manuscripts) that
should be read before this is taken further. Recorded as a **lead with a named test**,
not a result.

---

## Pass 2493 — the certificate defect is **not** one cause

Pass 2482 diagnosed integer dict keys. Testing that theory across the remaining six:

```text
w33_pass1872_1876_five_frontiers          53 integer-like keys, live form still does NOT reproduce
w33_pass1887_exact_global_weight5_decoder  0 integer-like keys, still fails
```

> **The integer-key defect is one real cause, confirmed on one file and repaired. It does
> not explain the rest.** `1887` has no integer keys at all.

The producer grep flagged four files hashing a live dict
(`1861_1865`, `1872_1876`, `1876_merge_dual_histograms`, `2300_2305_verify_frozen`), which
is a necessary but not sufficient condition. **The five remaining certificates are not
repaired**, and each needs its own investigation.

The round-trip rule is now in `CLAUDE.md` next to the heredoc and Unicode warnings, since
the trap is invisible and passes every `checks` block.

---

## Pass 2494 — ledger

| claim | discharged by | status |
|---|---|---|
| `73 = ` weighted orbit count `1095` | committed orbit histogram | **solved** |
| best exhibited packing is 4, need 9 | frozen disjointness graph | frontier, not a refutation |
| the ladder is one Gauss sum | direct computation + Gauss | proved (law is classical) |
| `Sp(4,3)` has no degree-3 irreducible | character table | **corrects Pass 355** |
| Weil split is `5 + 4` | parity split + character table | proved |
| `FS` indicator = KO `ε` | convention alignment only | **lead, not result** |
| certificate defect has one cause | — | **withdrawn**; mixed causes |
| five certificates | — | **not repaired** |

---

## Prior art

- `data/w33_pass1510_bidirectional_cover_saturation.json` and Pass 1533 — **own** the
  327-orbit census, the stabiliser histogram, and the clique-number-3 frontier. Pass 2488
  only factored what was already there.
- Passes 353/355 (2026-07-15) — **own** the `q ≡ 3 (mod 4)` FS-indicator chirality
  reading, with Gow (1985) and Vinroot (2005/2010) cited there.
- `analysis/CROSS_TRACK_NOTICE_pass355_collision.md` — my own 2026-08-01 notice, which
  scopes this.
- `analysis/W33_SPACETIME_DIMENSION_FROM_KO.md` — **owns** `KO-dim(F) = 6` and `(+,+,−)`.
- Gauss — the quadratic Gauss sum sign law.

## Still open

- `χ(H) = 9`. Evidence against is accumulating; no proof either way.
- Five certificates, causes unknown.
- Whether the FS/KO alignment survives contact with the repo's actual spectral-triple
  construction.
