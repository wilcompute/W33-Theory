# Passes 5595–5602 — projectivity closure and three falsifiable TOE probes

## 5595 — the full projectivity-incidence automorphism mechanism

Let \(D_q\) have rows \(G=\mathrm{PSL}_2(q)\), columns \(X\times X\) for \(X=\mathbf P^1(q)\), and incidence \(g\sim(x,y)\iff y=g(x)\).  Distinct columns have zero common rows exactly when they share one coordinate.  Therefore the incidence structure itself reconstructs the square rook graph on \(X\times X\), so every incidence automorphism acts on the columns through

\[
(S_{q+1}\times S_{q+1})\rtimes C_2.
\]

Without the ruling swap a column map is \((x,y)\mapsto(a x,b y)\).  It preserves the graph-row set exactly when

\[
bGa^{-1}=G.
\]

Since \(1\in G\), this forces \(ba^{-1}\in G\) and \(a\in N_{S_{q+1}}(G)\); conversely those conditions suffice.  In the natural projective-line action the normalizer is the standard

\[
N_{S_{q+1}}(\mathrm{PSL}_2(q))=\mathrm{P}\Gamma\mathrm L_2(q),
\]

whose order for odd \(q=p^f\) is \(2f|G|\).  Transpose/inversion doubles the fiber product.  Hence

\[
\boxed{|\operatorname{Aut}(D_q)|=4f|\mathrm{PSL}_2(q)|^2.}
\]

The verifier enumerates all natural automorphisms at \(q=3,5\), obtaining \(576\) and \(14,400\).  This explains the Reye \(576\) as the \(q=3\) member of an all-\(q\) normalizer law.

**Boundary.** General completeness uses the standard normalizer theorem; the executable enumeration is finite at \(q=3,5\).

## 5596 — Reye and Klein-\(V_4\) Latin actions are explicitly the same 12-point action

Write

\[
A_4=V_4\rtimes\langle r\rangle,
\qquad r=(0\ 2\ 3\ 1),
\qquad r^3=1.
\]

The Reye rows are the twelve elements \(vr^k\).  The Klein-\(V_4\) Latin autoparatopy action is the affine symmetry of

\[
x+y+z=0
\]

on three labelled copies of \(V_4\cong\mathbf F_2^2\).  The explicit bijection

\[
\boxed{\Phi(vr^k)=\bigl(k,\,r^k(v(0))\bigr)}
\]

conjugates the entire 576-element Reye row action onto the entire 576-element Latin 12-symbol action.  Both degree-12 actions have orbital sizes

\[
12,\ 36,\ 96,
\]

and the 36-orbital is exactly \(3K_4\).

This upgrades the previous abstract-group isomorphism to a permutation-action isomorphism.

**13-cover boundary.** The committed 13-cover certificate retains only the abstract image structure and the orbit sizes \(1+12\); it does not retain explicit \(S_{13}\) generators.  Therefore this pass does not silently identify the nonfixed 12-orbit with the Reye/Latin action.  That last equivariant comparison still needs the actual generators or an index-12 subgroup-conjugacy proof.

## 5597 — extension fields: \(q=9\) and \(q=25\) now replay genuinely

The prime-only restriction of the first projectivity verifier is removed.  Using explicit quadratic fields

\[
\mathbf F_9=\mathbf F_3[w]/(w^2-2),
\qquad
\mathbf F_{25}=\mathbf F_5[w]/(w^2-2),
\]

the verifier reconstructs all projective points, the singular Segre grid, one nonsingular square class, all projectivities, and every symplectic-incidence equality.

The non-prime anchors are

\[
\begin{array}{c|c|c|c}
q&|\mathrm{PSL}_2(q)|&(q+1)^2&\operatorname{rank}_2M\\\hline
9&360&100&50\\
25&7800&676&338
\end{array}
\]

so the all-prime-power law

\[
\boxed{\operatorname{rank}_2M=(q+1)^2/2}
\]

