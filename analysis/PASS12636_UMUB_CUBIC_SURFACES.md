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
