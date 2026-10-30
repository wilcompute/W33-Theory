# Pass 1147: Schläfli–Steinberg Fourier Bridge

Date: 2026-07-27; integral completion 2026-07-30

## Headline

The three \(432\)-element \(W(E_6)\)-orbits killed by the cubic-incidence
map are now identified and recovered object by object.

Fix an \(A_2\) subsystem in \(E_8\). Its six \(27\)-root shells pair by
negation into three colors. For each color, an \(A_2\) triple contains one
\(E_6\) root and one root in each of two opposite shells. Sending
\(\{x,y,z\}\) to the ordered pair \((x,-y)\) is an equivariant bijection
onto the directed edges of the Schläfli graph

\[
\operatorname{SRG}(27,16,10,8).
\]

Thus each color fibre has \(27\cdot16=432\) objects and directed-edge
stabilizer \(S_5\). The three formerly anonymous \(432\)-orbits are exactly
three colored copies of one directed Schläfli-edge carrier.

## Corpus ownership after the three-day reconciliation

The Schläfli graph and its \(216\) undirected edges already occur in the
paper's earlier \(E_6\) geometry. Pass 1149 already owns the abstract
module-level statement
\(81_-\otimes\mathbb C[C_3]\) and its rank-\(243\) Fourier split. Pass 1301
later supplies different carrier-level \(M_3\) matrix units, and Passes
1315--1329 supply the literal rank-\(26\) Hecke algebra, the six-channel
\(432\leftrightarrow480\) transport, triality globalization, and their Smith
forms.

Pass 1147's distinct ownership is object-level: it identifies each actual
\(432\)-orbit with directed Schläfli edges, writes the natural
edge-to-cycle transform, constructs the \(216\)-line frame, welds the three
transforms to the literal \(2240\)-object cubic map, and now determines the
integral image lattice of that transform.

## The natural edge-to-cycle transform

Let \(K\) be the sum of the \(36\) reflections in the \(2C\) class acting on
\(\Lambda^2(\operatorname{Aug}\mathbb Q^{27})\). Define

\[
Q=(K-24)(K-18)(K-12)(K-9).
\]

For an oriented Schläfli edge \(i\to j\), the map

\[
T(i\to j)=\operatorname{primitive}\!\left(Q(e_i\wedge e_j)\right)
\]

is integral, \(W(E_6)\)-equivariant, and has rank \(81\). It satisfies

\[
K\,T=4T,\qquad Q\,T=11200T,\qquad
T(j\to i)=-T(i\to j).
\]

Every image vector lies in the contraction kernel
\(\Lambda^2(\operatorname{Aug}\mathbb Q^{27})\), so \(T\) is an explicit
edge-to-cycle transform

\[
\mathbb Q^{\overrightarrow E(\mathrm{Schl})}
   \longrightarrow
\Lambda^2(\operatorname{Aug}\mathbb Q^{27}).
\]

The antisymmetric \(216\)-edge module is multiplicity-free:

\[
6\oplus15\oplus20\oplus30\oplus64\oplus81_-.
\]

The transform \(T\) projects onto the last summand. Its kernel on oriented
edges is therefore the explicit \(135\)-dimensional module

\[
6\oplus15\oplus20\oplus30\oplus64.
\]

This \(135\) is a representation-theoretic residual; no identification with
the separate isotropic \(135\)-set in \(E_8/2E_8\) is asserted.

## The integral tight frame

The \(432\) primitive image vectors have norm squared \(600\), occur in
\(216\) antipodal pairs, and have Gram matrix \(G_T\) satisfying

\[
\boxed{G_T^2=3200\,G_T}.
\]

Their unordered off-diagonal inner-product distribution is

\[
(-600)^{216},\quad
(-120)^{7560},\quad
(-40)^{12960},\quad
0^{51840},\quad
40^{12960},\quad
120^{7560}.
\]

After quotienting antipodes, this gives a transitive tight
three-angle code of \(216\) projective lines in \(\mathbb R^{81}\), with
absolute normalized inner products

\[
0,\qquad \frac1{15},\qquad \frac15
\]

and per-line valencies \(120,60,35\), respectively. GAP also checks that the
three absolute-angle relations do **not** form a three-class association
scheme, so no stronger fusion claim is made.

## The \(C_3\) Fourier trichotomy

The \(A_2\) Coxeter element has order three, centralizes \(W(E_6)\), and
cycles the three color fibres and their three transforms literally. Hence
the rank-\(243\) image is, as a \(W(E_6)\times C_3\)-module,

\[
81_-\boxtimes\mathbb Q[C_3].
\]

Over \(\mathbb Q\) the color factor is \(1\oplus V_2\). After adjoining
\(\omega=e^{2\pi i/3}\), exact finite Fourier transform gives

\[
(81_-\boxtimes1)\oplus
(81_-\boxtimes\omega)\oplus
(81_-\boxtimes\omega^2).
\]

