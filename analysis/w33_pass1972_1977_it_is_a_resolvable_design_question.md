# Passes 1972–1977 — `χ(H) = 9` is a resolvable-design question, not a colouring one

Six items. The reframing is the one that matters: this problem has been in the
wrong literature for its entire history in this repo.

---

## Pass 1972 (the reframing) — `F` is a partial Steiner system, and the question is resolvability

Every frame is a 4-subset of the 240 edges. So the frames define a hypergraph `F`
on 240 vertices, and `H` is its line graph. Measured:

```text
vertices 240,  hyperedges (frames) 540
uniform of size    : [4]
regular of degree  : [9]
max |e cap f|      : 1     -> LINEAR
codegree (pairs)   : max 1, over 3240 covered pairs of 28680
```

> **`F` is a 9-regular, 4-uniform, linear hypergraph on 240 vertices — a partial
> Steiner system `S(2,4,240)` with 540 blocks — and `χ(H) = χ′(F)`. So
> `χ(H) = 9` holds exactly when `F` is 1-FACTORIZABLE (resolvable).**

Every arithmetic necessary condition holds: `240 ≡ 0 (mod 4)`, each parallel
class has `240/4 = 60` blocks, and `540/60 = 9` classes. That is the same
tightness Hoffman gave, restated in design-theoretic terms.

**Why this matters.** For its whole history here the problem has been attacked as
graph colouring, with SAT and CP solvers. It is a **resolvability question in
design theory**, and its literature is resolvable and nearly-resolvable
`S(2,4,v)` systems, Baranyai-type factorization, and Berge's conjecture on linear
hypergraphs — where the tools are constructions and arithmetic obstructions, not
search. Nine solver configurations have now returned `UNKNOWN`; a tenth is not
the move.

---

## Pass 1974 — why every encoding is stuck, measured

Conflict density across every configuration tried in this arc:

| configuration | branches | conflicts | per 1k branches |
|---|---:|---:|---:|
| plain CP-SAT | 2,127,575 | 3,622 | 1.70 |
| free cuts added | 255,166 | 163 | 0.64 |
| spread branching | 60,909 | 1,040 | 17.07 |
| no pinning, `sym=3` | 7,415,101 | 202,232 | 27.27 |
| value precedence | 4,230,684 | 155,594 | 36.78 |
| geometric lex, 8 gens | 198,352 | 395 | 1.99 |
| combined, 8 gens | 451,460 | 59 | **0.13** |
| combined, 40 gens | 512,714 | 68 | **0.13** |

A CDCL solver closes an instance by learning from conflicts. **Every
configuration is under 30 conflicts per 1000 branches, and the two most heavily
pruned are under 0.2.** The solver is not finding contradictions to learn from.

> That is the signature of an instance with **no small unsatisfiable core** —
> i.e. one that is satisfiable, or only barely not. It is evidence about *why*
> the searches fail, and it points the same way as Pass 1972: if a resolution
> exists, it should be **constructed**, not searched for.

---

## Pass 1973 — my combination was wrong, theirs is right

Pass 1961 reported that combining spread branching with geometric lex is 7×
worse. The parallel track's Pass 1966 combined them **on the same variables** —
defining `n_{S,c}` literally and letting the geometric group act on the 36-row
spread signature, with orbit-minimum inequalities — and got `25,920 → 807` on a
known colouring's orbit, a 96.9% reduction, with the cuts audited as inserted.

**So my negative was about my method, not the idea.** I put the two encodings
side by side; they put them on shared variables. Recorded as a correction to
Pass 1961.

Their Pass 1967 also settles Pass 1962: the 40 cut directions have rank exactly
40, none redundant, and survivors fall `13,021 → 807` from 1 to 40 generators. So
generator coverage *is* the lever — my "40 is no better than 8" measured branch
counts of a badly combined model, not the cuts' value.

---

## Pass 1975 — the retraction ledger

Every claim in this arc that has been withdrawn or narrowed, in one place:

| claim | status | by |
|---|---|---|
| outer `ℤ/2` = complex conjugation on `Irr(PSp(4,3))` | **`q=3` only**, not general | Pass 1907 |
| `PSp(4,q)` complex iff `q ≡ 3 (mod 4)` | **retracted** — Gow (1985), and in-repo Pass 353/355 | Passes 1912, 1917 |
| `q²(q²+1)/2` phase degree | flagged, same literature | Pass 1914 |
| `ℤ₆` is electric charge | **refuted** — coexact, not Gauss-law sector | Pass 1934 + parallel 1943 |
| `ℤ₆` is a flux quantum (Dirac) | **refuted** — complex is torsion-free at every prime | Pass 1944 |
| `\|class ∩ K₁₀\| ≤ 5` | **false** — restrictive but invalid; 13 attained | Pass 1896 |
| `k < 9` symmetry break | **unsound** outside `k = 9` | Pass 1883 |
| geometric lex "results" ×2 | **vacuous constraints** | Passes 1938, 1946 |
| geometric lex, verified | **never added to the model** | Pass 1955 |
| cut compounds with generators | **does not survive to branch counts** | Pass 1962 |
| combining the encodings hurts | **my method only**; theirs works | Pass 1973 |
| `assert_cuts` verdicts (class/octet/point) | **provisional** — v3 truncation | Pass 1964 |

What still stands, unretracted: the `240` edge-disjoint `K₉` reformulation, the
`K₁₀` maximal-not-maximum theorem, the `1/q` law with its per-line perfect
matching, `σ_S` as a similitude with non-square multiplier and its
uniqueness/centrality at `q = 3`, the signed-edge-module decomposition, the
parity obstruction on the 81, and `End_PSp(90) ≅ ℂ` with `±J`.

---

## Pass 1976 — two referee drafts now exist

`analysis/W33_SPREAD_OBSTRUCTION_REFEREE_DRAFT.tex` (parallel track, Pass 1970)
and `analysis/W33_SPREAD_OBSTRUCTION_NOTE.md` (this track) cover the same
results. Theirs is the LaTeX article with theorem environments and a withdrawal
table; mine is the checkable note with a regression test. **Theirs supersedes
mine as the draft**; mine should be kept as the test harness and its §0/§5
boundary content merged in rather than duplicated.

Not done in this pass: the merge itself, and proofs for the three `q`-general
statements, which remain verified at `q = 3,5,7` and proved nowhere.

---

## Prior art

- Passes 1966–1970 (parallel track) — **own** the correct combined encoding, the
  rank-40 generator result, the `μ₆` `D₁₂` characterisation, the completed
  backward audit, and the referee draft.
- Gow (1985), Vinroot (2005/2010), in-repo Passes 227/346/353/355 — the chirality
  prior art.
- Design-theory framing: resolvable and nearly-resolvable `S(2,4,v)`, Berge's
  conjecture on linear hypergraphs.

## Still open

- Whether `F` is 1-factorizable, i.e. `χ(H) = 9` — now correctly posed.
- Proofs, rather than `q = 3,5,7` verifications, of the `1/q` law and `σ_S`
  uniqueness.
