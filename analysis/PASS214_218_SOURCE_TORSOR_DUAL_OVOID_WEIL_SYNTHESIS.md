# Passes 214–218 — Source Torsor, Dual Ovoid Carrier, and Weil Shadows

Status: **complete and GAP-verified**. These five passes continue directly
from the canonical Pass-212 carrier and the corrected Pass-213 group ledger.
Every new mathematical experiment and certificate is owned by GAP; the
Python files are launch/parser regressions only.

## 1. The four slots exist on the source line (Pass 214)

For every active pair `(Sigma,L)`, the stabilizer is a faithful `S4` on the
four points of `L`. Its intrinsic kernel on the three complementary `2+2`
partitions is the normal Klein group

\[
K_{\Sigma,L}=\ker(S_4\to S_3)\cong V_4.
\]

GAP checks all 1,080 active pairs and proves that `K` acts regularly on the
source line. After choosing the carrier point `p`, the four points are the
identity plus the three nonidentity double transpositions. Each nonidentity
element is labelled by its two cycles, exactly one complementary
pair-partition.

This is the missing canonical regular *source-line* `V4` torsor. It is not a
canonical assignment to four named runtime roles: the residual `S3` permutes
the three nonidentity labels. It also does not contradict Pass 212's
`1+1+2` action, which lives on a completion line under a different `V4`.

## 2. The 4320 carrier reaches the local-axis sign cover (Pass 215)

For a sheet `(Sigma,L,p)`, let `M` be the unique spread line through `p`.
Then `{L,M}` is one endpoint of a local pencil-octahedron axis at `p`:

\[
(\Sigma,L,p)\longmapsto(p,\{L,M\}).
\]

The complete equivariant tower is

\[
4320\xrightarrow{18:1}240\xrightarrow{2:1}120.
\]

The first fibre is `18=2*9`: either endpoint line may be external and nine
spreads contain its owner. The second map quotients by endpoint complement,
a fixed-point-free `C2` deck map that centralizes the code action and generates
the extended order-103680 action. Thus the exact minimal sign sheet is

\[
C_2\longrightarrow240\text{ local-axis endpoints}\longrightarrow120\text{ axes}.
\]

Via Pass 123's chosen quadratic-space/chamber isometry, these endpoints and
axes may be represented by signed E8 roots and root lines. That representation
is a gauge, not another equivariant theorem. The two `W(E6)` lenses remain
nonconjugate: the W33 code embedding is transitive on the `240/120`
endpoint/axis carriers, whereas GAP independently
reconstructs the standard reflection embedding `W(E6)<W(E8)` with signed
root orbits

\[
1^6+27^6+72
\]

and root-line orbits `1^3+27^3+36`. Therefore composing with the existing
chamber-coordinate E8 lift is an explicit gauge, not an equivariant map for
the standard `E6 x A2` embedding. A trivial phase sheet cannot repair an
orbit-fingerprint obstruction.

## 3. The dual carrier changes type from spreads to ovoids (Pass 216)

Exact-cover enumeration gives:

| geometry | spreads | ovoids | noncollinear span |
|---|---:|---:|---:|
| `W(3,3)` | 36 | 0 | 4 |
| `Q(4,3)` | 0 | 36 | 2 |

Hence

\[
\Delta_{SO}(G)=\#\operatorname{Spreads}(G)-\#\operatorname{Ovoids}(G)
\]

is a convention-free duality-odd spread--ovoid imbalance with values
`+36/-36`; it is not an Euler characteristic. Under incidence duality, a
Pass-209 common-zero W spread becomes a Q ovoid on the dual point set.

For each Q ovoid, 30 external points form 15 two-point owner fibres. Their
15 owner blocks form a `2-(10,4,2)` design. They are indexed equivariantly by
the 15 `S6` duads, each duad selecting four of the ten `3+3` bisections. The
two points in a fibre are noncollinear, have
the owner block as their full common perpendicular, and span exactly the
pair. This yields the complete bijection

\[
(\Omega,x,m)\longmapsto(x,\Omega\cap m,\tau_\Omega(x))
\]

and the tower

\[
4320=36\cdot15\cdot2\cdot4,
\qquad S_6>C_2\times S_4>S_4>S_3.
\]

