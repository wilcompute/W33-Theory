# Pass 4424 — the corpus-wide regeneration audit, finished

> ## ⚠ RETRACTED AT PASS 4461 — the NO-CERT row is an artifact
>
> **The headline of this file is wrong.** The certificate detector matched only
> `PART_*.json`, while this repository's dominant convention is `w33_passNNNN_*.json`. It
> was blind to **746** passes that do emit a certificate.
>
> | | reported here | corrected (Pass 4461) |
> |---|---:|---:|
> | emit a certificate | 114 | **878 of 1148 (76%)** |
> | **NO-CERT** | **1015** | **270** |
>
> So "90% of pass scripts emit no certificate" is false; roughly a quarter do not. The
> DRIFTED / FAILED / REPRODUCES rows below are unaffected — those passes were re-run and
> their results stand. Everything downstream of the NO-CERT row is retracted: Pass 4427's
> "the backlog is 780", and Pass 4459's "23 passes searched and emit nothing".
>
> The file is kept unedited below because a record that quietly rewrites its own numbers
> cannot be audited. See `w33_pass4461_4462_the_regex_that_invented_a_backlog.py`.

`scripts/check_certificates_regenerate.py` re-ran every `analysis/w33_pass*.py` in the
repository at a 240-second budget and compared each emitted `data/*.json` byte for byte
against the committed one. Pass 4392 measured this over ~50 recent passes and explicitly
declined to extrapolate. Here is the whole corpus.

| verdict | count | meaning |
|---|---:|---|
| **NO-CERT** | **1015** | the script emits no `data/*.json` at all |
| REPRODUCES | 67 | re-run produced identical bytes |
| **DRIFTED** | **26** | re-run produced *different* bytes — the committed certificate is stale |
| **FAILED** | **13** | the script no longer runs |
| TIMEOUT | 8 | exceeded the budget; not a defect |

## The headline is the row I was not looking at

**1015 of 1129 pass scripts emit no certificate.** Every discussion of certificate hygiene
in this repository — the round-trip rule at Pass 2482, `check_certificates.py`, Pass 4392's
drift taxonomy, `cert_util.py` — governs the **10%** of passes that produce one. The other
90% are unaudited by any of it, and not because they fail a check: because there is nothing
for a check to read.

That reframes Pass 4392 entirely. It found 6 stale certificates in 50 passes and treated
staleness as the problem. The corpus says the dominant condition is *absence*, and a missing
certificate is strictly worse than a stale one — a stale certificate at least records what
was computed and can be diffed.

**This is not a demand that all 1015 be retrofitted.** Many are exploratory, superseded, or
one-line probes where a certificate would be ceremony. The actionable version is narrower:
a pass whose *result is cited elsewhere* and which emits no certificate is a claim with no
machine-checkable record, and that intersection is what should be enumerated next.

## 13 FAILED — scripts that no longer run

Eleven are `AssertionError`, which is the interesting kind: these passes assert their own
invariants and the assertions now fire. That is the checks working, years later, on code
nobody has run since. One is a `FileNotFoundError` for a missing external binary
(`w33_pass4129_4136`), which is an environment problem rather than a result problem.

An assertion firing means either the pass was always wrong, or something it depends on has
changed underneath it. Both are worth knowing and neither was visible before this run.

## 26 DRIFTED — up from 6

Pass 4392's taxonomy holds and extends: the new members are dominated by the same
**line-number** class (`w33_pass3997_4004_layout_tomography`, `w33_pass4013_4018_incidence_
link_h1_memory`, and the manuscript-scanning passes 4300/4307/4370/4375/4388), plus
physics-continuation passes in the 4033–4104 range that are likely **float-tail**.

Three of the drifted certificates are mine from *this session* — 4375 and 4388 scan the
manuscripts and today's plain-language boxes moved every line beneath them, which is
precisely the failure mode Pass 4392 named. `cert_util.anchor()` exists to fix exactly this
and has not yet been applied to them.

## Evidence boundary

This is one run at one budget on one machine. The 8 TIMEOUTs are unclassified — a pass that
exceeds 240 seconds may well reproduce. The FAILED count is a lower bound on breakage for
the same reason. Nothing here says the 26 drifted certificates are *wrong*: drift means the
bytes changed, and Pass 4392 showed two of six such changes were 15th-decimal float tails
with no effect on any claim. Classifying all 26 requires reading them, which has not been
done.
