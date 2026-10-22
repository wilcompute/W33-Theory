# Pascal CSS: transvection action on the logical quotient (2026-10-22)

## Status and prior-art boundary

**Finite computation:** reproduced for primes 2, 3, 5 and 7.  
**Conjecture, not a theorem:** uniform general-prime Jordan block formula below.  
**Algebraic fact:** for prime p, the symplectic noncollinearity row code is the homogeneous degree-(p-1) projective polynomial evaluation code on PG(3,p). In the p=3 case this is precisely the repository's *previously documented* quadratic Veronese identification (see \`analysis/w33_pass5744_5751_quadratic_code_overlays.py\`). The new target here is the induced action of a point transvection on the **CSS logical quotient**, not the existing polynomial identification. This project does not claim novelty over the modular representation theory literature without further review.

The input CSS construction and proof of its distance are already present in
\`analysis/w33_20261022_allq_pascal_CSS_exact_distance.py\`.
Do not conflate this point-coordinate CSS code with the older 240-edge or 160-flag homological CSS codes.

## Definitions

Let V = F_p^4 have nondegenerate alternating form \`omega\`; let P = PG(3,p) consist of its one-dimensional subspaces.

\`\`\`
B[x,y] = 1 if omega(x,y) != 0; otherwise 0  (in F_p)
C = rowspace(B)
Q = ker(B)/C = C^perp/C
n = (p+1)(p^2+1)
r = rank(B) = binom(p+2,3)
dim(Q) = n-2r = (2p^3+p+3)/3.
\`\`\`

Let \`w\` represent any projective point, and let the symplectic transvection
\`tau_w(x) = x + omega(x,w) w\` act on projective coordinates. Because it preserves \`B\`, it preserves \`C\` and \`ker(B)\`, inducing \`T\` on \`Q\`. The action on the logical CSS X/Z label spaces is by the coordinate permutation and its dual.

The program calculates \`rank((T-I)^k|_Q)\` *without selecting a quotient basis*: for any matrix \`D=P_tau-I\`, and row basis \`N\` of ker(B),

\`\`\`
rank_Q(D^k) = rank_Fp([basis(C); N D^k]) - dim(C).
\`\`\`

The Jordan multiplicities follow from second differences of this rank sequence. All matrices use exact modular Gaussian elimination, not floating point rank thresholds.

## Verified census

| p | n | rank(B) | dim Q | ranks of (T-I)^k, k=0..p | nonzero block multiplicities |
|---:|---:|---:|---:|---|---|
| 2 | 15 | 4 | 7 | 7,2,0 | J1:3, J2:2 |
| 3 | 40 | 10 | 20 | 20,10,3,0 | J1:3, J2:4, J3:3 |
| 5 | 156 | 35 | 86 | 86,60,37,18,5,0 | J1:3, J2:4, J3:6, J4:8, J5:5 |
| 7 | 400 | 84 | 232 | 232,182,135,92,55,26,7,0 | J1:3, J2:4, J3:6, J4:8, J5:10, J6:12, J7:7 |

For each verified prime, \`B^2=0 mod p\`, \`rank(B)=binom(p+2,3)\`, the transvection preserves B, and \`(T-I)^p=0\` on Q.

## Conjectural uniform pattern

Write J_j for an indecomposable unipotent Jordan block of length j over F_p. The observed pattern is

\`\`\`
Q|_{<tau_w>}  ~  J1^3 + (sum_{j=2}^{p-1} J_j^(2j)) + J_p^p.
\`\`\`

Consequences **if proved**, for every prime p:
- \`dim ker(T-I) = p^2+1\`
- \`rank(T-I) = p(p-1)(2p-1)/3\`
- \`rank((T-I)^(p-1)) = p\`
- \`dim Q = (2p^3+p+3)/3\`

These identities pass at p=2,3,5,7; they are *not* promoted to general theorems by four samples.

## Why a polynomial model should help prove it

Fermat's theorem gives the identity

\`\`\`
B[x,w] = omega(x,w)^(p-1).
\`\`\`

As w varies, nondegeneracy of omega supplies all linear forms. Since p-1<p, polarization allows powers of linear forms to span every homogeneous polynomial of degree p-1 in four variables; the degree-(p-1) evaluation map on PG(3,p) is injective. Hence the code C is the image of Sym^(p-1)(V*) and has the stated binomial rank.

A transvection on V has one 2-dimensional unipotent block and two fixed directions. Thus the restricted **C module** has a tractable decomposition from degree partitions:
\`\`\`
C|_<tau> ~  sum_{j=1}^p (p-j+1) J_j.
\`\`\`
The missing proof step is to derive the extension/gluing in
\`0 -> C -> ker(B) -> Q -> 0\`. Knowing the separate C and ambient permutation-module Jordan types alone does **not** determine Q; this is why the general formula remains conjectural.

## Replication

\`\`\`bash
python analysis/w33_20261022_pascal_css_logical_transvection_jordan.py
pytest -q tests/test_w33_20261022_pascal_css_logical_transvection_jordan.py
\`\`\`

## Physical boundary

The action is a genuine symplectic incidence automorphism on quantum **logical labels**, not a demonstration of an experimentally realizable gate or a universal quantum computer. A projective-point permutation implements the associated logical Clifford operation only if the physical platform can enact that permutation while respecting the code. This calculation says nothing by itself about non-Clifford injection, thresholds, fault-tolerant locality, the Standard Model, or a theory of everything.

## Five independent follow-ups

1. Prove or disprove the general-prime logical Jordan formula using the projective polynomial filtration and the extension class of C inside ker(B).
2. Compute the full Sp(4,p) character/Brauer fingerprints of Q and its irreducible constituents, beginning with p=3.
3. Determine which point-coordinate transvections admit low-depth geometrically local implementations in the photonic Holonet compiler, including explicit overhead.
4. Construct the prime-power (t>1) field-descent analogue and check whether Jordan packet multiplicities depend on Frobenius twisting.
5. Benchmark the family against published projective Reed-Muller/finite-polar-space quantum codes, separating genuine new representations from rephrasings.
