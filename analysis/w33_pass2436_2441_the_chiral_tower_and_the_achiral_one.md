# Passes 2436–2441 — the substrate has **two** 240→40 towers, and only one of them is chiral

The parallel track's Pass 2308 found a second 6:1 fibration of a 240 over a 40. My
Pass 1021 owns the first. They have the same shape and **different fibre groups**, and
that difference is exactly an orientation.

---

## Pass 2436 — the two fibre groups are `C₆` and `S₃`, and the antipode sits differently

```text
Pass 1021 (mine)   : 240 E8 roots       -> 40 W(3,3) POINTS   fibre = Eisenstein units = C6
Pass 2308 (theirs) : 240 dual codewords -> 40 Q(4,3)  points   fibre = S3
                                              = W(3,3) LINES
```

Both fibre groups are **regular** on their 6-element fibre — both towers are torsors.
Both have order 6. `C₆` is abelian, `S₃` is not. Measured:

```text
code side : |G| = 51840, 40 fibres of 6, setwise stabiliser 1296, kernel 216
            induced group on the fibre : S3, order 6, regular
            antipodal map w -> -w      : order 2, fixed-point-free
            antipode IN the induced group ?  FALSE
            antipode CENTRALISES it ?        TRUE
            centre of the induced group :    trivial
```

The antipode being outside is **forced, not incidental**: `PGSp(4,3)` acts on the
codewords by *permutation* matrices, and `−I` is not a permutation matrix. On the root
side the group acts orthogonally and `−1` **is** an Eisenstein unit, so there the
antipode is *inside* the fibre group.

> **The antipode is inside the fibre group on the point side and outside it on the
> line side.**

---

## Pass 2437 — quotient by the antipode and the two towers separate

Each fibre has 3 antipodal pairs. What acts on those 3?

```text
POINT side (E8 roots)       C6 / <-1>  ->  C3   order 3, kernel 2
                            odd permutation (a reflection) present ?  FALSE
LINE  side (dual codewords) S3         ->  S3   order 6, faithful
                            odd permutation (a reflection) present ?  TRUE
```

> **The point-side fibre carries `C₃` — a cyclic order on three things, i.e. an
> ORIENTATION. The line-side fibre carries the full `S₃`, whose reflections destroy
> that orientation.**

The mechanism is the Pass 2436 observation: `C₆` **spends its involution on the
antipode**, so only `C₃` survives on the quotient; `S₃` still has its involutions free,
and they act as reflections.

And the two towers cannot be exchanged: **`W(q) ≅ Q(4,q)` iff `q` is even**, and `q = 3`
is odd — the parallel track measured the two 40-point graphs non-isomorphic despite both
being `SRG(40,12,2,4)`.

> **The chirality is confined to the point side. The reflection that would destroy it
> lives on the line side, inside the same group, and no duality of the substrate
> connects them.**

This is a new reading of the closed selection-layer result (Pass 346: chirality is
hostable but unselectable). The substrate does not merely *fail* to select a handedness —
it carries a chiral tower and an achiral tower simultaneously, over two non-isomorphic
bases.

### Prior art, cited not re-derived

`analysis/2026-05-30_c3_fano_triangle_orientation.md` already owns the **principle**
that `C₃ = A₄ ∩ S₃` inside `S₄ = PGL(2,3)` is "the cyclic rotation of the three
non-anchor points" — `C₃` vs `S₃` on three points **is** orientation vs none. That
reading is the repo's. What Passes 2436–2437 add is **which of the two 240→40 towers
carries which**, which is a statement about objects that did not exist when that file
was written.

---

## Pass 2438 — the bifurcation as hardware, simulated and SAT-proved

Encode a fibre element as `(p, s)`: `p ∈ {0,1,2}` the antipodal-pair index — the
**orientation register** — and `s ∈ {0,1}` the sign. Then the whole bifurcation is one
question about the involution:

```text
C6 antipode  :  (p,s) -> ( p, s^1)     orientation register UNTOUCHED
S3 reflection:  (p,s) -> (-p, s^1)     orientation register NEGATED mod 3
```

Built as `rtl/w33_pass2438_fibre_chirality.sv`, exhaustively simulated with Icarus 13.0
over every fibre element and every group element:

```text
Pass 2438 fibre chirality: C6 states 6, S3 states 6, errors 0
PASS  C6 antipode preserves orientation; S3 reflection reverses it
```

and proved over **all** inputs with Yosys 0.67 SAT:

```text
Solving problem with 375 variables and 1011 clauses..
SAT proof finished - no model found: SUCCESS!        (5/5 assertions)
```

Synthesised to iCE40:

```text
w33_c6_fibre          9 cells   (3 SB_CARRY, 6 SB_LUT4)
w33_s3_fibre          7 cells   (2 SB_CARRY, 5 SB_LUT4)
w33_orientation_probe 2 cells   (1 SB_CARRY, 1 SB_LUT4)
```

The probe collapses to 2 cells because **one of its two outputs is a constant**: Yosys
imported the `C₆` assertion as the literal `1'1`, i.e. it discharged
`c6_orientation_changed == 0` *structurally*, by constant propagation, before the solver
ran. The synthesis tool proves the point-side half of the theorem on its own; only the
line-side half needs logic.

**Scope:** this is a faithful hardware encoding of a proved group-theoretic fact, not
independent evidence for it. The cell counts compare two small controllers with
different port widths and are reported as measurements, not as an optimisation claim.

---

## Pass 2439 — `R₄²U₆` **is** the Fibonacci map (their Pass 2306's open question)

Their Pass 2306 states the open question directly: whether the golden word means
anything operationally. It does.

