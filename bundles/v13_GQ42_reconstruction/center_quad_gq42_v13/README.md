# v13 — Reconstructed GQ(4,2) from the 90 center-quad association scheme

We start with the 90-node center-quad graph (degree 32, diameter 3) and its antipodal relation (distance-3 perfect matching).

## Step 1: Antipodal quotient (45 nodes)

Collapsing antipodal pairs yields a strongly regular graph Q with parameters (45,32,22,24).
Its complement H has parameters (45,12,3,3).

## Step 2: Recover the generalized quadrangle GQ(4,2)

In H:
- the clique number is 5,
- there are exactly 27 cliques of size 5,
- each edge lies in exactly one 5-clique,
- each vertex lies in exactly 3 such cliques.

Therefore those 27 size-5 cliques give a point–line incidence structure with:
- 45 points,
- 27 lines,
- 5 points per line,
- 3 lines through each point,

which matches the parameter counts of a generalized quadrangle of order (4,2).

## Step 3: Z2 voltage / 2-cover structure on Q

The original 90-node graph is a nontrivial Z2-cover of Q:
- for each Q-edge between fibers, the 2 edges in the 90-graph form either a parallel or crossed matching;
- this defines a Z2 voltage/sign on Q edges (file: quotient_Q_edges_with_Z2_voltage.csv).

Triangle parity statistics show the voltage is nontrivial (not a coboundary), so the cover is genuinely twisted.

Files:
- gq42_points_antipodal_pairs.csv: 45 points as antipodal pairs of the 90 quads
- gq42_lines_points.csv: 27 lines (size-5 cliques in H)
- gq42_point_line_incidence.csv: incidence list
- quotient_Q_edges_with_Z2_voltage.csv: Z2 signing on Q edges
