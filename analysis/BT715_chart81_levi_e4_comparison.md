# BT715 — Chart-81 / Levi-

BT715 executes the second BT713 next step: compare the selected chart-side \(81\)-sector with the Levi \(E_4\) Hodge sector.

## Inputs

From the corrected BT700/BT706 chart overlap calculation:

```text
H H^T = 9I + A_Gamma
A_Gamma eigenvalue -1 has multiplicity 81
therefore H H^T eigenvalue 8 has multiplicity 81
```

So the chart \(81\)-sector is not a nullspace. It is the positive-energy eigenspace

```text
E_chart = Eig_8(HH^T), dimension 81.
```

From BT545--BT551, the Levi flag side has:

```text
Levi graph vertices = 80
Levi flag edges = 160
beta_1 = 160 - 80 + 1 = 81
E4 = CC^T / 160
rank(E4) = 81
```

From BT714, the selected hinge sheet has:

```text
rank(S_hinge) = 81
rank(D_Levi) = 79
D_Levi S_hinge^T = 0
rank(D_Levi) + rank(S_hinge) = 160
```

## Comparison theorem

The selected hinge rows are boundaryless, so their rowspace lies inside the Levi cycle space. Since both spaces have dimension \(81\), equality follows:

```text
rowspace(S_hinge) = ker(D_Levi) = im(E4).
```

The chart-side selected rows have rank \(81\) as well, so the induced comparison has full rank on the chart \(81\)-sector:

```text
rank(E_chart -> E4) = 81.
```

Equivalently, the BT714 selector realizes the desired bridge:

```text
chart 81-sector  --->  Levi E4/H1 sector
       8^81                 160^81 projector sector
```

## Result

BT715 turns the BT708 completion criterion into a finite-rank certificate:

```text
rank(Z_chart^T S_hinge) = 81
D_Levi S_hinge^T = 0
image(S_hinge on chart81) = Levi E4
```

Boundary: this proves sector equality for the rank-complete hinge representative from BT714. It does not prove uniqueness of the tomotope/Fano hinge selector among the 19 full-rank sheets identified in BT713.
