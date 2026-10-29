# Six fronts: half-size native Bloch repair and a disciplined 5:3 / Schläfli audit

**Date:** 28 October 2026. **Scope:** continuation of native gauge/matter results at `9baf04f`, `686188ce`, and the later exact finite-momentum counterexample `52f055d`. Producer: `analysis/w33_20261028_sixfront_ratio_and_12repair.py`; controls: `tests/test_w33_20261028_sixfront_ratio_and_12repair.py`; frozen summary: `data/w33_20261028_sixfront_ratio_and_12repair.json`.

The analysis addresses the previous five independent problems as far as exact structure and finite numerical evidence permit, plus a sixth falsifiability-minded audit of the `120:72=5:3` ratio. **No observed particle spectrum, Einstein gravity, Lorentzian time, full interacting matter determinant, gauge coupling prediction, or TOE is derived.**

## 1. Microscopic action selection: a symmetry obstruction

The pre-existing exact common-cone family is `H(theta)=H0+theta J`. The verified native orientation reflection has `S^T H0 S=H0` and `S^T J S=-J`, so `H(theta)` transforms into `H(-theta)`. Therefore a reflection-invariant quadratic action **within this affine family** must have `theta=0`. The compressed three-channel endpoints `theta=+2,-2` are exchanged, not independently invariant.

A nonzero endpoint may be physically relevant only after explicit reflection breaking, spontaneous endpoint selection, or additional fields and dynamics that transform appropriately. The exact E6 quadratic charge trace alone is insufficient to compute which effective endpoint charged matter selects. **This is a negative selection constraint, not a fermion-loop calculation.**

## 2. Twelve compact cosine harmonics repair the finite-momentum magnetic zero

The later Pass12340 work discovered the exact nongauge flat mode at `z=(omega,omega,1,1)` where `omega^2+omega+1=0`. Its selected short-face/mixed/six-loop/gradient ranks are `105/107/108/27`; this is an **actual counterexample** to extrapolating the three-channel generic rank into an all-momentum gap. Pass12340 added **24** translated loop-difference cosine harmonics to restore equality with the six-loop kernel at all momenta without changing the longwave O(k²) cone.

There is a strictly smaller repair. Let the already-owned three-by-six integral mixed-loop matrix be

```text
R = [1 0 5 -5 1 0
     0 1 -1 0 1 0
     0 0 5 -5 0 1].
```

Select three original commutator channels, indices **2,3,4 (zero-based)**:

```text
S = [0 0 1 0 0 0
     0 0 0 1 0 0
     0 0 0 0 1 0].
```

The six-by-six `[R;S]` matrix has exact determinant **-1**: it is an integral unimodular basis change, not a numerical approximation. Take the three compact Wilson phases `g=S f` and the twelve positive translation-difference terms

```text
Delta V = epsilon sum_(mu=0..3) sum_(a=0..2)
          [1 - cos(g_a(x+e_mu)-g_a(x))], epsilon>0.
```

Their quadratic Bloch symbol is `epsilon w(z) (S L6(z))^dagger(S L6(z))`, with `w(z)=sum_mu |z_mu-1|²`. For every **nonidentity** unitary character, `w>0` and `[R;S]` invertible imply

```text
ker(short, R L6, sqrt(w) S L6) = ker(short, L6).
```

At the identity all six commutator Bloch rows vanish, so equality holds there too. The repair enters at **O(|k|^4)** since each commutator row is O(k) and w=O(k²); it cannot spoil the already-proved O(k²) common acoustic cone.

This cuts the **24** terms of the Pass12340 separable full-six-difference construction to **12**, an exact factor-of-two saving in cosine terms, at the cost of one integral linear recombination. It is **minimal only in this specific separable three-complement-by-four-translation repair architecture**; arbitrary smaller, nonseparable or direction-selective repairs have not been excluded.

On the *actual frozen 135-link, 2-component Q(omega) witness*, all six original commutator norms are `[4112913,4112913,4112913,4112913,4112913,0]`; thus the selected complement norm is `12338739`. At `epsilon=1/1000` and `w=6`, its normalized quadratic witness cost is **49/13000 > 0**, compared with **49/7800** in the 24-term repair. This extra 3/5 factor is a **choice-dependent projection of the witness**, not a new universal physical constant.

## 3. Rigorous *formula* for a compact 3-rotor truncation bound

For the previously verified Gauss-invariant 3-angle flux Hamiltonian,
`H=(g²/2) m^T G_E m + sum w_a(1-cos(q_a.theta))`, the native lifted-loop electric Gram has

```text
G_E = [794 -42 768
       -42 22 -52
       768 -52 766].
```

Exact Sylvester-principal-minor arithmetic proves `G_E-7 I` is **positive definite**; the total positive cosine weight is exactly `7009/28125`. Project onto the electric box `|m_i|<=L`. Call its **true** minimum `E_L`; the complementary block has electric kinetic lower bound `K_out=7g²(L+1)²/2`; and the cross-boundary cosine operator has norm at most `W=sum w_a`. The two-by-two min-max/Schur comparison gives the all-flux lower bound

```text
E_infinity >= (E_L + K_out - sqrt((K_out-E_L)^2+4W^2))/2,
E_infinity <= E_L.
```

Using the **previously computed numerical estimate** at L=5,g=.2, `E_L≈0.2485320384493`, the formula yields the indicative interval `[0.2356053, 0.2485321]`. This is **not an interval-certified numeric bound** until the finite-box eigenvalue itself has a rigorous lower certificate. It is a valid analytic bound formula with an explicitly labeled numerical input and concerns just the three-loop sector, not infinite-volume 4D lattice gauge dynamics.

## 4. Reflection-based 3+1 reduction remains a hypothesis, not observed spacetime

