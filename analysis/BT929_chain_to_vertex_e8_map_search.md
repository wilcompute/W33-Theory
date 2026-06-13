# BT929 — Chain-to-vertex \(E_8\) map search

BT929 maps the BT925 chain symplectic form into the BT926 vertex \(E_8\) witness.

## Result

There is an explicit mod-2 isometry

```text
M^T G_vertex M = B_chain mod 2.
```

The found \(0/1\) matrix \(M\) has integer determinant \(1\). Therefore its integral lift inside the vertex \(E_8\) lattice is unimodular.

## Lifted Gram

The lifted Gram

```text
M^T G_vertex M
```

has:

- determinant 1;
- even diagonal;
- positive-definite spectrum;
- minimum eigenvalue `0.026512767609722727`.

So the lift is an even unimodular positive-definite rank-8 lattice, hence \(E_8\).

## Honest boundary

This is a major map witness but not yet a canonical chain lift. The isometry is constructed from chosen symplectic bases, so it is basis-dependent. It proves that the chain shadow can be identified with the vertex \(E_8\) modulo 2 and lifted unimodularly in the vertex lattice; it does not yet derive a unique canonical selector from the chain complex.

## Witness

```text
analysis/bt929_chain_to_vertex_e8_map_search.py
data/bt929_chain_to_vertex_e8_map_search.json
```
