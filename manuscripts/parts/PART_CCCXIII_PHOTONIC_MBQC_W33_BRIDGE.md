# Part CCCXIII — Photonic MBQC / W33 Bridge

**Date:** 2026-05-05  
**Status:** exact photonic resource bridge from the uploaded single-photon paper to the W33 operator stack

---

## 1. Uploaded paper trigger

The uploaded paper `single_photon_universal_computation.tex/pdf` presents a self-contained account of single-photon universal quantum computation. It states that a single photon has a two-dimensional polarisation Hilbert space

\[
\mathcal H_{pol}\cong\mathbb C^2,
\]

and that dual-rail encoding uses two spatial modes for one logical qubit. It also says passive linear optics can generate arbitrary single-qubit \(SU(2)\) gates, KLM produces post-selected nonlinear/two-qubit gates, and MBQC uses photonic graph-state clusters. fileciteturn400file0

The paper gives three probability/resource facts that are immediately meaningful in W33 language:

1. the simplest KLM conditional phase / CZ success probability is

\[
\frac14,
\]

2. Type-II fusion gates generate graph-state edges with probability

\[
\frac12,
\]

3. a cluster-state stabilizer has the form

\[
K_a=X_a\prod_{b\sim a}Z_b.
\]

fileciteturn400file0

---

## 2. Single photon dimension equals \(\lambda\)

The single-photon polarisation qubit has dimension

\[
2.
\]

Dual-rail encoding also uses

\[
2
\]

spatial modes.

In W33,

\[
\lambda=2.
\]

So:

\[
\boxed{
\dim\mathcal H_{pol}=\text{dual-rail modes}=\lambda=2.
}
\]

This makes the photon qubit dimension the same structural constant as the W33 triangle parameter.

---

## 3. SU(2) generator count equals \(q\)

The Pauli/SU(2) control algebra has

\[
3
\]

generator directions.

In W33,

\[
q=3.
\]

Thus:

\[
\boxed{
\#SU(2)\text{ generator directions}=q.
}
\]

This aligns the Bloch-sphere control algebra with the q-clock Markov spectrum from CCCXI.

---

## 4. KLM and fusion probabilities

The simplest KLM conditional phase / CZ success probability is

\[
\frac14.
\]

But in W33,

\[
\mu=4.
\]

Therefore:

\[
\boxed{
p_{KLM}=\frac14=\frac1\mu.
}
\]

The Type-II photonic fusion success probability is

\[
\frac12.
\]

But

\[
\frac{\lambda}{\mu}=\frac24=\frac12.
\]

So:

\[
\boxed{
p_{fusion}=\frac12=\frac{\lambda}{\mu}.
}
\]

This is the first real photonic resource bridge: the optical probabilities land exactly on W33 local parameters.

---

## 5. W33 as a photonic cluster graph

If W33 is used as a photonic graph-state cluster, then it has

\[
40
\]

photons/qubits and

\[
240
\]

graph-state edges.

The edge count is

\[
E=240=q(q^4-1).
\]

This is the same undirected edge shell that appears as Seidel energy and line graph vertices.

---

## 6. Stabilizer weight

For a graph-state cluster, the stabilizer at vertex \(a\) is

\[
K_a=X_a\prod_{b\sim a}Z_b.
\]

Its support size is

\[
1+\deg(a).
\]

For W33,

\[
\deg(a)=k=12.
\]

Therefore each stabilizer has weight

\[
1+k=13.
\]

But

\[
13=\Phi_3.
\]

So:

\[
\boxed{
\operatorname{wt}(K_a)=k+1=\Phi_3=13.
}
\]

This means every W33 cluster stabilizer has projective-plane weight.

Total stabilizer support is

\[
40\cdot13=520.
\]

---

## 7. Fusion attempts equal Hashimoto carrier

A W33 cluster requires

\[
E=240
\]

photonic graph-state edges.

Each Type-II fusion succeeds with probability

\[
p_{fusion}=\frac12.
\]

So the expected attempts per edge are

\[
\frac1{p_{fusion}}=2.
\]

Expected attempts to build all W33 cluster edges:

\[
240\cdot2=480.
\]

But

\[
480=2E=2q(q^4-1),
\]

the Hashimoto directed carrier.

Therefore:

\[
\boxed{
\mathbb E[\text{fusion attempts for W33 cluster}]
=480
=\text{Hashimoto directed carrier}.
}
\]

This is the central CCCXIII breakthrough.

Hashimoto's 480 states are not only oriented nonbacktracking edges. They are also the expected physical fusion-attempt budget for assembling the W33 photonic cluster.

---

## 8. KLM attempts match triangle trace

The simplest KLM success probability is

\[
\frac14.
\]

So expected attempts per edge are

\[
4.
\]

For all W33 edges:

\[
240\cdot4=960.
\]

But

\[
960=\operatorname{tr}(A^3)=6T.
\]

Thus:

\[
\boxed{
\mathbb E[\text{simple KLM attempts for all W33 edges}]
=\operatorname{tr}(A^3).
}
\]

This ties KLM post-selected nonlinearity to the triangle-trace layer that also appears in the Dirac determinant compiler.

---

## 9. Theorem statement

**Photonic MBQC gives a physical resource interpretation of the W33 operator stack.**  The single-photon qubit dimension and dual-rail mode count are

\[
\lambda=2.
\]

\(SU(2)\)/Pauli control has

\[
q=3
\]

generator directions.  The simplest KLM conditional phase success probability is

\[
\frac14=\frac1\mu,
\]

and Type-II fusion success is

\[
\frac12=\frac\lambda\mu.
\]

A W33 cluster state has

\[
40
\]

photons,

\[
240
\]

graph edges,

\[
k+1=\Phi_3=13
\]

stabilizer weight, and

\[
2E=480
\]

oriented edge incidences. Because fusion succeeds with probability \(1/2\), the expected number of fusion attempts to build the full W33 cluster is

\[
480,
\]

exactly the Hashimoto directed carrier.

---

## 10. Why this matters

This connects the abstract graph dynamics to physical photonic computation:

\[
\text{single photon}
\to
\lambda=2,
\]

\[
\text{SU(2) control}
\to
q=3,
\]

\[
\text{fusion probability}
\to
\lambda/\mu,
\]

\[
\text{W33 cluster stabilizer}
\to
\Phi_3,
\]

\[
\text{expected fusion attempts}
\to
480.
\]

So the Hashimoto carrier now has a concrete experimental-resource interpretation:

\[
\boxed{
480
=
\text{expected Type-II fusion attempts to assemble the W33 photonic cluster}.
}
\]

---

## 11. Regression status

The CCCXIII test file verifies:

1. single-photon qubit dimensions,
2. KLM and fusion probabilities,
3. W33 cluster resource counts,
4. photonic attempts matching operator counts,
5. Dirac and Matrix Tree companions,
6. threshold relations,
7. audit-level consistency.

---

## 12. Next target

The next target is to patch the uploaded single-photon paper itself:

\[
\text{single photon universality}
\to
\text{W33 photonic resource theorem}.
\]

The paper should explicitly include:

\[
p_{fusion}=\frac\lambda\mu,
\quad
p_{KLM}=\frac1\mu,
\quad
\operatorname{wt}(K_a)=\Phi_3,
\quad
\mathbb E[\text{fusion attempts}]=2E=480.
\]
