# Pass 1983 — my "maximal independent set" claim was wrong, and the other track caught it

The parallel track's Pass 1971 reconciled my standalone note against their
referee draft and reported one theorem-level error in my work. They are right.

## What I claimed

From Pass 1828, repeated in roughly ten subsequent passes, in the commit history,
and in the standalone note:

> "Every spread's 45-frame `K₁₀` is a **maximal** independent set of `H` that is
> not maximum."

## What is actually true

```text
K10 frames                                    : 45
candidates inside the residual                : 15
candidates edge-disjoint from ALL 45 (addable): 15
=> the 45-set is MAXIMAL independent?           FALSE
   45 + 1 = 46 still independent               : True
   greedy extension reaches                    : 48
   uncovered edges remaining                   : 48, so 60 is unreachable
```

Every one of the 15 candidates is edge-disjoint from all 45 seed frames — by
construction, since the seed covers only the 180 off-line edges and the
candidates live entirely in the 60 residual ones. So a candidate can always be
adjoined, and the seed is **not maximal**. It extends to at least 48.

## The correct statement

The obstruction is real; my characterisation of it was not.

> The 45-frame seed **cannot be completed to a 60-frame exact cover**, because
> the 15 admissible candidates collectively touch only 20 of the 60 residual
> edges — **40 residual edges lie in no candidate frame at all**.

That is *residual support deficiency*, not maximality. It is the same
computation Pass 1828 actually ran; I attached the wrong word to it and then
reused the wrong word for ten passes without re-deriving it.

## What is unaffected

The `1/q` law and its Pass 1982 proof are about candidate counts and edge
support, not about maximality, and stand unchanged. So do the `240` edge-disjoint
`K₉` reformulation, `σ_S` as a similitude, and the signed-module results. The
error is confined to one word in one characterisation — but that word was in the
headline of the batch it came from.

## Why it survived so long

The claim was never checked in the direction that would falsify it. Pass 1828
verified that *no completion to 60 exists*; it never asked whether *any single
frame could be added*, which is a one-line test and the definition of maximality.
Every later pass quoted the conclusion rather than re-running it.

This is the same failure family as the vacuous constraints — a statement that
looked verified because a *neighbouring* statement had been. The fix is the same
in kind: when a claim has a one-line falsification test, run it.

Credit to the parallel track's Pass 1971 for catching it in a reconciliation I
should have done myself when I wrote the note.

## Ledger

- `analysis/W33_SPREAD_OBSTRUCTION_NOTE.md` §2 — already corrected in place by
  the parallel track.
- `analysis/W33_CLAIM_STATUS_LEDGER.md` — their controlling ledger.
- Pass 1975's retraction table in
  `w33_pass1972_1977_it_is_a_resolvable_design_question.md` listed the `K₁₀`
  theorem under "still stands". **That row is now wrong** and this pass is its
  correction.
