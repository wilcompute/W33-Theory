# Passes 1950–1954 — U6 rigidity, five minimum-shell geometries, a sound frame ABI, SL3(Z), and the internal Z6 boundary

All five requested fronts were executed. The aggregate packet verifies **35/35** assertions.

## 1950 — U6 collision graph

The 28 primitive shards of the Pass-1939 super-shard form a complete weighted collision graph: 378 edges, 3,163,606 shared-syndrome-group incidences, 5,389,182 cross-shard collision edges, and 125 distinct edge labels. Its weighted automorphism group is trivial. The stabilizer of the fixed W33 edge has order 216 and 230 orbits on all 28,441 unordered pair charts. Thus the present numeric-minimum partition has no useful symmetry compression. Global U6 remains open.

## 1951 — minimum shell

The 540 weight-four primal words are exactly the 540 frame matchings. Exceptional S6 splits them into five orbits:

| geometry | split type | orbit | stabilizer |
|---|---:|---:|---:|
| residual tetrahedral boundaries | `(4,0,0)` | 15 | 48 |
| mixed residual-triangle flags | `(1,3,0)` | 120 | 6 |
| pair-coordinate parallel tetrads | `(0,4,0)` | 45 | 16 |
| pair rectangles | `(0,4,0)` | 180 | 4 |
| pair-phase bridges | `(0,2,2)` | 180 | 4 |

The nominal 225 pair-only words therefore split as 45+180. The 45 parallel tetrads partition all 180 pair coordinates once. The 15 residual words are tetrahedral boundaries on four-subsets of six.

## 1952 — frame-to-duad ABI and sound lex

The binary matrix `B[f,d]`, half the residual-row multiplicity among the four edges of frame `f`, has shape 540 by 15. Its row weights are `1^180 2^225 3^120 6^15`, every column sum is 72, and its rank is 15 over Q and F2, F3, F5, F7. All 720 exceptional-S6 equivariance equations hold.

A proper 14-colouring and one geometric image certify a corrected prefix-equality lex leader: one feasible assignment is removed and a symmetry-equivalent representative survives. A genuinely unpinned nine-colour MILP with no value precedence returned `TIME_LIMIT/UNKNOWN` after 20 seconds. Hence `chi(H)=9` remains open.

## 1953 — arithmetic closure

Exact words of length 11 or 12 in the Gaussian quarter-turn `R4` and Eisenstein sixth-turn `U6` produce all six elementary transvections `E_ij(1)`. Therefore

`<R4,U6> = SL3(Z)`.

The group is arithmetic of index one, not thin, and reduces onto `SL3(F_p)` for every prime.

## 1954 — the two order-six actions

The internal endomorphism C6 has complex-character multiplicities `(150,45,0,0,0,45)`. The E8 Coxeter `C^5` action on the 240 roots is 40 copies of the regular C6 representation, with multiplicities `(40,40,40,40,40,40)`. No injective, surjective, or bijective full-carrier C6-intertwiner exists.

On the shared V9 multiplicity space, the internal `mu3` commutator with the exceptional-S6 quarter-turn has rank two, hence rank 18 after tensoring with V9. Multiplicity-freeness also forces every PSp-equivariant linear map between the 90 and the rational 15, 24, 30, or 81 blocks to vanish.

## Boundary

Pass 1944's withdrawal is adopted. The internal order-six action is not a homological flux quantum, electric-charge derivation, QCD-colour group, generation label, or neutrino assignment. Here “colourless” means only trivial under this internal `mu3`; it is not a theorem about Standard Model colour. No canonical E8-to-coexact subquotient map is known.
