# Pass 1020 — the two groups of order 51840, and which 240-set each one owns

**Certificate:** `analysis/w33_pass1020_e8_transitive_51840.g` →
`data/w33_pass1020_e8_transitive_51840.json` (24/24 checks, idempotent, GAP 4.16.0)

---

## The question

Carried over as the flagship open item: **does `W(E8)` contain a subgroup of order
51840 acting transitively on the 240 roots?**

The previous session attacked it with `MaximalSubgroupClassReps` on a group of
order 696,729,600 and it did not terminate. That approach was wrong, not slow.
No subgroup search is needed — the subgroup can be written down.

## The answer: yes

**Springer's theory of regular elements.** The degrees of `W(E8)` are
2, 8, 12, 14, 18, 20, 24, 30. Those divisible by 3 are **12, 18, 24, 30**, and

```text
12 · 18 · 24 · 30 = 155520
```

So for a regular element `w` of order 3, `C_{W(E8)}(w)` is the rank-4 complex
reflection group with degrees `{12,18,24,30}` — Shephard–Todd **G32**, the Witting
polytope group, `= Z3 × Sp(4,3)`. Its derived subgroup is `Sp(4,3)`, order 51840.

Computed directly inside `W(E8)` acting on the 240 roots (3 seconds, not a search):

| object | value |
|---|---|
| `\|W(E8)\|` | 696729600, transitive, root stabiliser 2903040 = `\|W(E7)\|` |
| `w` | order 3, **no fixed roots** (regular) |
| `C = C_{W(E8)}(w)` | **155520** = `\|G32\|`, transitive |
| `K = C'` | **51840**, **transitive on all 240 roots** ✔ |
| root stabiliser | **216**, structure `((C3 × C3) : C3) : Q8` = `3^{1+2}:Q8` |
| `K` perfect | yes; `Z(K)` = order 2; `K/Z(K)` simple of order 25920 |
| `Z(K)` generator | **exactly the antipodal map** `α ↦ −α` |
| subdegrees | `[1,1,1,1,1,1, 27,27,27,27,27,27, 72]` — **rank 13** |
| blocks | sizes 2 (120 antipodal pairs), 3, and 6 (40 Eisenstein lines) |

`K ≅ Sp(4,3) = 2.U4(2)`.

Two structural facts fall out and both check:

- The stabiliser fixes **six** roots, not two — because every element of `C` is
  ℂ-linear, so fixing `v` forces fixing the whole Eisenstein line
  `{±v, ±ωv, ±ω²v}`. The stabiliser `3^{1+2}:Q8` is the determinant-1 subgroup of
  the Hessian group ST25 = `3^{1+2}:SL(2,3)` of order 648, exactly as the Witting
  picture predicts.
- The 13 suborbits **refine the inner-product partition** `(1, 56, 126, 56, 1)`
  forced on any subgroup of `W(E8)`: `56 = 2+27+27`, `126 = 27+27+72`.

## What this settles about 240 = 240

Both 240-sets carry a faithful transitive order-51840 action with a
216-point stabiliser. Order, degree, transitivity, faithfulness and stabiliser
order **all agree**. They are still not the same action:

| | 240 E8 roots | 240 W(3,3) edges |
|---|---|---|
| group | `Sp(4,3) = 2.U4(2)` | `PGSp(4,3) = U4(2):2 = W(E6)` |
| perfect? | **yes** | **no** |
| centre | order 2 (the antipodal map) | trivial |
| subdegrees | `[1⁶, 27⁶, 72]` | `[1,1,4,18,18,18,18,27,27,108]` |
| **rank** | **13** | **10** |

**No equivariant bijection exists**, for three independent reasons:

1. **The groups differ.** Equal order, non-isomorphic — one is perfect, the other
   is not.
2. **The rank differs**, 13 vs 10. Rank is an invariant of the permutation
   action, so no relabelling and no choice of isomorphism can reconcile them.
   This is the strongest form: it does not depend on which map you try.
3. **The centre dies.** `Sp(4,3)` acts on the roots with its centre realised as
   the antipodal map; on the edges that same centre is the projective scalars and
   acts trivially. The root action is faithful, the edge action is not.

Pass 1012 eliminated the `W(E6)` route via `E6 × A2`. This eliminates the only
other order-51840 candidate. **The 240 = 240 correspondence is closed, not open.**

## Four corrections to the corpus

The numerical coincidence `|Sp(4,3)| = |W(E6)| = 51840` was read as an
isomorphism, and that error propagated.

1. `EXPLICIT_BIJECTION.py:561` — *"No proper subgroup of W(E8) acts transitively
   on 240 roots (this is a well-known fact)."* **False.** `Sp(4,3)` (51840) and
   `G32` (155520) are both proper and both transitive.
