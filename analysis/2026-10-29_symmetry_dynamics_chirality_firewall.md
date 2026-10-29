# Dynamics selection and chirality firewall — one-body W33 symmetry cannot do the job alone

**October 29, 2026.** This is an explicit *control/corollary of prior repository results*, not a newly discovered rank-three theorem. W33's automorphism group has three ordered-pair orbits of sizes 40, 480 and 1080 (diagonal, adjacent, nonadjacent). Its complex permutation commutant is spanned by the real symmetric matrices \(I,A,J\). Thus a fully \(PSp(4,3)\)-invariant one-body Hermitian Hamiltonian in the canonical 40-mode point basis has the general form
\[
H=aI+bA+cJ,\qquad a,b,c\in\mathbb R.
\]
Requiring *W33 nearest-neighbor plus on-site locality* makes \(c=0\), leaving \(H=aI+bA\). The irrelevant global energy \(a\) may be discarded; **\(b\) is still an undetermined clock/energy conversion factor**. Therefore automorphism symmetry plus point-graph locality selects the dimensionless matrix shape but cannot determine physical rates or constants.

Since every such Hermitian invariant matrix is real symmetric, complex conjugation \(K\) is a time-reversing antiunitary in this one-particle model: \(KHK=H\). No orientation-odd imaginary hopping phase or genuinely chiral scalar flux exists in the fully symmetric one-body commutant. A physical chirality selector needs additional degrees of freedom, an explicitly symmetry-breaking order parameter, a nontrivial projective lift, or interactions.

A straightforward non-uniqueness control uses the already known spectrum \(12^1,2^{24},(-4)^{15}\): \(H_1=A\) gives \(e^{-i\pi H_1}=I\), while \(H_2=A+J/40\) gives \(e^{-i\pi H_2}=I-J/20\). On-site probabilities are respectively \(1\) and \(361/400\); for \(H_2\) each off-site output has probability \(1/400\). Both Hamiltonians preserve the full graph symmetry, but only \(H_1\) obeys strict adjacency locality. These calculations are **existing repo results reproduced for a clean dynamics-selection boundary** in \`analysis/w33_20261029_symmetry_dynamics_no_chirality.py\`.

This does not rule out spontaneous chirality breaking in an appropriate interacting infinite-volume limit, nor a separate physical clock sector, nor a dynamical metric. It does rule out claiming that the 40-point one-body symmetry representation alone uniquely fixes chirality or dimensionful time.
