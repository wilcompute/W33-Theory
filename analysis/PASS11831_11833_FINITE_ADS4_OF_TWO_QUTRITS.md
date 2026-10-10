# Passes 11831–11833 — the finite AdS₄ of two qutrits: measurement contexts are its boundary, Kramers time reversals its bulk, and fixing a time reversal leaves a Lorentz group SL(2,9) with a light cone

Producer: `analysis/w33_pass11831_11833_finite_ads4.py` (exact, all 51 840 elements of Sp(4,3))
Frozen: `data/w33_pass11831_11833_finite_ads4.json`
Regression: `tests/test_w33_pass11831_11833.py`

**Why this direction.** The heterotic orbifold route has now closed twice: Z6-I in 11818, Z6-II in 11826–11830. The
parallel Round 22 §3 proved a sharp no-go: Sp(4,3) is transitive on the 80 nonzero vectors of the Pauli phase space
F₃⁴, so the only Sp-invariant translation graph is K₈₁, and no local four-dimensional lattice can live there. This packet
looks one level up, at the **bivectors** of the phase space. There Sp(4,3) is *not* transitive. Its orbits form a causal
structure, which is the finite form of the classical isomorphism Sp(4) ≅ Spin(5), real form Sp(4,ℝ) ≅ Spin(2,3), the
isometry group of anti-de Sitter space AdS₄.

## 11831 — one quadric for contexts, subsystems and time reversals

Let ω be the symplectic form on V = F₃⁴. For every skew form b with ω-trace zero (a 5-dimensional space), set
J_b = Ω⁻¹B. This is ω-self-adjoint and satisfies the **Clifford relation**

  J_a J_b + J_b J_a = 2β(a,b)·I,  J_b² = Q(b)·I,

checked exactly on all pairs. So V is the 4-dimensional spinor module of the 5-dimensional quadratic space (Λ²₀V, Q). The
121 projective points split into three Sp(4,3)-orbits, each with a physical identification proved point by point:

| class | Q(b) | points | J_b is | physical object | stabiliser |
|---|---|---:|---|---|---:|
| null | 0 | 40 | nilpotent, im = ker a Lagrangian plane | a **measurement context** (stabiliser basis) | 1296 |
| square | 1 | 45 | a symplectic involution, eigenplanes ω-orthogonal and nondegenerate | a **tensor factorisation** C⁹ = C³⊗C³ | 1152 |
| non-square | −1 | 36 | anti-symplectic with J² = −1 | a **Kramers time reversal** (Pass 11210) | 1440 |

**Orthogonality = anticommutation**, and it reproduces four results that the corpus proved separately.

* **Pass 11210.** A Kramers reversal is local in exactly 15 splits, always as a swap. *Explanation:* p is local in split f
  **iff β(p,f) = 0**. Anticommuting J's swap the two eigenplanes, and commuting is impossible because J_pJ_f would be
  scalar. Checked on all 36 × 45 pairs.
* **Pass 11177.** The octet-disjointness graph on the 45 splits is SRG(45,12,3,3), and perfect two-qutrit gates move a
  split to a disjoint one. *Explanation:* two splits are octet-disjoint **iff their involutions anticommute** (all 990
  pairs). Hence **a gate g is perfect iff J_{gF} anticommutes with J_F**.
* **The 27 complete factorisation frames** (Holotrade 5419c27) are exactly the 27 orthonormal 5-frames consisting of
  splits only. Their octets partition the 40 points.
* **Rounds 23/24 (parallel track).** The "share three rays" graph on the 1620 point-apartments has 45 components of 36
  apartments, which Round 24 matched to the protected tritangent supports through an XOR-fibre construction.
  *Explanation:* an apartment is **a factorisation plus a choice of two of the four rays in each factor**. The 45
  components are the 45 factorisations, 36 = C(4,2)². Each component graph is **J(4,2) □ J(4,2)**, the Cartesian square
  of the octahedron. Its spectrum 8¹ 4⁶ 2⁴ 0⁹ (−2)¹² (−4)⁴ is exactly Round 23's.

**Signature becomes parity.** Over F₃ a quadratic form has no signature, only a discriminant. So every orthonormal
5-frame contains an **even** number of Kramers reversals. The frame types are 27 (0+5), 270 (2+3) and 135 (4+1).

