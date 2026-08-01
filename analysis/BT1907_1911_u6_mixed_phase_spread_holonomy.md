# Passes 1907–1911 — U6 shard execution, complete mixed enumerator, complete S6 phase poset, Gaussian phase cuts, and stabilizer-weighted holonomy

## Executive result

All five requested fronts were executed. Four close as exact finite theorems. The fifth, the global sixth-order decoder coefficient, remains behind an explicit data-volume boundary, but its literal external-memory pipeline is now exercised on a complete nontrivial shard rather than existing only as unrun code.

The aggregate packet verifies **48/48** frozen assertions.

## Pass 1907 — exact U6 shard execution and global resource theorem

The complete fixed-coordinate chart contains

\[
\binom{239}{5}=6{,}230{,}484{,}547
\]

weight-six errors. A lossless 16-byte `(syndrome, combinadic rank)` stream therefore occupies exactly

\[
99{,}687{,}752{,}752\text{ bytes},
\]

and the external-partner bitmap occupies

\[
778{,}810{,}569\text{ bytes}.
\]

The literal shard fixing coordinates `0,1,2` was executed over all

\[
\binom{237}{3}=2{,}190{,}670
\]

remaining triples. It has `1,830,866` syndrome groups, `1,531,651` singleton groups, maximum multiplicity `9`, and `447,447` internal collision edges. Exhaustive comparison with every weight-0, weight-2, and weight-4 syndrome marks `245,161` lower-shadow groups and leaves exactly `1,349,896` nonlower singleton groups **within the shard**.

A shard singleton is not yet a global singleton: it may collide with another chart shard or with a partner omitting the fixed coordinate. Consequently no `U6` coefficient is promoted. The remaining boundary is precisely the merge of all chart shards and all weight-4/6/8/10/12 complementary codeword marks.

## Pass 1908 — complete 20+180+40 split weight enumerator

All `156` exceptional-S6 residual orbits were contracted against all `2^30` fiber assignments and merged. The resulting exact trivariate enumerator contains

\[
2^{45}=35{,}184{,}372{,}088{,}832
\]

words in only

\[
\boxed{7{,}355}
\]

nonzero cells of the nominal `21 x 181 x 41 = 155,841` array.

It reproduces all 91 coefficients of the previously frozen ordinary dual weight enumerator and satisfies

\[
H(r,p,h)=H(20-r,180-p,40-h),
\]
\[
H(r,p,h)=H(r,p,40-h),
\]
\[
H(r,p,h)=H(20-r,180-p,h).
\]

These are not accidental histogram symmetries. The row code contains a literal complement subgroup

\[
\boxed{C_2\times C_2}.
\]

The XOR of the first 30 fiber generators flips exactly the 40 phase coordinates. The XOR of the final 15 residual generators flips exactly the 20 residual plus 180 pair coordinates. Their sum is the all-one word. Neither the residual-20 mask nor the pair-180 mask alone lies in the code.

## Pass 1909 — all 56 exceptional-S6 subgroup classes and the two J's

All conjugacy classes of subgroups of `S6` were enumerated independently. Exact class algebras recover every irreducible character, its Frobenius–Schur indicator, and its multiplicity in the restricted 24-, 90-, and 114-dimensional carriers.

Among the 56 subgroup classes:

- `26` admit an invariant complex structure on the 24-sector;
- `22` admit one on the 90-sector;
- `12` admit one on the full 114-sector;
- all `56` admit the paired-natural-`V9` complex structure.

The complete calculation resolves the relation between the two known complex structures. Under `A6`, let

- `A` be the natural `V9` in the 24-sector;
- `B` be the natural `V9` in the 90-sector;
- `C` be the sign-twisted `V9` in the 90-sector.

The sign is trivial on `A6`, so `B` and `C` become equivalent. The exceptional-S6 paired structure rotates `A <-> B`; the restriction of the canonical `PSp(4,3)` structure rotates `B <-> C`. They are distinct adjacent-plane rotations. Their commutator is the `A <-> C` rotation, so together they generate

\[
\boxed{\mathfrak{so}(3)}
\]

on the real multiplicity space `R^3`. They neither coincide nor form a quaternionic pair.

This dovetails with the q=3 parallel theorem: the outer `Z/2` of `W(E6)` acts as complex conjugation on every complex-type `PSp(4,3)` irreducible. This is not a general `PSp(4,q)` rule: q=5 has no complex-type irreducibles although outer fusion still occurs. Finite tables at q=3,4,5,7,9 support complex type precisely for q=3 mod 4. The signed oriented-edge module realizes the degree-45 pair; permutation modules are real, so orientation is necessary for the substrate phase.

## Pass 1910 — projective KG blindness and sound phase-aware spread cuts

The paired Gaussian `V9` lattice has 60 minimal vectors, arranged as 15 projective lines with graph

\[
KG(6,2)=\operatorname{SRG}(15,6,1,3).
\]

Projectivization quotients the central `C4` unit torsor. Therefore unsigned `KG(6,2)` incidence cannot detect complex conjugation or chirality: the line graph is phase-blind.

The sound lift uses oriented variables `y[l,k,c]`, where `k in Z4` records the Gaussian unit. Define

\[
\Phi(c)=\sum_l\bigl(y[l,1,c]-y[l,3,c]\bigr).
\]

Conjugation sends `k -> -k`. Hence a certified transported color pair obeys

\[
\Phi(c')=-\Phi(c),
\]

and a transported fixed color obeys

\[
\Phi(c)=0.
\]

These are exact linear equalities. They replace guessed cardinality cuts.

For a spread `K10`, the only unconditional color-count equation is

\[
\sum_{c=1}^{9}|C_c\cap K_{10}|=45,
\]

so the mean is 5. The value 13 is attained in certified covers. A direct search for an intersection at least 14 returned `UNKNOWN`, so the maximum remains undecided. In particular the false `<=5` bound is excluded everywhere in this packet.

## Pass 1911 — stabilizer-weighted primitive holonomy

Fourier inversion of the four `C4` Artin–Ihara factors yields canonical stabilizer-weighted primitive quotient-cycle counts `W_{n,h}`. The full 90-state representation splits by character dimensions

\[
26+20+24+20=90.
\]

The common natural-`V9` channel splits as

\[
12+8+8+8=36,
\]

and its Hashimoto complement as

\[
14+12+16+12=54.
\]

The exact recursion

\[
T_k(n)=\sum_{d\mid n}d\sum_{h\in\mathbb Z_4}
W_{d,h}\,\mathbf 1[(n/d)h=k]
\]

reconstructs every twisted trace through length 32.

This separates the shared 36-dimensional `V9` graph channel from the 54-dimensional complement. It cannot distinguish `A24` from `A90`, because both maps factor through the same `V9` source. Their distinction is representation-theoretic—orthogonal embeddings and outer conjugation—not graph-holonomic.

## Evidence boundaries

- The complete split enumerator, subgroup phase poset, Gaussian cut theorem, and weighted holonomy ledger are exact.
- The global `U6` coefficient is not claimed. A complete 2,190,670-error shard and the exact full resource/merge contract are certified.
- Applying the phase-aware cut schema to the resolution solver requires a literal transport between Gaussian chart variables and solver colors.
- Weighted holonomies are finite graph-of-groups invariants, not physical optical phases or a Hamiltonian evolution law.
