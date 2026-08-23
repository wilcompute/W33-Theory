# Pass9985–10048 — eight-front synthesis

## Executive result

This packet executes the five open fronts from Pass9885–9980 and three additional outside-box attacks.  The strongest positive closure is arithmetic: the transverse-glue \(F_9^6\) phase space lifts from an associated-graded coincidence to the full truncated cyclotomic residue ring

\[
\mathcal O_{\mathbf Q_3(i,\zeta_9)}/3\mathcal O
\cong \mathbf F_9[t]/(t^6),\qquad t=\zeta_9-1,
\]

with an explicit regular order-nine nondegenerate unitary action.  The six residue layers form a full Bruhat–Tits chamber for \(PGL_6(\mathbf Q_3(i))\).  Independently, the parallel lane's new \(E_8/3E_8=H(3,9)\) theorem and the glue construction are shown to be two ranks of one exact \(\mathbf F_9\)-Hermitianization functor.

The selector side became more restrictive rather than more speculative.  An actual \(C_{13}\) in the canonical \(V_2/Co_0\) stabilizer is **not** certified.  Instead the problem is reduced to exact group-theoretic gates.  The natural Q−/Q+ two-space fusion also fails spectrally despite identical valencies.  These negative results remove several tempting but noncanonical welds.

---

## Pass9985–9992 — actual \(C_{13}\) in the canonical \(V_2\) stabilizer: exact gate, existence still open

The canonical \(V_2\) is built from the unique pure order-eight Co0 class \(M\), whose centralizer has order

\[
|C_{Co_0}(M)|=48384=2^8 3^3 7.
\]

Every nonzero vector of \(V_2\) is a type-eight/frame direction.  A frame stabilizer in \(Co_1\) is \(2^{11}{:}M_{24}\), whose order is also prime to 13.  Therefore any \(C_{13}\leq \operatorname{Stab}_{Co_0}(V_2)\) would fix no nonzero vector and hence would have exactly

\[
4095/13=315
\]

cycles on \(V_2\setminus\{0\}\).

There is a second obstruction.  Since

\[
N(\langle M\rangle)/C(M)\hookrightarrow \operatorname{Aut}(C_8),
\qquad |\operatorname{Aut}(C_8)|=4,
\]

an element of order 13 normalizing \(\langle M\rangle\) would have to centralize \(M\), impossible because 13 does not divide 48384.  Thus any actual \(C_{13}\) stabilizing \(V_2\) must move \(M\) through an orbit divisible by 13.

The ATLAS maximal-overgroup gate reduces the remaining search to the 13-bearing branches

\[
3.\mathrm{Suz}{:}2,
\qquad
(A_4\times G_2(4)){:}2.
\]

**Boundary:** this is not an existence theorem.  No explicit Co0 word of order 13 stabilizing the canonical \(V_2\) has yet been certified.

---

## Pass9993–10000 — the 315 cycles are a \(C_{315}\) torsor; exact mismatch with G2 clocks

For the abstract irreducible \(C_{13}\) on \(\mathbf F_2^{12}\),

\[
\operatorname{ord}_{13}(2)=12,
\]

so the module is the additive group of \(\mathbf F_{2^{12}}\).  The centralizer and normalizer are

\[
C_{GL(12,2)}(C_{13})=\mathbf F_{2^{12}}^\times=C_{4095},
\]

\[
N_{GL(12,2)}(C_{13})=C_{4095}{:}C_{12}.
\]

Because \(4095=13\cdot315\), the 315 thirteen-cycles form a **regular \(C_{315}\) torsor** under \(C_{4095}/C_{13}\).

On the certified \(G_2(4){:}2\) carriers, a \(C_{13}\) is semiregular because the vertex, edge, and flag stabilizers are prime to 13:

- 416 vertices \(\to 32\) cycles;
- 20,800 edges \(\to 1,600\) cycles;
- 41,600 flags \(\to 3,200\) cycles.

The G2 torus normalizer is only

\[
C_{13}{:}C_{12}.
\]

Thus the two sides share the same local \(C_{12}\) automorphism clock, but the abstract \(V_2\) realization carries one extra exact ambiguity:

\[
\boxed{C_{315}}.
\]

