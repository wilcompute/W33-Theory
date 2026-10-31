# Passes 12490–12497: the Petersen graph is a regulus too, and W(13) has no twin-paired Hoffman–Singleton set

Claude track. Producer: `analysis/w33_pass12490_to_12497_moore_family_hs_exclusion.py`. Drivers in `analysis/search_drivers_12466`:

- `regulus_matching.py q tries 2`: the Moore family, built geometrically;
- `chord_search.py --square` and `chord_search_gf.py`: complete matching searches over GF(q);
- `cube_recognise.py`: recognises cube-family sets.

This builds on 12482–12489, which records the twin-pair Moore bound (12485) and the cube family (12489).

## 12490: the second regulus family

Antiregularity leaves two cases for a regulus R₀ of isotropic lines: its opposite regulus contains **0** or **2** isotropic lines.
12489 used the 0 case. In the 2 case, with isotropic opposite lines A and B, both A and B lie in every perp {L, L′}^⊥ for L, L′ ∈ R₀.
Summing mod 2 over a perfect matching M of R₀:

> S(R₀, M) = R₀ + Σ_{{L,L′}∈M} {L, L′}^⊥ (mod 2). When (q+1)/2 is odd, A and B survive and |S| = (q+1) + (q+1)(q−1)/2 + 2 =
> **2 + (q+1)²/2**, which is the twin-pair Moore bound of 12485 exactly.

| q | matchings | even S(R₀, M) | size |
|---|---|---|---|
| 3 | 3 | 0 | – |
| **5** | 15 | **5** | **20 = the minimum: the Petersen set of 12484** |
| 7 | 105 | 0 | – |
| 13 | 135,135 (for each of 20 reguli) | **0** | (the 100-line target) |

## 12491: the matching condition flips to "square"

S(R₀, M) is even exactly when **every two pairs of M have a square cross-ratio** and no three chords are concurrent. That is the cube
family's condition with "non-square" replaced by "square". The combinatorial count equals the geometric count at q = 3, 5, 7, 13
(0, 5, 0, 0). The q = 5 solutions all have three square cross-ratios and no concurrent triple.

## 12492: every Moore-equality set is of this kind (proof)

Let S be a coverage-{0,2} even line set of W(q), q odd, that is twin-paired with a Moore pair graph (12485). Take any twin pair
{A, B}.

- By 12485, N(A) = N(B) = {A, B}^⊥ =: R₀, the regulus of transversals of A and B. Its opposite regulus contains A and B.
- The pair-graph neighbours of {A, B} are the (q+1)/2 twin pairs inside R₀; they define a perfect matching M of R₀.
- Each such pair {L, L′} has neighbourhood {L, L′}^⊥ ∋ A, B.
- A Moore graph has diameter 2, so every other pair is adjacent to some {L, L′} and lies in its perp. Counting gives
  1 + m + m(m−1) = 1 + m² pairs, with m = (q+1)/2, which is every pair.

Hence S = S(R₀, M), and its evenness is the square condition. Equality in the twin-pair bound occurs **exactly when a square-good
matching of PG(1,q) exists**.

## 12493: equality only at q = 5, and no Hoffman–Singleton set at q = 13

Complete backtracking finds square-good matchings:

- **only at q = 5** among primes ≤ 41;
- and at none of the prime powers 9, 25, 27, 49.

The q = 13 geometry agrees: 0 of 135,135 matchings, for each of 20 reguli. One regulus would suffice, since PSp(4,q) is transitive
on pairs of disjoint lines.

> **W(13) contains no twin-paired even line set of 100 lines.** The Moore case of 12485 at q = 13 (Hoffman–Singleton) does not
> occur. Among the q tested, the twin-pair bound is attained only at q = 5, by the Petersen graph.

This excludes only **twin-paired** sets. A non-twin-paired even set of 100 lines at q = 13 is not excluded here. A 3-hour
order-7-symmetric search for one was still running at commit time. The q = 113 case (the open Moore degree 57) is running as a
square-good-matching search.

## 12494: neither family over prime powers

`chord_search_gf.py` runs both conditions over any GF(q). It reproduces the prime results (cube at 3, 7, 11; Moore at 5) and finds
**neither family at q = 9, 25, 27, 49**. With 12489, the regulus families are:

| | condition on the matching | exists at | sets |
|---|---|---|---|
| cube family (0 isotropic opposite lines) | all cross-ratios non-square | q = 3, 7, 11 | square, **cube** (q = 7 minimum 40), icosahedron (84) |
| Moore family (2 isotropic opposite lines) | all cross-ratios square | q = 5 | **Petersen** (q = 5 minimum 20) |

