# W33: group theory + algebraic topology starting point

This repo already has a lot of numerology/physics-facing exploration. The goal here is to ground the project in **hard invariants** that you can keep building on: explicit group actions, explicit chain complexes, and computed homology.

## What was added

- `claude_workspace/lib/w33_io.py`
  - Loads W33 rays (`W33_point_rays_C4_complex.csv`) and lines (`W33_line_phase_map.csv`) using repo-relative paths.
  - Builds a **simplicial complex** where each W33 line (4 points) is treated as a 3-simplex (a tetrahedron).

- `claude_workspace/lib/simplicial_homology.py`
  - Builds boundary matrices and computes ranks over several large primes.
  - Reports Betti numbers via:  
    \(\beta_k = n_k - \mathrm{rank}(\partial_k) - \mathrm{rank}(\partial_{k+1})\) (over a field).

- `claude_workspace/lib/permutation_group.py`
  - Tiny pure-Python finite permutation-group closure/orbit code (BFS on generators).

- `claude_workspace/w33_group_topology_workbench.py`
  - Computes homology of the “line-K4 flag complex”.
  - Searches for a **ray-realization automorphism subgroup** using monomial unitaries of the form `U = D P` where:
    - `P` is a coordinate permutation in `S4`.
    - `D` is diagonal with entries in the 12th roots of unity (`Z12` phases).

- `claude_workspace/w33_sage_incidence_and_h1.py`
   - Sage-backed computation of the **full incidence automorphism group** of the bipartite graph (points+lines).
   - Computes the induced linear action on **$H_1$** and (optionally) uses **PySymmetry** for isotypic decomposition.

Outputs are written to:
- `claude_workspace/data/w33_group_topology_results.json`

## Current computed facts (from the workbench)

Using the simplicial complex where:
- 0-simplices: 40 points
- 3-simplices: the 40 lines as tetrahedra

Counts:
- n0=40, n1=240, n2=160, n3=40
- Euler characteristic: \(\chi = 40 - 240 + 160 - 40 = -80\)

Homology (stable across multiple primes tested):
- \(\beta_0 = 1\)
- \(\beta_1 = 81\)
- \(\beta_2 = 0\)
- \(\beta_3 = 0\)

Ray-realization automorphisms:
- Detected subgroup order: 108
- Point-orbit structure (under this detected subgroup): sizes `[2,18,2,18]`
- Line-orbit sizes: `[27,6,1,6]`

## How to run

```powershell
python claude_workspace\w33_group_topology_workbench.py
```

For Sage + PySymmetry (recommended via WSL Sage):

- See `claude_workspace/SAGE_PYSYMMETRY_NOTES.md`
- In VS Code, run the task: “WSL: W33 Sage incidence + H1”

## Where to go next (group theory)

1. **Separate “geometry automorphisms” from “ray automorphisms”.**
   - The full automorphism group of the incidence geometry should be much larger than 108.
   - The ray-realization adds extra structure (phases), shrinking the group.

2. **Compute the full incidence automorphism group.**
   - Ideal: use a graph/hypergraph automorphism engine (nauty/traces) or Sage.
   - If staying pure-Python: implement a partition-refinement + backtracking automorphism enumerator for the bipartite incidence graph (80 vertices, 160 edges).

3. **Extract representations.**
   - Once you have a big automorphism group, study its permutation representation on:
     - points (40)
     - lines (40)
     - edges (240)
     - K4 components, triangle classes, etc.

## Where to go next (algebraic topology)

1. **Try different complexes** (each gives different invariants):
   - Bipartite incidence graph (1D CW complex)
   - Clique complex of the non-collinearity graph
   - Complex built from K4 outer sets / centers

2. **Cohomology operations**
   - Cup products mod 2 or mod 3 can sometimes distinguish spaces with same Betti numbers.

3. **Group action on homology**
   - Once you have a good automorphism group: compute its induced linear action on \(H_1\) (over \(\mathbb{F}_p\)) and decompose into irreps.
   - That’s a genuine “group theory → topology → physics” pipeline.
