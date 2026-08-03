# Passes 2967–2970 — S6 curvature, route decoding, and receiver correction

Pass 2967 refines the completed all-spread D4 holonomy theorem. Taking permutation sign yields a gauge-invariant triangle curvature. On every one of the 36 spreads, the 60 odd triangles form a 2-(10,3,4) design and every tetrahedron contains an even number of odd faces. All 1024 vertex-sign gauges preserve the curvature. Its switching class contains the Petersen graph and has automorphism group PΣL(2,9) ≅ S6 of order 720 in the degree-ten action on 3+3 partitions of a six-set. The abstract identification is standard two-graph theory; the project-specific theorem is its exact emergence from every W33 spread router.

Pass 2968 proves the triangle-edge matrix H has rank 36 and kernel equal to the cut space of K10. Therefore the parity layer is the binary [45,9,9] code with weight enumerator

1 + 10 z^9 + 45 z^16 + 120 z^21 + 210 z^24 + 126 z^25.

All nongauge odd faults through weight 8 are detected and odd faults through weight 4 are correctable modulo slot gauge.

Pass 2969 corrects the Pass 2954 receiver label. The minimum project-local Pauli cover remains {YI,IY}, but its success (1+1/sqrt(3))/2 = 0.788675 is not the unrestricted Helstrom bound. Since every conjugate pair has squared overlap 1/3, ideal equal-prior Helstrom success is (1+sqrt(2/3))/2 = 0.908248. For n copies it is (1+sqrt(1-3^-n))/2. Adaptive individual attainability is published prior art: Acín et al., Phys. Rev. A 71, 032338 (2005), arXiv:quant-ph/0410097.

Pass 2970 welds the completed three-pilot theorem to the parity code. Three pilots identify one arbitrary nonidentity S4 edge error, including even errors invisible to sign curvature. The curvature layer adds multi-edge correction for odd faults. No simultaneous arbitrary-S4 pilot theorem is claimed.

Reproduce with:

```bash
python analysis/bt2967_oam_holonomy_s6_two_graph.py
python analysis/bt2968_curvature_route_code.py
python analysis/bt2969_chirality_receiver_correction.py
python analysis/bt2970_layered_route_fault_architecture.py
```
