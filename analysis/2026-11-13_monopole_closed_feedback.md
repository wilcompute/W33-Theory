# Closed-channel feedback on the monopole tail

For the real energy E=0.002, split the native radial Weyl space into vacuum open and massive closed channels. The flux matrix F preserves both sectors. In the radial generator convention G=−iFH, the Hermitian interaction is V=iF(G−G₀). The producer measures the spectral norms of the closed perturbation Vqq and the open-to-closed block B=Vqp on a sampled piecewise-constant exterior shell.

There is an a priori bound for the part of the feedback sourced by the shell. Extend its interaction by zero to the full radial line and impose decay on the closed solution at both ends. The Fourier symbol of the free closed Dirac operator has energies ±sqrt(p²+m²), because its vacuum mass term anticommutes with F. Its resolvent at E has L² operator norm at most 1/Δ with Δ=m_min−|E|. If v=ess sup ||Vqq|| is below Δ, the Neumann series gives a closed resolvent of norm at most 1/(Δ−v). The source is B times the open field. Cauchy–Schwarz then bounds the return term B†(Hqq−E)⁻¹B from bounded open fields to integrable open forcing by

    integral ||B(r)||² dr / (Δ−v).

The numerator sums spectral norms squared over the actual piecewise-constant shell. This bound is for a specified numerical Hamiltonian and for the induced forcing, with double precision norms. It does not bound the scattering matrix of the core-plus-shell system by itself. The actual core also supplies homogeneous massive amplitudes at the inner interface, and the open scattering response can amplify an operator perturbation near a pole. The replay therefore makes a second, direct comparison of the full and projected scattering matrices at the same outer endpoint and energy. [Feshbach, Unified theory of nuclear reactions](https://doi.org/10.1016/0003-4916%2858%2990007-1)

Replay with `py -3 analysis/toe_20261113_monopole_closed_feedback.py`. For the alternate Robin background use `--outer 5 --elements 100 --output data/toe_20261113_monopole_closed_feedback_robin5.json`.

## Direct comparison

| Robin background | Exterior shell | Source-feedback bound | Reflection operator difference | Conversion probability difference |
| --- | --- | ---: | ---: | ---: |
| Radius 9 | 36–72 | 4.70e−5 | 4.26e−7 | 2.14e−7 |
| Radius 5 | 20–40 | 2.88e−4 | 2.45e−6 | 1.26e−6 |

At radius 72 the full conversion is 80.6580221%. The projected value is 80.6580007%. Restoring closed channels on this shell changes conversion by about one part in 20,700 of the conversion change caused by extending the tail from 36 to 72. The alternate calculation was run through Remote Desktop Commander. These tests cover a single real energy at two finite shells. They leave separate bounds on the homogeneous interface contribution and the infinite-radius scattering error open.