```text
M = R4^2 U6 = [[-1,0,0],[0,0,-1],[0,-1,1]]
char poly   = (t + 1)(t^2 - t - 1)
rational eigenvalue -1, primitive integer eigenvector (1,0,0)
induced action on Z^3 / <(1,0,0)>  =  [[0,-1],[-1,1]]
   det -1, trace 1, char poly t^2 - t - 1
Fibonacci matrix [[1,1],[1,0]] : det -1, trace 1, char poly t^2 - t - 1
```

`(1,0,0)` is the **A-sector** in their basis — the `V₉` inside the 24.

> **`R₄²U₆` negates the 24-sector and runs the Fibonacci recursion on the 90-sector.**
> Its orbits on the quotient grow like `φⁿ` and satisfy `a(n) = a(n−1) + a(n−2)`.

By contrast `R₄U₆` — their supergolden word — has **irreducible** characteristic
polynomial, so it preserves no rational line and does not descend. It is genuinely
3-dimensional.

---

## Pass 2440 — the dichotomy: reducible ⟺ invariant rational line ⟺ **quadratic** mean

Census of every word of length ≤ 7 in `⟨R₄,U₆⟩ = SL₃(ℤ)` — 27 distinct characteristic
polynomials, 22 with spectral radius > 1 (= 16 irreducible + 6 reducible; the two
finite-order words `rr` and `rR` read as 1.0000000051 and 1.0000065704 under a numeric
root-finder and must be excluded by hand -- they are exactly 1):

```text
IRREDUCIBLE (16)  -> acts irreducibly on Z^3 -> stays in SL3(Z) -> CUBIC mean
   t^3 - t   - 1    1.3247179572  len 3  ruu     plastic (smallest Pisot)
   t^3 - t^2 - 1    1.4655712319  len 2  ru      supergolden psi
   t^3 - t^2 - t -1 1.8392867552  len 5  ruruu   tribonacci

REDUCIBLE (6)     -> preserves a rational line -> descends to SL2(Z) -> QUADRATIC mean
   t^3 - 2t   - 1   1.6180339887  len 3  rru     GOLDEN phi        Q(sqrt5)
   t^3 + 2t^2 - 1   1.6180339887  len 3  rrU     GOLDEN phi        Q(sqrt5)
   t^3 - t^2 -3t -1 2.4142135624  len 7  rruruRu silver 1+sqrt2    Q(sqrt2)
   t^3 -4t^2 +4t -1 2.6180339887  len 6  rrurru  phi^2             Q(sqrt5)
```

> **A word is reducible exactly when it preserves a rational line; then it descends to
> `SL₂(ℤ)`, where the quadratic metallic means live. `φ` is the SHORTEST reducible word,
> at length 3 — the next reducible ones are at lengths 6 and 7.**

Every reducible word up to length 7 lands in `ℚ(√5)` or `ℚ(√2)`. Nothing else.

### This corrects my Pass 2107

Pass 2107 said "the three shortest words give the three smallest metallic constants."
**Wrong.** `φ` ranks 11th of 22 by size, and three growth rates in the ball
(`1.1510`, `1.2106`, `1.3562`) are smaller than the plastic number and are not named
constants. The real pattern is the reducibility dichotomy above, not an ordering by size.

---

## Pass 2441 — the two-`i` incompatibility, full-group, at `q = 7`

Their Pass 2302 proves the `D₄` relation objectwise for the canonical **Weil** family at
`q = 7, 11`, and says explicitly it does not cover the `q = 3` signed-edge 90. The
character-table half, for the **whole** group:

```text
q = 3   PSp(4,3) = U4(2) < U4(2).2      non-real irreds 10   FUSED 10/10
        degrees [5, 10, 30, 40, 45]
q = 5   PSp(4,5) < PSp(4,5).2           non-real irreds  0   (Gow control)
q = 7   PSp(4,7) < PSp(4,7).2           non-real irreds 18   FUSED 18/18
        degrees [25, 150, 900, 1050, 1200, 1225, 1600]
q = 11                                  ATLAS table unavailable
```

> **Every complex character is fused by the outer coset at `q = 3` and `q = 7`, not just
> the Weil constituents.** `q = 5` is the clean control: no complex characters exist, so
> there is no phase to lose.

Together with their Pass 2302 this closes both halves: they have the explicit `J`, `K`,
`KJK = −J` matrices for the Weil family; this has the full-group statement that nothing
complex survives the coset.

---

## Prior art

- Pass 2308 (parallel track) — **owns** the ternary dual code, the 240→120→40 tower, the
  `Q(4,3)` identification, and the `E₈`-root falsifier. Passes 2436–2437 read its objects
  and ask a different question of them.
- Pass 1021 (mine) — owns the `E₈`-root fibration and its `C₆` Eisenstein fibre.
- Passes 2051/1942/1953 (parallel track) — own `R₄`, `U₆`, `⟨R₄,U₆⟩ = SL₃(ℤ)`.
- Pass 2306 (parallel track) — poses the operational question Pass 2439 answers.
- Pass 2302 (parallel track) — owns the Weil-family `D₄` at `q = 7, 11`.
- `2026-05-30_c3_fano_triangle_orientation.md` — owns `C₃` vs `S₃` as orientation.
- `W(q) ≅ Q(4,q)` iff `q` even — classical (Payne–Thas).

## Still open

- `χ(H) = 9`. Their Pass 2412 has now made it sharply finite: choose one of the 394,200
  frozen first covers plus eight pairwise frame-disjoint global covers. Not attempted here.
- Whether the chiral/achiral split has any consequence for the closed selection layer,
  or is a restatement of it in new objects.
- The final ledger audit. Still not done — seventh report.
