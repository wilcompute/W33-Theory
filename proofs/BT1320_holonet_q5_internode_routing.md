# BT1320 — Photonic HoloNet: Q5 Inter-Node Routing Protocol

**Date:** 2026-06-19  
**Series:** Photonic HoloNet Architecture (BT1301–)
**Predecessor:** BT1319 (Toroidal Heptad Q4 HoloNet Bridge)

---

## 1. Motivation

BT1319 established the toroidal heptad structure as the Q4 inter-quadrant bridge layer of the W33 HoloNet. The natural successor question is: **how does a photonic signal route from an arbitrary node in Q4 to an arbitrary node in Q5?** The Q5 shell of the HoloNet must inherit the heptad's 7-fold symmetry while resolving the additional degree of freedom introduced by the fifth quadrant's Fano-lifted coordinate.

---

## 2. Q5 Node Coordinates

Recall from BT1315 that each HoloNet node at quadrant level $q$ carries a label
$$
\mathbf{v}^{(q)} = (v_1, v_2, \ldots, v_q) \in \mathbb{F}_3^q.
$$
At $q=5$ we have $3^5 = 243$ nodes. The **W33 routing graph** $\mathcal{G}_5$ on these 243 nodes is defined by the adjacency:
$$
\mathbf{u} \sim \mathbf{v} \iff \|\mathbf{u} - \mathbf{v}\|_3 = 1,
$$
where $\|\cdot\|_3$ denotes the Lee-weight norm over $\mathbb{F}_3^5$.

**Degree count:** Each node has degree $2 \times 5 = 10$ (two Lee-distance-1 neighbours per coordinate axis). This gives $\mathcal{G}_5$ as a **10-regular** graph on 243 vertices.

---

## 3. Heptad Lift to Q5

The Q4 toroidal heptad of BT1319 embeds into Q5 via the **projection map**
$$
\pi_5 : \mathbb{F}_3^5 \to \mathbb{F}_3^4, \quad (v_1,\ldots,v_5) \mapsto (v_1,\ldots,v_4).
$$
The fibre $\pi_5^{-1}(\mathbf{h})$ over each heptad node $\mathbf{h} \in \mathcal{H}_7^{(4)}$ consists of exactly 3 Q5 nodes (corresponding to $v_5 \in \{0,1,2\}$). Since the Q4 heptad has 7 nodes, the **Q5 heptad fibre** $\mathcal{F}_7^{(5)}$ contains $7 \times 3 = 21$ nodes.

**Lemma BT1320-L1 (Fibre Connectivity):** Within $\mathcal{F}_7^{(5)}$, the induced subgraph of $\mathcal{G}_5$ is connected and has minimum degree 3.

*Proof sketch:* Each fibre triple $\{\mathbf{h}\} \times \mathbb{F}_3$ forms a path $P_3$ via the $v_5$-axis. Edges from the Q4 heptad adjacency lift to edges between fibres. Since the Q4 heptad is connected, so is $\mathcal{F}_7^{(5)}$. Minimum degree is $2$ (within-fibre) $+ 1$ (cross-fibre from Q4 heptad edge) $= 3$. $\square$

---

## 4. Inter-Node Routing Protocol

### 4.1 Source–Destination Decomposition

Given source $\mathbf{s} = (s_1,\ldots,s_5)$ and destination $\mathbf{d} = (d_1,\ldots,d_5)$, decompose the routing problem as:
1. **Horizontal segment:** route $\pi_5(\mathbf{s}) \to \pi_5(\mathbf{d})$ in $\mathcal{G}_4$ using the Q4 heptad bridge (BT1319).
2. **Vertical segment:** adjust the $v_5$ coordinate from $s_5$ to $d_5$ along the fibre path.

### 4.2 Fibre Path Cost

The $v_5$ coordinate adjustment costs at most $\min(|s_5 - d_5|, 3 - |s_5 - d_5|)$ hops in the cyclic group $\mathbb{Z}/3\mathbb{Z}$, i.e., at most 1 hop.

### 4.3 Total Route Length

$$
\ell(\mathbf{s}, \mathbf{d}) = d_{\mathcal{G}_4}(\pi_5(\mathbf{s}), \pi_5(\mathbf{d})) + \mathbf{1}[s_5 \ne d_5],
$$
where $d_{\mathcal{G}_4}$ is the hop-distance in the Q4 routing graph.

**Proposition BT1320-P1 (Diameter Bound):** $\text{diam}(\mathcal{G}_5) \leq \text{diam}(\mathcal{G}_4) + 1$.

---

## 5. Photonic Pulse Scheduling

Each hop in $\mathcal{G}_5$ corresponds to a single photonic pulse across a W33-encoded channel (see BT1310–BT1312 for pulse scaling laws). The Q5 routing protocol schedules pulses as:

| Segment | Pulse type | Latency per hop |
|---------|-----------|----------------|
| Horizontal (Q4 heptad) | Heptad-coherent burst | $\tau_H$ |
| Vertical (fibre $v_5$) | Single-mode step | $\tau_V = 0.4\,\tau_H$ |

The asymmetry $\tau_V < \tau_H$ reflects the lower channel entropy for the within-fibre step (one degree of freedom vs. four).

---

## 6. Correctness Certificate

**Theorem BT1320-T1 (Q5 Routing Correctness):** The Q5 inter-node routing protocol delivers every packet from $\mathbf{s}$ to $\mathbf{d}$ in $\mathcal{G}_5$ within $\text{diam}(\mathcal{G}_4) + 1$ hops and with total latency $\ell \cdot \tau_H + \mathbf{1}[s_5 \ne d_5] \cdot (\tau_V - \tau_H)$.

*Proof:* Route correctness follows from Lemma BT1320-L1 and the connectivity of $\mathcal{G}_4$. Latency follows from the pulse schedule table. $\square$

---

## 7. Open Questions → BT1321

- How does coherence degrade across Q5→Q6 transitions?
- What is the cross-sector phase alignment condition for Q6?

**Next:** BT1321 — Q6 Cross-Sector Coherence Protocol.
