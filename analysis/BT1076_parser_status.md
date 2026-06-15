# BT1076 — Parser status

BT1076 inspects the existing BT876 artifacts.

## Existing data

The current JSON records only summaries:

```text
C40 grades: 22, 9, 9
fixed plane size: 13
module profile: 1 + 3 + 8
```

It does not include the actual index sets.

## Existing script

The script builds the point list, group action, selected symmetry, fixed points, neighbours, shell, and centralizer. It verifies the grade counts using the permutation matrix of the selected symmetry.

The script writes only summary fields to JSON.

## Parser conclusion

The real rank-22 block is not extractable from the current JSON alone. It should be extractable by patching the script to export the internal permutation and orbit data.

## Needed exports

```text
selected permutation
fixed point indices
neighbour indices
shell indices
orbit cycles on the shell
three grade blocks
```

## Boundary

This is an inspection note. The old script has not yet been patched.
