# Invariant-Tangent / Phase-Torque Riemann Audit

## Verdict

The three reviewed presentations are **not a valid proof of the classical Riemann Hypothesis in their current form**. Their strongest legitimate content is a geometric heuristic built around reflection symmetry and compactification. The exact W33 result remains the finite **Ihara graph-RH theorem** for the `SRG(40,12,2,4)` collinearity graph.

This audit preserves that exact graph theorem while isolating the gaps in the proposed classical transfer.

## What is exact

1. `W(3,3)` has adjacency spectrum `12^1, 2^24, (-4)^15`.
2. The correct Ihara determinant is

   ```text
   Z_W(u)^(-1) = (1-u^2)^200 (1-u)(1-11u)
                 (1-2u+11u^2)^24 (1+4u+11u^2)^15.
   ```

3. Since `|2|, |-4| < 2 sqrt(11)`, the graph is Ramanujan.
4. Therefore every nontrivial Ihara pole lies on `|u|=1/sqrt(11)`.
5. Under the correct substitution `u = 11^(-s)`, that circle maps to `Re(s)=1/2`.

The existing `manuscripts/tex/part27_graph_rh_theorem.tex` uses `u=(sqrt(11))^(-s)` while still claiming `Re(s)=1/2`. That normalization maps the circle to `Re(s)=1`; the base must be `11` to obtain `1/2`.

## Fatal issues in the topological proof

### 1. The "invariant tangent metric" is not a metric

The relation

```text
tan(theta) = Im(z)/Re(z) = tan(phi/2)
```

is an angular-coordinate assertion, not a positive-definite Riemannian metric. In standard stereographic coordinates the polar angle is controlled by `|z|`, while `arg(z)` is the azimuthal angle. No manifold, chart atlas, metric tensor, or invariant boundary functional is actually defined.

### 2. Compactification does not impose zero phase torque

Stereographic compactification sends a divergent value to the north pole of the Riemann sphere. That is a coordinate completion, not a theorem that

```text
lim_(sigma->1) d/dsigma arg(xi(sigma+it)) = 0.
```

The stationary boundary condition is assumed, not derived.

### 3. Phase is undefined at a zero

`Phi(s)=Im log xi(s)=arg xi(s)` is multivalued away from zeros and undefined at `xi(s)=0`. A zero can be treated through winding number, the argument principle, or a punctured neighborhood, but not as a regular point of a continuous phase field.

### 4. The local pair algebra does not support the stated cancellation

For the natural same-height symmetric pair

```text
rho_+ = 1/2 + delta + i t0,
rho_- = 1/2 - delta + i t0,
```

the logarithmic phase contribution is

```text
d/dsigma arg[(s-rho_+)(s-rho_-)]
 = -(t-t0)/((sigma-1/2-delta)^2+(t-t0)^2)
   -(t-t0)/((sigma-1/2+delta)^2+(t-t0)^2).
```

At `delta=0` these terms **add**. They are generically nonzero at `sigma=1`. Thus the slide-deck boundary condition fails even for a critical-line pair under the natural product-phase convention.

A difference of the two terms vanishes at `delta=0`, but that inserts an extra relative minus sign and is not the derivative of the argument of the zero-pair product. It would require an independent derivation.

### 5. A local pair cannot be isolated from the completed product

Even a valid nonzero local contribution would not prove a contradiction. The completed zeta logarithmic derivative includes all nontrivial zeros, trivial zeros, gamma terms, and normalization factors. The proof gives no positivity theorem, no sign-definiteness, and no result excluding global cancellation.

### 6. Reflection symmetry does not force the critical line

For any `delta>0` and `t0>0`, define

```text
F_delta,t0(s)
 = (((s-1/2)-delta)^2+t0^2)
   (((s-1/2)+delta)^2+t0^2).
```

Then

```text
F(1-s)=F(s),
F(conj(s))=conj(F(s)),
```

but the zeros are

```text
1/2 +/- delta +/- i t0,
```

all off the critical line. This exact counterexample proves that reflection/conjugation symmetry, compactification, and paired-zero geometry are insufficient by themselves.

### 7. The Hilbert-Polya map in the repo is tautological

`analysis/w33_riemann_spectral_determinant.py` maps each positive eigenvalue to

```text
rho = 1/2 + i sqrt(lambda-1/4).
```

That puts the image on `Re(rho)=1/2` by definition. A Hilbert-Polya construction requires a proof that a self-adjoint operator has spectral determinant equal to the completed zeta function, with its eigenvalues matching every zeta-zero ordinate. The current finite `9x9` Laplacian does not establish that transfer.

## Repo-level claim classification

| Surface | Status |
|---|---|
| W33 SRG spectrum | exact |
| W33 Ramanujan property | exact |
| W33 Ihara graph-RH | exact |
| `u=11^{-s}` critical-line normalization | exact correction |
| Riemann zeta special-value denominator matches | exact arithmetic identities, non-probative |
| W33/GUE numerical analogies | heuristic |
| Deligne/Weil implication from shared `11` | unsupported |
| `q! = 2q` implying graph-RH | unsupported |
| invariant-tangent boundary condition | undefined/assumed |
| local phase-torque contradiction | algebraically invalid as written |
| classical RH conclusion | not proved |

## Productive salvage route

The useful research direction is not to defend the current Q.E.D. step. It is to replace the metaphorical boundary with a mathematically defined global object:

1. Specify a Hilbert space and self-adjoint operator.
2. Prove an exact determinant or trace formula equal to completed `xi(s)`.
3. Define the phase functional on a punctured domain or through the argument principle.
4. Derive, rather than assume, a coercive or positive boundary identity.
5. Prove the W33 Ihara object enters through an explicit transfer functor, limit, or automorphic correspondence.

Until those steps exist, the correct public claim is: **W33 proves its finite graph-RH analogue and supplies candidate structures for a classical transfer problem; it does not prove the classical Riemann Hypothesis.**
