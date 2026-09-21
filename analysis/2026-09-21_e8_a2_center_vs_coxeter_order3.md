# The external A2 contains two different C3 structures: center versus Coxeter

The current frontier had two order-three objects whose shared A2 provenance
made them easy to conflate.

The **physical FI / CE2 grading** is the center phase of the external
`SU(3)`.  On the standard branching

[
248=(78,1)+(1,8)+(27,3)+(\overline{27},\overline3),
]

the central element `omega I_3` acts trivially on the two adjoints, by
`omega` on `(27,3)`, and by `omega^2` on its conjugate.  Hence

[
oxed{248=86+81+81},
]

with fixed algebra `E6+A2`.

Pass 1147 uses a different order-three element: the **Weyl Coxeter 3-cycle**
of the same type-A2 factor.  In the triplet it has eigenvalues
`1,omega,omega^2`; in the A2 adjoint its multiplicities are `2,3,3`.
Therefore

[
egin{aligned}
248
&=(78,1)+(1,8)+(27,3)+(\overline{27},\overline3)\\
&\mapsto
(78,0,0)+(2,3,3)+(27,27,27)+(27,27,27),
end{aligned}
]

so

[
oxed{248=134+57+57}.
]

The fixed reductive algebra is `E7+u1`.

An independent affine-Kac sweep in the repository's frozen E8 root gauge
finds exactly four normalized inner order-three classes:

[
80+84+84,quad
86+81+81,quad
92+78+78,quad
134+57+57.
]

The physical center and Pass-1147 Coxeter spectra each select a unique class:

[
s_{m center}=(0,0,0,0,0,1,0,0,0),
]

[
s_{m Coxeter}=(1,0,0,0,0,0,1,0,0).
]

Thus they are not two realizations of the same automorphism.  They are
complementary order-three structures inside an external A2: the center acts
as a uniform scalar on the triplet; the Coxeter element cyclically permutes
the three triplet weights.

This also resolves a carrier ambiguity.  Pass 1147's color module is
`81_- tensor C[C3]`, of rank 243, split over C into three rank-81 Fourier
modes.  It is therefore **not** the physical E8 grade-one root sector of
dimension 81, even though both constructions use C3 and A2 language.

External Kac-class literature agrees that the `86+81+81` order-three class
has fixed `A2+E6`; modern treatments classify finite-order E8 automorphisms
by affine Kac coordinates and their fixed subalgebras.  The new part here is
the repo-internal comparison to the Pass-1147 Coxeter carrier and its unique
`134+57+57` class.

## Evidence

- `analysis/w33_e8_a2_center_vs_coxeter_order3.py`
- `data/w33_e8_a2_center_vs_coxeter_order3.json`
- `data/w33_pass1147_schlaefli_steinberg_fourier_bridge.json`
- `data/w33_qpsi_mod12_unification.json`

## Boundary

This is a finite E8 representation/Kac-class theorem.  It does not prevent a
larger machine from using both actions, and it does not identify either C3
with observed generations or measured photonic channels.
