# Passes 5675–5682 — the BdG moduli cone, an exact E6 locality projector, connected voltage refinement, and three physics no-go tests

This packet continues the physics-first line after Passes 5627–5634.  The theme is sharper than the previous packet: several structures that looked underdetermined can now be classified completely, while three especially tempting physical identifications fail exact representation or scaling tests.

## Pass 5675 — the full deck-odd Hamiltonian cone is only a Hermitian \(2\times2\) multiplicity problem

Pass5630 proved that the signed deck module for the 96-element vector Segre stabilizer is

\[
V_{16}\cong2A\oplus2\overline A,
\qquad \dim_{\mathbb C}A=4,
\]

with \(A\) non-real, and that stabilizer-equivariant Hermitian Hamiltonians satisfying ordinary-conjugation particle-hole symmetry form a four-real-dimensional vector space.

Schur's lemma now closes that space completely.  After choosing multiplicity coordinates every allowed Hamiltonian has normal form

\[
\boxed{
H_X=(I_A\otimes X)\oplus(I_{\bar A}\otimes-\overline X),
\qquad X=X^\dagger\in M_2(\mathbb C).
}
\]

If the two eigenvalues of \(X\) are \(\lambda_1,\lambda_2\), then

\[
\boxed{
\operatorname{spec}H_X=
\lambda_1^4\oplus\lambda_2^4\oplus(-\lambda_1)^4\oplus(-\lambda_2)^4
}
\]

and every allowed operator obeys

\[
\boxed{
H^4-(\lambda_1^2+\lambda_2^2)H^2+\lambda_1^2\lambda_2^2I=0.
}
\]

Equivariant unitary changes diagonalize \(X\).  Therefore, after quotienting by basis and one overall nonzero energy scale, **one continuous dimensionless level ratio remains**.  The magnetic point is the special choice with absolute levels \(3,6\):

\[
H_{\rm mag}^4-45H_{\rm mag}^2+324I=0,
\qquad |\lambda_2/\lambda_1|=2.
\]

So the earlier ratio \(2\) is not merely perturbatively unprotected: it is one point in a continuous symmetry-allowed moduli space.

## Pass 5676 — an exact gauge-invariant selector exists, but it is locality rather than gauge symmetry

For a cubic support \(T\) in the reconstructed \(E_6\) bundle, let \(n_b(T)\) be the number of its three vertices lying over base site \(b\in AG(2,3)\).  Define the same-fiber collision number

\[
\boxed{
\mathcal C(T)=\sum_b\binom{n_b(T)}2
=\frac{\|n(T)\|^2-3}{2}.
}
\]

Then

\[
\mathcal C=0
\quad\text{on every one of the 36 horizontal line lifts},
\]

where the occupancy is \(1+1+1\), while

\[
\mathcal C=3
\quad\text{on every one of the nine complete vertical fibers}.
\]

Thus on the 45-dimensional cubic-support basis,

\[
\boxed{
C_{45}=0^{36}\oplus3^9,
\qquad
P_H=I-C_{45}/3,
\qquad
P_V=C_{45}/3.
}
\]

The construction is invariant under arbitrary independent \(\mathbb Z_3\) translations within every fiber because those translations do not change the projection occupancy \(n_b\).

This gives an exact mechanism **if** the physical action imposes a hard-core/fiber-locality rule: at most one field insertion from each gauge fiber.  In that limit the vertical nine vanish exactly.

But the additional principle is genuinely additional.  The \(9\times12\) point-line incidence matrix of \(AG(2,3)\) satisfies

\[
BB^T=3I_9+J_9,
\qquad\operatorname{rank}B=9.
\]

Hence the horizontal line occupancies already span the whole base site space.  No linear projector acting only on base \(C^0\) can preserve every horizontal line while killing every vertical site vector.  The collision invariant is the first nonlinear/local separator.

## Pass 5677 — the connected cover tower exists after all

Pass5629 proved that repeating the same Kronecker \(C_2\) lift disconnects after one stage.  The correct statement is cohomological rather than absolute.

The W33 point-line Levi graph has

\[
|V|=80,
\qquad |E|=160,
\qquad \beta_1=81,
\qquad d=4.
\]

