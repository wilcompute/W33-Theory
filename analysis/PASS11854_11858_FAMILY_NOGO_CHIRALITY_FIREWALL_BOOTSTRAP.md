# Passes 11854–11858 — no exact family SU(3) can commute with GUT and finite Lorentz in E₈; Lorentz-commuting projections cannot make chirality; the boundary bootstrap reads off every bulk coupling; spinorial Lorentz × central ℤ₃ commutes with su(3) ⊕ so(5) ⊕ u(1)

**Files.**
* Producers:
  * `analysis/w33_pass11854_11857_family_nogo_chirality_firewall_combined.py`
  * `analysis/w33_pass11856_boundary_bootstrap_channels.py`
* Frozen:
  * `data/w33_pass11854_11857_family_nogo_chirality_firewall_combined.json`
  * `data/w33_pass11856_boundary_bootstrap_channels.json`
* Lean: `formal/W33/Pass11858A5LatticeMod3.lean`
* Regression: `tests/test_w33_pass11854_11858.py`

**Context.**
* Passes 11843–11853: the faithful finite Lorentz group A₆ commutes with su(5)_GUT in E₈.
* A₆ × central ℤ₃ commutes with su(3) ⊕ su(2) ⊕ u(1)_Y.
* The spinorial SL(2,9) commutes with so(11), a result owned by the parallel Rounds 34/35.
* The bulk four-point space is 3-dimensional.
* Parallel Round 35 §2 showed that the unprojected spinorial spectrum is vector-like and said a chiral model needs an
  extra projection. 11855 below shows what kind of projection cannot supply it.

## 11854 — three generations as an exact family SU(3): a centraliser no-go

* **The two centralisers.** Inside E₈ ⊃ SU(5)_L × SU(5)_GUT, take the family su(3) to be the upper-left sl₃ of su(5)_L,
  through the explicit homomorphism of 11849. Then:
  * **c(su(5)_GUT ⊕ su(3)_fam) = su(2) ⊕ u(1)** (dim 4, rank 2);
  * **c(SM ⊕ su(3)_fam) = su(2) ⊕ u(1)²** (dim 5, rank 3).
* **Theorem (conditional on the classical fact that C_E₈(SU(5)_GUT) = SU(5)_L is connected).** A finite Lorentz group
  commuting with SU(5)_GUT and SU(3)_fam lies in C_{SU(5)_L}(SU(3)) ≅ U(2). Finite subgroups of U(2) project in
  SO(3) to cyclic, dihedral, A₄, S₄ or A₅ groups. A₆ is simple of order 360, so **neither A₆ nor SL(2,9) has a
  nontrivial homomorphism to U(2)**.
* **Conclusion.** In E₈ three generations cannot arise as an exact family SU(3) that commutes with both the GUT and the
  finite Lorentz group.
* **Scope.** For the SM version (su(2) ⊕ u(1)²) the same finite-subgroup argument applies to the identity component.
  The component group of that centraliser is not computed here.

## 11855 — chirality firewall

**Theorem.** Let g be any automorphism of E₈ commuting with the spinorial finite Lorentz group SL(2,9) (embedded as in
Rounds 34/35 or 11849, with E₈ = (55,1) + (11,5) + (32,Di) + (1,10)). Then:
1. g acts on Di by a scalar (Schur), and inside Sp(4) ≅ Spin(5) that scalar is ±1.
2. So the g-invariant part of (32, Di) is V_{±1}(32) ⊗ Di, where V_{±1} is the ±1 eigenspace of g's Spin(11) part on
   the 32.
3. The so(11) spinor 32 is **quaternionic**: an antilinear J with J² = −1 commutes with Spin(11). J maps the real
   eigenspace V_{±1} to itself, so the kept spectrum is self-conjugate under every subgroup of the unbroken group.
4. **Every orbifold-type projection by a Lorentz-commuting automorphism leaves the spinorial matter vector-like.**

**Verification (explicit Spin(11) Clifford model).**
* The 32-dimensional spinor is built from Jordan–Wigner γ-matrices. The commutant of Spin(11) among antilinear maps is
  one-dimensional (Schur), J² = −1, and J commutes with all 55 generators.
* Over **200 random finite-order elements** of Spin(11), in random tori and of orders 2–8, the ±1 eigenspaces were
  non-empty in 186 cases. **All of them are J-invariant** (worst error 10⁻¹³).
* **Contrast.** The Spin(10) volume element ω = γ₁⋯γ₁₀ lies in Spin(11) and acts by ±i on 16 / 1̄6̄. Combined with a
  Lorentz-commuting sign on Di it keeps nothing. Combined with a **Lorentz-breaking phase i on Di** it keeps exactly
  **16 ⊗ Di (net chirality 16)**.
* **So chirality requires a projection that does not commute with the finite Lorentz group**: a parity / time-reversal-
  type orbifold, a boundary condition, or an index. Projections normalising but not centralising Lorentz (e.g. by the
  Frobenius/parity element of 11832) are not covered by the theorem and remain open.

## 11856 — the boundary bootstrap: s-channel decomposition of the four-point function

* **The four structures.** On the boundary 15 these are contact C, 15-exchange E₁₅, hidden-20 exchange E₂₀ and the
  disconnected (generalised free) part D. Read as s-channel operators on 15 ⊗ 15, all four are **scalar on each
  channel**.
