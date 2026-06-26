# BT1816 hinge orientation solver

Executed the 54-hinge orientation test against the committed BT1801 F3 left-kernel basis.

The basis-consistent count syndrome is:

```text
[0,2,1,1,2]
```

Therefore the repair vector must evaluate to:

```text
[0,1,2,2,1]
```

Search space:

```text
54 directed Hesse hinges
3 choices of return table per hinge
162 oriented candidates
```

Result:

```text
unique repairing candidate:
T010, T210, T222
return table: T222
source/removal tables: T010, T210
support indices: 10,22,44
```

So the observed repair is not merely one convenient member of the 54-hinge class. It is the unique directed hinge orientation that repairs the BT1801 F3 syndrome while preserving the parity layer.

Computational guardrail: this uses the committed BT1801 F3 left-kernel basis. That basis gives the actual count syndrome `[0,2,1,1,2]`; earlier prose summaries that wrote `[0,2,1,1,1]` are superseded for this solver.
