# Passes 12518–12525: the q = 9 minimum is 48; the four-anyon braid image is the centraliser of the next generator; the 216 codewords are Sylvester's synthematic totals and carry the Hesse configuration

Claude track. Producer: `analysis/w33_pass12518_to_12525_hesse_dictionary.py`. Test: `tests/test_w33_pass12518_to_12525.py`. Drivers in
`analysis/search_drivers_12466`: `star_cubes.py`, `star48_control.py`, `heavy_cases.py`, `heavy_split.py`, `heavy_control.py`, `classify_q7.py`, `classify_q7b.py`, `cube_stabiliser_q7.py`, `cuiwang_compare.py`,
`braid_point_stabiliser.py`, `five_circuit_map.py`, `ten_lines_five_sentinels.py`, `common_bell_contexts.py`, `synthematic_totals.py`, `kramers_doily.py`, `codeword_vs_spread.py`, `pair_of_sic.py`, `syndrome_theorem.py`, `bell_generalisation.py`, `recheck_cadical.py`, `classify_q9.py`, `hesse_dictionary.py`, `hesse_dictionary2.py`, `hesse_dictionary3.py`, `tprime_block.py`.

Labels: **[E]** exact computation or proof, **[N]** numerical with a stated tolerance, **[I]** interpretation.

## 12521: why the four-anyon numbers are what they are

Passes 12507–12516 measured the B₄ image: order 648, 9 = 1 + 2 + 3 + 3, and a split of the 216 minimal codewords into 108 + 108. All of these turn out to
follow from one fact.

### One fixed Pauli

**[E]** The braid generators are transvections along an induced path p₀, …, p₄ in the noncommutation graph. So p₄ commutes with p₀, p₁, p₂. Put c = p₄.
Then, computed on the 40 points:

> **The B₄ image is exactly the stabiliser of c in PSp(4,3), which is the centraliser of the transvection T_c, the fifth braid generator.**

Far commutativity says σ₁, σ₂, σ₃ commute with σ₅. The computation says they generate *everything* that commutes with σ₅.

*Prior art.* The group is already known in this corpus. Pass 1047 names it 3^{1+2}₊:2A₄, the W(3,3) point stabiliser, as opposed to the other class of order
648. `2026-09-21_physical_a2_clifford648_w33_bridge.md` matches it to the qutrit Clifford group H₂₇:SL(2,3). What is added here is that the braid words reach
all of it, with the fixed point named: c = p₄. PASS12506_12513 had the structure but did not notice that G fixes a point.

### 108 + 108 is "covered or not"

**[E]** A minimal even set has 10 lines covering 20 of the 40 points, each twice. So exactly half of the codewords cover c:

| half | coverage of c | codewords | stabiliser in G |
|---|---|---|---|
| covered | 2 | 108 | S₃ |
| uncovered | 0 | 108 | Z₆ |

These are the two B₄ orbits, checked directly. The halves are **not isomorphic as G-sets**, since their stabilisers differ. This closes the question left open in
12507 and 12513: the split has nothing to do with chirality because it is a statement about one point.

### Reproducing the 2026-08-29 partition

`2026-08-29_216_CLIFFORD_TORSOR_NOGO.md` studies 216 "sentinel five-circuits" with stabiliser S₅. It found that the centre C₃ acts as 72 three-cycles with no fixed
circuit, and that the derived subgroup (order 216) has orbits 108 + 36 + 36 + 36.

**[E]** The codeword stabiliser in PSp(4,3) has order 120 with element-order profile 1, 25, 20, 30, 24, 20, which is S₅'s. T_c fixes no codeword. The derived subgroup's
orbits here are 108 (the uncovered half) + 36 + 36 + 36 (the covered half splits). So the partition is reproduced, and now explained.

The explicit bijection with those five-circuits is built in 12523.

### The dictionary

Pass to T_c-classes (3 codewords each), giving 36 + 36 objects under the Hessian group G/⟨T_c⟩ of order 216.

**[E] Uncovered half.** Each stabiliser Z₆ has one involution. There are 9 involutions in G, each with fixed points two hyperbolic lines of 4, one through c, and they
biject with the 9 hyperbolic lines through c (the tensor factorisations in which P_c lies in a factor). Its order-3 element fixes exactly one of the 4 lines through c.
So:

> uncovered T_c-class ↔ (involution, line through c): a bijection onto all 36 such pairs, each involution having 12 codewords over it.

