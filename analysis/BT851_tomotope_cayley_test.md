# BT851 — The Tomotope Is a Cayley Maniplex Over the Klein Group

**Status: PROVEN (machine-verified, `analysis/bt851_tomotope_cayley_test.py`, data `data/bt851_tomotope_cayley_test.json`)**

Cunningham–Mochán–Montero (*Cayley extensions of maniplexes and polytopes*,
JCTA 2025) generalize Cayley maps: a maniplex is **Cayley** when a subgroup of
its automorphism group acts regularly on its vertices. Applied to the
middleware:

## Results

- **Vertex action:** Aut(tomotope) (order 96) acts on the 4 vertices with
  image the **full S₄** (kernel of order 4 — four automorphisms fix every
  vertex).
- **Cayley verdict: YES**, with regular subgroup the **Klein four-group
  V₄ = Z₂×Z₂**. The tomotope is a Cayley maniplex over F₂² — the substrate's
  register group (the flat F₂-register bundles of BT741, the F₄² icosahedral
  register of BT809, the mask groups of the selector layer).
- **Other induced actions:** faithful (order 96) and transitive on the 12
  edges and on the 16 faces; cells split **[4, 4]** — the BT850 phase split
  (tetrahedral vs hemioctahedral), as forced by class 2_{0,1,2}.

## Reading

The maniplex-literature dig (BT849–851) now gives the middleware a complete
modern classification card:

```text
tomotope = uniform 4-polytope, monodromy 18432 = 96 × 192 (not a C-group)
         = 2-orbit maniplex, class 2_{0,1,2} (cell-alternating: sphere/projective)
         = Cayley maniplex over V4 = F2^2
         covers: infinitely many minimal regular ones (the rank-4 pathology)
```

Hardware translation: the runtime's vertex layer is a *free F₂² torsor* — the
packet phase space is literally a Cayley structure over the register group,
so register XOR-addressing extends from the chart layer (BT777) into the
middleware's vertex layer with no further structure needed.

## Open

- Cayley *extensions*: CMM build extensions where a chosen group acts
  regularly on the facets of the extension. Candidate: extend the compass
  hemi-dodecahedra by V₄ or F₄² and see which member of the BT831 cover
  architecture appears.
- The kernel-4 subgroup (vertex-fixing automorphisms): identify it among the
  BT85 matched-pair data (the 2-core of P?).
