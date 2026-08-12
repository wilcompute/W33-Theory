# ERRATUM — Retraction of srg(33,8,2,2) Claims from Prior Session

**Date:** 2026-08-12  
**Severity:** MAJOR — affects Passes 4801–4812 and 4968–4972 (first proposal)
**Status:** FORMALLY RETRACTED

## Summary of Retracted Claims

A prior session ("Passes 4801–4812: The SRG Constellation Breakthrough") and the
initial Pass 4968–4972 proposal introduced multiple false claims about a graph
called "srg(33,8,2,2)". These are formally retracted:

### Retracted Theorem: "W33 = srg(33,8,2,2)"

> "W33 = srg(33,8,2,2) is not an isolated object. It sits at the base of a
> canonical 4-level SRG tower."

**Retracted.** W33 = W(3,3) = srg(**40**,12,2,4). The "33" in W33 denotes the
parameters (3,3) of the symplectic polar space, not the vertex count.

### Retracted: "4-level SRG tower with W33 at base"

The claimed tower:
- srg(33,8,2,2) — DOES NOT EXIST in this context
- srg(40,12,2,4) — ✅ this IS W(3,3)
- srg(45,12,3,3) — exists but unrelated to W(3,3) by Fano deletion
- Gewirtz srg(56,10,0,2) — exists but unrelated

### Retracted: "W33 eigenvalues ±√6"

Correct eigenvalues: **+2 (×24) and −4 (×15)**, both rational integers.
See Perplexity Pass 5 commit (2026-07-26) for explicit verification.

### Retracted: "W33 Ihara zeta has transcendental poles"

Correct: all Ihara poles are in imaginary quadratic fields Q(i√43) and Q(i√107).
No transcendental poles.

### Retracted: "Fano-G₂ Deletion Theorem"

The claim that removing 7 Fano-plane vertices from srg(40,12,2,4) gives srg(33,8,2,2)
is false. The 33-vertex induced subgraph is not strongly regular.
See analysis/BT1779_induced_subgraph_obstruction.md.

### Retracted: "33-vertex Witting hyperplane section"

The Witting polytope W₂₄₀ has 240 vertices. There is no canonical 33-vertex
hyperplane section relevant to W(3,3).

### Retracted: "PSL(2,32) as Aut(W33)"

Aut(W(3,3)) = PSp(4,3), order 25,920. PSL(2,32) (order 32×33×31/2 = 16368) is
unrelated to W(3,3).

## What Remains Valid

| Claim | Status |
|-------|--------|
| W(3,3) = srg(40,12,2,4) | ✅ Correct |
| v=40, k=12, λ=2, μ=4 | ✅ Correct |
| Eigenvalues +2(×24), −4(×15) | ✅ Correct |
| Aut = PSp(4,3), order 25920 | ✅ Correct |
| Ramanujan (both |r|,|s| ≤ 2√11) | ✅ Correct |
| Bulk CSS code [[240,81,3]]₃ | ✅ Correct |
| n_B = q(q-1)(q+1)(q²+1) = 240 | ✅ Correct |
| Fano-7 stabilizer ≅ PSL(2,7) | ✅ Correct |
| SM hypercharge critical group | ✅ Correct (at v=40) |
| v = 40 = q×p_Ih + Φ₆ = 33+7 | ✅ Correct |

## Root Cause

The error originated from conflating the name "W33" (= W(3,3), parameters)
with a vertex count of 33. This led to fabrication of a non-existent srg(33,8,2,2)
and an entire false tower of SRG relations. The repo's own pass_992 and
BT1779 files contain the correct information that should have been consulted first.

## Action Items

- [x] PASS4968 corrected: orbit structure on 40 vertices
- [x] PASS4969 corrected: character table based at v=40
- [x] PASS4970 corrected: rational Ihara zeta, Ramanujan confirmed
- [x] PASS4971 retracted: Fano deletion theorem
- [x] PASS4972 corrected: critical group at v=40
- [ ] Review all prior session outputs referencing srg(33,8,2,2) for cascading errors
