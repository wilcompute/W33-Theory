# Passes 12482–12489: the minimal even line set of W(3,7) is a cube; Petersen at q = 5, a Moore bound, and an icosahedron at q = 11

Claude track. Producer: `analysis/w33_pass12482_to_12489_even_line_sets_pair_structure.py`. Drivers in
`analysis/search_drivers_12466`: `even_line_sets_gf.py` (any GF(q)), `pair_structure.py` (enumeration and twin test), `orbit_q3.py`
(the PSp(4,3) orbit).

An **even line set** of W(3,q) is a nonempty set of lines covering every point an even number of times. Equivalently, it is a
codeword of the binary code ker₂(N), where N is the point–line incidence matrix. 12467 and 12474 found the minima 6, 10, 20, 40 at
q = 2, 3, 5, 7. These passes ask what the optima look like.

## Prior art and scope

- **Even q is known.** For q even the binary dual code of Q(4,q) ≅ W(q) has minimum weight 2(q+1), attained by grids
  (Kim–Mellinger–Storme 2007, cited as [9] in Pepe–Storme–Van de Voorde 2010). The q = 4 and q = 8 values below are a control.
- **Odd q is the cross-characteristic case.** Pepe–Storme–Van de Voorde define their codes over the characteristic of F_q, and
  their binary results are for q even. Pass 12442 already recorded that the binary, odd-q case is outside that literature.
- **Searched space:** the corpus (`Mellinger|LDPC|Storme`), two web searches (the GQ-LDPC literature, and "sets of even type" in
  Q(4,q) for q odd), and the full text of Pepe–Storme–Van de Voorde. No minimum for the binary odd-q case was found. That is a
  negative search, not a novelty claim.

## 12482: every finite field

`even_line_sets_gf.py` builds W(3,q) over GF(p^k) with explicit field tables. It checks (q+1)(q²+1) lines, q+1 lines per point,
and that the lines are totally isotropic.

| q | 2 | 3 | 4 | 5 | 7 | 8 |
|---|---|---|---|---|---|---|
| minimum | 6 | 10 | **10** | 20 | 40 | **18** |
| source | control | control | new run (= 2(q+1), known) | control | 12474 | new run (= 2(q+1), known) |

Every optimum covers each point 0 or 2 times.

## 12483: q = 3 completely

- **Count.** CP-SAT enumeration with a single worker finds **exactly 216** minimum even line sets. (Multi-worker enumeration
  silently under-counts.)
- **Control.** No even line set of weight 1–9 exists.
- **One orbit.** The 216 form a **single PSp(4,3)-orbit**, with stabiliser of order 120. This was checked by a breadth-first
  orbit under the symplectic transvections.
- **Shape.** Every optimum has intersection graph **K₅,₅ minus a perfect matching**, with spectrum ±4, ±1⁴. Lines are vertices,
  joined when they meet.

## 12484: q = 5 is the Petersen graph

The q = 5 optimum (20 lines) has 10 pairs of **twin** lines: two lines with the same neighbours in the set. For each pair {L, L′}:

- the two lines are disjoint;
- their q + 1 = 6 neighbours are **exactly** {L, L′}^⊥, the common transversals of L and L′;
- those 6 lines are 3 other pairs.

The **pair graph** (twin pairs as vertices, joined when their lines meet) is the **Petersen graph**.

**Symmetry.** The set's PSp(4,5)-orbit has 4,875 members, so its stabiliser has order **960**, eight times |Aut(Petersen)| = 120
(`orbit_q5.py`, a breadth-first orbit under the transvections). How the stabiliser acts on the pair graph has not been computed.

## 12485: the twin-pair Moore bound (proof)

Let q be odd and S a coverage-{0,2} even line set. Lines of W(q) are the points of Q(4,q), which are **antiregular** for q odd
(Payne–Thas 3.3.1): for disjoint lines L, L′ and any third line M, |M^⊥ ∩ {L,L′}^⊥| ≤ 2.

1. **Degree.** Each point of a chosen line is covered exactly twice. So a line of S meets exactly q+1 others in S, at distinct points.
2. **Twins.** Twins L, L′ are disjoint, because a line is not its own neighbour. Their q+1 common neighbours all lie in
   {L, L′}^⊥, which has size q+1, so **N(L) = {L, L′}^⊥**. A third twin L″ would put q+1 > 2 lines in L″^⊥ ∩ {L, L′}^⊥. So
   **twin classes have size at most 2**.
