# Moonshine + Monster Group + W(3,3): Precise Mathematical Connections

**Research Date:** 2025  
**Scope:** Exact numerical and structural connections between the j-invariant, Monster group M, Eisenstein series, McKay correspondence, vertex operator algebras, and the generalized quadrangle W(3,3) = GQ(3,3).

---

## 0. Structural Parameters of W(3,3) = GQ(3,3)

The symplectic generalized quadrangle W(3,3) is the polar space of totally isotropic points and lines of PG(3,3) with respect to a non-degenerate symplectic form.

| Parameter | Value | Formula |
|-----------|-------|---------|
| Points (vertices) | **40** | (q+1)(q²+1) with q=3 |
| Lines | **40** | (q+1)(q²+1) = 40 (self-dual) |
| Points per line | 4 | q+1 |
| Lines per point | 4 | t+1 = q+1 |
| Collinearity graph | Sp(4,3) | strongly regular |
| Edges (Sp(4,3)) | **240** | v×k/2 = 40×12/2 |
| Vertex degree k | 12 | q²+q = 9+3 |
| λ (common neighbors of adjacent vertices) | 2 | |
| μ (common neighbors of non-adjacent) | 4 | |
| Automorphism group of GQ(3,3) | **PGSp(4,3)** | order **51840** |
| Automorphism group of collinearity graph | **PGSp(4,3)** | = PSp(4,3).2 |

The automorphism group **PGSp(4,3) ≅ W(E₆)** (Weyl group of E₆) of order **51840**.  
The simple group **PSp(4,3)** of order **25920** is the index-2 subgroup (the "rotation" automorphisms).

**Key isomorphisms:**
- PSp(4,3) ≅ PSU(4,2) ≅ B₂(3) ≅ PSΩ₅(3)  (unique simple group of order 25920)
- W(E₆) ≅ PSp(4,3):2 ≅ PGSp(4,3) ≅ Aut(GQ(3,3) collinearity graph)

