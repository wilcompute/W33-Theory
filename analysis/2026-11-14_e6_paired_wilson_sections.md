# Common sections of compact root-packet Wilson loops

The [single-plaquette census](2026-11-14_six_fronts_exact_USp8_hierarchy_Wilson_photon_MUB_HP3.md) found both maximal coordinate section types for each nonflat commutator of the 36 packet gates. Taking intersections of the fixed-section sets distinguishes the types.

| Common maximal coordinate types | Unordered pairs of nonflat plaquettes |
| --- | ---: |
| Five and six | 44,100 |
| Six only | 1,080 |
| Five only | 0 |
| Neither | 19,440 |

The census uses the exact integer signed permutations and independently reconstructs the 216 maximal five-sections and 72 maximal six-sections as maximal independent sets of the cubic triple graph. All 6,840 pairs sharing a link generator preserve both types. The six-only examples therefore require more than two commutators built from three packet generators with a repeated generator.

One explicit example is the pair of commutators of links (0,1) and (14,15) in the existing root-packet order. Both plaquette actions are 18. The loops commute and their product has trace zero. They have six common maximal coordinate sections, all of dimension six. Their lists are in the JSON certificate.

Intersecting the fixed-section masks gives a stronger limit on this ensemble. Start with the 120 distinct masks and repeatedly intersect with a single-plaquette mask. States with no six-section can be discarded because adding constraints cannot restore one. The closure has 726 masks through pairs and 762 through triples, and is unchanged by a fourth intersection. Among the resulting six-only masks, 120 retain six sections and 36 retain two sections. None retains exactly one. The packet-square holonomies preserve every coordinate subspace, so adjoining these six squares does not remove the residual multiplicity.

## A covariant finite holonomy witness

For this example add six packet-square holonomies, using links 0,1,2,3,4,8. In the native signed cubic chart these are commuting diagonal involutions. Their simultaneous characters distinguish all 27 coordinate lines. In fact, multiplying the six factors I plus or minus the corresponding involution gives 64 times each coordinate projector exactly. Every real subspace invariant under the six involutions is then a sum of coordinate lines: for a vector in the subspace, applying these polynomial projectors extracts each component inside the same subspace.

For coordinate subspaces the cubic section condition holds precisely when no two indices belong to a common cubic triple. Maximality can also be checked against general real extensions. For a fixed coordinate index, contraction with the cubic gives a signed matching on the other indices, because each co-occurring pair lies in a unique triple. Therefore a vector that can be added to a coordinate section has zero coefficient at every neighbor of every index already in the section. If a coordinate section is maximal in the graph test, that intersection of kernels is already the section itself.

Together the two commutators and six involutions thus admit exactly the six listed invariant maximal real sections. A gauge change simultaneously conjugates all holonomies on the section representation and transports the cubic condition in that representation. It preserves the count and dimensions. The six extra holonomies are prescribed inputs. The witness establishes a dimension distinction for that finite tuple. A dynamical selector would need a lattice realization and action that generate the tuple or its gauge orbit, and a stability comparison against other configurations. The continuum distinction between six- and five-coordinate sections comes from exceptional field theory. [Hohm and Samtleben](https://arxiv.org/abs/1312.0614)

Replay with py -3 analysis/toe_20261114_e6_paired_wilson_sections.py.