That is now the scalar ambiguity an actual weld has to eliminate or geometrize.

---

## Pass10001–10008 — the natural common 7,371 fusion fails spectrally

The full Q− and Q+ orthogonal coherent configurations are already nonisomorphic.  The canonical coarse Grassmann fusion remembers only whether two candidate two-spaces are identical, intersect in one projective point, or are disjoint.

Surprisingly, both signs have exactly the same valencies:

\[
\boxed{1,\ 320,\ 7050}.
\]

Let \(B\) be the incidence matrix between the 7,371 nondegenerate two-spaces and the 364 projective points of \(PG(5,3)\).  Then the point-intersection graph is

\[
A=BB^{\mathsf T}-4I.
\]

The exact spectra are different:

\[
Q^-:\quad
320^1,\ 86^{112},\ 80^{90},\ 68^{160},\ (-4)^{7008},
\]

\[
Q^+:\quad
320^1,\ 86^{142},\ 74^{90},\ 68^{130},\ (-4)^{7008}.
\]

The verifier certifies these without floating-point eigenvalue assumptions by exact integer annihilating polynomials for \(B^{\mathsf T}B\) and exact trace recovery of multiplicities.

So even the most natural nontrivial common fusion is not an isomorphism.  The trivial self/nonself complete-graph fusion is the only automatic intersection-only common fusion left.

---

## Pass10009–10016 — full residue-ring lift: \(\mathbf F_9[t]/(t^6)\) and an order-nine unitary operator

Put

\[
K=\mathbf Q_3(i),\qquad L=K(\zeta_9),\qquad t=\zeta_9-1.
\]

The extension \(L/K\) is totally ramified of degree six.  Directly,

\[
\Phi_9(1+t)
=t^6+6t^5+15t^4+21t^3+18t^2+9t+3,
\]

so modulo 3,

\[
\Phi_9(1+t)\equiv t^6.
\]

Hence the entire reduction is

\[
\boxed{
\mathcal O_L/3\mathcal O_L\cong \mathbf F_9[t]/(t^6)
}.
\]

This is stronger than the prior associated-graded statement: the six \(\mathbf F_9\) layers are the actual truncated residue algebra.

The pass also constructs an explicit regular nilpotent shift \(N\) with \(N^6=0\) and

\[
U=I+N,\qquad U^9=I,\qquad U^3\neq I,
\]

representing multiplication by \(1+t=\zeta_9\) up to power-basis reversal.  An explicit rank-six skew matrix \(A\) gives the nondegenerate Hermitian Gram matrix

\[
H=iA,
\]

and exactly

\[
U^\dagger H U=H.
\]

**Boundary:** this closes the complete mod-3/local residue module.  It does not yet construct an integral self-dual \(\mathcal O_L\)-lattice realizing the Niemeier lattice.

---

## Pass10017–10024 — joint Bargmann/F9 orientation detector

The Bargmann chirality and the \(F_9\) norm parity are independent representations of the same binary orientation bit.  Use an agree-or-erase decoder.

If Bargmann flips with probability \(p_B\), and a nonzero \(F_9\) symbol is independently corrupted with probability \(\epsilon\), uniformly to one of the other seven symbols, then exactly four of those seven lie in the opposite norm coset:

\[
p_N=\frac{4\epsilon}{7}.
\]

Acceptance is

\[
a=(1-p_B)(1-p_N)+p_Bp_N,
\]

and the error among accepted shots is

\[
e_{\rm cond}=\frac{p_Bp_N}{a}.
\]

Using the frozen moderate Bargmann error \(p_B=0.0035\) and a 5% F9-symbol corruption stress gives

\[
p_N=\frac1{35},\qquad
 a=\frac{67769}{70000}\approx0.96812857,
\]

\[
\boxed{
e_{\rm cond}=\frac7{67769}\approx1.03292\times10^{-4}
}.
\]

That is about a 34-fold reduction versus Bargmann alone, at about 96.8% acceptance.

**Boundary:** the decoder algebra is exact.  The Bargmann error comes from deterministic seeded simulation; F9 corruption and independence are explicit modeling assumptions, not hardware measurements.

---

# Three outside-box fronts

