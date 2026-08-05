# Passes 3390–3403 — exterior switch boundary, defect realizability, proof sidecars, Clifford+T bounds, and shell duality

## Executive result

This packet executes the five requested continuations and two additional high-risk constructions. It is intentionally strict about the object/evidence boundary:

- the exact-cover census supports a two-sheet-plus-cap decomposition, but the readable repository still lacks the complete representative/switch ledger needed for an objectwise second-sheet theorem;
- all eleven balanced arithmetic-semidefinite defect types survive the canonical 45-block local laws;
- a live fail-closed sidecar packet is frozen for all 100 active depth-four chromatic leaves;
- the explicit 1,350-token walk receives a concrete source-level Clifford+T upper bound and an arithmetic alternative;
- the shell-spectrum reversal is promoted from a five-coordinate observation to an exact infinite odd-dimensional Hamming family;
- the Q15 dual and span are joined by an exact MacWilliams transform;
- the 57-class exceptional cap is isolated as the full stabilizer-eight locus in a precise branched-double-cover census skeleton.

The chromatic boundary remains

\[
\boxed{10\leq\chi(H)\leq11}.
\]

---

## Passes 3390–3391 — objectwise exterior-switch audit

The complete cover-orbit census is

\[
327\text{ orbit classes},\qquad3{,}547{,}800\text{ covers}.
\]

The known Hamming switch component is

\[
135\text{ classes},\qquad1{,}574{,}640\text{ covers},\qquad2^{108}4^{27}.
\]

The exceptional nonlinear-signature cap is

\[
57\text{ classes},\qquad398{,}520\text{ covers},\qquad2^{12}4^{30}8^{15}.
\]

Exact subtraction leaves

\[
135\text{ classes},\qquad1{,}574{,}640\text{ covers},\qquad2^{108}4^{27}.
\]

Hence

\[
\boxed{327=135+135+57}
\]

and

\[
\boxed{3{,}547{,}800=1{,}574{,}640+1{,}574{,}640+398{,}520}.
\]

The verifier searches the expected readable representative-ledger paths before attempting any graph claim. In the currently readable source tree, those complete representatives are not available. Therefore this pass closes the **objectwise audit**, not the objectwise connectivity theorem: no second switch component, path system, canonical pairing, or graph isomorphism is asserted from counts alone.

---

## Passes 3392–3393 — exact local realizability of all eleven defect types

For a balanced ten-colouring, every colour class has size 54. Under an \(S_m\times S_{10-m}\) colour split, write the defect-Gram off-diagonal values as

- \(a\) within the first block;
- \(b\) within the second block;
- \(c\) across the split.

The exact conditions are

\[
K_{ii}=324,\qquad K\mathbf1=0,\qquad K\succeq0,\qquad K_{ij}\equiv9\pmod{15}.
\]

Exhaustion gives the same split census as Pass 3346:

\[
1,1,5,3,5
\]

for splits \(1+9,2+8,3+7,4+6,5+5\), respectively. The 15 split-tagged matrices collapse to eleven distinct spectra.

The new result is a common 45-block witness. The 540 colour tokens are distributed through the canonical

\[
45\times\bigl(K_{12}\setminus3K_4\bigr)
\]

local blocks so that:

- each colour appears exactly 54 times;
- in every block a colour occurs in at most one of the three independent four-cells;
- every local colour-pair edge contribution lies between 40 and 60;
- every defect template requires at least 176 global edges for each of its pair types.

Thus

\[
\boxed{\text{all eleven arithmetic-semidefinite templates survive every canonical local block law}.}
\]

The obstruction to a ten-colouring, if one exists, must involve the 6,480 inter-block edges, not the induced 45-block geometry alone.

Frozen local-witness SHA-256:

```text
728c61a1e147b422ae2dc149ad995ceb7b84edc0301642ba131cd91315b455ba
```

---

## Pass 3394 — live 100-leaf fail-closed sidecar packet

The active depth-four leaves are

\[
(0,3,c,d),\qquad c,d\in\{0,\ldots,9\}.
\]

This packet emits one canonical sidecar record per leaf. Until a solver result and independent model/proof verification are attached, every leaf remains `UNKNOWN`.

Each record includes:

- the frozen base-DIMACS SHA-256;
- the exact shard tuple;
- solver exit code;
- terminal status;
- independent model/proof-check flags;
- proof/model artifact reference;
- a content hash.

Parent promotion remains:

- SAT after one checked SAT child;
- UNSAT only after all ten children are independently proof-checked UNSAT;
- UNKNOWN otherwise.

No current leaf is promoted merely because a large workflow artifact exists or a job completed.

---

## Passes 3395–3396 — source-level Clifford+T compiler bounds

