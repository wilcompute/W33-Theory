
# SAGEMATH CODE FOR W33 ANALYSIS
# Run in SageMath notebook or sage shell

# 1. Construct Sp(4,3)
G = Sp(4, GF(3))
print(f"Order: {G.order()}")

# 2. Build the graph
from sage.graphs.strongly_regular_db import strongly_regular_graph
# W33 is the symplectic graph Sp(4,3)
W33 = graphs.SymplecticPolarGraph(4, 3)
print(f"Vertices: {W33.order()}")
print(f"Edges: {W33.size()}")
print(f"Is strongly regular: {W33.is_strongly_regular()}")
print(f"Parameters: {W33.is_strongly_regular(parameters=True)}")

# 3. Compute clique number (should be 4)
print(f"Clique number: {W33.clique_number()}")

# 4. Independence number
print(f"Independence number: {W33.independent_set(value_only=True)}")

# 5. Chromatic number
print(f"Chromatic number: {W33.chromatic_number()}")

# 6. Automorphism group
A = W33.automorphism_group()
print(f"Automorphism group order: {A.order()}")

# 7. Character table of Aut(W33)
# This takes time for large groups
# print(G.character_table())

# 8. Clique complex and homology
cliques = W33.cliques_maximum()
print(f"Maximum cliques: {len(cliques)}")

# 9. Build simplicial complex from cliques
from sage.topology.simplicial_complex import SimplicialComplex
facets = [tuple(c) for c in W33.cliques_maximal()]
SC = SimplicialComplex(facets)
print(f"Facets: {len(SC.facets())}")

# 10. Homology groups
for i in range(4):
    print(f"H_{i} = {SC.homology(i)}")
