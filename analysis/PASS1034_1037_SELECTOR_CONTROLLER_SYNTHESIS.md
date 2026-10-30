# Passes 1034–1037: selector algebra, correction refinement, and the external controller

## Executive result

The project now contains three distinct order-six structures that must not be conflated:

1. **Internal fibre:** the Eisenstein units
   \[
   \langle c^5\rangle\cong C_6.
   \]
   This is an abelian torsor on each six-root fibre. Its order-two subgroup is the antipodal sign already inside \(\mathrm{Sp}(4,3)\).

2. **Selector local controller:**
   \[
   S_3=C_3\rtimes C_2,
   \]
   visible on the three matchings of a four-object local fibre. The binary element inverts the ternary phase.

3. **External global controller:**
   \[
   N_{W(E_8)}(\langle\omega\rangle)/\mathrm{Sp}(4,3)\cong S_3.
   \]
   Its normal \(C_3\) is the complex-determinant phase detector from Pass 1031. Its quotient \(C_2\) is the base chirality character from Pass 1033.

Thus equal cardinality six does not identify the objects. The internal fibre is cyclic; the required controller is nonabelian.

---

## Workstream 1 — complete rank-five orbital algebra

Pass 1034 reconstructs the line-phase action of \(PSp(4,3)\) on

\[
40\text{ lines}\times3\text{ perfect matchings}=120\text{ sheets}.
\]

The action is a symmetric rank-five association scheme with relation valencies

\[
\boxed{1,2,36,27,54}.
\]

These correspond respectively to:

- the same sheet;
- the other two phases above the same line;
- all three phases above each intersecting line;
- one matched phase above each skew line;
- two unmatched phases above each skew line.

The selector overlap values are therefore the orbital relations:

\[
108^1,\quad54^2,\quad12^{36},\quad4^{27},\quad2^{54}.
\]

The first eigenmatrix is

\[
P=
\begin{pmatrix}
1&2&36&27&54\\
1&2&-12&3&6\\
1&-1&0&-3&3\\
1&-1&0&9&-9\\
1&2&6&-3&-6
\end{pmatrix},
\]

with primitive multiplicities

\[
\boxed{1,15,60,20,24}.
\]

The second eigenmatrix is

\[
Q=
\begin{pmatrix}
1&15&60&20&24\\
1&15&-30&-10&24\\
1&-5&0&0&4\\
1&5/3&-20/3&20/3&-8/3\\
1&5/3&10/3&-10/3&-8/3
\end{pmatrix},
\]

and

\[
PQ=QP=120I_5.
\]

The complete intersection tensor and Krein tensor are stored in the generated certificate. All Krein parameters are nonnegative.

---

## Workstream 2 — selector correction solved at the correct level

The draft golden transport rule has:

\[
480\text{ directed transports}=240\text{ undirected transports}.
\]

On the \(1620\) unique nonlocal quadrangles, exactly

\[
\boxed{108}
\]

have nontrivial binary holonomy.

Let \(\partial\) be the quadrangle/transport incidence matrix over \(\mathbb F_2\). Pass 1035 proves

\[
\operatorname{rank}\partial=200,
\]

so the correction space has dimension

\[
240-200=40.
\]

More sharply,

\[
\ker\partial
=
\operatorname{im}(\delta_{\rm line})\oplus\langle\mathbf 1_{\rm edges}\rangle,
\]

where the line-coboundary space has rank \(39\) and the constant all-edge cochain supplies the fortieth dimension.

Therefore all valid corrections form one affine class, unique modulo:

- ordinary line gauge;
- one global parity sheet.

A deterministic gauge-fixed representative has weight

\[
\boxed{54=18\cdot3}
\]

and repairs all \(1620\) quadrangles. Locally it is a three-edge star in the four-line pencil at each of eighteen selected points.

### Bose–Mesner no-go