3. **Pair graph.** Suppose every class is a pair. A pair's neighbourhood is closed under taking twins, so the pair graph is
   ((q+1)/2)-regular.
   - *No triangle.* Three pairwise meeting lines in a GQ are concurrent, and a point covered 3 times is impossible.
   - *No 4-cycle.* Take a 4-cycle A–B–C–D of pairs, with b, b′ the lines of B and d a line of D. Then a, a′, c, c′ all lie in
     d^⊥ ∩ {b, b′}^⊥. That is 4 > 2 lines, contradicting antiregularity.
4. **Bound.** A k-regular graph of girth ≥ 5 has at least 1 + k² vertices (the Moore bound). So

> **|S| ≥ 2 + (q+1)²/2 for every twin-paired even line set of W(q), q odd. Equality holds iff the pair graph is a Moore graph of
> girth 5.** By Hoffman–Singleton such graphs exist only in degrees 2, 3, 7 and possibly 57, so equality requires
> **q ∈ {3, 5, 13, 113}**.

| q | 3 | 5 | 7 | 9 | 13 | 113 |
|---|---|---|---|---|---|---|
| twin-paired bound | 10 | 20 | 34 | 52 | 100 | 6500 |
| Moore graph | C₅ | Petersen | none (the (4,5)-cage has 19 vertices, so ≥ 38) | none (the (5,5)-cage has 30, so ≥ 60) | Hoffman–Singleton | the open case |
| true minimum | 10 (not twin-paired) | **20 = bound, Petersen** | 40 | running | ? | ? |

**Reading.**

- q = 5 meets the bound with the Petersen graph realised inside W(5).
- q = 3 has the same minimum, 10, but none of its 216 optima is twin-paired. A C₅ of pairs does not occur, which also serves as
  the non-vacuous control.
- **Open questions** [C]:
  - Does W(13) contain a Hoffman–Singleton even line set of 100 lines?
  - Does the bound 2 + (q+1)²/2 hold for every even line set at odd q? It holds at q = 3, 5, 7.
  - The data rules out the exponential fit 5·2^((q−1)/2) of 12474 as a law only if q = 9 comes in below 80.

## 12486: symmetric search, and the exponential fit is refuted

`symmetric_even_sets.py` restricts the search to even line sets invariant under a cyclic symplectic map g = A ⊕ B. Here A has order
r in SL(2,q) on ⟨e₀,e₂⟩ and B = A^k on ⟨e₁,e₃⟩. CP-SAT then has one variable per g-orbit of lines and one parity constraint per
g-orbit of points. Every set it finds is verified even, so it is an **upper bound** on the minimum.

- **Controls.** Symmetric sets reach the true minima: **10 at q = 3** (r = 2), **20 at q = 5** (r = 3, k = 1) and **40 at q = 7**
  (r = 4 and r = 8 with k = 1, 3). Each takes seconds, against 2.2 h for the full MILP at q = 7.
- **q = 11:** an even set of **84** lines (r = 12, k = 1 and k = 3).
- **q = 13:** an even set of **168** lines (r = 7, k = 1).

**The 100-line target at q = 13.** A Hoffman–Singleton set (12485) would have 100 = 2 + 7·14 lines with an order-7 symmetry
fixing one twin pair. The k = 0, 2, 3 runs are INFEASIBLE only by arithmetic: all their line orbits have size 7, which does not
divide 100, so they say nothing about the geometry. The k = 1 run, the only family with fixed lines, was UNKNOWN after 1,500 s,
and a 3-hour run was still in progress at commit time.

> **The fit 5·2^((q−1)/2) of 12474 is refuted.** It predicts 160 at q = 11 and 320 at q = 13; explicit even sets have 84 and 168.

Both values are above the twin-pair bound of 12485 (74 and 100), so that bound stands.

## 12487: q = 7 is not twin-paired

The symmetric 40-line optima at q = 7 (r = 8, k = 1 and 3) have 4 twin pairs and 32 single lines (`sym_structure.py`). So
twin-pairing is special to q = 5, where the optimum is the Petersen graph; it is not the general shape of minimal sets.

## 12489: the cube and the icosahedron — an explicit family, and why it is sporadic

**The anatomy that suggested it.** The q = 7 optimum has 40 = 8 + 32 lines:

- four twin pairs {Lᵢ, Lᵢ′};
- their perps {Lᵢ, Lᵢ′}^⊥, each a regulus of q + 1 = 8 transversals (4 × 8 = 32).

**The construction.** Take a regulus R₀ of q + 1 totally isotropic lines whose opposite regulus contains **no** isotropic line
(antiregularity allows 0 or 2). Take a perfect matching M of R₀ into (q + 1)/2 pairs, and set

> S(R₀, M) = R₀ ∪ ⋃_{{L,L′} ∈ M} {L, L′}^⊥,  |S| = (q + 1) + (q + 1)²/2 = **(q + 1)(q + 3)/2**.

