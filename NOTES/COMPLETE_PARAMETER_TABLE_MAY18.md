# Complete W(3,3) Parameter Table
## Updated May 18, 2026 (Sessions 15-16)

All parameters expressed in terms of $q = 3$ (GF field characteristic).

## Spectral Parameters

| Parameter | Symbol | Formula | Value | Derivation |
|-----------|--------|---------|-------|------------|
| Field char | $q$ | — | 3 | GQ(q,q) base |
| Regularity | $k$ | $q(q+1)$ | 12 | GQ formula |
| Vertex count | $n$ | $(q+1)(q^2+1)$ | 40 | GQ formula |
| Edge count | $|E|$ | $nk/2$ | 240 | $k$-regular |
| Eigenvalue 1 | $\lambda$ | $\Phi_1(q)=q-1$ | 2 | Spectral theory |
| Eigenvalue 2 | $-\mu$ | $-\Phi_2(q)=-(q+1)$ | $-4$ | Spectral theory |
| Multiplicity 1 | $f_1$ | $2q(q+1)=2k$ | 24 | = $\dim(\Lambda_{24})$ |
| Multiplicity 2 | $f_2$ | $q(q+2)$ | 15 | Spectral theory |
| Genus | $g$ | $|E|-n+1$ | 201 | Topology |

## Arithmetic Parameters

| Parameter | Symbol | Formula | Value | Derivation |
|-----------|--------|---------|-------|------------|
| Ihara prime | $p_{\rm Ih}$ | $k-1 = q^2+q-1 = \Phi_1(k) = \sqrt{\Phi_5(q)}$ | 11 | Ihara theory |
| Ihara prime² | $p_{\rm Ih}^2$ | $\Phi_5(q)$ | 121 | Cyclotomic |
| 6th cyclo | $\phi_6$ | $\Phi_6(q) = q^2-q+1$ | 7 | Eisenstein norm |
| 3rd cyclo | $\beta$ | $\Phi_3(q)=q^2+q+1=\Phi_2(k)$ | 13 | TWO cyclotomic derivations |
| 12th cyclo | — | $\Phi_{12}(q)=q^4-q^2+1$ | 73 | Full ring norm |
| 5th cyclo | — | $\Phi_5(q) = q^4+q^3+q^2+q+1$ | 121 | $= p_{\rm Ih}^2$ |

## Physical Constants

| Constant | Formula | Value | Source |
|----------|---------|-------|--------|
| $\alpha^{-1}$ | $\Phi_5(q)+\Phi_2(q)^2 = p_{\rm Ih}^2+\mu^2$ | 137 | Gaussian norm |
| $\alpha^{-1}$ | $q^4+2q^3+2$ (q=3 only) | 137 | Previous formula |
| $\beta_0$ | $N_{\mathbb{Z}[\omega]}(q+\omega)=\Phi_6(q)$ | 7 | Eisenstein norm |
| $\beta_{1/2}$ | $N_{\mathbb{Z}[\omega]}(\mu+\omega)=\Phi_6(\mu)$ | 13 | Eisenstein norm |
| $k_3$ | $q$ | 3 | RG ambiguity fixed |

## Heegner Numbers Appearing

All Heegner numbers: $\{1, 2, 3, 7, 11, 19, 43, 67, 163\}$

W(3,3) uses: $\{3, 7, 11\}$ (positions 3, 4, 5 in sequence)

- $q = 3$: field characteristic, GF(3)
- $\phi_6 = 7$: Eisenstein norm of $(q+\omega)$, $\Phi_6(q)$  
- $p_{\rm Ih} = 11$: Ihara prime, $\Phi_1(k) = \sqrt{\Phi_5(q)}$

## Splitting Behavior of 137 = $\alpha^{-1}$

- $137 \equiv 5 \pmod{12}$: Frobenius $\sigma_5$ in $\text{Gal}(\mathbb{Q}(\zeta_{12})/\mathbb{Q})$
- $137 \equiv 1 \pmod{4}$: splits in $\mathbb{Z}[i]$ as $(11+4i)(11-4i)$
- $137 \equiv 2 \pmod{3}$: inert in $\mathbb{Z}[\omega]$
- $137 \equiv 4 \pmod{7}$: **splits** in $\mathbb{Q}(\sqrt{-7})$
- $137 \equiv 5 \pmod{11}$: **splits** in $\mathbb{Q}(\sqrt{-11})$
- Inert in $\mathbb{Q}(\sqrt{-43}), \mathbb{Q}(\sqrt{-67}), \mathbb{Q}(\sqrt{-163})$

$\alpha^{-1}$ splits in exactly the W(3,3) Heegner pair $\{-7,-11\}$ and is inert thereafter.
