# Passes 1944–1948 — the flux reading fails its own test, and the physical sector is colourless

Five items. The first is a negative against my own physics from last batch, found
by testing it the way it should be tested.

---

## Pass 1944 (physics) — no integral torsion, so the Dirac reading is **not supported**

Pass 1934 read the `ℤ₆` as a flux quantum and leaned on Dirac duality to reach
charge in thirds. A Dirac quantum is a *topological* statement, so it should be
visible integrally — as torsion in the chain complex, not only in a character
field. Testing that by comparing ranks over `ℚ` and over small primes:

```text
map            rank_Q  rank_F2  rank_F3  rank_F5   torsion primes
d1 (E->V)          39       39       39       39   none
d2 (T->E)         120      120      120      120   none
d3 (Tet->T)        40       40       40       40   none

torsion primes in the whole complex : NONE
```

**Every boundary map has the same rank over every field.** The clique complex is
torsion-free, so there is no `ℤ/3`, no `ℤ/6`, and nothing for a flux quantum to be.

> **The `ℤ₆` is not a homological flux quantum.** It is the unit group of
> `End_PSp(90)`, an endomorphism-ring fact about one representation — not a
> topological quantization of the complex.

Pass 1934's Dirac framing is therefore withdrawn. What survives from Passes
1933–1935 is narrower and still true: exactly one block has a non-rational
character field, that field is `ℚ(ω)`, its integral units are `ℤ₆`, and the `ℤ₆`
is internal. What does *not* survive is the inference from there to flux
quantization and thence to charge, because the object that would carry it is
absent.

This is the second physics reading in two batches to be corrected by its own
test — Pass 1934 corrected Pass 1933's sector, and Pass 1944 now removes the
mechanism both were using. The remaining claim is a representation-theoretic one,
and should be stated as such.

---

## Pass 1945 (physics) — the physical sector is colourless as well as neutral

`V` is multiplicity-free, so its endomorphism ring splits over the blocks:

```text
dim_R End_PSp(V) = 6
   degree 15 : FS 1 -> R      degree 24 : FS 1 -> R
   degree 30 : FS 1 -> R      degree 81 : FS 1 -> R
   degree 45 + 45 : FS 0 -> C
=> End_PSp(V) = R x R x R x R x C
```

The `ℤ₆ = ℤ[ω]^×` lives in the `ℂ` factor **alone**. The only finite units of `ℝ`
are `±1`, and `ω` has order 3, so `ω` acts as the identity on the 15, 24, 30 and
81.

> **The `ℤ₃` touches only the flux sector. The physical sector 81 is colourless
> as well as neutral** (Pass 1936 gave neutrality by parity; this gives
> colourlessness by the endomorphism split).

Two structural predictions about the same sector, from two independent
mechanisms, and neither is a fit.

---

## Pass 1947 — why only the curvature sector is non-rational

The asymmetry noted last batch has a one-line reason:

```text
C_0 = 40 points     : 0-cells carry NO orientation -> a permutation module -> REAL
C_2 = 160 triangles : 2-cells DO carry an orientation -> a signed module -> may be COMPLEX
```

The exact block is `im(d₁ᵀ)`, built from unoriented 0-cells, so it sits inside a
real module and must be rational. The coexact block is built from **oriented**
2-cells and is under no such constraint. That is Pass 1909's "a phase requires
orientation" applied one degree up, and it explains why gradients are rational
while curvature is not.

---

## Pass 1946 — clique pinning beats value precedence by 70×, and the geometric test failed *again*

Pass 1938 showed dropping the pinned clique is expensive. The sound alternative to
pinning is **value precedence** — require the first occurrence of colour `c` to
precede that of `c+1` — which removes the `9!` colour symmetry without pinning
anything, and so is compatible with variable symmetry.

```text
clique pinned, spread branching (Pass 1892) :    60,909 branches
value precedence, spread branching          : 4,230,684 branches, UNKNOWN
```

> Pinning one clique is worth about **70×** more than value precedence, even
> though both remove the same `9!`.

**And the geometric lex constraints were vacuous again.** I wrote
`x[i] ≤ x[g[i]] + 8` over a domain of `0..8`, which is true for every assignment.
That is the **third** run in which I have reported on geometric symmetry breaking
without actually imposing it. The measurement above is sound and is about colour
symmetry alone; the geometric combination remains **untested**, and I am recording
that rather than letting a third vacuous run stand as evidence.

---

## Pass 1948 — the `240 = 6 × 40` fibration is already ours

The `ℤ₆` invited a connection to the six-fold fibration of the `E₈` roots. It is
in the corpus, and owned:

- `analysis/w33_e8_eisenstein_witting_weld.py` — "E8 roots, Coxeter order 30,
  `C^10` order-3 omega triangles, `C^5` 40 hexagons, W(3,3) rays"
- BT1745–BT1751 — "The E8 `C^5` hexagons form 40 Witting-ray hexagons."

So the `240 → 40` six-fold structure is **BT1745–1751's**, built from the
Coxeter element's `C^5` (order 6). My `ℤ₆` is a different construction — the unit
group of an endomorphism ring, not a power of a Coxeter element. Both are
order-6 and both are Eisenstein-flavoured, which is suggestive and **not
verified**: no map between them is exhibited here, and the connection is recorded
as an open question rather than a result.

Found by grepping for the *result* (`Eisenstein unit`, `6:1`), which is now the
default first move.

---

## Prior art

- BT1745–BT1751 — **own** the `E₈` `C^5` hexagon fibration onto the 40 rays.
- Pass 1933/1934/1935 — the readings this pass narrows.
- Pass 1909 — "a phase requires orientation", which Pass 1947 extends to 2-cells.
- Pass 1892/1938 — the encodings Pass 1946 measures against.

## Still open

- What the `ℤ₆` *is* physically, now that flux is ruled out. It is a real internal
  symmetry of one block; that is all this arc currently supports.
- Whether the endomorphism `ℤ₆` and the Coxeter `C^5` hexagon `ℤ₆` are the same.
- `χ(H) = 9`, and a geometric symmetry break that is actually imposed.
