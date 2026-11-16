# Pass 12679: the logical stabiliser fidelity of the F₈ minimiser is (3 + √3)·cos²(π/18)/9; 64 of 64 global minimisers sit on type-A or type-B code spaces; the regulus stabiliser codes are trivial; scoping of the exact c₈ certificate

Claude track. Follows Pass 12678. **Not a theory of everything.**

## 1. Magic of the minimiser in closed form (`w33_f8_minimiser_magic_and_codes.py`)

On the 8-dimensional code space (effective three-qubit model), all **124** distinct Newton-polished minimisers found from 500 starts have the same logical stabiliser fidelity, max over the 1,080 three-qubit stabiliser states of |⟨s|ψ⟩|². Code-space Cliffords preserve stabiliser states, so the value is basis-independent. A 40-digit mpmath Newton refinement plus the exact stabiliser projector give

  **F_stab = 0.50992911292363054618773114488762…** = **(3 + √3)(γ + γ²)/36** (difference 1.5×10⁻³²), γ = 2cos(2π/9).

Since γ + γ² = 2 + 2cos(π/9) (the roots of x³ − 3x + 1 sum to zero), this is

  **F_stab = (3 + √3)·cos²(π/18)/9.**

**Comparison with the qutrit side** (Pass 12677). The two-qutrit Clifford eigenstates of the E₆(a₁) element have F_stab = (2 + γ)/9 = 4cos²(π/9)/9. Both values lie in the real field Q(cos 2π/9, √3) and are cos² of a ninth-root angle over 9. This is a parallel of form, not an identity between the two problems.

## 2. Reduction evidence, larger census (`w33_f8_global_minimiser_stabilisers.py 600`)

- 600 random starts in C⁶⁴: **48** reach c₈.
- **All 48** have an uncovered Pauli stabiliser of order exactly 4: **24 type A and 24 type B**, with no other type.
- With Pass 12674's 16, that is **64 of 64** global minimisers on type-A or type-B 16-dimensional code spaces.

Local rigidity (Pass 12675) says the minimum families stay on these code spaces. A proof of the reduction is still open.

## 3. The regulus stabiliser codes are trivial as error-correcting codes

In the six physical qubits that define the regulus (the bits of the Pauli labels):

| code | parameters | stabiliser weights |
|---|---|---|
| T (rank 3) | [[6, 3, 1]] | 3, 4, 4, 5, 5, 5, 6 |
| A, B (order 4) | [[6, 4, 1]] | 4, 5, 5 |
| C (order 4) | [[6, 4, 1]] | 3, 4, 5 |

So the code spaces carrying the minimum have no error-correcting power in this labelling. They are not candidates for holographic stabiliser codes, which need perfect or near-perfect tensors such as [[6,0,4]] or [[5,1,3]]. This is a negative for the "certainty constants as holographic costs" idea in its simplest form.

## 4. Scoping the exact certificate at c₈ (Pass 12678 follow-up)

Pass 12678 showed the degree-8 SDP at C = c₈ is strictly feasible on the face spanned by the 128 minimisers (margin 0.649). Making it exact requires:
1. The face over the field of the minimisers. The face is Galois-stable over Q(γ, i), since automorphisms fixing c₈ permute the minimisers, so a basis over Q(γ, i) (degree 6) exists. Building it from the exact eigenstates over Q(ζ₇₂) (degree 24) is about 10¹⁰ field operations in the present pure-Python arithmetic.
2. Rounding the Gram matrices restricted to the face's complement over Q(γ, i), followed by an exact solve of the (non-diagonal) coefficient system and an exact PSD check.

This is a well-defined engineering task, best done with a compiled number-field library (PARI/GP is available at C:/tools/pari per the project notes). It was not attempted here.

## 5. Not done

- The exact Galois test at q = 16 needs an exact torus minimiser over Q(cos 2π/17), and was not attempted.
- The mapping of the F₈ minimiser through PSU(4,2) ≅ PSp(4,3) has no canonical state map: the effective three-qubit space is 8-dimensional, while the two-qutrit Weil representation is 9-dimensional (4 + 5 under PSp(4,3)). Only the class-and-field comparison of §1 is meaningful.
