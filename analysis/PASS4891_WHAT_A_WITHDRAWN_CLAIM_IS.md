# Pass 4891 — defining "claim withdrawn", then counting once

I measured this quantity twice without defining it and got 14 (Pass 4810) and 21 (Pass 4819)
— a 50% spread on a statistic offered *as a correction* to a figure given from memory. Both
were counting commit messages that sound like retractions, which is not a quantity.

## The definition

> A **withdrawn claim** is a specific assertion that was published in a pass, and that a
> later pass states is false and names.

Three exclusions follow from it, and each removes something the earlier counts included:

- **A bug fixed inside the pass that made it is not a withdrawal.** Nothing was published.
  My inverted map at Pass 4782 and the doubled divisor at Pass 4824 were caught before the
  commit; they are visible in the commit message because I chose to record them, not
  because a claim stood and fell.
- **A commit is not the unit.** Pass 4795 published two claims that later failed, and one
  commit withdrawing both is two withdrawals, not one.
- **A tool's false positive is not a claim** unless it was reported as a finding. Pass 4855's
  ten "hash mismatches" became a finding the moment I wrote them down; Pass 4857's "five
  stale" likewise. Both count.

## The count

**Eleven.** Enumerated, not pattern-matched:

| # | claim | published | withdrawn by |
|---|---|---|---|
| 1 | the exchange constraint "survives the attempt to break it" | 4685 | 4693 — traces are parameter-determined; the test could not fail |
| 2 | the cancellation condition is `s = t` | 4682 | 4694 — it is self-duality; GQ(3,3) has s=t and fails |
| 3 | the distillation space is 315,057,600 | 4680 | 4691 — it is 3,830,918,130; power was 12.2× overstated |
| 4 | the LC-invariance branch giving a 12,117,600× reduction | 4688 | 4691 — the clean input is a magic state; reduction is 6× |
| 5 | the Hoffman deficit at odd q equals q | 4795 | 4800 — α(W(3,5)) = 18, not 21; deficit 8 |
| 6 | 720 = 36 × 20 is a coset partition by Sz(2) | 4795 | 4797 — 6 ovoids, stabiliser 120 |
| 7 | eight certificates are unverifiable from birth | 4728 | 4801 — all eight verify |
| 8 | sixteen literature-priority novelty claims | 4804 | 4841 — zero of sixteen |
| 9 | the six ovoids are the synthematic totals | 4799 | 4813 — they are the six stars |
| 10 | ten registry entries are hash mismatches | 4855 | 4857 — pointer semantics, not self-digest |
| 11 | five registry pointers are stale | 4857 | 4873 — the registry is correct; one certificate is stale |

## What the number is worth

**Nine of the eleven were refuted by a computation the original pass had itself named as
missing.** That is the finding, and it is more useful than the count: the claims were not
guesses, they were results published one step ahead of a check that was already identified,
costed, and deferred. Running the named check before publishing costs nothing extra — it is
the same computation.

The two exceptions are #10 and #11, which are consecutive false positives in one checker,
and those trace to a different habit — assuming a key name implies a convention — which
Pass 4882 now has a guard for.

## Why this is not a bad number

The alternative to eleven withdrawals is not zero withdrawals; it is eleven claims still
standing. Pass 4761 found a retraction that sat unpropagated for two hundred passes, and
Pass 4841 found a corpus in which the phrase "the first" is used sixteen times and never
once against the literature. Those are what a low correction rate looks like from inside.

## Boundary

The enumeration is mine and covers claims I published in this session's window. A claim
withdrawn *silently* — edited away without a pass saying so — would not appear, and would
be the more worrying kind. I am not aware of one, which is exactly the assurance worth
least.
