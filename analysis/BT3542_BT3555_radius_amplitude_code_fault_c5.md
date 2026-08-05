# Passes 3542–3555 — relation planes, exact magnetic conductors, code duality, compound fault distance, and the pentagonal rank-20 bridge

## Status

The exact verifier reports

```text
PASS_7_FRONTS 7f81f6763278f1e1fad5fafb0ea63c9b1b7c9518cbb9b0fd24375eb5832812a3
```

The live boundaries remain

\[
\boxed{389\le D_{H^1}\le435},
\qquad
\boxed{10\le\chi(H)\le11}.
\]

The unrestricted real five-channel optimum also remains open. Every finite-field relation, pair/triple census, rational spectral bound, code invariant, fault-CSP result, and subgroup restriction below is regenerated exactly. The algebraic stationary amplitude is explicitly separated from the certified global statements.

---

## 3542 — a new 263-term cohomology circuit

The 45-octet filled port complex is reconstructed independently. Its flat cochain model has 480 coordinates, the vertex-coboundary image has rank 44, and therefore

\[
\dim H^1=480-44=\boxed{436}.
\]

The 720 projective minimum defects generate this quotient. A deterministic basis-exchange search found a fundamental relation of weight

\[
\boxed{263},
\]

improving the previous 260-term witness. Its exact ternary relation has SHA-256

```text
d22f3661c1b2ab8e96936a693b887d2539c83fa9bd683b8465cbf900ce025fb8
```

and is checked directly against the reconstructed \(436\times720\) generator matrix. This does not change the universal upper bound: the exact one-circuit alphabet theorem from Pass 3514 still prevents a one-circuit proof below 435.

---

## 3543–3544 — complete rank-two direction census and an exact rank-three pilot

The 263 relation was made fundamental by retaining 262 of its support columns and extending them deterministically to a basis.

### All two-column relation planes

All

\[
\binom{284}{2}=\boxed{40{,}186}
\]

pairs of nonbasis columns were exhausted. Their rows define projective directions in \(PG(1,3)\), which has four points.

Exact results:

- maximum union support: \(\boxed{319}\);
- maximum occupied projective directions: \(\boxed3\);
- pairs occupying all four directions: \(\boxed0\);
- maximum population of one direction: \(\boxed{264}\).

For the direction-class pigeonhole method, the adversarial cancellation-cap histogram is

\[
\{2:34119,\ 3:5277,\ 4:790\}.
\]

Consequently, in this exact basis,

\[
\boxed{\text{the pure two-circuit direction method cannot prove }D_{H^1}\le433.}
\]

Exactly 790 pairs remain possible candidates for a 434 proof, but they require label-sensitive optimization rather than direction counting alone.

### Rank-three heavy-column pilot

The 64 heaviest nonbasis columns were selected canonically, and all

\[
\binom{64}{3}=\boxed{41{,}664}
\]

triples were exhausted in \(PG(2,3)\). The pilot found maximum union support 360, six occupied projective directions out of 13, maximum one-direction population 253, and direction-cap histogram

\[
\{3:544,\ 4:3383,\ 5:10325,\ 6:27407,\ 7:5\}.
\]

This is an exact selected-frontier pilot, not a global rank-three optimization. It shows that moving from a relation line to a relation plane genuinely increases projective diversity, but the endpoint remains open.

---

## 3545–3547 — exact \(2+5\) factorization of the five-channel amplitude algebra

The five exact channel sizes are

\[
\boxed{2,1,30,60,627}.
\]

The real 90-dimensional representation contains a 14-dimensional active subspace. Objectwise exact reduction shows that it is two real copies of one seven-dimensional rational conductor. For arbitrary channel weights \(w_0,\ldots,w_4\), the complex Hermitian characteristic polynomial is

\[
\boxed{(x+4w_4)^{17}(x-2w_4)^{21}q_2(x)q_5(x)}.
\]

The quadratic factor is

\[
\boxed{q_2(x)=x^2+(w_1+w_4)x+w_1w_4-9w_3^2}.
\]

