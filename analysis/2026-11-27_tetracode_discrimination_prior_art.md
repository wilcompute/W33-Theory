# Tetracode operational discrimination and explicit prior-art reconciliation

2026-11-27. Follow-up to ba0f928 and 10918253.

Repository overlap found in the further search:
- PASS10948_CLOCK_TETRACODE_NEGACYCLIC_HYPERBOLIC_BRIDGE already enumerated the eight monomial tetracode images, stabilizer 48, and a transverse pair. The count eight and E8 gluing are not new to this repository.
- PASS11164_THREE_QUTRIT_TETRACODE already recognizes the two-qutrit tetracode gate and established MDS-to-AME constructions. The AME existence is not new.
- PASS11869_11873_SIEGEL_LEVEL3_TWO_QUTRITS treats a different genus-two theta-function representation on C^9; the present finite double uses C^6561 at genus two and counts mapping-class invariant vectors. Do not conflate those carriers.

The new packet combines the complete orthogonal ruling geometry with the exact seven-dimensional modular fixed span, positive integral cone, folded primitive null vectors, genus-two recovery of the eighth direction, and state discrimination certificates.

Minimum-error discrimination (uniform prior): write R = positive square root of Gram G_g, n = 2(p+1). Its diagonal is constant d = Tr(R)/n by transitivity of the Gram automorphisms. Represent the states as columns r_i of R. The support-projected computational-basis POVM realizes the square-root measurement, with mean success d^2. A matching dual certificate is Y=d R/n. For every vector v, |v^* R e_i|^2 <= (v^*Rv) R_ii = d v^*Rv by positive semidefinite Cauchy-Schwarz, so Y-r_i r_i^*/n >=0. Its trace is d^2. This proves optimality including the rank-deficient one-copy case, without assuming orthogonality of states.

Therefore P_min_error_success = (Tr sqrt(G_g)/n)^2, evaluated by the three exact eigenvalues in the companion note. For p=3, g=1, P=13/24+sqrt(3)/6. For two copies P~0.9874917451, while error-free unambiguous discrimination succeeds with probability 16/27. The latter allows an inconclusive result. Distinct operational tasks; not a contradiction. Eight-qutrit joint POVM assumed for two copies; no implementation efficiency claimed.

Numerical independent check: build actual 81x8 code-state columns and 6561x8 two-copy columns; verify Gram equality and the dual PSD conditions to 1e-12 for g=1..4; verify reciprocal-vector USD completeness for g>=2. All checks passed on server. Exact proof above does not rely on the numerical slack tolerance.

References: Eldar, arXiv:quant-ph/0206093 (USD SDP); Eldar and Forney, On quantum detection and the square-root measurement (2001). No priority claim for standard discrimination machinery.

Replay: python analysis/toe_20261127_tetracode_discrimination.py (NumPy).

No new hardware data, CI run, or full weekly diff audit is claimed.
