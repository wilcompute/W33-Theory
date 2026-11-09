# Pass 12637: the six particles are a six; no lifted hidden zeros; strongly unextendible MUBs; triality needs the antiunitary coset; an E7 candidate; the q-ladder

Claude track. All scripts are in `analysis/`, with JSON outputs in `data/`. Continues Passes 12634–12636 and the other track's Yoshida and canonical-form packets (779cc43ba, 3dd4b78cb), which are cited, not repeated.

**Not a theory of everything.**

## 1. The six external particles (`w33_six_particles.py`, all 4320 root facets of the 432 pezzotopes)

On each double-six facet the pezzotope amplitude restricts to the 6-point φ³ tree (Pass 12636 addendum 3). Results:
- The 6 neighbouring roots always form a 6-cycle under "never in a common vertex", the crossing pattern of a hexagon's short diagonals.
- Each neighbouring root pairs non-trivially with exactly 2 lines of each six. These duads form a Hamiltonian 6-cycle on the six, and the same duads appear in both sixes under the double-six pairing.
- Two channels cross exactly when their duads share a line.

> **The six particles are the six lines of a six, in a cyclic order. The channel s_{i,i+1} is the root of the duad (aᵢ, aᵢ₊₁), and the three-particle channels are the three adjacent two-qutrit contexts.**

With these labels, the residue of the full amplitude on each facet vanishes at that facet's φ³ hidden zero (1200/1200). This is an independent check of the labelling.

## 2. Hidden zeros do not lift (`w33_pezzotope_hidden_zeros.py`; negative)

- **Control.** A₆ vanishes at c₁₃ = c₁₄ = c₁₅ = 0 (Arkani-Hamed, Cao, Dong, Figueiredo and He) and is nonzero at random points.
- **One facet.** With one facet's hexagon zero imposed, the full 15-variable amplitude is nonzero (0/400 zeros).
- **Two or three facets.** Simultaneous zeros on 2 or 3 facets, over all 6 rotations each, gave 44 apparent zeros at a single random point. **None survived six fresh points**, so they were accidental zeros on sub-loci, not identities.
- **Conclusion.** The pezzotope amplitude has no hidden zeros lifted from its facets' φ³ zeros (k ≤ 3).

## 3. Item 3: standalone note

`analysis/NOTE_TWO_QUTRIT_UNEXTENDIBLE_MUBS.md` is written for quantum-information readers. Literature placed: Mandayam–Bandyopadhyay–Grassl–Wootters, Thas, Szántó, arXiv:2105.05833.

## 4. Strongly unextendible MUBs (`w33_pentad_strong_umub.py`; outside-the-box 1)

| set | min Σ(\|⟨e\|v⟩\|² − 1/9)² |
|---|---:|
| 4 bases of a complete set (control) | 9×10⁻¹⁸ |
| every 4-subset of a pentad | ≤ 7×10⁻¹⁸ |
| **pentads** | **0.147114** (3 sets × 200 starts) |
| **size-8 sets** | **0.4444** (3 sets × 80 starts) |

- The pentads appear to be **strongly unextendible 5-MUB sets in d = 9**, with no vector unbiased to all five. **[N]**: numerical, not a proof.
- Szántó (arXiv:1502.05245) constructs strongly unextendible 8-MUB sets in dimension p² (p ≡ 3 mod 4), consistent with the size-8 result. A 5-set is not reported there.
- The minimum 0.14711376… has no recognised closed form; none is claimed.

## 5. Triality (`w33_split_triality.py`; outside-the-box 2)

For each of the 45 factorisations, consider the stabiliser's action on the three entangled 8-MUB classes:
- in PSp(4,3) the stabiliser has order 576 and its image is **Z₃**;
- in PGSp(4,3) it has order 1152 and its image is **S3**, and the **transpositions come only from the outer (antiunitary) coset** (45/45).

D4 triality on the three frames is realised inside the two-qutrit Clifford group. Its odd part requires the antiunitary coset, the same coset that carries the corpus's chirality (Pass 346; e92a047).

## 6. The E7 rung: a candidate (`w33_e7_orbit_census.py`, `w33_e7_scalene.py`; item 4 + outside-the-box 3)

Sp(6,2) has 12 orbits on triples of three-qubit maximal commuting sets (Lagrangian planes of W(5,2)).
- **Exactly one has size 60,480**, the E7 pezzotope count. It is the triples with pairwise intersection dimensions (0, 1, 2).
- Its exact stabiliser (inside GL(3,2) acting on a complementary pair) is **S4**: order 24, with element orders 1:1, 2:9, 3:8, 4:6. This matches the S4 diagram symmetry in the E7 region count.
- Its point orbits are [1, 3, 3, 4, 4, 6, 6, 12, 12, 12], which can supply the 10 root facets in more than one way.
- **Status:** a candidate (unique orbit, stabiliser S4), not an identification. The facet test is not done.

## 7. The q-ladder (`w33_q_ladder.py`; item 5)

Double-perp sizes for W(3,q) points against Q(4,q) points:
- q = 2: 3 / 3, self-dual;
- q = 3: 4 / 2;
- q = 5: 6 / 2.

The Satake boundary of A₂(q) carries both halves for every q: 1-cusps are points and 0-cusps are Lagrangian planes. At level 2, the self-dual case, the Segre and Igusa fans coincide. At level 3 a *second* moduli space, cubic surfaces, carries the line half alone, through W(E6) ≅ PGSp(4,3). At q = 5 no Weyl-group partner exists, so the level-3 split is an exceptional coincidence, not a series.
