# Passes 2586–2591 — the value index found **two** cross-track rediscoveries

---

## Pass 2586 — `42,912`: Pass 2432 re-derives Pass 1843

Pass 2583 flagged that `42,912` appears both as the parallel track's Pass 2432
nine-signature fibre total and as `candidate_total` in
`w33_pass1843_second_orbit_no_lift.json`. Reading Pass 1843 settles it — **it is the same
object**:

```text
Pass 1843 candidate_counts : [288, 288, 864, 864, 2808, 2808, 11664, 11664, 11664]
Pass 2432 fibre sizes      : [288, 288, 864, 864, 2808, 2808, 11664, 11664, 11664]
IDENTICAL MULTISET : True        both total 42,912
```

And the theorems say the same thing:

> **Pass 1843:** *"The newly discovered free 25,920-element signature-resolution orbit has
> no lift to nine pairwise-disjoint exact frame covers. The deterministic nine-partite
> search closes after 289 nodes and 288 dead ends."*
>
> **Pass 2432:** *"the selected balanced nine-signature tuple cannot lift to a nine-cover
> transversal"* — 3,359,232 candidate pairs, 0 disjoint.

Both carry the identical caveat that it is **not** global nine-cover UNSAT because the
signature-resolution orbit census is incomplete. Pass 1843 also cites **Pass 1835**: two
inner signature orbits comprising 28,800 capacity resolutions.

> **Pass 2432 re-derives Pass 1843 with a different search, reaching the same nine fibre
> sizes and the same no-lift conclusion.** Neither cites the other.

The later work is not wasted — 2432's pair-level census is finer, and 2471/2552 extend it
to trade radii four and five, which 1843 does not attempt. But the **base case** was
already established, and the extension should cite it.

---

## Pass 2587 — `91,007,752`: Pass 2550 re-derives Pass 1829

The same sweep found a second one:

```text
91007752 -> w33_pass1829_weight4_decoder.json/distinct_syndromes
```

Their Pass 2550 reports the complete lower shadow from weights `0, 2, 4` as `134,839,021`
records reducing to **`91,007,752`** distinct syndromes, and concludes *"the complete
lower-shadow image is exactly the weight-four image"*.

> **`w33_pass1829_weight4_decoder.json` already records `distinct_syndromes = 91,007,752`.**
> The weight-four image was computed long before, under the name that describes it.

Pass 2550's genuinely new content — the 63 singleton witnesses and the
`63 × 51,840 = 3,265,920` lower bound — stands. The lower-shadow reduction underneath it
does not appear to be new.

---

## Pass 2588 — what this says about the index

Pass 2570 built it; Pass 2583 gave it a fair test; this pass is the payoff.

> **Two cross-track rediscoveries, found by looking up two integers.** Neither
> `w33_pass1843_second_orbit_no_lift.json` nor `w33_pass1829_weight4_decoder.json`
> shares any vocabulary with the passes that re-derived them — no topic search reaches
> either.

That is the mechanism `CLAUDE.md` describes, operating on **certificates** rather than
date-named prose, and it is a category the existing `RESULTS_INDEX.md` and
`TOPICAL_ALIASES.md` do not cover because certificates contain no prose to index.

**Recommendation for both tracks:** before publishing a count, run

```text
py -3 scripts/build_certificate_index.py <the count>
```

It is one command and it has now hit twice in its first two uses.

---

## Pass 2589 — ranks 10–14: **second failed attempt**, reported as such

Pass 2581 failed with random merging. This pass tried seeded coherent closure — the
parallel track's method — over 1,200 non-binary seeds of 3, 4, 5 and 6 parts:

```text
ranks found : [2, 3]        rank 9 reached ? False        ranks 10-14 ? none
```

Again it never reaches rank 9, the one rank known to exist, so again this is evidence
about the method rather than the ranks.

**The identified error:** my closure merges the *pair where a violation was detected*.
A correct coherent closure merges only what is **forced** — classes that become
indistinguishable under the refinement — and starting from 22 singletons upward rather
than from a coarse seed downward. I have not written that correctly, and two flawed
searches are not evidence of absence.

> **Ranks 10–14 remain unsearched.** The ceiling `Σ m = 14` (Pass 2569) stands; the
> intersection-number test (Pass 2580) is correct and fast; only the search strategy is
> missing.

---

## Pass 2590 — the four integer-key producers

Confirmed present, not repaired:

```text
1872_1876  53 integer-like keys      1891  87
2011_2015   5                        2012   4
1887        0   (the outlier)
```

They share the necessary condition identified in Pass 2482 and now surface on every push
via the Pass 2577 CI job. Repair needs each producer's own hashing path inspected —
counting key types is not enough, as Pass 2517 showed when reversing the round-trip still
failed to reproduce their digests.

---

## Pass 2591 — ledger

| claim | discharged by | status |
|---|---|---|
| `42,912` is one object across 1843 and 2432 | identical 9-element multiset + same theorem | **rediscovery confirmed** |
| `91,007,752` is one object across 1829 and 2550 | index lookup, same quantity | **rediscovery confirmed** |
| ranks 10–14 are empty | — | **not shown; second inadequate search** |
| my seeded closure is correct | never reaches rank 9 | **refuted** |
| four producers share the integer-key condition | key-type census | confirmed, unrepaired |

---

## Prior art

- Pass 1843 / 1835 — **own** the nine-signature no-lift result and the 42,912 fibre census.
- Pass 1829 — **owns** the weight-four distinct-syndrome count.
- Pass 2432 / 2550 (parallel track) — re-derive those; their extensions (radius 4–5, the
  63 singleton witnesses) are new.
- Pass 2433 (parallel track) — the seeded-closure method I failed to implement correctly.

## Still open

- Ranks 10–14, needing a correct coherent closure.
- `χ(H) ∈ {10, 11}`.
- Five certificates.
- Whether Pass 1835's second orbit changes anything in the radius-4/5 picture.
