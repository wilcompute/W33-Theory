# Signed knight translations and the shared E6 lattice gauge identity

The repository already constructs the exact toroidal knight isomorphism with Q4 and the full Clifford product on its blade basis. In the unsigned cube the four bit flips commute. With each flip of bit i weighted by the parity of the occupied bits below i, the four signed flips square to +1 and anticommute. This is left multiplication on the sixteen Clifford blades. The 1,4,6,4,1 grades count the subsets of four generators. The signs encode Clifford multiplication in addition to those grades. [Repository construction](2026-11-02_native_knight_clifford_cover_bridge.md) · [Doran et al., Adinkras for Clifford Algebras](https://arxiv.org/abs/0811.3410)

Translate the original board by one step in x or y. These graph automorphisms swap the two cube axes in their respective Gray-code coordinate pairs. Demand that the signed translations intertwine the Clifford moves with these permutations of the four axes. Propagating along the cube edges determines each lift up to its overall sign because the cube is connected. The certificate checks the exact lifts A and B and obtains

    A^4 = B^4 = -I
    AB = -BA

They generate a 32-element real signed group over the sixteen board translations. Rephasing either operator by a scalar can change its fourth power over the complex numbers. The commutator −I survives scalar rephasing and vertex-basis sign changes. This is a holonomy of the signed translation action.

The shared E6 lattice result has a specific use for commuting shifts. Its linear gauge complex satisfies D_i G_j = −D_j G_i and D_i G_i = 0. With only two active differences, the composition is therefore D_i G_j tensored with their commutator. Using A−I and B−I as differences gives the commutator 2AB. The producer exhibits a nonzero composition entry −2 in the native cubic gauge. Thus directly substituting the signed knight translations for the ordinary shifts would make a trivial gauge parameter act nontrivially. This result uses the unchanged linear stencil coefficients. It leaves open discretizations that put gauge fields on different cells or explicitly compensate for the translation curvature. [Shared lattice gauge complex](2026-11-13_exft_lattice_gauge.md)

The linear obstruction can be canceled by a two-component auxiliary space. The ordinary Pauli X and Z anticommute, so A tensor X and B tensor Z commute. Both have fourth power −I. Multiplying each by exp(iπ/4) gives commuting order-four translations, and their character is two copies of the regular representation of the board translation group. The linear gauge identity holds with these compensated differences. A one-component scalar rephasing cannot cancel the commutator. This construction adds a degree of freedom and leaves the pointwise nonlinear closure problem in place.

Replay with `py -3 analysis/toe_20261113_knight_translation_flux.py`.
