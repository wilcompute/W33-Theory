# Passes 11879–11883: the Siegel modulus is the flat direction of an E₈ Higgs field

Producer: `analysis/w33_pass11879_11883_e8_higgs_siegel_modulus.py`
Certificate: `data/w33_pass11879_11883_e8_higgs_siegel_modulus.json` (13/13 checks)
Regression: `tests/test_w33_pass11879_11883.py`
Track: Claude.

## The question

Passes 11869–11878 read W(3,3) as the level-3 structure of a genus-2 modulus Ω. That left open where Ω comes from, and
what fixes it. Two facts were already on the table:
* The parallel track's TOE40/41 list "a full Sp(4,ℤ)-invariant potential" as their first open target.
* The corpus already owns the E₈ side of the answer:
  * E₈ = sl₉ ⊕ Λ³ℂ⁹ ⊕ Λ⁶ℂ⁹ for two qutrits (11681);
  * the Vinberg Cartan of Λ³ℂ⁹ is the odd Weil 4, "Di" (11680/11699);
  * its GSW Coble covariant is Maschke's quartic map onto the Burkhardt quartic (11699).

The 84 = Λ³ℂ⁹ is exactly the ℤ₃-twisted (W(3,3)-twist) matter of E₈. So I asked whether the modulus is a Higgs vev.

## 11879: the E₈ Cartan is the moduli space of genus-2 curves with a Weierstrass point

Take a torus Ω. For each half-integer characteristic (α,β) form the level-3 theta-null θ[c/3+α, β](0, 3Ω), then remove the
Pauli twist diag(ω^{c·2β}).

**Forward direction, on 3 random moduli:**
* The **six odd characteristics** give vectors lying exactly in the odd 4 (≤ 10⁻¹² oddness).
* Their Maschke images equal the Coble point of the even theta-null ψ(Ω), to 10⁻¹².
* The six points are distinct.
* The **ten even characteristics** do not match (mismatch ≥ 10⁻⁶).

**Inverse direction.** Take random Cartan points c. Least squares finds a torus whose Coble point is Maschke(c), with
residual ≤ 10⁻¹⁰, and c *is* (projectively) one of that torus's six odd theta-nulls, to 10⁻¹⁰.

**What this means.** The Cartan P³ of the 84 is the moduli space of level-3 genus-2 curves *together with a Weierstrass
point* (equivalently, an odd spin structure). The 6:1 Maschke map forgets that point.
* **Prior art:** the degree-6 map and its Weierstrass interpretation are stated by Bruin–Filatov (arXiv:2207.04393,
  Thm 1.1(b), §3.2), with no theta formulas.
* **New here:** the explicit odd-characteristic theta realisation and the qutrit/E₈ reading.

**Physics.**
* **Di is the odd-spin-structure sector.** The odd spin structures are the ones carrying Dirac zero modes on the curve,
  so this sharpens 11875, where Di was the odd theta gradients.
* **Rac is the even sector**, which has no zero modes.

## 11880: the 84 breaks SU(9) to the two-qutrit Pauli group, and to trinification at the W(3,3) points

**A generic Cartan vev**, and also a random 84 vev, has zero stabiliser Lie algebra in gl(9) and in u(9). SU(9) is
therefore broken to a finite group, and that group contains the two-qutrit Pauli group exactly:
* the four generators fix the vev to 10⁻¹⁵, with det 1;
* ωI is unbroken;
* ζ₉I is broken.

**So W(3,3) is the commutation geometry of the unbroken discrete gauge group of a Higgsed SU(9).** It emerges; it is not
put in.

**At each of the 40 Witting rays**, i.e. the E₈ root rays, which are the W(3,3) points (11681):
* the stabiliser is 24-dimensional, with rank 6 and zero centre (complex and compact);
* that is **SU(3)³: trinification**;
* in coordinates, the ray trivector is the sum of three disjoint decomposable 3-forms, one per affine line of a
  parallel class.

**The resulting picture:**
* the generic vacuum carries a discrete Pauli gauge symmetry;
* the 40 enhanced-symmetry points carry trinification;
* these points are the base locus of the Maschke map, i.e. the degenerations of the curve.

This is the standard enhanced-symmetry-point structure of a string moduli space, realised by a 4d gauge theory.

**Known versus new.** Finiteness of generic stabilisers is Vinberg–Elashvili theory, and the Heisenberg stabiliser is
in Gruson–Sam–Weyman. The trinification enhancement at the Witting rays and the gauge-theory reading are what this pass
adds.

## 11881: the renormalizable potential has a flat Kempf–Ness moduli space, and that space is the Siegel modulus

**Only two quartic invariants.** Sym²(84) has exactly two independent quartic SU(9) invariants: (tr ρ)² and tr ρ², with
ρ = x x† contracted on two indices. The rank of four candidate contractions is exactly 2, matching the plethysm
Sym²Λ³ = S₂₂₂ ⊕ S₂₁₁₁₁. The most general renormalizable potential is therefore

  V = −μ²|x|² + λ₁|x|⁴ + λ₂ tr ρ².

