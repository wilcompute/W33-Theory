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