The unbased \(C_3\)-torsor is intrinsic relative to the fixed \(A_2\).
A displayed ordering of its three Fourier modes chooses an origin color and
a Coxeter generator; using the inverse generator exchanges
\(\omega\) and \(\omega^2\).

## Integral completion: where the primes \(2,3,5\) enter

Use contraction zero to delete the \(26\) wedge coordinates incident with
one chosen vertex. This is an integral chart, not a rational minor: the
deleted coordinates are recovered as integral sums of the retained
coordinates. In this chart \(T\) is a \(432\times325\) integer matrix of
rank \(81\). GAP computes its nonzero Smith factors as

\[
\boxed{1^{15},\;2^6,\;4^8,\;8^{29},\;40^{23}}.
\]

If \(L_T\) is the image lattice and \(\overline L_T\) its saturation, then

\[
\overline L_T/L_T\cong
(\mathbb Z/2)^6\oplus(\mathbb Z/4)^8\oplus
(\mathbb Z/8)^{29}\oplus(\mathbb Z/40)^{23},
\]

with

\[
[\overline L_T:L_T]=2^{178}5^{23}.
\]

The rank falls from \(81\) to \(15\) modulo \(2\), and to \(58\) modulo
\(5\); it remains \(81\) modulo \(3,7,11\). Thus the within-color frame
lattice has exact bad-prime set

\[
\boxed{\{2,5\}}.
\]

The normalization itself explains the upper Smith scale. On a natural
Schläfli edge, \(Q(e_i\wedge e_j)\) has content \(280\), while \(Q\) acts
on the selected \(K=4\) space by \(11200\). Therefore, on this literal edge
carrier,

\[
\boxed{T=Q/280=40P_4},
\qquad P_4=Q/11200.
\]

Every nonzero Smith invariant consequently divides \(40\), as GAP checks
directly. The prime \(7\) in \(11200=2^6\cdot5^2\cdot7\) also divides the
edge content \(280=2^3\cdot5\cdot7\); it cancels from the primitive
multiplier \(40\), the Smith index, and the modular rank drop. This is a
statement about this constructed edge lattice, not a general theorem about
integral spectral projectors.

The integral basis separating the color permutation lattice into its
trivial and augmentation parts has Smith form

\[
\operatorname{SNF}
\begin{pmatrix}
1&1&0\\
1&-1&1\\
1&0&-1
\end{pmatrix}
=\operatorname{diag}(1,1,3).
\]

Tensoring with the rank-\(81\) image therefore makes the rational
\(81\oplus162\) color split a sublattice of index \(3^{81}\). This cleanly
separates the arithmetic roles:

- primes \(2,5\) belong to the integral Schläfli--Steinberg image;
- prime \(3\) enters when the three colors are integrally Fourier-separated;
- Pass 1326's six-channel transport has bad primes \(2,3\), while its full
  Hecke-unit lattice has bad primes \(2,3,5\).

This is an integral representation boundary, not a hardware threshold or a
particle-family derivation.

### The \(5\)-primary quotient is the sign-twisted W33 sandpile module

**Ownership boundary.** The spanning-tree factor
\(\tau(W_{3,3})=2^{81}5^{23}\) and the bare arithmetic
\(81-23=58\) already belong to
`analysis/w33_BREAKTHROUGH_spanning_trees.py`; `w33_paper.tex` already
records \(K(W_{3,3})_{(5)}\cong(\mathbb Z/5)^{23}\). Pass 1147 does not
reclaim those counts. Its new content is the literal \(\mathbb F_5\) module
quotient, the outer-sign Hom calculation and isomorphism, and the nonsplit
extension class below.

GAP rebuilds the reduced W33 Laplacian and obtains

\[
\operatorname{SNF}(L_{\mathrm{red}})
 =1^{16},10^8,40,160^{14},
\qquad K(W_{3,3})_{(5)}\cong(\mathbb Z/5)^{23}.
\]

It then constructs two literal \(\mathbb F_5W(E_6)\)-modules from the same
displayed \(W(E_6)\) generators:

1. the \(23\)-dimensional quotient
   \((\overline L_T/L_T)_{(5)}\);
2. the \(23\)-dimensional W33 sandpile primary part
   \(K(W_{3,3})_{(5)}\), transported through
   \(W(E_6)\cong PGSp(4,3)\).

Both are irreducible. Solving the full simultaneous intertwiner equations
gives

\[
\dim\operatorname{Hom}_{W(E_6)}(Q_T,K_5)=0,\qquad
\dim\operatorname{Hom}_{W(E_6)}(Q_T\otimes\mathrm{sgn},K_5)=1,
\]