## Pass10025–10032 — universal \(\mathbf F_9\) Hermitianization

Let \((V,K)\) be symplectic over \(\mathbf F_3\) and let \(R\) be symplectic with \(R^2=-I\).  In the row-vector convention of the glue code define

\[
B=KR^{\mathsf T}.
\]

Then \(B\) is symmetric and nondegenerate.  With \(i^2=-1\) in \(\mathbf F_9\), define

\[
\boxed{h=B-iK}.
\]

Interpreting multiplication by \(i\) as \(R\), the exact identities are

\[
h(xR,y)=ih(x,y),
\qquad
h(x,yR)=-ih(x,y),
\qquad
h(y,x)=\overline{h(x,y)}.
\]

This was verified on the actual transverse Golay/E6 glue matrices.

The new parallel \(E_8/3E_8=H(3,9)\) construction is the dimension-four instance of this same Hermitianization mechanism; the glue construction is the dimension-six instance.  Thus the two independent appearances of \(\mathbf F_9\) have a common exact functorial origin.

---

## Pass10033–10040 — the shared \(C_{13}\) clock has a canonical orientation bit

Both clock normalizers carry

\[
\operatorname{Aut}(C_{13})=C_{12}.
\]

The unique index-two subgroup is \(C_6\), hence there is a canonical character

\[
\boxed{C_{12}\twoheadrightarrow C_2}.
\]

On the G2 side,

\[
N_{G_2(4)}(C_{13})=C_{13}{:}C_6,
\qquad
N_{G_2(4){:}2}(C_{13})=C_{13}{:}C_{12},
\]

so this \(C_2\) is exactly the outer-extension bit \(G_2(4){:}2/G_2(4)\).

On the abstract \(V_2\) Singer side it is Frobenius parity in the semilinear \(C_{12}=\langle x\mapsto x^2\rangle\).

This gives a precise candidate orientation character for a future weld.  It is not yet identified with the earlier Golay \(A_4<S_4\) orientation bit.

---

## Pass10041–10048 — the six \(\mathbf F_9\) layers are a full Bruhat–Tits chamber

Because \(L/K\) is totally ramified of degree six and

\[
3=u t^6
\]

for a unit \(u\), the \(\mathcal O_K\)-lattice chain

\[
\mathcal O_L
\supset t\mathcal O_L
\supset t^2\mathcal O_L
\supset\cdots
\supset t^5\mathcal O_L
\supset t^6\mathcal O_L=3\mathcal O_L
\]

has six one-dimensional \(\mathbf F_9\) quotients.  Therefore

\[
[\mathcal O_L], [t\mathcal O_L],\ldots,[t^5\mathcal O_L]
\]

form a **full chamber**, i.e. a maximal 5-simplex, in the Bruhat–Tits building of

\[
\boxed{PGL_6(\mathbf Q_3(i))}.
\]

Multiplication by \(\zeta_9=1+t\) preserves every ideal \(t^j\mathcal O_L\), so the order-nine cyclotomic action fixes this chamber vertex-by-vertex while acting nontrivially on the residue module.

This is the rank-six/residue-\(F_9\) analogue of the parallel cyclotomic lattice simplex in the \(PGL_{24}(\mathbf Q_2)\) building.

**Boundary:** this is standard Bruhat–Tits lattice-chain geometry applied to the exact local-field lift.  No p-adic holography or physical spacetime identification is claimed.

---

## Combined frontier

The packet changes the selector question from “find one miraculous common finite geometry” to a much sharper hierarchy:

1. the natural point and two-space Q−/Q+ identifications fail;
2. the abstract C13 clock is real but its Co0 realization is gated, not yet proved;
3. the two clock sides share a canonical \(C_{12}\) automorphism and \(C_2\) orientation, while the abstract V2 side has an extra \(C_{315}\) scalar torsor;
4. the arithmetic F9 side is now much stronger: the actual glue, the new E8 unitary branch, the full truncated residue ring, the order-nine unitary action, and the Bruhat–Tits chamber all fit one exact local-field/Hermitian package.

The next selector should therefore be sought as an **arithmetic/controller reduction of the C315 ambiguity**, not as another bare cardinality match.
