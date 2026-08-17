# Passes 5725--5732: torsion-center pairing, higher-algebra rank, finite family bridge, and three hard falsifiers

## Scope and evidence boundary

This packet starts from the exact Pass5720--5724 affine-face theorem
\[
H_1(X;\mathbb Z)\cong (\mathbb Z/3)^2
\]
with translation kernel \(\mathbb F_3^2\) and residual homology image \(GL(2,3)\), and from the corrected Pass5704--5711 Wilson/generation/\(L_\infty\) frontier.  Everything below is a finite graph, group, representation, cohomology, switching-class, or higher-algebra statement.  Nothing here identifies QCD color, observed particle generations, measured masses, confinement, a continuum anomaly, spacetime, or laboratory physics.

The packet also corrects one finite-group label from Pass5708.  The matrices called there
\[
T=\operatorname{diag}(1,\omega,\omega^2),\qquad C=(012)
\]
are the qutrit Weyl operators \(Z\) and \(X\).  They generate the order-27 Heisenberg group \(H_3\), not the full Lie group \(SU(3)\).  The scalar-commutant result remains correct because the three-dimensional Schrödinger representation of \(H_3\) is already irreducible.  The separate statement that the defining irreducible \(SU(3)\) module has scalar commutant remains true by Schur's lemma; the old finite generator test was simply mislabeled.

## Pass 5725 -- the torsion doublet is observable only through a charge pairing

Let
\[
H=(\mathbb Z/3)^2,
\]
and write the Pass5723 residual action as
\[
Q(M)=P^{-1}(\det M\,M^T)P,\qquad M\in GL(2,3).
\]
Exact enumeration of all 48 matrices gives:

* the only fixed covector in \(H^*\) is zero;
* the eight nonzero covectors form one orbit;
* every nonzero \(h\in H\) is detected by exactly six of the eight nonzero covectors.

For \(t\in\{1,2\}\) the finite Wilson character
\[
W_{t,\ell}(h)=\omega^{t\ell(h)}
\]
is therefore nontrivial on every nonzero torsion class for a suitable nonzero charge \(\ell\).  The canonical affine-equivariant object is not a scalar character but the evaluation pairing
\[
H^*\times H\longrightarrow \mathbb F_3,
\]
with the charge transformed contragrediently.  There is no canonical nonzero full-\(GL(2,3)\)-equivariant map \(H\to Z_3\) without choosing a charge direction and thereby reducing the residual symmetry.

This sharpens Pass5709: the missing triality/character layer exists abstractly, but no physical matter representation follows from it.

## Pass 5726 -- exact firewall Jacobiator rank is 234

The firewall-filtered binary bracket was replayed on the complete 248-dimensional E8 basis.  The computation enumerates all
\[
\binom{248}{3}=2{,}511{,}496
\]
unordered triples.  Exactly
\[
\boxed{32{,}400}
\]
triples have nonzero Jacobiator.

The integer Jacobiator rows were reduced independently modulo
\[
1{,}000{,}003,\qquad 1{,}000{,}033.
\]
Both modular ranks are
\[
\boxed{234}.
\]
The union of occupied output basis coordinates also has size 234.  Therefore
\[
\operatorname{rank}_{\mathbb F_p}J\le \operatorname{rank}_{\mathbb Q}J
\le |\operatorname{supp}_{\rm out}J|
\]
forces
\[
\boxed{\operatorname{rank}_{\mathbb Q}J=234}.
\]
In fact \(\operatorname{im}J\) is the entire coordinate subspace on those 234 occupied basis coordinates, leaving an untouched coordinate complement of dimension
\[
\boxed{248-234=14}.
\]