**λ₂ > 0.** The bound tr ρ² ≥ (tr ρ)²/9 is saturated exactly when ρ ∝ I, which is the moment map μ = 0:
* every Cartan point saturates it, including all 40 Witting rays (to 10⁻¹⁶);
* random 84s do not (ratio ≥ 0.13).

So the vacuum manifold is the Kempf–Ness set μ⁻¹(0) = SU(9)·h.
* **Local dimension:** 168 − rank dμ = 88 = 80 (orbit) + 8 (the Cartan).
* **Modulo gauge:** h/G₃₂, the cone over the genus-2 moduli with a level-3 structure and a Weierstrass point.

**The Siegel modulus of 11869–11878 is the classical flat direction of the most general renormalizable SU(9) + 84
theory.**

**λ₂ < 0.** The vacuum is a decomposable trivector, with ratio exactly 1/3. The u(9) stabiliser has dimension 44:
su(3) ⊕ su(6) ⊕ u(1)′, where u(1)′ combines an SU(9) generator with the accidental phase symmetry.

## 11882: the modulus is flat to all renormalizable orders; the first lift is at dimension 12

**The test.** The Clifford normaliser acts on h by the Witting group. Exact linear algebra on Sym^d(ℂ⁴), using the
common fixed vectors of the five generators, finds:
* no invariant in degrees 1–11;
* exactly one in degree 12;
* (scratch run to degree 18) one more in degree 18.

These match the Vinberg–Elashvili degrees 12, 18, 24, 30.

**Consequences.**
* **The modulus is not fixed by any renormalizable term.** The renormalizable potential sees only |x|² and tr ρ², which
  are flat along h. So the genus-2 modulus, together with the accidental overall phase of x, is lifted only by holomorphic
  terms of degree ≥ 12: dimension-12 operators, suppressed by Λ⁻⁸. That makes the modulus naturally light.
* **CP comes from the same operators.** A complex coefficient κ in κ·I₁₂(x) + c.c. is the CP-odd datum. The invariant
  ratios of 11878 are rational functions of these Maschke invariants pulled back to the Burkhardt quartic. So the CP
  phase of the torus (11870/11878) and the phase of the degree-12 operator are the same object.
* **The accidental phase.** The overall phase of x is a symmetry of the renormalizable theory broken only at degree 12.
  It behaves like an axion-like direction tied to the modulus's CP phase. This is a reading, not computed dynamics.

## 11883: synthesis: what this changes

The corpus's finite objects now sit inside one ordinary gauge theory: SU(9) with a single 84, the ℤ₃-twisted half of E₈.

| corpus object | in the SU(9) + 84 theory |
|---|---|
| two-qutrit Pauli group / W(3,3) | the unbroken discrete gauge group of a generic vacuum (and its commutation geometry) |
| W(3,3) points = Witting rays = E₈ root rays | the 40 enhanced-symmetry vacua, unbroken SU(3)³ (trinification) |
| the genus-2 modulus Ω (11869–11878) | the flat direction of the renormalizable potential (Kempf–Ness set modulo SU(9)) |
| Di (odd Weil 4) | the Cartan of the 84 = odd spin structures = Weierstrass points |
| Burkhardt quartic / Coble cubic | the image of the vacuum moduli forgetting the Weierstrass point (6:1) |
| generalised CP / the qutrit arrow | the phase of the first lifting operator (degree 12) |

**The physically new statements:**
1. The corpus's finite qutrit structure emerges as a Higgs phase.
2. Trinification sits at the W(3,3) points.
3. The modulus is classically flat and lifted only at dimension 12.

**What is not done here:**
* no Coleman–Weinberg computation of the one-loop lifting (the obvious next step);
* no embedding of this SU(9) into the realistic heterotic or brane vacua: in the flagship, SU(9) contains the SM, so an
  84 vev there would break it, and the natural home is a hidden or second E₈;
* no fermion coupling;
* no fit to data.

## Next

1. The one-loop Coleman–Weinberg potential on h: it is G₃₂-invariant. Does it select the trinification rays (Michel's
   maximal-isotropy points) or a generic Heisenberg point?
2. Place the 84 in the hidden E₈ of E₈×E₈, so the visible SM is untouched and the modulus and the Pauli discrete gauge
   symmetry act on the hidden sector and on flavour.
3. Near a trinification ray, give the hierarchy and CP phase as functions of the displacement in h. These are 11876 and
   11878 in Higgs variables.

## Prior art

* Vinberg–Elashvili (1978) on Λ³ℂ⁹ and G₃₂.
* Gruson–Sam–Weyman (2013) on Coble cubics from trivectors and Heisenberg stabilisers.
* Bruin–Filatov (arXiv:2207.04393) on the degree-6 Maschke P³ → Burkhardt and Weierstrass points.
* Kempf–Ness (1979).
* Hunt (Burkhardt).
* Corpus:
  * Passes 11680, 11681, 11690, 11699, 11651–11659;
  * Passes 11869–11878;
  * TOE38–41 (parallel track: framing firewall, theta parity, Clifford-frame purity, Albert cubic in trinification
    coordinates).
