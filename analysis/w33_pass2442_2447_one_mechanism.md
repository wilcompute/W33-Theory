# Passes 2442–2447 — three results were one mechanism, and it is the **central character**

Three findings landed independently this week, in different objects and different
languages. They are the same statement.

---

## Pass 2442 — the chiral tower sits over the **contextual** side

Passes 2436–2441 split the two 6:1 towers over 40 by fibre group. The corpus already
holds a *different* distinction of the same two 40s —
`analysis/w33_pass1021_corollary_ovoid_orientation.py`:

```text
W(3,3) = (36 spreads,  0 ovoids)      Q(4,3) = (0 spreads, 36 ovoids)
"W(q) is contextual iff q is odd, because an ovoid -- a Kochen-Specker 0/1
 assignment satisfying every context -- exists iff q is even."   (Thas)
```

Independently recounted here, not taken from the prose:

```text
W(3,3) point graph  SRG(40,12,2,4)   ovoids  0    max partial ovoid  7
Q(4,3) point graph  SRG(40,12,2,4)   ovoids 36    max partial ovoid 10
```

Laying the two distinctions side by side:

| side | ovoids | KS-colourable | fibre | quotient | |
|---|---:|---|---|---|---|
| `W(3,3)` points | 0 | **no** | `C₆` | `C₃` | **CHIRAL** |
| `Q(4,3)` points | 36 | yes | `S₃` | `S₃` | achiral |

> **They agree. The chiral tower sits over the side with no ovoid — the
> Kochen–Specker *uncolourable*, contextual side. The achiral tower sits over the
> colourable one.**

Certificate `data/w33_pass2442_chirality_meets_contextuality.json`, 6/6 checks.

**Scope.** The prior file uses "orientation" for *which side of the duality*; this pass
uses it for the `C₃` cyclic order *inside a fibre*. Different senses, kept apart. This
pass claims the alignment of two known distinctions, not either distinction.

---

## Pass 2443 — one mechanism: whether the central involution is **spent**

```text
my Pass 2436     antipode INSIDE the root-side C6 (-1 is an Eisenstein unit),
                 OUTSIDE the line-side S3 (PGSp acts by permutation matrices,
                 and -I is not a permutation matrix)
their Pass 2414  Hom_{2.U4(2)}(8, 90) = 0 -- the central involution acts as -I on
                 the E8 carrier and +I on the coexact 90: OPPOSITE CENTRAL CHARACTERS
their Pass 2307  the quadratic map space is an S3-module because the order-six phase's
                 central sign "acts twice on a bilinear map", so C3:C2 = S3
```

Let `z` be the central involution of the order-6 phase. It has exactly two options:

```text
z -> -1   z is SPENT on the antipode.  The quotient by z is C3 alone -- an
          ORIENTATION.                                              CHIRAL
z -> +1   z is FREE.  It survives as an independent involution, acts on the C3
          by inversion, and gives S3 -- reflections.                ACHIRAL
```

Measured in `2.U₄(2)`:

```text
|2.U4(2)| = 51840        |U4(2)| = 25920      central class: order 2, size 1
z -> +I (inflated, trivial central character) : 20 irreducibles
        degrees [1,5,5,6,10,10,15,15,20,24,30,30,30,40,40,45,45,60,64,81]
z -> -I (faithful, central character the sign): 14 irreducibles
        degrees [4,4,20,20,20,20,20,36,36,60,60,60,64,80]
every irreducible lies in exactly one class : true
```

The obstruction is one line: if `χ(z) = −χ(1)` and `ψ(z) = +ψ(1)`, then substituting
`g → zg` in `⟨χ,ψ⟩` negates every summand, so `⟨χ,ψ⟩ = −⟨χ,ψ⟩ = 0`. **Hom vanishes for
every pair with opposite central characters**, hence for every subgroup whose preimage
contains `z` — which is their Pass 2414, and it is the *same* fact as the antipode
being inside one fibre group and outside the other.

### A correction to the framing (not the conclusion)

`90` is **not** an irreducible of `U₄(2)` — the degree list above has no 90, and `45`
appears **twice**. The coexact 90 is `45 + 45`, which is exactly the pair my Pass 2076
found `σ_S` swapping. Their Hom-vanishing conclusion is unaffected: both degree-45
constituents have trivial central character, so both are orthogonal to the faithful
`E₈` carrier. The `E₈` carrier itself is `4 + 4` — the two faithful degree-4s, which is
what `χ₂₁ + χ₂₂` means.

---

## Pass 2444 — the two towers **are** the two groups of order 51840

```text
|2.U4(2)| = Sp(4,3)    = 51840      centre of order 2
|U4(2).2| = PGSp(4,3)  = 51840      centre trivial
same order : true          isomorphic : FALSE
```

> **`U₄(2) ≅ PSp(4,3)` has order 25920 and is doubled in two different ways. The
> central doubling `Sp(4,3)` carries the `E₈` tower and is CHIRAL. The outer doubling
> `PGSp(4,3) = W(E₆)` carries the codeword tower and is ACHIRAL. They have the same
> order and are not isomorphic.**

