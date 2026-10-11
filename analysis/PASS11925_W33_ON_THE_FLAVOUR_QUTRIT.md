# Pass 11925: W(3,3) seen from the flavour qutrit — collinear points are stabiliser states (the charm–up lock), non-collinear points are the maximally magic strange states (the theta-zero law)

Producer: `analysis/w33_pass11925_w33_on_the_flavour_qutrit.py`
Certificate: `data/w33_pass11925_w33_on_the_flavour_qutrit.json`
Regression: `tests/test_w33_pass11925.py`
Track: Claude.

**Builds on.**
* The parallel packet 34e149d79: the flavour-Higgs qutrit is the transverse tangent of a Witting ray of the E8 84-Higgs
  Cartan.
* Passes 11923 and 11924: the stabiliser lock and the residual S₃.

## Setup

**The tangent qutrit.** Take v = e₀ among the 40 Witting rays of ℂ⁴ (the Pass 11879 list). On v⊥ = span(e₁, e₂, e₃),
the canonical qutrit Paulis X (cyclic shift) and Z = diag(1, ω, ω²) fix v and permute all 40 rays. So v⊥ is the
flavour qutrit, with its H₂₇ acting in the standard way.

## 1. Collinear points are the stabiliser states

**The points.** The 12 rays orthogonal to v are the W(3,3) points collinear with v (Pass 11681: orthogonal = commuting
Paulis). They are exactly the **12 qutrit stabiliser states**.

**The lines.** The 4 isotropic lines through v are the 4 stabiliser bases: pairwise-orthogonal triples.

## 2. Non-collinear points are the maximally magic strange states

**The projection.** The 27 non-collinear rays have |⟨v,w⟩|² = 1/3. Projected onto v⊥, they land **3 : 1 onto 9
states**, one per hyperbolic line through v. Each fibre spans the 2-plane span(v, w).

**The states.** The 9 states are the Clifford orbit of the qutrit strange state (0, 1, −1)/√2.

**Their magic.** Each has stabiliser Rényi magic **M₂ = log 2**. That is the maximum over qutrit states: 40 random
optimisations top out at 0.6931471805.

## 3. The two classes are the two corpus endpoints

**The Yukawa.** Use the common up Yukawa Y_u(h)_{ab} = h_{a+b} g_{a−b}, with g even (Passes 11918–11924). Both classes
were checked over 100 random complex even g.

| Higgs flavour state | W(3,3) direction | magic M₂ | up spectrum | corpus |
|---|---|---|---|---|
| stabiliser | collinear point | 0 | (1, ε, ε): m_c = m_u (to 1.3·10⁻¹⁵) | the lock of Pass 11903 |
| strange | non-collinear point | log 2 (maximal) | (1, 1, 0) exactly: m_u = 0 and m_t = m_c (to 1.1·10⁻¹⁵) | the theta-zero law of Pass 11904 |

**Why (1, 1, 0).** For h = (0, 1, −1) the a + b ≡ 0 class vanishes. The determinant is −ε²g₀ + ε²g₀ = 0, and the
reflection pairs the two nonzero values.

**Consequence.** Both W(3,3) classes sit on the degenerate locus of Pass 11923. Realistic up masses need an intermediate,
reflection-breaking Higgs state, neither pointing at a collinear W(3,3) point nor at a non-collinear one. This is
consistent with the misaligned-flavon mechanism of Pass 11924.

**A real interpolation stays locked.** Along h = cos θ e₀ + sin θ s, with s the strange state, the pair stays locked
(m_u/m_c = 1) on the stabiliser side, because both endpoints are reflection-symmetric. The scratch scan shows this.

## 4. A tested non-result

**The guess.** I expected that F-flat second vevs would have to be collinear with v, forcing aligned (stabiliser)
flavons, so that the lock would survive every F-flat vacuum.

**Why it fails.** Pass 11681's "orthogonal = commuting" refers to **Pauli** commutation. All Cartan (Witting) vevs
commute under the **E8 bracket** (Pass 11893: F-flat = commuting 84s). So F-flatness does not tell collinear directions
from non-collinear ones.

## Reading

**One picture for both earlier laws.** The two "laws" found by explicit computation in Passes 11903 and 11904 — m_c = m_u
in all local-10 models, and "a massless up forces top = charm" — are the two W(3,3) classes:
* the collinear class: zero magic, the stabiliser states;
* the non-collinear class: maximal magic, the strange states.

**Where the up quark lives.** Realistic up-quark masses lie strictly between these two classes of W(3,3) directions.

## Prior art

* The Witting polytope and its 40 rays: Coxeter.
* The Hesse group G₂₅ and the qutrit Clifford group.
* The qutrit strange state and its maximal magic: Veitch–Mousavian–Gottesman–Emerson 2014; stabiliser Rényi entropy
  (Leone–Oliviero–Hamma 2022).
* New here:
  * the W(3,3) projection identity on the flavour qutrit;
  * its identification with the corpus's two charm–up laws.
* Corpus: Passes 11681, 11879, 11893, 11903, 11904, 11923, 11924; parallel packet 34e149d79. The strange state appears
  in the corpus's computing passes (10942) only as a distillation resource.
