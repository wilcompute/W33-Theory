# Inclusive three-particle KK thresholds from a five-point superamplitude

The [noncompact graviton calculation](2026-11-16_noncompact_graviton_threshold.md) derived one polarized channel. Here the spin sum is evaluated first for eleven-dimensional graviton descendants and then for the entire eleven-dimensional supergravity multiplet. Work at leading supergravity order and fix a signed, labeled, noncollinear KK charge triangle. Its three masses are \(a,b,c\), its rest energy is \(M=a+b+c\), and \(\Delta=\sqrt{s}-M\). Strip \((\kappa_5/2)^3\) from each tree amplitude. Retain the previous Lorentz-invariant phase-space convention, with no permutation factor for the fixed charge labels.

## Exactly twelve graviton configurations for the circular beam

Use the beam \(Z\otimes Z\) on both incoming legs in the all-outgoing convention of the prior calculation. Under rotations in the real noncompact spectator plane defining \(Z\), each Yang–Mills copy has incoming charge \(+2\) and the three outgoing vector polarizations must have charges \((-1,-1,0)\) in some order. The neutral leg can only have either of the two helicities in the momentum four-plane. A neutral polarization along any other spectator axis vanishes by reflection of that axis, since it occurs only once and the momenta and other polarizations are fixed. These are statements about vector spin under the spectator rotation. The separate compactification momenta still label the KK charges.