and restriction to \(W(E_6)'=PSp(4,3)\) also gives Hom dimension \(1\).
All four nonzero scalars in that one-dimensional \(\mathbb F_5\) Hom space
are invertible. Hence

\[
\boxed{Q_T\otimes\mathrm{sgn}\cong K(W_{3,3})_{(5)}}
\]

uniquely up to \(\mathbb F_5^\times\). The untwisted Hom-space zero is an
important part of the theorem: the outer sign cannot be discarded.

There is a further integral consequence. Put
\(S_5=\overline L_T/5\overline L_T\). The edge image is its irreducible
\(58\)-dimensional submodule, and GAP finds that the complete submodule
dimension profile of \(S_5\) is just \(0,58,81\), both for \(W(E_6)\) and
after restriction to \(PSp(4,3)\). Equivalently,
\[
\operatorname{Hom}_{W(E_6)}(Q_T,S_5)=
\operatorname{Hom}_{PSp(4,3)}(Q_T,S_5)=0.
\]
Consequently the exact sequence
\[
\boxed{
0\longrightarrow I_{58}\longrightarrow S_5
\longrightarrow K(W_{3,3})_{(5)}\otimes\mathrm{sgn}
\longrightarrow0
}
\]
is nonsplit over both groups. Thus the saturated reduction is a length-two
module with unique proper nonzero submodule, not \(58\oplus23\). This proves
that this displayed extension class is nonzero. Pass 1335 subsequently
computes the cyclic-defect Brauer tree and proves that the relevant directed
\(\operatorname{Ext}^1\) space has dimension one over both groups, so this
class spans it.

The module isomorphism class is intrinsic, but any displayed intertwiner matrix
depends on the chosen \(W(E_6)\cong PGSp(4,3)\) identification and quotient
bases. No canonical integral lift, sandpile-to-edge map over \(\mathbb Z\),
or physical channel identification is asserted.

## The enhanced \(2240\)-carrier map

Let

\[
M:\mathbb Q^{2240}\longrightarrow\mathbb Q^{45}
\]

be Pass 1138's cubic-incidence map. It has rank \(45\), is supported exactly
on the unique \(240\)-orbit, and kills all three \(432\)-orbits. Extending the
three colored transforms by zero off their respective fibres gives

\[
\Phi =
M\oplus T_0\oplus T_1\oplus T_2:
\mathbb Q^{2240}\longrightarrow
\mathbb Q^{45}\oplus
\bigoplus_{c\in C_3}
\Lambda^2(\operatorname{Aug}\mathbb Q^{27}_c).
\]

GAP constructs the literal \(1020\times2240\) integer matrix and proves

\[
\boxed{\operatorname{rank}\Phi=45+3\cdot81=288},
\qquad
\boxed{\dim\ker\Phi=2240-288=1952}.
\]

The supports are disjoint: \(240\) source basis vectors feed \(M\), \(1296\)
feed the three Steinberg blocks, and the remaining \(704\) are silent under
both.

Combining this construction with Pass 1135's exact character decomposition
removes precisely the three \(81_-\) constituents from \(\ker M\). Therefore

\[
\ker\Phi =
13\cdot1+16\cdot6+5\cdot15+4\cdot15_a+21\cdot20+2\cdot24+
9\cdot30+4\cdot60_a+10\cdot64+90,
\]

of dimension \(1952\).

The old mnemonic
\(1952=7\dim\Lambda^2(\mathbb Q^{24})+20\) is not the decomposition of this
kernel. It named no map and is superseded by the explicit formula above.

## External comparison and novelty boundary

The classical carrier is not new. Lee's treatment of the Gosset polytope
\(2_{21}\) records \(27\) vertices and \(216\) unoriented edges, with
\([E_6:A_1\times A_4]=216\)
([Canadian Journal of Mathematics 64 (2012), 123--150](https://doi.org/10.4153/CJM-2011-063-6)).
The ATLAS records \(U_4(2)\cong PSp(4,3)\) of order \(25920\), outer
automorphism group of order \(2\), the \(27\)-point action, and an integral
\(81\)-dimensional representation of \(U_4(2):2\)
([ATLAS of Finite Group Representations](https://brauer.maths.qmul.ac.uk/Atlas/clas/U42/)).
General arithmetic criteria for critical groups of strongly regular graphs
are also established in Ducey--Duncan--Engelbrecht--Madan--Piato--Shatford--
Vichitbandha
([JCTA 180 (2021), 105424](https://doi.org/10.1016/j.jcta.2021.105424)).

Those sources provide comparison and prior ownership; they do not by
themselves construct the displayed Schläfli-edge transform, its Smith
profile, or the sign-twisted nonsplit \(58|23\) module. Targeted searches for
those exact objects found no published match. That is a bounded literature
search, not a claim that no equivalent construction exists anywhere.

## Reproducibility and scope

- GAP witness:
  `analysis/w33_pass1147_schlaefli_steinberg_fourier_bridge.g`
- deterministic certificate:
  `data/w33_pass1147_schlaefli_steinberg_fourier_bridge.json`
- focused regression:
  `tests/test_pass1147_gap_schlaefli_steinberg_fourier_bridge.py`

The certificate establishes exact finite \(E_8/W(E_6)\) geometry, integer
intertwiners, a tight projective code, and a \(C_3\) representation grading.
It does not by itself identify the three Fourier modes with Standard Model
generations, masses, Yukawa couplings, physical polarizations, or measured
hardware channels.
