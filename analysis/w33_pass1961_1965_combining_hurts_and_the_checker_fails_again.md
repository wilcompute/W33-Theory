# Passes 1961–1965 — combining the encodings hurts, and the checker failed a third time

Five items. Three are negatives against my own last batch, and the checker built
two batches ago failed again — in a new way, caught by an invariant rather than
by its self-test.

---

## Pass 1961 — combining the two encodings makes it **worse**

Spread-variable branching gives 60,909 branches; geometric lex gives 198,352.
They prune by different mechanisms, so combining them looked obvious:

```text
spread branching alone               :    60,909 branches, 1,040 conflicts
geometric lex alone (8 gens)         :   198,352 branches,   395 conflicts
COMBINED, spread branching + 8 gens  :   451,460 branches,    59 conflicts
COMBINED, spread branching + 40 gens :   512,714 branches,    68 conflicts
```

> **Combining is 7× worse than the better half alone.** The lex constraints
> interfere with the spread-variable decision strategy — the fixed search order
> that strategy imposes is exactly what a lex leader needs to be free to reorder.

A negative for the configuration I predicted would win.

---

## Pass 1962 — 40 generators is no better than 8

Pass 1957 measured the cut compounding with generators: 19.8% at one, 42.8% at
three, on a witness model. At full scale:

```text
 8 generators : 451,460 branches
40 generators : 512,714 branches   (slightly WORSE)
```

> **The compounding does not survive to search performance.**

That qualifies my own Pass 1957 conclusion, and the general lesson is worth
stating: solution-count reduction and search-tree reduction are different
quantities. I measured the first and claimed relevance for the second.

---

## Pass 1964 — the checker failed a third time, caught by an invariant

Auditing the constraint families used in earlier pushed models:

```text
CUTS    class size == 60 (Hoffman)     13,222 -> 5,549    58.0% removed
CUTS    octet family == 8              13,576 -> 9,991    26.4% removed
CUTS    point family == 12             13,824 -> 12,875    6.9% removed
VACUOUS clique-0 pinning (k=9, WLOG)   11,670 -> 13,857  -18.7% removed
```

The last line is impossible. **A constraint cannot increase the number of
solutions.** The cause: `_count` enforced a 60-second solver limit but checked
only whether the *cap* was hit, so a time-limited enumeration returned a partial
count and the comparison became meaningless.

Three distinct failures of this one function now — cap saturation (v1), biased
sampling (v2), time-limit truncation (v3) — each producing confident output. v4
checks solver status for completeness **and** asserts the monotonicity invariant
`b ≤ a`, reporting `INVALID` rather than a verdict when it fails. Re-running:

```text
UNKNOWN clique-0 pinning (k=9)     enumeration truncated
UNKNOWN K10 <= 5 (KNOWN FALSE)     enumeration truncated
```

> **Refusing to answer is the correct output**, and it exposes a scope limit:
> `assert_cuts` works on small witness models and **cannot audit constraints on
> the full 540-variable instance**, because exact enumeration does not terminate.

The three `CUTS` verdicts above came from v3 and are therefore **provisional**,
not established. Marked so rather than keeping the convenient numbers.

---

## Pass 1963 — the `ℤ₆` is confined, and that is its structural role

Both physical readings are dead (Passes 1934, 1944). What the `ℤ₆` *is*
structurally follows from multiplicity-freeness: every constituent of `V` appears
once, so `Hom_PSp(90, X) = 0` for `X ∈ {15, 24, 30, 81}`.

> **No `PSp(4,3)`-equivariant linear map can transfer the `ℤ₆` out of the coexact
> block** — not the boundary maps, not the Hodge maps, nothing equivariant. The
> `ℤ₆` is *dynamically isolated*: the substrate's only internal symmetry beyond
> block signs, acting on one sector, unable to couple to any other.

The parallel track's Pass 1954 states the same confinement independently, and
closes Pass 1948's open question with a **no**: the internal `C₆` has character
multiplicities `(150,45,0,0,0,45)` while the `E₈` Coxeter `C⁵` has
`(40,40,40,40,40,40)`, so no `C₆`-equivariant bijection between them exists.

---

## Pass 1965 — the standalone note, and what it is not

`W33_SPREAD_OBSTRUCTION_NOTE.md` has an ownership boundary (§0), a retraction
table (§5), and a 20-check regression test. Turning it into a referee-shaped
draft — abstract, numbered theorems, proofs written out rather than verified — is
a larger job than one pass and is **not** claimed done here.

What the note is today: a correct, checkable internal document. What it is not
yet: a paper. (The parallel track pushed `Pass 1970: add referee-shaped
standalone spread-obstruction draft` while this batch was running; that is theirs
and should be read before either is extended.)

---

## Prior art

- Pass 1957 — the compounding claim Pass 1962 qualifies.
- Passes 1951/1955/1958 — the three earlier versions of the checker.
- Passes 1934/1944 — the two refuted readings behind Pass 1963.
- Passes 1950–1954 and Pass 1970 (parallel track) — **own** the `SL₃(ℤ)`
  identification, the five-orbit minimum shell, the frame-to-duad ABI, the `C₆`
  multiplicity comparison that closes Pass 1948, and the referee-shaped draft.

## Still open

- `χ(H) = 9`. Best single encoding remains spread-variable branching at 60,909
  branches; combining and scaling both made it worse.
- Auditing full-scale constraints, which needs a method that is not exact
  enumeration.