For a connected graph, a \(\mathbb Z_2\) voltage cover is connected precisely when the cycle-voltage image generates \(\mathbb Z_2\), equivalently when the voltage class is nonzero in \(H^1(G;\mathbb F_2)\).

At each level choose a spanning tree and one non-tree chord, assign voltage one to that chord and zero elsewhere, and then repeat the procedure **on the newly obtained graph**.  The chord's fundamental cycle has odd voltage, so each lift is connected.

This produces an indefinite hierarchy with exact counts

\[
\boxed{
|V(L_n)|=80\,2^n,
\qquad
|E(L_n)|=160\,2^n,
\qquad
\beta_1(L_n)=1+80\,2^n,
\qquad d=4.
}
\]

The old no-go is now precisely understood: pulling the first voltage class back to the cover trivializes the class that created that cover, so lifting by it again duplicates components.  A **fresh** nonzero cohomology class repairs connectivity.

## Pass 5678 — connected is not the same as continuum-like

For every \(2\)-lift the sheet-parity basis gives the standard exact decomposition

\[
\boxed{
A_{\rm lift}\simeq A_{\rm base}\oplus A_\sigma,
}
\]

where \(A_\sigma\) is the signed adjacency matrix.  The first five deterministic tower levels have verified distinct-adjacency-eigenvalue counts

\[
\boxed{5,13,29,61,125.}
\]

So fresh voltage classes really do proliferate spectral scales rather than simply duplicating the old spectrum.

However, the one-chord construction is spectrally pathological in a useful way.  A single negative base edge produces exactly **two** cross-sheet edges.  For a four-regular \(N\)-vertex base, the two equal sheet halves therefore have conductance at most

\[
\Phi\le \frac{2}{4N}=\frac1{2N}.
\]

The easy Cheeger inequality then yields for the next combinatorial Laplacian gap

\[
\boxed{\lambda_1\le\frac4N.}
\]

Hence the deterministic tower becomes nearly disconnected even though it stays topologically connected.  This is not an isotropic continuum.  The next serious target is a **balanced voltage signature** whose new signed spectrum remains controlled; this is exactly the kind of issue studied in the general 2-lift literature.

## Pass 5679 — the old section operator contains both intrinsic sectors as its real and imaginary parts

Pass5634 wrote the intrinsic two-sheet matrix as

\[
H_{32}=\begin{pmatrix}A&B\\B&A\end{pmatrix}.
\]

The new exact identity is

\[
\boxed{B=\overline A.}
\]

Therefore one complex Hermitian section matrix reconstructs the whole intrinsic lift:

\[
\boxed{
H_{32}=\begin{pmatrix}A&\bar A\\\bar A&A\end{pmatrix},
\qquad
H_+=2\operatorname{Re}A,
\qquad
H_-=2i\operatorname{Im}A.
}
\]

Because \(A=A^\dagger\), \(\operatorname{Re}A\) is real symmetric and \(\operatorname{Im}A\) is real skew-symmetric.  Thus the class-D-like signed block is literally the imaginary/antisymmetric part of the old section-dependent magnetic matrix; the even block is its real/symmetric part.

This gives the earlier correction a much cleaner interpretation.  The section matrix is not intrinsic **alone**, but it is a complex parent coordinate.  Restoring its conjugate sheet splits its real and imaginary data into the two intrinsic deck sectors.

The exact one-sheet Schur operator becomes

\[
H_{\rm eff}(E)
=A+\bar A(E-A)^{-1}\bar A.
\]

Its fifteen distinct bare poles do not coincide with any physical eigenvalue of \(H_{32}\); they cancel against the prefactor in

\[
\det(E-H_{32})
=\det(E-A)\det(E-H_{\rm eff}(E)).
\]

They are decimation/coordinate poles rather than physical particle levels.

## Pass 5680 — the class-D Pfaffian bit is trivial

For \(H=iS\) with \(S\) real skew, the finite zero-dimensional class-D invariant may be represented by a Pfaffian sign once an orientation convention is chosen.  Pass5675 forces fourfold multiplicities, hence

\[
\boxed{|\operatorname{Pf}S|=|\lambda_1\lambda_2|^4.}
\]