This converts the Pass5707 correction into a sharp size theorem.  Any two-term arity-three repair
\[
l_1:Y\to\mathfrak g,\qquad l_1(l_3)=-J
\]
must satisfy
\[
\operatorname{im}J\subseteq\operatorname{im}l_1,
\]
so necessarily
\[
\boxed{\dim Y\ge 234}.
\]
At arity three the lower bound is attained by
\[
Y=\operatorname{im}J,\qquad l_1=\iota,\qquad l_3=-J.
\]
Because \(l_1\) is injective in this minimal model, \(l_3\) is unique there.  For a larger \(Y\), two lifts differ by a \(\ker l_1\)-valued trilinear map.

This does **not** certify the arity-four or higher \(L_\infty\) identities.  Those remain independent equations.  It does, however, rule out any small auxiliary repair of the actual firewall Jacobi defect.

## Pass 5727 -- a finite torsion-to-E8-family intertwiner exists

The qutrit Weyl pair obeys
\[
ZX=\omega XZ,
\]
and generates
\[
|H_3|=27,\qquad |Z(H_3)|=3,
\qquad H_3/Z(H_3)\cong \mathbb F_3^2.
\]
After choosing a basis of the affine torsion doublet, the projective map
\[
e_1\mapsto [X],\qquad e_2\mapsto [Z]
\]
identifies the torsion quotient with the Heisenberg quotient.  The corresponding Schrödinger representation acts on the same \(\mathbb C^3\) multiplicity factor used in the E8 \((27,3)\) branch.  In the chosen bases, the finite intertwiner is literally the identity on that \(\mathbb C^3\) carrier.

This is a genuine finite-module bridge.  Its ambiguity is also exact: torsion basis, orientation, and central-character choice.  It does **not** identify the affine Lie \(\mathfrak{su}(3)\) found in earlier passes with the E8 family \(SU(3)\) Lie algebra; a common infinitesimal action remains to be constructed or ruled out.

## Pass 5728 -- spectral radius removes the raw three-colour label on the known Ramanujan candidate sets

The six 2-of-4 matching signings at each known level occur in complementary pairs, giving three complement-switching classes.  Signed spectral radius
\[
\rho(A_\sigma)
\]
is invariant under vertex switching and graph automorphism.  At parent sizes \(160,320,640,1280\), the three class radii are strictly ordered:

* 160: \(3.4232028039<3.4385989393<3.4649402103\);
* 320: \(3.3960725809<3.4440201356<3.4674591280\);
* 640: \(3.4539332142<3.4723847469<3.4738921251\);
* 1280: \(3.4467824163<3.4517171378<3.4541159313\).

Thus \(\arg\min\rho\) gives a unique label-independent choice on each transported three-class candidate set, and every chosen signing remains Ramanujan.

The all-level theorem is still open.  The three candidate classes themselves come from a deterministic perfect-matching factorization of a labeled parent; no proof yet shows that this candidate set is intrinsic under the full automorphism group or globally optimal among all balanced switching classes.

## Pass 5729 -- exact finite family-symmetry breaking lattice

On \(\mathrm{Herm}(3)\), the real dimensions of the invariant commutants are
\[
\begin{array}{c|ccccccc}
G & 1 & Z_3^{\rm scalar} & \langle X\rangle & \langle Z\rangle & C_2 & S_3 & H_3\\
\hline
\dim_{\mathbb R}\mathrm{Herm}(3)^G & 9&9&3&3&5&2&1.
\end{array}
\]
Consequences:

* a scalar center imposes no family texture;
* a single cyclic \(C_3\) leaves a three-real-dimensional commutant and permits a generic nondegenerate three-level spectrum;
* a transposition \(C_2\) gives \(\mathrm{Herm}(2)\oplus\mathbb R\), dimension 5;
* full permutation \(S_3\) forces a \(1\oplus2\) decomposition and an invariant doublet degeneracy;
* the irreducible Heisenberg action collapses the commutant to scalars.

The \(X\)- and \(Z\)-cyclic axes are Fourier conjugate, with every basis-overlap magnitude
\[
\boxed{1/\sqrt3}.
\]
Thus a single residual cyclic symmetry merely selects a basis.  Nontrivial finite mixing becomes meaningful as a **relative mismatch** between independently selected residual axes for two operator/species sectors.  Imposing both \(X\) and \(Z\) on the same operator restores \(H_3\) and destroys the splitting.

