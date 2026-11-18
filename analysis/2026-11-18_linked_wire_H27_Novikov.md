# Linked H27 wires remove the unlink mirror sector with a finite unitary twist

18 November 2026. **Exact local-system topology, with conditional effective-physics interpretation. The physical TOE is still unsolved.**

## What changed after reading the parallel work

The original wire producer, `analysis/toe_20261118_wire_Novikov_E6.py`, was already preserved and published by the parallel track in **1ae97a492**. It should not be republished as a new result. The subsequent quartic E6 Yukawa, full spinor gamma tensor, Higgs vacuum, moduli/cutoff failures and two-wire packet were reviewed through **c0ca57dab**. Relevant reports are:

- `analysis/2026-11-18_wire_E6_singlet_rank_W33_BF_photonic_anytime_audit.md`;
- `analysis/2026-11-18_E6_native_quartic_DF_W33_S3_wire_BF_anytime_fivefront.md`;
- `analysis/2026-11-18_W33_dual_parabolics_H27_E6_gamma_GS_Hodge_BF_memory.md`;
- `analysis/2026-11-18_E6_flat_moduli_BF_cusp_W33_Fourier_qutrit_memory.md`;
- `analysis/2026-11-18_sixfront_H27_min7ancilla_two_wire_E6_EFT_BF_multitime_commoncone.md`.

The last packet constructs an onto H27 local system on two **unlinked** wire loops. With one relative spherical puncture its rank-three flavor cohomology is (b1,b2)=(6,3): net three, with three vectorlike pairs. The calculation here changes the link type, then combines it with the earlier native chi Higgs period. It does not change or invalidate the unlink result.

## A concrete linked complement

Let X be the exterior in S3 of the two-component torus link T(2,6), with two torus boundary components. The standard torus-link presentation reduces to

    pi1(X) = <a,c | [a,c^3]=1>.

