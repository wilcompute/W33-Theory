# Passes 1861–1865 — Exceptional-\(S_6\) outer doily transfer clock

## Executive result

Pass 1859 froze a literal integral realization of the exceptional outer automorphism of \(S_6\): a permutation matrix \(P\in GL_{15}(\mathbb Z)\), \(\det P=-1\), carrying the duad action to the outer-twisted syntheme action. The older doily packet independently froze the \(15\times15\) syntheme/duad incidence matrix \(D\), with rank \(10\), nullity \(5\), and singular-square spectrum \(9^1+4^9+0^5\).

Define the folded outer incidence transfer

\[
T=P^{\mathsf T}D\in\{0,1\}^{15\times15}.
\]

It is a doubly 3-regular, nonnormal, outer-twisted \(S_6\)-equivariant operator. The exact verifier proves all 24 checks.

## Pass 1861 — saturated integral transfer

The transfer has

\[
\operatorname{rank}_{\mathbb Q}T=
\operatorname{rank}_{\mathbb F_2}T=10,
\qquad
\dim\ker T=5.
\]

Its Smith normal form has ten nonzero invariant factors and every one equals \(1\). Hence \(\operatorname{im}_{\mathbb Z}T\) is a saturated rank-10 sublattice of \(\mathbb Z^{15}\); the rank defect is not hiding torsion.

The exact characteristic polynomial is

\[
\boxed{
\chi_T(x)=x^5(x-3)(x-2)(x+2)^2(x^2+4)(x^4+16).
}
\]

The exact minimal polynomial is

\[
\boxed{
\mu_T(x)=x(x-3)(x^8-256).
}
\]

## Pass 1862 — nine-dimensional order-eight clock

The all-ones vector spans the Perron line with eigenvalue \(3\). Removing that line from the nonzero image leaves a nine-dimensional balanced carrier

\[
W=\operatorname{im}(T)\cap\mathbf 1^\perp,
\qquad \dim W=9.
\]

On \(W\),

\[
\boxed{(T/2)^8=I_W.}
\]

Equivalently, the balanced spectrum consists of twice all eight eighth roots of unity, with \(-2\) occurring once more. The integral identity avoiding rational projectors is

\[
\boxed{
(T^8-256I)T=1261J,
}
\]

where \(J\) is the \(15\times15\) all-ones matrix. The closed-walk traces obey, for every \(n\ge1\),

\[
\boxed{
\operatorname{tr}(T^n)=3^n+(-2)^n+8\,2^n\,[8\mid n].
}
\]

The verifier checks this formula through \(n=16\), while the factorization of \(\mu_T\) proves it for all \(n\).

## Pass 1863 — exceptional twisted equivariance

Let \(\rho\) be the natural action of \(S_6\) on the 15 duads and let \(\alpha\) be the exact exceptional outer automorphism frozen in Pass 1859. For each Coxeter generator, and therefore for every \(g\in S_6\),

\[
\boxed{
T\rho(g)=\rho(\alpha^{-1}(g))T.
}
\]

Thus \(T\) is not an ordinary commutant operator; it is an intertwiner between the natural duad module and its exceptional outer twist. The exact enumeration of all 720 elements also finds

\[
\alpha^2=\operatorname{conj}_h
\]

for a unique \(h\) in the chosen coordinate gauge, with cycle type \((4,2)\).

## Pass 1864 — doily Gram bridge

Because \(P\) is orthogonal,

\[
\boxed{T^{\mathsf T}T=D^{\mathsf T}D.}
\]

Therefore the outer fold changes phase/orientation data without changing the doily singular geometry:

\[
\operatorname{spec}(T^{\mathsf T}T)=9^1+4^9+0^5.
\]

Moreover,

\[
A_{\rm doily}=T^{\mathsf T}T-3I
\]

is exactly the point graph of the generalized quadrangle \(W(2)\), with

\[
\boxed{A_{\rm doily}\text{ is }\operatorname{SRG}(15,6,1,3).}
\]

This separates the symmetric doily metric from the new outer-twisted directed clock: the Gram operator remembers the former, while \(T\) itself records the exceptional phase transport.

## Pass 1865 — evidence boundary

This is a finite representation-theoretic theorem. The phrase “clock” refers only to the exact order-eight normalized action on the nine-dimensional balanced image. No physical time evolution, Hamiltonian unitarity, continuum limit, or empirical prediction is inferred.

Artifacts:

- `analysis/w33_pass1861_1865_outer_doily_transfer_clock.py`
- `data/w33_pass1861_1865_outer_doily_transfer_clock.json`
- `tests/test_w33_pass1861_1865_outer_doily_transfer_clock.py`
- `analysis/BT1865_outer_doily_transfer_clock_insert.tex`
- `.github/workflows/pass1861_1865_outer_doily_transfer_clock.yml`
