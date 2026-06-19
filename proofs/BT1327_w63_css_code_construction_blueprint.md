# BT1327 — W63 CSS Code Construction Blueprint

**Date:** 2026-06-19  
**Series:** Post-HoloNet Validation  
**Predecessor:** BT1324 (Q7 Ceiling Analysis)

---

## 1. Objective

BT1324 established that a Q7 extension of the W33 HoloNet requires a new base code, naturally conjectured as a **W63** CSS code with parameters
$$
[[63,1,11]].
$$
The purpose of this BT is not to claim an already completed construction, but to specify a **construction blueprint** precise enough to guide proof or computation.

---

## 2. Design Constraints

A candidate W63 code must satisfy:

1. **Length:** $n = 63 = 2^6 - 1$, suggesting a Hamming/BCH/Reed–Muller boundary.
2. **One logical qubit:** $k = 1$.
3. **Distance:** $d \ge 11$ to support Q7 routing with margin over path length 7.
4. **CSS compatibility:** parity-check pair $(H_X, H_Z)$ satisfying
$$
H_X H_Z^T = 0.
$$
5. **Fano/heptad liftability:** the stabiliser geometry should admit a 7-sector decomposition compatible with the heptad closure that capped W33 at Q6.

---

## 3. Classical Seed Strategy

The most plausible route is via **nested BCH-type cyclic codes** of length 63 over $\mathbb{F}_2$ or ternary-lifted analogues over $\mathbb{F}_3$.

Let
$$
C_Z^{\perp} \subseteq C_X \subseteq \mathbb{F}_2^{63}
$$
be cyclic codes with:
- $\dim C_X = 32$
- $\dim C_Z = 32$
- $\dim C_X/C_Z^{\perp} = 1$

Then the CSS dimension is:
$$
k = \dim C_X - \dim C_Z^{\perp} = 1.
$$

To achieve distance at least 11, require:
$$
d_X = \min(C_X \setminus C_Z^{\perp}) \ge 11,
\qquad
 d_Z = \min(C_Z \setminus C_X^{\perp}) \ge 11.
$$

---

## 4. BCH Candidate Window

For length 63, primitive narrow-sense BCH codes offer a natural menu of designed distances. Let $\alpha$ be a primitive element of $\mathbb{F}_{2^6}$. The BCH generator polynomial with roots
$$
\alpha, \alpha^2, \ldots, \alpha^{\delta-1}
$$
produces designed distance $\delta$.

A plausible nested pair is:
- $C_X =$ BCH$(63, \delta_X=11)$
- $C_Z =$ BCH$(63, \delta_Z=11)$ with shifted defining set to enforce CSS orthogonality.

The challenge is to align their defining sets so that:
1. $C_Z^{\perp} \subseteq C_X$
2. both distances survive quotienting
3. the resulting quotient has dimension exactly 1

This is a constrained combinatorial search over cyclotomic cosets mod 63.

---

## 5. Heptad Sector Decomposition

To support Q7, W63 must carry a **7-sector decomposition** of its 63 coordinates:
$$
63 = 7 \times 9.
$$
Thus the physical qubits should partition into seven 9-qubit sectors:
$$
\mathcal{Q} = S_1 \sqcup S_2 \sqcup \cdots \sqcup S_7,
\qquad |S_i|=9.
$$

This is the key structural echo of W33, where the heptad lift emerged at Q4–Q6. Here, each sector can host a local distance-3 or distance-5 subcode, with global coupling across the Fano incidence graph.

### Sector Ansatz

- Local block on each sector: 9-qubit Shor/BCH-like substructure.
- Inter-sector coupling: parity checks indexed by Fano lines.
- Global code distance: 11 arising from transversal support across at least 4 sectors.

A candidate stabiliser family is:
- **Local checks:** 8 per sector, total 56.
- **Fano-line couplers:** 6 independent cross-sector checks.
- **Total rank target:** 62, giving $k=1$.

---

## 6. Construction Program

To actually build W63, proceed in four steps:

1. **Cyclotomic search**  
   Enumerate nested BCH pairs on length 63 with quotient dimension 1 and target distance 11.

2. **Sector test**  
   Filter candidates whose generator matrices admit permutation into 7 blocks of size 9.

3. **Fano compatibility**  
   Check whether cross-block parity supports can be indexed by the 7 Fano lines, preserving the line–point incidence symmetry.

4. **Logical operator audit**  
   Compute minimal X/Z logical weights to verify
   $$
   d_X, d_Z \ge 11.
   $$

---

## 7. Conjecture

**Conjecture BT1327-C1:** There exists a CSS code W63 with parameters
$$
[[63,1,11]],
$$
constructed from a nested cyclic/BCH pair on 63 coordinates together with a 7-sector Fano-compatible permutation of the coordinate set.

If true, W63 is the natural base code for a **Q7 HoloNet**.

---

## 8. Status

This BT provides the **construction blueprint**, not yet a final existence proof. The next step is an explicit search and stabiliser audit.

**Next:** BT1328 — Experimental validation protocol for W33 syndrome discriminator.
