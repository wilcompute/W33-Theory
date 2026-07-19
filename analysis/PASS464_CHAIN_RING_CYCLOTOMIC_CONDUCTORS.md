# Pass 464 — chain-ring cyclotomic covariance and conductor radicals

For \(R=\mathbb Z/p^n\mathbb Z\), let \(B_t\) be the central Weyl block attached to the additive character indexed by \(t\in R\). Pass 464 proves and verifies exactly:

\[
\sigma_a(B_t)=B_{at}\qquad(a\in R^\times).
\]

Inverse closure makes each \(B_t\) Hermitian, and

\[
B_{-t}=\overline{B_t}=B_t^{\mathsf T}.
\]

If \(v_p(t)=r<n\), then:

- the central character has order \(p^{n-r}\);
- its kernel on the center has size \(p^r\);
- the radical of the induced alternating bicharacter on \(R^2\) has size \(p^{2r}\);
- block entries lie in \(\mathbb Z[\zeta_{p^{n-r}}]\);
- characteristic coefficients fixed by the star involution lie in \(\mathbb Q(\zeta_{p^{n-r}})^+\).

The local polynomial \(\Phi_{p^k}(1+u)\) is Eisenstein at \(p\), so the coefficient order is totally ramified with index \(\varphi(p^k)\).

The exact witnesses are:

- \(\mathbb Z/9\): conductor strata of sizes \(6\) and \(2\), radical sizes \(1\) and \(9\), primitive ramification index \(6\);
- \(\mathbb Z/25\): strata of sizes \(20\) and \(4\), radical sizes \(1\) and \(25\), primitive ramification index \(20\).

The integral Smith module does not split under this Fourier decomposition because the characteristic-prime Fourier transform is not unimodular. Pass 466 addresses that coupling.