## 11832 — the stabiliser of a time reversal is a Lorentz group

The real model is AdS₄ = {X ∈ ℝ^{2,3} : X² = −1}. A point X is in the bulk exactly when its orthogonal complement has
Witt index 1, i.e. its light cone is a sphere with no lines. Its stabiliser is Spin(1,3) = SL(2,ℂ). Spacelike X have
stabiliser Spin(2,2) = SL(2,ℝ)², and the projective null cone is the conformal boundary. The same Witt-index criterion
over F₃ singles out the **36 Kramers reversals**: the perpendicular hyperplane of each meets the null quadric in an
elliptic quadric of 10 points. The perpendicular of each split meets it in a hyperbolic quadric of 16 points. With F₉/F₃
in the role of ℂ/ℝ:

* **Bulk.** The centraliser of a Kramers reversal J₀ has order 720. Its element-order statistics are exactly those of
  **SL(2,9)** (1, 1, 80, 90, 144, 80, 180, 144 for orders 1, 2, 3, 4, 5, 6, 8, 10), and its centre is ±1. The full
  stabiliser is SL(2,9)·2; the extra coset anticommutes with J₀, i.e. it is F₉-antilinear, a parity.
* **Spacelike.** A split has stabiliser of order 1152 = |SL(2,3)|²·2, the analogue of Spin(2,2).
* **Boundary.** A context has stabiliser of order 1296, the parabolic analogue of the conformal-boundary stabiliser.
* **Celestial sphere.** The J₀-invariant 2-planes are exactly **10 Lagrangians = P¹(F₉)**, and they are exactly the 10
  null points orthogonal to J₀. Through J₀, V is an F₉-plane, and these are its F₉-lines. The stabiliser acts on them as a
  group of order 720 with element orders {1, 2, 3, 4, 5, 6}, i.e. **S₆ ≅ PΣL(2,9)**, and the centraliser acts as
  **A₆ ≅ PSL(2,9)**. These are Möbius maps of the celestial sphere, as SL(2,ℂ) acts on ℂP¹, with parity acting as the
  Frobenius ("complex conjugation" of F₉).

