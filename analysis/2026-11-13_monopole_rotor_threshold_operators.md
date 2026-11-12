# Which W33 monopole threshold channels need interactions?

At fixed total Cartan weight w₋ + pα, the zero-step three-fermion channels identified in the split-threshold charge ledger require changes of occupation that a quadratic fermion–rotor Hamiltonian cannot generate. The obstruction extends to every multiplicity built from the same restricted asymptotic modes. The lowest triples also fail a separate test for a derivative-free four-dimensional vacuum vertex. [Triplet charge and rotor thresholds](2026-11-13_monopole_triplet_charge.md)

## A selection rule for quadratic rotor couplings

For a physical fermion weight w, let n = w(m) be its magnetic pairing and put q(w) = 2w − nα, with α(m) = 2. The root rotor has q = 0. Choose one representative s of each pair {q, −q} with q nonzero, and let N_s count the number of excitations with q = s minus the number with q = −s. A normal quadratic term can only join equal q. A pairing term can only create or annihilate opposite q. In the bare excitation Fock representation each N_s therefore commutes with quadratic terms preserving the perpendicular Cartan, including rotor-dependent coefficients and particle-hole pairing. Repeated insertions and virtual rotor propagation preserve this grading in that representation. Neutral modes carry zero. The regulated chiral sea has a mixed anomaly. Its integer winding contributions leave the threshold obstruction intact in the stated spectra. [Sea flow and dressed asymptotic channels](2026-11-13_monopole_rotor_sea_flow.md) [Fermion–rotor scattering and asymptotic states](https://arxiv.org/abs/2408.04577)

Both external single weights have q = (0, 1, 1, 1). In each signed species space used to build the triples, every nonzero sector s has a unique value c_s = n times the sign of q relative to s. The code verifies this on the complete input list and verifies the absence of q = 0 in each list. Thus for any product of these excitations the total magnetic pairing is exactly Σ_s c_s N_s. There is no restriction on multiplicity or momenta in this argument.

| Lower rotor level | Restricted asymptotic space | Single weight to match | Pairing required by weight | Pairing forced by single's grading | Grading-compatible weight |
| --- | --- | --- | ---: | ---: | --- |
| p | Incoming, with H_u and its hole removed | w₋ | −1 | +1 | w₊ |
| p−1 | Outgoing | w₊ | +1 | −1 | w₋ |

The grading forces the weight one root away. At fixed total charge that change requires the other rotor level, which is above the total energy in the split interval. The result uses the signed unit-flux spectrum and applies before projection to residual-color singlets. It covers all exact zero-step triples and quintets in the stated spaces. Restoring H_u and its hole at level p adds a correction of −2 per net H_u to the inferred magnetic pairing. Matching −1 therefore requires exactly one net H_u excitation in any grading-compatible state. The quadratic model can use that channel with additional excitations, subject to the rest of the scattering dynamics. Other asymptotic sectors and interactions that violate the quadratic grading require separate treatment.

## Chirality of the leading candidates

Incoming left-handed particles annihilate through an undotted Weyl field. Outgoing left-handed particles are created through its dotted conjugate. Holes reverse these assignments. For either scattering direction, an external physical weight with n = +1 therefore contributes a dotted field in the stated unit-flux convention.

| Process at lower rotor level | Fermions at the four-field vertex | Undotted : dotted |
| --- | --- | --- |
| 3 incoming → 1 outgoing at p | Q, D^c, gluino hole → conjugate L or conjugate H_d | 3 : 1 |
| 1 incoming → 3 outgoing at p−1 | Conjugate D^c → Q, charged wino hole, L or H_d | 1 : 3 |

A Lorentz singlet made from Weyl fields alone needs even numbers of each chirality, since each of the two complexified spin factors has its own central sign. The homogeneous-vacuum derivative-free four-fermion contact vanishes for these external chirality assignments. A vector index from a derivative or the background permits a scalar contraction by this test. In a smooth monopole the projected radial vertex can use background tensors and dressed wavefunctions, so its coefficient requires an explicit calculation.

## Formal flavor filters and threshold powers

The signed exterior characters reproduce all 9 incoming and 12 outgoing residual-color singlets at degree three. Using the repo's formal baryon and lepton labels as additional conservation rules gives the following conditional census. [Residual color and formal flavor labels](2026-11-10_monopole_color_operators.md)

- At level p, the 9 incoming triples all have (3B,L) = (0,0), which matches the conjugate Higgsino. A conjugate lepton needs (0,−1). In the same restricted incoming spectrum the first such singlets occur at degree five, with multiplicity 27.
- At level p−1, the incoming conjugate down antiquark has (3B,L) = (1,0). Three of the outgoing triples match those labels through H_d. The nine involving L have (1,1).

For a free massless radial continuum with a smooth, nonzero contact form factor and constant single-mode spectral density, integration over the positive energies of k excitations at excess energy ε gives ε^(k−1)/(k−1)!. Thus the stripped triple and quintet weights are ε²/2 and ε⁴/24. These powers describe the integrated many-body side. A derivative on an outgoing soft mode can add powers. At a split threshold the incoming energy can remain finite, so derivative counting alone does not fix the exponent. The calculation gives no microscopic coefficient and does not establish a unitary completion.

Run `python analysis/toe_20261113_monopole_rotor_threshold_operators.py` to regenerate the [exact charge, grading, chirality and flavor checks](../data/toe_20261113_monopole_rotor_threshold_operators.json).
