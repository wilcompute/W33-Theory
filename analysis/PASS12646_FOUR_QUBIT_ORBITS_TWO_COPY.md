# Pass 12646: at least five orbits of nine-element four-qubit Pauli MUB sets, all with min F = m*/16; four certified exactly; mirror partner ⟺ ϑ > α so far; two copies do not help

Claude track. Follows Passes 12643–12645. **Not a theory of everything.**

## 1. Census of d = 16 nine-sets (`w33_four_qubit_set_census.py`, `w33_four_qubit_minF_census.py`)

Five size-9 maximal partial spreads: the saved one plus four from random-objective integer programs, each excluding the earlier ones.

| # | Lagrangians inside C | partitions of C | m* | ϑ | α = 15 − m* | numerical min F | exact certificate |
|---|---|---|---|---|---|---|---|
| 0 (saved) | 17 | 1 | 1 | 14.000000 | 14 | 0.0625 | **1/16, D = 4** (P12645) |
| 1 | 26 | 1 | 2 | 13.000000 | 13 | 0.125 | **1/8, D = 4096** (1,712 equations, rank 1,592) |
| 2 | 14 | 1 | 1 | 14.000000 | 14 | 0.0625 | **1/16, D = 16** |
| 3 | 32 | **2** | 2 | **13.011** | 13 | 0.125 | Lovász not tight |
| 4 | 12 | 1 | 1 | 14.000000 | 14 | 0.0625 | **1/16, D = 8** |

**Readings.**
- **At least five Sp(8,2)-orbits.** Every sample has a different number of Lagrangians inside C. Unlike d = 8, where the minimal sets form a single orbit, the d = 16 minimal sets are many. Five samples give five orbits, so the total is unknown.
- **min F = m*/16 in every sample**, i.e. the stabiliser value. No non-stabiliser optimum occurs at d = 16 in these samples.
- **Mirror partner ⟺ ϑ > α in every case examined.** Set 3 is the only sample with a mirror partner, and the only one whose Lovász number exceeds α (13.011 against 13, beyond solver precision). At d = 8 every set has a partner and ϑ = 4 + √5 > 6 = α. This is an observation on these cases, not a theorem, though a mechanism is plausible: a partner shares C, hence shares U, and a second structure on the same U may supply the extra vector-chromatic room. **Labelled a conjecture.**
- **Exact certificates** for sets 1, 2 and 4, plus set 0 from Pass 12645: facial reduction with α-set slackness, rounded at D = 4096, 16 and 8 respectively, then an exact rational LDLᵀ check. Set 1 (m* = 2) has 16 maximum independent sets. **Four inequivalent d = 16 sets have exact min F (1/16, 1/16, 1/16, 1/8).**

## 2. Two copies do not help (`w33_two_copy_lovasz.py`)

The idea was to bound (Σ_U ⟨P⟩²)² by the Lovász number of the 784-vertex anticommutation graph G₂ on the operators P⊗Q.
- **Control, two qubits:** ϑ(G₂) = 6 > 4 = ϑ(G)².
- **Three qubits:** ϑ(G₂) ≤ 38.98 ≈ ϑ(G)² = 38.89 (coherent-closure dual), so √ϑ(G₂) = 6.244 and nothing is gained.

**Mechanism:** the inequality holds for all two-copy states, including entangled ones. All 28 operators P⊗P commute, for instance, so Bell-type states score highly on them. The product structure of ψ⊗ψ is lost. **Negative result.**

## 3. The 1/6 level of the d = 25 optimiser (`w33_d25_sixth_level.py`)

The 144 Weyl vectors with |⟨W_u⟩| = 1/6 (deviation 3.6×10⁻⁹) are 36 whole points.
- They contain 6 full lines, hence form a **6-line partial spread** (6 × 6 = 36 forces disjointness).
- 12 of the 36 points are covered; 6 of the 14 covered lines meet the spread in 2 points each.

So the optimiser has |⟨W_u⟩| = 1/6 uniformly on a 6-line partial spread, which gives a concrete ansatz for proving 13/75. Not pursued to a proof.

## 4. Replay check

The other track's commits since Pass 12645 concern flux and dark-mode results; there is **no replay yet** of the requested certificates (handoff of Pass 12645).

## Not done

- **Exact three-qubit 1/8:** the two-copy route fails (§2). The remaining route is symmetry-reduced degree-6 rounding.
- **Five qubits:** W(9,2) has 75,735 Lagrangians and 1,023 points. The transvection-orbit construction and the integer program used at four qubits do not scale in pure Python. A constructive route (Mandayam et al.'s d/2 + 1 construction) would be needed.


---

**Correction (Pass 12647, 2026-11-12).** The conjecture "mirror partner ⟺ ϑ > α" is **refuted** by a 23-class census: 2 classes have ϑ > α but no partner, and 1 has a partner but ϑ = α (`data/w33_four_qubit_greedy_census.json`). The nine-element sets are also not minimal. Maximal partial spreads of size 8 (greedy) and size 5 (integer program; Grassl's size, per Kantor 2017) exist. The exact certificates above stand for the sets they name.
