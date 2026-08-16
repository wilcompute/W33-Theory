# Certificate key naming convention

Proposed at Pass 5572. **Not yet adopted** — this is a proposal with a measurement
behind it, and adopting it is the user's call, not a pass's.

## The measurement that motivates it

| | |
| --- | --- |
| certificates in `data/` | 5,048 |
| distinct integer-valued key names | 26,718 |
| **new key names per certificate** | **5.3** |
| key reuse ratio (distinct ÷ total uses) | 0.474 |
| keys shared between the two lanes | **13%** of the smaller lane's vocabulary |

A reuse ratio of 0.474 means nearly half of all key uses are the *first* use of that
name. The two lanes writing into this repository share 1,309 key names out of 9,399
and 14,796 — they invent different words for the same quantities **87% of the time**.

That is the structural cause of the rediscovery rate. `CLAUDE.md` says *search for the
RESULT, not the topic* — but a result is only searchable when two authors spell it the
same way, and here they systematically do not. Pass 4800 wrote `alpha`; BT818 wrote
`alpha_exact`; six passes re-derived a value that was already committed.

## The convention

**1. Name the quantity, not the computation.**
`alpha`, not `alpha_from_milp` or `computed_alpha` or `alpha_exact`.
The method belongs in a sibling key: `alpha_method: "milp"`.

**2. Use the corpus's existing word.** Before inventing a key, check whether the
quantity already has a name:

```
py -3 scripts/check_key_nearmiss.py data/YOUR_CERTIFICATE.json
```

It reports any new key that is one small edit from a name already in use. Renaming
before commit costs nothing.

**3. Qualify with a suffix, never a prefix.** `alpha_q5` sorts and greps next to
`alpha`; `q5_alpha` does not. Stem first, qualifier after.

**4. One value per key.** A key whose value is a list of numbers is invisible to the
result index unless each entry is itself a named field. Prefer
`rows: [{q: 5, alpha: 18}]` over `alphas: [7, 18, 33]`.

**5. Reserve these stems** for their established meanings, which the corpus already
uses consistently enough to be worth protecting:

| stem | means |
| --- | --- |
| `alpha` | independence number |
| `hoffman` | the ratio bound |
| `aut` | automorphism group order |
| `deficit` | bound minus attained value |
| `orbit_sizes` | list of orbit lengths |
| `genus` | surface genus |

## What this does not fix

Short names. `q`, `mu`, `k`, `s` are below the four-character floor of the near-miss
reporter and always will be — they are everywhere and matching on them produces
nothing but noise. Two authors inventing short names for one quantity stay
uncatchable.

And a convention only binds what is written after it. The 26,718 names already here
are not renamable: the certificates are committed evidence, and rewriting them to fit
a rule invented later would break every replay that reads them.
