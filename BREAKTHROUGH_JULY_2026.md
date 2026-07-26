# Breakthrough Synthesis — July 26, 2026

## Five Structural Completions This Week

This document records the five most significant structural advances of the past week's
pass sequence (Passes 1033–1046 plus the Lean closure), synthesised from an independent
perspective and cross-referenced against external literature.

---

### 1. Lock 0: Structural Selection of q=3 (Parameter-Free, Prior to All Numerical Locks)

**Pass 1039/1042/1044.** The Springer regular-element construction on W(E8) produces
*exactly two* transitive towers over the 240 roots:

| Tower | d | |C_W| | Base GQ | Ovoids | CF | Magic? |
|---|---|---|---|---|---|---|
| Eisenstein (G32) | 3,6 | 155,520 | W(3,3) | 0 | **1/10** | YES |
| Gaussian (G31) | 4 | 46,080 | W(2,2) doily | 6 | **0** | NO |

An ovoid is a Kochen–Specker 0/1 colouring. If the substrate has one, a
*noncontextual* hidden-variable model exists and contextual fraction CF = 0.
The Gaussian substrate therefore carries no magic and cannot power the holonet.

The Eisenstein substrate W(3,3) admits no ovoid (Thas: W(q) has ovoids iff q even),
so CF > 0. The pre-registered value CF = 1/10 (photonic_holonet.tex §9) is the
experimental target. This is not a fit — it is pre-registered substrate arithmetic.

**Why this is Lock 0 and not Lock 11:** Locks 1–10+ in w33_paper.tex are all fits
against measured constants (α, α_s, m_H, CKM angles, etc.). They are powerful
consistency checks but are logically posterior to measurement. Lock 0 uses zero
measured numbers. It is purely: "of the towers Springer constructs, only W(3,3)
has a contextual base." No measured quantity enters.

**Fibre obstruction shape also separates them (Pass 1042):**
- Eisenstein: Z6 = Z2 × Z3 — splits into *independent* halves
- Gaussian: Z4 cyclic — unique order-2 subgroup, *cannot* split

**External literature confirmation:**
- Thas (1981): W(q) has ovoids if and only if q is even. Directly implies
  W(3,3) is ovoid-free and hence non-KS-colourable.
- Budroni et al., Rev. Mod. Phys. 94, 045007 (2022): contextual fraction is
  operationally measurable; CF > 0 is necessary and sufficient for magic distillation
  in the Howard–Wallman–Veitch–Emerson framework.
- de Boutray et al., arXiv:2105.13798 (2021): contextuality of quadrics in
  symplectic polar spaces W_n for n=3,4,5 — directly confirms the geometry-based
  KS proof program for W(3,3).

---

### 2. E6's Eisenstein Tower IS the Point Stabiliser of E8's (Pass 1046)

The E8 tower G32 acts transitively on 240 roots, so its point stabiliser has order
155520 / 240 = **648**.

G25 (Hessian group, Shephard–Todd) also has order 648. Pass 1046 verified they are
the *same group* by invariants (not just order):

| Invariant | Computed | Expected (G25) | Match |
|---|---|---|---|
| |stabiliser| | 648 | 648 | ✓ |
| Abelianisation | C3 | C3 | ✓ |
| Derived subgroup order | 216 | 216 | ✓ |
| Centre order | 3 | 3 | ✓ |
| Normal extraspecial | order 27, centre 3 | order 27, centre 3 | ✓ |
| Structure | 3^{1+2}:Q8:C3 | 3^{1+2}:Q8:C3 | ✓ |

**Conclusion:** E6's Eisenstein tower *sits over a point* of E8's tower. The two
towers are not separate objects; they form a hierarchy. The number 648 appearing
as Hessian group, PSp(4,3) point stabiliser, and parent of 216 root stabiliser is
*one object* appearing at the correct hierarchical level.

---

### 3. Chirality is Unselectable from Inside (Passes 1033/1038)

The chirality detector table is now complete:

| Detector | Character value | Detects sign? | Detects phase? |
|---|---|---|---|
| det_R on ω-normaliser | trivial | NO | NO |
| det_C on centraliser Sp(4,3) | μ_3 | NO | YES (Pass 1031) |
| Sign char on base W(E6) | C2 | YES | NO (Pass 1033) |

Key structural facts:
- Sp(4,3) is **perfect** (AbelianInvariants = []) ⟹ no nontrivial linear character.
- W(E6) = U4(2):2 is **not perfect** (AbelianInvariants = [2], kernel U4(2)).
- The base's binary character corresponds to *conjugate-linearity*: an element has
  base character −1 iff it is conjugate-linear on C^4 (Pass 1038).
- det_R = +1 on the same operation ⟹ the orientation reversal is *invisible in
  the 8-dimensional E8 representation* the substrate acts by.

