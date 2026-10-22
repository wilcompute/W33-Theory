# Faithful 20-qutrit logical symmetry from W(3,3) (2026-10-22)

## Exact finite theorem and limits

Consider the **point-coordinate** ternary CSS code from the 40-by-40 noncollinearity matrix B of W(3,3). Its row code C has rank 10, satisfies C subset C^perp, and defines a [[40,20,4]]_3 CSS code (distance proved by the preceding all-q Pascal CSS work). Its logical X-label vector space is Q=C^perp/C, with dim_F3 Q = 20.

Every projective symplectic incidence automorphism g in PSp(4,3) permutes the 40 coordinates, fixes B, and hence preserves C and C^perp. It induces a linear map rho(g) on Q. This is a **well-defined group homomorphism** rho:PSp(4,3)->GL(20,3).

The new exact computation in \`analysis/w33_20261022_pascal_css_logical_transvection_jordan.py\` gives, for one nontrivial symplectic transvection, the logical Jordan type

    J_1^3 + J_2^4 + J_3^3,

so rank(rho(t)-I)=10 and rho is nontrivial. Since PSp(4,3) is simple, ker(rho) is either trivial or the whole group. It is not the whole group. Therefore

    rho: PSp(4,3) -> GL(20,3) is faithful.

This conclusion uses the **projective** group of order 25920. The symplectic double-cover Sp(4,3) has a central -I acting trivially on projective points. Do not identify that double cover with the distinct W(E6) extension merely because both have order 51840.

Since the X and Z CSS stabilizer spaces are the same C, physical coordinate permutations preserving C normalize the stabilizer. Thus this faithful action on logical X labels has a corresponding contragredient action on logical Z labels, giving a symplectic logical Pauli-label transformation. Every such coordinate permutation is an **abstract encoded Clifford operation**.

## Physics firewall

"Abstract encoded Clifford operation" does not imply a depth-1 local gate in an optical device. A potentially nonlocal physical permutation of 40 optical modes may have nontrivial routing, timing, and error costs. The faithful 20-dimensional representation does not establish a non-Clifford gate, a magic-state injection protocol, threshold, universality, or a physical spacetime theory.

The 20-dimensional Q here is **not** the 81-dimensional Steinberg/Hodge module of the W33 point-line Levi flag graph, nor the older 240-edge CSS code. Identifying their carrier spaces merely because both use W33 would be an error.

## Independent follow-ups

- Give explicit 20-by-20 matrices over F3 for a minimal generating set of PSp(4,3), with certified group order 25920.
- Compute the irreducible/modular composition factors and invariant bilinear forms of Q.
- Compare logical gate word length against physical Witting/Holonet optical routing depth.
- Search for code automorphisms outside PSp(4,3) and determine the full permutation automorphism group of C.
- Verify this representation against published ternary Veronese/projective Reed-Muller coding literature.
