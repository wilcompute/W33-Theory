# Pass 12059: observers see the clock's space but not its time

Claude track. This pass joins the event-clock chain (12052–12058) to the corpus's finite Lorentz geometry
(11831–11836).

## Setting

- **Model.** V = F₃⁴ with its symplectic form, and G = Sp(4,3).
- **Event and clock group.** An *event* is a point p of W(3,3). Its *clock group* is H_p, the stabiliser of a clock
  real form E8(−24) at p (12052–12058).
  - GAP shows the point stabiliser (order 1296) has a **unique** subgroup of index 3, with structure 2 × Q₈ over its
    3-core. So H_p is canonical: H_p = U_p : (2 × Q₈), where U_p = 3^{1+2} and the centre of U_p is the tick ⟨t_p⟩.
  - The quotient Stab(p)/H_p ≅ ℤ₃ permutes the three clock real forms at p. We call it the clock-choice group.
- **Observer and Lorentz group.** An *observer* is a Kramers time reversal J: J is anti-symplectic with J² = −1. Up to
  sign there are 36. Its Lorentz group is the centraliser C_J ≅ SL(2,9), and its sky is the 10 J-invariant contexts,
  i.e. P¹(F₉) (11831).

## Theorem (exact, for all 40 × 36 event–observer pairs)

1. **Every observer sees every event at exactly one point of its sky:** the context ⟨p, Jp⟩, which is an F₉-line.
2. **The event's little group in the observer's Lorentz group** is C_J ∩ Stab(p) = ±1 × 3². It has order 18 and
   element orders 1:1, 2:1, 3:8, 6:8. Its 3² part is the nine null rotations about that sky point.
3. **Space translations are null rotations; time is not.**
   - C_J ∩ U_p is a single ℤ₃, and it is never the tick.
   - Each of the 12 non-central ℤ₃ subgroups of U_p (the space translations of 12058) is a null rotation for exactly
     3 observers. The central ℤ₃ (time) is a null rotation for none: 12 × 3 = 36.
   - Proof of the tick statement: J t_p J⁻¹ = t_{Jp}⁻¹ with Jp ≠ p. So no observer's stabiliser, in either coset
     (Lorentz or parity), contains a tick.
4. **No observer can choose the clock.** C_J ∩ Stab(p) ∩ H_p = ±1 × ℤ₃ has order 6. The other six null rotations fix
   the event but permute its three clock real forms. Every observer's little group therefore maps **onto** the
   clock-choice group ℤ₃, so the clock real form at an event is Lorentz-invariant for no observer.

## Reading

12058 found that time is the central charge of the clock's space translations. Here that central charge turns out
to be the one translation that **no Lorentz group contains**, while every space translation is a null rotation for
some observer. This is the finite counterpart of the Bargmann picture, in which the Galilean central charge is not
an element of the Lorentz group.

The clock is also not a choice any observer's symmetry can make, since each observer's event little group moves the
clock. Something non-kinematic must choose it. In the corpus that is the one-loop vacuum and the matter content
(12056–12057: b ≤ 0 gives one time).

## Prior art

- **Classical, cited:**
  - Hermitian (regular) spreads of W(3): an F₉-structure gives SL(2,9), and 36 of them meet every point.
  - The elation group of W(q) (Payne–Thas ch. 8).
  - Wigner's little groups.
- **Corpus:**
  - 11831: Lorentz SL(2,9), with the sky as 10 contexts.
  - 11833: the 270 + 360 split of reversal products, reproduced here and **not** claimed.
  - 11836: the massless little group 3² ⋊ ℤ₄ of a null *vector*. Ours is the stabiliser of an *event*, of order 18.
  - 12058: the Heisenberg clock.
- **New:** how the clock group meets the observers' Lorentz groups (statements 3–4), and the uniqueness of H_p as the
  index-3 subgroup.

## Scope

These are finite-group statements. "Event", "observer", "space", "time" and "null rotation" are the corpus's
stabiliser-defined names, not a derivation of continuum kinematics.

## Certificates

- Producer: `analysis/w33_pass12059_observers_see_space_not_time.py`, which writes
  `data/w33_pass12059_observers_see_space_not_time.json`.
- Independent cross-check: GAP, with Sp(4,3), ConformalSymplecticGroup(4,3), LowIndexSubgroups and PCore.
