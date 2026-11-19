# Physical closure checks: AdS4 / E8-H27 / PW / E6 / quantum-memory power

2026-11-18. **Five independently tested conditional calculations; not a solved Theory of Everything or a measured experiment.**

The baseline repo head was 9321eb27ecaeacea9d640b31c8d010fa3a9f84f7. We read the parallel commits ccdd3fe, d7280e0, 6ef448a and 9321eb2 on E8/Callias and PW three-mode localization / mirror lifting / harmonic tilt, preserving those results as prior work. The 19 preexisting locally modified tracked files must not be staged. Earlier work already established the AdS4-vs-AdS5 BF distinction, an H27-equivariant E8 embedding, the original 65-dimensional E6 modulus obstruction and a design-point photon confidence bound. Here we check the missing global and operational requirements.

## 1. Genuine 11D AdS4, round S7 homogeneous breathing control

Start from F4=(3/L)vol(AdS4) in eleven-dimensional Freund-Rubin supergravity. Einstein equations yield R_S7=2L_AdS4. The 4D Einstein-frame metric, potential, and kinetic term for a uniform sphere-radius variable u are

    ds11²=e^(-7u)ds4,E²+e^(2u)(2L)²dOmega7²,
    V(u)=[-21 exp(-9u)+9 exp(-21u)]/(2L²),
    Lkin=-(63/2)(partial u)².

Direct differentiation gives V(0)=-6/L², V'(0)=0 and m_breath²L²=18. A minimally coupled *spectator* massless eleven-dimensional scalar has round S7 harmonics m_l²L²=l(l+6)/4, all above the correct AdS4 scalar BF bound -9/4. This is an actual 11D 4+7 control background, unlike the prior conditional AdS5 x Tpq winding branch. It does NOT diagonalize the coupled 11D graviton, 3-form, fermion or ghost KK spectrum, nor establish weak-G2/W33 chiral geometry. Literature: https://link.springer.com/article/10.1007/JHEP02%282024%29144

## 2. E8/H27 gauged-family anomaly and adjoint Higgs obstruction

The standard E8 branching under E6 x SU3 is 248=(78,1)+(1,8)+(27,3)+(27bar,3bar). If a 4D *gauged* SU3 family theory keeps only left-chiral (27,3), then its SU3_family cubed anomaly coefficient is 27 (fundamental triplet normalized +1). Adding the conjugate (27bar,3bar) cancels this perturbative continuous anomaly, but also returns conjugate matter unless a physical projection/mass mechanism is derived. Gauging finite H27 instead has a separate discrete/global anomaly problem; a global SU3 label is not subject to this local gauge-anomaly consistency check.

The E6-singlet adjoint directions in E8 248 form only the SU3 adjoint8. Under H27, the native shift X and clock Z act irreducibly on a qutrit. Solving [M,X]=[M,Z]=0 and tr M=0 yields zero traceless commutant. Consequently a *covariantly parallel E6-neutral adjoint Higgs preserving full H27 holonomy* must vanish. A spatially varying Higgs, new multiplet or changed holonomy could avoid this restricted obstruction.

## 3. Global energy of the latest tilted Pantev-Wijnholt localizer

The latest parallel PW local model uses f_a=Re[(x+iy)^4]/4-(x²+y²)/2+z²-a*x, whose flat Laplacian vanishes. Parallel work derived three local L2 charged modes and removed the previous near-mirror critical pair via harmonic tilt. We independently integrated the exact squared gradient on B_R:

    integral_B_R |grad f_a|² =
        64*pi*R^9/315 + 8*pi*R^5/5 + 4*pi*a²*R^3/3.

Hence the source-free flat auxiliary Higgs energy diverges as R^9, with additional positive tilt cost. A smooth, globally exact harmonic df cannot be nonzero on a closed compact connected three-manifold (integrate f Delta f). This is a **globalization obstruction to an unchanged source-free local polynomial**, not a refutation of the three local L2 states. Sources, cut boundaries, nonexact harmonic fields, non-Abelian backgrounds or a genuine G2/7D action would change the problem. Relevant framework: https://arxiv.org/abs/1812.06072

## 4. Arbitrary powers of the same E6 invariant cannot stabilize the toy vacuum

The native three SM-singlet weights (-5,-3),(+5,-1),(0,4) have polynomial invariant ring C[xyz], exactly checked through total degree12. The only nonconstant renormalizable singlet monomial is cubic I=xyz, but W=lambda I has nonzero F terms at an all-three-nonzero VEV when lambda!=0; the previous example used higher-dimensional I²/Lambda³.

Generalizing the prior obstruction: for any holomorphic W=f(I) at a smooth nonzero I=c where f'(c)=0 and dI !=0, the complex F-flat locus contains hypersurface I=c and Hess(W)=f''(c)dI tensor dI, rank<=1. Arbitrarily many higher powers of I alone cannot eliminate the existing at-least-65 complex moduli in the specified complete chiral 78+27+27bar field inventory with smooth SM-preserving D-flat quotient. For the *restricted separable* class W=sum f_a(I_a) with k independent smooth stationary invariants, reduced moduli obey dim >=max(0,66-k). No universal E6 no-go is claimed: a different superpotential, field inventory, supergravity couplings, source sector and UV invariants can change everything.

## 5. Photon three-time witness: confidence is not power

The previous source-model fixed-n Clopper-Pearson example with gamma=.96, p=.45, eta2=eta3=.95 gave a 99% negative upper witness at a particular rounded design-point dataset of n=450 accepted observations per setting. We exactly summed the binomial probabilities of that *decision rule* using independent fixed-n p_gamma=.98 and p_eta=.975:

    n per setting | total accepted | P(reject classical witness)
       300        |  900           |  0.23398
       450        | 1350           |  0.66128
       600        | 1800           |  0.90855
       900        | 2700           |  0.99794

Therefore 450/setting is NOT even an 80%-power design under the stipulated sampling model; 600/setting exceeds 90%. This is not observed photon data, and detector/heralding bias, instrument drift and a missing physical multitime process could invalidate the inference. Original genuine multitime theorem: https://arxiv.org/abs/2611.17268

## Reproduction and next physical gates

Run python analysis/toe_20261118_fivefront_global_physics_closure.py, which writes data/toe_20261118_fivefront_global_physics_closure.json. Run python -m unittest discover -s tests -p test_toe_20261118_fivefront_global_physics_closure.py -v. The 22 regression tests validate the exact conditions and statistical model; they cannot validate full physics. All files are additive and preserve other assistants' changes.

**Five best independent next steps:** (1) actually diagonalize mixed 11D AdS4 KK fluctuation operators in a weak-G2/flux background; (2) supply a gauged-family anomaly-free E8/E6-H27 chiral matter spectrum and admissible Higgs action; (3) build a finite-energy stationary G2/PW gluing of the tilted three-mode localizer with derived source and boundary data; (4) obtain a UV-controlled E6 superpotential with independent invariants and stabilized masses; (5) build an event-ready genuine three-time photonic or intrinsically qutrit witness experiment with power analysis and calibrated detection.

**Physical assessment:** The five mathematical fronts constrain the construction, but neither finite-geometry correspondences nor local normalizable kernels are sufficient to establish observed quantum gravity or a TOE.
