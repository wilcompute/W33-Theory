# Part MCLXI: Lovasz-Hoffman Extremal Certificate

## Claim Boundary

MCLXI is a finite W33 graph-extremality certificate. It packages the accepted
Lovasz theta, Hoffman, Delsarte, clique, and fractional-coloring equalities
into the MCL ledger style. It is not a continuum theorem.

## Statement

For W(3,3), with SRG parameters

```text
v = 40, k = 12, r = 2, s = -4,
```

the Hoffman/Delsarte independence bound is

```text
alpha <= -v*s/(k-s) = -40*(-4)/(12+4) = 10.
```

The project ledger treats this bound as tight:

```text
alpha(G) = 10 = v/4.
```

The Lovasz theta value is the same number:

```text
theta(G) = -v*s/(k-s) = 10.
```

For the complement graph, the parameters are

```text
Gbar = SRG(40, 27, 18, 18),
eigenvalues 27, 3, -3,
```

and

```text
theta(Gbar) = -40*(-3)/(27+3) = 4.
```

Thus the Lovasz product is exactly tight:

```text
theta(G) * theta(Gbar) = 10 * 4 = 40 = v.
```

## Clique And Coloring Shell

The GQ lines give 4-cliques, and the Hoffman clique expression gives

```text
omega(G) = 1 + k/|s| = 1 + 12/4 = 4.
```

The chromatic and fractional chromatic values are pinned to the same shell:

```text
chi(G) = chi_f(G) = 4.
```

So MCLXI records the finite extremal packet

```text
alpha = theta(G) = 10,
omega = theta(Gbar) = chi = chi_f = 4,
alpha * omega = v.
```

## Artifacts

- Analysis: `analysis/w33_lovasz_hoffman.py`
- Tests: `tests/test_w33_lovasz_hoffman.py`
- Result: `PART_MCLXI_LOVASZ_HOFFMAN_results.json`
