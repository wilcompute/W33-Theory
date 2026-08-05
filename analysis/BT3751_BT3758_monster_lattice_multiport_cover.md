# Passes 3751–3758 — Monster filters, the rooted code lattice, quadratic Walsh parent, and holonomy frame

## Release status

The archive-backed exact verifier

`analysis/w33_pass3751_3758_monster_lattice_multiport_cover.py`

verifies the SHA-256 of the complete embedded implementation, reconstructs W(3,3), its forty isotropic lines, all thirty-six spreads, the 120 Fischer triples, the Miyamoto groups, the binary six-dimensional code, and every matrix used below. It reproduces the frozen semantic certificate

`6271dafcc58467d6e758cdbcc9a1b220fe21693b3ace3c727fb5b5499be60ce6`.

The focused regression passes two tests locally. The separately committed GAP workflow is self-reporting: it writes either an executed CTblLib census or a structured failure artifact to `data/PART_3751_MONSTER_U42_CLASS_FUSION_EXECUTION.json`. No unobserved Monster fusion is silently promoted.

## Eight-front result map

| front | exact outcome |
| --- | --- |
| Monster class fusion | a self-reporting GAP/CTblLib workflow publishes success or structured failure; the result remains pending until that artifact appears |
| Monster words | exact abstract class sizes, cycle fingerprints, and compressed standard-pair filters for U4(2) and U4(2):2 |
| code lattice | an even 36-dimensional Construction-A lattice with discriminant group `(Z/2)^24`, minimum norm 2, and root system `A1^36` |
| multiport factorization | the exact 36-port involution is a product of 21 pairwise commuting rational Householder reflections |
| 120-cover classification | full automorphism group U4(2):2, non-distance-regularity, subdegrees `1,2,27,36,54`, and Terwilliger dimension 55 at three large primes |
| bonkers I | the 36 ports are the nonsingular set of a `(64,36,20)` quadratic difference set, and the multiport is a principal quadratic-Walsh minor |
| bonkers II | the integral triple-incidence cokernel is `(Z/2)^5 × Z/6`, of order 192 |
| bonkers III | the nonregular S3 cover carries a canonical rank-20 four-angle tight frame on all 120 Fischer lines |

# I. Monster-search filters become objectwise

The abstract Miyamoto action contains

\[
U_4(2)\triangleleft U_4(2){:}2,
\qquad |U_4(2)|=25,920,
\qquad |U_4(2){:}2|=51,840.
\]

The compressed inner standard pair remains

\[
a=\tau_0\tau_1\tau_2\tau_9,
\qquad
b=\tau_0\tau_3\tau_4\tau_9\tau_3\tau_5,
\]

with

\[
(|a|,|b|,|ab|)=(2,5,9),
\qquad |[a,b]|=3.
\]

Its exact internal class data are:

- `a`: class size 45, axis cycles `1^12 2^12`, triple cycles `1^16 2^52`;
- `b`: class size 5,184, axis cycles `1^1 5^7`, triple cycles `5^24`;
- `ab`: class size 2,880, axis cycles `9^4`, triple cycles `3^4 9^12`.

For the outer extension,

\[
c=\tau_0,
\qquad
d=\tau_1\tau_2\tau_3\tau_4\tau_9\tau_3\tau_5\tau_9,
\]

with

\[
(|c|,|d|,|cd|)=(2,9,10),
\quad |cd^2|=8,
\quad |[c,d^2]|=2.
\]

Its exact fingerprints are:

- `c`: class size 36, axis cycles `1^16 2^10`, triple cycles `1^30 2^45`;
- `d`: class size 5,760, axis cycles `9^4`, triple cycles `3^4 9^12`;
- `cd`: class size 5,184, axis cycles `1^1 5^3 10^2`, triple cycles `5^6 10^9`.

The size-36 outer involution class has centralizer order 1,440 and fixes sixteen axes and thirty Fischer triples. A future Monster search can now reject candidates in stages: first the 36-involution Fischer geometry, then these cycle fingerprints, then the standard-pair relations, and only afterward expensive Monster closure and character tests.

These words live in the exact abstract Miyamoto action. They are not serialized `mmgroup` words.

# II. The six-bit code yields an exact rooted Construction-A lattice

Let `C` be the binary code obtained from the left kernel of the 36 by 120 axis–triple incidence matrix. Its parameters and complete weight distribution are

\[
[36,6,16],
\qquad W_C(z)=1+27z^{16}+36z^{20}.
\]

The code is doubly even and self-orthogonal. Define

\[
L(C)=2^{-1/2}\{z\in\mathbf Z^{36}:z\bmod2\in C\}.
\]

The verifier constructs an integral basis and proves

\[
\det G=2^{24},
\qquad \operatorname{SNF}(G)=1^{12}2^{24}.
\]

Therefore

\[
L(C)^*/L(C)\cong(\mathbf Z/2\mathbf Z)^{24}.
\]

The lattice is even, has minimum norm two, and its complete root system is

\[
\boxed{A_1^{36}},\qquad72\text{ roots}.
\]

The initial theta coefficients by squared norm are

\[
1+72q^2+2520q^4+57120q^6+2712024q^8+\cdots.
\]

The coordinate automorphism group is `O6-(2) = U4(2):2`, of order 51,840. Including independent sign changes gives the exact signed-coordinate subgroup

\[
2^{36}{:}O_6^-(2)
\]

of order 3,562,417,673,994,240. This rooted, 2-elementary lattice is neither unimodular nor Leech-like; the `A1^36` roots explicitly obstruct that interpretation.

