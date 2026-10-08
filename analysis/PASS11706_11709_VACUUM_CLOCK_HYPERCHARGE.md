# Passes 11706–11709 — which vacuum can coexist with the Standard-Model clocks: the grade obstruction, the operator-type Standard Model (9 = 5 + 4), the unique hypercharge, and how the handedness is chosen

Producer: `analysis/w33_pass11706_11709_vacuum_clock_hypercharge.py`
Certificate: `data/w33_pass11706_11709_vacuum_clock_hypercharge.json`
Regression: `tests/test_w33_pass11706_11712.py`

**Question (Pass 11703 open items 1–3).**
* Is there a principle making the chirality vacuum (Pass 11698) and the SM-shaped clocks (Passes 11701–11703) select consistently?
* Which of the five u(1)s is hypercharge?
* Does anything lift the degeneracy between a vacuum and its C-partner?

**Criterion.** A vacuum ψ enters e₈ through ρ = |ψ⟩⟨ψ| − I/9, which lies in the operator grade sl(9). The vacuum leaves a generator unbroken when the generator commutes with ρ. For the vector criterion in 11708, the generator must annihilate ψ itself.

## 11706 — two candidate principles, both negative, one with an exact reason

**The clock Hamiltonian does not align.** Take the shortest E₈ Cartan element h with exp(2πi·h) = clock, i.e. Kac's alcove representative. Over the 1,944 line-trinification patterns:
* its ground state is an aligned vacuum in 736 patterns and a misaligned one in 525, against a random baseline of 50%;
* 553 patterns have the trivial state |00⟩ as ground state, and 130 are degenerate;
* reversing time rarely gives the conjugate partner.

**Line-trinification SM excludes every pure-state vacuum.** For all 1,944 patterns from Z⊗I, **0 of the 320 vacua** commute with the su(3) ⊕ su(2) root vectors. Over all 320 vacua × 240 roots, each vacuum commutes with 0, 30 or 56 roots. The reason is exact:
* The colour SU(3)_q of a line point q is spanned by the three-fermion states that **fill the three eigenspaces of D_q**, plus their duals: 6/6 roots are trivectors, and the triples are the eigenspaces, for all four q. It lies in the **three-fermion grade**.
* The E₈ centraliser of a pure-state vacuum is su(8) ⊕ u(1) (dimension 64, zero Λ³ component, three random checks), entirely in the **operator grade**.

## 11707 — the operator-type Standard Model: 9 = 5 + 4

**Census.** **83,592** pairs of commuting third-level clock patterns leave an SM-shaped centraliser built entirely from *operator* roots:
* colour SU(3) rotates three of the nine two-qutrit levels;
* weak SU(2) rotates two more.

**Worked example.** The clocks are ζ₉^{3xy²} [lift 1] and ζ₉^{x³+3xy+3x²y} [lift 1].
* Colour acts on |0,0⟩, |0,1⟩, |0,2⟩; weak acts on |2,1⟩, |2,2⟩.
* The vacua on |1,0⟩, |1,1⟩, |1,2⟩, |2,0⟩ commute with all 8 SM root vectors (full E₈ bracket); the others do not.
* These are stabiliser states of ⟨Z₁, Z₂⟩ with a nontrivial character, i.e. genuine chirality vacua.

**Universality (600/600 sampled patterns).**
* exactly six SU(5) completions, all with the standard spectrum;
* **exactly one** completion is all-operator, a **Georgi–Glashow SU(5) acting on five of the nine levels**;
* those five levels are always disjoint from the vacuum levels.

> **The two-qutrit Hilbert space splits 9 = 5 + 4: Georgi–Glashow SU(5) acts on five levels, and the chirality vacuum sits among the other four.**

This is a split of computational levels. It is *not* the Weil split 9 = 5 + 4 (even/odd sectors) of `analysis/THE_SELECTION_LAYER.md` and Pass 2448; whether an operator-type SM can act on the Weil sectors is open.

## 11708 — hypercharge

**Six candidates, one spectrum.** Every SM-shaped pattern has exactly six SU(5) completions with six distinct hypercharge axes. All give the standard E₈ ⊃ SU(5) × SU(5)′ spectrum:
* 5 × 10 and 10 × 5̄, plus conjugates;
* X/Y bosons at ±5/6;
* 20 neutral singlets;
* no exotic charges.

This holds for 1,944/1,944 line-trinification patterns and 600/600 operator-type patterns.

**What selects one.**
* **Along a clock chain** E₆×SU(3) → SU(5)×SU(2) → SM, the intermediate SU(5) is one of the six, so the chain fixes Y.
* **For operator-type patterns**, require the vacuum *vector* to be annihilated by Y, i.e. Y = 0 on every vacuum level. **Exactly one** hypercharge survives (600/600), always the Georgi–Glashow one.
* Its values on the five SU(5) levels are 6Y = (−2,−2,−2,3,3) or (2,2,2,−3,−3), i.e. the **hypercharges of a 5 or a 5̄**: (d, L̄) or (d^c, L). The overall sign is the convention Y → −Y.

## 11709 — handedness

Pauli inversion Π|x,y⟩ = |−x,−y⟩ is Pass 11689's C-type operation. Over 600 operator-type patterns:
* **In 189**, no SM-preserving vacuum has an SM-preserving C-partner. In these, **preserving the SM by itself fixes the handedness** once the clocks are chosen.
* **In 411**, two of the free levels form a C-partner pair. The clock Hamiltonian splits 386 of these pairs (94%), and reversing the clocks (h → −h) exchanges which partner is lower. The handedness is then set by the clocks' direction of time.

## Scope

* **Claimed:**
  * explicit configurations, certified with the full E₈ bracket;
  * an exact grade obstruction;
  * samples of 600 out of 83,592 patterns.
* **Not derived:**
  * why these clocks;
  * the sign of Y;
  * which of the two handedness outcomes nature has;
  * family structure and masses.
* The "5 or 5̄ on the levels" reading is a hypercharge assignment, not a derivation of fermion fields.

## Prior art

* E₈ ⊃ SU(9) ⊃ SU(5) × SU(4) × U(1), and E₈ ⊃ SU(5) × SU(5), are classical.
* Georgi–Glashow SU(5) is classical.
* New here: these structures realised by commuting two-qutrit clocks with a stabiliser chirality vacuum, the grade obstruction, and the hypercharge selection by the vacuum.