now has genuine extension-field replay rather than only a representation-theoretic proof plus prime anchors.

## 5598 — the projectivity code sits inside the footprint **kernel**, not the footprint image

Let \(C_W\) be the binary W-line incidence code.  Pass 5376 proved

\[
C_W=\ker(F^T),
\qquad
C_W^\perp=\operatorname{im}(F).
\]

For \(p\) in one nonsingular \(Q\)-class, let \(N(p)\) be the full symplectic-neighbour indicator of \(p\) on all W-points.  Summing the \(q+1\) W-lines through \(p\) modulo two cancels \(p\), because \(q+1\) is even, and leaves every neighbour once.  Thus

\[
N(p)\in C_W=\ker(F^T).
\]

If \(\pi_S\) restricts coordinates to the singular Segre sheet \(S=Q^+(3,q)\), then

\[
\boxed{M_p=\pi_S N(p)}.
\]

Therefore

\[
\boxed{\operatorname{row}(M)
=\pi_S\operatorname{span}\{N(p):p\in C_+\}
\subseteq \pi_S(C_W).}
\]

This is the exact bridge to the older footprint theorem.  It is a projected subcode of the footprint kernel, not a disguised copy of the footprint image.

At \(q=3,5,7\), the verifier finds

\[
\dim \pi_S(C_W)=15,34,61,
\qquad
\dim\operatorname{row}(M)=8,18,32,
\]

so equality with the full restricted line code is decisively false.

## 5599 — a fixed-point fusion scheme, and why \(q=3\) collapses

On \(G=\mathrm{PSL}_2(q)\), define \(R_t(g,h)\) by the number \(t\in\{0,1,2\}\) of fixed points of \(g^{-1}h\) on \(\mathbf P^1(q)\).  The observed valencies are the uniform formulas

\[
\boxed{k_0=\frac{q(q-1)^2}{4}},\qquad
\boxed{k_1=q^2-1},\qquad
\boxed{k_2=\frac{q(q+1)(q-3)}{4}}.
\]

Full intersection-number constancy is checked at \(q=3,5,7,9\).  The same closed polynomial intersection matrices are then replayed at \(q=11,13,25\).  This is strong evidence for an all-odd 3-class fusion, but the packet deliberately leaves the all-\(q\) symbolic counting/character proof open rather than calling interpolation a theorem.

At \(q=3\),

\[
k_2=0.
\]

The would-be 3-class scheme collapses to two nontrivial relations:

\[
R_0=3K_4,
\qquad
R_1=K_{4,4,4}.
\]

Those three \(K_4\) blocks are exactly the three cosets of the normal \(V_4\triangleleft A_4\), and exactly the three four-symbol parts exposed by the Reye–Latin intertwiner.  This gives a structural reason the \(q=3\) member is exceptional.

## 5600 — outside the box: the Segre sheet as a finite null-coordinate kinematic primitive

The hyperbolic quadric has two canonical rulings:

\[
Q^+(3,q)=\mathbf P^1(q)\times\mathbf P^1(q).
\]

A projectivity graph \(y=g(x)\) meets every member of each ruling exactly once.  It is therefore simultaneously a perfect matching and a transversal of the two ruling families.  Two such transversals meet in \(0,1,2\) events according to the fixed points of their relative projectivity.

This is mathematically very close to a pair of discrete null-coordinate foliations: two one-dimensional coordinate families, with projectivities as exact transversal histories.  It is a useful kinematic picture for the Holonet.

**Physics firewall.** It is only a finite split-quadric analogy.  There is no derived Lorentz metric, causal partial order, continuum limit, \(3+1\) dimension, mass shell, or measured value of \(c\).  In fact the object is intrinsically a two-ruling surface, so identifying it directly with physical \(3+1\) spacetime would be an overclaim.

## 5601 — outside the box: determinant chirality gives an exact half-rate isodual code

