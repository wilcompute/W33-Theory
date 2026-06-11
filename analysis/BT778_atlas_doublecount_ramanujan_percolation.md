# BT778 — Atlas Double-Counts, the Two 2160-Spaces, the Ramanujan Defect,
#          and Web Percolation

Four creative tests on the BT777 hypercube atlas, all exact except the
Monte Carlo.

## T1/T2: the atlas double-count theorems

```text
every W33 NONEDGE is a hypercube-chart edge in exactly 12 = k charts
   (540 nonedges x 12 = 6480 = 540 charts x 12 edges)
every W33 EDGE is an antipode pair in exactly 9 = q^2 charts
   (240 edges x 9 = 2160 antipode slots)
```

The valency k and the square q^2 are the atlas multiplicities of the two
pair types.  Every hyperbolic relation of the substrate is a routing edge
in twelve hypercube charts; every collinear relation is a self/antipode
channel in nine.

## T2b: the two 2160-spaces are NOT isomorphic (discovery via refutation)

Antipode slots number 2160 = the centered rectangles, and both G-sets are
transitive with order-12 stabilizers — but the stabilizers differ:

```text
rectangles:      Stab = Z12   (cyclic - the BT746 clock)
antipode slots:  Stab = D6    (dihedral order 12: orders {1,2x7,3x2,6x2})
```

PSp(4,3) carries two distinct homogeneous 2160-spaces of the same size,
one clock-like (cyclic, chiral) and one mirror-like (dihedral).  The
rectangle/antipode coincidence of cardinality conceals a cyclic/dihedral
dichotomy — the same chirality theme (BT745-BT772) at the G-set level.

## T3: the Ramanujan defect is exactly the g_neg sector (prediction hit)

The 6-regular cube web has Ramanujan bound 2*sqrt(5) = 4.4721.  The
spectrum violates it ONLY at (-1-sqrt(73))/2 = -4.772, with multiplicity
exactly 15 = g_neg.  For the holonet's Ihara immune system (idea 7):

```text
zeta^-1(u) = (1-u^2)^1080 * prod_lambda (1 - lambda u + 5 u^2)
```

and the single non-Ramanujan sector is the natural "sentinel" eigenspace:
any spectral drift is most visible where the graph already presses
against the bound.

## T4: percolation threshold at 1/F_5

Bond percolation Monte Carlo (60 trials/point):

```text
p     : 0.10  0.15  0.18  0.20  0.22  0.25  0.30  0.40
giant : 0.019 0.043 0.089 0.140 0.266 0.494 0.748 0.925
```

The transition brackets the mean-field threshold 1/(k-1) = 1/5 = 0.2 =
1/F_5, linking the percolation-script corpus to the chart atlas: the
holonet fabric percolates when each apartment link is alive with
probability about one in F_5.

## Boundary

Open: identify the D6 antipode-slot space among known 2160-objects (the
BT702-era flag structures? tomotope blocks?); the exact percolation
threshold via the spectral gap; and whether the 15-dim non-Ramanujan
sector is the g_neg = 15-dim irrep of U4(2) inside the web module
(character check, same method as BT742).
