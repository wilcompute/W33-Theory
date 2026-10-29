# Passes 12450–12457: the Majorana rescue of SM_2541, d ≥ q + 3, and the holographic dictionary at q = 3

Claude track. Producer: `analysis/w33_pass12450_to_12457_majorana_rescue_deficit_cutrank_index.py`. Drivers: `analysis/search_drivers_12450`
to `12453`, `12373/vet_maj.py`, and `12357/lift_exact.py` (new `LIFT_MAJORANA` option). Tool: `scripts/code_parameter_index_all_repos.py`.

## Correction first: the SM_2541 "unliftable (1,2,0) pair" was a Dirac-only artefact (12451)

Passes 12437 and 12443–12444b reported that every SM_2541 model keeps exactly one massless pair of fractionally charged (1,2,0) doublets,
whatever the hypercharge. **That claim is withdrawn.**

The lifting test paired only **distinct** conjugate fields (Dirac masses). The two leftover doublets are each a single Weyl fermion in the
**real** representation (2,2) of SU(2)_hidden × SU(2)_L, with Y = 0. A real-representation fermion can take a **Majorana** mass ψψ s^n on its
own. That mass passes the same exact, all-orders lattice test: gauge U(1)s, point group, Witten parity and space-group translations.

`which_rule.py` on SM_2541_c22:

- **Dropping one rule at a time** (gauge, point group, Witten parity or translations): every relaxation still leaves the same 2 Dirac-unmatched
  doublets. No single selection rule is the obstruction.
- **Representations:** the two doublets that Dirac matching does pair are pseudo-real (three SU(2) doublet factors). The two leftovers are
  real.
- **Self-pairing:** allowed for both leftovers, so `unmatched_after_majorana = []`.

**For the whole family** (`vet_maj.py`, all 52 models): Dirac pairing leaves exactly 2 fractional fermions in each model, and Majorana
self-pairing lifts **every** fractional state in every model: 92 or 104 fractional fermions per model, depending on k_Y.

**The control is not vacuous.** On c22 the self-mass lattice test passes for only **8 of the 92** fractional fields, and all 6 real Y = 0
fields are among those 8. So the test can fail, and here it does not fail where it matters. Result: 52 of 52 models are fully liftable, and
each one needs exactly 2 Majorana self-masses.

**SM_2618 (Pass 12365) is unaffected.** Its leftover types are (±3, 1, ∓1/6) and (1, 1, ±1/2), which are colour triplets or have Y ≠ 0. No
self-mass is possible.

