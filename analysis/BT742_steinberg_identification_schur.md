# BT742 — chart81 = Levi E4 = Steinberg; Selector Uniqueness IS Schur's Lemma

The selector program (BT696–BT741) has been matching two 81-dimensional
sectors: the chart-overlap eigenvalue-8 sector and the Levi Hodge/cycle
sector.  BT742 identifies BOTH as the Steinberg representation of the
substrate automorphism group, turning the program's uniqueness and
full-rank theorems into corollaries of Schur's lemma.

## GAP input

```text
CharacterDegrees(CharacterTable("U4(2)")) =
  [[1,1],[5,2],[6,1],[10,2],[15,2],[20,1],[24,1],
   [30,3],[40,2],[45,2],[60,1],[64,1],[81,1]]
```

U4(2) = PSp(4,3) has EXACTLY ONE irreducible of degree 81 — the Steinberg
representation St, with dim = q^(n^2) = 3^4 = 81.  (Minimal nontrivial
degree 5 also re-proves the BT739 forcing argument.)

## Computation (pure fixed-point counting, exact integers)

Enumerated all 25920 point-permutations of PSp(4,3) by BFS over the 40
symplectic transvections.  Because Sp(4,3) preserves the point/line
bipartition, orienting all Levi flags point->line makes the signed and
unsigned flag modules coincide, so the cycle-space character is

```text
chi_E4(g) = #fixed_flags(g) - #fixed_Levi_vertices(g) + 1.
```

Results:

```text
chi_E4(1)            = 81
<chi_E4, chi_E4>     = 1      cycle space IRREDUCIBLE
<chi_E4, 1>          = 0
<chi_chart, chi_E4>  = 1      St appears exactly once in chart module
<chi_chart, chi_chart> = 12   chart module commutant
<chi_flag, chi_flag>   = 8    flag module commutant
<chi_point, chi_point> = 3    W33 scheme rank (SRG)
```

## Theorem chain

1. The Levi cycle space is irreducible of dimension 81, hence **the
   Steinberg representation** (GAP uniqueness).
2. St appears exactly once in the 240-chart permutation module.  The HH^T
   eigenspace dimensions are {1, 24, 75, 81, 24, 35}; eigenspaces are
   G-invariant, and only the 81-dimensional one can contain an 81-dim
   irreducible.  Hence **chart81 = St**.
3. Schur: `dim Hom_G(chart81, LeviCycle) = dim Hom(St, St) = 1`.
   - The chart81 -> LeviE4 bridge intertwiner is **unique up to scalar**:
     BT720's selector-orbit uniqueness is Schur's lemma in disguise.
   - Any nonzero equivariant map chart81 -> cycle space is **injective**:
     BT739's full-rank theorem is also Schur's lemma.
4. The substrate identity 81 = q^mu = Steinberg dimension (BT538) is not a
   dimension coincidence: both protected 81-sectors are THE Steinberg
   module of Sp(4,3) = W(E6).

## Why this matters

Steinberg modules are the cohomologically distinguished representations of
finite groups of Lie type (the top cohomology of the Tits building; the
unique irreducible projective module in defining characteristic).  The W33
program's "protected memory H_1 = 81" is now literally the Tits-building
cohomology of the substrate group.  Every future 81-sector found in the
substrate must be St — there is no other 81-dimensional option.

## Boundary

The chart module commutant is 12 and the flag commutant is 8 (neither
multiplicity-free): full decompositions into the U4(2) degrees
{1,5,6,10,15,20,24,30,40,45,60,64,81} remain to be pinned classwise.
Open: realize the Steinberg module explicitly as the top homology of the
Tits building of Sp(4,3) (apartments = W(3,3) hyperbolic lines structure)
and transport the BT740 braid functor along it.
