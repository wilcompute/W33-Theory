# Passes 3418–3429 — Supplemental magnetic, coding, routing, fusion, and Clebsch–D5 closure

## Status

The exact source wrappers retain the provisional `bt3388_3399` build tag solely for byte-for-byte hash continuity after a parallel namespace collision. The published theorem namespace is 3418–3429. This supplemental packet starts from the parallel Passes 3364–3375 Clebsch–Petersen closure and does not replace it. The source-complete verifier reports **PASS 11/11**. It independently rebuilds the 45-block W33 port complex, its 720 minimum gauge-defect supports, the nonlinear signature controller, the five-bit envelope, the mirrored hypercube routers, and the folded-cube checksum graph.

The live chromatic boundary remains

\[
\boxed{10\leq\chi(H)\leq11}.
\]

All finite counts, code minima, graph isomorphisms, group orders, orbit decompositions, routing lower bounds, and fault censuses below are exact. The explicitly marked magnetic eigenvalue search is a deterministic high-margin numerical spectral audit with a posteriori residual data; it is not promoted to an exact rational SDP certificate.

---

## 3418 — edge-dependent magnetic audit beyond the three-cone compiler

The earlier packet proved that every separable lift \(A_{45}\otimes K\), even with arbitrary \(K\succeq0\) in the full local \(M_{22}\) algebra, retains Hoffman value nine. The parallel Clebsch–Petersen packet then reduced the full block-distance-invariant nonseparable class to three independent 22-by-22 PSD cones. The next tested family depends on the **individual block edge** as well as the local orientation sector.

For a flat \(C_3\) edge cochain \(z\), define the Hermitian magnetic adjacency

\[
M(z)_{ab}=\omega^{z_{ab}},\qquad
M(z)_{ba}=\overline{M(z)_{ab}},\qquad \omega=e^{2\pi i/3}.
\]

This is not a tensor product of one 45-block matrix with one local kernel. The packet exhausts:

- all 24 \(PSp(4,3)\)-orbits of unordered pairs of the 720 geometric minimum-defect supports;
- the same- and opposite-coefficient fusion on every pair orbit;
- all 48 resulting one/two-defect magnetic representatives.

The best nonzero candidate is already a single minimum defect:

\[
\lambda_{\min}\approx-5.073280337457312,
\qquad
\lambda_{\max}\approx31.877958425086288,
\]

and

\[
1-\frac{\lambda_{\max}}{\lambda_{\min}}
\approx
\boxed{7.283500280818951}.
\]

Using a conservative \(10^{-8}\) eigenvalue enclosure radius, its upper enclosure is

\[
\boxed{7.283500295176<9}.
\]

Across the entire nonzero family, the observed interval is

\[
6.539511211018519
\lesssim h(M(z))\lesssim
7.283500280818951.
\]

Thus the first exact finite nonseparable orientation family does **not** improve the chromatic lower bound. It actually weakens the spectral ratio. The useful result is a design constraint:

\[
\boxed{\text{edge-dependent phases alone are insufficient.}}
\]

A successful nonseparable dual must also retain profile-sensitive matrix amplitudes, not merely unit-modulus orientation gains.

---

## 3419 — independent nonlinear witness and minimum linear all-word code

The previous four-bit Clebsch tag corrected two state-bit errors only when the tag itself was trusted. The parallel packet already established the seven-parity nonlinear minimum; this packet supplies an independent distance-five witness and closes the previously open linear all-word minimum. Here the state and redundancy are jointly encoded so errors may strike either surface.

### Minimum nonlinear envelope code

For the 22 valid envelope states, search for a systematic code

\[
x\longmapsto (x,p(x))
\]

with minimum distance five. Global XOR symmetry fixes \(p(0)=0\), after which deterministic domain propagation exhausts the remaining assignments.

Results:

| parity bits | result | search nodes |
|---:|---:|---:|
| 4 | UNSAT | 1 |
| 5 | UNSAT | 1 |
| 6 | UNSAT | 232 |
| 7 | SAT | 666 |

Therefore

\[
\boxed{7\text{ parity bits are necessary and sufficient}}
\]

for arbitrary systematic encoding of the 22-state envelope. The resulting code has length 12, size 22, and distance distribution

\[
5^{83},\;6^{90},\;7^{13},\;8^{18},\;9^{25},\;10^2.
\]

Its radius-two balls are disjoint, and the exhaustive RTL target contains

\[
22\left(1+12+\binom{12}{2}\right)=\boxed{1738}
\]

received words.

### Minimum linear all-word code

For a linear systematic code, every nonzero five-bit difference occurs among pairs of envelope states, so the problem is exactly a binary linear \([5+r,5,5]\) code.

