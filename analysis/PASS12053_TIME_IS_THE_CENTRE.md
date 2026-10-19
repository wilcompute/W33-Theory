# Pass 12053: time is the centre of the clock's symmetry group

* **Producer:** `analysis/w33_pass12053_gate_sets_and_real_forms.py` (8/8 checks)
* **Certificate:** `data/w33_pass12053_gate_sets_and_real_forms.json`
* **Regression:** `tests/test_w33_pass12053.py`
* **Track:** Claude. Reservation `e7a248afa`.
* **Continues:** Pass 12052 (Theorem 7.3).

## Setting

**Ticks.** These are the determinant-one transvections t_p, centred at points of W(3,3). The 40 ticks generate Sp(4,3):
the closure gives 51,840 elements.

**Compatibility.** A dynamics is compatible with a real form iff it fixes the form's involution.

## 1. Gate sets (exact)

| gate set | clock involutions fixed | split involutions fixed |
|---|---|---|
| one tick | 3 | 0 |
| two ticks, collinear centres (commuting) | 0 | 0 |
| two ticks, non-collinear centres | 0 | 0 |
| ticks on an isotropic line / on p^⊥ | 0 | 0 |
| ticks on one hyperbolic line (SL₂(3) on one qutrit) | 0 | 0 |
| ticks on a factorisation (local Clifford SL₂(3) × SL₂(3)) | 0 | 0 |
| all ticks (Sp(4,3)) | 0 | 0 |

**The tested hypothesis is false.** "Local dynamics selects the split form" fails, and it is recorded as such. A
non-compact real form tolerates ticks at **one centre only**.

## 2. The full compatible groups (exact)

| real form | stabiliser order | centre | derived subgroup | abelianisation | ticks contained |
|---|---|---|---|---|---|
| clock E₈₍₋₂₄₎ at p | 432 | **exactly ⟨−1⟩ × ⟨t_p⟩ ≅ ℤ₆** | 54 | 8 | t_p^±1 only |
| split E₈₍₈₎ | 384 | {±1} | 192 | 2 | none |

## Reading

**The time generator is central.** In the clock real form, the tick is central in the form's entire symmetry group.
Every dynamics compatible with the one-time real form commutes with the tick. That is the finite analogue of a
Hamiltonian commuting with every conserved symmetry, i.e. time translation is central.

**The split form has no tick.** The split real form admits no tick at all.

**Beyond 12052.** So "one time" is not only *selected* by a tick (12052): the tick is the **centre** of everything
compatible with it.

## Scope

* **Compatibility:** a fixed involution. Since Sp(4,3) sits in the compact form, this is equivalent to commuting with the
  real structure.
* **Involutions:** inner ones only.
* **Nature of the statements:** finite group statements.

## What is not new

* Transvection groups and parabolics of Sp(4,3).
* The classification (12052).
