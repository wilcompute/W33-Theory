# Passes 3614–3627 — Monster/U4(2), Steinberg register, and exact falsifiers

## Executive result

This packet executes the Monster embedding, restriction, local-algebra, 3-local, integration, and two outside-the-box fronts under the evidence firewall.

The structural spine is

\[
W(3,3)\rightsquigarrow PSp(4,3)\cong U_4(2)\rightsquigarrow\mathbb M,
\]

where the last arrow is a documented subgroup direction plus a character-fusion program, not yet a chosen generator-level embedding.

## Exact W33 carrier

The verifier reconstructs the forty projective points of \(\mathbf F_3^4\), joins symplectically orthogonal points, and proves

\[
A^2=8I-2A+4J.
\]

For the eigenvalue-two projector numerator

\[
N=(12I-A)(A+4I)
\]

it obtains

\[
N^2=60N,\qquad \operatorname{rank}N=24,
\]

with diagonal 36, adjacent entry 6, and nonadjacent entry -4.

## U4(2) class fusion and the 81 restriction problem

The GAP companion enumerates possible class fusions with decomposability initially disabled, imposes the documented 5B-type constraints

\[
2\mapsto2B,\qquad3\mapsto3B,\qquad5\mapsto5B,
\]

and then restores the character criterion by restricting the Monster degree-196883 character. It records every nonnegative integral decomposition and the set of possible multiplicities of the unique degree-81 constituent. Ambiguity is reported rather than silently resolved.

The degree 81 is not only a repeated count:

\[
81=3^4=|\operatorname{Syl}_3(U_4(2))|.
\]

The GAP certificate checks that the unique degree-81 Steinberg character vanishes on every nonidentity 3-power class, hence restricts regularly to a Sylow-3 subgroup. The protected Levi module is therefore a concrete candidate 3-local register.

## Concrete embedding front

The mmgroup harness refuses promotion unless a candidate supplies serialized Monster generators, exact generator and relation orders, a class-fusion map, and an independent image-order certificate equal to 25920. Character-table fusion alone is not accepted as a concrete embedding.

## Majorana/Griess boundary

For the documented 5B-type U4(2) class, both subgroup involution classes fuse to Monster 2B. Standard Monster Majorana axes model 2A involutions. Therefore a direct identification of subgroup involutions with Majorana axes is blocked. The surviving direction is a 2B-centralizer/orbifold local algebra or an ambient construction of 2A axes.

## Bonkers I — direct Leech seed falsifier

Uniformly normalize the forty-vector rank-24 frame to squared norm four. The two off-diagonal inner products become

\[
\frac23,\qquad-\frac49.
\]

An integral lattice cannot contain this Gram submatrix. Thus the raw W33 frame is not directly a uniformly rescaled Leech subset. The surviving route is a nonuniform integral extension, glue code, quotient, or multi-copy cancellation.

## Bonkers II — raw moonshine-moment falsifier

Any sequence in the span of the three W33 adjacency eigenmodes \(12^n,2^n,(-4)^n\) obeys

\[
s_{n+3}=10s_{n+2}+32s_{n+1}-96s_n.
\]

The first Monster 1A coefficients violate this recurrence with exact residuals

\[
10933957100,\quad105149879960,\quad355102291024.
\]

Therefore raw adjacency moments are not the moonshine coefficients. A surviving bridge must use graded induction, Hecke/replicability, a VOA construction, or an ambient Monster module.

## Prime-separation theorem

\[
|U_4(2)|=2^6 3^4 5
\]

contains no element of order 47, 59, or 71, whereas

\[
196883=47\cdot59\cdot71.
\]

The factorization is external to the subgroup element-order geometry and cannot be narrated as an internal U4(2) mechanism.

## Integration

The shared TeX manifest carries the insert into `w33_paper.tex`, `photonic_holonet.tex`, and `holonet_machine_blueprint.tex`. The public index and standalone page separate proved computations, documented facts, pending certificates, and exact no-go results.

## Honest boundary

This packet does not claim a chosen pair of Monster words generating the repo's concrete U4(2), a unique class fusion, or an observed Steinberg multiplicity until the GAP certificate is generated. It does not claim that W33 incidence alone reconstructs the Griess product or the Leech lattice.
