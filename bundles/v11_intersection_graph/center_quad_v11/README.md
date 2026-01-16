Center-quad (K4 component) intersection graph for W33 (v11)

Background
- W33’s four-center triads form 90 disjoint K4 components.
- Each component has a 4-point "center quad" C (the common-neighbor set of its four triad states).

Construction
- Nodes: the 90 distinct center quads.
- Edge between two center quads iff they intersect in exactly one W33 point.

Empirical results (from W33_line_phase_map.csv)
- n = 90 nodes, regular degree k = 32
- adjacent pairs have exactly 13 common neighbors (constant lambda)
- nonadjacent pairs split into 3 classes by common-neighbor count: 12, 9, or 0

This is not a single SRG; it is a 3-class association structure.
Notably, Aut(W33) acts transitively on these 90 nodes.

Files
- center_quad_nodes.csv
- center_quad_edges_intersection1.csv
- center_quad_intersection1_graph.gexf
- stats.json

Adjacency spectrum: 32^1, 8^15, 2^24, (-4)^50
