# Pass 11643 — the Hamming null cube is the set of eight Clifford transvection ticks; its arrow is the handedness of the tick on the Hesse sphere

Producer: `analysis/w33_pass11643_hamming_cube_is_transvection_clock.py`
Certificate: `data/w33_pass11643_hamming_cube_is_transvection_clock.json`
Regression: `tests/test_w33_pass11641_11646.py`

## Objects

* **Pass 11550's null cube.** Eight oriented rank-one symmetric matrices S = c·vvᵀ over F₃. The Veronese sheet (c = 1)
  has χ = −1 and stored Weil phase −i. The negative sheet (c = −1) has χ = +1 and Weil phase +i.
* **The tick of S.** t_S = I + SΩ on qutrit phase space F₃², with coordinates (x, z), Weyl operators XˣZᶻ and
  Ω = [[0,−1],[1,0]].
  * (SΩ)² = 0, so t_S has order 3 and t_{−S} = t_S⁻¹.
  * Its Clifford gate U_S is taken in the canonical Weil representation: a conjugate of D_c = diag(ω^{2cj²}), which
    implements the shear z → z + cx.
  * A conjugate of D_c does not depend on the phase of the conjugating unitary, so U_S and tr U_S are canonical.
* **The tick on the Hesse sphere.** R(U_S) = BᵀU_S^{⊗3}B is its action on the Hesse doublet (Pass 11641), an order-3
  rotation of the Hesse Bloch sphere.

## Results (all eight, objectwise)

| check | count |
|---|---|
| tr U_S / \|tr U_S\| equals Pass 11550's stored Weil phase (= iχ) | **8/8** |
| U_{−S} = U_S⁻¹: Pass 11550's "outer temporal reversal" S → −S runs the tick backwards | **8/8** |
| R(U_S) is a 120° rotation fixing the vertex m_v of the MUB of v | **8/8** |
| Veronese sheet: right-handed axis = **+m_v**, a stabiliser vertex (xyz > 0) | **4/4** |
| negative sheet: right-handed axis = **−m_v**, the antipodal T-magic vertex (Pass 11641) | **4/4** |
| χ = −sign(xyz) of the right-handed axis | **8/8** |
| complex conjugation: conj(U_S) is the gate of J₀t_SJ₀, a negative-sheet tick | **8/8** |

## Reading

**The 8 points, 4 ways.** The eight points of Codex's Hamming null cube are the eight elementary Clifford clock ticks of
a qutrit, the order-3 transvection gates. On the Hesse sphere of Pass 11641 they are the eight oriented rotation axes
through the cube vertices:
* the 4 stabiliser vertices (singular pencil members);
* the 4 T-magic vertices (equianharmonic members, containing T|+⟩).

**Four languages for one sign.**
* Pass 11550's Weil phase: the trace phase of the tick.
* Its Hamming arrow χ: the handedness of the tick about its stabiliser vertex.
* Its square/non-square sheet: whether the tick turns right-handed about a stabiliser vertex or about a magic vertex.
* Its "outer temporal reversal": playing the tick backwards.

**Two time reversals, now told apart.**
* **Pass 11550's PSp = W(D₃)** acts on S by *congruence* and preserves χ.
* **Wigner time reversal** (complex conjugation) acts on *ticks*. A det = −1 element of GL(2,3) acts on t_S by
  congruence followed by S → −S. So the **Hamming arrow of a tick is T-odd**: conjugation takes every Veronese tick to a
  negative-sheet tick.
* The trace phase is just the trace of a gate, and antiunitary conjugation complex-conjugates traces. That explains
  "Weil phase = iχ flips under T" in one line.
* Unitary Cliffords preserve each sheet: these are the two conjugacy classes of order-3 unipotents in SL(2,3), which are
  mutually inverse.
* This is the finite form of the "one-way clock" found in the one-gate work (MEMORY: a transvection tick is reversed
  only antiunitarily).

**What a convention fixes.** The objectwise phase match uses one global orientation of the symplectic form (Ω above)
and Codex's (a, b, c) read as [[a, b], [b, c]] in (x, z) order. With the opposite orientation, every phase and every
handedness flips together. The convention-free statement is:

> **trace phase −i ⇔ right-handed about the stabiliser vertex** (8/8).

This uses the canonical Weil representation and the complex orientation of the pencil sphere.

**Prior art.**
* Classical: SL(2,3) has two classes of elements of order 3; Weil characters are Gauss sums.
* Pass 10954 already identifies the det character of GL(2,3) with the unitary/antiunitary extended-Clifford character
  and the Hesse spinor-norm character. Pass 11643 realises that character on the eight ticks: Wigner reversal flips the
  sheet. It does not claim the character itself.
* In the repo: the F₃ nilpotent-cone/Hesse dictionary (2026-09-23 adjoint intertwiner) and Pass 11550's sheets.
* New here: the identification with Clifford ticks, the trace match, the Hesse-sphere handedness, and the T-odd reading.