Sources: [E₆ Wikipedia](https://en.wikipedia.org/wiki/E6_(mathematics)), [Groupprops PSp(4,3)](https://groupprops.subwiki.org/wiki/Projective_symplectic_group:PSp(4,3)), [LSU four-dimensional symplectic geometry](https://www.math.lsu.edu/~hoffman/papers/spreads4.pdf)

---

## 1. The j-Invariant and W(3,3) Numbers

### 1.1 The j-Invariant Expansion

\[
j(\tau) = q^{-1} + 744 + 196884\,q + 21493760\,q^2 + 864299970\,q^3 + \cdots, \quad q = e^{2\pi i\tau}
\]

### 1.2 The Constant Term 744

**Exact decompositions of 744:**

| Identity | Value |
|----------|-------|
| 3 × 248 | 3 × dim(E₈) |
| 24 × 31 | 24 × (h(E₈) + 1), where h = 30 is the Coxeter number of E₈ |
| 24 + 3×240 | rank(Leech) + 3 × |roots(E₈)| = 24 + 3 × (edges of GQ(3,3)) |
| 720 + 24 | h(E₈)×rank(Leech) + rank(Leech) |

**Moonshine explanation of 744:**  
The Leech lattice theta function satisfies:
\[
\frac{\Theta_\Lambda(\tau)}{\eta(\tau)^{24}} = J(\tau) + 24
\]
where J(τ) = j(τ) − 744. The constant 24 is the rank of the Leech lattice. The full j-function constant 744 = 720 + 24 = 3 × 240 + 24.

**W(3,3) connection:** 240 = edges of GQ(3,3) collinearity graph = E₈ roots. Therefore:
\[
744 = 24 + 3 \times (\text{edges of } W(3,3)) = \text{rank}(\Lambda_{24}) + 3 \times |\text{roots}(E_8)|
\]

Source: [Monstrous Moonshine from Orbifolds (Tuite)](https://projecteuclid.org/journals/communications-in-mathematical-physics/volume-146/issue-2/Monstrous-Moonshine-from-orbifolds/cmp/1104250193.pdf), [Borcherds moonshine proof](https://math.berkeley.edu/~reb/papers/monster/monster.pdf)

### 1.3 The Coefficient 196884 and 196883

\[
196884 = 196883 + 1
\]

**Prime factorization:**
- 196884 = 2² × 3³ × 1823 = 4 × 49221 = 12 × 16407
- 196883 = **47 × 59 × 71** (all three primes divide |M|)

**W(3,3) numerical checks:**

| Division | Result | Integer? |
|----------|--------|----------|
| 196884 / 40 | 4922.1 | No |
| 196884 / 240 | 820.35 | No |
| 196884 / 12 | **16407** | **Yes** |
| 196884 / 4 | 49221 | Yes |

**Key observation:** 196884 = 12 × 16407, where **12 = vertex degree of GQ(3,3)**. However, 16407 = 9 × 1823 where 1823 is prime and has no known W(3,3) or group-theoretic interpretation.

**Monster representation decomposition:**
- V₂♮ (graded piece of moonshine module) = ρ₁ ⊕ ρ₁₉₆₈₈₃ (dim = 196884)
- This is the ONLY decomposition: 196884 = 1 + 196883

**Note on 196883 = 47 × 59 × 71:** These are the three largest prime factors of the Monster order. The dimension of the smallest nontrivial Monster representation equals the product of the three largest primes dividing |M|. This is not a W(3,3) relation but a pure Monster numerology fact. See [3Blue1Brown on Monster](https://www.3blue1brown.com/lessons/groups-and-monsters).

### 1.4 Higher Coefficients — Moonshine Decompositions

The Monster has 194 irreducible representations with smallest dimensions:  
r₁ = 1, r₂ = 196883, r₃ = 21296876, r₄ = 842609326, ...

| j-coeff | Decomposition |
|---------|---------------|
| **c(1) = 196884** | r₁ + r₂ = 1 + 196883 |
| **c(2) = 21493760** | r₁ + r₂ + r₃ = 1 + 196883 + 21296876 |
| **c(3) = 864299970** | 2r₁ + 2r₂ + r₃ + r₄ = 2 + 2×196883 + 21296876 + 842609326 |

Source: [Monstrous Moonshine Wikipedia](https://en.wikipedia.org/wiki/Monstrous_moonshine), [Secret Blogging Seminar](https://sbseminar.wordpress.com/2009/01/08/generalized-moonshine-i-genus-zero-functions/)

### 1.5 Direct W(3,3) Connection to 196884 — Assessment

**FINDING:** No known direct W(3,3)-specific decomposition of 196884 exists in the literature. The division 196884 = 12 × 16407 uses the GQ(3,3) vertex degree (12) but the quotient 16407 is arithmetically opaque (= 9 × 1823, with 1823 prime). The correct decomposition of 196884 is purely via Monster irreducible representations.

---

## 2. W(E₆) and the Monster Group

### 2.1 The Group Theory

| Group | Order | Description |
|-------|-------|-------------|
| PSp(4,3) | **25920** = 2⁶×3⁴×5 | Simple group, = PSU(4,2) |
| W(E₆) | **51840** = 2⁷×3⁴×5 | Weyl group of E₆, = PSp(4,3):2 |
| Monster M | **≈ 8.08×10⁵³** | Largest sporadic simple group |

### 2.2 Subgroup Chain: GQ(3,3) → W(E₆) → Monster

The precise embedding chain is:

```
GQ(3,3) collinearity graph
    ↓ (automorphism group)
PGSp(4,3) = W(E₆) [order 51840]
    ↓ (Weyl group inclusion)
²E₆(2) [order ≈ 2.3×10²³]
    ↓ (maximal subgroup embedding)
Monster M [order ≈ 8.08×10⁵³]
```

**Step 1:** W(E₆) = PGSp(4,3) is the automorphism group of the GQ(3,3) collinearity graph (the Sp(4,3) symplectic graph).

**Step 2:** W(E₆) is the Weyl group of the Lie algebra E₆. The twisted Chevalley group ²E₆(2) has W(E₆) as its Weyl group. W(E₆) embeds in ²E₆(2) as the normalizer of a maximal torus modulo the torus.

**Step 3:** Monster M contains ²E₆(2) via **maximal subgroup #4:**  
\[ \text{Monster maximal subgroup \#4: } 2^2 \cdot {}^2E_6(2) \cdot S_3 \]
with order 2³⁹ × 3¹⁰ × 5² × 7² × 11 × 13 × 17 × 19 = 1,836,779,512,410,596,494,540,800.

**CONCLUSION:** W(E₆) ≅ Aut(GQ(3,3) collinearity graph) **IS a subgroup of the Monster**, embedded via the chain W(E₆) ↪ ²E₆(2) ↪ 2².²E₆(2).S₃ ↪ M.

**PSp(4,3) as Monster subgroup:** PSp(4,3) is the index-2 subgroup of W(E₆), hence also embeds in M by the same chain. Its order 25920 = 2⁶×3⁴×5 divides |M|, which is a necessary (though not sufficient) condition.

Source: [Monster group Wikipedia – maximal subgroups](https://en.wikipedia.org/wiki/Monster_group), [arXiv:2304.14646 maximal subgroups](https://arxiv.org/abs/2304.14646), [LSU symplectic geometry paper](https://www.math.lsu.edu/~hoffman/papers/spreads4.pdf), [E₆ Wikipedia Weyl group](https://en.wikipedia.org/wiki/E6_(mathematics))

### 2.3 W(E₆) Is NOT a Maximal Subgroup of the Monster

The 46 maximal subgroups of M (as of 2025, fully classified) do **not** include PSp(4,3) or W(E₆) directly. PSp(4,3) and W(E₆) are subgroups of M but not maximal — they are contained in larger subgroups such as ²E₆(2) or the orthogonal groups O⁻₈(3), O⁺₈(3) that appear in the maximal subgroup list.

Source: [arXiv:2304.14646 – complete maximal subgroup classification](https://arxiv.org/abs/2304.14646), [Monash University publication](https://research.monash.edu/en/publications/the-maximal-subgroups-of-the-monster/)

---

## 3. The Eisenstein Series and W(3,3)

### 3.1 Eisenstein Series with W(3,3) Parameters

| Series | q-expansion | Key coefficient |
|--------|-------------|-----------------|
| E₄(τ) | 1 + **240**q + 2160q² + 6720q³ + ... | **240** = E₈ roots = GQ(3,3) edges |
| E₆(τ) | 1 − **504**q + 16632q² − ... | 504 = 7 × 72, where 72 = E₆ roots |
| E₈(τ) = E₄² | 1 + **480**q + 61920q² + ... | **480** = 2 × 240 = 2 × GQ(3,3) edges |

**Exact formulas:**
\[
E_4(\tau) = 1 + 240 \sum_{n=1}^\infty \sigma_3(n)\,q^n, \qquad E_6(\tau) = 1 - 504\sum_{n=1}^\infty \sigma_5(n)\,q^n
\]

### 3.2 The 240 Coincidence: E₈ Roots = GQ(3,3) Edges

**240** appears as:
1. The number of roots of the E₈ root system (the shortest vectors in the E₈ lattice)
2. The number of edges of the GQ(3,3) collinearity graph (Sp(4,3))
3. The leading coefficient of the normalized Eisenstein series E₄(τ)
4. The |W(E₈)| / |W(E₇)| = 696729600 / 2903040 = 240 (orbit size of E₈ roots under W(E₇))

**Is this coincidence?** Partially. The coincidence 240 = E₈ roots = GQ(3,3) edges is genuine numerically, but the mathematical mechanisms are distinct:
- **E₈ roots:** arise from the lattice structure of E₈ in ℝ⁸ (112 vectors of type ±eᵢ±eⱼ plus 128 half-integer vectors)
- **GQ(3,3) edges:** arise from the symplectic structure of PG(3,3) over 𝔽₃

Both numbers equal 240 because both are controlled by the symplectic/orthogonal symmetry groups over related fields. The Sp(4,3) graph (240 edges) and E₈ root system (240 vectors) are both degree-4 "B₂-type" structures, but over 𝔽₃ vs ℝ respectively.

### 3.3 The 504 = 7 × 72 Connection

504 = 2³ × 3² × 7 admits:
- **504 = 7 × 72** where 72 = number of E₆ roots
- **504 = |PSL(2,8)|** since |PSL(2,8)| = 8(8²−1)/gcd(2,7) = 8×63 = 504
- **504 = 6 × 84** where 84 = ?

The E₆ connection (504 = 7 × 72) is numerically striking but not structurally established in the literature. The 504 arises from the Bernoulli number B₆ = −1/42 and the formula for E₆ coefficients: E₆ first coefficient = (−2k)/B₂k evaluated at k=3 gives −6/B₆ = −6/(−1/42) = 252... wait, actually the normalization is −504 (the sign convention). More precisely: 504 = 2 × 252 = 2 × (dual Coxeter number of E₇ × something). The identification 504 = 7 × 72 is a numerological curiosity without deeper known significance.

Source: [Eisenstein series Wikipedia](https://en.wikipedia.org/wiki/Eisenstein_series), [E₈ lattice Wikipedia](https://en.wikipedia.org/wiki/E8_lattice)

### 3.4 The j-Invariant as E₄³/Δ

\[
j(\tau) = \frac{E_4(\tau)^3}{\Delta(\tau)}, \qquad \Delta(\tau) = \eta(\tau)^{24} = q\prod_{n=1}^\infty (1-q^n)^{24}
\]

| Factor | W(3,3) connection |
|--------|-------------------|
| E₄ coefficient = 240 | = edges of GQ(3,3) |
| η²⁴ exponent = 24 | = rank of Leech lattice (no W(3,3) connection) |
| E₄³ = 1 + 720q + ... | 720 = 3 × 240 = 3 × GQ(3,3) edges |
| j constant = 744 | = 720 + 24 = 3×edges(GQ(3,3)) + rank(Leech) |

### 3.5 Question: Modular Form With All-GQ(3,3) Coefficients?

**The question:** Does there exist a modular form f(τ) = Σ aₙqⁿ such that all aₙ are W(3,3) invariants?

**Answer:** Not known to exist in the strict sense. However:

- The **theta function of the E₈ lattice** E₄(τ) = 1 + 240q + 2160q² + ... has its first coefficient equal to a GQ(3,3) invariant (240 edges), but subsequent coefficients (2160 = 240×σ₃(2) = 240×9, etc.) are not GQ(3,3) parameters.

- The **McKay-Thompson series T_g(τ)** for elements g of Monster in the subgroup ²E₆(2) would be modular functions with W(E₆)-equivariant properties. For elements g in the W(E₆) ⊂ ²E₆(2) ⊂ M subgroup chain, the series T_g are Hauptmoduls for certain genus-0 subgroups of SL₂(ℝ), and their coefficients involve traces of g on Monster representations. These are the closest known analog.

- There is **no known VOA** or modular form whose full Fourier expansion consists entirely of GQ(3,3) combinatorial invariants.

---

## 4. The McKay Correspondence and Generalized Quadrangles

### 4.1 Classical McKay Correspondence

The McKay correspondence: finite subgroups G ⊂ SU(2) ↔ extended Dynkin diagrams of ADE type ↔ ADE singularities ℂ²/G.

| Subgroup of SU(2) | Order | Dynkin type |
|-------------------|-------|-------------|
| Cyclic Zₙ | n | Ãₙ₋₁ |
| Binary dihedral D̃ₙ | 4(n-2) | D̃ₙ |
| Binary tetrahedral | 24 | Ẽ₆ |
| Binary octahedral | 48 | Ẽ₇ |
| Binary icosahedral | 120 | Ẽ₈ |

### 4.2 PSp(4,3) Is NOT a Finite Subgroup of SU(2)

PSp(4,3) has order 25920 and is simple. Finite subgroups of SU(2) have orders 1, 2, 3, 4, 6, 8, 12, 24, 48, 120 — none equal to 25920. **Therefore standard McKay correspondence does not apply to PSp(4,3) or GQ(3,3).**

### 4.3 McKay's Extended E₈ Observation for the Monster

McKay observed (1979) that the **9 conjugacy classes of pairs of 2A-involutions** in the Monster correspond to the **9 nodes of the extended Ẽ₈ Dynkin diagram**, with the orders of the product of involution pairs matching the Ẽ₈ node labels {1,2,3,4,5,6,4,2,3} (Coxeter number h = 30).

This is a McKay-type correspondence at the level of the Monster, involving E₈ rather than subgroups of SU(2). The construction proceeds through:
- The moonshine module V♮
- Conformal vectors of central charge 1/2
- Miyamoto involutions (bijection: 2A-involutions of M ↔ c=1/2 Virasoro vectors in V♮)

**GQ(3,3) does not appear** in this McKay-E₈-Monster correspondence.

Source: [A moonshine path from E₈ to the Monster (Griess-Lam)](https://sites.lsa.umich.edu/rlg/wp-content/uploads/sites/1335/2024/09/moonshinepath13oct09.pdf), [McKay's E₇ observation (Baby Monster)](https://arxiv.org/pdf/1002.1777)

### 4.4 Generalized McKay Correspondence and Generalized Quadrangles

**What is known:**
1. The classical McKay correspondence generalizes to **finite subgroups G ⊂ SL(2,ℂ)** → ADE Dynkin diagrams (same result) and partially to **finite subgroups G ⊂ SL(3,ℂ)** → non-ADE quivers (Craw-Ishii, 2002; Bezrukavnikov-Kaledin).

2. Generalized quadrangles arise naturally from **buildings** of type B₂ = C₂ (the rank-2 building for symplectic groups). The Dynkin diagram B₂ is the diagram with two nodes connected by a double bond.

3. The automorphism groups of classical GQ correspond to groups of Lie type: W(3,q) → PSp(4,q), Q(4,q) → PΩ(5,q), Q⁻(5,q) → PSU(4,q). These are NOT subgroups of SU(2) and are therefore outside the classical McKay setting.

4. **Proposed generalization:** A McKay correspondence for GQ would need to relate:
   - Polar spaces (GQ, generalized hexagons, octagons) 
   - Dynkin diagrams of types B, C, G₂, F₄
   - Singularities of the form ℂ²/G where G is a Weyl group?
   
   No rigorous such correspondence is established in the literature.

5. **Monster-building connection:** The Monster has a presentation by the incidence graph of the projective plane of order 3 (21 involutions for M, 26 for the Bimonster M≀C₂). Projective planes are related to (but distinct from) generalized quadrangles. The projective plane PG(2,3) is a generalized "3-gon," while GQ is a generalized "4-gon."

Source: [McKay correspondence nLab](https://ncatlab.org/nlab/show/McKay+correspondence), [Generalizations of McKay](https://ymsc.tsinghua.edu.cn/en/info/1050/2868.htm), [Monstrous Moonshine 25 years](https://arxiv.org/pdf/math/0402345)

---

## 5. Vertex Operator Algebras and GQ(3,3)

### 5.1 The Moonshine Module V♮

**Construction (Frenkel-Lepowsky-Meurman, 1988):**
1. Start with Leech lattice Λ (rank 24, no roots, even self-dual)
2. Build lattice VOA V_Λ
3. Form Z₂-orbifold: V♮ = (V_Λ ⊕ V_Λ^{twisted})^h, where h = −1 involution of Λ

**Properties:**
- Aut(V♮) = Monster M (proven by FLM)
- Graded dimension: J(τ) = j(τ) − 744 = q⁻¹ + 196884q + ...
- Central charge c = 24
- No level-1 states (V₁♮ = 0)

Source: [Monstrous moonshine Wikipedia](https://en.wikipedia.org/wiki/Monstrous_moonshine), [What is moonshine? (Borcherds)](https://math.berkeley.edu/~reb/papers/icm98/icm98.pdf)

### 5.2 Known VOA Connections to Root Systems and Symplectic Groups

The moonshine module V♮ is built from the Leech lattice, which in turn decomposes as:
\[
\Lambda_{24} \supset E_8^{\oplus 3} \text{ (as sublattice)}
\]
The E₈ lattice VOA V_{E_8} is the basic building block. Its theta function = E₄(τ) = 1 + **240**q + ...

**Connection to GQ(3,3):** The number 240 = GQ(3,3) edges appears as the first non-trivial Fourier coefficient of E₄(τ), which is the theta function of E₈. The Leech lattice theta function divided by η²⁴ gives the j-function. This is the **deepest known connection** between the moonshine construction and the GQ(3,3) number 240.

### 5.3 No Direct GQ(3,3) VOA Construction in Literature

Systematic searches of papers by:
- **Conway & Norton** (1979) — no GQ mention
- **Borcherds** (1986–1992) — no GQ mention  
- **Frenkel, Lepowsky, Meurman** (1988) — no GQ mention
- **Carnahan** (generalized moonshine) — no GQ mention

**No paper in the moonshine literature** references generalized quadrangles GQ(s,t) or symplectic polar spaces W(n,q) in the context of VOA constructions.

### 5.4 The Symplectic Singularities and VOA Connection

There is a **recent research program** (Arakawa et al., BIRS 2024) connecting symplectic singularities with vertex algebras. The paper "Symplectic singularities and vertex algebras" ([BIRS 2024](https://www.birs.ca/iasm-workshops/2024/24w5501/files/9.3-01%20Tomoyuki%20Arakawa.pdf)) constructs VOAs associated to symplectic resolutions. Generalized quadrangles are affine buildings of type C₂ = B₂, and their point-stabilizers are precisely symplectic groups. This is a potential (currently undeveloped) connection route.

### 5.5 The Qudit/Quantum Information Connection

An indirect connection exists through quantum information: the paper "The N-qudit fabric: Pauli graph and finite geometries" ([Saniga 2007](https://www.astro.sk/~msaniga/pub/ftp/ICSSUR2007_oral.pdf)) shows that symplectic polar spaces W(q) classify the commutation structure of Pauli operators on n-qudit systems. Specifically, W(3,3) classifies 2-qutrits. While moonshine connects to string theory (bosonic string on Leech torus), no direct path from W(3,3) qudit geometry to moonshine VOA has been established.

---

## 6. Summary of Exact Numerical Connections

### 6.1 Confirmed Exact Connections

| Connection | Numerical identity | Status |
|------------|-------------------|--------|
| GQ(3,3) edges = E₈ roots | 240 = 240 | **CONFIRMED** |
| GQ(3,3) edges = E₄ first coefficient | 240 = 240 | **CONFIRMED** |
| Aut(GQ(3,3)) = W(E₆) | |W(E₆)| = 51840 | **CONFIRMED** |
| W(E₆) ↪ Monster M | via ²E₆(2) ↪ Monster | **CONFIRMED** |
| 744 = 24 + 3×240 | rank(Leech) + 3×(GQ edges) | **CONFIRMED (numerically)** |
| 480 = 2 × 240 | E₈ coeff = 2 × GQ edges | **CONFIRMED** |

### 6.2 Unconfirmed / Negative Results

| Claim | Status |
|-------|--------|
| 196884 decomposes in W(3,3) parameters | **NO** — decomposes as 196883+1 via Monster reps |
| GQ(3,3) yields a modular form | **NOT KNOWN** — no such form identified |
| PSp(4,3) is maximal in Monster | **NO** — it is a sub-subgroup |
| McKay correspondence extends to GQ | **NOT ESTABLISHED** in the literature |
| VOA constructed from GQ(3,3) | **NOT FOUND** in the literature |

### 6.3 The Central Numerical Fact

The most precise and exact connection found is:

\[
\boxed{240 = |\text{edges of } W(3,3)| = |\text{roots of } E_8| = \text{first Fourier coefficient of } E_4(\tau)}
\]

Combined with:
\[
j(\tau) = \frac{E_4(\tau)^3}{\Delta(\tau)} \implies j(\tau) \text{ encodes the 240-edge structure of GQ(3,3) in its leading coefficient}
\]

And:
\[
\text{Aut}(\text{GQ}(3,3) \text{ collinearity graph}) = W(E_6) \hookrightarrow {}^2E_6(2) \hookrightarrow 2^2 \cdot {}^2E_6(2) \cdot S_3 \hookrightarrow \mathbb{M}
\]

---

## 7. Open Questions and Research Directions

1. **The 196884 puzzle:** Is there a natural 196884-dimensional representation of the Monster that decomposes under the W(E₆) ≅ Aut(GQ(3,3)) subgroup, with the decomposition reflecting GQ(3,3) geometry?

2. **GQ(3,3) and the Monster Lie algebra:** The Monster Lie algebra m has root multiplicities = j-coefficients. Does the Weyl group W(E₆) = Aut(GQ(3,3)) act naturally on m or its root system?

3. **Generalized McKay:** GQ(s,s) are buildings of type B₂. Is there a McKay-type correspondence: B₂ buildings ↔ ??? (analogous to A₁ buildings = trees ↔ ADE Dynkin diagrams)?

4. **McKay-Thompson series for W(E₆) elements:** For elements g ∈ W(E₆) ⊂ M, the McKay-Thompson series T_g(τ) are Hauptmoduls for certain genus-0 subgroups. Computing these for specific W(E₆) representatives would give modular forms naturally associated to GQ(3,3).

5. **Theta function of GQ(3,3)-associated lattice:** Is there a lattice L associated to GQ(3,3) (e.g., the lattice of 𝔽₃-points of the dual building) whose theta function has coefficients that are GQ(3,3) invariants?

---

## 8. Key References and URLs

| Source | URL |
|--------|-----|
| Monstrous Moonshine (Wikipedia) | https://en.wikipedia.org/wiki/Monstrous_moonshine |
| Monster group (Wikipedia) | https://en.wikipedia.org/wiki/Monster_group |
| E₆ Weyl group (Wikipedia) | https://en.wikipedia.org/wiki/E6_(mathematics) |
| Eisenstein series (Wikipedia) | https://en.wikipedia.org/wiki/Eisenstein_series |
| E₈ lattice (Wikipedia) | https://en.wikipedia.org/wiki/E8_lattice |
| Maximal subgroups of Monster (arXiv 2304.14646) | https://arxiv.org/abs/2304.14646 |
| Monstrous Moonshine: 25 years (arXiv math/0402345) | https://arxiv.org/pdf/math/0402345 |
| Borcherds moonshine proof | https://math.berkeley.edu/~reb/papers/monster/monster.pdf |
| Borcherds: What is moonshine? | https://math.berkeley.edu/~reb/papers/icm98/icm98.pdf |
| Groupprops: PSp(4,3) | https://groupprops.subwiki.org/wiki/Projective_symplectic_group:PSp(4,3) |
| LSU: Symplectic geometry over 𝔽₃ | https://www.math.lsu.edu/~hoffman/papers/spreads4.pdf |
| McKay path E₈ → Monster | https://sites.lsa.umich.edu/rlg/wp-content/uploads/sites/1335/2024/09/moonshinepath13oct09.pdf |
| A moonshine path ScienceDirect | https://www.sciencedirect.com/science/article/pii/S0022404910001556 |
| W(E₆) odd presentation | https://www.math.ru.nl/~heckman/An%20odd%20presentation%20for%20W(E_6).pdf |
| Moonshine module for Conway group | https://www.cambridge.org/core/services/aop-cambridge-core/content/view/DBB48A6B72D7D9B64FBD5C818D047C37/S2050509415000079a.pdf |
| Monstrous moonshine from orbifolds | https://projecteuclid.org/journals/communications-in-mathematical-physics/volume-146/issue-2/Monstrous-Moonshine-from-orbifolds/cmp/1104250193.pdf |
| Generalized quadrangle (Wikipedia) | https://en.wikipedia.org/wiki/Generalized_quadrangle |
| McKay correspondence (nLab) | https://ncatlab.org/nlab/show/McKay+correspondence |
| Symplectic singularities & VOAs (BIRS) | https://www.birs.ca/iasm-workshops/2024/24w5501/files/9.3-01%20Tomoyuki%20Arakawa.pdf |
| Characterizations of symplectic polar spaces | https://arxiv.org/pdf/2205.14426 |
| Sp(4,2) GQ page | https://aeb.win.tue.nl/graphs/GQ22.html |
| E₄ theta function OEIS A004009 | https://oeis.org/A004009 |
| Conformal field theories with sporadic groups | https://par.nsf.gov/servlets/purl/10299493 |
| PSp(4,3) subgroup lattice | https://leemans.dimitri.web.ulb.be/atlaslat/psu42.pdf |
