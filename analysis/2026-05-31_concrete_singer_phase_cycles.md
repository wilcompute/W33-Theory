# Concrete Singer Phase Cycles

Date: 2026-05-31

This extracts the actual Singer phase structure attached to the concrete Csaszar/Szilassi toroidal system.

Previous theorem:

```text
8 toroidal seven-hexagon systems
    ~=
8 Sylow-7 / Singer choices in GL(3,2)
```

Each toroidal system has collineation stabilizer

```text
7:3
```

of order 21.

This theorem chooses the concrete system from the Csaszar/Szilassi map and extracts the actual Singer `C7` inside its stabilizer.

## Stabilizer

For the concrete toroidal seven-hexagon system, the verifier checks:

```text
stabilizer size = 21
```

with order profile:

```text
1 identity
14 elements of order 3
6 elements of order 7
```

The six order-7 elements generate one unique Sylow-7 subgroup:

```text
C7.
```

So the stabilizer is exactly:

```text
7:3.
```

## Singer generator

The verifier selects a generator of the `C7` Singer subgroup.

It records the generator as a permutation on the 14 Heawood vertices.

Then it checks that this one generator cycles:

```text
all 7 Fano points
all 7 Fano lines
all 7 Szilassi hexagonal faces
```

So the concrete toroidal map is phased by one simultaneous 7-cycle across:

```text
point layer
line layer
hexagon-face layer
```

## 84 flags as 12 Singer phase orbits

The verifier constructs the 84 directed hexagon-edge flags of the chosen toroidal system.

Then it acts by the Singer generator.

Result:

```text
84 flags split into 12 orbits of size 7.
```

So the earlier identity

```text
84 = 7 * 12
```

now has a dynamical phase reading:

```text
84 = 12 local flag phases * 7 Singer steps.
```

This is stronger than the static chart-axis reading.

The local 12 is transported through a global 7-step Singer cycle.

## Normalizer action

The order-3 elements in the stabilizer normalize the Singer `C7`.

The verifier computes their action by conjugation on the Singer generator.

They act by multiplication of the exponent modulo 7:

```text
k -> 2k
k -> 4k
```

So the normalizer is:

```text
C7 ⋊ C3
```

where `C3` acts by the automorphisms

```text
2, 4 in (Z/7Z)^*.
```

This is exactly the expected Singer normalizer structure.

## Interpretation

The toroidal seven-hexagon system is a Singer phase structure on the Fano/Heawood skeleton.

The Singer cycle supplies the seven-step global phase.

The twelve local flags supply the local codec.

Together:

```text
84 = 12 local phases * 7 Singer phase steps.
```

## Relation to previous results

Previously we had several static decompositions:

```text
84 = 7 Fano chart axes * 12 local chart states
84 = 7 Csaszar vertex axes * 12 local vertex flags
84 = 7 Szilassi face axes * 12 local face flags
```

Now we have a dynamic decomposition:

```text
84 = 12 local flag phases * 7 Singer-cycle time steps.
```

The same number is not just an incidence count. It is organized by a cyclic phase structure.

## Compressed theorem

```text
The concrete Csaszar/Szilassi toroidal system has collineation stabilizer 7:3. Its unique Sylow-7 subgroup is a Singer cycle. A Singer generator cycles the seven Fano points, the seven Fano lines, and the seven toroidal hexagons. On the 84 directed hexagon-edge flags, this generator has exactly 12 orbits of length 7. The order-3 normalizer acts on the Singer exponent by multiplication by 2 and 4 mod 7. Thus the toroidal 84-codec is a 12-local-state system transported through a 7-step Singer phase cycle.
```

## Honest boundary

This proves the concrete Singer phase structure. The next hard step is to compare the Singer cycle with the Fano-line addition law and identify whether the 12 local flag phases correspond to edge/direction classes, local Borel 12-codecs, or the tetrahedral directed-edge codec from the affine chart model.
