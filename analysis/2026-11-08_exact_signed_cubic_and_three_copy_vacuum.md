# Exact signed cubic generators and a three-copy vacuum

The committed 45 signed tritangent terms determine an exact integral generator basis for the 27-dimensional representation. The full infinitesimal stabilizer of the associated 81-dimensional alternating tensor is (E_6\oplus\mathfrak{sl}_3). Its alternating coupling admits a concrete three-copy F-flat and D-flat point in a supplied potential. The point retains an internal (A_2) and a nine-dimensional family of physical scalar minima.

## Scope and prior work

The November 8 parallel [coherence and Ward report](PASS20261108_FIVE_FOLLOWTHROUGH_PLUS_COHERENCE.md) checked six Cartan and eight external directions. The prior [minuscule generator builder](../tools/build_e6_27rep_minuscule.py) already constructs the Chevalley representation and checks its signed cubic. The prior [native operator closure](w33_20261027_native_operator_closure.py) supplies a signed permutation to the SU(5) plus two U(1) chart. This packet solves the coefficient equations directly and proves completeness on all 81 coordinates. The input is the canonical cubic JSON, with exact equality of its signed term dictionary to the independently stored archive. It runs without the local binary generator export.

The 27-line representation and its 45 tritangent terms are classical. Manivel explains the cubic stabilizer and the (E_6+A_2) decomposition of (E_8). Baez and Pumpluen describe the related Albert algebra constructions. These supply context for the group identification. The coefficient, bracket and Hessian certificates below are calculated from the repository's actual signed coordinates. [Manivel](https://arxiv.org/abs/math/0507118) · [Baez and Pumpluen](https://arxiv.org/abs/2609.07538)

Targeted repository searches covered the complete cubic stabilizer, root generators, the canonical and archived cubic, Cartan subspaces, and the family anomaly. The previous 35-commit parallel review is recorded in the magnetic completion manifest. The repository and remote matched at intake. Manuscript text reading continued through pages 149–150, covering reversal and cubic-gate ledger entries. Full weekly patch reading remains incomplete.

## The exact coefficient kernel

For each matrix entry (T_{ij}), replace one factor (x_i) in each tritangent term by (x_j). Collect coefficients of sorted output monomials. The resulting linear map is the derivative of the cubic under (x\mapsto (1+tT)x).

| Representation and tensor | Matrix variables | Coefficient rows | Exact rank | Kernel dimension |
|---|---:|---:|---:|---:|
| 27 and symmetric cubic | 729 | 2475 | 651 | 78 |
| 81 and alternating three-form | 6561 | 48870 | 6475 | 86 |

The first rank comes from rational elimination. Back substitution gives six diagonal generators and 72 one-dimensional root spaces. Commutators with the diagonal basis give exact root characters. Pairing roots by transpose constructs the simple coroots. Their Cartan matrix is of type (E_6), and the simple matrices satisfy the Chevalley and Serre relations. The 36 transpose pairs and six diagonals give the compact real form in the standard Hermitian metric. The machine certificate serializes all 78 generators as integer triples `(row,column,value)`.

The 81-dimensional calculation uses exterior signs when sorting monomials and discards repeated exterior factors. Its 270 ordered-coordinate wedge terms reproduce all 1,620 signed bracket records when antisymmetrized. Elimination modulo 101 gives rank 6475, a lower bound over characteristic zero. The 78 exact lifts (T\otimes I_3) and eight (I_{27}\otimes S), (\operatorname{tr} S=0), are independent and annihilate every integer coefficient row. Together these prove equality and exhaust the infinitesimal kernel. A separate V8 calculation uses descending pivots modulo 103 and obtains both ranks. On the authorized desktop, a numerical comparison with the older local generator export gives mutual span errors below (3.2\times10^{-15}).

## What the invariant permits

The 27-dimensional Cartan action restricts degree-three weight-zero candidates to the 45 tritangent supports. Root constraints have rank 44 on their symmetric monomials and rank 45 on their exterior monomials. The symmetric cubic is unique up to scale and the alternating cubic on the 27 has dimension zero.

For one commuting 81-component scalar, external SL(3) invariance at cubic order would use its determinant tensor. Commuting the scalar factors then requires an alternating tensor on the internal 27, which the exact calculation excludes. The native alternating three-form instead gives the nonzero trilinear (W=T(X_1,X_2,X_3)) on three independent copies. The ordered bracket and wedge contraction agree on an independent integer-field test. The three-copy structure is present in the parallel report's three distinct columns.

For a left-handed Weyl 81, the cubic trace on the E6 Cartan vanishes identically. Conjugacy of the regular semisimple elements and polarization extend the result to the E6 anomaly tensor. The family probe (\mathrm{diag}(1,1,-2)) gives trace `-162`, or 27 times the fundamental trace. Mixed cubic terms vanish by tracelessness. The conjugate decuplet cancels that family trace, as established by Pass 11613 and the October 1 spectator work. Here it is an independent check in the reconstructed tensor action. The vacuum below uses three bosonic copies. A chiral supersymmetric completion with three such copies would require an anomaly inventory for their fermionic partners. For related nonperturbative E6 dynamics and global family anomaly matching, see [Goh et al.](https://arxiv.org/abs/2505.07931).

## A balanced three-copy point and its physical zero modes

Take the supplied positive sum of the F-term, Hermitian moment-map, and Gram residual squares. The Gram term fixes (X^\dagger X=3I_3) in the chosen field units. The holomorphic part is (W=T(X_1,X_2,X_3)). Its F-equations are the three pairwise signed brackets.

The all-plus disjoint triad search gives 1,440 unordered support triples whose pairwise brackets vanish in this chart. Choose the first in lexicographic order, using the flat index (3i+a) for internal line (i) and external coordinate (a).

```
X1 support = (0,52,80)
X2 support = (5,37,75)
X3 support = (26,40,54)
```

The three columns have disjoint support and norm squared three. Direct integer contractions give zero F and all 86 zero D moments. The full stabilizer of the point has complex dimension eight and nondegenerate Killing form. It lies entirely inside E6. Its simple Cartan matrix is (A_2), and the internal 27 restricts to nine singlets, three triplets and three conjugate triplets. This particular vacuum therefore leaves an internal compact SU(3) algebra. An electroweak sector would require a different symmetry-breaking pattern or further structure.

At zero residual the Hessian kernel is the kernel of the linearized constraint map for any strictly positive coefficients on the three squares. Exact real and imaginary block ranks are 204 and 195 on the 486 real coordinates. The kernel has dimension 87, including 78 gauge orbit tangents. The species U(3) symmetry acts on the copy index and preserves the energy. Its nine independent directions modulo gauge fill the remaining kernel. Thus the nine directions extend to actual symmetry-related minima. Adding a cubic F-term and the full D-term to the Gram potential drastically restricts the Stiefel degeneracy, while an isolated vacuum still requires a mechanism that fixes the species orientation.

The construction supplies the Hermitian metric, the action terms, their positivity and the field scale. A supersymmetric realization of the Gram term, a complete chiral matter inventory, threshold effects, radiative stability, and a physically selected vacuum remain open.
