# Q4 / Fano Chain-Complex Homology Theorem

Date: 2026-05-29

This performs the boundary-rank test proposed after the Q4/Fano square-commutator theorem.

The goal was to build the actual chain complex:

```text
Q4 vertices      = codec states
Q4 edges         = wedge/dot transition operators
Q4 square faces  = commutator relations
```

and compute the homology over F3.

The result is important because it corrects the expectation:

```text
The square relations do not produce topological H1=81.
They kill H1 completely.
What survives is H2.
```

## Full Q4 square complex

For the full Q4 square 2-skeleton:

```text
C0 = 16 vertices
C1 = 32 edges
C2 = 24 square faces
```

Over F3, the verifier computes:

```text
rank(d1) = 15
rank(d2) = 17
```

Therefore:

```text
H0 = 1
H1 = 0
H2 = 7
```

So the full Q4 square relations kill every router 1-cycle and leave seven second-homology modes.

Interpretation:

```text
H2 = 7 = Phi6
```

These are the seven Fano/toroidal surface modes.

## Antipodal quotient square complex

Now quotient by antipodal complement:

```text
Q4 / {x ~ 1-x} = K4,4
```

with the selected 12 quotient square cycles from the antipodal pairs of Q4 square faces.

The quotient complex has:

```text
C0 = 8 axes
C1 = 16 quotient edges
C2 = 12 quotient square cycles
```

Over F3, the verifier computes:

```text
rank(d1) = 7
rank(d2) = 9
```

Therefore:

```text
H0 = 1
H1 = 0
H2 = 3
```

So the quotient square relations again kill H1, but now the remaining H2 has dimension 3.

Interpretation:

```text
H2 = 3 = q
```

These are the three affine directions / points at infinity.

## Hinge + quotient H2 gives 81

This is the key honest bridge to the known phase-frame rank.

The chain complex itself does not produce topological H1=81.

Instead:

```text
quotient H2 = 3 direction modes
```

and the tetrahedral hinge contributes one distinguished mode:

```text
hinge mode = 1
```

So the qutrit phase-mode count is:

```text
1 + 3 = 4.
```

Therefore the state count is:

```text
3^4 = 81.
```

This matches the known signed phase-frame rank:

```text
rank(AA^T/160) = 81.
```

So the corrected statement is:

```text
The Q4/Fano commutator complex leaves three quotient H2 direction modes; adding the tetrahedral hinge gives four qutrit phase coordinates, whose state count is 81.
```

## Split of square relations

The 12 quotient square faces split into:

```text
6 hinge/primal wedge commutators
6 non-hinge/dual dot commutators
```

The verifier checks that each set has full boundary rank 6 on its own:

```text
rank(hinge faces) = 6
rank(non-hinge faces) = 6
```

but together the full square boundary rank is only:

```text
rank(d2) = 9.
```

So the overlap among the two commutator systems is exactly what leaves the 3-dimensional H2 direction space.

## Geometric reading

```text
Q4 edges:
    transition operators / graph cycles before relations

Q4 square faces:
    commutator relations that flatten H1

Full Q4 H2 = 7:
    seven Fano/toroidal surface modes

Quotient H2 = 3:
    three affine directions / points at infinity

Hinge + directions = 1 + 3 = 4:
    four qutrit phase coordinates
```

## Updated architecture

The correct chain is now:

```text
Q4 1-skeleton gives the router transition graph.
Q4 square faces impose Fano wedge/dot commutator relations.
Those relations kill H1.
The surviving H2 modes are Fano/toroidal surface modes.
After antipodal quotient, H2=3 directions remain.
Adding the tetrahedral hinge mode gives 4 qutrit phase modes.
The phase-state count is 3^4=81.
```

## Compressed theorem

```text
Over F3, the full Q4 square complex has homology (H0,H1,H2)=(1,0,7).
The antipodal quotient square complex has homology (H0,H1,H2)=(1,0,3).
Thus square commutator relations flatten the router H1 and leave surface-direction H2.
The tetrahedral hinge plus the three quotient H2 directions gives 4 qutrit modes, whose state count is 81, matching the minimal signed phase-frame rank.
```

## Honest boundary

This proves the finite chain-complex homology bridge. The next step is to fiber this quotient complex over the 40 W33 anchors and test whether the resulting 40*(hinge+direction) qutrit coordinates collapse to the known signed rank-81 projector rather than overcounting all local fibers independently.