**[E] Covered half.** Each stabiliser S₃ has 3 involutions forming a line of the affine plane on the 9 (t₁t₂t₁ gives the third point; there are 12 lines, in 4 parallel
classes of 3). The two chosen lines through c never contain the line through c that the stabiliser's order-3 element fixes pointwise (108/108). So:

> covered T_c-class ↔ (Hesse line, pair of lines through c): a bijection onto 36 labels, each Hesse line having 9 codewords over it.

**[N] In Hilbert space** (tolerance 10⁻⁷, on TL₆ braid matrices). The isolated eigenvector of each involution on a 3-dim block gives 9 states with
|⟨a|b⟩|² = **1/4** on all 36 pairs: a **SIC**, the Hesse SIC, on both blocks. Exactly 12 triples are collinear (rank 2). Their 12 dual vectors have overlaps 0 (12 pairs) and
1/3 (54 pairs): **four MUBs**. That second value is the control, since the same procedure does not return 1/4.

Together:

> **216 = 9·12 + 12·9. Relative to a Pauli c, the minimal even line sets of W(3,3) fibre over the Hesse configuration 9₄12₃ of one qutrit: uncovered codewords over the 9
> SIC states, covered codewords over the 12 MUB states.**

The SIC, the MUBs and their duality in d = 3 are classical. The map from the even line sets to them is what is new here, and it is the kind of "cover/quotient
correspondence" the 2026-08-29 no-go said a real bridge would need. The no-go itself stands: the action does not descend through C₃ on codewords. It descends only after
passing to T_c-classes.

### 1 + 2 + 3 + 3 is a stabiliser code with one syndrome blind to Paulis

**[N]** P_c commutes with all three generators, so its three eigenspaces are invariant (no leakage), each of dimension 3. So **P_c stabilises a one-qutrit code and B₄ acts
on its three syndrome spaces.**

- Two syndromes are irreducible 3s (commutant 1). The third is reducible, 1 + 2 (commutant 2).
- **[E/N]** The normal subgroup N of order 27 acts by scalars on the 2-block and is traceless off the centre on a 3-block, with absolute traces 3 (3 elements) and 0 (24).
  So N is a logical Pauli on two syndromes and invisible on the third.
- **[N]** The absolute-character profile on the reducible syndrome is exactly 27 × that of the qutrit Weil representation of SL(2,3), built independently from F and D:
  {1: 15, √3: 8, 3: 1} × 27 = {405, 216, 27}. Control: a 3-block gives a different profile.

So the reducible syndrome carries the **Weil representation of SL(2,3)**, which decomposes as even (dimension 2) + odd (dimension 1). The operator identity behind this is 12524.

**[E] The 2-block is the T′ doublet** in the sense of 12413: normalised to determinant 1 it generates a group of order 24, centre 2, element orders 1¹2¹3⁸4⁶6⁸, with
traces 2, −2, −1, 0, 1. Also σ₁ = ±σ₃ on this block, so it factors through B₃. This refines 12413, which found T′ doublets only on F₃⁴ vectors: here one also sits in the
Hilbert space. **No flavour claim is made.** Nothing connects this doublet to fermions.

## 12520: which matrices are "Cui–Wang's"

Correcting my earlier "exactly Cui–Wang". **[N]** With Cui–Wang's published σ₁, σ₂, σ₃ normalised to reflections, both groups have order 648 and centre 3. An intertwiner exists
(null dimension 1, invertible) for σ⁻¹ and for σ̄, in either generator order, and **none for σ itself**. So the map is an isomorphism with the Shephard–Todd group G₂₅ **only
with the mirror convention**: the native generators match the inverses of theirs.

## 12518: W(3,9) has no hyperoval of at most 46 lines

Coverage-{0,2} even sets are hyperovals of Q(4,q). Fix a chosen line X. There is one further chosen line through each of its q + 1 points: a *star*, a function PG(1,q) → F_q.

**[E]** The radical of Stab(X) acts on stars by evaluating quadratic forms, and it is regular on triples (asserted). So stars modulo the radical are cosets of a [q+1, 3] conic
code, with q^(q−2) normal forms. These are reduced by GL(2,q), the similitude and Frobenius to **2, 4, 24, 511 star classes at q = 3, 5, 7, 9**.

