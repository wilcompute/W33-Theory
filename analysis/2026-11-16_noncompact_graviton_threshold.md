# Noncompact graviton scattering resolves the degree-two torus theta series

The [previous torus calculation](2026-11-16_kk_unitarity_and_isospectral_tori.md) found two isospectral six-tori whose first all-massive three-particle energies differ. The five-point calculation here exhibits the effect with incoming five-dimensional gravitons whose tensor polarizations are entirely noncompact. It also gives the absolute cubic onset coefficient in a specified polarization channel and an inverse map from mass-resolved cuts to ordered lattice Gram matrices.

## A purely noncompact polarization

Take a strict internal triangle with momenta \(v,w,-v-w\) and masses \(a,b,c>0\). Its rest threshold is \(M=a+b+c\). At threshold the eleven-dimensional null momenta of the two incoming and three outgoing states are in the Minkowski four-plane spanned by time, the noncompact beam axis, and the internal \(v,w\) plane. Choose two orthonormal noncompact axes \(e,f\) orthogonal to the beam and put \(Z=(e+if)/\sqrt2\). Both \(Z\otimes Z\) and \(\bar Z\otimes\bar Z\) are unit transverse traceless graviton polarizations.

Use the all-outgoing convention with \(Z\otimes Z\) on legs \(1,2\), \(\bar Z\otimes\bar Z\) on the KK legs \(3,4\), and a positive plane helicity on leg \(5\). The conjugates of the all-outgoing states on \(1,2\) give the physical incoming polarizations. In each Yang–Mills copy the transverse directions \(Z,\bar Z\) behave as a conjugate scalar pair for momenta in the four-plane. They can be represented by \(\phi^{12},\phi^{34}\) in the dimensionally reduced bosonic gauge amplitude. The \(\delta^8(Q)\) component with \(\phi^{12}_1,\phi^{12}_2,\phi^{34}_3,\phi^{34}_4,g^+_5\) has numerator \(\langle12\rangle^2\langle34\rangle^2\) for all orderings. The four scalar fields are polarizations of the parent gluons. Their tensor squares project onto pure Einstein gravitons, and the on-shell tree amplitudes use ordinary Einstein interactions. [Elvang, Freedman and Kiermaier, MHV generating function](https://arxiv.org/abs/0808.1720) · [Five-point field-theory KLT](https://arxiv.org/abs/0707.1035) · [Kawai, Lewellen and Tye](https://doi.org/10.1016/0550-3213%2886%2990362-7)

Let \(A_{ij}=|s_{ij}|=|\langle ij\rangle|^2\). Write \(\widehat{\mathcal M}_5\) for the KLT amplitude with the common coupling \((\kappa_5/2)^3\) and irrelevant phase removed, using canonically normalized KK states. The two KLT terms have ratio \(-q^2/|q|^2\) with \(q=\langle12\rangle\langle34\rangle/(\langle13\rangle\langle24\rangle)=1-u_4/u_3\) and \(u_j\) the unit complex directions of the internal momenta. Thus the squared sum relative to the squared first term is \(2+2\cos\angle(v,w)>0\). The first term squared is
\[
 \frac{(A_{12}A_{34})^4}{A_{23}A_{45}A_{51}A_{14}A_{35}A_{52}} .
\]
At threshold \(A_{12}=M^2\), \(A_{34}=M(M-2c)\), and \(A_{1j}=A_{2j}=M m_j\) for each final leg. The corresponding \(A_{35},A_{45}\) take the same form as \(A_{34}\) with the complementary mass. Using \(2+2\cos\angle(v,w)=(M-2a)(M-2b)/(ab)\) gives
\[
 |\widehat{\mathcal M}_5|^2=\frac{M^6(M-2c)^4}{(abc)^2}.
\]
The strict triangle inequality makes this positive for every noncollinear charge pair, for any of the three choices of the plane-helicity leg. Holding the two noncompact incoming axes fixed works for every orientation of the internal triangle. For comparison the prior metric-scalar polarization has stripped squared amplitude \(M^{10}/(abc)^2\) under the same convention.

## Absolute onset of the specified three-particle channel

Use \(d^4p/[(2\pi)^4 2E_p]\) per final particle and \((2\pi)^5\delta^5\) for conservation. Fix distinguishable charge labels without summing over orders. With excess energy \(\Delta=\sqrt{s}-M\), elimination of the third spatial momentum gives the nonrelativistic quadratic form with \(2\times2\) mass matrix in each spatial coordinate,
\[
 B=\begin{pmatrix}1/a+1/c&1/c\\1/c&1/b+1/c\end{pmatrix},
 \qquad \det B=M/(abc).
\]
The eight-dimensional energy-shell integral contributes \((2\pi)^4\Delta^3/[6(\det B)^2]\). Hence
\[
 \Phi_3=\frac{abc}{48(2\pi)^3 M^2}\Delta^3+o(\Delta^3).
\]
Equivalently one can factor the exact relativistic phase space into two sequential two-body phase spaces integrated over their shared invariant mass. The verifier uses this independent integral at decreasing \(\Delta\) and compares it with the eight-dimensional Gaussian coefficient.

The selected final polarization therefore contributes to \(2\operatorname{Im}\mathcal M_{\rm forward}\), with the common factor \((\kappa_5/2)^6\) removed, an onset
\[
 \frac{M^4(M-2c)^4}{48(2\pi)^3 abc}\,\Delta^3+o(\Delta^3).
\]
This is one signed, labeled charge triangle and one polarization choice. Its coefficient also gives a lower bound on the inclusive coefficient for the same incoming state. The lower-threshold torus consequently has a positive all-massive three-KK-graviton cut for pure noncompact graviton beams just above \(15.3416602\). The other torus has no contribution from this sector before \(15.6662155\). Other intermediate species and states containing zero KK charge are outside this sector. [Cutkosky](https://doi.org/10.1063/1.1703676)

## What mass-resolved scattering reconstructs

An ordered mass triple gives a pair Gram matrix directly:
\[
 (a^2,b^2,c^2)\ \longmapsto\
 \begin{pmatrix}a^2&(c^2-a^2-b^2)/2\\(c^2-a^2-b^2)/2&b^2\end{pmatrix}.
\]
For fixed noncompact incoming polarization, any two ordered internal triangles with the same Gram matrix are related by an orthogonal transformation of the local internal frame. The leading pure-graviton production rate summed over final graviton tensor polarizations therefore has the same coefficient for each such triangle. This uses the local flat-space tree vertex and a common normalization by the compactification volume. The explicit polarized calculation proves that the universal inclusive weight for a strict triangle is positive. Equivalently, for the selected final polarization the universal weight above is explicit. With mass-resolved and ordered channels, division by the per-triangle weight recovers the ordered rank-two Gram multiplicities. Degenerate masses can be treated with labeled counting and the corresponding common permutation factor. An untagged scan in total energy alone can merge distinct mass triples.

Rank-one coefficients are already fixed by the one-particle theta series. Write \(r(\lambda)\) for the number of lattice vectors of squared norm \(\lambda>0\), and \(P(\lambda)\) for the number of unoriented primitive directions of that squared norm. Then \(r(\lambda)=2\sum_{k\ge1}P(\lambda/k^2)\). Möbius inversion recovers \(P\), and each primitive line supplies the ordered pairs indexed by integers \(i,j\) with Gram entries \(\lambda i^2,\lambda j^2,\lambda ij\), excluding \((0,0)\) until the final rank-zero term. Together the ordinary mass spectrum and the ordered three-body cut data therefore determine the degree-two theta series of the KK momentum lattice. This is a reconstruction of a definite lattice invariant. The question of whether it uniquely determines every six-torus remains open in this calculation. [Two-loop charge correlations in toroidal supergravity](https://arxiv.org/abs/hep-th/9910055)

## When total-energy scans separate the thresholds

For almost every torus shape, the ordinary KK masses suffice to decode the unordered mass triple from a rank-two threshold energy. For each primitive direction \(u\), up to sign, put \(L_u(Q)=u^TQu\). Vectors on the same primitive line have masses \(k\sqrt{L_u(Q)}\) in common units. Distinct primitive directions give pairwise nonproportional linear polynomials in the entries of the form \(Q\). Over the rational-function field in those entries, the square classes of any finite list of distinct \(L_u\) are independent. This follows by taking the valuation along each distinct linear prime. In the extension obtained by adjoining the square roots, an automorphism can flip each \(\sqrt{L_u}\) independently. Therefore a relation with constant coefficients between distinct primitive masses cannot hold identically. Each nontrivial integer relation vanishes on a measure-zero real-analytic set. There are only countably many such relations. The argument holds at fixed determinant as well, since each relation is homogeneous under rescaling \(Q\).

For a shape outside these exceptional sets the primitive masses are rationally independent. A noncollinear charge triangle uses three distinct primitive directions. Its total rest energy determines the integer coefficient on each of those directions, so any alternative decomposition into three KK masses gives the same unordered masses. The primitive masses themselves can be recovered from the ordinary mass list by the rank-one inversion above. This generic statement decodes the threshold positions of the three-body sector. Ordered or mass-resolved data remain a direct way to obtain multiplicities, and the argument requires a separately identifiable three-particle onset.

An exact square-lattice control shows what fails in a symmetric metric. The pairs \(((12,9),(0,-4))\) and \(((12,0),(-6,8))\) give distinct mass triples \((4,13,15)\) and \((10,10,12)\) at the same total energy \(32\). Both are strict charge triangles. The example embeds isometrically in a six-dimensional cubic momentum lattice. The equality of total energy therefore does not identify the underlying Gram matrix on all tori.

The [verifier](toe_20261116_kk_unitarity.py) evaluates both KLT terms, checks the threshold coefficient for each choice of the plane-helicity leg, and tests the rank-one and rank-two reconstruction and the energy collision on square-lattice data. The numerical values are in the [generated certificate](../data/toe_20261116_kk_unitarity.json).