In each gauge copy the positive plane-helicity amplitude uses the MHV numerator \(N_j=\langle12\rangle^2\langle kl\rangle^2\), where \(j\) is the neutral leg and \(k,l\) are the other two final legs. The negative plane-helicity amplitude is its CPT-conjugate component with square brackets. In the five-point KLT kernel a mixed choice of the two helicities vanishes. For the angle denominators the ratio of first to second left denominators is \(-q\), and it is \(q\) on the right, with \(q=\langle12\rangle\langle34\rangle/(\langle13\rangle\langle24\rangle)\). Conjugating one copy therefore gives \(-|q|^2\) in that ratio product. The ratio of the Mandelstam factors cancels \(|q|^2\), so the two KLT terms cancel. This argument applies equally to the case where the neutral legs differ between copies. [Five-point field-theory KLT](https://arxiv.org/abs/0707.1035) · [Component generating amplitudes](https://arxiv.org/abs/0805.0757)

For each common helicity, a coincident neutral leg gives three possible pure plane-helicity graviton states. Distinct neutral legs give three unordered pairs of split states. On a split leg the normalized graviton tensor is the symmetric sum of \(\bar Z\otimes g\) and \(g\otimes\bar Z\), divided by \(\sqrt2\), where \(g\) is the plane-helicity polarization vector. All surviving tensors are traceless. The two left-right terms in the split case add coherently and compensate the two factors \(1/\sqrt2\). Thus one same-helicity configuration for each pair \(j\le k\) has stripped amplitude of magnitude \(|C N_j N_k|\), where \(C\) is the helicity-independent MHV prefactor. The opposite common helicity yields a second orthogonal copy.

Put \(w_j=M-2m_j>0\), where \(m_j\) is the mass on outgoing leg \(j\), \(j=3,4,5\). At threshold \(|N_j|^2=M^6w_j^2\), and the prior pure metric-scalar component fixes \(|C|^2=1/[M^6(abc)^2]\). The sum over final graviton tensor polarizations is therefore
\[
 \sum_{\mathrm{graviton}}|\widehat{\mathcal M}_5|^2
 =\frac{2M^6}{(abc)^2}
       \left(\sum_j w_j^4+\sum_{j<k}w_j^2w_k^2\right).
\]
Only twelve orthonormal final configurations contribute in the indicated helicity and spectator-spin basis at rest. This graviton-only formula uses the specified circular incoming beam.

## A polarization-independent full supermultiplet sum

At any nondegenerate real five-point kinematics, momentum conservation puts the five eleven-dimensional null momenta in a Lorentzian subspace of dimension at most four. In this plane the local tree amplitude is the four-dimensional \(\mathcal N=8\) superamplitude. The 256 one-particle states are the 44 graviton, 84 three-form, and 128 gravitino polarizations organized in a different basis. The restriction is legitimate for a tree since every internal momentum is a sum of external momenta and stays in the same plane. At five points there are just the MHV and CPT-conjugate sectors, with prefactors \(C\) and \(\overline C\) up to a convention-dependent phase. [Eleven-dimensional supergravity and the four-dimensional SU(8) formulation](https://doi.org/10.1016/0370-2693%2885%2991030-5) · [Supersymmetry Ward identities](https://arxiv.org/abs/0911.3169) · [Tree superamplitude generating functions](https://arxiv.org/abs/0805.0757)

For one of the eight R indices write the outgoing spinor rows as \(x,y\in\mathbb C^3\). In the center of mass \(\sum_{j=3}^5\lambda_j\lambda_j^\dagger=\sqrt{s}\,I_2\), so \(x,y\) are orthogonal with squared norm \(\sqrt{s}\) each. Choose incoming spinors \(i\,s^{1/4}(1,0)\) and \(i\,s^{1/4}(0,1)\) in the all-outgoing convention. For that R index, the component of \(\delta^{16}(Q)\) maps the four input occupation patterns to outgoing exterior forms proportional to
\[
 x\wedge y,\qquad i\,s^{1/4}y,\qquad -i\,s^{1/4}x,\qquad -\sqrt{s}.
\]
They are orthogonal, each with squared norm \(s\). The common image is \(\bigwedge U\) for \(U=\operatorname{span}_{\mathbb C}(x,y)\). Taking the tensor product over the eight indices multiplies the squared norms to \(s^8\). Grassmann reordering can be absorbed into input and output basis phases. CPT complements the incoming bits and takes the conjugate Hodge dual of the outgoing forms. The dual of \(\bigwedge U\) contains an exterior factor in \(U^\perp\), so the two outgoing images are orthogonal even for superpositions of incoming components.

Consequently, for any normalized incoming state at the fixed momenta, the complete final multiplet sum is
\[
 \sum_{\mathrm{multiplet}}|\widehat{\mathcal M}_5|^2
 =2s^8|C|^2
 =2|\widehat{\mathcal M}^{\rm plane}_{--+++}|^2 .
\]
Here the reference component uses the momentum-plane graviton helicities in the all-outgoing convention. This is a local tree matrix-element sum at fixed outgoing momenta. It neither integrates over the compactification spectrum nor changes its external-state normalization. At rest \(s=M^2\), so the full weight is \(2M^{10}/(abc)^2\). As an independent component check on the circular beam, the four R indices unoccupied on both incoming legs each choose a pair among the three outgoing slots. Thus there are \(3^4=81\) MHV components and \(81\) CPT-conjugate components, with total fixed by \(A_{34}+A_{35}+A_{45}=M^2\), where \(A_{ij}=|s_{ij}|\).

## Inclusive onset and calibrated inverse data

Multiplying by the prior three-body phase space \(abc\,\Delta^3/[48(2\pi)^3M^2]\) gives the **full multiplet** contribution to \(2\operatorname{Im}\mathcal M_{\rm forward}\), with the common \((\kappa_5/2)^6\) removed,
\[
 \frac{M^8}{24(2\pi)^3 abc}\,\Delta^3+o(\Delta^3).
\]
This is an all-massive cut of a specified signed, labeled charge triangle. Together with the three measured masses it calibrates the rank-two Gram multiplicity in the inverse result. When combining all charge triangles, each physical final state is counted once, and all triangles with the same ordered masses have the same calibration. The formula applies at a noncollinear threshold where the tree is smooth. Zero modes, collinear charge thresholds, and other two-loop cuts are separate sectors.

For the circular incoming beam the graviton-only fraction of this coefficient is \(\big(\sum_j w_j^4+\sum_{j<k}w_j^2w_k^2\big)/M^4\). Since \(\sum_j w_j=M\), the fraction is minimized at equal masses and then equals \(2/27\). Indeed the numerator equals \(\tfrac12[(\sum_j w_j^2)^2+\sum_j w_j^4]\) and both sums are minimized at equality. The [verifier](toe_20261116_kk_unitarity.py) checks the twelve tensor contributions, the 81-term MHV component sum, the single-index Gram matrices and Hodge orthogonality, and the independent relativistic phase-space integral. The [certificate](../data/toe_20261116_kk_unitarity.json) gives coefficients per signed triangle for both isospectral tori.
