# Heavy mass winding in radial monopole spectra and reflection

Each heavy W33 mass phase winds three charged asymptotic radial channels of the primitive monopole. For an isolated massive half-line model with fixed self-adjoint boundary, a full winding gives three downward zero crossings. In a model coupled to massless channels the same asymptotic winding can instead appear in the light reflection determinant, with no bound-state crossing. The calculation distinguishes these mechanisms and gives an explicit boundary invariant to test on the smooth core. [Standard Model bundle and Witten response](2026-11-13_sm_threshold_theta.md) · [Spectral flow of half-line Dirac operators](https://arxiv.org/abs/2007.06193)

## Which massive channels wind

On the canonical five-block the monopole cocharacter is `m=(1,0,0,−1,0)`. Write eᵢ for its diagonal characters. The sphere Dirac index for a weight λ is `λ(m)` in the chosen flux orientation. For unit flux the lowest angular space is one-dimensional. A color or weak adjoint root and its opposite form a charged Dirac pair within a chiral Majorana multiplet. Choosing the representative of each pair with positive magnetic pairing, the winding weights are

| Mass phase | Unit-flux weights | Electromagnetic charges |
| --- | --- | --- |
| Adjoint | `e1−e2`, `e1−e3`, `e5−e4` | 0, 0, −1 |
| Triplet | `e1`, `e1`, `e1` | −1/3, −1/3, −1/3 |

The other weights in those representations have zero flux or are their opposite-weight partners. The triplet count follows from the exact mass determinant `det B(z_T)/det B(1)=z_T³`. At the charged weight, its mass loop is invertible for every unit-modulus z_T. The rank-three projector gives a gapped homotopy to three winding masses and 18 constant ones. The adjoint roots already carry a common phase. Each table row sums to the previously derived Witten weight and consists of three κ-odd channels. [Exact colored determinant](2026-11-13_canonical_strong_cp.md) · [W33 angular channels and the rotor endpoint](2026-11-11_monopole_electric_phase.md)

## Isolated massive channels

For the exterior model use `H=−iσ3∂x+M(cos φ σ1+sin φ σ2)` on x≥0 with `M>0`. The boundary current vanishes for `ψ_−(0)=e^{iβ}ψ_+(0)). Substitution of a decaying wave gives

```text
E = M cos(φ−β),     decay exponent = M sin(φ−β) > 0.
```

There is one downward crossing at `φ=β+π/2` per full winding. This count holds with unequal positive masses and a fixed unitary mixing among winding channels. At zero energy the decaying boundary ratio is `−i e^{iφ}` for each channel, independent of its mass. Crossings occur at the eigenphases of the unitary boundary. For crossing vector v the derivative of the eigenvalue is `−Σ|v_j|² / Σ(|v_j|²/M_j)`, strictly negative. The derivative form is negative definite on a degenerate crossing space, so multiplicity is retained. The signed weight sum of the three downward crossings agrees with the canonical electric relabeling when a negative-energy level is filled. This exterior calculation supplies no occupation dynamics for an isolated monopole.

## Mixing with gapless channels

The full canonical GUT spectrum includes light charged fields. Once they are coupled to the massive channels, zero energy belongs to the essential spectrum of the half-line operator. A bound-state Fredholm count by itself is then insufficient. An explicit exterior model shows how winding can be transferred to reflection.

At zero energy let A be the boundary ratio of the decaying heavy wave. For a general invertible complex mass matrix in the convention `H_offdiag=(M†,M)`, A is `−i` times the unitary polar factor of M, so its determinant has the mass winding. Impose a unitary boundary matrix U from outgoing to incoming components and split it into heavy h and massless light ℓ blocks. Eliminating the decaying heavy amplitudes gives the outgoing-to-incoming light relation

```text
S = U_ℓℓ + U_ℓh (A−U_hh)⁻¹ U_hℓ
det S = det U · det(I−U_hh† A) / det(U_hh−A).
```

The determinant identity follows by taking the Schur complement in `U−diag(A,0)` and factoring out U. If `||U_hh||<1` throughout the loop, both determinant factors of the form I minus a strict contraction have zero winding. There is no localized zero-energy state and the physical incoming-to-outgoing reflection `S⁻¹` has winding `wind det A−wind det U`. The hypothesis makes the reflection result stable against changes in the positive heavy singular values. [Boundary and spectral-flow splitting](https://arxiv.org/abs/math/9902142)

For one heavy and one light channel, take the real rotation with first row (3/5,4/5) and second row (−4/5,3/5). For `A=z` on the unit circle, S is `(1−3z/5)/(3/5−z)`. It has a pole inside the disk and a zero outside, giving winding +1 for the inverse. Direct sums with isolated massive channels give all four splits of the three-channel count between downward crossings and positive reflection winding. If the heavy row of U itself acquires a factor z, `det U=z` and S becomes the constant −1 while the compression stays strictly contractive. Thus an imposed winding boundary can compensate the asymptotic mass winding in the reflection observable.

## What a finite smooth-core transfer can change

In a closed finite set of radial channels write the zero-energy equation as `−iJ ψ′+Vψ=0`, with `J=diag(I,−I)` and V Hermitian. The transfer matrix preserves the flux form J. It transports a maximal zero-flux subspace to another such subspace. At any finite radius the projection onto the positive-current coordinates is invertible on this subspace. Indeed, a vector in its kernel has only negative-current components, so zero flux forces that vector to vanish. The transported subspace therefore remains a unitary graph at every radius.

If the starting regular boundary graph is independent of the mass phase, the full graph at any finite matching radius is homotopic to that constant loop by radial transfer. Its determinant winding is zero. Consequently, a closed finite-channel core with phase-independent regular origin data and a strictly contractive heavy compression at matching would give light reflection winding three. This statement uses the full graph before eliminating channels. Projecting out other channels, passing through singular limits, or using an origin graph with nontrivial phase dependence requires a separate analysis. The physical smooth core still needs its radial channel space, regular origin data and heavy compression computed. The asymptotic Witten shift alone leaves the distribution between bound levels and scattering open.

Run `python analysis/toe_20261113_monopole_heavy_phase_flow.py` from the repository root. [Exact output](../data/toe_20261113_monopole_heavy_phase_flow.json)