Let \(C_+\) be the binary span of vectorized permutation matrices from \(\mathrm{PSL}_2(q)\), and let \(C_-\) use the opposite determinant coset in \(\mathrm{PGL}_2(q)\).  For permutation matrices,

\[
\langle P_g,P_h\rangle
\equiv |\operatorname{Fix}(g^{-1}h)|\pmod2.
\]

If \(g\) and \(h\) lie in opposite determinant classes, \(g^{-1}h\) has nonsquare determinant class.  It cannot be unipotent/one-fixed-point: a repeated eigenvalue has square determinant class.  Therefore the relative projectivity has \(0\) or \(2\) fixed points, and every cross inner product vanishes modulo two:

\[
C_-\subseteq C_+^\perp.
\]

Pass 5594 gives

\[
\dim C_+=\frac{(q+1)^2}{2}.
\]

Multiplication by one fixed opposite-coset projectivity is only a coordinate permutation of the \((q+1)\times(q+1)\) grid, so \(\dim C_-=\dim C_+\).  Since the ambient length is \((q+1)^2\), dimensions force

\[
\boxed{C_-=C_+^\perp.}
\]

Thus \(C_+\) is an exact binary isodual code

\[
\boxed{[(q+1)^2,(q+1)^2/2]}
\]

for every odd prime power \(q\).

At \(q=3\) the weight enumerator is

\[
1+12z^4+64z^6+102z^8+64z^{10}+12z^{12}+z^{16},
\]

and at \(q=5\) the measured minimum distance is \(6=q+1\).  The all-\(q\) minimum-distance law is left open.

**TOE reading.** The square/nonsquare determinant split supplies two canonically paired half-rate information sectors on the same finite carrier.  That is a genuine algebraic duality.  Calling those sectors matter/antimatter, past/future, electric/magnetic, or entropy flow would require a separate physical map and is not done here.

## 5602 — outside the box: a spectral-action firewall

The centered projectivity frame is *too* spectrally clean to be a spacetime kinetic operator.  After removing the constant direction,

\[
\boxed{\operatorname{spec}(M_c^TM_c)
=\left(\frac{q^2-1}{2}\right)^{q^2}\oplus0^{\,*}.}
\]

Equivalently the unit-norm frame operator is a scalar multiple of the identity on its \(q^2\)-dimensional span, with frame bound

\[
\frac{q^2-1}{2q}.
\]

So its heat trace has only one nonzero exponential scale.  There is no multi-level Weyl-law spectral ladder from which a local continuum dimension could emerge.

This is a useful negative result for the Theory-of-Everything program:

\[
\boxed{\text{the projectivity-frame Gram is a projector/frame observable, not the spacetime Laplacian.}}
\]

If physical dynamics is to emerge from the finite geometry, it has to live in a richer operator already present elsewhere in the repository—Hodge, Hashimoto/non-backtracking, transport, holonomy, or a genuinely new dynamical operator—and that operator must pass its own continuum/scaling tests.

## External prior-art boundary

The literature check for this packet found nearby but distinct structures: projective-line derangement graphs for \(\mathrm{PGL}_2(q)\)/\(\mathrm{PSL}_2(q)\); coherent configurations from \(\mathrm{PGL}_2(q)\) acting on a conic; and coding theory on hyperbolic quadric surfaces \(\mathbf P^1\times\mathbf P^1\).  Those sources support the standard group/conic/quadric background.  They do not, by themselves, establish the repo-specific Reye/Latin intertwiner, footprint-kernel projection, determinant-coset isodual code, or Holonet physical interpretation.

## Global evidence boundary

Passes 5595–5602 establish or test finite group, incidence, code, and frame statements.  The three TOE probes are intentionally asymmetric: one supplies a candidate kinematic primitive, one supplies an exact information duality, and one kills a tempting spectral-dynamics interpretation.  None is presented as a derivation of gravity, the Standard Model, cosmological parameters, or laboratory physics.
