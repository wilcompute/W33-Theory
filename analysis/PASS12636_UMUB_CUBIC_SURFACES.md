# Pass 12636: every unextendible set of two-qutrit Pauli MUBs is a piece of cubic-surface geometry; a codeword is a chiral pair of positive-geometry regions

Claude track. Scripts: `analysis/w33_pentad_umub.py` (`data/w33_pentad_umub.json`) and `analysis/w33_pezzotope_reflection.py` (`data/w33_pezzotope_reflection.json`). Continues Passes 12634–12635.

**Not a theory of everything.** The results are exact finite combinatorics plus one explicit Hilbert-space check.

## 1. The spectrum of unextendible Pauli MUB sets in dimension 9

Lines of W(3,3) are the maximal commuting classes of two-qutrit Paulis, and disjoint lines give mutually unbiased stabiliser bases. A maximal partial spread is therefore a *weakly unextendible* set of Pauli-class MUBs (Mandayam, Bandyopadhyay, Grassl and Wootters, arXiv:1302.3709; Thas, arXiv:1407.2778).

**Hilbert-space check.** Common eigenbases were built from X^a Z^b ⊗ X^c Z^d. Unbiasedness (|⟨a|b⟩|² = 1/9) coincides with disjointness for all 780 pairs of lines. A pentad gives 5 MUBs, and no Pauli-class basis is unbiased to all five.

**Exhaustive enumeration (Bron–Kerbosch).** Maximal partial spreads of W(3,3) come in **exactly three sizes**:

| size | count | in the tropical / positive geometry of cubic surfaces |
|---:|---:|---|
| 10 (complete MUB sets, spreads) | 36 | the 36 positive roots = type-(a) rays = double-sixes |
| **8** | **135** | **the 135 aaaa maximal cones** of the Naruki fan (orthogonal root 4-frames = 45 D4 × 3) |
| **5** | **432** | **the 432 E6 pezzotopes**, the positive-geometry regions (two chiralities of 216) |

- **Size 10 ↔ roots** (Pass 12635): the 10 A2³ containing a root form a spread.
- **Size 8 ↔ orthogonal frames, bijectively.** For each size-8 set, its 8 A2³ subsystems give the same root multiplicity profile: 4 roots in 6 of them, 24 roots in 2, and 8 roots in none. The 4 roots of multiplicity 6 always form an orthogonal 4-frame, and the 135 sets give the 135 distinct frames.
- **Size 5 ↔ pezzotopes**: Pass 12634 addendum 4.

There is **no size 7**. Thas's general construction ("ℓ² − ℓ + 1 or ℓ² − ℓ + 2", i.e. 7 or 8 at ℓ = 3) can only give 8 here. Thas, and Mandayam et al., state no size-5 or size-8 two-qutrit examples explicitly. The finite-geometry size spectrum is probably in Cimráková and Fack's exhaustive searches (q ≤ 5); I did not read their tables.

## 2. Chirality is one Weyl reflection, and a codeword is a left-right pair

For each of the 216 (double-six, synthematic total) pairs, both tests hold in all 216 cases:
- **Reflection.** The reflection s_α in the double-six's root α (determinant −1, so in the outer coset of PSp(4,3)) maps the left pezzotope to the right one. Control: a reflection in a root orthogonal to α never does (0/216).
- **Codeword.** The union of the two pentads is 10 lines covering 20 points twice each and missing the other 20: an even line set, and the 216 unions are distinct. Pass 173 certifies exactly 216 minimal even line sets of W(3,3), the corpus's codewords, so **each codeword is a left and a right positive-geometry region glued together.**

Pass 12523 characterised a codeword as "a Kramers reversal θ + a doily spread", and the 36 Kramers reversals are the 36 fixed-point-free outer involutions, one per double-six. The reflection s_α is the natural candidate for θ. I have not checked their identity element by element.

## Prior art

- The double-six, total and pentad structure: Pass 12523, BT837, BT844/BT845.
- The 216 even sets: Pass 173.
- UMUBs and the partial-spread dictionary: Mandayam et al., Thas.
- The size spectrum of maximal partial spreads of W(3,3): probably Cimráková and Fack.

**New here:** the three-way identification of the whole spectrum {10, 8, 5} with roots, aaaa cones and pezzotopes; the chirality-as-reflection test; and codeword = chiral pezzotope pair.

## Addendum: the E7 rung does not lift naively (`w33_e7_rung_mubs.py`, negative result)