* **The channels.** Sym²15 (120) splits into channels of dimension **1, 15, 20, 24 and 60**:
  * the characters identify 1, 15_S, 20_b and 24;
  * the 60 has norm 2, so it is two irreducibles.
  * Λ²15 (105) is annihilated by every symmetric structure.

| channel | contact C | 15-exchange | hidden-20 exchange | disconnected D |
|---|---:|---:|---:|---:|
| 60 | 0 | −0.713 | 0 | 0.667 |
| 24 | 0 | 0.713 | −0.977 | 0.667 |
| 20 | 1.818 | 2.138 | 2.443 | 0.667 |
| 15 | 1.818 | 2.850 | 1.955 | 0.667 |
| 1 | 4.546 | 4.276 | 3.909 | 5.667 |

  Each structure is normalised to maximum entry 1.
* **Bootstrap reading.**
  * No channel is fed by the hidden 20 alone. But **the 60-channel is fed only by 15-exchange** and **the 24-channel by
    15- and 20-exchange but not by contact**.
  * So boundary OPE data fix every bulk coupling in sequence: the cubic φ³ coupling from the 60-channel, then the hidden
    φ²χ coupling from the 24-channel, then the quartic from the remaining channels.
  * Five channels against three couplings leaves **two linear crossing relations** that any boundary theory with this
    bulk dual satisfies.
* **Reflection positivity.** It requires D + connected ≥ 0 channel by channel. At small couplings it holds, since D is
  positive on all of Sym². The 60 and 24 channels give upper bounds on the exchange couplings in these normalisations.

## 11857 — one finite group: spinorial Lorentz × central translation

* **It is a direct product.** The central ℤ₃ translation t_c of 11850 commutes with the spinorial SL(2,9) lift (error
  2·10⁻¹³), so the group is **SL(2,9) × ℤ₃**.
* **Its commutant in E₈** has dimension 19, rank 5, centre 1, and contains su(3)_A₂ and su(2)_α.
  * The centraliser of su(3) inside it is so(5) ⊕ u(1) (derived dimension 10, rank 2, containing su(2)_α).
  * The centraliser of su(2)_α inside it is su(3) ⊕ su(2)′ ⊕ u(1).
* **So the commutant is su(3) ⊕ so(5) ⊕ u(1)**, i.e. so(11) ⊃ so(6) ⊕ so(5) with the central translation breaking
  so(6) = su(4) to su(3) ⊕ u(1).
* It contains the **left–right-symmetric algebra** su(3) ⊕ su(2)_L ⊕ su(2)_R ⊕ u(1) as a subalgebra, via so(5) ⊃ so(4).
  It is **not** the Standard-Model algebra: the bosonic A₆ × ℤ₃ gives the SM (11850), while the spinorial lift keeps an
  extra su(2)′ and an so(5).

## 11858 — Lean: the A₅ lattice mod 3

`W33.Pass11858A5LatticeMod3` works in S = {x ∈ (ZMod 3)⁶ | Σx = 0}, with A₆ generated by the 3-cycles (0 1 k). It proves
by `decide`:
* the all-ones vector lies in S and is fixed;
* it is the radical of Q = 2Σx², i.e. Q(x + c·1) = Q(x) on S;
* the nonzero vectors split **62 + 90 + 90** by Q (the radical plus 20·3 + 30·3 + 30·3);
* **no nonzero A₆-invariant linear functional on S** (only constant coefficient vectors are invariant).

Since A₆ is perfect, the last statement excludes any invariant 4-dimensional subspace: the Minkowski module occurs only
as the non-split ℤ₃ · M of 11844, which parallel Round 33 also found.

## Prior art and scope

* **Classical.**
  * E₈ ⊃ SU(5) × SU(5) and ⊃ Spin(11) × Spin(5).
  * The finite subgroups of SU(2)/U(2).
  * The quaternionic so(8k+3) spinor.
  * Schur's lemma.
* **Corpus.**
  * Passes 11834, 11843–11853.
  * Parallel Rounds 33 (§3, §3b), 34 and 35 (§1, §2), cited.
* **New here.**
  * The centraliser no-go for an exact family SU(3).
  * The chirality firewall theorem with its Clifford-model verification and Lorentz-breaking contrast.
  * The s-channel bootstrap table and the sequential determination of the bulk couplings.
  * The SL(2,9) × ℤ₃ commutant su(3) ⊕ so(5) ⊕ u(1).
  * The Lean module facts.
* **Scope.** These are kinematic and representation-theoretic statements. No vacuum, symmetry-breaking dynamics or
  chirality mechanism is derived. The firewall says where chirality cannot come from, not where it does.

## Correction (Pass 11859)

The "contrast" in 11855, where a Lorentz-breaking phase i on Di keeps exactly one 16, holds in the abstract product
32 ⊗ Di but is **not an automorphism of E₈**. Inside E₈ the 1̄6̄ pairs with Di*, on which that phase acts as −i. In fact
no single automorphism of E₈ yields a chiral fixed spectrum (the adjoint is a real representation). 11855's theorem for
Lorentz-commuting projections stands as a special case. Chirality requires pairing complex E₈ eigenspaces with complex
geometric sectors. See `analysis/PASS11859_11863_PARITY_ORBIFOLD_TRIALITY_POSITIVITY.md`.
