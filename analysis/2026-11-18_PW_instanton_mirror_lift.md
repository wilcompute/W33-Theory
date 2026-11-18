# The PW quartic lifts one mirror pair, but strong localization makes that pair light

18 November 2026. Local internal-operator and actual native E6 pairing tests. No compact G2 vacuum, observed mass scale, realistic Yukawa matrix or completed TOE is established.

## Why the zero-mode count was not enough

**d7280e023**, `analysis/2026-11-18_PW_Clifford_A3_chiral_localizer.md`, proves exactly three degree-one L2 zero modes for the harmonic background

    f=Re(x+iy)^4/4-(x^2+y^2)/2+z^2.

There are nevertheless four index-one critical points and one index-two point. The extra perturbative chiral profile and mirror must pair. Here we resolve their coupling and its scale in the specified local operator. The important additional conclusion is that this pair becomes parametrically light as localization is strengthened. An exactly three-dimensional kernel does not establish that only three families are light.

The established PW mass functional is the matrix element of the twisted differential, as in [Braun et al., section5.2, equations5.9–5.16](https://arxiv.org/html/1812.06072v2#S5.SS2). The general Morse/instanton interpretation is prior literature; the explicit trajectories, normalized spectral test and native pairing below are the new calculation in this packet.

## Four trajectories and a rank-one differential

Let the positive parameter q multiply f in d_q=d+q df wedge. It denotes the total Higgs/localization amplitude after absorbing the fixed representation charge, not a continuous change of a particle's gauge charge.

For unscaled negative gradient time t, all four connecting trajectories are

    (x,y,z)=(plus/minus r(t),0,0), (0,plus/minus r(t),0),
    r(t)=(1+exp(-2t))^(-1/2).

The producer checks these identities exactly. They run from the origin, f=0, to the four outer points, f=-1/4. A factor q rescales time but leaves their spatial curves unchanged. To see that there are no additional connecting curves, the planar equations are

    r_dot=r-r^3 cos(4theta), theta_dot=r^2 sin(4theta), z_dot=-2z.

A curve emerging from the origin at negative infinite time has z=0. At each outer endpoint the angular linearization is +4, so approaching that endpoint at positive infinite time requires the invariant axis itself. There is one trajectory modulo time translation to each endpoint.

C4-compatible orientation choices give Morse incidence row (1,1,1,1), rank one. Its kernel projector is I4-J4/4, rank three. Its Fourier transform is (2,0,0,0): the invariant combination pairs with the central mirror, while the three nontrivial C4 characters survive. The instanton action is q/4. The unnormalized Morse incidence is not itself the canonically normalized finite-q physical mass matrix.

## A normalized low-subspace mass map

Write f=f2+z^2. In planar top degree the exact scalar operator is

    H2(q)=-partial_x^2-partial_y^2+q^2|grad f2|^2-2q.

Let v_q be its positive, normalized, C4-invariant ground eigenfunction, with eigenvalue lambda_q>0. There is no zero mode because exp(q f2) is not L2. The z factor is its degree-zero Gaussian. Supersymmetric pairing gives the normalized degree-one partner

    u_q=d_q^dagger(v_q dx wedge dy)/sqrt(lambda_q),
    d_q u_q=sqrt(lambda_q) v_q dx wedge dy.

Together with the three exact zero modes, u_q spans a four-dimensional C4 regular representation. In an orthonormal basis obtained by Fourier transforming these four character states, the exact restricted differential has row

    sqrt(lambda_q)/2 * (1,1,1,1).

This is a basis choice in an exact spectral subspace, not a claim that four point-centered Gaussian trial states are exact eigenstates. It gives one nonzero singular value sqrt(lambda_q) and three zeros. Arbitrary unit phases on the four entries preserve their squared row norm and rank; such phases alone cannot generate the missing three light-family masses.

## Native E6: the vectorlike bilinear is allowed, the two-family cubic still vanishes

Use the actual clock-Albert product from Pass10950, already tied to the native adjoint16 in **580972009**. For its primitive idempotent c and each Peirce-half basis vector h, define

    M_h^minus=L_h-2[L_c,L_h], M_h^plus=L_h+2[L_c,L_h],
    Psi=6L_c-2I.

All sixteen generators in each set satisfy [Psi,M_h^plus/minus]=plus/minus3 M_h^plus/minus. Exact arithmetic gives

    Tr27(M_i^plus M_j^minus)=12 delta_ij.

Thus the conjugate16bar_3 and16_-3 have a nondegenerate invariant bilinear. The same-charge minus generators still commute in all120 pairs. Lifting one vectorlike pair through the derivative/background bilinear is consistent with the older zero two-family adjoint-cubic result; it does not produce a Yukawa coupling for the remaining three families. The factor12 is a trace normalization and must also enter the kinetic normalization, not an observable mass prediction.

## The mass is exponentially suppressed

The top-form problem is equivalent to the scalar Witten operator for the metastable potential -f2. Its origin has Hessian I2. Each exit saddle has Hessian eigenvalues (-2,4), height1/4. The usual interior-saddle Eyring-Kramers estimate, summed over four exits and translated from h=1/q to H2(q)=q^2 Delta_h, predicts

    lambda_q ~ (2sqrt(2)/pi) q exp(-q/2),
    singular mass ~ sqrt(2sqrt(2)/pi) sqrt(q) exp(-q/4).

The semiclassical framework and dependence on interaction matrices are standard; see [Michel, About small eigenvalues of the Witten Laplacian](https://msp.org/paa/2019/1-2/paa-v1-n2-p01-s.pdf). Boundary placement changes prefactors, as emphasized by the distinct Dirichlet problem of [Le Peutrec and Nectoux](https://arxiv.org/html/1907.07517v2). We test this whole-space escape estimate numerically; we do not claim that either cited theorem has been verified to cover this nonconfining -f2 domain. The exact kernel and rank statements above do not depend on this asymptotic claim.

|q|Computed lambda_q, N=48|Ratio to leading estimate|
|---|---:|---:|
|1|1.03611106|1.89740|
|4|0.51363411|1.05387|
|8|0.12825083|0.97219|
|12|0.02612388|0.97550|
|16|0.00474923|0.98280|
|20|0.000807254|0.98748|
|24|0.000131478|0.99033|

All nine amplitudes were run with two basis sizes. Three independent oscillator-width controls and two higher-resolution controls agree. At q=24,N=96, lambda_q=0.000131478464609, giving singular mass0.011466405915 in the specified internal units. The next internal excitation has squared value about47.1233; the mass ratio is about0.00167036. The z oscillator's first positive value4q and the planar degree-zero spectrum, H0=H2+4q, are included in identifying this next scale.

These are internal differential eigenvalues. Conversion to four-dimensional masses requires the dimensional reduction normalization and a physical length scale. This noncompact example does not supply either an observed mass or a compact Kaluza-Klein spectrum.

## Residual and reproduction checks

Hermite polynomial matrix elements are evaluated before truncation. The true rectangular exterior map B:N^2 ->2(N+3)^2 satisfies B^T B=H2(q) in the Galerkin space, with relative matrix error at floating roundoff. Its action on the computed eigenvector has squared norm lambda_q, independently checking the partner normalization.

Projected eigensolver residuals alone are misleading: at q=24,N=48 the projected residual is about4.5e-15 while the full operator residual is about2.3e-5. Since the Hamiltonian is a degree-six polynomial differential operator, embedding into N+6 basis functions per coordinate captures its entire action on any finite vector. At N=96 the full L2 residual falls to1.09e-9. This is floating-point a posteriori evidence, not an interval-arithmetic eigenvalue enclosure or a certified lowest-gap bound.

Run `python analysis/toe_20261118_PW_instanton_mirror_lift.py`. The three owned files are this report, that producer and its JSON certificate. All prior and parallel files remain intact.

The physics constraint is sharper now: increasing q improves localization but exponentially lowers the extra vectorlike pair relative to other internal excitations. A global completion must retain the three chiral profiles, cancel the existing anomalies, provide gauge and Higgs dynamics, and place this extra pair above phenomenological limits. None of those missing steps is solved by the local index or the instanton calculation.
