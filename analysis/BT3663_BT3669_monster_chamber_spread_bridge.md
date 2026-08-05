# Passes 3663–3669 — Canonical Monster-facing chamber/spread bridge

## Release status

The exact verifier

`analysis/w33_pass3663_3669_monster_chamber_spread_bridge.py`

passes all 25 checks and reproduces frozen semantic certificate

`ea0d3d989c05d51dc1e60de05cb9fe9f3308d8c36f1e40749b915f7bc0aaefca`.

This packet is deliberately objectwise. It does **not** identify two 36-point objects merely because their orbital graphs share parameters.

## Prior-art boundary

Two earlier fronts are retained rather than reclaimed.

1. Passes 3635–3648 constructed the explicit order-25,920 group, all 432 A5 subgroups, the 36 A6 chambers, their S6 normalizers, and the 36 disjoint K6,6 components of the D10-sharing graph.
2. Passes 1072/1079 and BT813 already identified the degree-36 spread action, its subdegrees 1+15+20, and the valency-15 rank-three orbital graph. Pass 1072 explicitly corrected an earlier attempt to infer this identification from SRG parameters alone.

The new result supplies the missing equivariant map and proves it preserves the full intersection relations.

## Theorem — the 36 A6 chambers are canonically the 36 W33 spreads

Let

\[
G=PSp(4,3)\cong U_4(2),\qquad |G|=25,920,
\]

acting on the forty points and forty lines of W(3,3). The exact cover search finds 36 spreads, each consisting of ten disjoint W33 lines.

Let \(H\cong A_6\) be one of the 36 A6 chambers reconstructed from a K6,6 component of the D10-sharing A5 graph. Its normalizer satisfies

\[
|N_G(H)|=720,
\qquad
[N_G(H),N_G(H)]=H.
\]

The normalizer fixes exactly one W33 spread \(\Sigma_H\), and the verifier proves

\[
N_G(H)=\operatorname{Stab}_G(\Sigma_H).
\]

Transport by the four explicit order-three generators is path-independent, giving a canonical G-equivariant bijection

\[
\boxed{
G/N_G(A_6)
\;\longleftrightarrow\;
\{\text{W33 spreads}\},
\qquad
H\longmapsto\Sigma_H.
}
\]

Both sides have size

\[
25,920/720=36.
\]

This is stronger than conjugacy of stabilizers: the verifier constructs the object attached to each chamber and checks equivariance generator by generator.

## Exact intersection dictionary

For distinct A6 chambers \(H,K\), exactly two cases occur:

\[
\boxed{
|H\cap K|=18
\iff
|\Sigma_H\cap\Sigma_K|=1,
}
\]

with 360 unordered pairs, and

\[
\boxed{
|H\cap K|=12
\iff
|\Sigma_H\cap\Sigma_K|=4,
}
\]

with 270 unordered pairs.

Thus the two complementary subgroup-intersection relations are precisely the two spread orbitals.

The order-12 relation is

\[
\operatorname{SRG}(36,15,6,6),
\qquad
\operatorname{spec}=15^1\oplus3^{15}\oplus(-3)^{20},
\]

and the order-18 relation is its complement,

\[
\operatorname{SRG}(36,20,10,12),
\qquad
\operatorname{spec}=20^1\oplus2^{20}\oplus(-4)^{15}.
\]

The graph identity is now carried by the explicit chamber/spread bijection, not by the parameter tuple.

## The exceptional S6 double-six inside every chamber

Each A6 chamber contains twelve A5 subgroups, split by the two global A5 conjugacy classes into

\[
6+6.
\]

Within either six-set, any two A5s intersect in A4 of order 12. Across the two six-sets, every pair intersects in D10 of order 10. Hence the cross-intersection graph is exactly

\[
K_{6,6}.
\]

The S6 normalizer acts faithfully on both six-sets. The two degree-six actions are not equivalent by an inner relabeling; their cycle types are exchanged by the exceptional outer automorphism of S6. The exact census includes

\[
(2,1,1,1,1)\longleftrightarrow(2,2,2)\quad(15+15),
\]

\[
(3,1,1,1)\longleftrightarrow(3,3)\quad(40+40),
\]

and

\[
(6)\longleftrightarrow(3,2,1)\quad(120+120).
\]

Cycle types \((5,1)\), \((4,2)\), \((4,1,1)\), and \((2,2,1,1)\) remain fixed as paired types. This supplies an executable exceptional-automorphism certificate rather than invoking the outer automorphism by name alone.

## Monster relevance

The Monster subgroup literature constructs 5B-containing U4(2) subgroups from compatible A5 configurations meeting in D10. The present theorem resolves the complete internal geometry of the resulting abstract U4(2) carrier:

\[
\text{A5 double-six}
\subset
S6=N_G(A_6)
\supset
A6=[S6,S6]
\longleftrightarrow
\text{one W33 spread}.
\]

Therefore any future concrete Monster-word embedding of this U4(2) automatically transports all 36 spreads, all 36 A6 chambers, both rank-three orbitals, and every local exceptional-S6 double-six chart.

## Evidence firewall

### Proved here

- the exact 36-spread census;
- the 36 A6 chambers reconstructed from the 432 A5s;
- equality of an A6 normalizer and a unique spread stabilizer;
- the G-equivariant 36-to-36 objectwise bijection;
- the complete intersection dictionary and both SRG identities;
- A6 as the derived subgroup of its S6 stabilizer;
- both faithful degree-six actions and the exceptional outer-automorphism cycle census.

### Not proved here

- serialized `mmgroup` words for U4(2) inside the Monster;
- a unique Monster class fusion or a degree-81 restriction multiplicity;
- identification with the 36 two-qutrit magic rays, whose orthogonality graph is not strongly regular;
- a Griess, Majorana, VOA, lattice-glue, or photonic multiplication law;
- remote CI or manuscript-PDF evidence until a workflow run is observed.

## References checked

- ATLAS of Finite Group Representations, Monster and U4(2) pages.
- P. E. Holmes and R. A. Wilson, *On subgroups of the Monster containing A5's*.
- GAP Character Table Library data for U4(2), U4(2).2, and the Monster.
