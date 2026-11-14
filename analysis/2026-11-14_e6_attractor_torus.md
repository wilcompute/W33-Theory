# Exact charge-norm minimum in the five-dimensional Pauli chart

[Pass 12665](PASS12665_ATTRACTORS_ARE_PURE_STATES.md) observed V_min = 3|N|^(2/3) and the quaternionic spectrum of its minimizing charges numerically. The exact Pauli intertwiner gives a constructive proof. All statements below use the charge and norm normalization of that pass. [Ferrara and Gunaydin on attractor orbits](https://arxiv.org/abs/hep-th/0606108)

## Attaining the global bound

The four real quaternionic eigenvalues of the traceless Hermitian charge operator can be diagonalized by a compact symplectic transformation. In that frame the operator lies in the span of Pauli labels 16, 32 and 48, the two commuting Z's on the last two factors and their product. Write the coefficients as a,b,c. The eigenvalues are sa*a+sb*b+sc*c for sign triples with sa*sb*sc=1. The norm squared V is a^2+b^2+c^2 and the cubic N is abc. These formulas and the native-coordinate signs are checked exactly.

For any charge on the same split-group orbit, diagonalize again and apply arithmetic-geometric mean to the three squared coefficients. This gives V >= 3|N|^(2/3). To attain it, the verifier solves the exact diagonal Lie algebra equations in the native chart. Each of the 45 signed cubic monomials has zero sum of weights. On the Pauli triad the two solutions restrict to (1,0,-1) and (0,1,-1). Their exponentials therefore implement all positive rescalings of the three components with product one. When N is nonzero, choose factors |N|^(1/3)/|a| and the corresponding factors for b,c. Each coefficient then has magnitude |N|^(1/3), giving equality. The symmetric-space norm minimization has the same value because the compact factor in a split-group polar decomposition preserves the norm.

This constructs a minimizing charge by diagonalizing, rescaling and rotating back. For N>0 the character given by the three coefficient signs has the unique top eigenvalue. It is unchanged by the positive rescaling. For N<0 the opposite character has the unique bottom eigenvalue and is also unchanged. The constructed endpoint thus lies on the top quaternionic line for positive cubic and on the bottom line for negative cubic. This proves an exact route to the endpoints found numerically. It leaves open the nearest point in the full scalar manifold and which endpoint a specified radial equation selects.

If N=0 and the charge is nonzero, at least one diagonal coefficient vanishes. Choose weight -1 on every occupied coordinate, with the balancing positive weight placed on an empty coordinate. The same torus scales the whole charge to zero in the limit. Invertibility at finite parameter implies that infimum zero is not attained for nonzero charge.

## Physical normalization of negative cubic charges

For negative N the normalized operator X/|N|^(1/3) has spectrum (-3,1,1,1) with quaternionic multiplicities. The affine density-matrix criterion is X+I positive semidefinite in the original normalization. Thus a balanced negative-cubic charge is a physical charge whenever |N|^(1/3) <= 1/3. For example, the state uniformly supported on three quaternionic lines has spectrum (1/3,1/3,1/3,-1), N=-1/27 and V=1/3. It is already a norm minimum on its orbit. The normalized negative endpoint in the parallel report lies outside the state body, while the physical rescaled example lies on its boundary.

Replay with py -3 analysis/toe_20261114_e6_attractor_torus.py.
