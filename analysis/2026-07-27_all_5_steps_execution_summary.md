# All 5 Next Steps — Exact Execution Summary

**Date:** 2026-07-27  
**Canonical release:** `PASS1132_1136_EXACT_EXECUTION_RELEASE.md`  
**Foundation:** `spec(D=A-I)=11^1+1^24+(-5)^15`

The earlier version of this file described plans as completed work and, in Step 3,
used the order-25920 projective group instead of the full order-51840 Weyl group.
This revision records the executed computations.

## 1. False-cubic descendant quarantine — executed

The historical cubic `(t+1)((t+1)^2-36)` and its determinant/Taylor descendants
are tracked by an explicit ledger. `scripts/check_shifted_adjacency_descendants.py`
scans occurrence signatures and exits nonzero for an active descendant that is
neither registered nor marked `{shifted-adjacency:retracted}` or
`{shifted-adjacency:corrected}`. The fatal changed-file guard is wired into
pre-commit; CI produces a full report.

Observed release audit: 5 matched files, 5 registered/corrected, 0 violations.

## 2. True projector functional calculus — executed

The exact projectors have ranks `1,24,15`, and

`f(D)=f(11)P_11+f(1)P_1+f(-5)P_-5`.

The positive heat trace is

`Tr exp(-tD^2)=exp(-121t)+24 exp(-t)+15 exp(-25t)`.

The first trace moments are `40,-40,520,-520,24040,114200`. The previous report's
`17480,-61480` values were arithmetic errors and are superseded.

## 3. Three 432-orbit stabilizers — executed

The relevant action is by `W(E6)=U4(2):2`, order 51840. Each 432-orbit stabilizer
has order 120. All three have element-order distribution

`{1:1,2:25,3:20,4:30,5:24,6:20}`,

trivial center, derived subgroup order 60, and abelianization `C2`; hence all are
`S5=SmallGroup(120,34)`. They are pairwise conjugate in `W(E6)`. Thus the three
Steinberg carriers are three isomorphic `W(E6)/S5` G-sets.

## 4. Complete cubic-map kernel decomposition — executed

The 45-support image is exactly `1+20+24`. Therefore

`ker L = 13*1 + 16*6 + 5*15 + 4*15a + 21*20 + 2*24 + 9*30 + 4*60a + 10*64 + 3*81_minus + 1*90`,

of dimension 2195. The full `3*81_minus` Steinberg packet lies in the kernel.
The earlier `1952=7*276+20` exterior-power observation was only numerology and is
not part of the decomposition theorem.

## 5. Corpus identity layer — executed

The 540 classifier is now occurrence-level and supports
`{540:line-nonedge}`, `{540:point-nonedge}`, and `{540:both}`. It ignores the
number inside tag literals, uses line-local evidence, reports genuinely mixed
files as mixed, and is fatal on new ambiguous occurrences. A synthetic line / point
/ mixed regression suite has ambiguity rate 0%; CI runs the full live corpus and
commits the generated report.

`data/w33_pass_namespace_registry_v2.json` makes Passes 1120–1128 canonical for
the merged glue track and reserves Passes 1132–1136 for this exact release. Draft
PR #162's branch-local Pass 1120/1121 labels are noncanonical; its exact character
and incidence data are imported under Pass 1135.

## Verification

- E8 roots: 240
- W(E6) closure: 51840
- A2 triples: 2240
- orbit census: `1,1,27x6,240,270,270,432x3`
- focused tests: `4 passed`
- all exact JSON certificates: `PASS`

Scope: finite geometry, finite-group representations, exact spectral algebra, and
repository-integrity controls. No physical claim follows merely from these counts.