For example, specialize section 3.1 of [Kitano, Morifuji and Tran](https://arxiv.org/html/1904.08026#S3.SS1) to mu=2,p=1,q=3, eliminate x=y^3, and take a=m1,c=y. Equivalently set c=ab in the closed two-strand braid presentation. These group and Fox-calculus methods are standard literature, not a novelty claim.

The cyclically reduced relator a c^3 a^-1 c^-3 is not a proper power: its unique positive a occurrence would have to repeat in a nontrivial power. Its presentation complex is aspherical by the one-relator identity theorem; see [Dyer and Vasquez, Theorem 2.1](https://doi.org/10.1017/S1446788700015147). The nonsplit torus-link exterior is aspherical, so the complex computes its local-system cohomology. The computation is not merely an Euler-characteristic guess.

Use the same three-level H27 clock/shift representation as the parallel native W33 point-parabolic construction. With omega=(-1+sqrt(-3))/2,

    X0 = cyclic shift, Y0=diag(1,omega^2,omega),
    [X0,Y0]=omega I3, (X0 Y0)^3=I3.

Send a to A=t X0 and c to C=u X0 Y0, for nonzero complex scalars t,u. The compact part still generates all 27 elements of H27: a gives X0 and a^-1 c gives Y0 after stripping scalar factors. Since C^3=u^3 I3, the link relation holds for every t,u. The full complex connection generally has infinite image. Calling that full image finite H27 would be incorrect.

The scalar multipliers are candidate periods of an additional commuting Higgs/flat line bundle. They are not nonunitary holonomies of a compact physical gauge connection. The closed-one-form complex used in local G2 gauge models is described in [Huebner, sections 5.2 and 6.4](https://arxiv.org/html/2009.07136v2#S5.SS2); applying it to this supplied complement is our conditional modeling step.

There is also a restricted minimality result. For the positive two-strand torus family T(2,2n), the relation is [a,c^n]=1. In exponent-three, nilpotency-class-two H27, an onto generator pair has nontrivial central commutator, so the relation holds precisely when 3 divides n. Therefore **T(2,6) is the first positive member of this family permitting onto H27 holonomy**. Exhaustive enumeration of all729 ordered H27 generator pairs at n=1,...,9 finds432 onto pairs when 3 divides n and none otherwise. This does not minimize over all links, derive a dynamical link, or predict three generations; it explains why this particular linking pattern is compatible with the supplied finite quantum group.

## Exact differential and contraction

The rank-three twisted cochain complex has dimensions (3,6,3), with

    d0 = vertical(A-I, C-I),
    d1 = horizontal((1-u^3)I, (A-I)(I+C+C^2)).

Fox differentiation of the entire unreduced relator independently reproduces both blocks; d1*d0=0 is checked over Q(sqrt(-3)). If u^3 differs from 1, both C-I and the first d1 block are invertible. More explicitly,

    h1 = horizontal(0, (I+C+C^2)/(u^3-1)),
    h2 = vertical(I/(1-u^3), 0),
    h1*d0=I3, d1*h2=I3, d0*h1+h2*d1=I6.

Thus X is **acyclic in this local system**, in all degrees. This proof holds for every nonresonant u and every nonzero t, rather than just sampled numeric characters. The finite tests include rational, cyclotomic, nonunitary and inverse-period controls, with the contraction identities checked exactly.

Remove one open ball and impose relative conditions on its S2, keeping both wire tori absolute. Excision gives H2(M;V)=V because the base X is acyclic. In the pair sequence, the new sphere maps isomorphically onto that new degree-two contribution, while H0(S2;V)=V contributes to relative degree one. Consequently

    H*(M,S2;V) = (0, C^3, 0, 0).

The Euler check is independent: chi(X)=0, chi(M)=1, chi(M,S2)=-1, and coefficient rank three gives relative Euler characteristic -3. The **vanishing of H2**, unlike the net index, depends on the linked differential and period.

| Chosen model | Base (b1,b2) | One relative sphere (b1,b2) |
|---|---|---|
| Two unlinked wires, onto H27, including scalar twists | (3,3) | (6,3) |
| T(2,6), finite H27 control u=1 | (2,2) | (5,2) |
| T(2,6), u^3 != 1 | (0,0) | (3,0) |

In particular, linking alone does not solve the mirror problem. A nonresonant twist is substantive. The jump at u^3=1 is a local-system cohomology resonance, not a physical mass formula.

## A stronger alternative: no nonunitary period is needed for this count

The exact u=-1 control is entirely unitary: A=X0 and C=-X0 Y0 give C^3=-I3. They generate **H27 x C2 of order54**, since the central minus identity is C^3 and the original H27 generators can then be recovered. This is a finite compact flat local system and has the same acyclic base and relative (b1,b2)=(3,0). Thus the nonunitary Higgs period is sufficient but **not necessary** to remove the unlink's flavor pairs after changing the link type. The finite local-system image differs from pure H27, whose central fiber is resonant.

The abstract order54 group is not new to the repository: `analysis/PASS10947_RESERVATION.md`, section3, and `analysis/w33_pass10947_five_front_execution.py` already identify H27 x S2 as a channel-projector stabilizer. That S2 swaps two channels. Here the C2 acts as the scalar minus identity on a three-dimensional local system and enters the Seifert-fiber holonomy; no equivalence of those representations or physical mechanisms is asserted.

Every native spinor chi weight (-1,+3,-5) is odd, so exp(i*pi*chi)=-1 on the entire16. A common order-two scalar twist can therefore treat every family block identically. The topology and representation calculations show this compatibility; they do not construct a physical E6/flavor gauge bundle. Also chi=+/-4 adjoint gauge-root weights are even: this order-two twist **does not** reproduce the earlier nonexact-Higgs gauge reduction20->14. Matter-pair removal and unwanted-gauge-generator removal remain distinct tests.

One can nonetheless combine a **different, already known** gauge twist with this construction. Parallel commit **f495122c1**, report `analysis/2026-11-18_optimal_W33_3D_symmetry_E6_global_Wilson_modular_memory.md`, already used an SU5 order-seven Wilson to obtain the Spin10 centralizer of dimension13; its closed-lens topology could not support it. The linked complement has no order-four fundamental-group relation. Choose W7 fundamental weights (2,2,2,4,4) modulo7 and append W7 to c. Counting all D5 roots gives eight invariant roots plus five Cartan generators, hence13 in Spin10 and14 after Psi. This does not remove the two extra U1s.

On any native family block with W7 phase zeta7^k, the central fiber now acts by -zeta7^(3k). It is never1: in fourteenth roots its exponent7+6k is odd. Therefore the exact acyclicity proof still applies on every block. The combined abstract holonomy generated by a=(X,1,1) and c=(XY,-1,W7) has image **H27 x C2 x C7, order378**, verified by explicit finite-group closure. This supplies a wholly compact finite-twist alternative for the stated matter and gauge-H0 tests. It does not identify that abstract flavor action inside an actual E6 gauge bundle, suppress neutral higher-cohomology modes, cancel anomalies, or establish a Standard Model vacuum. The order-seven centralizer is cited prior art; its compatibility with the linked acyclic family system is the additional calculation.

## Connection to native E6, and its limits

The native E6 chi values on the earlier spinor family are -1 on the decuplet, +3 on the antifundamental five, and -5 on the singlet. The original nonunitary choice u=2^(-chi) gives respectively 2,1/8,32. Each is nonresonant, as is the uniform unitary u=-1 alternative. The exact test therefore gives three degree-one copies and zero degree-two copies for every block, totaling 48 complex gauge components **if** these rank-three flavor bundles are realized as the stated matter coefficient bundles.

This is not an E6-adjoint construction of family multiplicity. A single irreducible 16 has only scalar complex endomorphisms commuting with Spin10 (Schur's lemma); it cannot internally support a noncommuting H27 flavor action. The added rank-three coefficient bundle is new input. An actual gauge enlargement, geometric multiplicity bundle, or other compatible ultraviolet mechanism is required. E8 branching with an SU3 multiplicity is a possible research direction, but its 27-family channel differs from the current adjoint16_-3 channel and has not been substituted here.

Nor is there yet a common physical boundary domain for all fields. Relative cohomology computes a specified de Rham/Higgs operator, not automatically a normalizable seven-dimensional spinor index. Required checks include the actual twisted fermion operator, gauge-covariant boundary projectors, source quantization, eta/inflow, normalizability and neutral-sector domains. A harmonic nonexact period can be defined on this complement; no complete BPS G2/ALE solution, singular-source action or metric has been built. A finite-radius cut boundary does not by itself justify a unique singular limit.

There is nevertheless a concrete continuum **auxiliary operator** behind the finite count. On a smooth compact cut complement with any fixed Riemannian metric, define f uniquely by Delta f=0, f=-1 on S2 and f=+1 on the two tori. The Hopf lemma gives inward/outward normal signs at the specified components. For the unitary flat coefficient connection, D=d_A+df wedge is conjugate to d_A by exp(f); mixed relative/absolute Hodge domains therefore realize the calculated cohomology. [Braun et al., section4.1 and appendixC](https://arxiv.org/html/1812.06072v2#S4.SS1) give the corresponding gauge-theory boundary framework. This existence-defined elliptic problem supplies neither a numerical spectrum nor a derivation of that domain from a singular ultraviolet defect. It also does not fix the missing gauge realization of the flavor bundle.

The parallel nonzero quartic Yukawa tensor remains useful; its existence does not supply Higgs zero modes, overlap integrals or observed masses. The earlier anomalous Psi, extra-U1 vacuum, at-least-65-modulus and cutoff problems are not repaired by this topology. Defect topology, the one sphere and its boundary condition, the H27 carrier and the period amplitude are selected inputs, not predictions.

## Reproduction

Run `python analysis/toe_20261118_linked_wire_H27_Novikov.py`. It writes `data/toe_20261118_linked_wire_H27_Novikov.json` and checks exact Fox derivatives, the relation, differential composition, H27 cardinality, all stated ranks, nonresonant chain contractions and native chi controls. No previous producer or parallel certificate is modified. The batch guard is run before publication.

The final exact run on TheHeavyCrown completed in68.15 seconds, including the compact order378 extension. An additional independent server-side JavaScript calculation used the original a,b meridians and the relator a(ab)^3 a^-1 (ab)^-3 rather than the producer's a,c generators. All18 phase-twisted/conjugate coefficient controls gave ranks(d0,d1)=(3,3), with maximum relation/differential residual2.35e-15. This numerical cross-check supports the exact proof; it is not a separate physical simulation.

The new contribution is a concrete way around the **specific unlink mirror obstruction** in the parallel model. It is a conditional mathematical improvement toward a physical model, not a completed compactification or theory of everything.
