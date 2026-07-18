# Pass 437 — Complete critical-group Smith weld

Pass 425 closed the characteristic-primary layers of the native Heisenberg bulk graph. Pass 435 proved every prime-to-characteristic layer. Pass 437 combines them into complete invariant factors.

## Primary decomposition

For \(q=p^f\), the characteristic-primary exponents are the affine-chart/projective-monomial layers from Pass 425. For every odd \(\ell\neq p\), Pass 435 gives

\[
K_{(\ell)}\cong
(\mathbb Z/\ell^{\nu_\ell(q-1)})^{m_+}
\oplus
(\mathbb Z/\ell^{\nu_\ell(q+1)})^{m_-},
\]

while the 2-primary component is

\[
K_{(2)}\cong
(\mathbb Z/2^{\nu_2(q-1)})^{q(q-1)}
\oplus
(\mathbb Z/2^{\nu_2(q^2-1)})^{m_-}.
\]

To recover invariant factors, sort each prime's exponent list increasingly, pad shorter lists on the left with zeros, and multiply coordinatewise. This is the unique invariant-factor alignment compatible with divisibility.

## Exact complete groups

### \(q=3\)

\[
\boxed{
K_3\cong
(\mathbb Z/3)^4
\oplus(\mathbb Z/6)^4
\oplus\mathbb Z/18
\oplus\mathbb Z/54
\oplus(\mathbb Z/216)^6.
}
\]

This reconstructs Pass 431 exactly and serves as the weld checksum.

### \(q=5\)

\[
\boxed{
K_5\cong
(\mathbb Z/5)^{29}
\oplus(\mathbb Z/20)^{20}
\oplus(\mathbb Z/120)^7
\oplus(\mathbb Z/600)^{10}
\oplus(\mathbb Z/3000)^{23}.
}
\]

### \(q=9\)

\[
\boxed{
\begin{aligned}
K_9\cong{}&
(\mathbb Z/3)^{128}
\oplus(\mathbb Z/9)^{140}
\oplus(\mathbb Z/72)^{72}
\oplus(\mathbb Z/720)^{80}\\
&\oplus(\mathbb Z/2160)^{92}
\oplus(\mathbb Z/6480)^{37}
\oplus(\mathbb Z/58320)^{79}.
\end{aligned}}
\]

### \(q=25\)

\[
\boxed{
\begin{aligned}
K_{25}\cong{}&
(\mathbb Z/5)^{3200}
\oplus(\mathbb Z/25)^{3399}
\oplus(\mathbb Z/600)^{600}
\oplus(\mathbb Z/15600)^{2977}\\
&\oplus(\mathbb Z/78000)^{2800}
\oplus(\mathbb Z/390000)^{800}
\oplus(\mathbb Z/9750000)^{623}.
\end{aligned}}
\]

### \(q=27\)

\[
\boxed{
\begin{aligned}
K_{27}\cong{}&
(\mathbb Z/3)^{1920}
\oplus(\mathbb Z/9)^{3678}
\oplus(\mathbb Z/27)^{3256}
\oplus(\mathbb Z/702)^{702}\\
&\oplus(\mathbb Z/19656)^{2854}
\oplus(\mathbb Z/58968)^{3354}
\oplus(\mathbb Z/176904)^{1596}\\
&\oplus(\mathbb Z/530712)^{595}
\oplus(\mathbb Z/14329224)^{727}.
\end{aligned}}
\]

## Verification

For every listed field:

- each primary valuation sum agrees with the Matrix--Tree spectrum;
- the invariant factors form a divisibility chain;
- the number of nontrivial invariant factors equals the characteristic-primary rank;
- the \(q=3\) group matches the independently computed exact Smith normal form.

This closes the characteristic/prime-to-characteristic boundary named in Pass 425.
