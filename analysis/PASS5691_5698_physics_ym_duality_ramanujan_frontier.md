# Passes 5691–5698 — finite Yang–Mills candidate, flat-ray duality, explicit Ramanujan depth

This packet executes the five carry-forward physics attacks from Pass5683–5690 and three independent falsifier-style probes.  It also repairs the prior packet's NumPy-version-sensitive Pass5685 replay gate.

## Pass5691 — what the affine `su(3)` does and does not give us

The nine affine sites have 36 links.  The 54 translation parallelograms span a 24-dimensional real boundary subspace, while the link cycle space has dimension 28.  Thus the minimal translation-plaquette complex has

\[
\dim H_1=28-24=4.
\]

Adding the twelve affine-line triangle boundaries raises the real face rank to 28 and kills this `H_1`.  Over `F_3` the combined face rank is only 26, leaving a two-dimensional modular quotient.  Therefore the choice of finite 2-cells is not innocuous: the exact affine point-line geometry has more than one natural face completion.  Over a field the corresponding cohomology has the same dimension, but the matrices actually computed here are the chain boundary and cycle quotient, so the certified object is homology.

Pass5686's determinant bracket has Killing form `-54` times the Euclidean metric on the zero-sum eight.  Hence a finite gauge candidate can be written

\[
F=da+\frac12[a,a],\qquad
S_{YM}=\frac1{2g^2}\sum_f\langle F_f,F_f\rangle,
\quad \langle x,y\rangle=-K(x,y)/54.
\]

The simple Lie algebra fixes the invariant quadratic form up to scale.  It does **not** fix the physical coupling `g`, and the finite geometry has not selected which admissible face set is dynamical.

There is also a useful no-go.  The old bundle `Z_3` translation acts as `I_9 tensor C_3`.  On the new base-adjoint sector `V_8 tensor span(1,1,1)` it acts trivially.  The old vertical `Z_3` connection therefore cannot simply be renamed as the new nonabelian adjoint connection.

## Pass5692 — the two magnetic flat rays are one duality orbit

The two Pass5685 flat-bond rays are related by the exact diagonal carrier involution

\[
D=\operatorname{diag}(+,+,+,+,-,-,-,-,-,-,-,-,+,+,+,+).
\]

`D^2=I`, it commutes with every signed element of the 96-element vector Segre stabilizer, and it is not itself in that group.  Adjoining it gives an order-192 kinematic extension.

The two rays are located by the bounded SVD/tolerance search inherited from Pass5685.
Flatness then quantizes their retained entries uniquely to \(0,\pm1\), and on those
stored integer sign matrices the final identity is exact:

\[
H_2=-D H_1D.
\]

Ordinary conjugation `K` is particle-hole on these imaginary Hamiltonians, so the antiunitary `DK` maps `H_1` to `H_2`.  The discrete two-ray ambiguity is therefore an exact identity of the quantized sign carriers, not two unrelated spectra.  The search that found those carriers remains numerical. Modulo this kinematic equivalence there is one ratio-two flat-bond class.  This still does not assign the two levels to physical particles or set an energy scale.

## Pass5693 — explicit Ramanujan levels 320 and 640

Starting from Pass5683's certified 160-vertex lift, each new 4-regular bipartite level is deterministically factored into four perfect matchings.  The six unions of two matchings are the locally balanced signings with negative degree two at every vertex.  Choosing the lowest signed spectral radius gives explicit connected lifts through 640 vertices.

The first two new signed radii are approximately

\[
3.4232028039,\qquad 3.3960725809,
\]

both below

\[
2\sqrt3\approx3.4641016151.
\]

The full 80/160/320/640 hierarchy is therefore explicitly Ramanujan to the recorded
eigensolver tolerance.  The graph lifts and signings are explicit combinatorial objects;
Pass5701 later supplies exact positive-semidefinite certificates for the spectral bounds.
What remains open is an automorphism-canonical all-level recursion: the preferred
matching-color pair may change, and deterministic factorization still depends on the
ordered graph presentation.

## Pass5694 — exact Jacobi expansion, but no unique `l_3`

For full bracket `b` and deleted vertical-cubic contribution `D`, the firewall bracket is `b-D`.  Bilinearity gives exactly

\[
J(b-D)=J(b)-B(b,D)-B(D,b)+J(D).
\]

Since the undeformed E8 bracket is Lie,

\[
J(b-D)=-B(b,D)-B(D,b)+J(D).
\]

The collision projector `C/3` determines the nine deleted supports, but it does not determine all coefficient signs and relative normalizations inside the full bracket.  Affine orientation fixes the sign of the separate determinant `su(3)` bracket, not the complete E8 operation.

