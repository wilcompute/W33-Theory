# W33 Path-Space Internal Algebra Bridge

## Honest status

On 2026-04-09 the repo established an important obstruction:

- the plain vertex Bose-Mesner algebra of W(3,3) is commutative and only has the form
  C + C + C,
- so W(3,3) cannot directly be the Connes internal algebra
  C + H + M3(C).

That obstruction is real and should be preserved.

The right move is therefore not to keep fitting observables on the vertex space.
The right move is to pass to the enriched object already present in the repo:

- W(3,3)
- Hashimoto path space
- Payne 27-sector
- Heisenberg / qutrit structure

## New candidate bridge

The script `exploration/w33_pathspace_internal_algebra.py` builds an explicit candidate internal algebra on the enriched space, not on the 40-vertex commutant.

The construction is:

1. Scalar block from the trivial Hashimoto mode
   - contributes the scalar block C.

2. Quaternionic shell block from the two nontrivial Hashimoto channels
   - for W(3,3) = SRG(40,12,2,4), the non-backtracking shell roots are
     beta_r = 1 +/- i sqrt(10)
     beta_s = -2 +/- i sqrt(7)
   - these obey the exact field-size identities
     |beta_r|^2 = |beta_s|^2 = 11
     Re(beta_s)^2 - Re(beta_r)^2 = 3
     Im(beta_r)^2 - Im(beta_s)^2 = 3
   - the two nontrivial channels therefore form a natural shell doublet
   - on that doublet the script realizes quaternion generators and verifies
     i^2 = j^2 = k^2 = ijk = -1
   - this gives the electroweak-style block H on the shell sector.

3. Color block from the Payne / Heisenberg qutrit sector
   - the repo already identifies the 27 non-neighbours with a qutrit / Heisenberg structure
   - using the standard qutrit Weyl pair X and Z, the script verifies
     XZ = omega ZX
   - the span of X^a Z^b for a,b in F3 has complex rank 9, so it generates all of M3(C)
   - this gives the color block M3(C).

## Candidate algebra

Putting the three pieces together gives the explicit candidate

A_cand = C + H_shell + M3(C)_Heis.

This is not yet a proof of the full noncommutative-geometric Standard Model package.
In particular, it does not yet prove:

- the correct KO-dimension
- the full real structure J
- the first-order condition
- the full spectral action

But it does achieve something the plain vertex algebra could not:

it provides an explicit, noncommutative candidate internal algebra built from structures already present in the repo, while respecting the April 9 obstruction.

## Minimal operator seed

The script also builds a minimal block-diagonal Dirac seed on

C + C^2 + C^3,

namely

D_cand = 1 + diag(beta_r, beta_s) + diag(0,1,-1).

This is only a seed operator, not the full finite Dirac operator, but it makes the enriched state space explicit.

## Why this is the right next step

The repo's strongest surviving structures after the honesty commits are:

- Hashimoto / non-backtracking transport
- Payne 27-point Schlafli / E6 sector
- Heisenberg qutrit structure
- the already-discovered family algebra C + M2(C)

The new bridge shows how these can be reorganized into the correct algebraic shape of the internal sector, instead of trying to force that shape out of the 40-vertex commutant.

## What remains to prove

The next hard problems are now sharply posed:

1. Reality / KO-dimension
   - lift the shell doublet and qutrit fiber into a real spectral triple with the correct J and grading.

2. Bundle version over the Payne 27/45 sector
   - replace the simple block model by a genuine bundle-endomorphism algebra over the 27/45 geometry.

3. Dirac operator with transport
   - upgrade the block seed D_cand to a transport-coupled operator using the 480-state Hashimoto carrier.

If those three land, the repo has a serious path past the April 9 obstruction.

## Files added

- `exploration/w33_pathspace_internal_algebra.py`
- `tests/test_w33_pathspace_internal_algebra.py`
- `data/w33_pathspace_internal_algebra_summary.json`
- `docs/W33_PATHSPACE_INTERNAL_ALGEBRA.md`

## Bottom line

The honest statement is:

- W(3,3) alone is not the final internal algebra,
- but the enriched W33 path-space / qutrit object carries a concrete candidate C + H + M3(C) bridge.

That directly answers the spectral-triple obstruction instead of routing around it.
