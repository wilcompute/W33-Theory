# Pass 12648: the smallest four-qubit maximal Pauli MUB sets have exactly 5 elements (105,283,584 sets, two types: lifted and genuine); a paper draft

Claude track. Follows Pass 12647. **Not a theory of everything.** The parallel track has been working on monopoles and thresholds (6950c50e1, 128cbc4fd); there is no overlap.

## 1. Sizes 3 and 4 do not occur (exhaustive) (`w33_exhaustive_small_maximal_spreads.py`)

By Witt's theorem, Sp(2n,2) is transitive on ordered pairs of complementary Lagrangians. So every maximal partial spread of size ≥ 2 is equivalent to one containing a fixed pair (L₀, L₁), and the remaining Lagrangians are enumerated completely.

| n (qubits) | size 3 | size 4 | size 5 through the fixed pair |
|---|---|---|---|
| 2 (control) | exists (1) | — | — |
| 3 (control) | none | none | 56 |
| **4** | **none** | **none** | **896** |

**Count check at n = 3.** 24,192 × 20 ordered pairs / (135 Lagrangians × 64 complementary partners) = 56, matching exactly.

> **The smallest maximal partial spread of W(7,2) has size exactly 5** (= q^{n/2} + 1, Grassl's size, per Kantor 2017). Total number of size-5 sets: 896 × (2295 × 1024) / 20 = **105,283,584**.

**Prior art.** Grassl's computer tables, cited by Kantor, may already contain this minimum. Here it is verified exhaustively. Not claimed as new.

## 2. Two types: lifted and genuine (`w33_four_qubit_size5_census.py`, `w33_four_qubit_type_lift.py`)

| type | through pair | Lagrangians inside C | partitions of C | ϑ | numerical min F | lift points |
|---|---|---|---|---|---|---|
| **A (genuine)** | 840 | 6 | 1 | 14.785 | **0.0523626 < 1/16** | **0** |
| **B (lifted)** | 56 | 10 | **2** | 14.609 | 1/16 | **120** |

- **Lift points.** For type B there are 120 uncovered points p such that, in the quotient p^⊥/⟨p⟩ ≅ W(5,2), the five Lagrangians project to a three-qubit maximal five-set. Type B is the lift of the three-qubit sets, which explains:
  - the count 56, equal to the three-qubit count through a pair;
  - its mirror partners, inherited from the three-qubit mirror pairs;
  - its stabiliser-optimal minimum.
- **Type A has no lift point.** It is genuinely four-qubit, and it carries the non-stabiliser optimum.
- **Exact bound for type A:** ϑ ≤ 74/5, hence **F ≥ |v|⁴/80** (Pass 12647).

## 3. The type-A optimum (`w33_four_qubit_size5_optimum.py`)

- min F = 0.0523625607566847 (200 starts, 198 reach it).
- The optima show **15 distinct |⟨P⟩| profiles**, so the minimum is possibly attained on a family, unlike the pentad's single orbit.
- A cubic identification (coefficients up to 9,216, residual 2.5×10⁻¹³) was **rejected**: with about 10¹⁷ candidate cubics, a match at that level is expected by chance. **The value is unidentified.** The acceptance rule in the script was too loose, and this is noted in the script and the JSON.

## 4. Pentad degree-6 SOS (`w33_pentad_degree6_sos.py`)

The unreduced degree-6 real SOS for a two-qutrit pentad (blocks of size 165 and 405; 913 s; identity residual 2×10⁻¹⁰) gives **δ* = 0.13654**:
- above the exact degree-4 value 1/9 = 0.1111 (Pass 12639);
- **below** the numerical minimum 0.14711.

So **degree 6 is not tight for the pentads**, and the identified value (207 − 19√57)/432 cannot come from a degree-6 certificate. This differs from three qubits, where degree 6 reaches 1/8 to within 10⁻⁶. The 0.13654 bound is numerical. Making it exact (the ε-rounding of Pass 12647, with a qutrit Weyl reduction) is straightforward but was not done.

## 5. Paper draft (`papers/strongly_unextendible_pauli_mubs.tex`, compiled to PDF)

A self-contained 3-page draft for quantum-information readers covering:
- the twirl identity and the Lovász bound;
- Theorem 1 (d = 4 exact);
- Theorem 2 (d = 8: one orbit, F ≥ (1/8 − 10⁻⁶)|v|⁴ exact, (3 − √5)/8 structural);
- Theorem 3 (d = 16: minimum size 5, 105,283,584 sets, F ≥ 1/80 for type A, exact 1/16 and 1/8 for nine-sets);
- the two-qutrit remark;
- what is not claimed, with references (Mandayam et al., Thas, Kantor, de Gois et al., Lovász).

**Not yet in the draft:** the lifted/genuine split of §2, which can go into Theorem 3(ii).

## 6. Degree 8 for the exact 1/8: not attempted

At degree 8 every monomial family has an even charge, so the Pauli centre acts trivially, and the reduction splits into 64 character blocks per family rather than one irrep. Implementing this is the next step for an exact certificate at 1/8. It was not done this round.

## Open

- An exact certificate at exactly 1/8 for three qubits.
- An exact certificate at 1/16 for type B (ϑ > α, so it needs an SOS).
- A closed form for the type-A optimum, and whether it is a family.
- Extending the exhaustive method to five qubits: the Witt reduction is the key, and the candidate counts grow quickly.