Three representatives cover the three gapped signature components of the Hermitian \(2\times2\) multiplicity matrix:

- positive definite: \(J=H_{\rm mag}/2-H_{\rm mag}^3/54\), spectrum \(\pm1\) each eightfold;
- negative definite: \(-J\);
- indefinite: \(H_{\rm mag}\), levels \(3,6\).

In the canonical deck ordering all three have the same Pfaffian sign.  In particular

\[
\boxed{
\operatorname{Pf}S_{\rm mag}
=-(3\cdot6)^4
=-104976.
}
\]

Thus the usual \(0D\) class-D \(\mathbb Z_2\) bit is **trivial on the entire stabilizer-equivariant gapped cone**.  It neither protects the ratio \(2\) nor selects one mass signature as physical.

## Pass 5681 — the vertical sector is genuinely \(1+8+28\), but not an eight-gluon adjoint

The full affine group of the nine base sites is

\[
AGL(2,3)=\mathbb F_3^2\!:\!GL(2,3),
\qquad |AGL(2,3)|=432,
\]

acting doubly transitively on the nine sites.  Therefore

\[
\boxed{\mathbb C^9=\mathbf1\oplus V_8}
\]

with \(V_8\) irreducible.

The complete nine-site one-skeleton has 36 oriented-edge coordinates.  Its incidence map has rank eight, leaving cycle dimension 28.  Representation-theoretically,

\[
\Lambda^2(\mathbf1\oplus V_8)
=V_8\oplus\Lambda^2V_8,
\]

so the exact cycle module is

\[
\boxed{Z_1(K_9)\cong\Lambda^2V_8,\qquad\dim=28.}
\]

This is a genuine \(1+8+28\) gauge-complex hierarchy.

But the tempting \(8=\dim\mathfrak{su}(3)\) reading fails the structural test it must pass.  Character theory gives

\[
\boxed{
\dim\operatorname{Hom}_{AGL(2,3)}(\Lambda^2V_8,V_8)=0.
}
\]

There is no nonzero affine-equivariant alternating bracket \(V_8\times V_8\to V_8\).  Therefore the eight site-augmentation modes cannot be the \(SU(3)\) adjoint/eight gluons while retaining full \(AGL(2,3)\) symmetry.  The count was real; the Lie algebra was not.

## Pass 5682 — what the finite geometry really says about a speed limit

Every graph cover is locally the same four-neighbour graph.  A nearest-neighbour discrete propagator therefore has the exact dimensionless causal statement

\[
\boxed{\Delta d_{\rm graph}\le1\quad\text{per tick}}
\]

at every refinement level.

If a graph edge is assigned physical length \(\ell_n\) and one update tick physical duration \(\tau_n\), then

\[
\boxed{c_n=\ell_n/\tau_n.}
\]

The cover topology fixes neither quantity.  It adds sheets and state-space capacity but does not geometrically subdivide an abstract edge.

If one separately assumes that the tower refines a fixed physical \(d\)-volume, then \(N_n=2^nN_0\) would imply

\[
\ell_n/\ell_0=2^{-n/d}.
\]

Maintaining a finite nonzero limiting speed requires the time scale to obey the same law,

\[
\tau_n/\tau_0=2^{-n/d}.
\]

Neither \(d\) nor the absolute calibration \(\ell_0/\tau_0\) is fixed by graph covering.  So the photon/processor-speed intuition has a precise finite core—one local hop per update—but total internal node count does not determine the SI value of \(c\).

## External boundary

The free-fermion/class-D language is standard; see Kitaev, arXiv:0901.2686.  The 2-lift old/new spectrum decomposition and controlled-signature problem are standard; see Bilu–Linial, arXiv:math/0312022.  Voltage-derived graph covers are likewise standard graph theory.  Exact citations and scope are recorded in `analysis/PASS5675_5682_external_prior_art.md`.

## Overall evidence firewall

This packet proves finite representation, bundle-projection, graph-cover, spectral, Pfaffian, cochain, and causal-scaling statements.  It does **not** derive Standard Model masses, an \(SU(3)\) gauge theory, interacting topological order, a continuum spectral dimension, Lorentz invariance, the SI speed of light, or a unique physical refinement tower.