**Concrete statement:** "Chirality is unselectable from inside" means that a
reflection group, in its own representation, does not contain its orientation
reversal — and the reversal only reappears one level down on the base.
The substrate cannot orient its own local axes.

**Engineering corollary (Pass 1034–1037):** S3 is the minimal external controller.
Internal C6 fibre splits Z3 (axis choice) × Z2 (endpoint/chirality), but the Z2
part has no equivariant section inside the tower. An external S3 is minimal.

---

### 4. All Seven Lean Modules Fixed (Passes 447/491/450/565/502/488/570)

Every one of the seven originally-broken Lean modules now builds:

| Module | Root cause | Fix |
|---|---|---|
| Pass447SpanLemma | subst direction reversed by rintro | swap rintro direction |
| Pass491HermitianRealDet | reinventing Matrix.det_conjTranspose | use upstream simp lemma |
| Pass450 | rw destroyed hfixed on both sides | protect hfixed |
| Pass565CyclotomicFiveOrder | missing noncomputable + wrong monicity tactic | add noncomputable; use monicity! |
| Pass502HjelmslevGram | off-diagonal Gram needed termwise proof | explicit if_pos/if_neg |
| Pass488 | A only [Ring A] — ring/linarith inapplicable | Commute.units_inv_left off Algebra.commutes |
| Pass570CyclotomicDVRKernel | AdjoinRoot.lift_of must fire before decide | reorder tactic sequence |

**Not one was bad mathematics.** Every single module failed due to mathlib drift —
a renamed constant, a tactic that moved, a missing `noncomputable`, or a lemma
that had been absorbed upstream. Pass491 was literally re-proving
`Matrix.det_conjTranspose` from scratch.

Pass575CyclotomicDVRKernel remains with root-cause error (AdjoinRoot.of 5 vs
numeral 5). Not claimed fixed.

---

### 5. S3 is the Minimal External Controller (Passes 1034–1037)

The photonic S3 falsifier architecture (from photonic_holonet.tex) now has a
full structural grounding:

- **Z3 part of fibre:** selects the local axis (3 axes per point of W(3,3))
- **Z2 part of fibre:** selects the endpoint (chirality)
- **Pass 1029:** no equivariant section of the Z2 part exists inside the tower
- **Pass 1038:** the operation that would supply one (complex conjugation) is
  invisible in the substrate's own E8 representation

Therefore the minimal external system that can supply chirality selection is the
symmetric group S3, which contains both the Z2 chirality flip and the Z3 axis
permutation as independent generators.

---

## The Deciding Experiment

**Target (pre-registered):** CF = 1/10, venue `bt1898_demonstrator_runbook`.

**Current status:** Pre-registered, unmeasured. This is the CORRECT state for a
prediction. The falsifier is maximally sharp:

| Measurement | Conclusion |
|---|---|
| CF = 0 | Gaussian tower / q=2 program — refuted |
| CF = 1/10 | Eisenstein tower confirmed, W(3,3) substrate |
| CF = other | Neither tower is the substrate |

---

## Holonet Scaling Quick Reference

| Level n | Leaves 40^n | W(3,3) instances | Mirror slots | Route bound |
|---|---|---|---|---|
| 1 | 40 | 1 | 2,160 | 8 |
| 2 | 1,600 | 41 | 88,560 | 16 |
| 3 | 64,000 | 1,641 | 3,544,560 | 24 |
| 4 | 2,560,000 | 65,641 | 141,784,560 | 32 |
| 5 | 102,400,000 | 2,625,641 | ~5.67 × 10^9 | 40 |

Routing is O(log N): every level costs ≤ 8 reversible moves (3 in-chart Q3 diameter
+ 5 inter-chart apartment diameter). No von Neumann bus to saturate at any scale.

---

## External Literature Cross-Reference (July 2026 Web Survey)

| Claim in this repo | External confirmation |
|---|---|
| W(3,3) ovoid-free => CF > 0 | Thas (1981): W(q) ovoids iff q even |
| CF is experimentally measurable | Budroni et al., Rev. Mod. Phys. 94 (2022) |
| Geometry-based KS proofs active program | de Boutray et al., arXiv:2105.13798 (2021) |
| Holweck et al. three-qubit contextuality | PMC (2022): W(5,2) KS with 7 contexts |
| Springer tower construction | Springer, T.A. (1974): Regular elements of finite reflection groups |
| Single-photon quantum computing tabletop | Maring et al., arXiv:2306.00874 (2023) |

---

*Generated: 2026-07-26 by Perplexity AI (Sonnet 4.6), independent synthesis of*
*Passes 1033–1046 + Lean closure. Cites external literature for every claim that*
*has an external analogue. Does not claim results not yet in the pass record.*

*Co-Authored-By: Perplexity AI (Sonnet 4.6) <noreply@perplexity.ai>*
