# Pass 4477 — apartment/H10 prior-art and rediscovery boundary

This note separates the new bridge from older repo ownership and from external finite-geometry literature.  It is intentionally conservative: absence from the searches below is **not** a proof of global novelty.

## Existing repo ownership

The following ingredients are **not new** in Passes 4469–4476:

- **Pass 164 / Pass 201:** the binary quotient `H10 = C^perp/C`, its nondegenerate plus-type `O+(10,2)` form, the 528 singular classes including zero, and the 40 weight-4 line logical operators of the `[[40,10,4]]` CSS code.
- **Pass 187:** the `H10 = 1|8|1` filtration, with the fixed one-dimensional class represented by `im(A_point mod 2)/C`, plus the line-side rank-10 / hull-dimension-9 module data.
- **Passes 4461–4464:** the 1620 building apartments, the `[1620,39]` apartment-parity code, its 29-dimensional radical, and its 10-dimensional nondegenerate symplectic quotient.
- **Pass 4465:** the exact `GQ(s,t)` apartment Gram formula.

The new statements in this continuation are therefore the *maps and identifications between those owned objects*, not the objects themselves.

## New relative to the searched repo corpus

Targeted commit/code searches found no earlier repo statement of the following exact results before this packet:

1. **Pass 4469:** the canonical incidence isometry
   
   `C_ap/rad(C_ap) ~= F_2^40/ker(N^T N) --N--> im(N)/ker(N^T) = H10`.

2. **Pass 4470:** the fact that the mismatch of the two natural Hamming quadratic refinements is represented exactly by Pass 187's fixed `im(A_point)/C` layer, and that one fixed-layer transvection repairs the quadratic isometry.

3. **Pass 4471:** the general characteristic-two criterion
   
   `H H^T = N^T N (mod 2) iff s = 3 (mod 4) and t is odd`.

4. **Pass 4474:** the line-by-line identification of weight-162 apartment generators with the 40 weight-4 minimum logical line classes, together with the singular/anisotropic W33 twin exchanged by the fixed transvection.

5. **Pass 4475:** the apartment-radical invariant filtration `8 | (6+1) | 14`.

6. **Pass 4476:** the six-intersection optimal 10-line basis `P4 + 3K2` and the information-optimal ten-bit protected software readout.

## External primary-source search

The external search was restricted to primary technical sources where possible.

- David B. Chandler, Peter Sin, Qing Xiang, **“The permutation action of finite symplectic groups of odd characteristic on their standard modules”**, arXiv:math/0603100.  This is the correct classical source lane for incidence modules and p-ranks of `W(3,q)` in odd characteristic.  It supplies incidence-module context, not the apartment-parity quotient bridge above.
- Dean Crnković, Daniel R. Hawtin, Andrea Švob, **“Neighbour-Transitive Codes and Partial Spreads in Generalised Quadrangles”**, arXiv:2105.05833.  This treats codes in generalized-quadrangle incidence graphs and automorphism structure, but it is a different code construction from the line/apartment parity image used here.
- Additional targeted arXiv searches for `W(3,3)`, `O+(10,2)`, 10-dimensional characteristic-two modules, apartment incidence codes, and generalized-quadrangle apartment codes did not surface the exact bridge, fixed-layer transvection, or the `s mod 4` Gram-matching criterion.

That last sentence is a search result only.  It should be cited as **“no prior occurrence found in the searched sources”**, never as **“proved novel.”**

## Reviewer-safe statement

A defensible summary is:

> The packet derives a new-to-this-repository explicit equivalence between the W33 building-apartment parity quotient and the previously established protected binary logical-label module.  The equivalence is symplectic by incidence, becomes quadratic after one fixed-layer transvection, and generalizes to `GQ(s,t)` exactly in the orientation class `s=3 mod 4`, `t` odd.  Classical incidence-module and generalized-quadrangle code literature provides relevant background, but the searched primary sources did not exhibit this exact construction.

## Nonclaims

This packet does **not** establish:

- global priority over all finite-geometry literature;
- a second physical code or a new species of logical qubit;
- a physical implementation of the comparison transvection;
- ten physical syndrome measurements in place of the full apartment acquisition problem;
- a causal explanation of the empirical line-signing Ramanujan success rates;
- particle, mass, generation, or cosmological identifications from the modular dimensions `8,6,1,14`.
