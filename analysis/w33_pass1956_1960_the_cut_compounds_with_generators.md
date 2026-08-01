# Passes 1956–1960 — the cut compounds with generators, and the two 96s are not the same group

Five items. The tooling item from last batch is now a real tool, and the
six-attempt geometric-symmetry sequence finally closes.

---

## Pass 1958 — `assert_cuts` promoted to `scripts/`, with `assert_added`

`scripts/constraint_audit.py` now carries both checks, importable from any solver
file:

- `assert_cuts` — does this constraint remove at least one feasible assignment?
  Catches failure modes 1–5 of this arc.
- `assert_added` — did the model actually grow? Catches failure mode **6**, the
  one where a *verified* constraint was never added.

```text
selftest: VACUOUS  x <= 8 over 0..8   504 -> 504  (0.0% removed)
          CUTS     x0 < x1            504 -> 252  (50.0% removed)
          selftest PASS
```

It lives in `scripts/` rather than in an analysis file for the same reason
`TOPICAL_ALIASES.md` needed a pre-commit hook: a tool nobody imports is a tool
that does not run.

---

## Pass 1957 — what a 17% cut is worth: it compounds with **generators**, not size

```text
14 cliques, 1 generator   21,436 -> 17,196   19.8% removed
18 cliques, 1 generator   18,247 -> 15,089   17.3% removed
14 cliques, 3 generators  22,332 -> 12,772   42.8% removed
```

> **Adding cliques does not change the rate; adding generators roughly doubles
> it.** One generator removes ~18–20%, three remove 43%.

That is the answer to whether the geometric break is worth pursuing: its value
scales with how much of the group you encode, not with problem size — so the
lever is *more generators*, and there are 40 available.

---

## Pass 1956 — the full model, with the constraint verified **and** asserted added

Six attempts in, with both checks in place:

```text
ADDED   geometric lex, 8 generators   constraints 249 -> 1209
STATUS  UNKNOWN [330 s, 198,352 branches, 395 conflicts]
```

The constraint is present this time — asserted, not assumed. Against the plain
model's 2,127,575 branches this is a **10× reduction**, though still behind the
spread-variable encoding's 60,909.

The conflict count is the interesting number: **395**, against 1,040 for the
spread encoding and 3,622 for the plain one. The solver is pruning by constraint
rather than by learning, which is what a symmetry break should look like — and
also why it does not close the instance on its own.

For the record, the sequence that ends here: vacuous (Pass 1938), vacuous
(Pass 1946), verified-but-unused (Pass 1955), verified-and-used (here). Three
failures, all of the same shape, all caught only after the fact until a checker
existed.

---

## Pass 1960 — the two 96s are a coincidence

The substrate's internal symmetry group and the frame stabiliser both have order
96, and the frame stabiliser is what reads the chirality locally (Pass 1816), so
the coincidence was worth one check:

```text
frame stabiliser        : order 96, C2 x C2 x S4, abelian FALSE
internal symmetry group : order 96, {+-1}^4 x Z6,  abelian TRUE
ISOMORPHIC              : FALSE
```

**Not the same group** — one is non-abelian and the other abelian. The shared
order is arithmetic coincidence, and this substrate has produced enough real
coincidences that ruling one out cheaply is worth doing rather than leaving it
suggestive.

---

## Pass 1959 — the refuted readings are retired in the note

`W33_SPREAD_OBSTRUCTION_NOTE.md` §5 now carries the phase result *and* an
explicit table of what it is not, so a reader is not left reconstructing two
retractions from five pass files:

| reading | refuted by |
|---|---|
| `ℤ₆` is electric charge (Gauss-law sector) | the phase is in the **coexact** block — Pass 1934, and independently the parallel Pass 1943 |
| `ℤ₆` is a flux quantum (Dirac) | the complex is **torsion-free at every prime** — Pass 1944 |

What stands is the representation theory: one non-rational block with field
`ℚ(ω)`, internal units `ℤ₆`, inverted by the outer involution, touching only the
coexact sector — hence the 81 is neutral (parity) and colourless (the
endomorphism split). **No physical identification of the `ℤ₆` is currently
supported**, and the note now says so.

---

## Prior art

- Passes 1938/1946/1955 — the three failed attempts this one closes.
- Pass 1816 — the frame stabiliser whose order 96 Pass 1960 tests against.
- Pass 1934/1944 and parallel Pass 1943 — the two refutations Pass 1959 records.

## Still open

- `χ(H) = 9`. Best encodings: spread-variable branching at 60,909 branches,
  geometric lex at 198,352 with only 395 conflicts. Neither closes it, and
  combining them is untried.
- What the `ℤ₆` is physically. Both proposed readings are dead.
