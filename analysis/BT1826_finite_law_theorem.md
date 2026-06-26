# BT1826 finite law theorem

## Assumptions

A1. The local fibre is

```text
Z3 x (Z2)^2
```

so each local fibre has 12 symbols.

A2. Hesse table labels are `T_i,j,s`, with `(i,j,s)` in `Z3^3`, restricted to the 18 nonconcurrent tables.

A3. The quartet is the K4 on four glue states:

```text
00, 01, 10, 11
```

A4. The Schlaefli transport is the BT1795 18-line image, and the stabilizer action is the BT1812 action.

A5. The syndrome constraint is the BT1801 F3 left-kernel constraint.

## Lemmas

### Lemma 1: Hesse hinge reduction

Among the 816 possible three-table supports, exactly 54 are Hesse hinges. The observed support `{T010,T210,T222}` is one of them.

### Lemma 2: Schlaefli slice reduction

Under the Schlaefli image stabilizer, the Hesse hinge class breaks into 10 slices. The observed support lies in a six-hinge slice.

Since

```text
6 = C(4,2)
```

the slice is naturally the edge set of a hidden K4 quartet.

### Lemma 3: quartet identification

The hidden K4 is identified with the D4 glue quartet:

```text
D4*/D4 = (Z2)^2
```

The observed support is the quartet edge `00--11` in the chosen old/new gauge.

### Lemma 4: unique F3-valid orientation

Among the 54 Hesse hinges and 3 possible return tables per hinge, the unique orientation repairing the BT1801 F3 syndrome is:

```text
T010,T210 -> T222
```

Equivalently:

```text
old + old -> new
00--11 oriented edge transfer
```

### Lemma 5: BC-ring closure

Under the BC-ring projection

```text
T_i,j,s -> (phase = 3j+s, strand = i)
```

the correction is

```text
(phase 3, strand 0) -> (phase 8, strand 2) -> (phase 3, strand 0)
```

It is a period-2 antipodal involution inside the ambient 30-cell BC/Coxeter clock. BT1825 shows this involution is central for the D5 bus action.

## Theorem

The finite fibre law is:

```text
12 = 3 x 4
3 = Hesse/BC strand coordinate
4 = D4/GKP/tetrahedral K4 quartet
unique correction = old+old -> new oriented K4 edge
observed section = twisted 9980
repaired section = untwisted F3-flat 9978
closure = D5-central antipodal involution inside the 30-cell BC/Coxeter clock
```

The same correction is selected from four equivalent faces:

```text
Hesse:        canonical hinge T010,T210 -> T222
Schlaefli:    six-hinge stabilizer slice containing supports 10,22,44
D4/GKP:       oriented K4 edge 00--11
BC/600-cell:  tetrahedral face-pair F0--F3, phase 3 <-> 8, strand 0 <-> 2
```

## Open physical derivation

The finite combinatorial theorem is closed. The remaining open layer is physical/operator realization: identify the BT1824 commuting finite operators

```text
P = strand mismatch projector
G = D4 glue parity
E = K4 edge energy
C = cyclic residue
```

as measured Hamiltonian or syndrome terms in the photonic hardware model.
