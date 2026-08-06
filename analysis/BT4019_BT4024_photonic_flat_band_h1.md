# Passes 4019–4024: the protected H1 sector is an exact photonic flat band

## What is new relative to BT548

BT548 already identified the protected Levi cycle projector with the \(-2\) eigenspace of the Levi line graph. This packet does not relabel that algebraic theorem as new. It supplies the missing **physical-model translation and refinement**:

- the 160 incidence couplers are promoted to 160 secondary lattice sites;
- all 1620 Tits-building apartments become explicit compact localized states;
- their normalized apartment vectors form a unit-norm tight frame of redundancy 20 for the complete 81-dimensional flat band;
- every secondary site has the exact local address law “81 apartments through one site”;
- uniform shifts preserve the flat band, while a one-site perturbation splits it at first order, so no generic disorder immunity is claimed.

The executed semantic certificate is:

```text
e7746ea1730daea1b29d0e7831bc627c4d115ee0ccf1c81441796363101aa59f
```

## Pass 4019 — coupler-as-site line graph

Let \(L\) be the 80-vertex, 160-edge W33 point–line Levi graph. Promote each incidence edge of \(L\) to a site of the line graph

\[
X=\operatorname{LineGraph}(L).
\]

Then

\[
|V(X)|=160,\qquad |E(X)|=480,\qquad \deg X=6.
\]

For the oriented Levi boundary matrix \(D\),

\[
\boxed{A_X=D^TD-2I.}
\]

This is a secondary 160-site Hamiltonian model. It is not the same object as the primary 80-mode point–line Hamiltonian or as passive link-current coordinates.

## Pass 4020 — H1 is exactly the minus-two flat band

The spectrum is

\[
6^1,\quad(2+\sqrt6)^{24},\quad2^{30},\quad
(2-\sqrt6)^{24},\quad(-2)^{81}.
\]

Since \(A_X+2I=D^TD\),

\[
\boxed{\ker D=E_{-2}(A_X).}
\]

Thus the protected Hodge memory is exactly the \(-2\) flat band, with multiplicity 81. If \(C\) is the signed edge-by-apartment matrix,

\[
\boxed{P_{H_1}=\frac1{160}CC^T}
\]

and

\[
\boxed{CC^T=\frac12(A_X-6I)(A_X-2I)(A_X^2-4A_X-2I).}
\]

## Pass 4021 — apartments are compact localized states

The Levi graph has exactly 1620 simple octagons, its Tits-building apartments. Orient an apartment and place alternating amplitudes \(+1,-1\) on its eight incidence edges. The resulting vector \(c\) satisfies

\[
\boxed{A_Xc=-2c.}
\]

Each apartment state is compactly supported on eight secondary sites, and the 1620 apartment states span the entire rank-81 flat band.

## Pass 4022 — exact apartment tight frame

Every apartment column has norm \(\sqrt8\). After normalization, the 1620 vectors form a unit-norm tight frame in the 81-dimensional flat band:

\[
\boxed{
\left(\frac C{\sqrt8}\right)
\left(\frac C{\sqrt8}\right)^T
=20P_{H_1}.
}
\]

The frame bound and redundancy are both

\[
\boxed{\frac{1620}{81}=20.}
\]

The exact integer identity is

\[
(CC^T)C=160C.
\]

## Pass 4023 — local address law

Every one of the 160 secondary sites belongs to exactly 81 apartment states, while each apartment contains eight sites:

\[
\boxed{160\cdot81=1620\cdot8=12960.}
\]

This turns one physical incidence-link address into a uniform local index for 81 compact flat-band states.

## Pass 4024 — exact perturbation boundary

A uniform onsite term \(\delta I\) shifts the full flat band rigidly and does not split it. A one-site perturbation does split it:

\[
P_{H_1}|e\rangle\langle e|P_{H_1}
\]

has rank one and nonzero eigenvalue

\[
\boxed{\frac{81}{160}.}
\]

For arbitrary diagonal onsite values \(v_e\),

\[
\boxed{\operatorname{Tr}(P_{H_1}\operatorname{diag}v)
=\frac{81}{160}\sum_e v_e.}
\]

Therefore the flat band is exact in the symmetric finite Hamiltonian but is **not generically immune** to nonuniform onsite or coupling disorder.

## Literature context and boundary

Photonic flat-band localization through destructive interference and compact localized states is established in the literature. The result here is the exact W33/Levi realization, its full apartment basis, tight-frame constant, address law, and explicit perturbation boundary.

No 160-site secondary lattice has been fabricated. No measured localization, loss tolerance, disorder protection, coupling synthesis, variable vacuum speed, hidden photon-node ontology, or laboratory performance is claimed.
