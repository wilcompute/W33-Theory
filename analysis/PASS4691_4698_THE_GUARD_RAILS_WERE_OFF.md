# Passes 4691–4696, 4705–4706 — every hook in this repository was dead, and two of my own results were wrong

Eight items executed. The largest finding was not in the physics.

## The repository had no pre-commit hooks for fourteen days

`.pre-commit-config.yaml` contained a check written as an inline `entry: "` whose
continuation lines began at column 0. A double-quoted YAML scalar must be indented past its
key, so the scalar ended at the first newline and the parser hit bare Python where a mapping
belonged. **The file did not parse**, confirmed by `pre-commit validate-config` itself.

The consequence was not that one hook failed. Every hook in the file was dead:

| hook | what it guards |
|---|---|
| `certificate-digests` | certificates that cannot reproduce their own hash |
| `novelty-claims` | novelty asserted against the encyclopedia |
| `rtl-folds` | RTL modules that synthesise away |
| `pass-namespace-collision-guard` | duplicate pass numbers |
| `topical-aliases`, `stale-boundaries`, +3 | — |

Introduced **2026-07-27** (`10cc58d94`). `.git/hooks/pre-commit` *was* installed, so at every
commit git printed `pre-commit not found for this environment` — which reads like a note
about the environment, not a dead guard rail. That is quieter than a vacuous check: a broken
checker reports cleanly, a broken config reports nothing.

**And `check_rediscovery.py` was never registered at all.** CLAUDE.md calls it the core
artifact of the two-agent protocol — "warns when a staged file asserts a code parameter that
exists elsewhere uncited." The script exists, is executable, is documented, and was wired to
nothing.

Fixed: inline script moved to `scripts/check_smin_formula.py` (with the self-test it could
never have had), rediscovery registered, both new checkers added. **11 hooks live, 9
resurrected.** Re-ran the guards over all 400 files touched in the unguarded window — clean.

## I was wrong twice, in my own recent work

### Pass 4685's test could not have failed

Pass 4685 reported "the exchange constraint survives the attempt to break it" because
`tr(A^k)` agreed for W(3,3)/Q(4,3) and disagreed for the dual pairs. But **`tr(A^k)` is a
function of the SRG parameters alone** — the spectrum is determined by (v,k,λ,μ), so the
traces are too. Verified: every trace reproduced from parameters without building a matrix.

W(3,3) and Q(4,3) are parameter-equal, so agreement was forced. The dual pairs have
different parameters, so disagreement was forced. No arrangement of the data could have
broken the constraint. That is a **vacuous check** — failure mode 7 — committed two passes
after I shipped a checker for vacuous checks. The constraint stands as a necessary
condition; what is withdrawn is that it was *tested*.

### And the condition is self-duality, not s = t

Pass 4682 wrote "the search should be restricted to s = t." GQ(3,3) has s = t and W(3,3) is
**not** self-dual (W(3,q) is self-dual iff q even). Track C's own table already shows their
cancellation *failing* at GQ(3,3), 712 ≠ 180 — exactly where my rule permitted it. **The
refuting row was in the same four-row table as the confirming one**; I read the row that
agreed with me.

**Prediction, recorded before computing:** cancellation holds at W(3,4) and W(3,8), fails at
W(3,5) and W(3,9). The old rule permits all four and predicts nothing. W(3,5) is the
cheapest place this can die.

## And my Pass 4680 denominator was 12.2× too small

Pass 2881 samples **syndrome projectors from k ≤ 4 generators with signs**, not maximal
stabilizer groups. The real space is 3,830,918,130, not 315,057,600. So coverage was
0.000783%, not 0.0095%, and power against a hundred witnesses was **0.078%, not 0.95%** —
the null is weaker than the pass criticising it for weakness said.

**The LC premise fails too.** The clean input is a magic state with cube-root-of-unity
amplitudes; exactly **1 of 576** local Cliffords fixes its ray. The reduction is 6×, not
12,117,600×. Pass 4688's 26 classes answer a different question — and its refusal to assume
the favourable branch was correct, because asserting it would have claimed a
nine-order-of-magnitude reduction that does not exist.

## What did work

- **WebAssembly executed.** `wasmtime` installed; the module runs **567/567** in a real
  runtime. The universality claim is now settled by execution.
- **32 property tests** (`tests/test_w33_l2_conformance.py`) — symplectic form preserved,
  origin fixed by linear opcodes and moved by the translation, minimal trio closing to
  51,840 by exhaustion.
- **Layer sweep of every manuscript: 8 raw → 1 real.** The false family included `GHZ`
  matched case-insensitively as `GHz` — a Greenberger-Horne-Zeilinger state read as a
  gigahertz clock. The real hit was a **corollary** claiming "6.5× compression of the
  fundamental constants" via an uncomputable Kolmogorov complexity and a ratio between two
  bit-counts that do not describe the same thing. Demoted to a remark stating what is
  actually true.
- **Relay fraction is not a mechanism.** It is a bijective function of (s,t), so "relay
  explains the residual after b" *is* "t explains the residual after s". The strict test at
  b = 6 returns **False** — W(3,3) and Q(4,3) are relay-tied and differently dense. One
  contrast, not three.
- **26 means nothing here.** No W(3,3) quantity equals it and none was predicted to.
  Reported as a coincidence, closed.

## Boundary

The layer checker is sentence-local; both examples Part 0 itself gives are cross-sentence.
Track C's four cancellation numbers are quoted, not re-derived — the refutation of my s=t
rule rests on their GQ(3,3) figure being right. Neither W(3,4) nor W(3,5) is computed here;
4695 is a prediction. The relay analysis rests on densities from 600–1000 samples per
carrier, quoted from Passes 4562/4563.