The explicit quotient-walk table has 1,350 rows and a 12-bit address (`8-bit species + 4-bit token`). A direct reversible source construction uses one twelve-controlled equality flag per row.

With ten clean ancillas, a twelve-controlled equality is implemented with

\[
2\cdot12-3=21
\]

Toffolis. Computing and uncomputing the flag for all rows gives

\[
\boxed{56{,}700\text{ Toffolis}}
\]

for the transition-table oracle. Under a conservative seven-\(T\) Toffoli decomposition,

\[
\boxed{396{,}900\ T\text{ gates}}
\]

is a source-level upper bound. Output fanout uses Clifford CNOTs.

The packet also freezes the lower-memory arithmetic alternative:

1. decode the five ternary symbols;
2. select one of five coordinates and one of two nonzero increments;
3. add \(\pm1\) modulo three;
4. compare the state with its \(\tau\)-image;
5. canonicalize the orbit representative;
6. XOR the quotient index.

The persistent interface remains 25 logical bits. These are exact source-network resource bounds, not optimized Toffoli or \(T\)-counts and not a hardware-synthesis result.

---

## Passes 3397–3398 — general odd-dimensional shell-spectrum theorem

Let

\[
n=2r+1
\]

and consider \(H(n,4)\), with one coordinate fixed by \(\tau\) and the other \(2r\) coordinates paired.

The full guard-shell generating polynomial is

\[
N_r(x)=(x+3)^{2r+1}.
\]

The \(\tau\)-fixed shell polynomial is

\[
F_r(x)=(x+3)(x^2+3)^r.
\]

Therefore the quotient-shell polynomial is

\[
\boxed{Q_r(x)=\frac{(x+3)^{2r+1}+(x+3)(x^2+3)^r}{2}}.
\]

Write

\[
Q_r(x)=\sum_{s=0}^{2r+1}q_sx^s.
\]

The exact theorem is

\[
\boxed{m_j^{(+)}=q_{2r+1-j}},
\]

where \(m_j^{(+)}\) is the \(\tau\)-invariant multiplicity of Hamming eigengrade \(j\).

For \(r=2\), this recovers

\[
(q_0,\ldots,q_5)=(135,207,144,48,9,1)
\]

and

\[
(m_0^{(+)},\ldots,m_5^{(+)})=(1,9,48,144,207,135).
\]

The verifier freezes instances through \(r=6\), i.e. through \(H(13,4)\). This is an exact Fourier/MacWilliams duality for the odd Hamming family, not a numerical coincidence restricted to \(n=5\).

---

## Pass 3399 BONKERS — MacWilliams bridge from PG(3,2) to the 11-dimensional span

The Q15 parity-check code has weight enumerator

\[
W_D(z)=1+10z^6+5z^{12}.
\]

Its nonzero words are the 15 points of \(PG(3,2)\). The binary MacWilliams transform gives the exact weight enumerator of the 11-dimensional span:

\[
\begin{aligned}
W_{D^\perp}(z)= {}&1+15z^2+90z^4+243z^5+270z^6+405z^7\\
&+405z^8+270z^9+243z^{10}+90z^{11}+15z^{13}+z^{15}.
\end{aligned}
\]

The coefficients sum to

\[
2048=2^{11}.
\]

This provides an exact algebraic bridge between the projective parity-check geometry and the binary ambient span used by the guard construction.

---

## Passes 3400–3401 BONKERS — branched-double-cover census skeleton

At orbit-type level, the complete cover census has the exact form

\[
\boxed{327=2\cdot135+57}.
\]

Each regular 135-class sheet carries stabilizer histogram

\[
2^{108}4^{27}8^0,
\]

while the exceptional 57-class cap carries

\[
2^{12}4^{30}8^{15}.
\]

The sharp new organizational fact is:

\[
\boxed{\text{all fifteen stabilizer-eight orbit classes lie in the exceptional cap}.}
\]

Thus the census has the exact orbit-type skeleton of two regular sheets plus an enhanced-symmetry branch cap. This is useful as a search ansatz, but no quotient map, ramification involution, or switch-graph branched cover is claimed without representatives.

---

## Reproduction

```bash
python analysis/bt3390_3401_validated_runner.py
pytest -q tests/test_bt3390_bt3403_exterior_switch_defect_clifford_shell.py
```

## Evidence boundary

Not promoted:

- objectwise connectivity or isomorphism of the exterior 135-class residual;
- any checked SAT or UNSAT decision for ten colours;
- an exact rational dual excluding ten colours;
- optimal Clifford+T counts;
- simulator, synthesis, placement, PDF or laboratory results;
- quantum speedup, physical qubits, spacetime, topological order, power or fabrication claims.