The central `C2` swaps the owner mates, so that fibre is not an absolute
left/right chirality label. The Q carrier is exactly Pass 212 retyped by
incidence duality, not a second independent carrier. The spread/ovoid
equivalence under the Klein correspondence is the standard symplectic
spread framework described by [Ball and Zieve](https://arxiv.org/abs/0810.2839).

## 4. Full spread-source carrier closure is unique at q=3 (Pass 217)

For `W(3,q)`, the source and target sizes are

\[
|X_q|=S(q)q(q^2+1)(q+1),\qquad
|P_q|=q^3(q+1)^2(q^2+1),
\]

so equality requires `S(q)=q^2(q+1)` spreads. The regular symplectic spread
orbit has size

\[
R(q)=\frac{q^2(q^2-1)}2,
\qquad
\frac{R(q)}{q^2(q+1)}=\frac{q-1}{2}.
\]

GAP constructs the regular orbit at `q=2,3,4,5,7`:

| q | regular orbit | required | all spreads | owner candidates per sheet |
|---:|---:|---:|---:|---:|
| 2 | 6 | 12 | 6 | 0 |
| 3 | 36 | 36 | 36 | 1 |
| 4 | 120 | 80 | not classified | 0 |
| 5 | 300 | 150 | not classified | 1 |
| 7 | 1176 | 392 | not classified | 1 |

At the tested odd anchors `q=3,5,7`, the regular-spread owner map is an
equivariant path cover of degrees `1,2,3=(q-1)/2`. Only `q=3` is bijective.
At `q=2`, exhaustive
enumeration gives too few spreads; for every `q>=4`, the regular orbit alone
already exceeds the required count. This proves the unique prime-power
count closure at `q=3`. The executable scope does not classify higher-q
nonregular spreads or prove the odd candidate formula beyond the displayed
anchors. The regular-spread stabilizer input is recorded in
[Crnković--Hawtin--Švob, Lemma 4.2](https://arxiv.org/abs/2105.05833); the
witness emits the corresponding symbolic PSp orbit--stabilizer quotient.

## 5. q=5 is the F4 Weil pair; q=7 splits with the Weil fingerprint (Pass 218)

At `q=5`, the binary shadow is irreducible of dimension 24 but not
absolutely irreducible:

\[
\operatorname{End}_G(H_5)=\mathbb F_4,
\qquad J^2+J+1=0.
\]

Over `F4` it splits as two nonisomorphic, absolutely irreducible,
Frobenius-conjugate self-dual modules `12a+12b`. CTblLib finds the unique
degree-12 pair and AtlasRep supplies `S45G1-f4r12aB0`. Thus `H5` is the
restriction of scalars of a degree-12 Weil module, not Golay/Leech.

At `q=7`, the 48-dimensional shadow is decisively split:

\[
H_7=U\oplus U^*.
\]

The complete submodule dimensions are `[0,24,24,48]`; the socle has
dimension 48, the radical is zero, and GAP constructs a commuting rank-24
idempotent. The two absolute 24s are nonisomorphic duals, totally singular,
and perfectly cross-paired by the nondegenerate rank-48 form of Arf invariant
zero.

Their transvection values are

\[
\frac{-1\pm5\sqrt5}{2}\quad(q=5),\qquad
\frac{-1\pm7\sqrt{-7}}{2}\quad(q=7),
\]

giving the exact characteristic-two Weil fingerprint of degree `(q^2-1)/2`
described by [Szechtman](https://arxiv.org/abs/math/0212378). The installed
databases independently label q=5; q=7 is reported at exact fingerprint
level because no local characteristic-two `S4(7)` table/representation is
available.

## Reproduce

```bash
gap -q analysis/w33_pass214_source_line_v4_torsor.g
gap -q analysis/w33_pass215_carrier_double_six_signed_e8.g
gap -q analysis/w33_pass216_q43_dual_ovoid_carrier.g
gap -q analysis/w33_pass217_w3q_owner_spread_uniqueness.g
gap -q analysis/w33_pass218_weil_shadow_split.g
python3 -m pytest -q \
  tests/test_pass214_source_line_v4_torsor.py \
  tests/test_pass215_carrier_double_six_signed_e8.py \
  tests/test_pass216_q43_dual_ovoid_carrier.py \
  tests/test_pass217_w3q_owner_spread_uniqueness.py \
  tests/test_pass218_gap_weil_shadow_split.py
```

Generated certificates are in `data/w33_pass214_*.json` through
`data/w33_pass218_*.json`. The five witnesses collectively distinguish
canonical objects, coordinate gauges, duality type changes, and database
boundaries rather than promoting count coincidences into identifications.