2. *"Sp(4,3) ≅ W(E6)"* / *"Aut(W(3,3)) = Sp(4,3)"* — **false**, and present in at
   least five files (`GROUP_THEORETIC_BIJECTION.py:308`,
   `docs/COMPLETE_SUMMARY.md:729`, `WITTING_W33_S12_SYNTHESIS.py`,
   `w33_BREAKTHROUGH_341_witting_polytope_SQNA.py`,
   `w33_eisenstein_grand_synthesis.py:81`).

   The constructive version: **the order is right and the edge-side work built on
   it is right.** `Aut(W(3,3))` really does have order 51840 — but that group is
   `PGSp(4,3) = U4(2):2 = W(E6)`, not `Sp(4,3)`; the symplectic group itself acts
   on the edges with its centre in the kernel. The misnomer is *harmless while you
   stay on the edge side*, and fatal the moment it is carried to E8, because there
   the two groups genuinely diverge — one is transitive on the roots and the other
   is not. Nothing on the edge side needs redoing; only the name, and every
   inference that crossed to E8.
3. `WITTING_W33_S12_SYNTHESIS.py` — *"W(E6) has 15 orbits on E8 roots."*
   The count is **13**: `[1⁶, 27⁶, 72]` — one 72, six 27s, six fixed A2 roots.
4. `WITTING_W33_S12_SYNTHESIS.py` — the stated *"THEOREM: there exists a
   W(E6)-equivariant bijection φ: W33 edges → E8 roots"* is **refuted**, and was
   already inconsistent with its own Part III item 4, which records that W(E6) is
   *not* transitive on the roots. A transitive source cannot map equivariantly
   onto an intransitive target; the proof strategy ("pick `e₀ ↔ r₀` and extend by
   the group action") fails at that step.

## Pass 338's two labels are interchanged

`analysis/w33_pass338_selector_frame_240.g` computes two degree-240 actions and
attaches the E8 label to the wrong one. **Every number it reports is correct**;
only the attribution is reversed.

- It calls the ATLAS `2.U4(2).2` action with subdegrees `[1,1,4,54,72,108]` the
  *"signed E8 action"*. That **cannot be an E8 root action at all**: suborbits of
  any subgroup of `W(E8)` containing `−1` must refine `(1,56,126,56,1)`, and no
  subset of `{4,54,72,108}` sums to 56. (Subset sums computed in the certificate:
  `0,4,54,58,72,76,108,112,126,130,162,166,180,184,234,238`.)
- That profile is instead the **W(3,3) edge** profile fused by the index-2
  overgroup: `4·18 = 72` and `2·27 = 54` carry
  `[1,1,4,18,18,18,18,27,27,108] → [1,1,4,54,72,108]`.
- Conversely the profile it calls the *"selector frame"*,
  `[1,1,1,1,1,1,27,27,27,27,27,27,72]`, is exactly the subdegree profile of the
  genuine E8 root action computed here inside `W(E8)`.

## Prior art — cited, not reclaimed

The rediscovery guard flagged `shephard-todd`, `witting`, `eisenstein`. These were
read end to end first:

- `analysis/w33_witting_degrees_unify.py` — ST32 degrees `{12,18,24,30}`, product
  155520 = 3·|Sp(4,3)|, cited to Lehrer–Taylor. **That is its result**, and it is
  the *input* to the Springer argument here.
- `analysis/w33_eisenstein_forcing.py`, `docs/index.html` — the Witting polytope's
  240 vertices are the E8 roots, symmetry ST32 of order 155520.
- `exploration/WITTING_W33_S12_SYNTHESIS.py`, `docs/index.html` — the 240 W(3,3)
  edges carry a transitive order-51840 action with stabiliser 216.
- Pass 1012 — no W(E6)-equivariant edge-root bijection for the `E6 × A2` embedding.

**What is new** is the finer question those leave open. That ST32 (order 155520)
is transitive on the 240 was known. Whether its **index-3 subgroup of order 51840
is still transitive** is a different question — and it is the one the flagship item
actually asks. Settled here by construction inside `W(E8)`, together with both
subdegree profiles, the rank obstruction, and the corrections above.

## Harness note — a fourth Windows trap

`scripts/run_gap.sh` must `cd` into the GAP install directory to invoke `./gap`, so
GAP's working directory is **not** the repo. A relative
`OutputTextFile("data/x.json")` therefore writes into the GAP installation, or —
if `data/` is absent there — silently returns `fail`, and the next
`SetPrintFormattingStatus` dies with `no method found ... 1st argument is 'fail'`.
That error names neither the path nor the directory, so it reads as a GAP bug.

The harness now exports `W33_REPO` (Windows style). Read it in GAP:

```gap
repo := GAPInfo.SystemEnvironment.W33_REPO;
out  := Concatenation(repo, "/data/whatever.json");
```
