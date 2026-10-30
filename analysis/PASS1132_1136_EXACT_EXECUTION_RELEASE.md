# Passes 1132–1136 — Exact Execution of All Five Fronts

Date: 2026-07-27

This release replaces the earlier planning-only layer with executed finite computations and fail-closed corpus controls.

## Pass 1132 — shifted-adjacency descendants quarantined

`D=A-I` has spectrum `11^1 + 1^24 + (-5)^15`. The historical cubic
`(t+1)((t+1)^2-36)` and its determinant descendants are retracted. The new
ledger and scanner distinguish registered historical copies, explicit corrected
contexts, and unregistered active descendants. The scanner exits nonzero on the
last class and is wired into pre-commit and CI.

Observed audit on the release fixture: five historical-signature files, all five
registered or explicitly corrected, zero active violations.

## Pass 1133 — complete three-mode functional calculus

The projectors are

- `P_11=(D-I)(D+5I)/160`, rank 1;
- `P_1=-(D-11I)(D+5I)/60`, rank 24;
- `P_-5=(D-11I)(D-I)/96`, rank 15.

Therefore every function of the point-carrier operator is

`f(D)=f(11)P_11+f(1)P_1+f(-5)P_-5`.

The genuine positive heat trace is the even one,

`Tr exp(-tD^2)=exp(-121t)+24 exp(-t)+15 exp(-25t)`.

The signed evolution `exp(-tD)` is not called a heat kernel because the negative
mode makes it grow. The trace moments begin
`40,-40,520,-520,24040,114200` and obey the exact cubic recurrence.

## Pass 1134 — all three 432 stabilizers are S5

The acting group is the full Weyl group `W(E6)=U4(2):2`, order 51840—not the
projective index-two subgroup of order 25920. Each 432-orbit stabilizer therefore
has order 120. Direct enumeration gives, for all three,

`{1:1, 2:25, 3:20, 4:30, 5:24, 6:20}`,

with trivial center, derived subgroup order 60, and abelianization `C2`. Thus each
is `S5 = SmallGroup(120,34)`. The three stabilizers are pairwise conjugate in
`W(E6)`, so the three Steinberg-bearing carriers are three isomorphic copies of
`W(E6)/S5`.

## Pass 1135 — complete cubic-kernel decomposition

The 45 cubic supports form the permutation module

`C[45] = 1 + 20 + 24`.

Subtracting this image from the exact 2240-point A2-triple carrier gives

`ker L_cubic = 13*1 + 16*6 + 5*15 + 4*15a + 21*20 + 2*24 + 9*30 + 4*60a + 10*64 + 3*81_minus + 1*90`,

of dimension 2195. In particular, all three `81_minus` copies lie in the kernel.
The cubic-support disjointness graph is independently recovered as
`SRG(45,32,22,24)` with spectrum `32^1,2^24,(-4)^20`, explaining the image
packet `1+24+20` geometrically.

## Pass 1136 — corpus identity layer

The 540 classifier now works occurrence-by-occurrence rather than assigning one
majority label to an entire file. Pass 1139 subsequently proved that the
point/line distinction was only the first layer: `PSp(4,3)` has exactly five
transitive degree-540 coset actions, one for each order-48 subgroup class at TOM
positions 77–81. The classifier and alias registry now use that complete
five-species census. Each explicit tag binds to one nearest literal occurrence,
so a tag beside one `540` cannot classify another occurrence on the same line.
Strict mode is fatal on any unresolved occurrence.

Canonical objects:

- `{540:point-nonedge}`: TOM 77, rank 25, noncollinear point pairs / `4A`;
- `{540:double-six-nonincident}`: TOM 78, rank 28, the `36*15` cubic
  nonincidence flags;
- `{540:gq42-arc}`: TOM 79, rank 27, ordered Hashimoto arcs of `GQ(4,2)`;
- `{540:outer-4c}`: TOM 80, rank 21, the restricted `W(E6)` class `4C`;
- `{540:line-nonedge}`: TOM 81, rank 32, disjoint/skew line pairs / `2D`;
- `{540:both}` and `{540:mixed}`: compatibility declarations for a genuinely
  mixed single occurrence.

The prior warning is strengthened, not withdrawn: neither the integer `540` <!-- {540:mixed} -->,
the factorization `51840=540*96` <!-- {540:mixed} -->, nor the abstract stabilizer type identifies a
carrier. The two TOM classes 78 and 81 even have the same abstract stabilizer
`C2 x S4` while defining nonisomorphic ranks 28 and 32.

The pass registry now reserves 1120–1128 for the already-merged glue track and
1132–1136 for this exact release. Draft PR #162's branch-local 1120/1121 labels
are explicitly noncanonical; its usable mathematics is imported under Pass 1135.
Pass 1139 is the exact extension of the Pass 1136 identity layer.

## Verification

- exact E8 root count: 240;
- exact W(E6) group closure: 51840 elements;
- exact A2-triple count: 2240;
- orbit census: `1,1,27x6,240,270,270,432x3`;
- all certificate checks: PASS;
- focused release tests: PASS.

Scope: exact finite algebra, finite geometry, representation characters, and
repository integrity controls. No new physical interpretation is inferred merely
from matching dimensions.
