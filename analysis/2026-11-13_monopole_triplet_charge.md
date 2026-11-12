# Charge-resolved triplet reflection and the W33 monopole rotor

The four incoming light states in the triplet sector have two distinct electric weights. Their reflection therefore needs two distinct rotor transitions. The charged-sector matching is evaluated in a basis that separates the conjugate down antiquarks, the up Higgsino, and the conjugate lepton and down Higgsino directions. [Triplet radial operator and determinant winding](2026-11-13_monopole_triplet_mass.md)

## Physical light directions

In the four-Cartan chart put `w_+=(0,1,0,−2)`, `w_-=(0,0,1,3)`, and `α=w_+−w_-`. The coroot pairings are +1 and −1. The light vectors are obtained from the canonical holomorphic mass kernels and projected orthogonally away from the broken gauge orbit in the kinetic metric.

| Direction | Light state | Multiplicity | Physical weight | Electric charge |
| --- | --- | ---: | --- | ---: |
| Incoming | Conjugates of (D^c) | 3 | (w_+) | −1/3 |
| Incoming | (H_u) | 1 | (w_-) | +1 |
| Outgoing | Conjugates of (L) | 3 | (w_-) | +1 |
| Outgoing | Conjugate of (H_d) | 1 | (w_-) | +1 |

The two outgoing types share all gauge weights. The exact down Yukawa covector `(0,−3,0,3)` on the four light down doublets selects their separation. Its kernel gives the three lepton directions, and the kinetic orthogonal complement gives the Higgsino. Weak lowering transports this decomposition to the charged lower component before taking charge conjugates. The solver uses these same orthonormal light frames throughout the loop. [Light Yukawa flavor decomposition](2026-11-10_light_yukawa_completion.md)

## Rotor charge rule

For (p=-i\partial_\chi), multiplication by (e^{i\chi}) raises the rotor momentum by one. In a fixed asymptotic frame the charge-conserving lift of a core reflection matrix R to the rotor Hilbert space is

```text
R_rotor = R diag(exp(iχ), exp(iχ), exp(iχ), 1).
```

