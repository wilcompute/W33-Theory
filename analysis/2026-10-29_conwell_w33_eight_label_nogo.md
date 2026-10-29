# Symmetry obstruction: W33's eight binary CSS logical dimensions are not Conwell's eight labels

**2026-10-29.** Companion to `analysis/2026-10-29_w33_adjacency_css40_hexads.md` and the finite Conwell `G_2(8)` construction.

The exact binary W33 adjacency code has eight **logical dimensions**. The Klein-quadric complement has 28 points identified with unordered pairs of **eight Conwell heptad labels**, equivariantly under `GL4(2) ≅ A8`. Equality of the two eight-counts is not enough to identify the representations.

**No-go under full permutations:** The W33 graph symmetry group `G=PGSp4(3)` has order 51,840; its index-two normal subgroup `H=PSp4(3)` is *nonabelian simple*, order 25,920. The natural Conwell label action is contained in `S8`, order 40,320. Since 25,920 does not divide 40,320, no injective group homomorphism `H -> S8` exists. Simplicity implies **every** homomorphism from H to S8 is trivial. Therefore any homomorphism `G -> S8` factors through `G/H ≅ C2`. In particular it cannot induce the transitive A8 action on eight labels, or act transitively on their 28 unordered pairs. Conversely, A8 of order20,160 cannot embed in G because 20,160 does not divide 51,840.

This also rules out a *surjective* full-W33-equivariant 40-point -> 28-Conwell-pair map under a natural induced eight-label permutation action. Such a map would send the W33 transitive orbit onto an orbit of size at most two.

**Crucial scope distinction:** The eight logical qubits form an **eight-dimensional vector space over F2**, and G can act nontrivially by an eight-by-eight invertible linear representation rather than by permutation of eight basis labels. The no-go concerns **permutation identification of eight labeled coordinates under full G**. It does not ban a common proper subgroup, a restricted symmetry after physical boundary or vacuum selection, an independently defined correspondence without full equivariance, or a representation-theoretic transform through a higher module.

This is a short group-theoretic consequence of established orders, *not* a new classification theorem or proof of a quantum particle's existence.

References: PSp4(3) simplicity/order and PGSp4(3) extension, *An Explicit PSp4(3)-Polynomial with 3 Parameters of Degree 40*, Math. J. Okayama Univ. 53 (2011), pp.155-165. W(E6)'s index-two PSp4(3) rotation subgroup, `https://cst.temple.edu/sites/cst/files/theses4/JessieHamm.pdf`. The repo's direct Conwell A8 incidence verification is in `analysis/w33_20261028_twistor_klein_ag_codes_round13.py`.

**Next falsifier:** calculate the actual G action on `ker_F2 A / im_F2 A`; compare that eight-dimensional linear module's composition factors after restriction to common subgroups of G and A8. This is the correct invariant way to test whether there is a weaker bridge.
