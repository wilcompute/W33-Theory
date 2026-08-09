# Part CCLII: Photon Fock Space and Thermal Statistics Bridge

## Abstract

We derive the Bose-Einstein statistics, Stefan-Boltzmann law, Planck distribution, and photon
number density from the combinatorial parameters of W(3,3). The integer photon spin, the power
laws governing radiative thermodynamics, the zero-point energy denominator, and the count of
cosmic photons all emerge from the SRG structure.

## 1. Introduction

The photon is the quanta of the electromagnetic field. As a massless spin-1 boson it obeys
Bose-Einstein statistics. The thermal properties of a photon gas — Planck distribution, Wien
displacement, Stefan-Boltzmann law — encode powers that are exactly the SRG parameters Q, LAM,
and MU.

## 2. Bose-Einstein Statistics

The mean photon occupation number at mode frequency $\omega$ and temperature $T$ is

$$\langle n \rangle = \frac{1}{e^{\hbar\omega/k_BT} - 1}.$$

The denominator $e^x - 1$ has a simple pole of order **1** at $x = 0$. This pole order equals
`be_pole_order = 1`, consistent with the photon's integer spin `photon_spin_integer = 1`.

## 3. Stefan-Boltzmann Law

The total radiated power per unit area scales as $T^4$:

$$j^* = \sigma T^4, \qquad \sigma = \frac{2\pi^5 k_B^4}{15 h^3 c^2}.$$

The temperature exponent is $4 = \text{MU}$ (`stefan_boltzmann_exp`).

## 4. Planck Distribution

The spectral energy density in 3-dimensional momentum space is

$$u(\omega) \propto \frac{\omega^3}{e^{\hbar\omega/k_BT} - 1}.$$

The numerator power $\omega^3$ has exponent $3 = Q$ (`planck_integrand_power = MU - 1 = Q`).

## 5. Photon Number Density

The total photon number density scales as $T^3$:

$$n \propto T^3, \qquad \text{photon\_number\_exp} = Q = 3.$$

The integrand for the number density is $\omega^2 / (e^x - 1)$, with power $2 = \text{LAM}$
(`photon_number_integrand_power`).

## 6. Polarisations and Mode Structure

Each photon mode has LAM = 2 transverse polarisation states. Momentum space is Q = 3 dimensional.
The zero-point energy per mode is $\hbar\omega/2$, with denominator LAM = 2 (`zero_point_denom`).

## 7. Zeta Function Values

The Riemann zeta function evaluations relevant to the photon gas:

- $\zeta(3)$: governs photon number density; argument = Q = 3 (`zeta_arg_number`)
- $\zeta(4) = \pi^4/90$: governs energy density; argument = MU = 4 (`zeta_arg_energy`)

## 8. Wien Displacement

The Wien displacement law $\lambda_{\max} T = b$ relates the peak wavelength to temperature.
The dimensionless peak frequency $x_{\max}$ satisfies $x_{\max} \approx 2.82$, bracketed by

$$\text{wien\_floor} = \text{LAM} = 2 \leq x_{\max} \leq \text{wien\_ceil} = Q = 3.$$

## 9. Fock Space Structure

The photon Fock space is spanned by number states $|n\rangle$ for $n = 0, 1, 2, \ldots$.
The vacuum state $|0\rangle$ has Fock dimension 1 (`fock_vacuum_dim`). A NOON state requires
LAM = 2 optical modes. Coherent states have mean photon number 1 at minimum uncertainty
(`coherent_mean_photon`).

## 10. Cosmic Photon Count

The estimated number of photons in the observable universe is $\sim 10^{88}$. The exponent is

$$\text{universe\_photon\_exp} = \text{LAM} \times \text{MU} \times (K - 1) = 2 \times 4 \times 11 = 88.$$

## 11. Conclusion

The photon Fock space and thermal physics are fully parametrised by W(3,3). The Planck integrand
power (Q=3), Stefan-Boltzmann exponent (MU=4), polarisation count (LAM=2), zero-point denominator
(LAM=2), and cosmic photon exponent (LAM×MU×(K-1)=88) all emerge from the graph's structure.

## References

- Planck, M. *Annalen der Physik* 4, 553–563 (1901).
- Einstein, A. *Annalen der Physik* 17, 132–148 (1905).
- Part CCLI: Single Photon QED Bridge (this series).