This gives the repo's long-standing `51840 = 51840` coincidence a structural reading: it
is not a coincidence between `W(E₆)` and a symplectic group, it is **one simple group
doubled twice**, and the two doublings are precisely the two towers. The involution that
decides chirality is *central* in one and *outer* in the other.

It also re-reads the closed selection layer (Pass 346, `T` with `det = −1` swaps `S±`):
the substrate does not fail to select a handedness by accident — it hosts both doublings,
and a handedness would require choosing between two groups of equal order that the
substrate treats symmetrically.

---

## Pass 2445 — ledger audit, exact arithmetic

Every claim in the previous batch that was decided with floating-point roots, re-decided
with exact algebraic comparison (`sympy`, `all_roots`, symbolic `ρ − 1 > 0`):

```text
distinct char polys                27
EXACTLY hyperbolic (rho > 1)       22   claimed 22   OK
  irreducible                      16   claimed 16   OK
  reducible                         6   claimed  6   OK
words with rho EXACTLY phi          2   at lengths [3, 3]
shortest reducible word length      3   phi at 3     phi IS shortest: True
quadratic fields among reducible    sqrt(5), 2*sqrt(2)
R4^2 U6 char poly                   (t + 1)(t^2 - t - 1)
quotient on Z^3/<(1,0,0)>           [[0,-1],[-1,1]]  det -1  trace 1
Fibonacci [[1,1],[1,0]]             det -1  trace 1        match: True
```

**All survive.** The float-based counts were right.

### One error the audit did catch, in this batch

Pass 2442's first run reported the maximum partial ovoid of `W(3,3)` as **6**,
contradicting the prior file's **7**. The prior file was right: my `best` tracker sat
inside a branch that prunes anything unable to reach size 10, so it under-reported the
independence number. Recomputed without the size-target prune: **7**, and `Q(4,3)`
gives **10**. Fixed before publication. *A disagreement with the corpus is a bug in the
new code until proved otherwise* — that is the fourth time that rule has paid.

---

## Pass 2446 — `χ(H) = 9`: attempted, blocked on data, stated precisely

Their Pass 2412 makes the problem sharply finite: **394,200 covers contain frame 0**,
3,547,800 global covers, and what remains is to choose one first cover plus eight
pairwise frame-disjoint global covers whose union is all 540 frames.

The frozen enumeration is a **47,304,008-byte binary**
(`f1180c87d3bada9d2ee14ae1b5ca7f4ec5e1ccc5d19946dd8146850511d3c491`) which is **not in
the working tree** — `data/` holds only the 2,133-byte summary
`w33_pass2412_proof_producing_nine_colour_search.json`. Re-enumerating it costs
477 million search nodes and ~508 seconds, which is affordable, but the meet-in-the-middle
packing over 394,200 × 3,547,800 is the part that needs their frozen bitsets to be
worth attempting rather than re-deriving.

**Not attempted this pass.** What would unblock it: commit the frozen cover bitsets (or
a regenerator with a fixed seed), and the disjointness graph can be built directly.

---

## Pass 2447 — scope: what generalises in `q` and what does not

Honest accounting, because the previous batch listed a `q = 5, 7` fibre census as a next
step and it does not exist as posed:

- **Does not generalise.** The `C₆`/`S₃` fibre census is `q = 3`-specific. It depends on
  the 240 `E₈` roots fibring 6:1 over the 40 points, and there is no `E₈` tower at
  `q = 5` (156 points) or `q = 7`. There is no `q`-general version of *that* computation.
- **Does generalise.** The central-character principle: `PSp(4,q)` has the double cover
  `Sp(4,q)` for **every odd `q`**, so a central involution exists and the spent/free
  dichotomy is available at every odd `q`.
- **Already classical.** `W(q)` has ovoids iff `q` is even (Thas), so the
  contextual/colourable split holds at every odd `q` and must be **cited, not
  re-derived** — re-measuring it at `q = 5` would be exactly the rediscovery this repo
  is built to avoid.

---

## Prior art

- `analysis/w33_pass1021_corollary_ovoid_orientation.py` — **owns** the `(36,0)/(0,36)`
  spread/ovoid duality count and the contextuality reading. Pass 2442 aligns against it.
- Thas — `W(q)` has ovoids iff `q` is even.
- Pass 2414 (parallel track) — **owns** the `Hom = 0` central-character obstruction.
  Pass 2443 shows it is the same fact as my antipode dichotomy and corrects only the
  irreducibility of the 90.
- Pass 2307 (parallel track) — **owns** the quadratic `S₃`-module decomposition.
- Pass 2412 (parallel track) — **owns** the 394,200-cover enumeration.
- Passes 2436–2441 (mine) — the `C₆`/`S₃` fibre split these passes build on.
- `Sp(4,3) ≇ PGSp(4,3)`, both of order 51840 — classical; the reading as *the two
  towers* is what Pass 2444 adds.

## Still open

- `χ(H) = 9`. Blocked on the frozen cover bitsets, not on ideas.
- Whether the chirality/contextuality alignment is a theorem or a two-point coincidence.
  It rests on one `q`. The honest test is a family where both sides are computable and
  the fibre structure exists — which, per Pass 2447, this construction does not supply.