Weight-one messages require each parity column to have weight at least four. Input-coordinate permutations reduce the search to unordered five-subsets of those columns:

- \(r=6\): all \(\binom{22}{5}=26{,}334\) candidates are UNSAT;
- \(r=7\): all \(\binom{64}{5}=7{,}624{,}512\) candidates are UNSAT;
- \(r=8\): SAT.

Hence

\[
\boxed{8\text{ linear parity bits are necessary and sufficient}.}
\]

One exact parity-column set is

\[
(15,51,85,106,150),
\]

with parity-row masks

\[
(7,27,21,9,22,10,12,16).
\]

The resulting \([13,5,5]\) code has weight enumerator

\[
1+7y^5+10y^6+6y^7+4y^8+3y^9+y^{12}.
\]

This creates a precise engineering choice:

- **12-bit nonlinear code:** one bit smaller, envelope-only, LUT encoder;
- **13-bit linear code:** all 32 words, XOR-only encoder and uniform decoder.

`rtl/w33_envelope_self_protecting_code.v` publishes both encoders and bounded-distance decoders.

---

## 3420 — post-fault symbolic remapping with six fixed spares

Static one-cycle state-availability tolerance replicates all 16 logical states, using 32 physical slots. That lower bound remains correct for stored state whose only copy is destroyed. Under a different and explicit contract—a symbolic finite-state controller whose current logical state is retained in a protected register or recomputed, after which the physical state map may be recompiled—bounded remapping permits a smaller exact spare bank.

For each failed layer-zero state, the search allows states in its controller orbit to migrate into fixed layer-one spare coordinates while preserving every original transition distance. It exhausts all

\[
\sum_{k=1}^{5}\binom{16}{k}=\boxed{6884}
\]

banks of size at most five and finds none.

At size six, exactly 96 banks work. The lexicographically first is

\[
\boxed{\{0,1,2,3,4,5\}}.
\]

Therefore

\[
\boxed{6\text{ fixed spares are necessary and sufficient}}
\]

for exact-schedule **symbolic remapping** after any one state-slot loss under this protected-state/recompilation contract. The reconfigurable transition fabric shrinks from 32 simultaneously populated state slots to

\[
\boxed{16+6=22\text{ slots}}
\]

while retaining

\[
\boxed{34\text{ hops and dilation }2}.
\]

Depending on the failed logical state, an unconstrained adaptive placement needs only one, two, or three state migrations. With the fixed six-coordinate bank, the frozen maps use between one and six migrations.

A cheaper degraded policy that moves only the failed state has the exact Pareto frontier:

| spares | worst dilation | worst work | aggregate work |
|---:|---:|---:|---:|
| 1 | 4 | 46 | 640 |
| 2 | 3 | 42 | 606 |
| 3 | 3 | 38 | 596 |

More such spares do not improve that restricted policy. The theorem therefore separates **spare capacity** from **reconfiguration freedom**.

`rtl/w33_q5_dynamic_spare_router.v` implements the exact six-spare placement ledger.

---

## 3421 — gauge-defect fusion algebra

The 720 geometric minimum-defect supports have 24 unordered-pair orbits under \(PSp(4,3)\). Their orbit-size histogram is

\[
720^2,\;1080^1,\;2160^1,\;3240^2,\;4320^1,
\;6480^3,\;8640^2,\;12960^8,\;25920^4.
\]

The local fusion laws are exact:

1. same support, opposite coefficient: annihilation to zero;
2. same support, same coefficient: coefficient reversal, still weight two;
3. two corners of one filled face, same coefficient: the third minimum root;
4. two corners of one face, opposite coefficient: a full three-edge face state;
5. different filled faces: weight four.

The shortest unfilled-triangle syndrome counts are:

- minimum root: 42;
- full-face state: 63;
- disjoint-face composites: predominantly 84, with exact orbit refinements 76, 80, 82, 83, and 84.

The full 24-orbit/48-coefficient table is frozen in the result certificate.

---

## 3422 — complete triple-fault census and the Q6 boundary

The mirrored \(Q_5\) router is exhausted under all three-fault families.

| fault family | cases | catastrophic | worst work | worst dilation |
|---|---:|---:|---:|---:|
| three edges | 82,160 | 0 | 40 | 3 |
| one vertex + two edges | 101,120 | 0 | 42 | 4 |
| two vertices + one edge | 39,680 | 1,280 | 45 | 4 |
| three vertices | 4,960 | 480 | 46 | 4 |

The catastrophic counts have exact forms:

\[
1280=16\cdot80,
\qquad
480=16\cdot30.
\]

They occur exactly when a logical replica pair is removed, with any additional edge or vertex fault.

