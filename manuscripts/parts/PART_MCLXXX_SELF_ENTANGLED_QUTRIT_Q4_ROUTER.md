# Part MCLXXX: Self-Entangled Qutrit Q4 Hypercube Router Law

## Claim Boundary

MCLXXX is a finite graph/network routing theorem. It connects the
self-entangled qutrit "now" context to the 4x4 toroidal knight graph and the
4-cube `Q4`. It does not replace the ternary W33 payload with a binary model.
The payload remains the `F3^4` two-qutrit Pauli geometry; `Q4` is a finite
binary router/clock around one four-ray now-context.

## External Alignment

John J. Watkins' *Across the Board* treats knight tours, graph theory, Gray
codes, Hamiltonian cycles, and toroidal chessboards as chessboard graph
problems. Public graph references record the key special case used here:

```text
the 4x4 toroidal knight graph is the four-dimensional hypercube graph Q4.
```

Network-theory language says the same thing differently: `Q4` has vertices
labeled by four-bit strings, and edges join strings that differ in one bit.

The executable verifier below proves this exact finite instance offline.

## Self-Entangled Qutrit Input

MCLXIII models the user's "past/future, computation is now" idea by the qutrit
Bell/Choi state

```text
|Omega> = (|00> + |11> + |22>) / sqrt(3).
```

Its now stabilizer projectivizes to a W33 line of size

```text
q + 1 = 4.
```

That four-ray Bell line is the present context. Squaring the context gives the
4x4 board:

```text
B x B, where |B| = 4.
```

So the 4x4 toroidal board is not the 3x3 history lattice. It is the square of
the four-ray now-context extracted from the self-entangled qutrit.

## Hypercube Router

On the toroidal 4x4 board, the knight has four distinct moves because `+2` and
`-2` coincide modulo `4`. The graph has:

```text
16 vertices,
degree 4,
32 edges.
```

The explicit labeling in the verifier sends its vertices to four-bit strings
so that every knight edge becomes a one-bit flip. Hence the graph is exactly

```text
Q4.
```

The hypercube network packet is:

```text
vertices          = 16,
degree            = 4,
edges             = 32,
diameter          = 4,
parity split      = 8 + 8,
spectrum          = {4^1, 2^4, 0^6, (-2)^4, (-4)^1},
square faces      = 24.
```

Each bit dimension contributes exactly eight edges:

```text
8 + 8 + 8 + 8 = 32.
```

That eight-edge dimension cut matches the self-entangled qutrit fact that the
now contraction erases the eight nonidentity single-qutrit Paulis.

## Knight Tour = Gray Clock

The closed 4x4 toroidal knight tour becomes a Gray-code Hamilton cycle on
`Q4`. The bit-flip sequence is

```text
1,2,1,3,1,2,1,0, 1,2,1,3,1,2,1,0.
```

Thus the knight tour is not only a chess tour. It is a native hypercube routing
clock: it visits every one of the sixteen context-pair slots exactly once while
changing only one control bit at a time.

## Bridge Reading

The resulting ternary/binary split is:

```text
payload = self-entangled qutrit / F3^4 W33 Pauli geometry,
router  = binary Q4 hypercube network on the 4x4 toroidal now-context square.
```

The key finite identity is:

```text
4 now rays -> 4 Q4 dimensions,
8 erased Pauli directions -> 8 edges per dimension.
```

So the 4x4 toroidal knight/hypercube packet is the binary control network
around a ternary self-entangled qutrit context.

## Sources

- Watkins, *Across the Board: The Mathematics of Chessboard Problems*.
- Public knight graph references: the toroidal 4x4 knight graph is `Q4`.
- NetworkX hypercube graph documentation: `Q_n` vertices are bit strings and
  edges flip exactly one bit.

## Artifacts

- Analysis: `analysis/w33_self_entangled_qutrit_q4_router.py`
- Tests: `tests/test_w33_self_entangled_qutrit_q4_router.py`
- Result: `PART_MCLXXX_SELF_ENTANGLED_QUTRIT_Q4_ROUTER_results.json`
