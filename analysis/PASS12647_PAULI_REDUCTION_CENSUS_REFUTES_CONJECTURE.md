# Pass 12647: three qubits exact to 10⁻⁶ (min F ∈ [1/8 − 10⁻⁶, 1/8]) via a Pauli-reduced SOS; a larger census refutes "mirror partner ⟺ ϑ > α"; four-qubit maximal sets of size 8 and 5 exist, and the size-5 set has a non-stabiliser optimum

Claude track. Follows Passes 12642–12646. **Not a theory of everything.**

## 0. Corrections first

1. **Pass 12646's conjecture is false.** I stated, and labelled as a conjecture, that a set has a mirror partner if and only if ϑ > α. A census of 23 invariant classes of four-qubit maximal partial spreads (`w33_four_qubit_greedy_census.py`) breaks both directions:

   | (partner, ϑ > α) | classes |
   |---|---|
   | (no, no) | 17 |
   | (yes, yes) | 3 |
   | **(no, yes)** | **2** (n_inside 28, m* = 3, ϑ = 12.46 > 12; n_inside 22, m* = 2, ϑ = 13.016 > 13) |
   | **(yes, no)** | **1** (n_inside 24, 2 partitions, ϑ = 14.000 = α) |

   The rule fitted every case in Pass 12646 only because the sample was small, five sets. *Vary the sample before believing* (memory: feedback_vary_the_sample_before_believing).
2. **The nine-element four-qubit sets are not the smallest.**
   - Randomised greedy produces maximal partial spreads of size **8**: 96 of 443 runs, 4 invariant classes, all with ϑ = α = 14 (m* = 1).
   - Kantor (*On maximal symplectic partial spreads*, Adv. Geom. 2017, Introduction) reports that Grassl gave maximal symplectic partial spreads of size q^{n/2} + 1 for all even n and q. In V(8, 2) that is **size 5**.
   - The sizes 9 and "d/2 + 1" in Passes 12644–12646 come from a time-limited integer program (dual bound 2) and from Mandayam et al.'s construction size, not from minimality. The exact results for those specific sets stand. The framing "minimal" or "d/2 + 1" should be read as "the sets studied".
   - A direct feasibility run for size 3 timed out (900 s); sizes 5 and 4 are rerunning.

## 1. The three-qubit certificate: Pauli reduction (`w33_threequbit_pauli_reduced_sos.py`)

F and |v|² are invariant under the three-qubit Pauli group. On both SOS spaces, the degree-3 monomials (Sym³, 120) and the monomials v_i v_j v̄_k (288), the centre acts as −1, so each space is 8 copies of the unique 8-dimensional irrep.
- An invariant Gram matrix is block-diagonal over the Z-sectors s = i ⊕ j ⊕ k, and the sector-a block is the X^a-translate of the sector-0 block.
- So the certificate reduces to **K₀ (15×15) and G₀ (36×36)**.
- In the unnormalised monomial basis every coefficient is a Gaussian rational (8|e⟩⟨e| has Gaussian-integer entries).

**Result:** δ* = 0.12499999997, solved in 1.3 s (the unreduced SDP took 367 s).

## 2. The face of the certificate (`w33_threequbit_exact_one_eighth.py`, `w33_threequbit_minimiser_variety.py`, `w33_threequbit_kernel_projector.py`)

- **K₀ = 0 is forced.** The degree-3 monomial vectors of the 160 stabiliser minimisers (20 Lagrangians meeting C once, × 8 states), shifted through all 8 sectors, span all of C¹⁵. So the whole certificate is a sum of squares of the monomials v_i v_j v̄_k:

  F(v)|v|² − |v|⁶/8 = q(v)† G q(v), with G = ⊕ (translates of G₀).

- **G₀ has a 20-dimensional kernel from the minimisers**, leaving a 16×16 block Y. Numerically Y has rank 16.
- **Minimisers are not isolated.** Of 300 random-start minima at F = 1/8, 299 are **not** stabiliser states. Each has exactly one Pauli with |⟨P⟩| = 1, always one of **15** particular uncovered Paulis. These match the 15-vertex class of the coherent closure, though that identification was not checked vertex by vertex.
- **They form a sub-variety, not whole eigenspaces:** random states in those eigenspaces have F ≥ 0.142.
- **They add no new kernel.** Their q-vectors lie in the same 20-dimensional span (numerical rank 20 with gtol 10⁻¹³). An earlier "rank 25" came from imprecise minima and is withdrawn.
- **The rounding obstruction.** With the 20-dimensional kernel imposed, the interior margin of Y is about 0 (2×10⁻⁶). Rounding then satisfies all 3,464 coefficient equations exactly (rank 100 of 256 unknowns) but leaves Y slightly indefinite at every denominator up to 4096. The optimal face is smaller than any point family certifies, which is the signature of a second facial-reduction step.

