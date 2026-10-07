# Pass 11645 — time reversal of the Hesse shadow is complex conjugation of a j-invariant; the CP sign is sign Im j

Producer: `analysis/w33_pass11645_time_reversal_is_conjugation_of_j.py`
Certificate: `data/w33_pass11645_time_reversal_is_conjugation_of_j.json`
Regression: `tests/test_w33_pass11641_11646.py`

## Every qutrit state lies on one elliptic curve

Every qutrit state ψ, except the nine Hesse SIC states, lies on exactly one member of the Hesse pencil:

  E_ψ : x³ + y³ + z³ = 3μ xyz,   μ(ψ) = (ψ₀³ + ψ₁³ + ψ₂³)/(3ψ₀ψ₁ψ₂) = √2·u₀/u₁ (Pass 11641's doublet).

Its j-invariant is j = 27μ³(μ³ + 8)³/(μ³ − 1)³. As a check, j − 1728 = 27·(square)/(μ³ − 1)³ exactly.

**Facts (exact or checked on 20 000 random states).**

| statement | result |
|---|---|
| j(gψ) = j(ψ) for every Clifford g (A4 acts on the pencil and fixes j) | 20000/20000 |
| **j(ψ̄) = conj j(ψ): time reversal acts as complex conjugation of j** | 20000/20000 |
| **sign Im j(E_ψ) = sign W(ψ)** (W of Passes 11600/11614, in Pass 11600's axes) | **20000/20000** |
| stabiliser states: E is a triangle (j = ∞); T\|+⟩: Fermat curve (j = 0); CP-symmetric states: j real | checked |

## The theorem

**sign W = sign Im j.**

*Proof.*
1. **Ramification.** j: P¹ → P¹ has degree 12 and is ramified only over three values:
   * 0, at the 4 equianharmonic (T-magic) vertices, with order 3;
   * 1728, at the 6 edge midpoints, with order 2;
   * ∞, at the 4 MUB vertices, with order 3.
2. **The real preimage.** So j⁻¹(R ∪ ∞) is a graph whose vertices are only these 14 points, with valences 6, 4 and 6.
3. **The mirrors.** The 6 mirror great circles of T_d are fixed by antiunitary Cliffords, so their curves are real and
   they map into R ∪ ∞. They meet exactly at those 14 points, with the same valences. Hence j⁻¹(R ∪ ∞) is exactly the
   six mirrors.
4. **The chambers.** The 24 open chambers (Pass 11614) contain no ramification points, so each maps bijectively onto
   the upper or the lower half-plane. Adjacent chambers alternate, and so does sign W. So sign Im j = ε·sign W, with
   ε = +1 checked. ∎

## j in terms of four measured numbers

With σ = Σ_b Π_b, the MUB triple products of Pass 11641:

  |j| = 27·[∏_b (σ − 2Π_b) / ∏_b Π_b]^{3/2} ,
  |j − 1728| = 3√3·∏_{pairings {ab|cd}} [6(Π_a + Π_b)(Π_c + Π_d) − σ²] / [∏_b Π_b]^{3/2} ,
  sign Im j = sign W = −sign ∏_{a<b} (Π_a − Π_b).

* **Structure.** These factorisations follow from j = c·Ψ³/Φ³ (Klein's tetrahedral forms):
  * |Φ|² ∝ ∏Π_b, since Φ vanishes at the MUB vertices;
  * |Ψ|² ∝ ∏(ρ − 6Π_b), since Ψ vanishes at their antipodes;
  * |χ₆|² ∝ ∏(ρ² − x²) over the edge midpoints, and ρ² − x² = 18[6(Π_Z + Π_X)(Π_XZ + Π_XZ²) − σ²] on the cone of
    Pass 11641.
* **Constants.** 27 and 3√3 were identified numerically, with spread < 10⁻⁸.
* **Reading.** The two moduli fix j up to conjugation, and the sign fixes it completely. So **the Hesse curve of a qutrit
  state is read off from four MUB triple-coincidence probabilities**, and its time direction from their ordering.

## Pass 11600's vacuum curve

* The canonical vacuum ray (1,2,3)/√14 has μ = −3 − √42/2 + i(√3 + √14/2).
* Its curve has j_vac = 728.7605 + 10082.4147 i.
* Exact minimal polynomial over Q:
  5168743489X⁴ − 7753689715968X³ + 528945987341869056X² − 23152393432844992512X + 46085036139193181405184.
* Re j satisfies 5168743489X² − 3876844857984X + 80213948338176.
* The leading coefficient is (7·13·19)³ = 1729³. This is arithmetic, not a claim.
* The 24 vacua are the 24 pencil points with j ∈ {j_vac, j̄_vac}: 12 each, the two A4-orbits.

## Reading

**One complex number.** The whole Clifford-invariant content of the Hesse doublet of a family qutrit is a single
complex number, the j-invariant of the elliptic curve the state lies on. Time reversal is its complex conjugation.

**What the sector's statements become.**
* **CP-symmetric** means **j real**.
* **The CP sign** is **the sign of Im j**.
* **Pass 11614's chamber walls** are where **E_ψ is isomorphic to its own conjugate**.
* **Pass 11600's CP-even potential** depends on (Re j, |Im j|) only.
* **The CP-breaking vacuum** is a choice of non-real j.

**Scope.**
* The pencil and its j-invariant are classical (Hesse; Artebani–Dolgachev).
* New here are the identification with the CP order parameter of Passes 11600–11614, the sign theorem, and the
  Π-formulas.
* Nothing here selects j_vac.
