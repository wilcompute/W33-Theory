# Passes 1310–1314 — Literal A5 Coset Correction and Carrier Firewall

## Scope

This packet repairs the newest Hecke/restriction frontier by replacing dimensional fits and candidate Burnside data with the literal finite permutation action. It is an exact statement about the groups

\[
W(E_6)\cong U_4(2){:}2,
\qquad
W(E_6)'\cong PSp(4,3)\cong U_4(2),
\]

and the three conjugate 432-point carriers arising from the action of \(W(E_6)\) on \(A_2\)-triples in the \(E_8\) root system. It makes no continuum, Hamiltonian, photonic-hardware, or particle-physics claim.

## Pass 1310 — Literal carrier reconstruction

The executable witness reconstructs:

- the 240 doubled \(E_8\) roots;
- the 2,240 \(A_2\)-triples;
- the faithful \(W(E_6)\) action of order 51,840;
- its derived subgroup \(PSp(4,3)\) of order 25,920;
- the exact \(A_2\)-triple orbit census

\[
1,1,27,27,27,27,27,27,240,270,270,432,432,432.
\]

For each 432-point orbit, the \(W(E_6)\) point stabilizer has order 120 and the intersection with the derived subgroup has order 60. Thus each carrier is simultaneously

\[
W(E_6)/S_5 \cong PSp(4,3)/A_5
\]

as a set with the restricted projective action.

## Pass 1311 — Exact A5 fixed-point and double-coset theorem

The literal \(A_5\) action on every 432-point carrier has classwise fixed-point vector

\[
\boxed{(f_{1A},f_{2A},f_{3A},f_{5A},f_{5B})=(432,24,36,2,2).}
\]

Burnside's lemma therefore gives

\[
\frac{432+15\cdot24+20\cdot36+12\cdot2+12\cdot2}{60}
=\boxed{26}.
\]

Hence the exact double-coset/Hecke dimension is

\[
\boxed{|A_5\backslash PSp(4,3)/A_5|=26},
\]

not 5 and not 9.

The complete orbit-size multiset is

\[
\boxed{1^2,\;5^6,\;10^4,\;20^9,\;30^4,\;60^1}
\]

which sums to 432 and has 26 parts.

## Pass 1312 — Exact restricted permutation character

Using the ordinary \(A_5\) character table, the 432-dimensional permutation character restricts as

\[
\boxed{
\mathbb C[\Omega_{432}]\downarrow_{A_5}
\cong
26\,\mathbf 1
\oplus16\,\mathbf 3
\oplus16\,\mathbf 3'
\oplus40\,\mathbf 4
\oplus30\,\mathbf 5.
}
\]

Dimension check:

\[
26+16\cdot3+16\cdot3+40\cdot4+30\cdot5=432.
\]

The restriction commutant has dimension

\[
\boxed{26^2+16^2+16^2+40^2+30^2=3688.}
\]

This number is distinct from the 26-dimensional double-coset algebra: 26 is the multiplicity of the trivial \(A_5\)-representation, while 3,688 is the full endomorphism-algebra dimension after restricting the carrier to \(A_5\).

## Pass 1313 — Carrier firewall

The directed-edge Hashimoto module has packet dimensions

\[
1+201+200+48+30=480.
\]

The coset carrier has dimension 432. Therefore:

\[
\boxed{\text{the five Hashimoto packets are not a decomposition of the 432-point coset carrier.}}
\]

Any species-to-packet dictionary must first state which representation it decomposes and must use literal characters or projectors. Divisibility, floor quotients, and dimension fits are capacity bounds only.

## Pass 1314 — Fail-closed correction ledger

The recent candidate vector

\[
(432,4,0,1,1)
\]

gives

\[
\frac{432+15\cdot4+20\cdot0+12\cdot1+12\cdot1}{60}
=\frac{43}{5},
\]

so it is not a permutation character and does not yield nine orbits. Any artifact that marks this calculation `PASS` must be demoted or corrected.

The following status corrections are required:

1. **Passes 1260/1263:** false fixed-point candidate; replace by the literal vector and 26-orbit theorem.
2. **Pass 1264:** a divisibility/capacity table, not an exact restriction decomposition.
3. **Passes 1265/1276:** a generic coordinate realization of \(M_{20}\), not yet a \(W(E_6)\)-equivariant AtlasRep matrix-unit embedding.
4. **Passes 1273–1277:** packet assignments inferred from dimension fits remain provisional until literal character/projector computation.
5. **All nine-basis Hecke tensors:** invalid for the 432 carrier; the literal basis has 26 double cosets.

## New research consequence

The corrected frontier is richer, not poorer. The next exact object is the 26-dimensional double-coset algebra

\[
\mathbb Q[A_5\backslash PSp(4,3)/A_5],
\]

with orbit valencies

\[
1^2,5^6,10^4,20^9,30^4,60.
\]

Computing its multiplication table and primitive idempotents gives a legitimate representation-theoretic bridge to compare against the 480-dimensional Hashimoto commutant. The comparison must be an explicit intertwiner or an explicit obstruction; shared dimensions alone are no longer admissible evidence.