**The corrected verdict for the SM_2541 lineage** (non-SUSY Z6-II SO(16)², 52 models) [E within the engine's selection rules]:

- three generations;
- an anomaly-free hypercharge;
- safe at large radius on both tori;
- free of hypercharge-independent exotics;
- **every fractionally charged state can be given a mass along singlet directions.**

What remains open:

- k_Y ≥ 11/3, so gauge coupling unification needs threshold help.
- The singlet VEVs that the masses use must be shown to be a vacuum (D/F-flatness and stability in the non-SUSY setting).
- It is tachyonic at small R5.

This is the first lineage in the Claude-track string search to clear the fractional-charge test.

## 12450: d = 2q — CP-SAT is not the lever, a dual theorem was already in the repo, and a new bound d ≥ q + 3

**CP-SAT with native XOR constraints.**

- The q = 3 controls are exact: no kernel word of weight ≤ 4, and a weight-6 word is found.
- At q = 5 with W = 8, both symmetry cases return UNKNOWN after 900 s each. The q = 5 value d = 10 was settled by MILP (cdde9b06b, and 12434),
  so CP-SAT is the weaker tool here.
- **Ownership.** The other track ran the same native-XOR CP-SAT model at q = 7 in parallel. It was committed first (5d32e6aa9 and c8337c96a,
  18:08), with both pair-orbit cases UNKNOWN after 90 s. That q = 7 run is theirs. Mine adds only the q = 3 and q = 5 calibration, which shows
  the encoding already stalls at q = 5, W = 8, and so explains their inconclusive result.

**Prior art, previously uncited (found by searching for the result).** **Pass 4754** (bac1e7df4, 2026-08-10) proves the *dual* statement for
every odd q: the binary kernel of the **line** graph of W(3,q), which is the point graph of Q(4,q), has distance **q + 1**. The minimum word
is an anisotropic-plane conic. Passes 12426–12449 should have cited it.

**The two graphs side by side:**

| graph | distance |
|---|---|
| point graph of W(3,q) | 2q (q = 3, 5 exact) |
| line graph of W(3,q) | q + 1 (all odd q, Pass 4754) |

**Lemma (proved here).** For the point graph of W(3,q) with q odd, **d ≥ q + 3**.

- **Step 1.** Pass 4754's double count also applies to the point graph: w ≥ q + 1, with equality only if S is pairwise non-collinear and every
  other point is collinear with 0 or 2 points of S.
- **Step 2.** Take a, b in S. Each z in {a,b}^⊥ already sees a and b, so it sees no other point of S. Now take a point s of S off the
  hyperbolic line {a,b}^⊥⊥. Its polar plane s^⊥ meets the projective line {a,b}^⊥, so s is collinear with some such z. That is a
  contradiction, so S lies inside the hyperbolic line.
- **Step 3.** With w = q + 1, S is the whole hyperbolic line. Points off it see 1 or q + 1 points of S, which is odd, so S is not a kernel
  word.
- **Step 4.** Hence w ≥ q + 2. Kernel weights are even, because a kernel word is a sum of an even number of lines (the other track's
  ker = {Ny : Σy even}) and each line has q + 1 points. So d ≥ q + 3.

At q = 3 this gives d = 6 **by hand**. Exhaustive check at q = 3: 9450 pairwise non-collinear 4-sets, none with an even profile; hyperbolic
lines have profile {1, 4}.

**Status of d = 2q:**

| q | lower bound | upper bound |
|---|---|---|
| 3 | 6 | 6 (proved) |
| 5 | 10 | 10 (exact, MILP) |
| 7 | 10 (certified computationally; the general lemma also gives exactly 10) | 14 |

The lemma is weaker than the computed bound at q = 5 (8 against 10). Its value is that it holds for every odd q, and that it explains *why*
the point graph cannot reach Pass 4754's q + 1: in W(3,q) the only candidate, a hyperbolic line, has an odd profile.

## 12452: the holographic dictionary — exact at q = 3, open at q = 5

Call a region R of the binary W(3,q) graph state *entanglement-deficient* if some nonzero x supported in R has Ax supported in R.

I minimised |R| exactly by MILP, with r ≥ x, r ≥ p, Ax = p + 2k and x₀ = 1:

| q | smallest deficient region | code distance |
|---|---|---|
| 3 | **6**, proved twice: the HiGHS optimum is a kernel word; CP-SAT finds no region of size ≤ 5 and one of size 6 | 6 |
| 5 | **open**: HiGHS stops at its 3000 s limit on the trivial incumbent 31 (a vertex and its neighbours); CP-SAT feasibility for size ≤ 9 returns UNKNOWN after 900 s | 10 |

**At q = 3 the smallest deficient region equals the code distance**, and the minimum is reached by a kernel word (Ax = 0). This makes the
12427 dictionary ("distance = smallest region that is not maximally entangled") an exact statement at q = 3. At q = 5 it remains a
conjecture.

A general bound comes from the Pass 4754 count. If ℓ ∈ supp x has t neighbours in supp x, then for the region R

  |R| ≥ (q + 1)(q + 1 − |x|) + |x| + t,

and also |R| ≥ |x|. Together these give |R| ≥ q + 1 for every q. Equality fails in the same way as in the 12450 lemma.

## 12453: the cut-rank profile — flat at the ceiling

For a bipartition (X, Y), the entanglement of a graph state measured in qudits is rank_p A[X,Y]. Since A[X,Y] = (A+I)[X,Y], it is at most
the ceiling rank_p(A+I) of 12418.

| state | ceiling | random balanced cuts (40) | local-search minimum |
|---|---|---|---|
| qutrit W(3,3) | 11 | **all 11** | 11 |
| 5-ary W(3,5) | 36 | **all 36** | 36 |
| binary W(3,3) | 40 | 15–16 | 11 |
| binary W(3,5) | 156 | 65–66 | 63 |

- **The own-characteristic states sit at their ceiling on every sampled balanced cut.** The entanglement profile is flat. These are not
  minimum-entanglement cuts proved exhaustively: local search simply never went below the ceiling.
- **The cross-characteristic (binary) states carry more entanglement on balanced cuts**: roughly 0.4 n.
- **Correction to how 12445 is read.** Along the family W(3,q) with growing q, the own-characteristic width 1 + C(q+2, 3) ≈ q³/6 grows
  linearly in the number of qudits n = q³ + q² + q + 1 (fraction → 1/6). So the necessary condition for universality is met
  along q, not only along the dimension. The "simulable qubit" statement of 12445 concerns W(2n−1, 2) only.
- Universality itself is still **not decided**.

## 12454: a code-parameter index across every repository

`py -3 scripts/code_parameter_index_all_repos.py` git-greps every primary repository under C:/Repos for [[n,k,d]] and [[n,k,d]]_q and writes
`CODE_PARAMETER_INDEX_ALL_REPOS.md`. For each parameter it gives the repositories, the file count, and the earliest dated file in a sample of
up to six files. Grep it for the parameters of a code before calling the code new.

Result: 188 distinct parameters. Worktree clones (w33-toe-*, w33_dualhost_*) count as repositories, so the repository column is noisy. The earliest date is taken over a sample of six files, so treat it as an upper bound on the true first appearance.

## 12457: synthesis

- **String route.** The SM_2541 lineage no longer fails on fractional charges. The earlier failure was a Dirac-only bookkeeping artefact.
  What remains is k_Y ≥ 11/3, the vacuum (singlet VEVs), and tachyons at small R5.
- **d = 2q.** There is now a general lower bound q + 3, exact at q = 3. The dual line-graph theorem (q + 1) had been in the repo since
  August.
- **Holography.** Deficient region = distance is proved at q = 3 and open at q = 5, where both exact solvers stall. Own-characteristic Pauli-geometry graph states have
  perfectly flat balanced entanglement at the ceiling.
