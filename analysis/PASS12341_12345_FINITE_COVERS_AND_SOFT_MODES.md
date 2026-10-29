# Finite-cover torsion census and nonzero-momentum soft modes

This is an addendum to `PASS12341_12345_GLOBAL_BLOCH_AND_PHYSICAL_CONTROLS.md`.
The input is the same native 27-vertex cover, selected short faces and three
mixed loops. It is a statement about the supplied magnetic quadratic form,
not a derivation of relativistic dynamics or a complete theory of physics.

## Exact finite covers

The prior all-momentum result identifies a nonidentity physical magnetic
zero precisely when `Q(h-1)=0`, with `h=z^W` and unimodular integer W.
On an n-periodic cover, W bijects the four-tuples of n-th roots of unity.
For **every n from 2 through 64**, an exact census finds:

| Period n | Nonidentity zero characters | Real kernel dimension modulo gauge |
|---|---:|---:|
| 3 divides n | 10 | 14 |
| 3 does not divide n | 0 | 4 |

The four identity-character modes are the global holonomies. Each listed
nonidentity character contributes one complex zero; conjugate characters
pair under the reality condition, so the real dimension equals the number
of nonidentity characters. The six-loop model and both positive repairs
have only the four holonomies for **every** n, by the prior global theorem.

For all multiples of 3, including those above 64, the ten known order-three
characters embed in the n-periodic grid. Hence the unrepaired kernel has
dimension **at least 14** on every such cover. We have not excluded additional
characters on covers above 64, and do not assert the above table for all n.

### Exact enumeration method

For each n the producer takes a prime `p = 1 (mod n)` and a primitive
n-th root `u` in the finite field. It screens **all n^4 tuples** against
`2Q(u^e-1) = 0 (mod p)`, using signed 64-bit arithmetic with an explicit
overflow bound. Every actual n-th-root zero survives: evaluation at u is a
ring homomorphism from `Z[x]/Phi_n`. Every survivor is then tested over the
integers by reduction modulo the cyclotomic polynomial `Phi_n`. Thus the
field screen cannot exclude a genuine zero and its false positives are not
accepted. At n=31 it admits one extra false positive, which exact reduction
rejects. Independent Gaussian- and Eisenstein-integer enumerations check the
period-four and period-six outputs, and earlier tests calculate all 81 actual
period-three Bloch-matrix ranks.

Eriko Hironaka, [Torsion Points on an Algebraic Subset of an Affine Torus](https://arxiv.org/abs/alg-geom/9607014),
describes Laurent's theorem and the resulting polynomial-periodic count of
n-torsion points on an algebraic torus variety. It applies to this explicit
Q-variety, but its general existence result does **not** prove that the
observed period-three table persists: finding the actual torsion cosets or
a sufficient explicit period bound remains open here.

## Soft modes on all sufficiently large covers

The lack of an **exact** zero on a particular grid does not remove the
finite-momentum problem. Let `A(k)` be the unweighted stack of the actual
selected short-face and mixed-loop symbols, and let `D(k)` be the vertex
gradient. Choose the exact normalized transverse null vector `v` from
Pass12340 at `k*=(2pi/3,2pi/3,0,0)`. For every n, choose `m` nearest to
`n/3` and set `k_n=(2pi m/n,2pi m/n,0,0)`. These grid momenta converge to
the nonidentity k*, with `|k_n-k*| <= 4/n`.

Since all rows are closed lifted loops, `A(k)D(k)=0`. The finite-range
symbols are Lipschitz. At k*, the connected graph and the four-step period
path give an explicit positive lower bound on the smallest singular value
of D. Projecting v onto the transverse subspace at k_n therefore changes it
by O(1/n), while its curl is O(1/n). Its Rayleigh quotient supplies a
magnetic eigenvalue upper bound of O(1/n^2) **at a momentum converging to
the fixed nonzero k***. This is separate from ordinary acoustic softening
near zero momentum.

The producer computes conservative, completely explicit constants directly
from the literal graph and paths:

* `||D(k)-D(k*)|| <= sqrt(342) |k-k*|`;
* `||A(k)-A(k*)|| <= sqrt(25818) |k-k*|`;
* `sigma_min(D(k*)) >= 1/sqrt(1692)`.

Consequently, for every `n >= 12172`, the lowest transverse eigenvalue at
the chosen k_n obeys

```
lambda_min(A(k_n)^* A(k_n)) <= 1652352 / n^2.
```

To obtain the third bound, a period-four path based at vertex 0 has
holonomy omega and bounds the root component of a vertex field by
`4 ||Df||/sqrt(3)`. A simple quotient-graph path to any vertex has at most
26 edges. Thus `||f||^2 <= (18*4^2+1404)||Df||^2`. For n at least the
given threshold, the gradient perturbation is at most one quarter of
that singular-value lower bound; the projected v has norm at least 1/2.
The stated quotient bound follows. The constants are deliberately crude;
they establish the asymptotic statement rather than a tight physical scale.

For a numerical control, the very same projected witness gives Rayleigh
quotients `0.0496826` at n=31 and `0.00490880` at n=100; multiplying by
n^2 gives `47.745` and `49.088`. Independent diagonalization verifies
that the actual lowest transverse eigenvalue is below each bound. These
two numerical evaluations are not substitutes for the all-large-n proof.

**Reproducibility:** `analysis/w33_pass12341_12345_torsion_census.py`,
`data/w33_pass12341_12345_torsion_census.json`, and
`tests/test_w33_pass12341_12345_torsion_census.py`. The source hash, every
field-screen prime and every enumerated zero label are recorded in the data.
