# Three mixed native magnetic channels: exact Maxwell-cone compression

**Independent continuation, 28 October 2026.** This packet builds directly on
`analysis/2026-10-27_native_gauge_propagation_completion.md` and
`analysis/2026-10-27_five_front_followthrough.md`. Its result is an
**exact mathematical construction on the supplied native periodic voltage
cover**, not a derived physical photon, Lorentzian spacetime, quantum gravity,
or microscopic selection principle. All GitHub code and certificate sources
are credited; no mathematical-priority claim is made for Hodge duality.

## Exact rank versus physical ellipticity

The connected native cover has 27 sites, 135 links, and a 105-row
zero-period face basis. At generic Bloch momentum the gradient rank is 27,
so completing all magnetic directions requires 108 independent curl rows.
The existing packet appended all six 16-step based commutators and verified
rank 108.

Independently enumerating the 64 subsets of these six loops modulo 101
shows that **three** are the minimum number of extra rows for generic rank:
16 of 20 triples attain rank 108; the other four attain rank 107. Every pair
reaches rank 107 and every singleton rank 106. The census reproduces at
moduli 103 and 107 with independent specialization values.

This does **not** make any three individual loops physically equivalent
to six. At leading order, each individual commutator represents one
coordinate 2-form `(Wn)_a (Wx)_b-(Wn)_b (Wx)_a`. A three-edge subset of the
six possible pairs on four directions has at least one vertex of incidence
degree at most one. Choosing momentum in that coordinate direction leaves
at most one nonzero independent curl row, rather than the three transverse
polarizations required by an elliptic four-spatial-dimensional Maxwell
symbol. Thus generic completion and all-direction ellipticity are distinct
constraints.

## Three **integer-mixed** flux channels recover the native common cone

Existing results classify all six-by-six symmetric flux couplings with the
specified common-cone symbol as `H(theta)=H0+theta J`; the four-form
direction J is invisible on decomposable 2-forms. Strict positivity holds
for -2<theta<2.

At either endpoint theta=+/-2, the coupling becomes **positive
semidefinite of rank three**. In particular the minus endpoint has an
integer/rational exact factorization

```text
H(-2) = R^T K R,
R = [ 1  0  5 -5  1  0
      0  1 -1  0  1  0
      0  0  5 -5  0  1 ],

K = [ 25/9  -5/3 -26/9
      -5/3  11/3      2
     -26/9     2   28/9 ].
```

The three leading principal minors of K are 25/9, 200/27, 16/27:
**K is positive definite**. Every entry and every equality is rational;
no floating eigenvalue fitting is used.

Let M be the native integral harmonic Gram matrix and W the primitive
unimodular four-period basis from the prior packet. Define the
six-by-four four-variable curl symbol

```text
C_(ab),i(n) = (Wn)_a W_(b,i) - (Wn)_b W_(a,i).
```

Exact SymPy expansion in all four independent components of n gives

```text
C(n)^T R^T K R C(n)
       = ((n^T M n) M - (M n)(M n)^T)/27.
```

This is the **same complete four-variable common-cone identity** as the
six-loop engineered metric, with only three linearly independent
gauge-invariant magnetic combinations `g=R f`, where f lists the six
literal commutator fluxes. No preferred momentum ray is chosen.

At three separate prime/Laurent specializations (101, 103, 107), the 105
native face rows together with the three mixed rows have **exact rank
108**, and `F D=0` exactly. A nonzero modular minor establishes a nonzero
Laurent polynomial over the integers, so generic rank 108 also holds over
the real Bloch torus outside a proper exceptional locus.

The construction is **minimal in magnetic channel count** for generic
completion because 108-105=3, and it preserves the full leading-order
native cone. It does **not** claim minimal total loop length, nearest-link
hardware complexity, finite-momentum degeneracy, nor a unique action.

## A compact positive potential with exactly nine harmonics

The three mixed angles g each are integer combinations of six genuine
based-loop Wilson phases. Thus every integer q.g is gauge invariant
and has a well-defined compact U(1) cosine.

Define

```text
V(g) = 1/10000 sum_(i=1)^3 (1 - cos g_i)
          + sum_(a=1)^6 w_a (1-cos(q_a . g))
```

with **strictly positive rational weights** and integer q vectors:

| q_a | weight w_a |
|---|---|
| (3,-4,-4) | 49937/630000 |
| (3,-4,-3) | 21313/378000 |
| (3,4,-3) | 49241/1350000 |
| (4,-4,-3) | 1241/90000 |
| (4,-3,-4) | 142189/3150000 |
| (4,4,-3) | 1/56 |

The exact rational identity

```text
K = I/10000 + sum_(a=1)^6 w_a q_a q_a^T
```

certifies the Hessian. Positive unit harmonics ensure V>=0 and
V=0 exactly when `g=0 modulo 2pi`. The Hessian in the six original
flux coordinates is `R^T K R=H(-2)`.

This is a **concrete compact, local-in-the-native-loop-sense** completion
with three independent angle channels and nine cosine terms. Individual
high-charge Wilson harmonics can entail longer traversals; their presence
is a supplied engineering choice. The six-flux Hessian is singular and
the three orthogonal combinations not seen by R are flat at quadratic
order and in this supplied potential. That is an actual physical-model
limitation, not hidden by matching one dispersion relation.

## Relationship to parallel October 27 work

The already-owned six-commutator, strict-positive H0 action and the
one-parameter theta classification are prerequisites. The new statement
is **endpoint rank-three compression plus its integer factorization,
Bloch-rank certification, and an explicit positive compact potential**.

Later October 27 packets construct interacting compact rotor patches,
native matter currents, overlap operators and an acoustic determinant
response. They do **not** establish a microscopic principle selecting
this rank-three endpoint; nothing here invalidates their common-cone,
thermal or no-global-bandgap caveats. This packet is a new candidate
to compare against them, not a replacement of those control results.

## Verification

```bash
python analysis/w33_20261028_three_mixed_loop_minimal_maxwell.py \
  data/w33_20261028_three_mixed_loop_minimal_maxwell.json
python -m pytest -q tests/test_w33_20261028_three_mixed_loop_minimal_maxwell.py
```

The symbolic factorization, all-four-variable identity and positive
rational cosine decomposition were independently computed before
publication. The mod-101, mod-103, mod-107 generic Bloch ranks were
independently recomputed against committed literal voltage/face rows.
The complete repository test run is separate and must not be claimed
successful until CI or a local runner reports it.

## Five independent next problems

1. **Microscopic action selection:** derive a preference for theta=-2
   (or rule it out) from charged native matter, reflection/orientation
   symmetry and radiative corrections, rather than tuning the flux metric.
2. **Finite-k dispersion:** compare the three-mixed and six-loop models
   over all four momentum directions, locating exceptional loci and
   determining whether extra flat/soft bands survive on the infinite cover.
3. **Compact rotor phase:** quantize the nine-harmonic three-angle theory
   on increasing native patches with controlled flux truncations, Gauss
   constraints and Wilson-loop correlations.
4. **Physical dimension reduction:** test a justified 4-spatial-to-3-spatial
   reduction, anomaly-compatible boundaries, and what happens to the extra
   scalar polarization under the reduced gauge constraints.
5. **Couple to the canonical E6 cubic:** connect this gauge sector to
   the actual 27-matter regulator and compute both electric and magnetic
   response from the same interacting theory; require a common cone
   and physically measurable predictions, not coincidence matching.
