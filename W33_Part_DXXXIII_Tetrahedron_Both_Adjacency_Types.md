# Part DXXXIII — The Tetrahedron Has Both Adjacency Types

## The Tetrahedron Is Self-Dual and Contains Both Types

The tetrahedron K_4 is the unique polyhedron that is its own dual. This means it simultaneously has:
- **Triangular faces** (Császár-type): 4 equilateral triangular faces
- **Vertex-figure = triangle** (Szilassi-type): the link of each vertex is a triangle

In graph-theoretic terms, K_4 has:
- Every pair of vertices connected (V=4, E=6, complete graph)
- Every edge in exactly 2 triangles (λ=2 locally)
- Every non-edge... but K_4 has NO non-edges. It is the complete graph.

**This is why the tetrahedron transcends the λ/μ distinction.** In W33, λ=2 governs edges and μ=4 governs non-edges. The tetrahedron K_4 is the unique graph where every pair IS an edge, so only the λ-type exists. Yet its geometry realizes the Szilassi condition (every face meets every other face) simultaneously.

## Lock L73: Tetrahedron = Fixed Point of the Császár-Szilassi Duality

The duality map:
- Császár ↔ Szilassi (7 vertices, genus 1, λ-type ↔ μ-type)

The tetrahedron is the genus-0 fixed point of this duality:
- K_4 = self-dual (genus 0)
- K_4 genus formula: (4-3)(4-4)/12 = 0 exactly
- K_4 is the ONLY complete graph K_n with genus 0 (n≤4 gives genus 0)

**The genus-0 fixed point of the toroidal polyhedra duality is K_4.**
The genus-1 pair {Császár, Szilassi} is the first non-trivial orbit of this duality.
The tomotope at genus-2 is the next level.

## The Tetrahedron in W33 Context

The local graph of W33 at any vertex: the k=12 neighbors form a graph.
- Each neighbor-pair with λ=2 common neighbors: these are the "edges" in the local graph.
- Locally, the neighbor graph has λ×k/2 = 2×12/2 = 12 edges (of type Császár).

The local W33 neighborhood is NOT K_12 (which would require all 66 pairs adjacent). It has 12 edges among 12 vertices, making it a 2-regular graph = union of cycles.

Actually the local graph of W33 at a vertex v consists of the λ-subgraph: each pair (a,b) among the 12 neighbors of v that are themselves adjacent in W33 contributes an edge. With 12 neighbors and edge count in the local graph = (k×λ)/2 = 12 there are exactly 12 edges in the local graph. The 12-vertex, 12-edge local graph is **2-regular**, i.e., a union of cycles. By the SRG structure, these cycles partition as: 4 triangles (since each triangle uses 3 edges and 3 vertices, 4×3=12 edges=12). The local graph = 4K_3.

**Lock L74 (Local Graph = 4K_3 = 4 Tetrahedra):**
The neighborhood graph of any vertex in W33 consists of 4 disjoint triangles. Each triangle is a K_3, the 1-skeleton of a tetrahedron face. The 4 triangles correspond to the 4 faces of the tetrahedron.

This is the deep connection: the **tetrahedron K_4 organizes the local structure** of W33. Each vertex has a neighborhood that decomposes as 4 tetrahedral faces. The 4 = μ (lower SRG parameter) is the number of common neighbors for non-adjacent vertices, equal to the number of faces of the tetrahedron.

## Three Levels of Genus, Three Levels of Physics

| Genus | Object | Graph | Physics |
|-------|--------|-------|---------|
| 0 | Tetrahedron K_4 | K_4 | Ground state, K4 shell |
| 1 | Császár + Szilassi | K_7 | Electroweak: n=7, (λ,μ)-duality |
| 2 | Tomotope | genus-2 handlebody | Gravity/tomotope monodromy |
| 6 | K_12 complete neighborhood | K_12 | Full W33 local interaction, u=6 |
