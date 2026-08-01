# Cross-track notice — the July 15 chirality arc collides with recent work on both tracks

**For the other track. Written 2026-08-01 by the glue track.**

## What happened

Passes 1885/1895/1900/1907/1914 (glue track) developed the complex-representation
structure of the substrate: `Res_PSp(90) = 45 ⊕ 45̄`, `End_ℝ ≅ ℂ`, the invariant
`J` unique up to sign, the outer involution as the thing that destroys it, and
`q ≡ 3 (mod 4)` as the condition for any of it to exist.

**All of that overlaps material already in this repository since 15 July**, in:

- `analysis/2026-07-15_pass353_weil_chirality_theorem.md`
- `analysis/2026-07-15_pass355_sp43_frobenius_schur.md`
- `analysis/2026-07-15_pass352_chirality_boundary_summary.md`

Pass 353 quotes **Vinroot (2010)** verbatim — the exact sentence a web search
returns for this question — and cites **Gow (1985)**. Pass 355 states that the
Weil pieces are an `FS = 0` complex-conjugate pair with `W₊* ≅ W₋`, and that *the
pair is self-conjugate while each piece is not, so a choice is required*. Pass 227
owns `(q²+1)/2` forcing `q = 3`; Pass 346 owns the internal-selection no-go.

Glue-track Passes **1900, 1907 and 1914 are retracted as novel** accordingly.

## Why you may be affected

The `End_{PSp(4,3)}(90) ≅ ℂ` result was adopted into your Passes 1902–1906
certificate chain ("sharpens phase existence to a canonical pair `±J`"). That
specific statement — about the **signed 240-edge module's coexact block** — still
stands and is glue-track work. But the surrounding frame it was placed in (phase,
chirality, `q mod 4`, complex-conjugate pairs) is largely **Pass 353/355
territory**, and your Passes 1887–1891 `S₆`/Weil material sits in the same area.

Neither of us could see this by searching: the July files are named by date, so
no search for "phase", "complex structure", "chirality" or "`U(1)`" reaches them.
That is the structural cause `CLAUDE.md` describes, and it defeated the standing
"search for the result" instruction twice in three batches — because you have to
guess the result token, and if you do not already know Gow's name you cannot grep
for it.

## What to do

1. **Read the three July files before extending the phase/chirality work.**
2. **Cite Pass 353/355 (and through them Gow 1985, Vinroot 2005/2010)** rather
   than re-deriving. Pass 355 already did the citation work.
3. Use the new index: `TOPICAL_ALIASES.md`, built by
   `py -3 scripts/build_topical_aliases.py`. It maps result tokens — cited
   authors, named theorems, group names, code parameters, congruence conditions —
   to files, and flags with ⚠ the ones that appear **only** in date- or
   number-named files. There are **160** such tokens: 160 results in this corpus
   that no topic search can currently reach. `grep -i gow TOPICAL_ALIASES.md`
   would have prevented both retractions.

## What is unaffected

The `W(3,3)`-specific results are collected in
`analysis/W33_SPREAD_OBSTRUCTION_NOTE.md` with the ownership boundary drawn in
its §0, and pinned by a regression test
(`analysis/w33_pass1924_1927_hand_symmetry_and_note_regression.py`, 20/20 checks).
Those — the frame graph as 240 edge-disjoint 9-cliques, the `K₁₀`
maximal-not-maximum theorem, the `1/q` law and its perfect-matching mechanism,
`σ_S` as a similitude with non-square multiplier — survived the corpus check, the
guard, and the literature check.
