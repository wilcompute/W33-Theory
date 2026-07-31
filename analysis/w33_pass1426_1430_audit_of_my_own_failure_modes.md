# Passes 1426–1430 — auditing the failure modes my own last batch produced

Five checks, all pointed at me rather than at the mathematics. Each of the two
errors the parallel track caught in Passes 1416–1420 turned out to be an instance
of a *class*, and each class is now measured and, where possible, checkable.

---

## Pass 1426 — the eigenspace-comparison audit: Pass 1397 is safe, for a reason worth stating

The signed/unsigned error killed Pass 1412. The obvious worry is that Pass 1397's
`coker(M) ⊗ Q ≅ ker(A+4I)` — the same *shape* of statement — is wrong the same
way. It is not, and the distinction is exact:

| | ambient | action |
|---|---|---|
| `coker(M) ⊗ Q` | quotient of `Q²⁴⁰` | **unsigned** edge permutation |
| `ker(A+4I)` | subspace of `Q⁴⁰` | **unsigned** point permutation |
| `ker(K−10I)` (Pass 1412) | subspace of the **signed** edge module | signed permutation |

Pass 1397 compared **two characters directly** — it decomposed both modules in
the same character table and found the shared degree-15 constituent. That is
legitimate for any two `QG`-modules regardless of ambient. Pass 1412 did
something different and invalid: it computed the *multiplicity of a constituent
inside a presumed ambient module* and drew a conclusion about a subspace that
was never in that ambient.

**The rule, stated so it can be applied:** comparing characters of two modules is
always valid; inferring from a multiplicity inside module `X` requires first
proving the object of interest is a submodule of `X`. Pass 1412 skipped that
step, and my own notes had already quoted the fact that would have caught it —
"Aut acts on *oriented* edges by *signed* permutations".

---

## Pass 1427 — the sweep could not have caught BT1420, for two independent reasons

I built the boundary sweep for exactly this situation and was saved instead by
reading a filename. Testing it directly:

```text
boundary section found in my Pass 1412 file : False
order_key(mine) = (1,1410)   order_key(BT1420) = (1,1420)
```

1. **My file has no boundary section at all.** I write open questions in running
   prose — *"So the question stays open, and it is now sharp"* — under no
   heading. `boundary_text()` returned `None`, so the file was never scanned. The
   tool assumed a convention I do not follow.
2. **BT1420 is a `.tex`.** The sweep globbed `analysis/*.md` only, while the
   parallel track publishes its theorems as manuscript inserts. Half the corpus
   was outside the file set.

Both fixed: prose open-questions are now recognised, and `.tex` files are
scanned. Scope went from 1,258 files to **1,482**, and candidates from 7 to 16.

**A third defect surfaced while fixing these, and it is the worst of them.**
Restoring the file's escapes replaced **five** literal backspace bytes — `\b`
word-boundary escapes eaten by a shell heredoc, *including patterns written in
Pass 1395 that had therefore never worked*. A regex with `\x08` in it compiles,
reads correctly in the source, and matches nothing. This is the third occurrence
in one session. `_assert_no_control_chars()` now runs at import and raises, so
this class fails loudly instead of silently.

---

## Pass 1428 — two guards for the two classes

**`edge_action_tokens()`** in `check_rediscovery.py`. The corpus has two distinct
240-dimensional edge modules and writes both as "240", "edge module", `Q^240`.
A file is now tagged `edge240:signed` or `edge240:unsigned`, so a claim about one
can collide with a claim about the other instead of looking identical to every
tool that consumes the grammar.

**`scripts/check_sampler_bias.py`.** Flags files that enumerate solutions,
truncate to the first few, and never randomise:

```text
scanned 3723 files
  deterministic-order samplers      : 133
  ...that also generalise in prose  :  92    <- the ones to read
```

Advisory, not fatal: truncating for display is fine, and exhaustive enumeration
makes order irrelevant. What is not fine is *"the sampled X all have property P,
therefore X has P"* when the sample came from one search order — which is exactly
what Pass 1411 did.

---

## Pass 1429 — 87% of manuscript inserts reach no manuscript

Asked whether the manuscript refactor had dropped an insert, the answer is **no**:
`w33_paper_body.tex` keeps its inputs, the root wrapper adds `BT1420` and
`BT1425`, and `BT1340_BT1344` was never committed into a manuscript in the first
place (`git log -S` over all four manuscript files returns nothing). Not a
refactor drop.

But the check found something larger:

```text
manuscript-insert .tex files under analysis/ : 217
included by a manuscript                     :  28
ORPHANED                                     : 189   (87%)
added in the last 14 days, still orphaned    :  15
```

**The promotion step, not the mathematics, is where work stops.** An insert no
manuscript inputs reaches no reader, is never compiled by CI, and will be
rediscovered later — all the cost of a result and none of the reach. My own
`BT1408` was about to join them.

`scripts/check_orphan_inserts.py` reports this, and reports the recent ones
separately because those are the ones still cheap to fix. Deliberately advisory:
a hook that fails the build on 189 pre-existing files is a hook people disable.

---

## Pass 1430 — what this batch is

Nothing here is new mathematics. It is the audit that the previous batch earned:
two errors were found by someone else, both were instances of classes, and the
classes are now measured (`133`/`92` samplers, `189` orphans, `5` dead regexes)
and instrumented. The one genuinely reassuring result is Pass 1426 — the theorem
that survived, survived for a stateable reason rather than by luck.

## Prior art

- Passes 1416–1420 (parallel track) — **own** the intertwiner and the refutations this batch audits.
- [Pass 1426 correction](analysis/w33_pass1410_1415_fourteens_diagonal_and_a_failed_shortcut.md) — where the two errors are recorded against the original claims.
- [Pass 1397](analysis/w33_pass1397_1401_cokernel_theorem_covers_collisions.md) — the eigenspace theorem audited and cleared here.
