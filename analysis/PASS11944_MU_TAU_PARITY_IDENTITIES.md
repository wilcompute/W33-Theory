# Pass 11944: the theta central inversion is μ–τ reflection — and the mixing matrices measure its breaking

> **Prior ownership (added after the intake).** The parity basis e₀, (e₁ ± e₂)/√2 and the block structure are owned by
> TOE39 (Codex, 2026-10-10). This pass owns:
> * the μ–τ identification;
> * the exact identities (CKM charm row = odd content of the down states; PMNS ν₂ column = odd content of the charged
>   leptons);
> * the fork they imply.

Producer: `analysis/w33_pass11944_mu_tau_parity_identities.py`
Certificate: `data/w33_pass11944_mu_tau_parity_identities.json`
Regression: `tests/test_w33_pass11944.py`
Track: Claude. Explains Pass 11941 (CKM) and Pass 11943 (PMNS failure) by one identity, and states the fork the data impose.

## 1. Identification

**What the inversion does.** The central inversion −1 of the level-3 structure acts on a flavour qutrit as c → −c. That
is the transposition (1 2), fixing 0. In a flavour basis (e, μ, τ) ↔ (0, 1, 2) it is **μ–τ reflection**.

**Which sectors respect it.** Every zero-characteristic (Wilson-line-free) theta-null Yukawa commutes with it
(Pass 11941). So every Wilson-free sector is μ–τ symmetric, and its odd mass state is exactly (0,1,−1)/√2.

**Novelty.** The corpus discusses S₃, S₄ and TM₁ residual symmetries (Passes 11225, 11243), but not μ–τ reflection as the
central element of the theta level structure.

## 2. The parity identities (exact)

**Lemma.** Let one sector be P-symmetric, with odd state o. Then for every state a of the other sector,
|⟨a|o⟩| = ‖P_odd a‖, because the odd subspace is one-dimensional. Checked on 2000 random bases: equality holds to
10⁻¹⁶.

**Quarks.**
* The up coupling is Wilson-free (Passes 11941/11942), and its odd state is the middle one, charm.
* So **the CKM charm row is the odd content of the down states**: (|V_cd|, |V_cs|, |V_cb|) = (‖P_odd d‖, ‖P_odd s‖,
  ‖P_odd b‖).
* The fits satisfy this to 10⁻⁹: (0.2257, 0.9733, 0.0412), against data (0.221, 0.975, 0.0411).
* The Cabibbo angle *is* the μ–τ-odd admixture of the down quark.

**Leptons.**
* A Wilson-free neutrino sector with the near-product texture has its odd state at ν₂ (exponent 1 sits between 0
  and 2; Pass 11943).
* So (|U_e2|, |U_μ2|, |U_τ2|) = the odd contents of e, μ, τ.
* Data (NuFIT-like central values, δ = 212°): (0.548, 0.605, 0.578). Every charged lepton is about one-third odd, close
  to TM₂. The μ and τ entries depend mildly on δ.
* The minimal fits of Pass 11942 have (0.71, 0.08, 0.70). That is exactly why Pass 11943 failed.

## 3. The fork

The measured mixing fixes how much μ–τ parity must be broken.

**(a) Odd neutrino = ν₂.**
* This keeps the near-product neutrinos and the Weber relation of Passes 11939/11940.
* It needs ‖P_odd ℓ‖ ≈ 0.55–0.60 for **all three** charged leptons: O(1) breaking, far more than in the quark sector.

**(b) Odd neutrino = ν₃** (the usual μ–τ paradigm).
* It needs only ‖P_odd e‖ ≥ |U_e3| = 0.148. That is comparable to the quark sector (‖P_odd d‖ = |V_cd| = 0.221).
* But ν₃ odd needs the odd theta coefficient to dominate, i.e. |Ω₁₂| = O(1). The neutrinos then sit outside the
  near-product regime, and the Weber neutrino relation (Σ = 0.0596 eV) is lost.

**Reading.**
* **Naturalness favours (b).** Comparable μ–τ breaking in quarks and leptons.
* **Cost of (b).** It removes the near-product premise of the 11939/11940 neutrino prediction.
* **Cost of keeping 11939/11940.** The charged leptons must be O(1) μ–τ-broken, with near-trimaximal odd contents.
* Both are concrete targets.
* **The quark half is unaffected.** It is a clean structural reading: in this framework the Cabibbo angle is a μ–τ-odd
  admixture.
