
# W33 Theory - SageMath Verification of Sp(4,3)
# Run this in SageMath

print("="*60)
print("W33 THEORY: Sp(4,3) VERIFICATION")
print("="*60)

# Create Sp(4,3) - the symplectic group over F_3
G = Sp(4, GF(3))
print(f"\nGroup: Sp(4,3)")
print(f"Order: {G.order()}")
print(f"Expected: 51840")
print(f"Match: {G.order() == 51840}")

# Get character table
print("\nComputing character table...")
chi_table = G.character_table()
print(f"Number of conjugacy classes: {chi_table.nrows()}")
print(f"Number of irreducible representations: {chi_table.ncols()}")

# Print dimensions of irreps
print("\nIrrep dimensions:")
dims = [chi_table[i,0] for i in range(chi_table.nrows())]
for i, d in enumerate(dims):
    print(f"  χ_{i}: dim = {d}")

# Check if 81 appears as an irrep dimension or sum
print(f"\n81 in irrep dims? {81 in dims}")
print(f"56 in irrep dims? {56 in dims}")
print(f"40 in irrep dims? {40 in dims}")
print(f"27 in irrep dims? {27 in dims}")

# Compute the permutation representation on isotropic 1-spaces
print("\n" + "="*60)
print("ISOTROPIC 1-SPACES (W33 GRAPH)")
print("="*60)

# Create projective space
V = VectorSpace(GF(3), 4)

# Standard symplectic form matrix
J = matrix(GF(3), [[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]])

def is_isotropic(v):
    """Check if v is isotropic under symplectic form."""
    return v * J * v == 0

# Find isotropic 1-spaces
isotropic_vectors = [v for v in V if v != 0 and is_isotropic(v)]
print(f"Isotropic nonzero vectors: {len(isotropic_vectors)}")

# Get unique 1-spaces (normalize)
def normalize(v):
    """Normalize vector to have first nonzero entry = 1."""
    for i in range(4):
        if v[i] != 0:
            return v / v[i]
    return v

isotropic_1spaces = list(set(tuple(normalize(v)) for v in isotropic_vectors))
print(f"Isotropic 1-spaces: {len(isotropic_1spaces)}")

# Build the graph
from sage.graphs.graph import Graph

def symp_form(u, v):
    """Compute symplectic form."""
    u = vector(GF(3), u)
    v = vector(GF(3), v)
    return u * J * v

edges = []
for i, u in enumerate(isotropic_1spaces):
    for j, v in enumerate(isotropic_1spaces):
        if i < j and symp_form(u, v) != 0:
            edges.append((i, j))

W33 = Graph(edges)
print(f"\nW33 Graph:")
print(f"  Vertices: {W33.num_verts()}")
print(f"  Edges: {W33.num_edges()}")

# Verify SRG parameters
if W33.is_strongly_regular():
    params = W33.is_strongly_regular(parameters=True)
    print(f"  SRG parameters: {params}")
else:
    print("  NOT strongly regular (unexpected!)")

# Compute eigenvalues
print("\nSpectrum of W33:")
spec = W33.spectrum()
print(f"  {spec}")

# Automorphism group
print("\nAutomorphism group of W33:")
aut = W33.automorphism_group()
print(f"  Order: {aut.order()}")
print(f"  Expected (Sp(4,3)): 51840")
print(f"  Match: {aut.order() == 51840}")

# Clique number
print("\nClique structure:")
print(f"  Clique number: {W33.clique_number()}")
cliques = W33.cliques_maximum()
print(f"  Number of maximum cliques: {len(cliques)}")

# Chromatic number
print(f"  Chromatic number: {W33.chromatic_number()}")

# Independence number
print(f"  Independence number: {W33.independent_set(value_only=True)}")

print("\n" + "="*60)
print("CHARACTER TABLE ANALYSIS")
print("="*60)

# The permutation character on W33 (40 points)
# This is the character of the natural action on isotropic 1-spaces

# For deep analysis, decompose the permutation character
print("\nPermutation character on 40 points:")
print("This represents the W33 action")

# Compute homology
print("\n" + "="*60)
print("HOMOLOGY OF W33 COMPLEX")
print("="*60)

# The clique complex
from sage.topology.simplicial_complex import SimplicialComplex

# Build simplicial complex from cliques
simplices = []
for clique in W33.cliques():
    if len(clique) >= 2:
        simplices.append(tuple(sorted(clique)))

# Add vertices
for v in W33.vertices():
    simplices.append((v,))

K = SimplicialComplex(simplices)
print(f"Simplicial complex from W33:")
print(f"  Dimension: {K.dimension()}")
print(f"  f-vector: {K.f_vector()}")

# Betti numbers
print(f"\nBetti numbers:")
for i in range(K.dimension() + 1):
    print(f"  β_{i} = {K.betti(i)}")

print("\n*** SAGE VERIFICATION COMPLETE ***")