No observed mass or CKM/PMNS value is predicted here.

## Pass 5730 -- bonkers: the full torsion symmetry is naturally extended-Clifford

The Fourier and quadratic-phase qutrit gates act projectively by
\[
F:X\mapsto Z,\quad Z\mapsto X^{-1},
\]
\[
P:X\mapsto XZ,\quad Z\mapsto Z,
\]
and realize the determinant-\(+1\) symplectic quotient action.  Complex conjugation satisfies
\[
K:X\mapsto X,\qquad Z\mapsto Z^{-1}.
\]
Therefore the determinant character
\[
\det:GL(2,3)\to\mathbb F_3^\times\cong C_2
\]
has an exact representation-theoretic meaning on the qutrit bridge:

* \(\det=+1\): unitary Clifford/symplectic action;
* \(\det=-1\): antiunitary extended-Clifford coset.

The same bit records whether the alternating form on the torsion doublet is preserved or reversed.

## Pass 5731 -- bonkers: no new mixed central Z3/Z2 topological invariant

For trivial action,
\[
H^2(C_3,C_2)=0,\qquad H^2(C_2,C_3)=0,
\]
because multiplication by 3 is invertible on \(C_2\) and multiplication by 2 is invertible on \(C_3\).  Hence a mixed central extension splits:
\[
C_3\times C_2\cong C_6.
\]
There is no new central coupling invariant from simply combining the torsion \(Z_3\) label with the deck/class-D \(Z_2\) label.

A noncentral route exists abstractly because
\[
\mathrm{Aut}(C_3)\cong C_2,
\]
and qutrit complex conjugation inverts the center, giving
\[
C_3:C_2\cong S_3.
\]
But this requires an explicit cross-carrier identification of the deck conjugation with the qutrit antiunitary \(K\); Pass5710 does not supply that map.  The equal Pfaffian parity of the deck magnetic rays remains unchanged.

## Pass 5732 -- bonkers: the p=2/p=3 bridge is an orientation bit, not CRT magic

Primary-group homomorphisms vanish:
\[
\mathrm{Hom}(C_2,C_3)=0,
\qquad
\mathrm{Hom}(C_3,C_2)=0.
\]
The Chinese remainder theorem
\[
C_6\cong C_2\times C_3
\]
packages independent primary data but does not manufacture an interaction.

There is nevertheless one exact cross-prime hinge already present internally:
\[
\boxed{\det:GL(2,3)\to\mathbb F_3^\times\cong C_2}.
\]
The fibers have sizes \(24+24\), with kernel \(SL(2,3)\).  This same determinant bit controls both orientation of the ternary torsion symplectic form and unitary versus antiunitary qutrit normalizers.

What remains absent is a canonical map from the binary Ramanujan switching/cohomology state space into this determinant quotient.  Therefore the p=2 and p=3 sectors are not yet welded.

## Combined frontier

The strongest new exact bridge is
\[
\boxed{
H_1(X;\mathbb Z)\cong(\mathbb Z/3)^2
\cong H_3/Z(H_3)
\curvearrowright_{\rm projective}\mathbb C^3_{\rm family},
}
\]
with residual \(GL(2,3)\) promoted to an extended-Clifford unitary/antiunitary action.  This is finite and representation-theoretically exact after a torsion-basis choice.

The strongest new no-go is equally sharp:
\[
\boxed{\operatorname{rank}_{\mathbb Q}J=234,\qquad \dim Y_{\min}=234.}
\]
The old small \(l_3\)-repair picture is not merely technically incomplete; the actual firewall defect spans almost the entire 248-dimensional carrier.  Any viable higher-algebra replacement must confront that scale and then satisfy the still-open arity-four and higher identities.