For guaranteed untouched-layer routing:

- three \(Q_4\) layers use 48 slots and are cardinality-minimal for arbitrary two-vertex loss;
- four \(Q_4\) layers form \(Q_6=Q_4\square Q_2\), use 64 slots, and are necessary and sufficient for preserving one clean layer after any three layer-local faults.

Thus \(Q_6\) is **not** minimal for two-vertex tolerance, but it is minimal in the exact-schedule four-layer model for arbitrary triple layer contamination.

`rtl/w33_q6_triple_fault_router.v` publishes the fail-closed clean-layer selector.

---

## 3423 BONKERS — the flat sector is an \(A_2\) flux crystal

On one oriented filled triangle, scalar flat cochains satisfy

\[
a-b+c=0\pmod3.
\]

The six nonzero weight-two solutions are

\[
(1,1,0),(2,2,0),(1,0,2),(2,0,1),(0,1,1),(0,2,2).
\]

They are precisely the six roots of an \(A_2\) root plane reduced modulo three. They span the full two-dimensional local flat plane.

Because the 240 filled triangles partition the 720 edges, the prequotient flat space has the exact direct-sum form

\[
\boxed{
Z^1(X;\mathbb F_3^5)
\cong
\left(A_2(\mathbb F_3)\otimes\mathbb F_3^5\right)^{\oplus240}
}
\]

with dimension 2400. Quotienting the 220-dimensional switching space leaves dimension 2180.

This upgrades the previous generation theorem: minimum defects are not merely generators; locally they form a root system with an exact addition, reversal, and annihilation law. “Flux crystal” is an algebraic mnemonic, not a material or particle claim.

---

## 3424 BONKERS — a moving folded-cube quotient atlas

The two-error Clebsch quotient uses the repetition kernel

\[
\langle11111_2\rangle.
\]

But the five-bit controller sends its generator through the orbit

\[
11111_2\longrightarrow01111_2,\;10111_2,
\]

of weights

\[
5,4,4.
\]

The corresponding quotient graphs are:

\[
\begin{array}{c|c|c}
\text{kernel weight}&\text{quotient}&\text{error distance}\\\hline
3&K_4\square C_4&3\\
4&K_{4,4}\square K_2&4\\
5&\text{Clebsch graph}&5
\end{array}
\]

The only nonzero line fixed by both controller generators is

\[
\langle00111_2\rangle,
\]

which has distance three. Therefore:

\[
\boxed{
\text{fixed controller equivariance and uniform two-bit folded-cube recovery cannot coexist in one 1D quotient.}
}
\]

The exact alternatives are:

1. recompute/re-encode the Clebsch syndrome after every controller step;
2. transport a moving three-chart quotient bundle;
3. use the 12- or 13-bit self-protecting code instead.

---

# 3425–3427 — deep Clebsch atlas

## A. It is the coset graph of the repetition code

The old four-bit tag is

\[
t(x)=x_{3:0}\oplus x_4(1111)_2.
\]

This is a parity-check syndrome for the binary repetition code

\[
\operatorname{Rep}(5)=[5,1,5],
\qquad
\ker t=\{00000,11111\}.
\]

Therefore the 16 checksum symbols are exactly the 16 cosets of \(\operatorname{Rep}(5)\), and the checksum network is its coset graph:

\[
Q_5/\operatorname{Rep}(5)=\boxed{\text{Clebsch}}.
\]

The minimum four trusted bits from the previous packet are consequently not an accidental graph coloring. They are the complete syndrome space of a perfect-radius-two repetition-code quotient.

## B. The decoder shell is \(1+5+10\), with a Petersen residual

Choose the representative of each antipodal coset having weight at most two. The 16 symbols split canonically as

\[
\boxed{1+5+10}.
\]

They are:

- one zero-error syndrome;
- five single-bit syndromes;
- ten double-bit syndromes.

For every center:

- its five neighbors are independent;
- the ten distance-two symbols induce a Petersen graph;
- under the error-position labeling, that Petersen graph is
  \[
  KG(5,2),
  \]
  where two double-error syndromes are adjacent exactly when their two error-position sets are disjoint.

Thus every local decoder chart has the exact shape

\[
\boxed{\text{center}\;\sqcup\;\text{five isolated one-errors}\;\sqcup\;\text{Petersen double-error shell}.}
\]

## C. Closed neighborhoods form a biplane

The Clebsch graph has exactly 16 maximum independent sets of size five, and every one is the open neighborhood of a vertex.

Adding the center to each neighborhood gives 16 six-element blocks. Every pair of checksum symbols belongs to exactly two blocks, so these blocks form a symmetric biplane