| q | W | classes | result | time |
|---|---|---|---|---|
| 3 | 8 / 10 | 2 | all infeasible / feasible at 10 | < 1 s |
| 5 | 18 / 20 | 4 | all infeasible / feasible at 20 | < 1 s |
| 7 | 38 | 24 | **all infeasible** | 497 s |
| 9 | 46 | 511 | **all infeasible, 0 unknown** | 3534 s |

The direct attempt `q9_le46.py` ran 38,814 s without a decision, so the split made the difference.

**Positive control** (`star48_control.py`): move the known 48-set onto X, read its star, normalise it, find its class. That class comes out OPTIMAL at weight 48. So the chain from
star to class to model does find what is there.

**Consequence.** Any even set of W(3,9) below 48 is not a hyperoval, so it has a point of coverage ≥ 4 and at least 4(q + 1) = 40 lines. That case is closed in 12519. These are CP-SAT
INFEASIBLE verdicts; no independent proof checker was run.

## 12519: the heavy case

An even set with a point x on ≥ 4 chosen lines. **[E]** If x has 2k chosen lines, their further neighbours are pairwise disjoint (no triangles), so the weight is ≥ 2k(q + 1) (the
bound for 2k = 4 is the other track's). So at q = 9, W ≤ 46 every coverage is at most 4.

`heavy_split.py` adds a symmetry break. The group K = q^{1+2}:F_q^* fixes every line through x. It is computed as explicit permutations, with asserts, and it is transitive on the q² lines
meeting a given L₁ off x. So one such line may be fixed, and further lines branched on modulo stabilisers. The four-line orbit split alone is too weak.

| q | W | cases | result |
|---|---|---|---|
| 3 | minimise | 9 | minimum **16** = 4(q + 1), confirmed unsplit (14 infeasible, 16 feasible) |
| 5 | 26 | 13 | **all infeasible**; unsplit finds 28, so minimum **28** > 4(q + 1) = 24 |
| 7 | 38 | 34 | **all infeasible, 0 unknown**, 4728 s |
| 9 | 46 | 42 | **all infeasible, 0 unknown**, 2511 s |

**Positive control** (`heavy_control.py`): a genuine even set with a point of coverage 4 (88 lines, the symmetric difference of the 48-set and a transvection image) is carried through the same
reductions. It lands in listed case 11 and satisfies that case's model, and the solver returns it with the set supplied as a hint. This tests the reductions and the model, not the solver's search.

**Theorem (12518 + 12519, computer proof by CP-SAT).** Every nonzero even line set of W(3,9) has at least 48 lines, and the known 48-set attains this:

| q | 2 | 3 | 4 | 5 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|
| minimum | 6 | 10 | 10 | 20 | 40 | 18 | **48** |

This closes the interval [32, 48]. No independent proof checker was run, and the proof depends on CP-SAT's INFEASIBLE verdicts over 553 cases plus the group reductions, which are asserted in code.
Among heavy sets, 4(q + 1) is tight at q = 3 and not at q = 5. The unsplit q = 5, W = 26 run did not finish, so that infeasibility rests on the split alone, plus agreement at q = 3 and at the
feasible value 28.

## 12522: the q = 7 classification

**Theorem (computer proof by CP-SAT).** The 40-line hyperovals of W(3,7) form **one orbit of PGSp(4,7), of size 720,300, with stabiliser of order 384**, and all of them are cube-family sets.

- `classify_q7.py` enumerates each of the 24 star classes (one CP-SAT worker, because multi-worker enumeration under-counts). 22 classes are empty and class 24 has one set, a cube.
- Class 11905 ran out of time at 38 sets, all cubes, which is not a proof. `classify_q7b.py` finishes it by search and exclusion: find a set, block its whole orbit under the star's stabiliser, repeat. It finds **one orbit of 42 sets, all cubes, then INFEASIBLE** (77 s). The earlier 38 is consistent with this.
- **Counting.** Sets through a fixed line: 343·(168·1 + 1·42) = 72,030, so 72,030·400/40 = 720,300 in total. The two classes contribute 4 : 1, matching the 32 + 8 lines of a cube.
- **Independent cross-check** (`cube_stabiliser_q7.py`). Direct orbit enumeration of one cube under transvections and a similitude, with no solver involved, returns exactly 720,300, so the orbit is everything. 276,595,200 / 720,300 = 384.

**q = 7 minimum.** All 34 heavy cases at W = 38 are INFEASIBLE, so the star and heavy halves together give the minimum 40 by the same method as q = 9. Whether a *heavy* 40-line set exists is reported under `heavy_status` (`q7_W40`). Until that is all INFEASIBLE, this theorem covers hyperovals, not every minimal even set.

## 12523: the 216 minimal codewords are the synthematic totals of the 36 double-sixes

**Prior art, read first.** Pass 173 has the 216 supports, the crown graph K₅,₅ minus a matching, and the 540 skew-line charts. BT855 and BT856 have the K₅ calculus and the "20 dark lines". BT837 has 36 × 6 = 216
"icosahedral cores" in the 36 spreads. Pass 7217 has the 36 doily slices and the K₆ model of six ovoids and six spreads. Pass 11210 has the 36 Kramers reversals and their 15 swapped splits.
`w33_s6_duad_syntheme_pentad_bridge.py` has the abstract duad/syntheme model on the Hoffman–Singleton graph. Pass 11143 has the 16 product and 24 entangled lines. **I did not find these joined to the codewords**, in the corpus or in
the literature I could reach. That is a search result and not a priority claim.

**[E] Five-circuits.** `five_circuit_map.py`: each codeword's S₅ stabiliser fixes exactly one five-circuit of the `2026-08-29` no-go, and transport by PSp(4,3) gives an equivariant bijection of the 216 onto the 216. This upgrades the
stabiliser-and-partition match of 12521 to an explicit map.

**[E] The circuit is the complement.** A codeword covers 20 points. Its five sentinels cover exactly the other 20, each twice, and any two share 2 points. That is why their F₂-sum vanishes. S is exactly the set of lines missing those 20 points, in all 216
cases.

**[E] Each sentinel comes from a grid** (`common_bell_contexts.py`). Each matching pair {L, L′} of the crown graph has 4 transversals sweeping a 16-point grid, and grid − L − L′ is exactly one sentinel H ∪ H⊥, for all 216 codewords.

**[E/N] Entanglement.** Against a factorisation, 24 lines miss H ∪ H⊥ and 16 meet it. In Hilbert space, for an explicit factorisation (tolerance 10⁻⁴ on spectra), the 24 give flat Schmidt spectrum (1/3, 1/3, 1/3) on all 216 states and the 16 give (1, 0, 0) on all
144. So:

> **A minimal codeword is exactly the set of two-qutrit contexts whose bases are maximally entangled with respect to all five factorisations of a zero-sum set.**

The 24/16 count is Pass 11143's. The "simultaneously for five" statement is the addition.

**[E] Sylvester.** `synthematic_totals.py`: the 45 sentinels with "disjoint" form GQ(4,2), its 27 lines are the frames (the 27 lines of the cubic), and there are 36 double-sixes. S₅ has orbits 12 + 15 on the 27. For each double-six the 15 tritangent planes inside the
c_ij are the synthemes, and exactly **6 of their 3003 five-subsets** cover all 15 c_ij: the synthematic totals, any two sharing one syntheme.

> **Every codeword's five sentinels are one total of one double-six, and every total arises exactly once: 216 = 36 × 6.**

**Refuted on the way.** My first guess, that codewords are pairs of skew lines (also 216), is false: S₅ has no orbit of size 2 on the 27.

**[E] Kramers and the doily.** `kramers_doily.py`: the outer coset of PSp(4,3) in PGSp(4,3) has 576 involutions: 540 with 8 fixed points and 36 fixed-point-free. These 36 are the only ones fixing 15 sentinels, and each swaps the factors of all 15, as Pass 11210 found. For each
such θ, the 15 sentinels and 15 frames form a GQ(2,2), with 6 spreads. All 216 codewords occur exactly once.

> **A minimal codeword = a Kramers reversal θ + a spread of the doily of the 15 splits θ swaps.**

A doily is the geometry of the two-qubit Pauli group, so a two-qubit geometry sits inside the two-qutrit one here. This is a combinatorial isomorphism **[I]**: no two-qubit Hilbert space is constructed.

**[E] Two sides of the outer automorphism.** `codeword_vs_spread.py`, GAP in `gap_a5.out`: each codeword fixes one spread and is disjoint from it, and meets the other 35 in 2 or 3 lines. Its A₅ has line orbits [5, 5, 10, 20]: the two pentads, that spread, and the 20 dark lines. BT837's cores have [10, 30].
GAP confirms these are **the two classes of A₅ in A₆**. So BT837's 216 cores and these 216 codewords are the letters and the totals of the double-six, exchanged by the outer automorphism of S₆, which PSp(4,3) does not realise.

**[E] A sharper Hesse statement** (`pair_of_sic.py`). Uncovered T_c-classes biject with the **36 unordered pairs of Hesse SIC points**: c lies in exactly two sentinels of the circuit, and the codeword's stabilising involution is the third point on that pair's affine line. This simplifies the (involution, line) labelling of 12521.

**Does it generalise?** `bell_generalisation.py`. At q = 3, 5, 7, 9 the minimal set's uncovered points are exactly the union of the factorisations it misses (5, 40, 87, 330 of them), and S is exactly the set of lines in its covered points. Those are data, without a theorem. The zero-sum five-set is specific to
q = 3 so far. The control of random line sets misses far fewer, but those cover more points, so it is not a fair baseline.

## 12524: the syndrome-controlled Pauli

**[N]** `syndrome_theorem.py`, on the 648 explicit 9 × 9 unitaries. Let Π_s be the P_c eigenprojectors, with s = 0 the reducible syndrome, and transport syndromes by a Pauli that does not commute with P_c. For every u in the order-27 normal subgroup N:

> u = ⊕ₛ λₛ Lˢ, with L a Weyl operator of the logical qutrit.

Exactly 27 elements are scalar on s = 0, so outside N nothing is. On s = 1 they give **9 operators modulo phase, an orthogonal basis**; on s = 2 they give L⁻¹. This proves the operator identity that 12521 only labelled as an interpretation.

## 12525: stabilisers and a second solver

**[E] GAP** (`gap_stab.out`), on line permutations of PΓSp(4,q):

| q | minimal set | stabiliser | structure | derived | orbit on lines | orbit size |
|---|---|---|---|---|---|---|
| 3 | 10-set | 120 | S₅ | A₅ | 10 | 216 |
| 7 | 40-set | 384 | **D₁₆ × S₄**, SmallGroup(384,18032) | C₄ × A₄ | 8 + 32 | 720,300 |
| 9 | 48-set | 1920 | A₅:(C₈:(C₂ × C₂)) | C₄ × A₅ | 48 | 3,586,680 |

The q = 7 row is the third independent count of 720,300. The S₄ is the cube's rotation group, matching 12515, and q = 9 is icosahedral.

**Correction to Pass 12501.** "Stabiliser of order 480" was the stabiliser inside GL(2,9).2 only, which omits the similitude and Frobenius. The full stabiliser in PΓSp(4,9) has order 1920.

**Second solver.** `recheck_cadical.py` uses CaDiCaL, a CDCL SAT solver sharing no code with CP-SAT. It reproduces the star verdicts at q = 3 and q = 5 (W = 8 and 18 UNSAT; W = 10 and 20 SAT in exactly one class, matching CP-SAT). Status at q = 7 is under `second_solver`. **It is not a proof certificate**, and the q = 9 theorem still rests on CP-SAT alone.

**q = 9 uniqueness.** GAP's numbers predict that if the 48-set is unique up to symmetry, exactly one star class is feasible at W = 48, with 288 sets through X modulo the radical. `classify_q9.py` tests this; status under `classify_q9`.

**Literature.** De Bruyn (ICMS 2020) lists W(3) and Q(4,3) among the quadrangles whose hyperovals can be classified, and Pasechnik's paper used computer classification for both. I did not find the values for q = 7, 9 or the Sylvester identification, but I could not read every candidate in full, so these are not claimed as new to the literature.

## What this does not do

No claim here concerns particles, forces or constants. The dictionary is one-qutrit quantum information sitting on a finite geometry, and the choice of c is external: nothing here selects a
point (compare `2026-10-22_anchored_transvection_hamiltonian.md`).

## Sources

- S. X. Cui, Z. Wang, *Universal quantum computation with metaplectic anyons*, J. Math. Phys. 56 (2015), arXiv:1405.7778.
- B. De Bruyn, *Classification results for hyperovals of generalized quadrangles*, ICMS 2020.
- D. V. Pasechnik, *The triangular extensions of a generalized quadrangle of order (3,3)*, Bull. Belg. Math. Soc.
- Corpus: Pass 173; BT837; BT855; BT856; Pass 7217; Pass 11143; Pass 11210; Pass 1047; 12413; 12507–12516; `2026-08-29_216_CLIFFORD_TORSOR_NOGO.md`; `2026-09-21_physical_a2_clifford648_w33_bridge.md`.
