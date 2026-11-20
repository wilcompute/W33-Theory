# Beyond W33: graph girth and repetition length jointly determine ternary CSS distances

**Status:** exact finite coding-theory specialization. This follows existing hypergraph-product CSS theory and does not establish physical quantum hardware or a Theory of Everything.

Let G be a finite connected simple graph with at least one cycle, V vertices, E edges and girth g. Let A be its (V-1) x E reduced oriented incidence check over F3 and let B_L be the (L-1) x L repetition-path check. Their signed hypergraph product gives

  H_X = [ A tensor I_L | I_(V-1) tensor B_L^T ],
  H_Z = [ I_E tensor B_L | -A^T tensor I_(L-1) ].

Full-row-rank checks and mod-3 commutation are exact. Graph cycle and quotient-by-cuts arguments yield:

  [[ L E + (L-1)(V-1), E-V+1, d_X=L, d_Z=g ]]_3.

For X, all L first-block edge slices are equal modulo the cut space im(A^T). If their common class is zero the vector is an X stabilizer, otherwise every slice contributes nonzero support, giving weight >=L; a nonbridge edge repeated L times is a paired logical witness. For Z, summing first-block repetition positions yields a graph cycle in ker(A). If its sum is zero the vector is a Z stabilizer; otherwise the graph's girth bounds its weight below by g. A shortest oriented cycle provides the paired Z logical. This also works for a connected graph with bridge edges, provided some cycle exists.

Independent examples with L=g:

| Graph | V | E | Physical qutrits | Logical qutrits | dX=dZ |
| --- | ---: | ---: | ---: | ---: | ---: |
| C4 | 4 | 4 | 25 | 1 | 4 |
| C4 plus pendant bridge | 5 | 5 | 32 | 1 | 4 |
| 3-cube | 8 | 12 | 69 | 5 | 4 |
| Petersen | 10 | 15 | 111 | 6 | 5 |
| Heawood | 14 | 21 | 191 | 8 | 6 |
| W33 Levi | 80 | 160 | 1833 | 81 | 8 |

For a connected bridgeless cubic graph, E=3V/2. Taking L=g gives N=(5V/2-1)g-V+1, K=V/2+1, and symmetric distance g. Cubic graph families with g proportional to log V therefore offer bounded-check-weight qutrit codes of rate on the order of 1/log V and distance on the order of log V. This is a standard graph-HGP scaling construction, NOT a constant-rate or polynomial-distance result.

**Prior art:** analysis/toe_20261120_graph_repetition_asymmetric_family.py (graph family at fixed L=3), analysis/toe_20261120_repetition_dial_codes.py (W33 Levi with variable L), Tillich-Zemor hypergraph products (arXiv:0903.0566). The present code unifies both parameters and independently tests the graph-with-bridge boundary.

**Reproduce:** python analysis/toe_20261120_graph_girth_balanced_hgp.py

**Physical boundary:** This is a multi-qutrit code and not a one-photon encoding. No decoder threshold, fault-tolerant extraction, experimentally realized holonomy, or derivation of particle physics/spacetime is claimed.
