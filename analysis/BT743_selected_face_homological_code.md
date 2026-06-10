# BT743 — Homological Code from Selected Levi Faces

Tests whether the BT741 flat global register F2^4 is the logical space of a
homological code: attach selected Levi 8-cycles as 2-faces and compute mod-2
homology (H1 = 81 - rank_F2(face matrix)).

## Results

```text
family                          faces  rank_F2  H1   H2
all 1620 Levi 8-cycles           1620    81      0  1539
mask 1110 bundle (BT741 flat)    1306    81      0  1225
BT718 sheet (1110, ch0)           710    81      0   629
sheets (1110, ch1 / ch2)        673/670   81     0  592/589
mask 1001 bundle                 1318    76      5  1242   <- DEFECT
all other mask bundles          1290-1535 81     0  ...
```

## Theorem 1 (mod-2 1-connectivity)

The 1620 lift octagons span the FULL F2 cycle space of the Levi graph; the
2-complex is mod-2 1-connected (H1 = 0).  Even a single channel sheet
(~670-710 faces) already spans.  Hence no nontrivial homological quantum
code arises from any of the standard selector families — and the BT741
equivariant gluing collapse is consistent with this simple-connectivity.

## Theorem 2 (the BT713 defect is homological and characteristic-free)

The unique exception is the BT713 Hodge-defective mask 1001: its family has
rank 76 over F2, exactly the BT713 rank over the big prime.  The defect is
not a characteristic-0 accident; it is a 5-dimensional hole

```text
H1(mask-1001 complex) = 5 = F_5.
```

The 1001 mask is the A-side split family (center-gauge on the two rectangle
edges through one A-vertex); within the edge-order convention class it is
the only family that fails to fill the cycle space.

## Theorem 3 (the global register is a sheaf, not a homology class)

Since H1 = 0 for the flat bundle, the BT741 global F2^4 register is NOT
mod-2 homology of the face complex.  Its correct home: the flat bundle
defines a LOCAL SYSTEM of F2^4 registers over the chart-gluing graph, and
the global register is its space of global sections H^0 (= F2^4 exactly
because the holonomy is trivial).  Selector theory at the register level is
sheaf cohomology, not surface topology.

## Boundary

Open: whether the 5-dimensional 1001-defect space carries any structure
related to the degree-5 irreducibles of U4(2) (the mask families are
edge-order conventions, so equivariance is not automatic), and the
H^1 of the flat local system (twisted cohomology of the gluing graph).
