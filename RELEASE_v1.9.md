# Release v1.9 — the register cell: two laws, a closed census, two collision mechanisms

**Scope.** Fix a point of the symplectic generalized quadrangle `W(3,q)`, `q`
odd. The `q³` opposite points — the *register cell* — carry the layered
structure surveyed in `papers/register_cell_filtration_survey.tex`. This
release records what four parallel streams (Python witnesses, GAP
certificates, a sandboxed release agent, and Lean formalization) proved and
machine-verified through Pass 481.

## What is proved (theorems)

- **Universal trace laws (P473).** For every odd `q`, every inverse-closed
  section, every nontrivial central character: `tr B_t = 0`,
  `tr B_t² = q(q²−1)`. Each central Weyl block has exactly `q−2` free
  characteristic coefficients — the q=3 flat/curved dichotomy and the q≥5
  near-injective censuses are the two ends of that one count.
- **The determinant congruence law (P479).**
  `det B_t(c) ≡ (q−1)^((q+1)/2)·(−(q+1))^((q−1)/2) (mod λ^(q+3))`,
  `λ = 1−ζ_q`, with depth `q+3` sharp at `q = 3,5,7`.
- **First-order core, proved for all odd primes (P481).**
  `T₁ = tr(adj(F)·D) = det(F)·q·S/(q²−1)` with `S = Σ_v(ζ^(−tc(v))−1)`, giving
  `v_λ(T₁) = (q−1) + v_λ(S) ≥ q+1`. The base valuation decomposes as
  **(q−1) from the ramification of q + 2 from inverse closure** — the latter
  formalized in Lean (`Pass481FirstOrderPairing.lean`:
  `w + w⁻¹ − 2 = −(1−w)(1−w⁻¹)`).
- **The unified law is UNCONDITIONAL off the primes (P485).**
  The last hypothesis is free whenever `f ≥ 2`, since `D = λD'` forces
  `v(det D) ≥ q` and `q ≥ v(q)+4` for every non-prime prime power. Confirmed
  at **q=25** (f=2, exponent 12) and **q=27** (f=3, exponent 10) by a Bareiss
  determinant over `Z[ζ_p]` — six data points across three values of f. At
  prime q the residual is exactly `v(det D) ≥ 2q` (measured 6, 10, 14;
  Newton proves only q+1), equivalent to *every eigenvalue of D having
  λ-valuation ≥ 2*.
- **THE UNIFIED DETERMINANT LAW (P484).**
  `det B_t(c) ≡ det F (mod λ^{v_λ(q)+4})` for every odd **prime power**,
  modulo one identified top-term bound. The constant `4` splits as
  `2` (inverse closure) plus `2` (the e₁/e₂ cancellation); only the
  ramification `v_λ(q) = f(p−1)` varies.
  The cancellation is proved: `Q ≡ 0` because a *symmetric*
  coefficient meets an *antisymmetric* symplectic form (Lean-formalized), and
  `R ≡ −2S` because the inner symplectic sum is `q²ω(v,s) ≡ 0`.
  Measured minima 6,8,10,8 at q=3,5,7,9 match exactly.
  *This retires the earlier "prime phenomenon" framing — q=9 was never a
  counterexample, only the same law at a different ramification.*
- **The determinant congruence, proved (P483).**
  `det B_t(c) ≡ det F (mod λ^(q+1))` for every odd prime and every section —
  via power-sum bounds `v(p_m) ≥ (q−1)+m` from character vanishing off the
  centre, Newton's identities, and a circulant argument in
  `F_q[y]/((y−1)^q)` for the top exterior power. The two steps that valuation
  counting alone cannot reach are **both rescued by inverse closure**.
  At `q = p^f` the same proof gives `v(T₁) ≥ f(p−1)+2`, sharp at q=9.
  The sharp exponent `q+3` now reduces to the single congruence
  `2p₁ ≡ p₂ (mod λ^(q+3))`.
