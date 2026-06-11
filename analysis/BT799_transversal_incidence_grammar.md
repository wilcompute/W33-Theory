# BT799 - Four-Transversal Incidence Grammar

BT798 proved that the residual `16+16+8+8` packet is the four common
transversal lines of the base skew-pair chart.

BT799 reads the nearby rank-32 packets by how their two target lines meet those
four transversals.

## Symbols

For each transversal:

```text
00 = neither target line meets it
10 = first target line meets it
01 = second target line meets it
11 = both target lines meet it
```

## Grammar

The key packets have exact signatures:

```text
R11 handle octet:       one 11 + three 00
R12 live edge:          four 10
R13 shadow edge:        four 00
R24/R26 connectors:     one 10 + one 01 + two 00
R09/R10 face sheets:    anchored side sees all four; other side selects one
```

So `R11` is not just "the remaining octet."  It is the packet that chooses one
common transversal and bridges both target lines through it.

## Interpretation

The local bridge now has a clean grammar:

```text
transversal tetrad  -> residual tetrahedral carrier
one 11              -> handle/cell transfer
four 10             -> live edge anchor
four 00             -> shadow edge
split 10/01         -> face connector
```

This is the exact incidence language behind the cube diagonal kill and the
tomotope face-phase lift.

## Validation

Run:

```bash
python3 analysis/bt799_transversal_incidence_grammar.py
```