Even after the Jacobiator is known, `d l_3=-J` fixes `l_3` only modulo `ker d`.  The existing restricted CE-H3/exhaustive homotopy tools remain the required coefficient-level uniqueness and obstruction gate.  This packet therefore closes the tempting stronger claim: collision support plus affine orientation do **not** uniquely determine the full `L_infinity` repair.

## Pass5695 — internal routing complexity and physical speed factor exactly

Take

\[
\mathcal H_{tot}=\mathcal H_{phys}\otimes\mathbb C^{N_n},
\qquad N_n=80\,2^n,
\]

and

\[
H_{tot}(p)=H_D(p)\otimes I+I\otimes H_{int}.
\]

Then

\[
E_{\alpha,\pm}(p)=\epsilon_\alpha\pm\sqrt{|p|^2+m^2},
\]

so

\[
\nabla_pE_{\alpha,\pm}=\pm\frac{p}{\sqrt{|p|^2+m^2}}
\]

is independent of the internal routing eigenvalue and cover level.  At the unitary level, tensoring the physical nearest-neighbor walk with an arbitrary internal unitary does not enlarge spatial support.  This is the clean finite statement behind the processor analogy: internal state/routing capacity may double repeatedly while the external split-step cone and `c_eff=ell/tau` remain unchanged in the tensor-separated model.

## Pass5696 — orientation breaking is not mandatory

Pass5686 was correct for the **plain** site representation: determinant-reversing affine maps flip the determinant bracket.  But define the affine determinant character

\[
\chi(g)=\begin{cases}+1&\det g=1,\\-1&\det g=2,\end{cases}
\]

and twist the augmentation action:

\[
\widetilde R(g)=\chi(g)R(g).
\]

Then the exact finite verifier gives

\[
[\widetilde R(g)f,\widetilde R(g)h]
=\widetilde R(g)[f,h]
\]

for all 432 elements of `AGL(2,3)`.  Thus the affine eight can be treated as an orientation pseudovector, restoring the full affine group as Lie-algebra automorphisms.  A physical `AGL -> ASL` spontaneous orientation breaking is therefore **not forced** by the algebra alone; bracket-sign domains require extra dynamics before they can be interpreted as physical phases or domain walls.

## Pass5697 — an internal adjoint gap, explicitly not the Yang–Mills mass gap

For every 4-regular Ramanujan level,

\[
L=4I-A,\qquad
\lambda_1(L)\ge4-2\sqrt3\approx0.5358983849.
\]

For the linearized affine adjoint field,

\[
L_{adj}=L\otimes I_8.
\]

There are eight constant zero directions, while every nonconstant graph mode is copied into the eight adjoint components and inherits the uniform finite graph gap.  This is useful as an internal routing/gauge solver gap.  It is **not** the Yang–Mills mass gap: it carries no physical energy units without a kinetic/metric scale and says nothing by itself about interacting infinite-volume confinement.

## Pass5698 — the simplest `three fiber phases = three generations` hypothesis fails

The bundle module is

\[
\mathbb C^{27}=\mathbb C^9\otimes\mathbb C[Z_3],
\qquad \mathbb C^9=\mathbf1\oplus V_8.
\]

If the vertical `Z_3` is ignored, ASL sees three copies of `1` and three copies of `V8`, giving an `M_3(C) direct-sum M_3(C)` commutant.  That is exactly why a generation-three interpretation looks tempting.

But retaining the actual vertical gauge action Fourier-decomposes the fiber into three inequivalent characters:

\[
\bigoplus_{k=0}^2
\left[(\mathbf1\otimes\chi^k)\oplus(V_8\otimes\chi^k)\right].
\]

The six joint `ASL x Z_3` constituents are multiplicity one, so the joint commutant is only `C^6`.  There is no gauge-commuting `M_3` mixing the three fiber phases as identical generations.  A true generation triplet must therefore come from a separate multiplicity space/intertwiner; the repo's independent `27 tensor 3` E8 factor remains a candidate only after such an intertwiner is demonstrated.

## Release correction inherited from Pass5683–5690

The previous workflow failure was traced to Pass5685's floating candidate-root deduplication under NumPy 2.5.2.  The theorem itself was not the failing condition.  The verifier now canonicalizes each projective flat-bond ray by its 60-bond sign pattern modulo global sign, which is the actual invariant being counted.

## Evidence boundary

The promoted content of this packet is finite graph, cochain, Lie-algebra, centralizer, tensor-product, representation and spectrum mathematics.  It does not claim a derived QCD action, physical gauge coupling, confinement theorem, Standard Model mass assignment, Yang–Mills mass gap, Lorentz-invariant spacetime continuum, numerical value of `c`, or three-generation derivation.
