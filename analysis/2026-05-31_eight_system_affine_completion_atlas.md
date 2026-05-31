# Eight-System Affine Completion Atlas

Date: 2026-05-31

This continues the Singer hexagon affine-completion result across all eight toroidal seven-hexagon systems on the Heawood skeleton.

Previous theorem:

```text
For one concrete Singer/toroidal system, every hexagon canonically completes to AG(2,2) by x=p+q+r.
```

The open question was:

```text
What happens to those affine completions across all eight Singer/Sylow toroidal systems?
```

## Main construction

For each of the eight toroidal systems, and for each of its seven Heawood hexagons:

1. Extract the three Fano point vertices of the hexagon.
2. Call them `p,q,r`.
3. Define the fourth affine point:

```text
x = p + q + r.
```

4. Record the affine completion:

```text
{p,q,r,x}.
```

So every system produces a seven-chart affine completion atlas.

## What the verifier checks

The verifier checks:

```text
8 toroidal systems
7 completion records per system
completion point defined for every hexagon
each completion has 4 affine points
each system has 7 completion points
each system is labeled by one unique Sylow-7/Singer subgroup
```

It also checks equivariance under the collineation group:

```text
atlas(g · system) = g · atlas(system)
```

at the signature level.

So the affine completion atlas is compatible with the `GL(3,2)` action.

## Why this matters

The previous Singer/Sylow result said:

```text
8 toroidal systems = 8 Sylow-7 / Singer choices.
```

Now each such Singer choice carries a seven-chart affine atlas.

So the hierarchy becomes:

```text
Singer/Sylow choice:
    one of 8 toroidal systems

Toroidal system:
    seven Heawood hexagons

Each hexagon:
    canonical AG(2,2) completion by x=p+q+r
```

## Honest classification boundary

This verifier intentionally does not assume that the eight affine atlases are all distinct or all identical as unlabeled signatures.

Instead, it records:

```text
number of unique atlas signatures
signature records
which systems share which signature
point membership distributions
```

in:

```text
data/w33_eight_system_affine_completion_atlas.json
```

That data should be inspected next to classify whether the eight Singer systems share one completion-atlas type or split into multiple types.

## Correct statement

What is proved structurally is:

```text
Every one of the eight Singer/Sylow toroidal systems has a canonical seven-chart affine completion atlas, and GL(3,2) transports these atlases equivariantly.
```

What remains data-dependent is:

```text
how many distinct unlabeled atlas signatures occur among the eight systems.
```

## Compressed theorem

```text
Across the eight toroidal seven-hexagon systems on the Heawood graph, each hexagon canonically determines an AG(2,2) completion by taking its three Fano point vertices p,q,r and adding x=p+q+r. Thus each toroidal system carries a seven-chart affine completion atlas. These atlases are equivariant under GL(3,2), and each system remains labeled by its unique Sylow-7/Singer subgroup. The verifier records the exact signature classification without assuming whether the eight atlases are all identical or split into multiple types.
```

## Honest boundary

The next hard step is to inspect the generated JSON classification and identify the unique atlas signatures explicitly. If there is one signature, the affine completion atlas is universal over Singer choices; if there are multiple, their split should reveal an additional invariant of the Singer/Sylow phase system.
