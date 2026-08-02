# Passes 2454–2459 — there are **two** `i`s, one per doubling, and the Weil straddle holds for every odd `q`

---

## Pass 2454 — the two-`i` incompatibility **is** the central character

Pass 2448 found the Weil representation of `Sp(4,3)` splits `9 = 4 + 5` with the halves
on opposite sides of the centre, both complex. So there are **two** complex structures,
one per doubling. Are they identifiable?

```text
Frobenius-Schur indicators (0 = genuinely complex, admits an i)
   degree 4 (faithful, CHIRAL side)  : [0, 0]
   degree 5 (inflated, ACHIRAL side) : [0, 0]

<chi_4, chi_5> = 0   for all four pairs     central characters  -1  vs  +1
```

> **Each half carries a genuine `i`, and the two live in orthogonal isotypic sectors.**

That is my Pass 2076 two-`i` incompatibility, but derived from the central character
rather than constructed by hand from `σ_S`. The "geometric `i`" and the
"representation `i`" are not two descriptions of one object competing for the same
carrier — they are **the `i`s of the two doublings**, and they cannot be identified for
the same reason `Hom = 0` (Pass 2443).

---

## Pass 2455 — arithmetic constraints on a 9-partition, and an unexplained prime

Independent re-derivation of the parallel track's numbers from the incidence structure
alone:

```text
frames 540, nine-cliques 240, cover size 60
cliques per frame       : 240*9/540 = 4
60 frames x 4 cliques   = 240        the cover is exact
covers through one frame: 3547800*60/540 = 394200
their Pass 2412 measured: 394200                   MATCH
double counting back    : 394200*540/60 = 3547800  MATCH
```

Their 394,200 is confirmed from a completely different direction. Then:

```text
|G|               = 51840   = 2^7 * 3^4 * 5
covers            = 3547800 = 2^3 * 3^5 * 5^2 * 73
through one frame = 394200  = 2^3 * 3^3 * 5^2 * 73
3547800 / |G|     = 68.4375   NOT an integer
```

Two consequences:

1. The cover set is **not** a union of regular orbits — some cover has a nontrivial
   stabiliser.
2. > **`73` divides the cover count but divides none of `|G|`, 540, 240, or 60.**
   Every `G`-orbit size divides `|G|`, so no orbit is `73`-divisible; the 73 can only
   arise from *how many* orbits there are. **Unexplained**, and flagged rather than
   explained.

Combined with Pass 2450 (no equivariant 9-colouring), any 9-partition lies in a
`G`-orbit of size at least 2, so the number of 9-partitions is even at minimum. **Not a
refutation.** Counting alone does not close `χ(H) = 9`.

---

## Pass 2456 — no single 240 carries both towers, and a correction to my own Pass 2444

The decisive argument needs no search. Pass 2436 measured how the central element `z`
acts on each 240:

```text
E8 roots       : z = -1 is the ANTIPODAL map -- fixed-point-free, order 2
dual codewords : z acts TRIVIALLY (the action factors through U4(2).2, which omits z)
```

> **A single permutation action cannot have `z` act both fixed-point-freely and
> trivially. So no 240-set carries both towers**, inside `2.U₄(2).2` or anywhere else.

### Correction to Pass 2444's framing

```text
|2.U4(2)|   = 51840     central doubling -- a SUBGROUP of 2.U4(2).2
|2.U4(2).2| = 103680
|U4(2).2|   = 51840     outer doubling
```

`2.U₄(2).2 / ⟨z⟩ = U₄(2).2`, so the outer doubling is a **quotient** of the big group,
not automatically a subgroup. Saying the two doublings "both sit inside `2.U₄(2).2`" —
which I wrote in Pass 2449 — was loose: one is a subgroup, the other a quotient. The
Pass 2449 *result* is unaffected (inducing the faithful degree-4s into `2.U₄(2).2` is a
statement about the subgroup, which is correct), but the phrase "both doublings inside
one group" should not be repeated.

