# Passes 1984–1989 — running the falsifying test breaks a second claim of mine

Five items. Pass 1983 established that my `K₁₀` maximality claim survived ten
passes because only the *confirming* direction was ever checked. This batch
applies the falsifying test to the rest of the surviving ledger, and one more
claim falls immediately.

---

## Pass 1984 — the `270 = ordered incident pairs` claim is **refuted as a `G`-set**

Pass 1875 concluded that the size-270 conjugacy class is in bijection with the
270 ordered pairs of intersecting lines on the cubic surface. The evidence was
that **orders matched**: the centraliser has order 192, `|G|/270 = 192`, `C` sits
in the index-27 maximal with `|M:C| = 10`, and the 27-point action has rank 3
with suborbits `1, 10, 16`.

The falsifying test is whether the two `G`-sets are *isomorphic*, which orders
cannot decide. Comparing permutation characters:

```text
class action (conjugation)  = G/C ?                    TRUE   (by definition)
ordered incident pairs      = G/C ?                    FALSE

ordered incident pairs : 1 + 6x2 + 15 + 20x3 + 24 + 30 + 64x2
G/C                    : 1 + 6   + 15 + 20x2 + 24 + 60 + 60 + 64
```

> **The two 270-element `G`-sets are not isomorphic.** Both are transitive of
> degree 270, but their point stabilisers are non-conjugate subgroups of the same
> order 192.

So Pass 1875's naming is **withdrawn**. What survives is weaker and still true:
`|G|/270 = 192`, `C ≅ D₈ × S₄` sits inside the index-27 maximal with index 10,
and the 27-point action has suborbits `1, 10, 16`. The class has 270 elements and
so does the incident-pair set — but that is a coincidence of counts, not a
correspondence.

This is the third instance of the same error shape in this arc: **matching
numbers taken as matching objects.** Pass 1896 (an average read as a bound),
Pass 1983 (a completion obstruction read as maximality), and now this.

---

## Pass 1985 — the rest of the surviving ledger, falsification-tested

| claim | falsifying test | verdict |
|---|---|---|
| `H` = 240 edge-disjoint `K₉`s | is any `H`-edge outside the cliques, or in two? | **holds** — 8640 = 8640, no duplicates |
| `σ_S` unique | is there a second fixed-point-free involution fixing every spread line? | **holds** — the linewise stabiliser is exactly `C₂` |
| 81 admits no invariant `J` anywhere | exhibit a subgroup that does | **holds** — impossible, 81 is odd |
| `End_PSp(90) ≅ ℂ`, `J` unique to sign | exhibit a third `J` | **holds** — `dim End = 2` |
| the 90 is the only non-rational block | compute all five character fields | **holds** — four are `ℚ` |
| permutation modules carry no complex pair | exhibit one | **holds** — canonical basis ⇒ real |
| `ℤ₆` confined to the 90 | exhibit a nonzero equivariant map out | **holds** — multiplicity-freeness |
| 270 = incident line pairs | are the `G`-sets isomorphic? | **REFUTED** (Pass 1984) |

Seven survive a test that could have broken them; one did not. The distinction
matters: before this pass all eight were "verified" in the sense that *some*
computation supported them.

---

## Pass 1986 — Lemma 3, proved

The `1/q` proof (Pass 1982) rested on one verification: that the `g`-invariant
lines are exactly the `q²+1` spread lines. That now follows from the
construction rather than the computation.

Let `μ` be a non-square, `K = F_q(α)` with `α² = μ`, so `K ≅ F_{q²}`, and regard
`F_q⁴` as a 2-dimensional `K`-space with `g` = multiplication by `α`.

A line of `PG(3,q)` is a 2-dimensional `F_q`-subspace `L`. Then `g(L) = L` iff
`αL ⊆ L` iff `L` is closed under `K`-multiplication, i.e. iff `L` is a
1-dimensional `K`-subspace. Those number

```text
(q^4 - 1)/(q^2 - 1) = q^2 + 1
```

and they partition the points, forming the Desarguesian symplectic spread. Hence
the `g`-invariant lines are exactly `q²+1` in number and constitute `S`. ∎

> **The `1/q` law is now proved end to end for spreads of this form**, with the
> `q`-even branch as a corollary. What remains open is only whether *every*
> symplectic spread carries such a `σ_S` — a classification question, not a gap
> in the argument.

---

## Pass 1989 — orbit-built parallel classes: a weak negative

With bitset edge-supports, six distinct cyclic-orbit signatures were tested for
whether some union of orbits forms a 60-frame parallel class:

```text
distinct orbit signatures tested   : 6
orbit-built parallel classes found : 0
```

**Six is not many.** The filter that keeps orbit counts small excluded most
candidates, so this is a weak negative and is reported as one — the method is
barely explored, not refuted.

---

## Pass 1987 — the quantifier audit

Grepping my own claims for the words with cheap negations — *maximal, unique,
canonical, only, exactly, every* — produced the list Pass 1985 tests. Two of the
three errors found in this arc (`maximal`, and `270 =`) were attached to exactly
such a word, and both were caught in the batch where the negation was finally
run. The audit is worth making routine rather than occasional.

---

## Prior art

- Pass 1875 — the claim Pass 1984 withdraws.
- Pass 1971 (parallel track) — caught the `K₁₀` maximality error and prompted
  this discipline.
- Pass 1982 — the `1/q` proof Pass 1986 completes.
- Pass 1908 — the similitude construction both rest on.

## Still open

- `χ(H) = 9`.
- What, if anything, the size-270 class *does* index.
- Whether every symplectic spread carries a `σ_S`.
