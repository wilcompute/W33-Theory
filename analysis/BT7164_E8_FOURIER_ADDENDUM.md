# Pass 7164 addendum — exact C6 Fourier decomposition of the E8 root graph

The Pass7164 hexagonal lift has a global cyclic phase shift `d=c^5` of order six, and root adjacency commutes with that shift. Therefore the 240-dimensional root-adjacency module decomposes exactly into six Fourier sectors of dimension 40.

The certificate works in the exact cyclotomic ring

`Z[zeta_6]`,  `zeta_6^2-zeta_6+1=0`,

not with floating-point eigenvalues. For each phase `k`, the 40x40 cyclotomic block is constructed from the vertical offsets `{+1,-1}` and the cross-fiber offsets `{s,s+1}`. The claimed annihilating polynomial is then multiplied out exactly and verified to be the zero matrix. Dimension and exact trace determine the multiplicities.

The result is

| phase k | exact spectrum |
|---|---|
| 0 | `56^1 + 8^15 + (-4)^24` |
| 1,5 | `28^4 + (-2)^36` |
| 2,4 | `8^10 + (-4)^30` |
| 3 | `(-2)^40` |

Hence the complete positive-inner-product E8 root graph has

`56^1 + 28^8 + 8^35 + (-2)^112 + (-4)^84`.

The phase-zero sector is especially simple. Cross-fiber adjacency counts two edges on every W33 nonedge and zero on every W33 edge, while each fiber contributes vertical degree two. Thus

`M_0 = 2I + 2 A(complement W33) = 2J - 2 A(W33)`.

Because `Spec A(W33)=12^1 + 2^24 + (-4)^15`, this gives immediately

`Spec M_0 = 56^1 + (-4)^24 + 8^15`.

The nonzero phase sectors therefore measure exactly the extra spectral information introduced by the cyclic E8 fiber phases beyond the W33 quotient. No physical Fourier-mode interpretation is asserted.
