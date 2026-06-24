# BT1707-BT1709 - Qubit Contextuality, Hexagon/Tomotope Bus, and Hesse Crossover

This packet records what the attached multi-qubit contextuality papers add to
the Holonet architecture without overclaiming equivalence.

## BT1707 - the contextuality ladder

The binary Pauli ladder from one through six qubits has a rigid sequence of
contextuality carriers:

```text
1 qubit  W(1,2)        3 points, no line-context KS proof
2 qubits W(3,2)        doily; Mermin square degree 1; doily degree 3
3 qubits W(5,2)        63 unsatisfied lines = split Cayley hexagon
4 qubits W(7,2)        315/DW(5,2) and Heawood/Coxeter separated cores
5 qubits W(9,2)        PG(4,2) point-hyperplane incidence core
6 qubits W(11,2)       K7,7 carrier with Heawood as 21-edge subgraph
```

The new Holonet-facing identity is

```text
|Aut(split Cayley hexagon of order 2)| = 12096 = 168 * 72 = 7 * 1728.
```

So the three-qubit contextuality layer carries exactly the product of the
Fano/Klein readout group (`168`) and the Holonet packet clock (`72`).

## BT1708 - the 48-incidence contextual bus

The Quantum 2025 hexagon paper contains a `(24_2,16_3)` configuration:

```text
24 observables * 2 incidences = 16 lines * 3 observables = 48.
```

That same `48` is already verified twice in the repo:

```text
tomotope middle layer = 12 edge axes / 16 faces = 48 blocks
Holonet body          = 16 Q6 edges * 3 pulse phases = 48 ticks
```

BT1708 therefore promotes the split-Cayley layer as a candidate timed
contextuality/readout module.  The claim is an incidence and symmetry-factor
bridge, not a graph isomorphism.

## BT1709 - binary-to-qutrit crossover

The two-qubit Saniga geometry starts with the projective line over `M2(F2)`,
the order-16 ring with `6` units and `10` zero-divisors.  Its two-qubit Pauli
subgeometry has the familiar `9+6`, `10+5`, and `8+7` decompositions of the
15-point doily.

The Marcelis Fano/cube material gives the missing ternary crossing: after
deleting two hyperovals, the 9 points left form an `AG(2,3)` grid; adding the
line at infinity gives `PG(2,3)` with `13` points.  This lands exactly on the
Holonet ABI:

```text
AG(2,3) = F3 x F3 = 9 = Hesse outcome field = Pauli feed-forward frame.
PG(2,3) = 9 + 4 = 13 = Eisenstein norm prime / projective closure.
```

The next proof target is now precise: construct a context-preserving functor
from the binary Pauli/doily/hexagon ladder to the qutrit Hesse/W33 packet,
rather than merely matching counts.
