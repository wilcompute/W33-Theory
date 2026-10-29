# October 29, 2026 — five-front independent continuation: optimized checks, fault propagation, q7 SAT, intrinsic address geometry, chirality, robust photon counting

**Scope and provenance.** Existing repository facts include the binary W(3,3) point-adjacency CSS code \([[40,8,6]]_2\), the exact adjacency-code weight histogram, the \([[400,48,d]]_2\) q7 interval \(10\le d\le14\), the 40-point W33/dual four-port three-photon event probabilities, and the algebraic H27 address group. The findings below are newly computed consequences, optimizations, controls and open tests **using those established ingredients**, not discoveries of quantum mechanics, a TOE, physical Standard-Model particles or fundamental constants.

## 1. EXACT globally optimal CSS measurement workload: 132 couplings and degree 4

Script: \`analysis/w33_20261029_minimum_132_check_basis.py\`.

The 40-bit binary adjacency row space \(C=\mathrm{im}_{\mathbb F_2} A\) has rank 16. Full enumeration of its \(2^{16}=65{,}536\) words reproduces the existing weight enumerator: **45 weight-eight octads**, 1,120 weight-twelve dodecads, and no nonzero word of smaller weight. The **45 weight-eight words span rank 15**, not rank 16; this is also structurally compatible with the known \([40,15,8]\) sentinel subcode, but the codes must not be conflated.

Consequently any 16-independent-generator basis must include at most 15 weight-eight rows and one row of weight at least 12, so the total number of data–ancilla couplings in a simple one-gate-per-support-site measurement is **at least \(15\cdot8+12=132\)**. The committed explicit basis contains exactly fifteen weight-eight checks and one weight-twelve check and has rank 16: **the bound is attained**.

Even more, count the incidence of each physical qubit among these sixteen checks: the committed basis has maximum incidence **4**, which is globally optimal because \(\lceil132/40\rceil=4\). Thus **both the minimal total coupling count and minimal possible maximum per-qubit check incidence are attained simultaneously** (per X or Z stabilizer type). The simple baseline of sixteen independent 12-weight adjacency rows has 192 couplings, so this reduces raw coupling count by **31.25%**. In the full CSS check set, multiply these nominal data couplings by two for the X and Z sectors: 264 vs 384; this is not a full physical-depth or noisy-hardware cost estimate.

## 2. A reproducible one-fault hook counterexample, not a fabricated fault-tolerant threshold

The same producer enumerates all 821 binary syndromes associated with weight-0/1/2 pure-Pauli errors. For **every** one of the sixteen new check supports, consider naive measurement of a Z-stabilizer via data(control)→ancilla(target) CNOTs. A single Z fault on the ancilla just before the final three data CNOTs propagates onto the last three data qubits. The resulting weight-three error has a syndrome **different from all 821 weight-0/1/2 patterns**. (If it shared one, their product would be a nonzero weight-at-most-five word of \(\ker A\), contradicting the known minimum kernel distance six.)

The script prints an exact bit-mask witness. A bare one-ancilla measurement is therefore *not* a fault-tolerant two-error-correcting extraction circuit. This diagnostic does not say that proper flag/cat verification cannot correct it. **No flagged protocol, leakage-aware extraction, noisy threshold, transversal non-Clifford gate or complete magic-injection cycle is certified in this packet.** Established general techniques: Chamberland et al., *Flag Fault-Tolerant Error Correction for any Stabilizer Code*, PRX Quantum 1, 010302 (2020), https://doi.org/10.1103/PRXQuantum.1.010302 . General CSS transversal diagonal classification: PTEP (2026), https://academic.oup.com/ptep/article/2026/8/083A03/8729099 .

## 3. q7 rigorous rank 176 reduction — stronger formulation, still no distance proof

Script: \`analysis/w33_20261029_q7_rank176_xor_sat.py\`.

The 400-by-400 W(3,7) binary symplectic adjacency matrix has **rank 176**, not rank 48; the number 48 counts \(\dim\ker A/\mathrm{im}A=400-2\cdot176\) *logical qubits*. The new parity solver applies the **176 independent original adjacency checks** instead of all 400 redundant checks, maintains 400 Boolean support variables, fixes a two-point support representative for both pair orbits, and searches all even kernel weights from 10 through 12 using native OR-Tools XOR constraints.

On the user's authorized Windows computer, with OR-Tools, 8 workers and 50 seconds each:
- Adjacent orbit, pair \((0,8)\): **UNKNOWN**, 247,469 branches and 25,628 conflicts, approximately 50.44 seconds.
- Nonadjacent orbit, pair \((0,1)\): **UNKNOWN**, 337,797 branches and 29,818 conflicts, approximately 50.07 seconds.

These statuses are **inconclusive**. The previously certified \(10\le d\le14\) interval remains; any claim of exact q7 distance 14 would be unjustified. The antecedent two-orbit reduction uses the point-transitive symplectic geometry; it is valid for supports of size \(\ge2\). A stronger proof would need either SAT UNSAT certificates for both cases or a structural theorem. Published LDPC work on classical GQ incidence codes uses different check spaces and, in some results, \(p\)-ary characteristic \(p\) checks; do **not** apply such theorems automatically to these binary **adjacency** equations: J.-L. Kim, K. Mellinger, L. Storme, *Small weight codewords in LDPC codes defined by (dual) classical generalized quadrangles*, Designs Codes Cryptogr. 42 (2007), https://doi.org/10.1007/s10623-006-9017-6 .

## 4. Intrinsic address-derived bounded-degree continuum control, but sub-Riemannian

Script: \`analysis/w33_20261029_heisenberg_intrinsic_growth_chirality.py\`.

Define integral Heisenberg \(H(\mathbb Z)\) by \((a,b,c)(x,y,z)=(a+x,b+y,c+z+ay)\), with the intrinsic four local generators \(X^{\pm1},Y^{\pm1}\). Finite reduction modulo 3 is **H27**, with Cayley ball volumes **1,5,13,25,27**, diameter **four**. Its extension modulo primes \(p\) supplies a mathematically natural bounded-degree *family*, rather than manually attaching an external cubic lattice. The exact BFS ball volumes of the integral group for radii \(0,\ldots,15\) are
\[
[1,5,17,53,135,299,593,1069,1793,2845,4309,6281,8871,12195,16381,21569].
\]
These are checked to match the finite \(H_{211}\) Cayley graph through radius 15. The volume doubling \(|B_{14}|/|B_7|=16381/1069\approx15.3237\), approaching the characteristic factor \(2^4=16\).

The *established* Bass–Guivarc'h theorem predicts growth degree \(1\cdot2+2\cdot1=\mathbf4\), because \(H/[H,H]\cong\mathbb Z^2\) and \([H,H]\cong\mathbb Z\). **The new result is the explicit H27-address-level finite validation**, not the previously published group-growth theorem. See Breuillard, *Geometry of locally compact groups of polynomial growth and shape of large balls*, https://www.cmls.polytechnique.fr/perso/breuilla/PolGrowth24.pdf , and standard Bass–Guivarc'h literature. Crucial physical boundary: this describes anisotropic sub-Riemannian geometry; **growth dimension four is not a derivation of 3+1 Lorentzian spacetime**, and the prime family changes the finite field/carrier from the physical q=3 candidate.

## 5. Chirality-vacuum selector firewall from the same H27 group

The H27 *regular representation* is 27-dimensional. Fourier decomposition along the center gives three nine-dimensional subspaces; these must not be confused with nine copies of a 3D Schrödinger irrep in other project representations.

For Hermitian real nearest-neighbor \(H=X+X^{-1}+Y+Y^{-1}\), the center-character \(k=1,2\) magnetic Hamiltonian blocks are exactly complex conjugates. The independent 9-by-9 eigensolvers confirm the spectra agree to \(8.9\times10^{-16}\). Thus a real K-invariant graph hopping operator **does not select one orientation**.

Adding an explicit Hermitian K-odd central hopping \(i(Z-Z^{-1})\) shifts the conjugate \(k=1,2\) sector energies by **opposite** amounts \(\mp\sqrt3\) for unit coefficient. This demonstrates how chirality can be *inserted* algebraically, not why the cosmos should choose one sign. A spontaneous dynamical chiral ground-state selection, with a sign fixed by an independently derived microscopic action, remains unsolved.

## 6. Photon overlap-agnostic fixed-port test: the old 20,333 is optimal for a *different*, harder objective

Script: \`analysis/w33_20261029_optical_overlap_agnostic_minimax.py\`.

Prior fixed-output four-port aggregate probabilities for a common pure-state *real* pairwise photon overlap \(s\in[0,1]\) are
\[
p_W(s)=(17496+52488s^2+34992s^3)/15^6,\quad
p_D(s)=(3376+1328s^2-2048s^3)/15^6.
\]
The previous pass correctly lowered the minimum **at known \(s=0\)** from \(20,333\) trials to **\(19,427\), cutoff 15**. Now require **one fixed test for every possible, uncalibrated \(s\)**. \(p_W(s)\) has its minimum at zero; \(p_D(s)\) has its **maximum at \(s=83/192\)**. Their respective worst-case probabilities are \(0.001536\) and \(0.0003036465350810344\).

A complete integer search over binomial threshold rules finds the global robust optimum **\(N=20,333\), cutoff 16**, under false-positive *and* false-negative tolerances each strictly below \(10^{-3}\). Thus the old 20,333 figure, although **wrongly called optimal for known \(s=0\)**, turns out **exactly optimal for the harder unknown-overlap test**. With independently unknown per-photon \(\eta\in[0.85,1]\), no failed-threefold false event (\(\beta=0\)), and conservative independent worst-case efficiencies for W and dual, the minimax requirement rises to **\(N=54,144\), cutoff 31**.

These are ideal independent-trial statistics under **uniform real** overlap; complex Gram phases, nonuniform overlaps, device-specific mode loss, drift, correlated photon noise and uncalibrated dark counts are **not** covered. The device should never be described as distinguishing W33 in the presence of arbitrary unmodeled imperfections.

## QA / custody

- The three new producers for minimal-check optimization/hook faults, intrinsic Heisenberg H27 growth/chiral spectral control, and overlap-agnostic photon minimax were independently run with PASS, then fetched from GitHub and re-executed on the authorized Windows computer with PASS. The maximally balanced check basis was subsequently upgraded to maximum incidence 4 (versus the first maximum 5); the producer is updated accordingly.
- New focused regressions: \`tests/test_w33_20261029_five_front_followthrough.py\` verifies 132/4, 16 hook witnesses, H27 finite and integral growth, conjugate-sector degeneracy, overlap-agnostic shot minima, and rank 176; no 100-second SAT run is included in ordinary unit tests.
- The shared Windows \`master\` checkout carries uncommitted work from parallel sessions. At a previous check, it held 17 tracked modifications and a transient \`.git/index.lock\`; a clean detached worktree or scoped fast-forward must never overwrite these. The GitHub-master publications were made using the connected GitHub app; we do not represent the shared main checkout as synchronized unless a subsequent explicit Git status confirms it.
- No experimental or fundamental-physics claims exceed the scope of exact finite mathematics, probability models or established group-theoretic growth.
 
## Five independent frontiers after this pass

1. Prove or falsify d=14 by a *genuinely different* q7 geometric argument or native parity UNSAT certificate for all weight-10 and weight-12 supports.
2. Replace naive ancilla checks with actual verified-cat or flag extraction and simulate all one/two faults, including preparation, measurement, leakage and feedback; evaluate a fully specified magic-injection protocol.
3. Find an internal K-odd *dynamical* order parameter with a bounded-below microscopic Hamiltonian where chiral sector selection occurs without putting a \(K\)-odd term in by hand.
4. Test a genuinely intrinsic *causal* finite geometry tower: anisotropic H27 address growth is an instructive non-Riemannian foil, not a 3+1 spacetime derivation.
5. Prove statistical robustness of the optical discriminator against **general complex three-photon Gram matrices**, adversarial mode-dependent loss and phase-calibration uncertainty; identify a reproducible experimental regime.
