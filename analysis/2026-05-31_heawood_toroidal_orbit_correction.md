# Heawood Toroidal Orbit Correction

Date: 2026-05-31

This corrects and sharpens the interpretation of the eight toroidal face systems on the Heawood skeleton.

The previous theorem correctly found:

```text
8 toroidal seven-hexagon systems
```

in the orbit of the concrete Szilassi system under the full Heawood automorphism group.

However, the suggested split

```text
4 collineation systems + 4 duality systems
```

was suspicious.  The reason is structural:

```text
GL(3,2) ≅ PSL(2,7)
```

has order 168 and is simple, so it cannot have a nontrivial index-4 action/stabilizer in the way that interpretation implied.

This verifier recomputes the orbit with collineations and dualities separated.

## Correct result

The full Heawood automorphism group splits as:

```text
168 collineations
168 dualities / polarities
336 total automorphisms
```

The eight toroidal systems satisfy:

```text
systems reached by collineations = 8
systems reached by dualities = 8
systems reached by full group = 8
```

and, crucially,

```text
collineation orbit = duality orbit = full orbit.
```

So the duality coset does not produce a separate second half of four systems.

The collineation subgroup is already transitive on all eight systems.

## Stabilizers

For a fixed toroidal seven-hexagon system, the verifier checks:

```text
collineation stabilizer size = 21
duality stabilizer size = 21
full stabilizer size = 42
```

So:

```text
8 = 168 / 21 = 336 / 42.
```

The collineation stabilizer has order profile:

```text
1 identity
14 elements of order 3
6 elements of order 7
```

This is the expected Frobenius-type

```text
7:3
```

stabilizer.

Adding the duality side doubles it to the full toroidal map stabilizer:

```text
7:6
```

of order 42.

## Corrected interpretation

The correct picture is:

```text
8 toroidal face systems = one GL(3,2) collineation orbit.
```

Dualities do not create another disjoint orbit.  Instead, they double the stabilizer of each system:

```text
21 -> 42.
```

So the factor 8 is:

```text
8 = GL(3,2) / (7:3)
```

and also:

```text
8 = Aut(Heawood) / (7:6).
```

## Why this matters

This correction is important because it respects the internal group theory.

The eight systems should now be interpreted as a single orbit under Fano collineations, not as four collineation choices plus four polarity choices.

This makes the next target cleaner:

```text
classify the eight systems as an F2^3 / affine-cube torsor, or as the eight cosets of the Singer normalizer 7:3 inside GL(3,2).
```

## Compressed theorem

```text
The eight toroidal seven-hexagon systems on the Heawood graph form one orbit under the 168-element collineation group GL(3,2). The stabilizer of one system inside GL(3,2) has order 21 and structure 7:3. The full 336-element Heawood automorphism group has stabilizer 42, structure 7:6, with 21 collineations and 21 dualities. Thus 8=168/21=336/42. The earlier 4+4 collineation/duality split is incorrect; dualities reach the same eight systems and double the stabilizer instead.
```

## Honest boundary

This proves the corrected orbit/stabilizer structure. The next hard step is to identify the eight systems explicitly with the eight elements of `F2^3`, or equivalently with cosets of a Singer-normalizer subgroup `7:3` in `GL(3,2)`.