Searched: all primes ≤ 61 for the cube family and ≤ 41 for the Moore family, plus 9, 25, 27, 49. Larger primes are running.

## 12495: the q = 7 optimum without symmetry is a cube

The 40-line optimum of the GF(7) MILP was found with no symmetry imposed (6-hour limit; optimality is 12474's). It is a cube-family
set: 4 twin pairs whose 8 lines form a regulus with no isotropic opposite line, plus their perps. A sample of further CP-SAT optima is
being recognised. **Whether every 40-line optimum is a cube is still open.**

## Prior art

Searched: two further web searches (W(q) reguli with octahedral/icosahedral matchings; Moore graphs realised in Q(4,q)/W(q)), plus
the sources of 12482. No such construction was found. That is a negative search, not a novelty proof.

## 12496: q = 9 goes below the twin-pair bound — the bound is not general

The GF(9) symmetric search (`symmetric_even_sets_gf.py`, `symmetric_fast.py`) finds even line sets of **48 lines** at q = 9. They are
optimal within their symmetry class for order-10 symmetry (k = 1, 4) and for order-8 symmetry (k = 1, 3): two unrelated symmetry
types. The GF(9) MILP had stopped at 164 with lower bound 33.

**48 < 52 = 2 + (q+1)²/2.** So the twin-pair Moore bound of 12485 is **not** a bound for all even line sets at odd q. That answers the
open question of 12488 in the negative.

**Structure:**

- not twin-paired;
- the line graph is bipartite and 10-regular with spectrum ±10, ±√10 (12 each), ±2 (5 each), 0 (12);
- the 48 lines split into two 24-line partial spreads covering the same 240 points;
- inside each half, the number of common neighbours in the other half takes only the values 0 (a perfect matching), 5 (a 2-regular
  graph) and 4;
- the PSp(4,9)-orbit exceeds 400,000 sets (BFS, capped), so the stabiliser has order at most about 1,500.

**Two hypotheses tested and refuted, each with a control:**

1. *A symmetric difference of two spreads (two ovoids of Q(4,9)).* Only 12 lines avoid the covered points, far fewer than the 58
   needed to complete either half to a spread (`spread_switch.py`: INFEASIBLE).
2. *Two parallel classes of the Hermitian lines missing a Baer W(3,3).* This would give 2√q(q − 1) = 48 lines. No Hermitian form
   vanishes on the 240 covered points (nullity 0, `hermitian_test.py`). The same solver finds the form on 240 points of a true
   Hermitian surface (nullity 1, `hermitian_control.py`).

**What the 48-set is remains open [C].**

## 12497: the fast builder, and q = 11 and q = 25

`symmetric_fast.py` enumerates the totally isotropic 2-spaces in reduced echelon form over any GF(q). Its line sets are identical to
the pairwise builder at q = 3, 5, 9. It builds W(3,25) (16,276 lines) in about 5 s, and it reproduces 48 at q = 9 in 64 s.

- **q = 11:** order-10 and order-5 symmetries, not tried before, give **84 again**, optimal within the order-10, k = 4 class. 84 now
  appears under five symmetry types (orders 3, 5, 6, 10, 12). It is the best known value, not a proved minimum.
- **q = 25** (order 26, k = 1): the one-hour run reached only 624 (bound 78). That is **inconclusive**: it neither supports nor
  refutes a different law at square q.

## Cross-track results and one correction (2026-10-31)

- **q = 113 is closed by the other track.** Commit 64d1762dc, `analysis/2026-10-31_five_front_continuation.md` §1: its conic backend
  completes the square-good search at q = 113 (15,319 states, no matching), with an independent backend agreeing on the full
  compatibility graph. With 12492 this gives the statement of record: **among twin-paired coverage-{0,2} even line sets of W(3,q),
  q odd, the Moore bound is attained only at q = 5.** My own q = 113 backtracking (`chord_search.py`) timed out after 4 h, and a
  timeout is not an exclusion.
- **Correction to 12484.** The order of the Petersen set's stabiliser (960) is correct, but "960 = 8 × |Aut(Petersen)|" wrongly
  suggests all of S₅ acts. The other track computed the full stabiliser (`w33_20261031_petersen_stabilizer.py`): its image on the 10
  pairs is **A₅**, element orders 1¹ 2¹⁵ 3²⁰ 5²⁴, with kernel 2⁴ on the cut module, so 960 = 60 × 16.
- **The 48-line set at q = 9 (12496) is a 48-point hyperoval of Q(4,9).** It lies below the twin-pair bound 52, and its size is not
  among the transitive families (q+1)² = 100, q(q+1) = 90, q² − 1 = 80. One literature search (hyperovals of Q(4,q), the Bayens
  thesis) did not find it. That is a negative search, not a novelty claim.