Whether `U₄(2).2` also **embeds** — whether the extension splits — is **not settled
here.** The check I ran (25 trivially-central irreducibles of `2.U₄(2).2` versus 25
irreducibles of `U₄(2).2`) only confirms the quotient relation, which is automatic and
tests nothing. Recorded as open rather than as a result.

---

## Pass 2457 — the periodic/growing split as a modulator, SAT-proved

The `A`-sector has period exactly 2 and the `BC`-pair grows like `φⁿ`. As a control
path that is a **chirality modulator**: a one-bit select line that alternates every
cycle, driving a two-path switch, plus a Fibonacci-scaled amplitude word.

Pass 2449 justifies the reading: the outer involution exchanges the two chiralities of
the `E₈` carrier, so an alternating one-bit select is the natural control for a two-path
chirality switch.

```text
Solving problem with 1506 variables and 4225 clauses..
SAT proof finished - no model found: SUCCESS!
```

Proved over all inputs in range: `a2 == a0` (period exactly 2), the **sign bit flips
every cycle** unless the seed is zero, and `c2 == c1 + c0`, `c3 == c2 + c1` — the
Fibonacci recursion. The sequential modulator synthesises to **230 cells** on iCE40.

**Scope:** this is a control path with proved invariants, not an optical model. No claim
about photonic implementability is made.

---

## Pass 2458 — the Weil straddle is a **theorem for every odd `q`**

The `q = 3` split `9 = 4 + 5` is not an accident, and it does not need a table.

The Weil representation of `Sp(2n,q)` acts on functions on `𝔽_qⁿ`, and the central
element `−I` acts by `f(x) ↦ f(−x)`. Therefore:

```text
even part, degree (q^n + 1)/2  :  z -> +1   INFLATED   achiral side
odd  part, degree (q^n - 1)/2  :  z -> -1   FAITHFUL   chiral  side
```

> **The parity split of the Weil representation IS the central-character split, for
> every odd `q`.** The oscillator representation always straddles the two doublings.

Classical Weil theory — **cited, not claimed**. Verified against the stored tables:

```text
q = 3   2.U4(2)   degree 4  faithful TRUE (2 of them)   degree 5  inflated TRUE (2)
q = 5   2.S4(5)   degree 12 faithful TRUE (2 of them)   degree 13 inflated TRUE (2)
q = 7   2.S4(7)   table unavailable -- predicted by the proof, not measured
```

This is the family statement Pass 2447 said the *fibre* census could not have. The
fibre census is `q = 3`-specific; the **Weil straddle is not**.

---

## Pass 2459 — ledger

| claim | discharged by | status |
|---|---|---|
| two `i`s, orthogonal isotypic sectors | FS indicators + `⟨χ₄,χ₅⟩ = 0` | proved |
| 394,200 covers through a frame | independent incidence count | confirms theirs |
| `73 ∣` cover count, `73 ∤ |G|` | factorisation | **unexplained** |
| no 240 carries both towers | `z` fixed-point-free vs trivial | proved |
| `U₄(2).2` embeds in `2.U₄(2).2`? | — | **open, not tested** |
| modulator period 2 + Fibonacci | Yosys SAT, 1506 vars / 4225 clauses | proved |
| Weil straddle for all odd `q` | classical + `q = 3, 5` instances | cited + verified |

---

## Prior art

- Weil representation parity split and the action of `−I` — classical.
- Pass 2412 (parallel track) — the 3,547,800 / 394,200 cover census, re-derived here.
- Pass 2414 (parallel track) — the central-character obstruction.
- Passes 2436–2453 (mine) — the doubling split these build on.
- Pass 2076 (mine) — the two-`i` incompatibility, now re-derived from central characters.

## Still open

- `χ(H) = 9`. Counting does not refute it. Still needs the frozen cover bitsets.
- **Why 73.** It divides the cover count and nothing else in sight.
- Whether the outer doubling embeds in `2.U₄(2).2`, i.e. whether the extension splits.
- Whether the chirality/contextuality alignment (Pass 2451) has a mechanism. No progress.