**Second facial-reduction step** (`w33_threequbit_second_facial_reduction.py`). The auxiliary dual returns Ω ≈ I/16, full rank, with solver status "inaccurate". With the zero primal margin, the most consistent reading is that **the degree-6 bound 1/8 is approached but not attained** inside this face. No exact degree-6 certificate at exactly 1/8 was found, and none may exist. This is a reading, not a proof.

## 2b. Exact bound to within 10⁻⁶ (`w33_threequbit_epsilon_exact.py`, `data/w33_threequbit_epsilon_exact.json`)

Certify δ = 1/8 − ε instead, using the full Pauli-reduced blocks (K₀ 15×15, G₀ 36×36):
- maximise the interior margin;
- round to Gaussian rationals with denominator 16;
- solve the pivot variables exactly from an exact rref;
- verify every coefficient equation in exact integer arithmetic;
- check both blocks by exact LDLᵀ.

| ε | interior margin (units of 64·Gram) | exact certificate |
|---|---|---|
| 10⁻³ | 0.0682667 | **yes** (D = 16) |
| 10⁻⁴ | 0.00682667 | **yes** |
| 10⁻⁵ | 0.000682667 | **yes** |
| 10⁻⁶ | 0.0000682667 | **yes** |

> **Theorem (exact).** For every size-5 three-qubit Pauli MUB set (all 24,192, one orbit) and every v ∈ C⁸:
> Σ_e (|⟨e|v⟩|² − |v|²/8)² ≥ (1/8 − 10⁻⁶)|v|⁴.
> Stabiliser states of the Lagrangians meeting C once give exactly 1/8, so **min F ∈ [1/8 − 10⁻⁶, 1/8]**.

The margin is exactly linear, (1024/15)·ε. That is consistent with the margin coming entirely from the added ε|v|⁶ term, with the degree-6 SOS at exactly 1/8 on the boundary. This replaces (3 − √5)/8 (Pass 12643) as the best exact three-qubit bound. The Lovász route stays the computer-algebra-light one.

## 2c. Four qubits: a size-5 maximal set, with a non-stabiliser optimum (`w33_four_qubit_small_sizes.py`, `w33_four_qubit_size5_exact.py`)

A feasibility integer program (124 s) found a **size-5** maximal partial spread of W(7,2), lines [129, 190, 287, 444, 530]: Grassl's size q^{n/2} + 1 (Kantor 2017).
- 180 uncovered Paulis; m* = 1, so the stabiliser value is 1/16.
- ϑ = 14.785 > α = 14.
- **Numerical min F = 0.05236 < 1/16**: a non-stabiliser optimum, like the two-qutrit pentads and the d = 25 single covers.

**Exact strong unextendibility.** The rounded Lovász dual of the 180-vertex uncovered graph passes an exact LDLᵀ check of (74/5)I − J − T ⪰ 0 (D = 65536), so ϑ ≤ 74/5. Hence

> **F(v) ≥ |v|⁴/80 for every v ∈ C¹⁶**, for this five-basis set in d = 16 (exact; numerical minimum 0.0524).

So a **strongly unextendible set of only 5 Pauli MUBs exists in d = 16**: as few bases as at d = 8 and d = 9. The looser target 14.85 also passes (D = 16384, F ≥ 3/320). The 14.9 attempt failed only because D = 4096 rounding is too coarse for 180 vertices. Prior art: Grassl's size-5 maximal partial spreads (via Kantor 2017) are weak-unextendibility objects; no strong-unextendibility statement for them was found in the sources checked.

Sizes 4 and 3 were not decided: both feasibility integer programs hit their time limits.

## 3. What stands

- **d = 4:** min F = 1/4, exact.
- **d = 8:** min F ∈ [1/8 − 10⁻⁶, 1/8] exactly (§2b). An exact certificate at exactly 1/8 is not available at degree 6 by the methods tried.
- **d = 16:** five sets with exact min F = m*/16 (Passes 12645–12646). In the census every class has min F equal to its stabiliser value; this was checked numerically for the Pass 12646 sets, not for all 23 classes.
- **Mirror pairs:** they exist at d = 8 (all sets) and in some d = 16 sets. They are **unrelated** to whether the Lovász bound is tight (§0).

## Open

- Whether the degree-6 SOS attains 1/8 (the evidence suggests not); a degree-8 certificate or a structural proof of 1/8.
- Whether sizes 5, 4 or 3 occur in W(7,2), and what min F is for them.
- What the 15 fixed Paulis of the minimiser variety are geometrically.