**Reading.** Choosing a Kramers time reversal is choosing an observer. Its symmetry is a Lorentz group, its sky is the 10
measurement contexts it preserves, and the phase space of the two qutrits becomes one F₉-spinor (Pass 11210's F₉-form h).

## 11833 — the tangent Minkowski space, its light cone, and the spinor map

Take the 4-dimensional space M = p^⊥ in the bivector space at a Kramers reversal p. Real analogue: T_pAdS₄ = ℝ^{1,3}.

* **Lorentz orbits on M.** Under SL(2,9), and also under the full stabiliser, the 81 vectors fall into
  **1 + 20 + 30 + 30**: the origin, the light cone (null), Kramers-type and split-type vectors. These are four orbits,
  like the origin, light cone, timelike and spacelike orbits of the real Lorentz group. Projectively, the split-type
  directions of M are the 15 splits in which p acts locally (11831). **The spatial directions of an observer are the
  subsystem splits in which its time reversal is local.**
* **Spinor map.** ψ ↦ ψ ∧ J₀ψ, read as an ω-traceless bivector, is **4 : 1 onto the 20 null vectors** and
  SL(2,9)-equivariant (checked on a sample of group elements). The fibres are the norm-one scalars of F₉. This is the
  finite form of p_μ = ψ̄σ_μψ: light rays are spinor squares.
* **The light-cone graph.** On M, join x and y when x − y is a nonzero null vector. The result is **SRG(81, 20, 1, 6)**
  with spectrum 20¹ 2⁶⁰ (−7)²⁰. This is the affine polar graph VO⁻(4,3), i.e. the **Brouwer–Haemers graph**, which is
  unique with these parameters (Brouwer–Haemers 1992). This **answers Round 22 §3**: its K₈₁ no-go needs full
  Sp(4,3)-invariance on the spinor space. Once a time reversal is fixed, the residual Lorentz group is
  translation-compatible with a sparse, nontrivial causal graph on the vector space. That graph is still not a
  Euclidean 4D lattice (diameter 2; no heat-kernel plateau is claimed).
* **Time from two reversals.** For two Kramers reversals p and q, M = J_pJ_q is always symplectic, i.e. a Clifford gate:
  * orthogonal pairs (270): M² = −1, a Fourier-type element (the oscillator's quarter period);
  * non-orthogonal pairs (360): (M − β)² = 0, a **unipotent tick of order 3**; the line pq is tangent to the null cone.

  No pair of reversals is "spacelike separated" (secant line). In W(E₆) language these are products of two reflections,
  in orthogonal roots and in roots at 60°/120° (Pass 11210's 36 reflections; 270 = 36·15/2).

## Prior art, and what is new

* **Classical.**
  * Sp(4,q) ≅ Spin(5,q) through the Klein correspondence, and W(3,q) dual to Q(4,q). The 40/36/45 point classes of
    Q(4,3) are the 40 null points and the two non-singular classes, which in W(E₆) language are the 36 double-sixes and
    the 45 tritangent planes.
  * Ω⁻(4,q) ≅ PSL(2,q²), and PΣL(2,9) ≅ S₆.
  * VO⁻(4,3) = Brouwer–Haemers.
  * The AdS₄ embedding picture.
* **Corpus.**
  * Pass 11210: Kramers class = 36 reflections, θ² = parity, F₉-form, 15 splits.
  * Pass 11192: A = 4 maximal arrow on the 36.
  * Pass 11177: SRG(45,12,3,3) and perfect gates.
  * Holotrade 5419c27/e92a047: factorisations, 27 frames.
  * Pass 11651: the 40 stabiliser bases carry the Q(4,3) form.
  * Pass 11174: a Lorentz group PGL(2,3) acting on 27 events, which is a different object, a one-qutrit Sym² light cone.
  * Rounds 22–24 (parallel track).
  * Rounds 27–28 (parallel track): heat-dimension and graph-wave no-gos for W(3,q) diffusion. These are complementary;
    nothing here is a diffusion or continuum claim.
* **New here.**
  1. One Clifford quadric that holds contexts, splits and Kramers reversals together, with orthogonality = anticommutation.
     It explains 11210's 15-and-swap, 11177's perfect-gate relation, the 27 frames, and Rounds 23/24's sectors with
     their J(4,2)□J(4,2) spectrum.
  2. The Lorentz-type stabiliser SL(2,9)·2 of a time reversal and its celestial sphere P¹(F₉) with S₆ action.
  3. The tangent Minkowski space: orbits 1+20+30+30, spinor map onto the light cone, and the Brouwer–Haemers light-cone
     graph as the answer to Round 22's no-go.
  4. Time from two reversals.

**Why two qutrits.** Sp(2n) is an orthogonal (spin) group only for n ≤ 2. One qutrit gives Sp(2) = SL(2) = Spin(1,2)-type,
and two qutrits give the last accidental isomorphism, Sp(4) = Spin(5), whose split real form is the AdS₄ group. For n ≥ 3
the bivector picture no longer has a spin-group form.

## Scope and boundary

* Every group-theoretic and counting statement is exact over all of Sp(4,3).
* Two statements are by element-order statistics only, not by an explicit isomorphism:
  * centraliser ≅ SL(2,9). Pass 11210's F₉-bilinear form h gives the isomorphism; here we check its statistics.
  * image ≅ S₆.
* "Bulk, boundary, timelike, Lorentz" are names fixed by the Witt-index and stabiliser criteria. They match the real
  Spin(2,3) pattern with F₉/F₃ for ℂ/ℝ. F₃ has no ordering, so time and space are distinguished by square class, not
  by sign.
* **No metric dynamics, no continuum limit, no Einstein equation, no speed of light and no physical scale is derived.**
  What is derived is the *kinematic* skeleton: a Lorentz group, a light cone, spinors whose squares are null vectors,
  and a conformal boundary made of measurements. It comes from two qutrits plus a choice of time reversal.

**Next (open).**
1. The Weil representation C⁹ = 5 ⊕ 4 as the finite Dirac singletons (Rac ⊕ Di). By 11210, T² = +1 on the 5 and −1 on
   the 4. Test a finite Flato–Fronsdal decomposition of 5⊗5̄ and 4⊗4̄ against the permutation modules on the 40, 45
   and 36.
2. Fields on the 36 bulk points as Sp-modules (a "bulk mode spectrum").
3. The analogous structure for the E₈ two-qutrit Cartan of Pass 11681.