The remaining factor \(q_5\) is an exact quintic frozen in the verifier and certificate. This proves that the entire five-channel spectral problem reduces from dimension 45 to one quadratic and one quintic.

At the normalized lower boundary \(w_4=1\), simultaneous contact of both active factors with \(x=-4\) gives

\[
w_1+3w_3^2=4
\]

and

\[
w_0^2+w_0w_2w_3+2w_1w_2^2-2w_1-9w_2^2w_3^2+8w_2^2+10w_3^2-8=0.
\]

These are exact algebraic equations for the observed double-boundary branch.

---

## 3548 — a sharper exact rational amplitude witness

The dyadic tuple

\[
\boxed{\frac1{32768}(-15576,44300,-28135,-30786,32768)}
\]

has residual characteristic factor

\[
x^2+77068x-7078377764
\]

multiplied by

\[
\begin{aligned}
x^5&-929036x^4-123569746314x^3+12019622717869256x^2\\
&+938578872802057568288x-48840032001367144572911616.
\end{aligned}
\]

Exact rational root isolation proves that no residual root lies below \(-4\), while the largest root yields

\[
\boxed{8.90622<h<8.90623}.
\]

This strictly improves the previous exact \(8.905<h<9\) witness.

The double-boundary KKT elimination also produces an exact degree-18 value polynomial. One isolated feasible stationary root is

\[
\lambda_{\max}\approx31.624923044652377,
\qquad
h\approx8.90623076116309.
\]

This is promoted only as an algebraic stationary candidate. A global proof over the unrestricted real cone has not yet been completed.

---

## 3549–3550 — complete duality atlas of the four frontier codes

For each exact binary \(S_3\)-equivariant dimension-five frontier code, the verifier computes the complete primal weight enumerator, exact MacWilliams dual enumerator, every generalized Hamming weight, every dual generalized weight by Wei duality, the hull dimension, and the full coordinate-set stabilizer in \(GL(5,2)\) by exhausting all 9,999,360 invertible maps.

### \([13,5,5]\)

\[
W(z)=1+6z^5+12z^6+4z^7+3z^8+6z^9.
\]

Dual distance 3; generalized weights \((5,8,10,12,13)\); hull dimension 2; automorphism order 48; coordinate orbits one singleton and one orbit of size 12.

### \([16,5,8]\)

\[
W(z)=1+30z^8+z^{16}.
\]

Dual distance 4; generalized weights \((8,12,14,15,16)\); hull dimension 5, so the code is self-orthogonal; automorphism order

\[
\boxed{322560=|AGL(4,2)|}.
\]

This independently certifies the objectwise identification with \(RM(1,4)\).

### \([24,5,11]\)

\[
W(z)=1+9z^{11}+9z^{12}+6z^{13}+6z^{14}+z^{15}.
\]

Dual distance 3; generalized weights \((11,17,21,23,24)\); hull dimension \(\boxed0\), so this frontier code is LCD; automorphism order 72; coordinate orbit sizes \(6,9,9\).

### \([28,5,14]\)

\[
W(z)=1+24z^{14}+7z^{16}.
\]

Dual distance 3; generalized weights \((14,21,25,27,28)\); hull dimension 3; automorphism order

\[
\boxed{64512=2^6|GL(2,2)||GL(3,2)|}.
\]

The code is exactly the binary simplex \([31,5,16]\) code punctured on the projective line \(\boxed{\{3,5,6\}}\).

---

## 3551–3552 — five companion bits are exactly necessary for robust double-fault readout

The sixteen Clebsch closed-neighbourhood columns give 30 base-syndrome collision classes among the 120 double faults. Every class contains four pairs, producing exactly 60 distinct four-point XOR constraints.

For an \(r\)-bit point label \(\ell_i\), the augmented syndrome difference on a collision constraint \(S\) is

\[
\bigoplus_{i\in S}\ell_i.
\]

To correct one corrupted readout bit, every such difference must have weight at least three. Exact canonical CSP exhaustion gives:

