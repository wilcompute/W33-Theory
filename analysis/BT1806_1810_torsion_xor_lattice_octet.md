# Passes 1806–1810 — reconciliation addenda for the torsion/XOR/lattice/octet frontier

## Executive result

A late parallel packet, Passes 1701–1705, independently completed the same five main workstreams while this calculation was in flight. It owns the primary nonsplit Loewy theorem, the globally minimal 240-XOR exporter, the chiral four-packing orbit, the determinant-two saturated bridge, and the rank-45 frame/octet coherent configuration.

This packet is therefore released as a **nonduplicative reconciliation addendum**. Its exact verifier rebuilds `W(3,3)`, the `540 x 240` frame matrix `M`, the 45 intrinsic `K4,4` octets `K`, and

\[
J=\frac12MK^{\mathsf T}\in\{0,1\}^{540\times45}.
\]

All **31/31** checks pass. The addenda are:

1. an alternative exact composition series with full vector-orbit and endomorphism-field fingerprints;
2. the exact relation between a color-symmetric 270-XOR generator and the globally minimal 240-XOR basis;
3. a universal theorem proving every exact cover has identical linear Bockstein signature;
4. an explicit primitive representative of the unique determinant-two parity coset;
5. a proof that the coarse five-valued frame Gram partition is not closed, together with the characteristic-dependent rank collapse of `J` and `J^T J`.

The global Hoffman nine-coloring remains open.

---

## Pass 1806 — composition-series reconciliation

The 30-dimensional binary Bockstein torsion module admits the invariant chain

\[
0<V_1<V_9<V_{10}<V_{16}<V_{30},
\]

with successive factors

\[
\boxed{1,8,1,6,14}.
\]

This is compatible with the primary Loewy description

\[
1\mid(6\oplus8)\mid1\mid14.
\]

There is no contradiction: composition factors have the same multiset

\[
\boxed{1,1,6,8,14},
\]

and the order in which the semisimple middle constituents are refined is not canonical.

The addendum freezes stronger factor fingerprints:

- the 8-factor has nonzero-vector orbits of sizes 120 and 135, each spanning all 8 dimensions;
- the 6-factor has orbits 27 and 36, each spanning all 6 dimensions;
- every one of the twelve nonzero-vector orbits in the 14-factor spans all 14 dimensions;
- the 8-factor commutant is two-dimensional and contains an endomorphism satisfying \(T^2+T+I=0\), so its endomorphism field is \(\mathbb F_4\);
- the 6- and 14-factor commutants are scalar \(\mathbb F_2\).

No Brauer-character names are assigned.

---

## Pass 1807 — symmetric 270-XOR generator versus minimal 240-XOR basis

Thirty octet columns are independent modulo the 195-dimensional edge-image for each color. Retaining all nine colors gives a transparent color-symmetric generator with

\[
\boxed{30\cdot9=270}
\]

native XOR equations.

However, its rank gain over the edge and frame-partition equations is only

\[
\boxed{240}.
\]

Therefore the cross-color redundancy has exact dimension

\[
\boxed{270-240=30}.
\]

The mechanism is the color sum: for each selected octet, summing its nine color equations is already forced by the one-color-per-frame partition equations. The parallel minimal exporter removes one color and retains

\[
\boxed{30\cdot8=240}
\]

globally independent XOR directions.

The symmetric file is still useful for solver diagnostics because it preserves all nine colors explicitly. Its deterministic hash is

```text
f104065b227f2bee0af61afb52d9e95feac232b4bd2397f72bc3c0cd2caa9109
```

No SAT or UNSAT conclusion is inferred.

---

## Pass 1808 — universal Bockstein-signature blindness

For any exact-cover indicator \(x\),

\[
M^{\mathsf T}x=\mathbf1_{240}.
\]

Since \(2J=MK^{\mathsf T}\) and every octet contains 16 W33 edges,

\[
2J^{\mathsf T}x=KM^{\mathsf T}x=K\mathbf1=16\mathbf1.
\]

Hence

\[
\boxed{J^{\mathsf T}x=8\mathbf1_{45}}
\]

for **every exact cover**, not merely the known chiral packing pair.

Therefore every four-cover packing has signature

\[
\boxed{32\mathbf1_{45}},
\]

and the complementary 300-frame residual carrier has signature

\[
\boxed{40\mathbf1_{45}}.
\]

This proves that every linear Bockstein signature is orbit-blind. Packing extendibility must be controlled by nonlinear or higher-order orbit data.

---

## Pass 1809 — primitive representative of the parity coset

The primary lattice theorem gives the saturated unsigned-to-signed transition determinant

\[
\boxed{|\det Q|=2}.
\]

The addendum freezes an explicit primitive representative of the unique missing orientation-parity coset. In the canonical 240-edge coordinates it has

\[
\boxed{\text{support}=128,\qquad \|v\|^2=152}
\]

and SHA-256

```text
9f8ddb3e4ec321bea4cfc7f8fac921dc9cb971fcf40a5091e1c82e69724afd2d
```

Thus the abstract quotient \(\mathbb Z/2\) is represented by a literal edge vector, suitable for future equivariant orbit and stabilizer analysis.

---

## Pass 1810 — Gram-partition nonclosure and modular collapse

The full frame/octet action is the rank-45 two-fiber coherent configuration. The half-incidence matrix has frame-row intersection profile

\[
6^1,\quad3^{32},\quad2^{15},\quad1^{300},\quad0^{192}.
\]

A tempting shortcut would treat these five values as a five-class association scheme. The verifier disproves that shortcut: if \(R_1\) is the relation where two frame rows meet in one octet, then \(R_1^2\) takes eight distinct values on \(R_1\):

\[
\boxed{146,158,160,162,165,166,168,191}.
\]

Therefore the coarse Gram partition is not closed. The full rank-32 frame orbital algebra is essential.

The characteristic-sensitive ranks are also frozen:

\[
\operatorname{rank}_{2}J=44,
\qquad
\operatorname{rank}_{3}J=44,
\qquad
\operatorname{rank}_{5}J=45,
\]

while

\[
\operatorname{rank}_{2}(J^{\mathsf T}J)=14,
\qquad
\operatorname{rank}_{3}(J^{\mathsf T}J)=0,
\qquad
\operatorname{rank}_{5}(J^{\mathsf T}J)=45.
\]

This separates the full incidence module from its Gram image and identifies characteristics two and three as genuinely singular.

---

## Evidence boundary

All claims are exact finite computations. This addendum deliberately defers primary ownership to Passes 1701–1705 where the results overlap. It does not decide the global nine-cover problem, prove a physical threshold, or assign unverified modular character labels.
