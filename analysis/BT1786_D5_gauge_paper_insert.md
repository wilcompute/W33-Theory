# BT1786 D5 gauge paper/codebase insert

This supersedes the earlier phase-only wording for the Coxeter bus action.

## Correct statement

The BT1774 inversion witness acts on the 40 Coxeter hexagons by a cyclewise reflection. In the original BT1750/BT1777 labels, this is not a single global phase law across all eight Coxeter 5-cycles.

After independently rephasing the eight Coxeter 5-cycles by

```text
[2,0,3,1,3,0,3,4]
```

the inversion becomes the uniform law

```text
q -> -q mod 5
```

on every cycle. Together with the Coxeter rotation

```text
q -> q+1 mod 5
```

this gives a gauge-correct D5-equivariant five-bus structure.

## Paper-ready phrasing

The five E8/Witting bus phases form a D5-equivariant object after a harmless independent phase choice on each of the eight Coxeter 5-cycles. In this gauge, the Coxeter rotation acts by `q -> q+1`, while the explicit BT1774 inversion witness acts by `q -> -q`. Without this gauge choice, the inversion is still valid but appears as eight cyclewise reflections with different phase origins.

## Guardrail

Do not claim that the original BT1750 labels already realize a global `q -> -q` law. The global D5 law is true only after the BT1783 rephasing gauge is chosen.
