# Pass 1147: Schläfli–Steinberg Fourier Bridge

Date: 2026-07-27

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

