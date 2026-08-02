# Passes 2467–2472 — `C₅` is the end of the road, and `73` is probably nothing

---

## Pass 2468 — `5:4` does **not** lift: the parallel track's step 5 is blocked

Their Pass 2434 escapes the central obstruction by restricting to `C₅`, and it works
because `C₅` has **odd** order — Schur–Zassenhaus splits the extension automatically.
Their step 5 proposes extending to the normaliser. My Pass 2466 computed that normaliser
to be exactly `5:4 = F₂₀` of order 20 — an **even** order, so the argument that made `C₅`
work no longer applies.

Computed in `Sp(4,3)` directly:

```text
|Sp(4,3)| = 51840          |Z(Sp(4,3))| = 2
|C5| = 5    |N_Sp(C5)| = 40    structure  C5 : C8      z in N : true

subgroups of N of order 20 meeting <z> trivially :  0
```

> **`N_{Sp(4,3)}(C₅) = C₅:C₈`, a non-split extension. Every order-20 subgroup of the
> preimage contains `z`. So `5:4` does not lift, and the central obstruction returns the
> moment we leave odd order.**

The mechanism is clean: the `C₄` in `U₄(2)` lifts to a `C₈` in `Sp(4,3)`, whose **unique**
involution *is* `z`. Any subgroup of order 20 must contain the `C₄ ⊂ C₈`, and that `C₄`
contains `z`.

And `C₅` cannot be enlarged within odd order either: `N/C` embeds in `Aut(C₅) = C₄`, and
`F₂₀` acts faithfully, so `C_{U₄(2)}(C₅) = C₅`. There is no element of order 3 commuting
with `C₅`, hence no subgroup of order 15 or 45 containing it.

> **`C₅` is maximal among odd-order subgroups containing it, and the even extension does
> not lift. Their 144-dimensional Hom space is therefore optimal — it cannot be cut
> equivariantly by the normaliser, and there is nothing between `C₅` and the obstruction.**

This is a negative result *for their step 5 as posed*, and it saves the attempt.

---

## Pass 2467 — the chiral carrier has **no invariant pairing** at `q ≡ 3 (mod 4)`

Pass 2462 found FS indicator `0` at `q ≡ 3` and `−1` at `q ≡ 1`. Those are not two
flavours of one thing:

```text
2.U4(2)   q = 3   chiral degree  4   FS =  0
    dim (Sym^2 V)^G   = 0
    dim (Lambda^2 V)^G = 0        -> NOT self-dual: NO invariant bilinear form at all

2.S4(5)   q = 5   chiral degree 12   FS = -1
    dim (Sym^2 V)^G   = 0
    dim (Lambda^2 V)^G = 1        -> self-dual, one invariant ALTERNATING form
```

> **At `q ≡ 3 (mod 4)` the chiral carrier admits no invariant bilinear form whatsoever.
> At `q ≡ 1 (mod 4)` it admits exactly one, and it is symplectic.**

This bears directly on the parallel track's Pass 2301 (the 50-dimensional quadratic map
space). That space lives on the **90** — the achiral side. The chiral side at `q = 3` has
**no** quadratic invariant to build from, so the asymmetry between the two towers is not
only about intertwiners between them; it is about what can be built *within* each.

---

## Pass 2469 — certificate sweep of the parallel track's frozen data

```text
certificates with an embedded hash : 28    verified 28    MISMATCH 0
certificates with no hash field    : 14
frozen `checks` blocks containing any false : none
```

> **Every hashed certificate reproduces its own digest, and every frozen checks block is
> all-true.** The Pass 2304 stale-hash defect found earlier in the session is repaired
> and has not recurred.

Recorded because six separate times in this repo a question was "open" while its answer
sat in a committed certificate. The certificates are currently trustworthy.

---

## Pass 2470 — the whole chirality stack fits on one UP5K

```text
w33_c6_fibre           ICESTORM_LC   9/5280    SB_IO 9/96
w33_s3_fibre           ICESTORM_LC   8/5280    SB_IO 9/96
w33_orientation_probe  ICESTORM_LC   4/5280    SB_IO 5/96
w33_chirality_modulator (Pass 2464)  73/5280   SB_IO 27/96   93.40 MHz
```

All four place and route on `--up5k --package sg48`. Combined: **94 of 5280 logic cells,
1.8% of the fabric**, leaving the rest free. A single-chip demonstrator of the whole
chirality result is now a routing problem that is already solved rather than a plan.

*(The fibre controllers report no `Fmax` because they are combinational.)*

---

## Pass 2471 — `73` is probably an artifact, not a structure

Probing the parallel track's Pass 2432 sub-counts — the nine signature fibre sizes:

```text
   288 = 2^5 * 3^2
   864 = 2^5 * 3^3
  2808 = 2^3 * 3^3 * 13
 11664 = 2^4 * 3^6
 total = 42912 = 2^5 * 3^2 * 149

73 in any fibre size ?   FALSE
73 in their total    ?   FALSE
73 | 3547800 (all covers) ?  TRUE
```

> **`73` is absent from every local count and appears only in the global total. And the
> sibling counts pick up sporadic primes just as freely — `2808` carries a `13`, their
> 42,912 carries a `149`.**

Large exact-cover counts routinely acquire primes with no group-theoretic meaning. That
is what `73` looks like.

**Not settled.** This downgrades the mystery from "unexplained structural prime" to
"probably an ordinary artifact", on evidence, not proof. The decisive test is still the
actual `G`-orbit count on covers, which needs the frozen bitsets.

---

## Pass 2472 — ledger

| claim | discharged by | status |
|---|---|---|
| `5:4` does not lift to `Sp(4,3)` | `N = C₅:C₈`, 0 complements of order 20 | proved |
| `C₅` maximal among odd-order subgroups | `C(C₅) = C₅` since `F₂₀` acts faithfully | proved |
| their 144 cannot be cut by the normaliser | the two above | proved |
| chiral carrier has no invariant form at `q ≡ 3` | `Sym²` and `Λ²` invariants both 0 | computed |
| 28 certificates self-consistent | recomputed digests | verified |
| four designs route on one UP5K | nextpnr-ice40 | measured |
| `73` is structural | — | **downgraded to "probably artifact"** |

---

## Prior art

- Pass 2434 (parallel track) — **owns** the `C₅` restriction and the 144. Pass 2466
  confirmed it independently; Pass 2468 shows it is optimal.
- Pass 2432 (parallel track) — the nine-signature fibre sizes probed here.
- Pass 2079 (mine) — the eight pentagons their `C₅` argument runs through.
- Schur–Zassenhaus — why odd order lifts.

## Still open

- `χ(H) = 9`.
- The actual `G`-orbit count on covers, which would settle `73` outright.
- Whether the chirality/contextuality alignment (Pass 2451) has a mechanism.
- Whether the missing invariant pairing at `q ≡ 3` blocks any specific construction, or
  is only an absence.
