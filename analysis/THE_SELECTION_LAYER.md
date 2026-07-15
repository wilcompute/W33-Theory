# The Selection Layer

**What this programme actually contributes, with every borrowed component cited.**

*Written at Pass 329, after Passes 322–328 audited the whole arc against the
corpus and the literature. It supersedes the framing of every earlier pass it
contradicts, including `W33_HONEST_SYNTHESIS.md`'s "two theorems that stand".*

---

## 0. The one-paragraph version

The W(3,3) programme's mathematical results are **not ours**. The incidence rank
law is published (Sastry–Sin; Chandler–Sin–Xiang) *and* was already proved in this
repository before the passes that re-derived it. The `[[40,10,4]]` CSS code and its
sentinel were already documented here, with a *stronger* structure theorem than we
produced. What is ours is one thing, and it is not a theorem: **an argument that
q=3 is forced rather than assumed.** It rests on two independent identifications,
both of which we can now state exactly — including exactly what blocks each.

---

## 1. What is borrowed, and from whom

| result | owner | where |
|---|---|---|
| `rank₂W(3,2ᵗ) = 1 + α₁ᵗ + α₂ᵗ` | **Sastry–Sin** | *The code of a regular generalized quadrangle of even order* |
| `rank₂W(3,q) = ½(q(q+1)²+2)`, odd q, **proved** | **this repo, 2026-07-10** | `analysis/2026-07-10_levi_next5.md` |
| `rank₂A_L = q²+1` (**= the CSS k**) | **this repo, 2026-07-10** | same, boxed |
| `rank_p`, defining characteristic; `det(B_p)` | **Chandler–Sin–Xiang** | *J. Algebra* **323** (2010) 3157–3181; [math/0603100](https://arxiv.org/abs/math/0603100), Thm 1.1 |
| `[[40,10,4]]`, `[40,15,8]` | **this repo, Passes 187/189** | `docs/index.html` (pre-Pass-224) |
| `F₂⁴⁰` uniserial `1\|14\|1\|8\|1\|14\|1`, `C⊥/C` forced | **Passes 187/189** | same — *stronger than ours* |
| 16/generation, three generations | **this repo** | `docs/index.html`, via trinification |
| Eastin–Knill; magic-state distillation | **standard QEC** | Eastin & Knill 2009 |

**CSX Theorem 1.1** deserves its own line, because it closed what we called our
last open problem:

> `rank_p = 1 + α₁ᵗ + α₂ᵗ`,  `α₁,α₂ = p(p+1)²/4 ± p(p+1)(p−1)√17/12`

At p=2 the αs **are** `(9±√17)/2`, the eigenvalues of the `B = [[4,2],[2,5]]` we
spent passes trying to explain. So `det(B_p) = −p²(p+1)²(2p²−13p+2)/36` (16, 76,
325 at p=2,3,5) and `Tr = p(p+1)²/2 = char₀(p)−1`. **"Why B?" is: B is the p=2
companion matrix of CSX's αs.** It also confirms our conjecture
`rank₃W(3,27) = 8353`.

---

## 2. What is ours

### 2.1 The claim

The corpus (and the literature) **assume** q=3 and derive consequences. The
selection layer argues q=3 is **forced**. Two arguments, resting on *different*
assumptions — so their independence is real.

### 2.2 Selection A (Pass 225) — the spinor count

The shadow group is `SO(q²+1)`; its half-spinor has dimension `2^{(q²−1)/2}`.
Setting that equal to **16** — one Standard Model generation, empirically 16 Weyl
fermions including ν_R — has the **unique odd solution q=3** (q=5 → 4096, q=7 →
16.7M).

**Status: a Dynkin-type correspondence, blocked by characteristic.** This is
*not* a numerical coincidence — Pass 327 checked for the disease that killed the
"42" claim and it is absent. The shadow exponent `(q²−1)/2` and the D_n
half-spinor exponent `(q²+1)/2 − 1` (with `2n = q²+1`) are **identically equal as
polynomials**. Both 16s are the half-spinor of Dynkin type `D_{(q²+1)/2}`, which
at q=3 is **D5 on both sides**. The type genuinely matches.

**What blocks it:** the shadow is `D5(2) = Ω⁺(10,2)` over **F₂**; the GUT is
`D5(ℂ) = Spin(10)`, and a generation is its **complex chiral** 16.

> **F₂ has no complex structure, so the F₂ half-spinor has no chirality** — and
> chirality is the entire physical content of "a generation". The F₂ object has
> the right dimension and the right Dynkin type and *cannot* have the property
> that matters.

The identification is therefore neither coincidence nor derivation, but a **change
of characteristic**. To close it you must supply a complex structure — a Weil
representation over ℂ, or a lift of `Ω⁺(10,2)` to a complex form. **That is the
sharpest open question this programme has.**

### 2.3 Selection B (Pass 227) — the exceptional rank

Every rung is Eastin–Knill non-universal; a magic cubic of `SO(q²+1)` needs rank
`(q²+1)/2 ≤ 8` (the maximal exceptional rank, E₈); only q=3 qualifies (rank 5),
via `SO(10) ⊂ E₆` with `27 = 16+10+1`.

**Status: an elegance argument, not a constraint — weaker than we claimed.**
`[[40,10,4]]` is a stabilizer code; magic-state injection restores universality
for *any* stabilizer code, requiring no Lie theory. Our own Pass 237 already
distils magic with `[[40,10,4]]` using exactly that standard machinery. **Every
rung is computationally universal.** What 227 actually establishes:

> q=3 is the only rung whose magic resource is *also* a geometric object of the
> same tower.

That is self-containment, not computability, and it should be written that way.

### 2.4 Also ours

- **`d ≤ q+1`** (Pass 229) — the CSS distance upper bound. The *equality* is
  proved only at q=3, where the code was already known. The honest family is
  **`[[(q+1)(q²+1), q²+1, ≤q+1]]`**, and `k·d = n` is a **tautology** (n is
  *defined* as `(q+1)(q²+1)`).
- **`Q(√6)`** (Pass 298) — the substrate's forced field. Survives the
  forced/chosen test.

---

## 3. The honest thesis

> **If** the shadow half-spinor is a Standard Model generation, **and if** the
> magic resource must be geometric, **then** q=3 is doubly forced — by two
> independent arguments resting on different assumptions.

Selection A's antecedent is a real Dynkin-type correspondence with one named
obstruction (chirality). Selection B's antecedent is a preference. **They are not
of equal strength. A is worth pursuing; B should be restated.**

---

## 4. What this cost, and what it bought

Over passes 224–328: ~15 passes of rank-law rediscovery, ~4 of CSS rediscovery, 2
multi-hour jobs computing a published closed form, and **four** measurements that
were uninformative by construction (Pass 287 the trace law, 319 the δ table, 323
`k·d=n`, 328 the guard's 97% flag rate — the last caught *before* shipping).

Against that: two conditional selections, one distance bound, one field ladder —
and the method: the five failure modes (`.continuity/INSTRUCTIONS.md`),
`RESULTS_INDEX.md`, and a calibrated pre-commit guard. **Measured duplication rate:
21% of pass files assert a code parameter that already exists uncited** (Pass 328).

**The arc produced better method than mathematics.** Given that "check index.html
first" was already in the standing instructions *and* the agent memory and still
failed twice, the method is plausibly the more durable output.

---

## 5. The boundary

The selection layer is a **paper-sized result, not a Theory-of-Everything-sized
one**, and it is honest at that size.

### 5.1 The one open computation that decides it (Pass 330)

**Do not build a complex structure — one already exists on this tower, and the
deciding case was simply never run.**

`PASS214_218_SOURCE_TORSOR_DUAL_OVOID_WEIL_SYNTHESIS.md` (the other track,
GAP-verified) builds the **characteristic-two Weil structure of the shadow at
exactly Selection A's degree `(q²−1)/2`**, citing
[Szechtman](https://arxiv.org/abs/math/0212378). And it splits by character field:

| q | transvection values | field | module | chirality |
|---|---|---|---|---|
| 5 | `(−1±5√5)/2` | `Q(√5)` — **real** | `12a+12b` over F₄, self-dual | achiral |
| 7 | `(−1±7√−7)/2` | `Q(√−7)` — **complex** | `H₇ = U ⊕ U*`, non-isomorphic duals | **chiral** |
| **3** | **never computed** | ? | ? | **?** |

A complex character field gives a dual pair `U ⊕ U*` — **that is chirality,
intrinsically, in characteristic two.** So Pass 327's "F₂ has no complex
structure" is too strong as a blanket claim: the structure exists at q=7. The
question is which side **q=3** is on, and the two indicators **conflict**:

- **By congruence** q=3 resembles q=7 (Gauss sum: `q ≡ 3 mod 4 → √−q`, complex → **chiral**).
- **By endomorphism field** q=3 resembles q=5 (`End(central 8) = F₄`, per Passes 187/189 → **achiral**).

Nothing in the q=5,7 data settles it — the two-point trap again (Pass 314; Pass 324
confirmed `det(B_p)` flips sign between p=5 and p=7, invisible from two points).

> **The deciding run:** `gap -q analysis/w33_pass218_weil_shadow_split.g` at **q=3**.
> **Chiral** → Selection A's obstruction is removed and it becomes the strongest
> result the programme has. **Achiral** → Selection A is conditional forever.
> Either way it closes. *(GAP is not installed in the Claude track; this is handed
> to the GAP-owning track.)*

### 5.2 The freeze

**Pending that one run, this arc is frozen.** The yield over passes 224–330 is two
conditional selections — one now demoted to elegance (§2.3) — one distance bound,
and one field ladder, against ~19 passes of rediscovery and four
uninformative-by-construction measurements. Duplication is **~20% across both
tracks** (Pass 330), so more passes at this rate have arguably negative expected
value.

The remaining mathematics is **one GAP run**, not a hundred passes. Everything else
here is bookkeeping on other people's theorems — and that is a result too, arrived
at honestly.
