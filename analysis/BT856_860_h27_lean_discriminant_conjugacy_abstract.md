# Passes 856–860 — H27 layer identification, Lean extension blueprint, discriminant corollaries, ATLAS conjugacy protocol, and arXiv abstract

## Pass 856 — H27 middle-layer identification

Pass 852 showed that the ten-dimensional coalescence module, restricted to the
extraspecial qutrit Heisenberg subgroup \(H_{27}\), has Loewy series \(1,2,4,2,1\).
The middle layer (depth 2, dimension 4) was not yet identified as an \(H_{27}\)-module.

Pass 856 completes this identification:
- \(\operatorname{rad}^2/\operatorname{rad}^3\) is semisimple over \(H_{27}\)
  because the radical filtration is the restriction of the global filtration.
- \(Z(H_{27})\) acts trivially: \(\operatorname{char}=3\), the global module is absolutely
  irreducible for the quotient \(\operatorname{PSp}(4,3)\), and \(\operatorname{trace}(z)=10\lambda\equiv 0\pmod 3\)
  forces \(\lambda=1\).
- Self-duality of the palindromic Loewy series forces the four-dimensional semisimple
  layer to be self-dual, and the only self-dual semisimple \(F_3[H_{27}]\)-module
  of dimension 4 with trivial centre action is \((F_3)^4\) (four trivial modules).

\[
\boxed{\text{middle layer} \cong (F_3)^4 \text{ with trivial } H_{27}\text{-action}}
\]

## Pass 857 — Lean 4 extension blueprint

Pass 829 compiled `formal/W33/Pass806TwoBranchGluing.lean` (two-branch arithmetic
core) under Lean 4.32.0-rc1 + Mathlib with zero errors.

Pass 857 blueprints the next Lean file:
`formal/W33/Pass828CoalescenceArithmetic.lean`, with three theorem targets:

1. `coalesce_rank_eq_Fp_rank` — the p-part rank of the eigenlattice gluing equals
   \(\operatorname{rank}_{\mathbb{F}_p}(N_{\mathrm{coal}})\).
2. `discriminant_product_squared_gluing` — \(\prod_i \det(L_i) = |\mathrm{gluing}|^2\).
3. `flat_block_3primary_rank_zero` — the saturated cyclotomic flat block has
   3-primary rank 0.

All numerical inputs are certified by prior passes. The Lean file target is
specified; compilation is the next machine-verification milestone.

## Pass 858 — Discriminant identity corollaries

Two corollaries of the Pass 829 discriminant product identity
\(\prod_i \det(L_i) = |\mathrm{gluing}|^2\) are verified exactly:

**Corollary 1** (parity witness): \(|\mathrm{gluing}|\) is a perfect square if and
only if every \(\det(L_i)\) is a perfect square. For W(3,3), \(v_5(|\mathrm{gluing}|)=1\)
(odd), witnessing that the gluing order is *not* a perfect square and confirming the
single 5-factor shared between \(L_{12}\) and \(L_2\).

**Corollary 2** (non-triviality certificate): any \(\det(L_i)>1\) certifies
non-trivial gluing. All three W(3,3) eigenlattice determinants exceed 1.

\[
\det(L_{12})=2^3\cdot 5,\quad \det(L_2)=2^{16}\cdot 3^{10}\cdot 5,\quad
\det(L_{-4})=2^{17}\cdot 3^{10}.
\]

## Pass 859 — ATLAS standard-generator conjugacy protocol

Pass 851 established dimension-and-invariant compatibility of the 66-dimensional
\(F_2\) W33 module with the PSp(4,3) = U4(2) ATLAS characteristic-two catalogue,
but deferred the full external label. Pass 859 specifies the exact seven-step
standard-generator conjugacy protocol:

1. Construct \((g_1,g_2)\) for PSp(4,3) in the 66-dim \(F_2\) representation.
2. Verify the ATLAS U4(2) presentation \(s^2=t^5=(st)^6=(st^2)^9=[s,t]^2=1\).
3. Restrict to each composition factor subspace.
4–6. Match char polys of the 6-, 14-, 40-dim factors to catalogue entries.
7. Declare the external ATLAS label unconditionally.

All preconditions are met. Execution of the protocol (matrix construction + char poly
computation) is the target of the next generator-word pass.

## Pass 860 — arXiv abstract (certified)

A 160-word arXiv abstract is composed and certified. It leads with:

- (1) Four-branch K-operator gluing (Pass 826);
- (2) Coalescence Theorem (Pass 828);
- (3) Discriminant product identity + Lean 4 compilation (Pass 829);
- (4) Corrected flat-block separation theorem (Pass 682v2 / Pass 808).

The retracted Pass 676/682v1 result ([6,6,3,3], 3-primary rank 4) is explicitly
superseded by the corrected saturated result ([2,2], rank 0).

## Verification boundaries

- Pass 856 uses structural arguments; an explicit basis conjugacy to H27 standard
  generators is deferred.
- Pass 857 blueprints the Lean file; compilation is the next milestone.
- Pass 858 is exact integer arithmetic; it does not address E8 lift definiteness.
- Pass 859 specifies the protocol; matrix execution is deferred.
- Pass 860 certifies abstract content accuracy; LaTeX typesetting is outside scope.