# III. The 36-port transform factors into 21 exact reflections

Let

\[
K=2A_{\rm spread}-J,\qquad H=K/6.
\]

The packet constructs twenty-one pairwise orthogonal primitive integer vectors spanning the `-1` eigenspace. Their rational Householder reflections

\[
R_i=I-2\frac{v_iv_i^{\mathsf T}}{v_i^{\mathsf T}v_i}
\]

commute pairwise and satisfy

\[
\boxed{H=R_1R_2\cdots R_{21}}.
\]

The complete integer vectors, support sizes, norms, and content hash are frozen in the JSON certificate. This is an exact rational transfer-matrix factorization, not a fabricated optical network, loss analysis, or laboratory claim.

# IV. The 120-cover is not distance-regular

The Fischer-line sharing graph has 120 vertices, degree 27, diameter three, and distance distribution

\[
1+27+90+2.
\]

Its forty distance-three fibers are intrinsic. The exact U4(2):2 action is faithful and transitive. A vertex stabilizer has order 432 and subdegrees

\[
\boxed{1,2,27,36,54}.
\]

The graph is not distance-regular: ordered pairs at distance two have profiles `(0,4,22,1)` for 6,480 pairs and `(0,6,21,0)` for 4,320 pairs. The intrinsic-fiber quotient and trivial deck kernel bound the full automorphism group by `Aut(W33)` of order 51,840, while the certified subgroup already has that order. Hence the full automorphism group is U4(2):2.

The Terwilliger algebra generated at one vertex has dimension 55 modulo each of 1,000,003, 1,000,033, and 1,000,037. Characteristic-zero equality is not promoted solely from modular agreement.

# V. The Monster class-fusion boundary is observable

The repository contains an exact GAP/CTblLib target for restricting the Monster character of degree 196,883 along admissible 5B-containing U4(2) class fusions. This packet adds a self-reporting workflow that installs GAP and CTblLib, executes the target under a timeout, validates its JSON, and commits either the census or a structured failure artifact to

`data/PART_3751_MONSTER_U42_CLASS_FUSION_EXECUTION.json`.

Until that artifact is observed, the class-fusion count and degree-81 multiplicities remain unclaimed.

# VI. Bonkers I: the Hadamard multiport is a quadratic-Walsh minor

The code identifies a six-dimensional binary quadratic space. Its nonsingular set `N` has 36 elements and satisfies

\[
|N\cap(N+t)|=20
\]

for every nonzero translation `t`. Thus `N` is an exact Hadamard difference set with parameters

\[
\boxed{(64,36,20)}.
\]

The character sums are 36 for the trivial character, +4 for nonzero singular characters, and -4 for nonsingular characters. For the full bilinear Walsh matrix

\[
W_{64}[x,y]=(-1)^{\beta(x,y)},
\qquad W_{64}W_{64}^{\mathsf T}=64I.
\]

Restricting to the 36 nonsingular vectors gives `W_N`, and the exact identity is

\[
\boxed{K=W_N-2I}.
\]

The W33 36-port Hadamard is therefore a diagonal shift of a six-bit quadratic-Walsh principal minor.

# VII. Bonkers II: the integral triple cokernel has order 192

For the 36 by 120 axis–Fischer-line incidence matrix `D`,

\[
\boxed{\operatorname{SNF}(D)=1^{30}2^5 6^1}.
\]

Hence

\[
\operatorname{coker}(D)\cong(\mathbf Z/2\mathbf Z)^5\times\mathbf Z/6\mathbf Z
\cong(\mathbf Z/2\mathbf Z)^6\times\mathbf Z/3\mathbf Z,
\]

of order 192. The two-primary sector is the six-dimensional minus-type module dual to the `[36,6]` code; the three-primary sector is a one-dimensional invariant conservation quotient. Equality with the tomotope flag count is recorded only as arithmetic—not as an objectwise identification.

# VIII. Bonkers III: the S3 cover carries a rank-20 holonomy frame

Let `P_standard` project each three-point fiber onto its two-dimensional standard representation and put `F=3P_standard`. If `A` is the cover adjacency matrix, define

\[
E_{20}=\frac{FAF+9F}{108}.
\]

The integer numerator satisfies

\[
Q_{20}^2=108Q_{20}.
\]

Thus `E20` is an orthogonal rank-20 projector with constant diagonal `1/6`. Its 120 projected coordinate vectors form a tight frame with frame bound six. The normalized pairwise-inner-product census is

\[
-\frac12:120,\qquad-\frac16:3240,\qquad0:2160,\qquad\frac13:1620.
\]

Within each fiber the three vectors form an equilateral triangle and sum to zero. The nonregular S3 holonomy therefore supports a canonical rank-20, 120-vector, four-angle tight frame.

# IX. Evidence boundary

Proved in the exact source certificate:

- abstract Monster-search class fingerprints and standard-pair filters;
- an even rooted Construction-A lattice with discriminant `(Z/2)^24`;
- a 21-reflection exact factorization of the 36-port involution;
- the cover's non-distance-regularity, full symmetry, and modular Terwilliger dimension 55;
- the `(64,36,20)` quadratic difference set and Walsh-parent identity;
- the Smith cokernel `(Z/2)^5 × Z/6`;
- the rank-20 twisted-holonomy tight frame.

Still outside this certificate:

- serialized Monster words or an actual Monster embedding;
- a Monster restriction multiplicity unless the separate GAP artifact is observed;
- characteristic-zero Terwilliger dimension inferred only from modular evidence;
- a Leech or even-unimodular lattice identification;
- any physical optical implementation or laboratory-performance claim.
