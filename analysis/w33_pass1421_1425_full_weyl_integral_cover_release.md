# Passes 1421–1425 — full-Weyl bridge, integral defect, and cover-orbit extension

## Executive result

The explicit frame-cokernel/signed-turn bridge from Pass 1416 survives the full
outer Weyl involution, but it is not primitive over the integers.

1. The bridge is equivariant for
   \(\mathrm{PGSp}(4,3)\cong W(E_6)\), not merely \(\mathrm{PSp}(4,3)\).
2. The common degree-15 character is evaluated on all \(51{,}840\) Weyl elements.
3. The integral bridge has Smith invariants
   \(1^{10},3^4,6\), hence saturation index \(486=2\cdot3^5\).
4. Six independent exact-cover orbits are disjoint from the Pass-1417 frontier,
   raising the certified lower bound from \(226{,}800\) to \(298{,}080\).
5. One shared addendum is injected into both root manuscripts so the full-Weyl
   theorem and integral boundary cannot drift.

## Pass 1421 — full-Weyl bridge theorem

Let

\[
F=d^T(A-12I)(A-2I)N/16
\]

be the integral bridge of Pass 1416. The verifier uses the outer symplectic
similitude represented by \(\operatorname{diag}(1,1,2,2)\) over \(\mathbb F_3\).
It has multiplier \(-1\), lies outside \(\mathrm{PSp}(4,3)\), and generates the
full group of order \(51{,}840\).

If \(U_\tau\) is its unsigned edge action and \(S_\tau\) its orientation-signed
edge action, then exactly

\[
S_\tau K=KS_\tau,
\qquad
S_\tau F=FU_\tau.
\]

Thus the frame-cokernel realization and the signed \(K=10\) realization are
isomorphic as full \(W(E_6)\)-modules.

## Pass 1422 — Weyl character fingerprint theorem

The two characters agree on every element of the full Weyl group. Their value
distribution is

\[
15^1,\;6^{80},\;3^{1320},\;2^{2160},\;1^{7920},\;0^{25248},
\;-1^{13635},\;-2^{1440},\;-5^{36}.
\]

On the outer coset alone the distribution is

\[
3^{540},\;1^{7920},\;0^{9504},\;-1^{6480},\;-2^{1440},\;-5^{36}.
\]

The chosen outer involution has trace \(3\) on the common degree-15 module.

## Pass 1423 — integral Smith obstruction theorem

The rational bridge is not an isomorphism of the natural integral lattices. Its
nonzero Smith invariants are

\[
1^{10},\quad 3^4,\quad 6.
\]

Therefore the image has index

\[
486=2\cdot3^5
\]

in its saturation, and the finite lattice defect is

\[
\mathbb Z/2\oplus(\mathbb Z/3)^5.
\]

The modular ranks are \(14,10,15,15\) at \(p=2,3,5,7\), so only the primes
\(2\) and \(3\) obstruct integral equivalence.

## Pass 1424 — exact-cover frontier extension

Pass 1417 certified sixteen distinct \(C_2\) cover orbits plus four additional
stabilizer types, giving the lower bound \(226{,}800\). The present verifier
reconstructs that deterministic prefix and compares it with seven independently
generated covers. Those seven collapse to six orbits—five \(C_2\) and one
\(C_4\)—and all six are disjoint from the frozen Pass-1417 \(C_2/C_4\) frontier.

Their added orbit mass is

\[
5\cdot12960+6480=71280,
\]

so the new certified lower bound is

\[
\boxed{298080}.
\]

This remains a lower bound, not a complete enumeration.

## Pass 1425 — shared manuscript addendum

`BT1425_full_weyl_integral_cover_addendum.tex` is inserted immediately after the
Pass-1420 bridge in both root manuscript wrappers. It states the full-Weyl
extension, the integral Smith obstruction, the improved cover lower bound, and
the scope firewall.

## Validation

- combined exact verifier: 24/24 checks pass;
- deterministic certificate SHA-256:
  `27fdcc78da468d8c220fd5f4e7145aa5a50b7cf6789a546b8ae0a046bbedcd30`;
- focused regression test passes;
- minimal LaTeX compilation of the shared addendum passes.

## Honest boundaries

- The exact cover total and complete orbit census remain open.
- The finite bridge is not a physical propagator by itself.
- Full \(W(E_6)\)-equivariance does not derive optical scalability, contextual
  fraction, Chern response, Standard-Model parameters, or cosmology.