The perps are pairwise disjoint and miss R₀: a line meeting three lines of R₀ lies in the opposite regulus, which has no isotropic
line. Every point of R₀ is covered exactly twice. Whether the remaining points are covered evenly depends only on M.

**The condition on M.** Parametrise R₀ by PG(1, q), through where its lines meet one transversal. Call M **good** when:

- every two pairs {a, b}, {c, d} of M have a **non-square** cross-ratio; and
- no three pairs are swapped by one Möbius involution, so no three chords of the conic are concurrent.

| q | perfect matchings of R₀ | geometrically even S(R₀, M) | good matchings | good matchings with all-non-square cross-ratios only |
|---|---|---|---|---|
| 3 | 3 | 3 | 3 | 3 |
| 5 | 15 | 0 | 0 | 10 |
| 7 | 105 | **14** | **14** | 35 |
| 11 | 10,395 | **22** | **22** | 132 |

The geometric count and the combinatorial count agree, and every geometric solution satisfies the condition
(`regulus_matching.py`, `chord_condition.py`). The last column shows that both conditions are needed.

**The good matchings are polyhedra.** In each case the good matchings form one PGL(2,q)-orbit (`exceptional_matching.py`). The
stabiliser is transitive on the q + 1 points, and the pairs are its blocks, the antipodal pairs:

| q | stabiliser in PGL(2,q) | element orders 1/2/3/4/5 | the matching is |
|---|---|---|---|
| 3 | order 8, D₄ | 1/5/–/2/– | the 2 diagonals of a square |
| 7 | order 24, **S₄** | 1/9/8/6/– | the 4 body diagonals of a **cube** (8 points of PG(1,7)) |
| 11 | order 60, **A₅** | 1/15/20/–/24 | the 6 axes of an **icosahedron** (12 points of PG(1,11)) |

**It is sporadic.** A complete backtracking search for a good matching (`chord_search.py`) finds:

- one at q = 3, 7, 11;
- **none** at any other prime q ≤ 61, including the q ≡ 3 (mod 4) primes 19, 23, 31, 43, 47, 59 (complete up to q = 61).

> **So the exact minimum 40 of W(3,7) is attained by a cube**: the antipodal pairs of the octahedral group S₄ ⊂ PGL(2,7), acting
> on a regulus of W(7). At q = 11 the icosahedral group A₅ ⊂ PGL(2,11) gives 84, the best known value there.

These are the exceptional embeddings behind Galois's theorem (PSL(2,p) acts on p points only for p = 5, 7, 11). Here q = 5 fails
the cross-ratio condition, and q = 3 enters through the square.

**Open questions** [C]:

- Are 3, 7, 11 the only q? A Weil-bound count of non-square cross-ratios is the natural route to a proof.
- Is every 40-line optimum at q = 7 a cube?
- Is 84 optimal at q = 11? The twin-pair bound is 74.
- The q = 13 symmetric searches stop at 168 = (q + 1)(q − 1) (orders 7, 6, 12), the same form as the 24 found at q = 5. A second
  family for q ≡ 1 (mod 4)?

## 12488: the local counting bound (proved, weak)

Fix a chosen line L in a coverage-{0,2} even set at odd q.

- Its q + 1 neighbours are pairwise disjoint.
- For a line X at distance 2, let c_X be its number of common neighbours with L. Then Σ c_X = q(q+1).
- By antiregularity, each triple of L's neighbours lies in N(X) for at most one X ≠ L, so Σ C(c_X, 3) ≤ C(q+1, 3).

Minimising the number of such X under these constraints gives |S| ≥ 1 + (q+1) + D_min. That is 9 at q = 3 and 16 at q = 5,
against true minima of 10 and 20. **Whether 2 + (q+1)²/2 bounds every even line set at odd q stays open [C].** It holds at
q = 3, 5, 7, and the q = 11 and q = 13 upper bounds are consistent with it.

## Sources

- J.-L. Kim, K. Mellinger, L. Storme, *Small weight codewords in LDPC codes defined by (dual) classical generalized quadrangles*,
  Des. Codes Cryptogr. 42 (2007). https://doi.org/10.1007/s10623-006-9017-6
- V. Pepe, L. Storme, G. Van de Voorde, *On codewords in the dual code of classical generalised quadrangles and classical polar
  spaces*, Discrete Math. 310 (2010). https://arxiv.org/abs/1201.3294
- S. E. Payne, J. A. Thas, *Finite Generalized Quadrangles*, 2nd ed. (2009), 3.3.1.
- A. J. Hoffman, R. R. Singleton, *On Moore graphs with diameters 2 and 3*, IBM J. Res. Dev. 4 (1960).