\[
\boxed{2-(16,6,2)}.
\]

If \(B=A_{\rm Clebsch}+I\) is its incidence matrix, then

\[
\boxed{BB^{\mathsf T}=4I+2J}.
\]

This is an exact design-theoretic checksum surface: every pair of syndrome symbols has exactly two common closed-neighborhood witnesses.

## D. The full symmetry is the \(D_5\) Weyl action

Exact automorphism enumeration gives

\[
|\operatorname{Aut}(\mathrm{Clebsch})|=\boxed{1920}=2^4\cdot5!.
\]

Using even-weight five-bit sign vectors, the 16 vertices are the weights of one half-spin orbit of type \(D_5\):

- Hamming distance two gives inner product \(+1/4\) and the 5-demicube graph;
- Hamming distance four gives inner product \(-3/4\) and the Clebsch graph.

Thus

\[
\boxed{\overline{\mathrm{Clebsch}}=\text{the 5-demicube/halved-5-cube skeleton}}
\]

and the Clebsch edges select the opposition relation among the 16 half-spin weights.

The controller’s valid/guard coloring reduces the 1920 symmetries to an eight-element elementary Abelian subgroup

\[
\boxed{C_2^3}.
\]

This is an exact colored-graph stabilizer, not a physical \(\mathrm{Spin}(10)\) identification.

## E. Segre/del-Pezzo line geometry

External algebraic geometry supplies another established realization: the Clebsch/projective-cube graph is the intersection graph of the 16 lines on a degree-four del Pezzo, or Segre quartic, surface. Removing one line and the five lines incident with it leaves the Petersen configuration on the ten skew lines—exactly the decoder residue found above.

This gives a clean dictionary:

\[
\begin{array}{c|c}
\text{checksum language}&\text{Segre surface language}\\\hline
\text{one syndrome symbol}&\text{one line}\\
\text{five one-error neighbors}&\text{five intersecting lines}\\
\text{ten double-error residues}&\text{ten remaining lines, Petersen incidence}
\end{array}
\]

The repository uses this only as a verified combinatorial/algebraic-geometric correspondence. It does not infer a physical surface, compactification, or particle multiplet.

## F. Additional exact Clebsch census

The packet also proves:

- strongly regular parameters \((16,5,0,2)\);
- spectrum \(5^1,1^{10},(-3)^5\);
- diameter two;
- 192 induced five-cycles;
- Cayley presentation over \(\mathbb F_2^4\) with generators
  \[
  \{1,2,4,8,15\},\qquad1\oplus2\oplus4\oplus8\oplus15=0;
  \]
- ten controller-invariant binary subspaces in the complete five-bit subspace lattice;
- six valid–valid antipodal axes and ten valid–guard axes.

---

## Published implementation surface

This packet contains:

- `analysis/bt3388_3399_engine.py` — finite reconstruction engine;
- `analysis/bt3388_3399_clebsch_d5_fault_closure.py` — deterministic verifier;
- frozen exact result, code, and dynamic-route manifests;
- `rtl/w33_envelope_self_protecting_code.v`;
- `rtl/w33_q5_dynamic_spare_router.v`;
- `rtl/w33_q6_triple_fault_router.v`;
- exhaustive RTL testbench;
- focused pytest;
- Icarus/Yosys/nextpnr and three-manuscript evidence workflow;
- one shared theorem insert for all canonical papers and the public index.

## Evidence boundary

This release does **not** assert:

- a ten-colour model or checked ten-colour UNSAT proof;
- an exact rational certificate for the magnetic eigenvalues;
- recovery of destroyed uncheckpointed state data from the six-spare remapping theorem;
- measured stochastic fault rates;
- observed FPGA area, placement, or timing before CI completes;
- successful fresh canonical PDFs before CI completes;
- physical \(D_5\), \(\mathrm{Spin}(10)\), del-Pezzo, quantum-group, particle, or spacetime identification;
- laboratory operation or fault-tolerant quantum memory.

## External references used only for established context

1. Simon Schmidt, “Quantum automorphisms of folded cube graphs,” *Annales de l’Institut Fourier* 70 (2020), 949–970, DOI 10.5802/aif.3328.
2. Reza Naserasr et al., “Signed Projective Cubes, a Homomorphism Point of View,” *Journal of Graph Theory* (2026), DOI 10.1002/jgt.70046.
3. Cameron Darwin, “A quadratically enriched count of lines on a degree 4 del Pezzo surface,” arXiv:2205.04456.
4. B. Kunyavskij, A. Skorobogatov, M. Tsfasman, “Del Pezzo surfaces of degree four,” *Mémoires de la SMF* 37 (1989), 1–113.
