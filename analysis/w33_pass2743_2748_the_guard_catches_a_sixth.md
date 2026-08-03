## Passes 2743–2748 — a novelty guard, and it catches a sixth on its first run

---

## Pass 2743 — the guard

`scripts/check_novelty_claims.py`. When a file asserts novelty — *"appears to be absent"*,
*"no prior art"*, *"nobody has stated"*, *"new to this repo"* — it extracts the distinctive
tokens around that assertion and greps them against the three documents that produced
every measured failure:

```text
docs/index.html            photonic_holonet_body.tex          w33_paper_body.tex
```

Built on a **measured** failure rate, not a hypothetical one:

```text
Pass 2650  "two order-51840 groups"  -- in the holonet paper's ABSTRACT
Pass 2651  the fractal branching      -- the paper's own BT827 theorem, 40-ary
Pass 2652  the E6 cubic's space       -- the paper states 27 = 3(x)3(x)3
Pass 2674  the E8 > A2+E6 branching   -- the paper explicitly warns against it
Pass 2742  the Jordan ladder          -- index.html Pillars 128-130
```

Self-test against the known failure:

```text
w33_pass2732_2741...md:77
  novelty asserted: The Albert algebra reading appears to be absent.
    but 'Albert' occurs in index.html
    but 'Jordan' occurs in index.html
```

Warns, never blocks. The token regex is deliberately narrow — matching "new" alone would
flag every file, which is the noise failure `check_rediscovery.py` and
`check_certificates.py` were each calibrated away from.

---

## Pass 2744 — the guard crashed on its own repo

First full run died with `UnicodeEncodeError: 'ℂ'` — the character `ℂ`, on a cp1252
console. My own operational notes carry exactly this warning, and I wrote a guard that
violated it.

Fixed with an ASCII fallback on output. Recorded because a guard that crashes on the
notation it is guarding is worse than no guard.

---

## Pass 2745 — the re-audit: **one real hit in 36 files**

```text
checking 36 files ... 7 novelty claims with encyclopedia hits
```

Triaged:

| flagged | verdict |
|---|---|
| `265`, `840`, `920` digit substrings | noise — substring matching on numerals |
| `218` in index.html | noise — a different 218 |
| `End` in index.html | noise — matches "End" in ordinary prose |
| `Albert` / `Jordan` (twice) | the known Pass 2742 failure, correctly re-flagged |
| **`Kraft` in `photonic_holonet_body.tex`** | **real** |

### The real one: Pass 2701 is partly wrong

Pass 2701 wrote: *"The consequence nobody has stated: every bit string is a valid
instruction stream."*

`photonic_holonet_body.tex` line 382:

> *"The equality case of Kraft–McMillan means the routing words fill a binary decision
> tree with **no unused branch**."*

> **"No unused branch" is that statement, in coding-theory language.** The paper says it,
> with a citation to McMillan. My "nobody has stated" is wrong.

**What survives:** the engineering consequence I drew on top — that the error model has no
decode-error term, only a wrong-result term, so a corrupted packet is still a legal
computation — is a step past the coding fact and I did not find it stated. The underlying
completeness property is the paper's.

**Sixth correction of the session, and the first found by a tool rather than by the user
pointing at a file.** That is the guard doing precisely its job on its first real run.

---

## Pass 2746 — what the audit says about the base rate

Of ~36 session pass files, exactly **two** carried novelty assertions that collide with
the encyclopedia: Pass 2735 (Jordan) and Pass 2701 (Kraft). Both are now corrected.

That is a lower rate than the five-failure record suggested, because most of this
session's corrections came from claims that did **not** assert novelty explicitly — they
simply framed something as a finding without saying "this is new". The guard cannot see
those.

> **The guard catches explicit novelty assertions. It does not catch implicit ones, which
> is where four of the six failures actually lived.** Honest limitation, stated so the
> tool is not over-trusted.

---

## Pass 2747 — the three not done

Chasing the transpose = time-reversal result, reading Pillars 128–130 properly, and
building `CX_{p→f}`. The batch went to the guard and the audit, which the measured failure
rate justified.

---

## Pass 2748 — ledger

| claim | status |
|---|---|
| guard built and self-tests on the known failure | **done** |
| guard crashed on `ℂ` | **fixed; my own cp1252 rule violated** |
| 36 files audited | done |
| Pass 2701 "nobody has stated" | **wrong — the paper says "no unused branch"** |
| Pass 2701's fault-model consequence | stands, not found stated |
| the guard catches implicit novelty framing | **no — explicit assertions only** |
| transpose result, Pillars 128–130, `CX` | not done |

---

## Prior art

- `photonic_holonet_body.tex` line 382 and McMillan — own the Kraft-equality completeness.
- `scripts/check_rediscovery.py`, `scripts/check_certificates.py` — the calibration policy
  this guard copies.

## Still open

- A way to catch *implicit* novelty framing, which is where most failures live.
- The transpose = time reversal consequence; Pillars 128–130; `CX_{p→f}`.