- **Cover law (P394), nesting tower law (P430), no abelian PDS all odd q
  (P433; Polhill et al. Cor. 4.7), the 2-adic pairing law (P433→P434/435),
  prime-power cyclotomic covariance (P459), chain/Galois-ring conductor
  towers (P464/469).**
- **Uniform projective cardinalities in Lean (P477)** — v1.9 gate 1 closed.

## What is machine-verified (certificates)

- **The spectral census is quantitatively closed.** q=5: 396/400 distinct
  (P447); the affine Burnside orbit counts are 2 / 20,592 /
  1,939,395,416,499,131 at q=3/5/7 (P446/479), and a birthday model matches
  the observed collision counts at both q=5 and q=7 (P479).
- **The collision landscape has exactly two mechanisms (P456/463/480/481,
  censused P482).** Genuine cospectral pairs have positive density. Over 6000
  sections, **66 genuine pairs = 34 Wedderburn sheet exchanges + 32 sheet
  coincidences + no third type** — the two mechanisms are the whole landscape
  at this scale, at comparable rates. (A *coincidence* has identical, not
  swapped, sheet data between affine-inequivalent sections.)
- **All orders of the determinant expansion (P482).** Every order term has
  `v_λ(T_k) ≥ q+1`, so `det B ≡ det F (mod λ^(q+1))` for all sections; and
  `v_λ(T_k) ≥ q+3` for `k ≥ 3` with `T₁+T₂ ≡ 0 (mod λ^(q+3))`. The sharp
  depth is base-(q+1) at every order plus exactly one order of T₁/T₂
  cancellation.
- **The determinant law is characteristic-sensitive (P480/481, corrected
  P482).** At q=9 the flat-det formula and flat spectrum extend verbatim, but
  the depth is non-uniform with **minimum 8**, below the prime value 12;
  F₉-collinear sections are the invisible flat class. *(P480/481 reported the
  depth set as {8,10} from 6 and 12 samples — a small-sample artefact; the
  invariant that survives is the minimum.)*
- **Exp-3/exp-9 extraspecial hosts** agree in PDS image, Frobenius–Schur
  indicators (P455), and PDS eigenvalues; the first separator is ramified
  integral-lattice data (P461).

## Open (named, not closed)

1. **v1.9 gate 3, residual core.** The exchanged genuine sheets are similar
   over `Q(ζ₅)`; whether they are `GL₅(Z[ζ₅])`-conjugate is a
   Latimer–MacDuffee ideal-class question in `K = Q(ζ₅)[x]/(f)`,
   `f = x⁵−60x³−35x²+366x+2` (P482). The natural cyclic generators are
   non-unimodular (P480/481); the integral-unitary and monomial/phase-gauge
   cases are closed negatively (P474/479). Needs number-field class-group
   tooling (pari/sage).
2. **The full `q+3` depth proof.** `T₁ ≥ q+1` is proved (P481); the remaining
   `+2` to `q+3` is the `T₁/T₂` cancellation, verified (P480) not proved.
3. **The q=9 depth criterion.** Which section gets which depth is open; two
   hypotheses are dead — "collinear ⇒ depth 8" (P481: collinear sections are
   determinantally invisible instead) and "the F₃-subfield indexes the depth"
   (P482: F₃-valued sections share the generic minimum and spectrum).
4. **A determinant congruence at prime powers** (the `λ^(q+3)` modulus is a
   prime-q statement).
5. **The measured optical run** — gate 5 is software-complete and physically
   blocked (P467/472/478).

## Two no-go boundaries

- **Chirality is unselectable from inside (P346):** `W(E₆)` exchanges the
  half-spin chiralities and acts transitively on every offered multiplicity.
- **The revival no-go (P399, synthesis P431):** no invariant Hamiltonian
  moves population between phase-fiber points — the dynamical twin of the
  static torsor obstruction.

*Ledger:* `w33_paper.tex` claims ledger, 100+ rows, machine-checked against
witness certificates by `scripts/check_claims_ledger.py`. Nothing in this
release is claimed new without a corpus search; attribution corrections are
visible in the ledger history.
