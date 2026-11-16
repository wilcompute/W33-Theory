# Reconstructing the toroidal gauge kinetic matrix from reflection sectors

The [reflection-sector census](2026-11-15_torus_cs_sectors.md) gives 45 supersymmetric STU sectors, one for each tritangent monomial of the signed $E_6$ cubic. Their gauge kinetic matrices recover only the six torus-radius directions. The eleven-vector half-maximal sectors supply the missing 36 generators. The distinction between observing the full matrix entry by entry and recovering its known coset generators gives different optimal covers.

## The 42 tangent generators in the signed charge basis

Use the [integral torus charge dictionary](2026-11-15_quiver_torus_charge_dictionary.md) and normalize the kinetic matrix at the flat reference point to the identity. In the convention $M=V V^{\mathsf T}$, a symmetric coset generator $X$ determines $M=\exp(2X)$ in exponential coordinates. The scalar and vector kinetic terms of maximal five-dimensional supergravity use the 42-dimensional coset $E_{6(6)}/USp(8)$. [Kreutzer, canonical analysis of maximal supergravity](https://arxiv.org/abs/2005.13553) · [Hohm and Samtleben, exceptional field theory and the torus frame](https://arxiv.org/abs/1312.0614)

The verifier builds the infinitesimal equation $dN(x)[Xx]=0$ directly from the 45 signed monomials. Torus-reflection characters split this equation into small independent blocks. The diagonal symmetric block has nullity six. The log-radii $t_i$ give its basis, with the three types of diagonal $X$ entries

$$
X_{P_iP_i}=t_i+\tfrac13\sum_j t_j,\quad
X_{M_{ij}M_{ij}}=-t_i-t_j+\tfrac13\sum_k t_k,\quad
X_{K_iK_i}=t_i-\tfrac23\sum_j t_j .
$$

These weights follow from the Einstein-frame volume factors and dualization of the two-form vectors. They annihilate the signed cubic term by term. For a pair of distinct charge labels $i,j$, its matrix entry has reflection character $\chi_i+\chi_j$. Each of the 27 singular nonzero characters supports five pairs and has zero symmetric or alternating nullity. Each of the 36 nonsingular characters supports six disjoint pairs and has one symmetric and one alternating solution. The symmetric generator can be normalized to have all six entries $\pm1$. Thus the exact cubic stabilizer gives a 42-dimensional symmetric space and a 36-dimensional skew space in the same orthonormal charge basis.

## Why the STU kinetic matrices see only six scalars

Every pair of distinct vectors in an STU sector belongs to a tritangent. Its character sum is the third singular character. No off-diagonal scalar generator has that character, and the diagonal is neutral. The three-vector block therefore reads two independent log-radius directions and none of the 36 nonsingular directions. Taking all 45 sectors covers all 27 diagonal entries and 135 tritangent off-diagonal entries, leaving 216 other entries unread. Its combined tangent information has rank six.

This invisibility holds for finite scalar values within each reflection-fixed sector in exponential coordinates. Every scalar generator fixed by the sector's reflections preserves its fixed vector subspace. The 12 retained off-diagonal scalar directions act as zero on the fixed three vectors. Four of the six retained radial directions also act trivially there, leaving a rank-two radial response. The restriction of the kinetic matrix is the exponential of the diagonal restriction alone. This gives 16 scalar directions invisible to the kinetic matrix inside each 18-scalar STU sector, consistent with the vector and hypermultiplet counts.

## Three half-maximal sectors recover all coset generators

Each eleven-vector sector individually reads the six radial directions. Each of the 36 other generators can be read in exactly 15 of the 27 sectors, with two of its six nonzero entries present in each such sector. The other four entries follow from the unique one-dimensional signed-cubic solution in its character block. Thus a covering measurement requires one compatible sector for every generator, with shared scalar and vector coordinates and a common normalization at the origin.

The exact minimum is **three**. The 45 triples attaining it are precisely reflection labels that form a tritangent. If the three labels sum to zero, their evaluation on any scalar character cannot be odd in all three. The verifier checks that every even nonsingular character actually has a nonzero retained entry and that no other triple covers all responses. Thus the three single-reflection sectors associated with an STU subgroup together recover the 42 generators even though their common STU sector only sees the diagonal. From these normalized generators the standard coset exponential gives the nonlinear kinetic matrix in the chosen coordinates. The conclusion uses the $E_{6(6)}/USp(8)$ framework and the signed cubic constraints.

## Eleven half-maximal sectors read the entire symmetric matrix entrywise

Without using the generator constraints, the coverage problem is different. Each diagonal entry lies in 11 sectors, each of the 135 tritangent pairs lies in three, and each of the 216 other pairs lies in five. The exact minimum for observing all 378 entries is **eleven**. There are 27 minimizers. Their sets of reflection labels are the 27 eleven-point perp-sets under the point–reflection identification of the previous calculation.

The certificate verifies both minima by branching on an entry or generator still lacking a reading. Every completing set must include an index from that uncovered requirement. Branching over those choices exhausts the lower cardinalities and all minimal covers. The entrywise statement refers to the array positions that can be read across the sectors, each on its own fixed scalar locus.

## The first nonlinear terms invisible to all 27 sectors

For a kinetic coefficient with incoming vector character $v$, reflection equivariance fixes the other vector character to $v+\chi_1+\cdots+\chi_n$, where the $\chi_i$ are its scalar characters. A reflection reads this coefficient directly if its character is orthogonal under the coordinate dot product to $v$ and every $\chi_i$. At degree at most two, these conditions leave a subspace of dimension at least three. Such a subspace contains a nonzero singular character. Indeed, if all nonzero vectors in it were nonsingular, the quadratic polar pairing would be one on any two distinct nonzero vectors. For independent $a,b,c$, bilinearity would then make the pairing of $a$ with $b+c$ zero, a contradiction. Every reflection-allowed Taylor coefficient through second order can therefore be read in some half-maximal sector.

At degree three there are missing coefficients even in the actual kinetic exponential. The verifier multiplies the signed generator matrices and counts **4,320 nonzero cubic coefficients** of upper-triangular entries that disappear from every sector restriction. An explicit example uses scalar characters $3,5,7$, encoded as bit masks for $g_{12}$, $g_{13}$ and $C_{456}$ respectively. In the certificate's generator normalization their product has coefficient $4$ in the $(M_{12},K_2)$ entry of $\exp(2X)$. Every half-maximal sector retaining all three scalars discards the relevant vector pair. The kinetic exponential predicts these coefficients from the first-order generators. Without the coset constraint, restrictions to the 27 fixed loci alone leave this Taylor data undetermined.

## Exceptional field theory changes the minimum

The strong section constraint of $E_{6(6)}$ exceptional field theory requires $d^{MNK}\partial_N f\,\partial_K g=0$ for any fields or gauge parameters. In the signed coordinate basis, a set of derivative labels obeys this for arbitrary dependence on those coordinates exactly when no pair belongs to a tritangent. A pair on a tritangent gives a nonzero component in the third direction. The [repository's section analysis](2026-11-14_E6_ExFT_dynamical_section_selection_flux_duality_audit.md) also treats the distinction between the five- and six-direction sections. The test here uses this constraint to select which reflection labels may be used together for kinetic readings. [Hohm and Samtleben, the M-theory and Type IIB sections](https://arxiv.org/abs/1312.0614)

The optimal three-reflection cover above violates this compatibility. Under the coordinate strong constraint, the minimum rises to **five**. All 216 maximal five-direction sections read all 42 generators. Every one of the 72 maximal six-direction sections leaves exactly one generator unread, and none of its subsets can recover it. For the six standard momentum directions the blind scalar is the dual six-form scalar. Each of the 36 nonsingular reflection characters has exactly two six-direction sections blind to it. Their union is the corresponding double-six. This is an operational distinction between the two coordinate section families under this measurement rule. The section constraint itself allows both families and supplies no dynamical selection between them. The result does not classify the measurement problem in non-coordinate sections.

The explicit cubic witness supplies three scalar and two vector labels for a five-point amplitude unavailable in every half-maximal sector. The coefficient above belongs to the local kinetic term. An on-shell comparison must include exchange graphs and account for field redefinitions. A dimensionally reduced double-copy superamplitude gives an independent tree-level benchmark. Protected automorphic higher-derivative couplings offer a separate test of which reflection restrictions lose quantum data. [Cachazo et al., maximal-supergravity tree amplitudes](https://arxiv.org/abs/1805.11111) · [Green, Russo and Vanhove, toroidal string amplitudes](https://arxiv.org/abs/1001.2535) · [Coimbra, Strickland-Constable and Waldram, generalized metric](https://arxiv.org/abs/1212.1586)

Replay with SymPy.

    python -B analysis/toe_20261115_torus_kinetic_reconstruction.py

The [certificate](../data/toe_20261115_torus_kinetic_reconstruction.json) records all 36 signed off-diagonal generators, the radial basis, and the optimal cover witnesses.