| companion bits | required distance | result | nodes |
|---:|---:|---:|---:|
| 3 | 2 | UNSAT | 29,513 |
| 4 | 3 | UNSAT | 1,553 |
| 5 | 3 | SAT | 10 |

Therefore

\[
\boxed{5\text{ companion bits are necessary and sufficient}.}
\]

One exact table is

\[
(0,0,0,0,30,25,0,7,0,27,13,22,14,18,29,1).
\]

The combined 21-bit readout has minimum distance three across all

\[
1+16+\binom{16}{2}=137
\]

zero-, single-, and double-device-fault patterns. It therefore both locates the device fault and corrects one corrupted compound-readout bit. The previous minimum three-bit injective locator has compound minimum distance exactly one.

`rtl/w33_clebsch_double_fault_locator5.v` publishes the new exact table.

---

## 3553 — the rank-20 firewall disappears exactly on \(C_5\)

The Perkel and W33 rank-20 modules have incompatible \(A_5\) characters, so no \(A_5\)-equivariant isomorphism exists. Their restrictions were classified for the subgroup types

\[
C_2,C_3,C_5,V_4,S_3,D_5,A_4,A_5
\]

inside the explicit common \(A_5\). The unique nontrivial subgroup type supporting a full rank-20 rational isomorphism is

\[
\boxed{C_5}.
\]

Both modules restrict as

\[
\boxed{4\cdot\mathbf1\oplus4\cdot\mathbb Q(\zeta_5)}.
\]

Thus

\[
\boxed{P_{20}\downarrow_{C_5}\cong W_{20}\downarrow_{C_5}}
\]

and the rational intertwiner space has dimension

\[
4^2+4(4^2)=\boxed{80}.
\]

This is a full module-level bridge, but it is not yet a canonical objectwise map. The larger subgroup types retain exact multiplicity obstructions.

---

## 3554 BONKERS — W33 edges resolve the entire filled port complex

The 45 port vertices are reconstructed as the canonical \(K_{4,4}\) octets of W33. Every W33 edge lies in exactly \(\boxed3\) canonical octets. Those three octets are pairwise adjacent in the 45-octet block graph, hence form one triangle.

This gives an exact objectwise bijection

\[
\boxed{\{240\text{ W33 edges}\}\longleftrightarrow\{240\text{ filled octet triangles}\}}.
\]

Moreover, the 240 triangles partition all \(240\cdot3=720\) edges of the 45-octet graph exactly once. So the filled port complex is not an auxiliary triangle choice: it is canonically resolved by the original W33 edge set.

---

## 3555 BONKERS — the magnetic cone has a quadratic conductor and a quintic conductor

The exact spectral reduction shows that all genuinely active five-channel information lives in

\[
\boxed{2\oplus5}
\]

rational spectral degrees. The remaining 38 complex dimensions depend only on the background channel \(w_4\).

This provides a new compiler principle: isolate the scalar \((-4,2)\) background sectors; solve one quadratic conductor exactly; solve one quintic conductor exactly; certify the extremal ratio with univariate root isolation. The result is a rigorous reduction of a 45-mode Hermitian optimization to two low-degree algebraic conductors. It is a finite spectral theorem, not a physical particle or spacetime claim.

---

## Reproduction

```bash
python analysis/bt3542_3555_radius_amplitude_code_fault_c5.py
pytest -q tests/test_bt3542_3555_radius_amplitude_code_fault_c5.py
iverilog -g2012 -s tb_w33_pass3542_3555 \
  -o /tmp/pass3542_3555 \
  rtl/w33_clebsch_double_fault_locator5.v \
  rtl/tb_w33_pass3542_3555.v
vvp /tmp/pass3542_3555
```

## Claim boundaries

- The covering radius remains open in \([389,435]\).
- The frame graph remains 10- or 11-chromatic.
- The unrestricted real amplitude optimum is not certified.
- The \(C_5\) module isomorphism is not yet a canonical objectwise map.
- No unobserved RTL, synthesis, placement, PDF, laboratory, particle, or spacetime result is promoted.