The first three incoming columns require the monopole to gain one root α, with electric charge −4/3. The (H_u) column has zero rotor step. This follows from equality of the total incoming and outgoing Cartan weights in each matrix element. The operator is unitary on the unrestricted dressed space and the shifts preserve either momentum lattice selected by the endpoint holonomy. Its determinant acquires (e^{3i\chi}) exactly, independently of flavor mixing. With (E_p=(p-\theta/(2\pi))^2/(2I)), the one-step channel requires the energy difference (E_{p+1}-E_p=[2(p-\theta/(2\pi))+1]/(2I)). This conditional lift implements charge conservation. Computing an energy-conserving rotor scattering amplitude requires the coupled dynamics. [W33 rotor quantization](2026-11-11_monopole_electric_phase.md) · [Fermion–rotor scattering](https://arxiv.org/abs/2408.04577)

At fixed total weight (w_-+pα) up to a common kernel weight, the three down-type incoming channels have rotor momentum (p-1), while the up-Higgsino and all four outgoing channels have momentum (p). The incoming rotor energies coincide at (p-\theta/(2\pi)=1/2). At zero theta this gives the degenerate transition from −1/2 to +1/2 on the half-integral momentum lattice. Away from this degeneracy the open-channel thresholds depend on the incoming rotor state.

For total energy strictly between (E_p) and (E_{p-1}), this single-excitation truncation has one incoming and four outgoing channels if (E_p<E_{p-1}). For the other ordering it has three incoming and zero outgoing channels. A nonempty unitary scattering problem within this truncation therefore requires all four channels in each direction to be open. A dynamical model at the intervening energies needs additional physical channels or a different asymptotic state space. [Fermion–rotor scattering](https://arxiv.org/abs/2408.04577)

There are explicit three-excitation candidates at the lower rotor energy on either side of this mismatch. With (E_p<E_{p-1}), the incoming signed spectrum has nine residual-color-singlet triples at weight (w_-) after excluding the up-Higgsino and its hole. They use a quark and a gluino color doublet contracted to a singlet, together with a (D^c) singlet. With (E_{p-1}<E_p), the outgoing signed spectrum has twelve singlet triples at weight (w_+). They use a quark color singlet, a charged wino hole, and a lepton or down-Higgsino. The counts come from the exterior character of the signed species space, subtracting the multiplicity at the next color weight. The three excitations are massless in the asymptotic calculation and provide candidate continua above the lower threshold. Their dynamical amplitudes and role in restoring unitarity remain open. [Residual color representation counting](2026-11-10_monopole_color_operators.md)

The triplet Witten relabeling is (3w_+). It evaluates to (3/2) on the phase lift generator (m/2) and is odd under the endpoint (kappa). The output-side Cartan trace for total winding three is (3w_-) because every outgoing weight is (w_-). Their difference is exactly (3α), a root-lattice transfer with even endpoint character. These charges agree after projection to the characters transverse to the rotor direction. The one-particle lift specifies which incoming channels can supply that root transfer. [Asymptotic Witten response](2026-11-13_sm_threshold_theta.md)

For the adjoint blocks the light gaugino on each side carries the same weight in the positive-flux slot. All three adjoint rotor steps are zero and their outgoing Cartan trace is the adjoint Witten weight. This comparison follows from the physical weights of the light states and the mass slots that remain gapless. [Adjoint light masses](2026-11-13_monopole_adjoint_phase.md)

## Projected reflection circulation

The matrix calculation approximates each phase interval by the shortest unitary arc joining its sampled endpoints. For an interval with (R_{j+1}=e^{iH_j}R_j), the outgoing trace increment is (H_j/(2\pi)) and the input-side trace increment is (R_j^\dagger H_j R_j/(2\pi)). Their full traces agree and sum to the determinant winding when the increments are resolved. Projecting them onto the matter and Higgsino subspaces measures how the phase circulation is distributed in the fixed channel frames. Individual projected traces can vary continuously when R mixes these subspaces. The input-side trace is a pullback of the same unitary circulation. A physical adiabatic pump additionally requires a specified incoming state and time-dependent gauge and rotor dynamics. [Scattering formulation of adiabatic pumping](https://arxiv.org/abs/cond-mat/9808347)

| Radial cells | Phase samples | Incoming (D^{c\dagger}) | Incoming (H_u) | Outgoing (L^\dagger) | Outgoing (H_d^\dagger) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 120 | 48 | 1.77757 | 1.22243 | 2.31434 | 0.68566 |
| 240 | 48 | 1.78004 | 1.21996 | 2.31331 | 0.68669 |
| 120 | 96 | 1.77520 | 1.22480 | 2.31496 | 0.68504 |

The static (H_u)-to-conjugate-lepton probability reaches 0.9939 on both radial meshes. The sum of the reverse-sector probabilities from the three conjugate down antiquarks to the conjugate down Higgsino is equal by unitarity. The formal input-minus-output Cartan trace is about (1.78α), since the (H_u) and outgoing weights coincide. The full determinant winding is three and the outgoing trace still carries the common weight (3w_-). The subspace circulation, the exact one-particle rotor selection rule, and the asymptotic Witten relabeling describe different calculations.

The full matrix also resolves the 12-point sampling ambiguity. On the 240-cell mesh the two intervals adjacent to π each have summed eigenangle about 3.373 radians, while the principal determinant angle is about −2.910. All individual relative eigenangles have magnitude at most 2.754 radians on that 12-point grid. The matrix arcs therefore retain the two positive wraps that the principal determinant increments drop. Their winding is +3 at 12, 24 and 48 samples, and the 96-sample control agrees. The determinants in the charge-resolved frame reproduce the previous determinants after removal of a constant frame phase, to below 10⁻¹⁰ on both meshes. This remains a finite-radius numerical calculation of the loop.

Run `python analysis/toe_20261113_monopole_triplet_charge.py` for the two radial meshes, or add `--counts 60 --phase-count 96 --output <control-path>` for the phase refinement. [Reflection matrices and charge ledger](../data/toe_20261113_monopole_triplet_charge.json)
