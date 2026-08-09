# Part DCCLIV — Octahedral Commute/Hitting-Time Bridge

## Why this part exists

DCCLIII gave exact effective resistances and Dirichlet energy on octahedral closure phase space. The next natural step is to derive exact random-walk timing laws from that same geometry.

## Exact commute-time law

For an undirected graph with `m` edges and effective resistance `R_ij`,

```text
C_ij = H_ij + H_ji = 2m R_ij.
```

On the octahedron, `m = 12`. Using DCCLIII values:

- adjacent resistance `R_adj = 5/12` gives

  ```text
  C_adj = 24 * (5/12) = 10,
  ```

- antipodal resistance `R_opp = 1/2` gives

  ```text
  C_opp = 24 * (1/2) = 12.
  ```

The verifier checks this identity for all pairs exactly.

## Exact hitting-time values

By direct Markov linear solves (`P = A/4`), the verifier proves one-way orbit values:

```text
H_adj = 5,
H_opp = 6.
```

So commute times split symmetrically by orbit:

```text
C_adj = 5 + 5,
C_opp = 6 + 6.
```

## Spectral walk invariant

From the transition spectrum, the verifier also recovers Kemeny's constant:

```text
K = 13/3.
```

So the same octahedral phase space now has a closed random-walk invariant layer.

## Meaning

The closure chain now unifies:

- resistance geometry,
- Dirichlet energy,
- and random-walk timing.

This is the cleanest exact transport-time bridge on octahedral closure phase space so far.

## Exact vs conditional

- **Exact:** commute times satisfy `C_ij = 2mR_ij` with orbit values `C_adj=10`, `C_opp=12`, and hitting-time values `H_adj=5`, `H_opp=6`.
- **Conditional:** continuum transport-time interpretation still requires a scaling limit.

## Executable artifact

- Verifier: `verify_dccliv_octahedral_commute_hitting_time_bridge.py`
- Tests: `tests/test_dccliv_octahedral_commute_hitting_time_bridge.py`
- Data: `data/dccliv_octahedral_commute_hitting_time_bridge.json`
