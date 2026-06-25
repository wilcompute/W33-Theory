# BT1787 solver materialization note

The relational solver frontier is now exact.

Current committed artifacts provide the variables, table counts, and accepted-count census:

```text
9 variables
12 values per variable
18 ternary tables
9980 accepted local triples total
```

A full global solve still requires the actual accepted tuple lists, not only their counts.

Next executable artifact should materialize 18 tables whose total allowed triples sum to 9980, then run pair consistency and incumbent-first DFS.

Current status: no uniqueness claim yet. The missing artifact is the accepted tuple list data.
