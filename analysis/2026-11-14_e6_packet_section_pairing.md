# Double-six obstruction for compact E6 packet words

The [paired Wilson census](2026-11-14_e6_paired_wilson_sections.md) found that even an arbitrary collection of single packet commutators cannot retain exactly one six-coordinate section. In the native cubic chart this obstruction extends to arbitrary words in the 36 packet gates and their inverses. The same extension admits a unique five-coordinate section.

## An invariant pairing

In the graph whose edges are co-occurring indices of the signed cubic, each six-section is an independent sextuple. For every sextuple A, precisely one disjoint sextuple B has 30 edges across to A. The other 20 disjoint sextuples each have 21. Symmetry and uniqueness imply that taking this partner is a fixed-point-free involution. Its 36 pairs are the classical Schlaefli double-sixes. Their role here is to constrain common invariant sections of the packet holonomies. [Cubic-surface incidence geometry](https://www.math.uni-bonn.de/people/huybrech/Notes.pdf)

The permutation part of each signed packet gate is a graph automorphism. Thus it commutes with the partner involution. The same holds for every word, and any word fixing A fixes B. Consequently every collection of packet words preserves an even number of coordinate six-sections, including zero. With the six separating packet squares used in the paired census, every invariant real section is coordinate in the native frame. So the evenness conclusion then applies to all invariant maximal real six-sections and is preserved under simultaneous gauge transport.

## Explicit five-section and six-section witnesses

Write U_i for a packet gate in the existing index order. The three holonomies U_0, [U_11,U_35], [U_14,U_26], together with the six separating involutions, retain exactly one maximal real section. Its indices are (2,3,5,9,21). A second tuple with [U_0,U_1], [U_14,U_15], U_4 and the same markers retains precisely the two members of a double-six. The explicit sextuples and all 36 partner pairs are recorded in the JSON.

Each tuple can be realized on an open two-row lattice strip with one face per holonomy. Set every bottom link and every rung to the identity. With faces traversed from bottom left along the bottom and the top links oriented rightward, set each top link to the inverse of its prescribed face holonomy. The face loops transport to one base point along identity bottom links. Each construction has total Wilson action 192 with the same trace normalization, so this action gives equal scores for these two distinct fixed-section outcomes. On the unconstrained strip the all-identity connection has action zero. A physical section selector would need dynamics or boundary conditions that favor a nonflat configuration. [E6 exceptional field theory](https://arxiv.org/abs/1312.0614)

Replay with py -3 analysis/toe_20261114_e6_packet_section_pairing.py.
