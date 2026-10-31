# Passes 12482–12489: the minimal even line sets of W(3,q) are built from line pairs, and twin-paired ones obey a Moore bound

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

## 12486–12487: q = 7 and q = 9

The structure of the q = 7 optimum and the q = 9 minimum come from long runs: `elgf7.log` and `elgf9.log`. When they finish,
the producer picks them up.

## Sources

- J.-L. Kim, K. Mellinger, L. Storme, *Small weight codewords in LDPC codes defined by (dual) classical generalized quadrangles*,
  Des. Codes Cryptogr. 42 (2007). https://doi.org/10.1007/s10623-006-9017-6
- V. Pepe, L. Storme, G. Van de Voorde, *On codewords in the dual code of classical generalised quadrangles and classical polar
  spaces*, Discrete Math. 310 (2010). https://arxiv.org/abs/1201.3294
- S. E. Payne, J. A. Thas, *Finite Generalized Quadrangles*, 2nd ed. (2009), 3.3.1.
- A. J. Hoffman, R. R. Singleton, *On Moore graphs with diameters 2 and 3*, IBM J. Res. Dev. 4 (1960).
