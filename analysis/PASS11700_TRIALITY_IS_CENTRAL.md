# Pass 11700 — no two-qutrit gate realises an odd triality; the only triality on a D₄ × D₄ dual pair is the central Z₃

Producer: `analysis/w33_pass11700_triality_is_central.py`
Certificate: `data/w33_pass11700_triality_is_central.json`
Regression: `tests/test_w33_pass11697_11703.py`

**Question (Pass 11693, "spacetime" item).** Pass 11687 found that the Z₃ grading of the two-qutrit E₈ cycles the three cosets (8_v,8_v) + (8_s,8_s) + (8_c,8_c) of a D₄ × D₄ dual pair. In ten-dimensional light-cone language, so(8) is the transverse algebra and 8_s/8_c are the two chiralities. Do qutrit gates realise the *odd* part of triality, the exchange 8_s ↔ 8_c?

**Method.**
* A gate U acts on e₈ only through a determinant-one lift U·det(U)^{−1/9}·ζ₉ᵏ.
* The three lifts differ by the central scalar ζ₉, whose E₈ image is the grading element g.
* So each of the three lifts of each generator was tested against the 64-root coset labels.

**Found.**

| gate | lift 0 | lift 1 | lift 2 |
|---|---|---|---|
| F⊗I, S⊗I, Z⊗I, X⊗I (qutrit-1 Cliffords) | one lift identity, two cyclic | | |
| I⊗F, I⊗S (qutrit-2 Cliffords) | one lift identity, two cyclic | | |
| SWAP | one lift identity, two cyclic | | |
| complex conjugation K | one lift identity, two cyclic | | |

**No lift of any of these is a transposition.** Each gate's coset action is exactly its central-lift ambiguity. Modulo the centre, the stabiliser of the tensor factorisation acts trivially on the three cosets. This includes the antiunitary elements and the qutrit exchange.

## Reading

* **Inside E₈ itself.** Odd trialities of D₄ × D₄ do exist inside E₈: the normaliser in W(E₈) maps onto S₃. None is a two-qutrit gate.
* **The realised triality.** The only realised triality is cyclic and central. It is the centre of SU(9)/Z₃ ⊂ E₈, i.e. the operator / three-fermion / three-hole grading of Pass 11687.
* **Light-cone dictionary.** Gates never exchange the two ten-dimensional spinor chiralities.
* **Contrast with Pass 11689.** The 27/27̄ chirality *is* flipped by Pauli inversion and by antiunitarity separately. The two "chiralities" behave oppositely under the same gates.

**Scope.** This is a statement about gate actions on root cosets. **No spacetime is derived.** The light-cone reading is a dictionary, not a result.