E7 corresponds to three qubits: W(E7) = Z₂ × Sp(6,2), and W(5,2) is the three-qubit Pauli geometry. W(5,2) has 135 Lagrangian planes (the maximal commuting sets, matching E7's 135 orthogonal 7-frames), and each is disjoint from 64 others.

**All maximal partial spreads of W(5,2)**, i.e. weakly unextendible three-qubit Pauli MUB sets, enumerated exhaustively:
- **size 9:** 960, one Sp(6,2)-orbit, stabiliser of order 1512 (the classical spreads);
- **size 5:** 24,192, one orbit, stabiliser of order 60 (A5).

**Prediction tested and failed:** the E7 pezzotope count 60,480 = |Sp(6,2)|/24 does not occur as an orbit. The E7 positive-geometry regions are not unextendible three-qubit MUB sets, and the E6 coincidence (regions = size-5 unextendible sets) does not carry over as stated.

**What does carry over:** W(5,2) has two size classes (5 and 9), and W(3,3) has three (5, 8 and 10). In both, the smallest unextendible sets have size 5, with S5 symmetry for two qutrits and A5 for three qubits. Mandayam et al. report unextendible Pauli MUBs in d = 8, so the three-qubit size-5 sets are probably prior art.

## Addendum 2: the size-8 sets are the entangled bases of a factorisation (`w33_size8_splits.py`, `data/w33_size8_splits.json`)

**The chain.** A size-8 set gives an orthogonal root frame (via its multiplicity-6 roots), the frame spans a D4, and the D4 is a tensor split (Pass 12635 dictionary). This chain sends the 135 size-8 maximal partial spreads **3-to-1 onto the 45 tensor splits**: these are the corpus's 135 "splits" (45 × 3).

**For every split {b, b⊥}**, a factorisation C⁹ = C³ ⊗ C³ with b and b⊥ the two local Pauli groups (all 45 cases):
- all 8 lines of each of its three size-8 sets miss b ∪ b⊥;
- the three sets are pairwise disjoint;
- together they are **exactly the 24 lines missing b ∪ b⊥**;
- the other 16 lines meet both b and b⊥.

The 16/24 split is Pass 11143's: product contexts, and contexts whose eigenbases are maximally entangled with respect to the factorisation (Pass 12523 checked the flat Schmidt spectra).

> **For every factorisation of two qutrits, the 24 maximally entangled stabiliser bases split into exactly three unextendible sets of 8 mutually unbiased bases. These 135 sets are all the weakly unextendible 8-MUB sets in dimension 9.**

**Status.** Exact on all 45 splits. Entanglement patterns of complete MUB sets have been studied in the literature (Lawrence; Wieśniak et al.). Whether this three-way partition is stated there is not checked. Corpus prior: Pass 11143 (16 + 24).

## Addendum 3: the pezzotope amplitude factorises into 6-particle φ³ amplitudes, with contexts as the 3-particle channels (`w33_pezzotope_amplitude.py`)

Take a simple 4-polytope with a variable X_f for each facet. Its amplitude is m = Σ over vertices of Π 1/X_f, and the residue of m at X_f = 0 is the amplitude of facet f.

**For all 432 E6 pezzotopes:**
- 45 vertices;
- every **cube (cusp) facet** has 8 vertices: a product of three two-point factors;
- every **root facet** has 14 vertices and 9 neighbours (6 roots and 3 cusps). Its compatibility graph is isomorphic to the non-crossing graph of the 9 diagonals of a hexagon **with the 3 cusps on the 3 long diagonals** (types matched in the isomorphism).

**Reading.** On each of its 10 double-six facets, a pezzotope's amplitude has the residue of a **6-particle tree-level φ³ amplitude** (the associahedron K₅):
- the **3 three-particle channels** are the 3 adjacent cusp facets, i.e. 3 maximal commuting two-qutrit contexts (lines of W(3,3));
- the **6 two-particle channels** are the 6 orthogonal root facets, i.e. double-sixes or complete MUB sets.

Long diagonals never cross-compatibly coexist, matching the fan fact that no cone holds two cusp rays. That the facets are associahedra and cubes is Early, Geiger, Panizzut, Sturmfels and Yun's. The channel-type identification with two-qutrit objects is this addendum's.

**Prior art added to this pass.** A size-5 maximal partial spread of W₃(3), unique as a neighbour-transitive code, appears in arXiv:2105.05833. The full size spectrum {5, 8, 10} could not be checked against Cimráková and Fack's tables, which were not accessible. The cone-by-cone identity of the reconstructed Naruki fan, the identification of the real regions with the pentads by facet labels, and the index-3 chirality class are the other track's (779cc43ba, `analysis/2026-11-09_yoshida_integral_fibers_and_chirality.md`).