The native deck involution splits the four *spatial* periods into a three-dimensional reflection-even subspace with Gram `[[10,0,-6],[0,12,-6],[-6,-6,12]]` (determinant648) and one orthogonal odd direction of squared norm18. That is an exact lattice-metric decomposition. It does not supply time, a Lorentzian dispersion or two physical photon helicities. Moreover the reflection interchanges the two rank-three magnetic endpoint actions; selecting the even deck without carrying the parity action through the flux dynamics is inconsistent.

## 5. E6 cubic and Abelian response

For the existing `27 -> 10_(1,1)+bar5_(-3,1)+1_(5,1)+5_(-2,-2)+bar5_(2,-2)+1_(0,4)` decomposition, the weighted linear, mixed quadratic and all cubic charge traces vanish, and

```text
Tr_27(Q_a Q_b) = diag(120,72).
```

All45 terms of the canonical E6 cubic are neutral in these two U1 charges. A **shared** matter response kernel implies the conditional trace weighting `120:72=5:3`. The physical response is not shown to be universal across distinct masses or couplings.

More importantly, the numeric ratio of *diagonal entries* is not invariant even under primitive lattice-preserving `GL(2,Z)` redefinitions. E.g. `Q'=Q, R'=Q+R` gives `[[120,120],[120,192]]` and diagonal ratio `120/192=5/8`. The **full quadratic bilinear form** transforms covariantly; its raw diagonal ratio is not a physical observable without a fixed group-embedding normalization and dynamical coupling prescription.

## 6. Where precisely does 5:3 appear in the Schläfli symbols and elsewhere?

**Schläfli is a *combinatorial* specification, not a measured physical parameter**. The 600-cell is `{3,3,5}`: tetrahedral cells, **5** around each edge; the dual 120-cell is `{5,3,3}`: dodecahedral cells, **3** around each edge. Their f-vectors are `(120,720,1200,600)` and `(600,1200,720,120)` (V,E,F,cells). Consequently,

```text
5 * 720 = 3 * 1200 = 3600
E(120-cell)/E(600-cell) = 1200/720 = 5/3.
```

This is a **genuine dual-incidence identity**, not pattern fitting. For the intrinsic 3D polytopal boundaries, 5 regular tetrahedral dihedral angles and 3 regular dodecahedral dihedral angles around respective edges yield positive Regge-style deficits of approximately **7.356°** and **10.305°**. These angles, not the bare ratio 5/3, would enter a candidate discrete curvature action; no gravitational normalization is derived.

A second genuine combinatorial identity is the number of roots: `H4` has `r*h=4*30=120` roots, `E6` has `6*12=72` roots, giving 5/3. **There is no demonstrated canonical embedding of the noncrystallographic H4 root system as a root subsystem of E6**: its Coxeter bond labeled5 requires irrational simple-root inner products unavailable among equal-length E6 roots. This does not rule out nontrivial embeddings after an E8/icosian projection.

Independent other appearances:

- The W33 graph adjacency eigenvalues 12, 2, -4 give gap ratio `(12-2)/(2-(-4))=10/6=5/3`. For the family W(3,q) the ratio is **`(q²+1)/(2q)`**, which equals 5/3 for *integer q* only when q=3. This is an intrinsic W33 spectral ratio, not a Bohr hydrogen energy ratio or proof of geometric quantization.
- Standard **SU(5) hypercharge normalization**: `Tr_5 Y²=3(1/3)²+2(1/2)²=5/6`; relative to the canonical generator trace1/2 this yields `k_Y=5/3` and conventionally `g1²=(5/3)g'²`. That is a **distinct physically used embedding normalization**.
- The Fibonacci ratio `F5/F4=5/3` is an approximation to the golden ratio, **not** the exact golden ratio. H4 has genuine icosahedral/golden-ratio geometry, but `5/3 != (1+sqrt5)/2`.

**Evidence ledger:** all these ratios are exact mathematics, but they have *different invariant meanings* and no proved joint operator intertwiner, natural trace/coupling equality or experimentally constrained common normalization. The 5:3 recurrence therefore remains an **interesting search lead, not a law of nature**.

References: Coxeter group classification https://people.math.osu.edu/davis.12/second_edition.pdf ; 600-cell incidence https://mathworld.wolfram.com/600-Cell.html ; H4 roots https://www.math.ru.nl/~heckman/CoxeterGroups.pdf ; canonical SU5 hypercharge https://frankwilczek.com/2015/maxwellUnification04.pdf . Repo-local prior math: `analysis/PASS12340_CAUSAL_RESPONSE_AND_IDENTIFIABILITY.md`, `exploration/w33_geometric_quantization_bridge.py`, `analysis/2026-10-28_five_fronts_followup.md`.

## Five independent next steps

1. **Full effective-action calculation:** derive the parity-even/odd flux Hessian from an explicit, anomaly-consistent E6 lattice matter regulator and check whether theta0 or a parity-breaking endpoint is selected dynamically.
2. **Minimum finite-momentum repair:** prove whether fewer than12 translated positive compact loops work on the *actual* native Brillouin torus, using exact Laurent ideal/saturation rather than a generic complement argument.
3. **Validated rotor energy interval:** certify the finite-cutoff minimum by interval arithmetic plus a residual/gap estimate and tighten the resulting infinite-flux Schur lower bound; then move to increasing spatial cells.
4. **Physical spacetime reduction:** impose and check a full parity-compatible compactification and electric Gauss law, including possible extra scalar and fermion anomalies, before claiming 3+1 Lorentzian photon dynamics.
5. **Natural 5:3 intertwiner falsifier:** seek a fixed normalization and functorial map from H4/E8 incidence or roots to the E6 two-U1 quadratic form that survives GL(2,Z) basis changes, rather than matching isolated cardinalities.
