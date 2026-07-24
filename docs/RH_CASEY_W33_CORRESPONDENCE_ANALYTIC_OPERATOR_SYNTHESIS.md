# Casey / W(3,3) RH Program: Correspondence, Conditional Defect, Fixed-E, Automorphic Packet, and Compact Resolvent

## Executive result

All five registered frontiers were executed. The release advances the program in two directions while closing three over-optimistic routes.

1. The `1+24+15` W33 decomposition now produces an explicit rank-78 projector-level correspondence
   \[
   (\mathbb Q^2\otimes V_2)\oplus(\mathbb Q^2\otimes V_{-4}),
   \]
   of ranks `48+30`. This exactly matches the rank of the elliptic packet
   \(H^1(E_2)^{24}\oplus H^1(E_{-4})^{15}\).
2. Casey's completed boundary defect has an exact positive contribution from every critical-line conjugate pair, conditional on RH and justified Hadamard summation.
3. That positivity is not a converse: an explicit off-line quartet can also give a positive second difference.
4. The fixed function `E_11=Xi+i Xi'/log(11)` is an RH-level Hermite--Biehler target, not merely an auxiliary numerical test.
5. The degree-78 elliptic packet is an honest automorphic L-packet, but it cannot collapse to the degree-one Riemann zeta function without an additional functorial theorem.
6. A Lambert-W Weyl ladder repairs the compact-resolvent and zero-density defects of the inverse-log operator, but it is only an asymptotic scaffold.

No proof of classical RH is claimed.

## 1. Exact projector-level correspondence

The script reconstructs `W(3,3)` directly from the symplectic form on the 40 projective points of `F_3^4`. Its adjacency matrix satisfies

\[
A^2=8I-2A+4J
\]

and has spectrum

\[
12^1,\qquad 2^{24},\qquad(-4)^{15}.
\]

The primitive projectors are checked to be idempotent, orthogonal, and of ranks `1,24,15`. Tensoring the nonconstant packets with the two-dimensional cohomology of an elliptic curve gives

\[
\operatorname{rank}(\mathbb Q^2\otimes V_2)=48,
\qquad
\operatorname{rank}(\mathbb Q^2\otimes V_{-4})=30.
\]

Both projectors become integral after multiplication by `120`, so the correspondence has an explicit denominator-cleared lattice model.

This closes the correspondence at the W33 projector level. It does **not** construct a map from the concurrent Pass-637 rank-78 conductor module: that module currently has no certified compatible W33 action. Equal rank alone is not a correspondence.

## 2. Conditional analytic completed-defect theorem

For one critical-line conjugate pair, write

\[
x=\frac12,\qquad h=2\delta,
\]

and let `gamma` be the zero ordinate. The pair contribution to the second difference of `H=-xi'/xi` is

\[
\boxed{
\frac{4h^2x(3\gamma^2+h^2-x^2)}
{(\gamma^2+x^2)(\gamma^2+(x-h)^2)(\gamma^2+(x+h)^2)}.
}
\]

For `0<|delta|<1/2` and every actual nontrivial zero ordinate, all factors are positive. Therefore, conditional on RH and on a justified symmetric Hadamard summation, every zero pair contributes positively to Casey's completed defect.

This explains the positive numerical boundary scan from the preceding release.

It is not a converse. A synthetic quartet with

\[
\beta=0.7,\qquad\gamma=14
\]

also produces positive second differences at all registered defects. Consequently

> positivity of this single completed second-difference functional is necessary under RH but is not sufficient for RH.

A stronger family of test functions or a matrix-valued positivity criterion is required.

## 3. Fixed-`E_11` logical status

Let

\[
\Xi(z)=\xi\!\left(\frac12+iz\right),
\qquad
E_{11}(z)=\Xi(z)+\frac{i}{\log 11}\Xi'(z).
\]

For a real entire function `F`, global Hermite--Biehler status of `F+i cF'` forces the real part `F` to have only real zeros. Thus a global proof that `E_11` is Hermite--Biehler would be an RH-level result for `Xi`; it is not merely a convenient sufficient condition unrelated to the zero problem.

The executable replay remains positive on its registered points and is consistent with the earlier 1010-point audit. Neither computation is interval arithmetic, and neither controls the unbounded upper half-plane.

## 4. Automorphic packet identification

For

\[
E_2:y^2=x^3+x-1,
\qquad
E_{-4}:y^2=x^3+x+2,
\]

define

\[
M_W=H^1(E_2)^{\oplus24}\oplus H^1(E_{-4})^{\oplus15}.
\]

Because elliptic curves over `Q` are modular, the formal packet

\[
L(M_W,s)=L(E_2,s)^{24}L(E_{-4},s)^{15}
\]

is an honest degree-78 automorphic L-packet. The two curves have distinct bad-reduction support,

```text
E_2    : {2,31}
E_-4   : {2,7},
```

and are not isogenous, as witnessed by their different traces at `p=5`.

A replay through `p<=500` again finds the W33 signature `(2,-4)` only at `p=11`, with normalized trace correlation approximately `-0.03445`.

The obstruction is categorical: this degree-78 packet cannot equal the degree-one Riemann zeta L-function. Any transfer must be a new functorial, trace-formula, or determinant construction rather than a direct equality of Euler products.

## 5. Compact-resolvent replacement

The rejected inverse-log prime model had ordinates tending to zero. A structurally compatible replacement begins with the leading Riemann--von Mangoldt inverse

\[
\boxed{
t_n=\frac{2\pi(n-7/8)}{W((n-7/8)/e)}.
}
\]

This sequence tends to infinity, has a finite counting function, and lies in the required `T log T` Weyl class. Against the first 20 Riemann ordinates its mean absolute relative error is approximately

```text
4.883%.
```

This is only an asymptotic scaffold. It does not reproduce individual zeros or a determinant equal to `xi`.

There is also a decisive multiplicity constraint. Repeating every level with all `24+15=39` W33 nonconstant states multiplies the zero density by 39. Therefore W33 must appear as a bounded internal fiber, interaction, or transfer matrix—not as 39 independent copies of every spectral ordinate.

## Validation

```text
python analysis/w33_rh_correspondence_analytic_operator.py
PYTHONPATH=. pytest -q tests/test_rh_correspondence_analytic_operator.py
5 passed in 0.39s
```

Certificate:

```text
data/w33_rh_correspondence_analytic_operator_certificate.json
```

## Combined frontier

The combined architecture is now sharply constrained:

- the W33 `24+15` packets are exact and can be lifted to rank `48+30` cohomological sectors;
- Casey's completed defect has a clean positive pair kernel under RH, but that scalar positivity is not equivalent to RH;
- the fixed de Branges candidate is a legitimate RH-level target;
- the elliptic packet is globally automorphic but cannot be identified directly with zeta;
- any viable Hilbert--Polya operator must have compact resolvent, `T log T` counting, and W33 as an internal rather than multiplicity-replicating degree of freedom.
