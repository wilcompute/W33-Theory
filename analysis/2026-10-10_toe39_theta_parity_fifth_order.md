# TOE39 — theta-null parity blocks and a fifth-order remainder

**Date:** 2026-10-10. **Status:** analytic identity plus independently reproduced numerical certificate.
**Prior ownership:** Pass 11872 establishes the 1:epsilon:epsilon² singular hierarchy; TOE Round38 gives its cubic determinant coefficient. This pass only strengthens their parity/selection rule and next-error order.

## Exact argument

Use the two-qutrit level-3 theta-null coefficient matrix
```
Theta[a,b](epsilon) = sum_{n,m in Z} exp(3*pi*i*(
    tau1*(n+a/3)^2 + 2*epsilon*(n+a/3)*(m+b/3)
    + tau2*(m+b/3)^2))
```
for a,b = 0,1,2 modulo 3, with Im Omega positive definite. Define P by P(0)=0 and P(1)=2, P(2)=1. Change n to -n with a replaced by -a, and independently m to -m: these are exact reindexings of absolutely convergent series. They yield
```
P Theta(epsilon) = Theta(-epsilon) = Theta(epsilon) P,
P Theta(epsilon) P = Theta(epsilon).
```
Thus Theta commutes with simultaneous parity, and is block diagonal in the qutrit parity basis e0, (e1+e2)/sqrt(2), (e1-e2)/sqrt(2), with even block 2x2 and odd block 1x1. As det P=-1,
```
det Theta(-epsilon) = -det Theta(epsilon).
```
The even block is an analytic even function of epsilon, the odd scalar an analytic odd function. At epsilon=0 the even block is rank one, and the odd scalar vanishes. The rank-one moment expansion already yields
```
C = (6*pi*i)^3/2 * det[u0,u1,u2] * det[v0,v1,v2],
u_r(a) = sum_n (n+a/3)^r exp(3*pi*i*tau1*(n+a/3)^2),
v_r(b) = sum_m (m+b/3)^r exp(3*pi*i*tau2*(m+b/3)^2).
```
Analyticity, oddness and vanishing of the lower-order determinant coefficients therefore imply the strengthened remainder
```
det Theta(epsilon) = C epsilon^3 + O(epsilon^5)
```
(not merely O(epsilon^4)). The identity persists for every positive-definite Im Omega, without tuning tau1 or tau2. If C vanishes at a special modulus, the cubic leading term disappears and the next possible nonzero order is odd and at least five.

## Independent reproducibility

```
py -3 analysis/w33_20261010_toe39_theta_parity_fifth_order.py
```
Three independent genus-two period pairs are tested. The certificate checks row and column parity, parity-adapted block diagonality, determinant oddness, rank-one splitting at epsilon=0, and quartering of leading-term relative error when epsilon is halved.

## Physical boundary and external cross-check

This is a selection rule in a chosen **marked** level-three theta basis, not a modular-invariant fermion mass law. TOE Round38 already demonstrated that a Siegel modular shear acts as an entangling CZ and changes Schmidt entropy in a fixed two-qutrit splitting. A physical flavor fit requires separately specified sector markings, couplings and a modulus potential. In the classical genus-two literature, separating-degeneration expansions of even/odd theta constants exhibit related parity constraints, but those conventional half-characteristics are not this level-three two-qutrit theorem. See Cléry–Faber–van der Geer, *Covariants of binary sextics and vector-valued Siegel modular forms of genus two* and Freitag–Salvati Manni, *The Burkhardt group and modular forms*.

## Independent next experimental test

Calculate an invariant, chart-independent scalar built from the **full Clifford orbit** of Theta, then couple it to a local positive modulus potential; test for an isolated CP-breaking minimum rather than assuming one from stationary symmetry points.
