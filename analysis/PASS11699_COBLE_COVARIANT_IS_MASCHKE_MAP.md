# Pass 11699 — the E₈ structure tensor produces the Maschke-to-Burkhardt map: the Coble covariant of the trivector Cartan is −2 × Pass 11663's Pfaffian quartic

Producer: `analysis/w33_pass11699_coble_covariant_is_maschke_map.py`
Certificate: `data/w33_pass11699_coble_covariant_is_maschke_map.json`
Regression: `tests/test_w33_pass11697_11703.py`

**Question (Pass 11693 programme, item 3).** Codex's quartic map from the odd Weil sector to the Burkhardt space (Pass 11663) has the E₈ root rays as its base locus (Pass 11690). Can it be derived from the E₈ bracket itself rather than chosen?

## The intrinsic map

The bracket [x, y] = ∗(x ∧ y) on Λ³V (V = C⁹, Pass 11681) is defined by the volume form ε. Using only ε, define for a trivector x the cubic form on V\*

  **P_x(y) = ⟨(ι_y x)³ ∧ x, vol⟩ = 6 Σ_{|I|=6} Pf((ι_y x)[I,I])·sgn(I,J)·x_J.**

Properties:
* It is an SL(9)-covariant of degree 4.
* So it is equivariant for every determinant-one gate, and Pauli-invariant when x is (checked to 10⁻¹⁵).
* This is the **Gruson–Sam–Weyman** construction of the Coble cubic from a trivector, passing to ι_y x ∈ Λ²C⁸ (Gruson–Sam–Weyman 2013; Rains–Sam 2018; already cited in Pass 11680). The covariant is not new.

## Found

Put x = Σ c_u h_u on the Pauli-singlet Cartan (Pass 11681 basis), and expand P_x in Pass 11663's five Pauli-invariant cubics. Then:

| component | E₈ covariant | Pass 11663 Pfaffian Q |
|---|---|---|
| 0 | 24abcd | −12abcd |
| 1 | −4a(b³+c³+d³) | 2a(b³+c³+d³) |
| 2 | 4b(a³+c³−d³) | 2b(−a³−c³+d³) |
| 3 | 4c(a³−b³+d³) | 2c(−a³+b³−d³) |
| 4 | 4d(a³+b³−c³) | 2d(−a³−b³+c³) |

* **β = −2Q exactly**, in the committed coordinates with c = f. The maximum deviation over 10 random points is 2·10⁻¹³.
* **The image** lies on exactly one quartic, y₁y₂y₃y₄ + (1/6)y₀Σyᵢ³ + (1/48)y₀⁴ = 0. With y₀ = −2t this is the Burkhardt quartic, as Codex already found for Q (Pass 11663, line 85).
* **Base locus.** All 40 Witting rays are zeros (max norm 7·10⁻¹⁵).
* **Uniqueness.** Take Pass 11663's determinant-one Weil generators. The space of equivariant quartic maps from odd (4) to even (5) is **one-dimensional**. Into the dual or conjugate of the even sector it is zero-dimensional.

## Reading

> **The Maschke map is not an extra choice.** It is the unique Clifford-equivariant quartic, and it is the Coble covariant of the two-qutrit E₈ Cartan.

This closes the triangle among three pieces:
* Codex's odd-sector normal map;
* the E₈ Cartan (Pass 11681, with the antilinear intertwiner of Pass 11690);
* the Burkhardt/Coble geometry (Passes 11651–11659).

All three are the same object read three ways.

**What is new:** the coefficient identity on the committed two-qutrit E₈, and the uniqueness count.

**What is classical:** the covariant (GSW), the Maschke parametrisation (Bruin–Filatov 2207.04393 §3.1) and the Burkhardt quartic.
