# BT1057 — Full 162-slot table

BT1057 materializes the complete indexed 162-slot carrier ledger as CSV data.

## File

```text
data/bt1057_full_162_slot_table.csv
```

## Columns

```text
i,c,g,f,w,k,Y0
```

where

```text
i = row index, 0..161
c = chirality in {L,R}
g = generation in {0,1,2}
f = fiber in {0,1,2}
w = weakslot in {S,D1,D2}
k = color in {0,1,2}
Y0 = trace-corrected U1 slot value
```

## Count checks

```text
rows excluding header = 162
Y0=2/3 count          = 54
Y0=-1/3 count         = 108
```

## Boundary

This is the full slot table for the BT1038/BT1053 carrier. It is not yet the final physical particle table.
