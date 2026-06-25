# BT1776 match note

Checked the BT1773 ring against the BT1767 completion graph.

Result: the 30-object count matches, but a bare ring has 30 adjacency links while the BT1767 completion graph has 60 links:

```text
BT1767 completion graph: 30 vertices, 60 links, degree 4
BT1773 ring spine:       30 vertices, 30 links, degree 2
```

So the BT1773 ring is a correct cyclic backbone candidate, but not the full three-strand completion graph.  The next test is to search 30-facet induced subgraphs in the 600-cell dual with 60 links and degree 4, then compare them to the BT1767 three-strand/cross-section graph.
