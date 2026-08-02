# Passes 2460–2465 — the two `i`s are **not twins**, and the doublings cannot share a group

---

## Pass 2461 — `U₄(2).2` does **not** embed in `2.U₄(2).2`

Pass 2456 left this open. It closes cleanly.

```text
|2.U4(2).2| = 103680     |2.U4(2)| = 51840     |U4(2).2| = 51840
linear characters :  2.U4(2)   1   -> PERFECT
                     U4(2).2   2   -> not perfect
                   2.U4(2).2   2   -> abelianisation of order 2
```

A subgroup `H ≤ G = 2.U₄(2).2` with `|H| = 51840` and `H ∩ ⟨z⟩ = 1` satisfies
`|H|·|⟨z⟩| = |G|` with `⟨z⟩` central, so `G = H × ⟨z⟩` — a **direct product**. If
`H ≅ U₄(2).2` then `G^ab = C₂ × C₂`, of order 4.

But `G^ab` has order **2**. There is exactly **one** index-2 subgroup, and it is the
perfect `2.U₄(2)`.

> **Contradiction. The extension does not split, and the outer doubling does not embed
> in the big group.**

Combined with Pass 2456 (no 240-set carries both towers), the two doublings are separated
at every level available: no common carrier, and no common ambient group holding both as
subgroups. One is a subgroup of `2.U₄(2).2`; the other is only its quotient.

---

## Pass 2462 — the two `i`s have **different existence conditions**

Pass 2454 found both Weil halves complex at `q = 3` and called them "two `i`s". Are they
the same kind of object? Frobenius–Schur indicators, by `q mod 4`:

```text
q = 3   (q = 3 mod 4)
   CHIRAL  half, degree  4 : real ? [false, false]   FS indicator [ 0,  0]
   ACHIRAL half, degree  5 : real ? [false, false]   FS indicator [ 0,  0]

q = 5   (q = 1 mod 4)
   CHIRAL  half, degree 12 : real ? [true,  true ]   FS indicator [-1, -1]
   ACHIRAL half, degree 13 : real ? [true,  true ]   FS indicator [+1, +1]
```

> **At `q ≡ 3 (mod 4)` both halves are genuinely complex (indicator 0) — two `i`s.
> At `q ≡ 1 (mod 4)` the chiral half goes QUATERNIONIC (indicator `−1`) and the achiral
> half goes ORTHOGONAL (indicator `+1`).**

The three Frobenius–Schur types land on the two halves differently, and only the
`q ≡ 1 (mod 4)` case separates them:

| | chiral (faithful, odd) | achiral (inflated, even) |
|---|---|---|
| `q ≡ 3 (mod 4)` | complex, `0` | complex, `0` |
| `q ≡ 1 (mod 4)` | **quaternionic, `−1`** | **orthogonal, `+1`** |

Indicator `−1` means an invariant **symplectic** form and a genuine `j` with `j² = −1`;
indicator `+1` means an invariant symmetric form and no such structure.

> **The chiral half carries a `j` with `j² = −1` at every odd `q` — complex at
> `q ≡ 3`, quaternionic at `q ≡ 1`. The achiral half has it only at `q ≡ 3 (mod 4)`;
> at `q ≡ 1` it is plainly real.**

This sharpens my Pass 2081, which said `q = 5` is "a substrate with an obstruction and no
phase to lose". Correct for the **achiral** side. The chiral side still has its `j` at
`q = 5` — it is quaternionic rather than absent.

**Scope.** Frobenius–Schur indicators of Weil representations are **classical** (Gow;
Prasad; Thiem–Vinroot) and are cited, not claimed. What this pass adds is the mapping of
those known indicators onto the chiral/achiral doubling split of Passes 2444–2448, which
is a statement about objects that classical Weil theory does not organise this way.

---

## Pass 2460 — why 73: searched, not found, not promoted

```text
covers            3547800 = 2^3 * 3^5 * 5^2 * 73
covers per frame   394200 = 2^3 * 3^3 * 5^2 * 73
|G|                 51840 = 2^7 * 3^4 * 5              73 does not divide it
73 divides 540? no    240? no    60? no
```

Every `G`-orbit size divides `|G|`, so no orbit is `73`-divisible; the 73 can only come
from **how many** orbits there are. The orbit-size constraint gives
`gcd(3547800, 51840) = 3240`, and the natural uniform structures would be:

```text
s = 3240  ->  1095 orbits, stabiliser order 16
s = 1620  ->  2190 orbits, stabiliser order 32
```

with `1095 = 3 · 5 · 73`. So the 73 would sit in the **orbit count**, not in any orbit.

Corpus search for 73 as a result: **negative** — every hit is a pass number or a date.

Count matches found and **rejected** by the repo's own rule (a count match is not a link
unless a map is named):

- `|PG(2,8)| = 64 + 8 + 1 = 73`, the projective plane of order 8. No map to `W(3,3)`.
- `2⁹ − 1 = 511 = 7 × 73`. No map.

> **Verdict: `73` is unexplained. Recorded as an open number, not a connection.**

---

## Pass 2464 — the modulator reaches place-and-route with timing closure

First design in this project to complete the full flow.

```text
synth_ice40, W = 12, then nextpnr-ice40 --up5k --package sg48

Device utilisation:
        ICESTORM_LC:      73/  5280     1%
              SB_IO:      27/    96    28%
Max frequency for clock 'clk': 93.40 MHz  (PASS at 12.00 MHz)
Max delay <async> -> posedge clk : 8.06 ns
Routing complete.
```

The parallel track's 36-lane mixer could not be placed because its interface exposes 432
pins; this design exposes 27 and fits with 99% of the fabric free. Combined with the
Pass 2457 SAT proof (1506 vars / 4225 clauses), the chirality modulator is **proved and
routable**.

### One coincidence, flagged and rejected

The design happens to use **73** logic cells, and `73` is the unexplained prime of
Pass 2460. This is meaningless: a synthesised cell count depends on the tool version and
on the parameter `W`, and changing `W` changes it. Recorded here only because failing to
flag it is exactly how a count match becomes a false claim.

---

## Pass 2465 — ledger

| claim | discharged by | status |
|---|---|---|
| `U₄(2).2` does not embed in `2.U₄(2).2` | `G^ab` has order 2, not 4 | proved |
| chiral half is quaternionic at `q ≡ 1 (mod 4)` | FS indicator `−1`, `2.S4(5)` | verified (classical) |
| achiral half is orthogonal at `q ≡ 1 (mod 4)` | FS indicator `+1` | verified (classical) |
| both complex at `q ≡ 3 (mod 4)` | FS indicator `0`, `2.U4(2)` | verified |
| 73 explained | — | **no; open** |
| modulator routes at 93.40 MHz | nextpnr-ice40, UP5K | measured |
| 73 logic cells means anything | — | **rejected as a count match** |

---

## Prior art

- Frobenius–Schur indicators of Weil representations — classical (Gow 1985; Prasad;
  Thiem–Vinroot). Cited, not claimed.
- Pass 2412 (parallel track) — the cover census whose 73 is examined here.
- Pass 2456/2458 (mine) — the open embedding question and the all-`q` straddle.
- Pass 2081 (mine) — "`q = 5` has no phase to lose", now sharpened to the achiral side only.

## Still open

- **Why 73.** Corpus-negative, structurally unlocated. The cheapest remaining probe is
  the actual orbit count of `G` on covers, which needs the frozen bitsets.
- `χ(H) = 9` itself.
- Whether the chirality/contextuality alignment (Pass 2451) has a mechanism.
