# Odd-\(q\) adjacency CSS: transversal Clifford and uniform-\(T\) obstruction

**Scope.** New gate-level deduction from existing binary adjacency/CSS certificates; not a new weight enumerator, new distance computation, proof of physical fault tolerance, or proof of a theory of everything.

**Prior art checked.** Pass85 had already computed the \( [40,16,8]\) adjacency code weight enumerator. The October 29 adjacency CSS packet \`analysis/2026-10-29_w33_adjacency_css40_hexads.md\` already certified \([[40,8,6]]_2\) and its 240 weight-six logicals. \`analysis/w33_pass204_transversal_clifford.py\` concerns a different **sentinel** \([[40,10,4]]\) code. This note concerns the *adjacency CSS* gate action, including an all-odd-\(q\) no-go.

Let \(A\) be the binary adjacency matrix of the point graph of any generalized quadrangle \(GQ(q,q)\) of **odd prime-power order \(q\ge3\)**. Put \(C=\operatorname{im}_{\mathbb F_2}A\), \(n=(q+1)(q^2+1)\). Standard SRG parameters are
\[
k=q(q+1),\quad\lambda=q-1,\quad\mu=q+1.
\]
Every adjacency row has weight \(k\). Distinct rows overlap in \(\lambda\) or \(\mu\) coordinates. Since all three integers are even, \(C\subseteq C^\perp\), giving the CSS check pair \(H_X=H_Z=A\).

**Theorem 1 (exact transversal-\(S\) criterion).** The row code \(C\) is doubly even if and only if \(q\equiv3\pmod4\). Indeed \(k\) is divisible by four exactly in that congruence class, and every distinct row intersection is even; the binary identity
\[
\operatorname{wt}(u+v)=\operatorname{wt}(u)+\operatorname{wt}(v)-2|\operatorname{supp}u\cap\operatorname{supp}v|
\]
preserves divisibility by four as generators are added. Conversely a row of weight \(k\equiv2\pmod4\) obstructs doubly evenness when \(q\equiv1\pmod4\).

For \(q\equiv3\pmod4\), \(S^{\otimes n}\) preserves the CSS code: \(S^{\otimes n}X(c)(S^\dagger)^{\otimes n}=i^{\operatorname{wt}(c)}X(c)Z(c)=X(c)Z(c)\) on the stabilizer for each \(c\in C\). Uniform \(H^{\otimes n}\) preserves every self-dual-check CSS pair \(H_X=H_Z\). In particular **\([[40,8,6]]_2\) admits uniform transversal logical Clifford \(H\) and \(S\)**, though it does not follow that these operations generate independent Clifford gates on all eight logical qubits. When \(q\equiv1\pmod4\), uncorrected uniform \(S\) changes stabilizer signs; a compensating physical \(Z\) pattern can be sought separately.

**Theorem 2 (uniform-\(T\) no-go, all odd \(q\)).** For \(T=\operatorname{diag}(1,e^{i\pi/4})\), applying \(T^{\otimes n}\) to the encoded zero state \(\lvert C\rangle=|C|^{-1/2}\sum_{c\in C}\lvert c\rangle\) gives amplitudes \(e^{i\pi\operatorname{wt}(c)/4}\). The intersection of codespace with computational basis support *exactly* \(C\) is one-dimensional, spanned by \(|C\rangle\). Thus \(T^{\otimes n}\) can preserve the CSS codespace only if every codeword has weight divisible by eight.

For \(q\equiv1,3,5\pmod8\), a single adjacency row has nonzero weight modulo eight. For \(q\equiv7\pmod8\), its weight \(k\equiv0\pmod8\), but the sum of two adjacent adjacency rows has weight
\[
2k-2\lambda=2q(q+1)-2(q-1)\equiv4\pmod8.
\]
Therefore **no odd-order \(GQ(q,q)\) adjacency CSS code admits the *uncorrected, uniform* physical gate \(T^{\otimes n}\) as a codespace-preserving logical operation**. This is narrower than a no-go for non-Clifford gates generally: it does not exclude encoded magic-state injection, code switching, nonuniform patterns, adaptive circuits, or other fault-tolerant architectures.

**Independent verification.** \`python analysis/w33_20261029_oddq_css_transversal_gate_obstruction.py\` regenerates the 40 symplectic projective points, all adjacency rows and pair overlaps, the \(16\)-dimensional row basis, and all \(65{,}536\) codewords. It reproduces the existing Pass85 enumerator
\[
1+45t^8+1120t^{12}+15570t^{16}+32064t^{20}
  +15570t^{24}+1120t^{28}+45t^{32}+t^{40}.
\]
The mathematical general-\(q\) argument is exact from the SRG parameters, not an extrapolation from the ten numerical examples. For \(q=7\), the explicit obstruction is a weight-100 sum of adjacent weight-56 generators.

**TOE / experimental boundary.** This is a statement about abstract **40 physical qubits** (and general \(n\)-qubit CSS blocks), not about one photon occupying 40 optical modes. It identifies a clean Clifford/non-Clifford engineering boundary; it does not derive physical qubit hardware, dimensionful couplings, a Lorentzian continuum, or a unique dynamics.
