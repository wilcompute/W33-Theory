# Passes 12518–12525: the q = 9 minimum is 48; the four-anyon braid image is the centraliser of the next generator; the 216 codewords carry the Hesse configuration

Claude track. Producer: `analysis/w33_pass12518_to_12525_hesse_dictionary.py`. Test: `tests/test_w33_pass12518_to_12525.py`. Drivers in
`analysis/search_drivers_12466`: `star_cubes.py`, `star48_control.py`, `heavy_cases.py`, `heavy_split.py`, `heavy_control.py`, `classify_q7.py`, `cuiwang_compare.py`,
`braid_point_stabiliser.py`, `hesse_dictionary.py`, `hesse_dictionary2.py`, `hesse_dictionary3.py`, `tprime_block.py`.

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

**Not established:** an explicit bijection between our codewords and those five-circuits. The evidence is the shared stabiliser profile and orbit partition.

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

So the reducible syndrome carries the **Weil representation of SL(2,3)**, which decomposes as even (dimension 2) + odd (dimension 1). A "syndrome-controlled Pauli" reading,
with exponent zero on that syndrome, fits these facts **[I]**; the operator identity itself was not written out.

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
| 9 | 46 | 42 | **all infeasible, 0 unknown**, 2511 s |

**Positive control** (`heavy_control.py`): a genuine even set with a point of coverage 4 (88 lines, the symmetric difference of the 48-set and a transvection image) is carried through the same
reductions. It lands in listed case 11 and satisfies that case's model, and the solver returns it with the set supplied as a hint. This tests the reductions and the model, not the solver's search.

**Theorem (12518 + 12519, computer proof by CP-SAT).** Every nonzero even line set of W(3,9) has at least 48 lines, and the known 48-set attains this:

| q | 2 | 3 | 4 | 5 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|
| minimum | 6 | 10 | 10 | 20 | 40 | 18 | **48** |

This closes the interval [32, 48]. No independent proof checker was run, and the proof depends on CP-SAT's INFEASIBLE verdicts over 553 cases plus the group reductions, which are asserted in code.
The q = 7 status at W = 38 is in the JSON under `heavy_status`.

Among heavy sets, 4(q + 1) is tight at q = 3 and not at q = 5. The unsplit q = 5, W = 26 run did not finish, so that infeasibility rests on the split alone, plus agreement at q = 3 and at the
feasible value 28.

## 12522: the q = 7 classification

`classify_q7.py` enumerates all 40-line hyperovals in each star class (one CP-SAT worker, because multi-worker enumeration under-counts) and applies `cube_recognise`. If complete, it decides
whether every optimum at q = 7 is a cube-family set. Status under `classify_status`. Any non-OPTIMAL class means no theorem.

## What this does not do

No claim here concerns particles, forces or constants. The dictionary is one-qutrit quantum information sitting on a finite geometry, and the choice of c is external: nothing here selects a
point (compare `2026-10-22_anchored_transvection_hamiltonian.md`).

## Sources

- S. X. Cui, Z. Wang, *Universal quantum computation with metaplectic anyons*, J. Math. Phys. 56 (2015), arXiv:1405.7778.
- Corpus: Pass 173; Pass 1047; 12413; 12507–12516; `2026-08-29_216_CLIFFORD_TORSOR_NOGO.md`; `2026-09-21_physical_a2_clifford648_w33_bridge.md`.
