# Heawood Eight Systems as Singer / Sylow-7 Choices

Date: 2026-05-31

This identifies the group-theoretic meaning of the eight toroidal face systems on the Heawood skeleton.

Previous correction:

```text
8 = 168 / 21 = 336 / 42.
```

The eight systems form one orbit under the collineation group

```text
GL(3,2) ≅ PSL(2,7)
```

with stabilizer of order 21.

This theorem identifies that stabilizer and the eight systems precisely.

## Singer cycles

In `GL(3,2)`, an element of order 7 is a Singer cycle: it acts transitively on the seven nonzero vectors of `F2^3`, i.e. on the seven Fano points.

A Singer cycle generates a Sylow-7 subgroup.

The verifier checks the element-order profile of `GL(3,2)`:

```text
1 identity
21 elements of order 2
56 elements of order 3
42 elements of order 4
48 elements of order 7
```

The 48 order-7 elements form exactly eight Sylow-7 subgroups:

```text
48 / 6 = 8.
```

This also matches Sylow theory:

```text
n_7 ≡ 1 mod 7
n_7 | 24
n_7 = 8.
```

## Singer normalizer

For each Sylow-7 subgroup, the verifier computes its normalizer inside `GL(3,2)`.

Each normalizer has order:

```text
21.
```

with structure:

```text
7:3.
```

This is the Singer normalizer.

## Toroidal systems

The verifier then takes the eight toroidal seven-hexagon face systems on the Heawood graph and computes the collineation stabilizer of each one.

For every system, it checks:

```text
stabilizer size = 21
stabilizer order profile = {1 identity, 14 elements of order 3, 6 elements of order 7}
```

So each system stabilizer is a `7:3` Frobenius/Singer normalizer.

Then it proves:

```text
stabilizer of system = normalizer of one Sylow-7 subgroup.
```

## Equivariant bijection

The verifier associates to every toroidal face system its unique Sylow-7 subgroup.

It checks:

```text
8 systems
8 Sylow-7 subgroups
bijection between them
```

and also checks equivariance:

```text
transporting a face system by g ∈ GL(3,2)
transports its Sylow-7 subgroup by conjugation.
```

So the eight toroidal systems are not just count-equivalent to the Sylow-7 subgroups. They are naturally the same `GL(3,2)`-torsor.

## Correct interpretation of the 8

The clean interpretation is:

```text
8 = number of Singer/Sylow-7 choices in GL(3,2).
```

Equivalently:

```text
8 = number of Singer normalizers 7:3 in GL(3,2).
```

Choosing one toroidal seven-hexagon system is equivalent to choosing one Singer phase structure on the Fano/Heawood skeleton.

Adding Heawood dualities extends the stabilizer:

```text
7:3 -> 7:6
```

and doubles the stabilizer order:

```text
21 -> 42.
```

## Why this matters

This is stronger than the earlier affine-cube guess.

The eight systems are not primarily the natural eight vectors of `F2^3`. They are the eight Sylow-7/Singer choices of `GL(3,2)`.

That means the toroidal face system is a cyclic phase structure:

```text
one 7-cycle on the Fano points,
plus its 7:3 normalizer.
```

This fits the Csaszar/Szilassi automorphism group:

```text
7:6
```

because the map remembers a Singer 7-cycle and the extra duality/reflection side of its normalizer.

## Compressed theorem

```text
The eight toroidal seven-hexagon systems on the Heawood graph are equivariantly bijective with the eight Sylow-7 subgroups of GL(3,2). Each system has collineation stabilizer equal to the Singer normalizer 7:3 of its corresponding Sylow-7 subgroup. Thus 8=168/21 is the Singer/Sylow-7 choice count. Adding Heawood dualities extends 7:3 to the full toroidal map stabilizer 7:6 of order 42.
```

## Honest boundary

This proves the Singer/Sylow interpretation of the eight systems. The next hard step is to extract the actual Singer 7-cycle associated with the concrete Csaszar/Szilassi map and compare it with the vertex rotation cycles, Fano line cycles, and the earlier `7*12=84` codec axes.
