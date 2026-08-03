# Passes 2967–2970 — S6 curvature, route decoding, and chirality receiver correction

## Pass 2967 — exceptional ten-point two-graph

Pass 2962 established the all-spread nonabelian D4 holonomy classification. Pass 2967 takes the permutation sign and classifies the resulting gauge-invariant triangle curvature.

For every one of the 36 spreads, the 60 odd triangle holonomies form a 2-(10,3,4) design. Every four-mode tetrahedron contains an even number of odd faces, so the finite connection obeys the exact Bianchi identity delta^2=0. All 1024 vertex-sign gauges preserve this curvature.

All 36 curvature hypergraphs are isomorphic. Their switching class contains the Petersen graph, and the full automorphism group is

PΣL(2,9) ≅ S6, of order 720,

in the degree-ten action on unordered 3+3 partitions of a six-set. The two S6 orbits on triples have sizes 60 and 60 and are exactly the odd/even curvature sectors.

This identification is standard two-graph theory, not a novelty claim about the abstract object. The project-specific theorem is its exact emergence from every W33 spread-router transport table. See Seidel, *Graphs and two-graphs* (1974), and Cameron–Spiga, arXiv:1407.5288.

## Pass 2968 — [45,9,9] parity route code

Let H be the 120 by 45 triangle-edge incidence matrix of K10. Subtracting the certified Pass 2967 curvature baseline from an observed parity table gives syndrome s=He.

Exact row reduction proves rank(H)=36 and ker(H)=Cut(K10), hence the invisible parity patterns form the binary [45,9,9] cut code. Its weight enumerator is

1 + 10 z^9 + 45 z^16 + 120 z^21 + 210 z^24 + 126 z^25.

Therefore every nongauge odd-parity fault through weight 8 is detected and every odd-parity fault through weight 4 is correctable modulo vertex switching. Single-edge syndromes are unique and have weight 8. The 120 raw checks compress to 36 independent bits.

## Pass 2969 — correction to the chirality receiver claim

Pass 2954 correctly found the minimum project-local Pauli probe alphabet {YI,IY}, and every conjugate hard-shell pair has squared overlap 1/3. However,

(1+1/sqrt(3))/2 = 0.788675...

is the success probability of the selected local Pauli receiver, not the unrestricted Helstrom bound. The correct equal-prior pure-state Helstrom success is

(1+sqrt(1-1/3))/2 = (1+sqrt(2/3))/2 = 0.908248....

For n copies, the exact optimum is

P_success(n) = (1+sqrt(1-3^{-n}))/2.

Published prior art proves that adaptive individual von Neumann measurements attain the collective bound for binary pure states at every finite n: Acín, Bagan, Baig, Masanes, and Muñoz-Tapia, *Multiple-copy two-state discrimination with individual measurements*, Phys. Rev. A 71, 032338 (2005), arXiv:quant-ph/0410097.

Six copies drive the ideal equal-prior error below 10^-3; twelve drive it below 10^-6. These formulas assume the conjugate pair/frame is known and measurements are ideal.

## Pass 2970 — layered route defense

The completed Pass 2965 theorem on master proves that three distinct pilot slots detect all 23 nonidentity S4 permutations for one faulty route edge, across all 8,280 triangle/edge/fault cases. Pass 2968 adds multi-edge protection only for the odd-parity projection.

The layers are complementary:

- three pilots identify one arbitrary even or odd S4 edge fault;
- the 36-bit curvature syndrome corrects up to four odd-parity edge faults modulo gauge and detects nongauge odd faults through weight eight.

No theorem extends the pilot guarantee to simultaneous arbitrary S4 faults. Even-permutation multi-edge errors, optical loss, coherent phase drift, and detector erasure remain outside the parity code.

## Reproduction

```bash
python analysis/bt2967_oam_holonomy_s6_two_graph.py
python analysis/bt2968_curvature_route_code.py
python analysis/bt2969_chirality_receiver_correction.py
python analysis/bt2970_layered_route_fault_architecture.py
```