The rank-five algebra cannot itself carry this correction. All transport between intersecting lines lies in the single valency-\(36\) relation. A binary orbital weight is constant on every transport step, so a four-cycle receives

\[
4c=0\pmod2.
\]

Since \(108\) cycles have nonzero holonomy, no Bose–Mesner-invariant correction exists.

The correction must therefore live in a **pointed coherent/Terwilliger refinement** that splits the valency-\(36\) relation by local pencil data. This is a structural theorem, not a failed search.

---

## Workstream 3 — the two primary detectors

The parallel verified passes complete the detector table.

### Ternary phase

Pass 1031 proves that on

\[
C=C_{W(E_8)}(\omega)=C_3\times\mathrm{Sp}(4,3),
\]

the complex determinant is the abelianisation map

\[
\det_{\mathbb C}:C\twoheadrightarrow\mu_3,
\]

with kernel exactly \(\mathrm{Sp}(4,3)\). It detects phase and is blind to the antipodal sign.

### Binary chirality

Pass 1033 proves that \(\mathrm{Sp}(4,3)\) is perfect and has no nontrivial abelian character, while

\[
W(E_6)=U_4(2):2
\]

has abelianisation \(C_2\). The binary character therefore exists on the base and nowhere inside the total-space group.

The real determinant in the ambient eight-dimensional representation remains trivial on the entire Eisenstein normaliser, so this base character is not the ambient determinant in disguise.

---

## Workstream 4 — six-response photonic falsifier

Pass 1036 compiles the controller into its faithful two-mode dihedral representation.

Let

\[
r=R(2\pi/3),\qquad s=\operatorname{diag}(1,-1).
\]

Then

\[
r^3=s^2=(sr)^2=I,
\]

and critically

\[
\boxed{srs=r^{-1}}.
\]

The six transfer responses are

\[
\{r^j s^\epsilon:j\in\mathbb Z_3,\ \epsilon\in\mathbb Z_2\}.
\]

They are distinct, closed under multiplication, and split into three determinant-\(+1\) and three determinant-\(-1\) responses.

A false scalar \(C_6\) implementation fails because its sign and phase commute. It therefore gives

\[
srs=r\neq r^{-1}.
\]

The decisive experimental sequence is:

1. verify \(r^3=I\);
2. verify \(s^2=I\);
3. measure the inversion echo \(srs=r^{-1}\);
4. distinguish \(sr\) from \(rs\);
5. resolve all six transfer matrices.

Observing only a ternary cycle certifies the residual \(C_3\) carrier, not the full controller.

---

## Workstream 5 — minimal external controller

Pass 1037 computes, inside \(W(E_8)\),

\[
C=C_{W(E_8)}(\omega),\qquad
K=C'=\mathrm{Sp}(4,3),\qquad
N=N_{W(E_8)}(\langle\omega\rangle).
\]

The group orders are

\[
|C|=155520,\qquad |K|=51840,\qquad |N|=311040.
\]

The quotient is

\[
\boxed{N/K\cong S_3}.
\]

It fits the exact sequence

\[
1\longrightarrow C_3\longrightarrow S_3\longrightarrow C_2\longrightarrow1,
\]

and the outer involution acts by inversion on the phase subgroup.

Minimality is exact: a controller containing independent order-three and order-two operations has order divisible by six, and the quotient realizes order six with the required nontrivial action.

---

## Architectural conclusion

The correct hierarchy is

\[
\boxed{
C_6\text{ internal state fibre}
\quad\neq\quad
S_3\text{ external controller}.
}
\]

The selector's local \(C_3\to S_3\) upgrade was not an isolated combinatorial curiosity. It is the finite-action shadow of the global normaliser quotient. The same inversion that fuses the rank-seven point-phase action into the rank-five selector scheme is the binary operation required by the six-response optical controller.

The remaining selector problem is no longer “find any correction.” The affine correction class is known. The remaining problem is to construct a **canonical pointed refinement** selecting one representative of that class compatibly with the external \(S_3\) controller.
