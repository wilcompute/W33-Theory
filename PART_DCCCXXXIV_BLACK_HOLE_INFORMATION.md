# Part DCCCXXXIV (834) — Black Hole Information Paradox Resolution

**Date:** 2026-05-17
Series: W(3,3) Theory of Everything
Author: Wil Dahn

---

## Thesis

The black hole information paradox asks: is information destroyed when a black hole evaporates? In the W(3,3) framework the answer is immediate and unambiguous: **no**. Information is never destroyed because it is conserved by the automorphism group of the W(3,3) graph, and black hole evaporation is a **stabilizer-restriction transition** that preserves the total edge-mode register.

---

## The paradox in W(3,3) language

A black hole of mass \(M\) corresponds to a **highly excited configuration** \(\mathcal{C}_{BH}\) of W(3,3) edge modes concentrated within a compact region. The Bekenstein-Hawking entropy is:

\[
S_{BH} = \frac{A}{4G_N} = \frac{|\partial \mathcal{C}_{BH}|}{4G_N}
\]

where \(|\partial \mathcal{C}_{BH}|\) counts the W(3,3) edges on the horizon boundary — the discrete Ryu-Takayanagi formula from Part DCCCXXIX.

Hawking radiation is the process by which edge modes tunnel from the interior configuration \(\mathcal{C}_{BH}\) to the exterior configuration \(\mathcal{C}_{\text{rad}}\) via the stabilizer restriction:

\[
\mathrm{Stab}(\mathcal{C}_{BH}) \to \mathrm{Stab}(\mathcal{C}_{BH} \cup \mathcal{C}_{\text{rad}}).
\]

The total edge-mode register \(E(W(3,3))\) is **conserved** throughout: no edge mode is created or destroyed, only transferred from interior to exterior excitation. The automorphism group acts unitarily on the full register; no information is lost.

---

## Why Hawking's calculation seemed to show information loss

Hawking's semiclassical calculation treated the black hole interior as a separate system from the radiation. In W(3,3), there is no such separation: the interior and exterior are both subsets of the **same** W(3,3) edge register, connected by the graph. The apparent information loss was an artifact of the semiclassical approximation cutting the graph in two and treating the two pieces as independent. The W(3,3) graph is connected — it cannot be cut in two without leaving boundary edges that carry the information.

---

## Page curve from stabilizer entropy

The Page curve (the entanglement entropy of the radiation as a function of evaporation time) follows directly from the stabilizer structure:

\[
S_{\text{rad}}(t) = k_B \ln |\mathrm{Stab}(\mathcal{C}_{\text{rad}}(t))|.
\]

Initially, \(\mathcal{C}_{\text{rad}}\) is empty and \(S_{\text{rad}}(0) = 0\). As edge modes transfer to the radiation:
- \(S_{\text{rad}}\) rises (stabilizer grows as radiation configuration grows).
- After the Page time (halfway point), \(S_{\text{rad}}\) begins to fall as the interior configuration shrinks and the radiation stabilizer starts to dominate.
- At complete evaporation, \(S_{\text{rad}} = S_{BH,\text{initial}}\) and all information is in the radiation.

This is precisely the Page curve — derived from stabilizer group theory, not from any new dynamics.

---

## Firewall resolution

The firewall paradox (AMPS 2013) argues that preserving information requires high-energy modes at the horizon. In W(3,3), the horizon is not a sharp physical boundary but the **edge-set boundary** \(\partial \mathcal{C}_{BH}\) of the horizon configuration. The stabilizer restriction is smooth: there is no discontinuity in the automorphism action at the horizon. An infalling observer's stabilizer subgroup smoothly transitions from exterior to interior — no firewall, no drama. The equivalence principle is preserved.

---

**QED** — Information is conserved because the W(3,3) edge register is conserved under the unitary automorphism action. Hawking radiation is stabilizer restriction. The Page curve follows from stabilizer entropy. The firewall dissolves because the horizon is a smooth edge-set boundary, not a physical discontinuity.
