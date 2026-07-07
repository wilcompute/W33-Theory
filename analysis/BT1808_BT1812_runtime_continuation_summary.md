# BT1808–BT1812 Runtime Continuation Summary

## BT1808 — TD(4,3) Balanced Edge Scheduler

BT1807 proved that every defect center has nine phase rows and each row exposes four cheap exits. BT1808 compiles this into a deterministic scheduler:

\[
40\cdot9\cdot4=1440=3\cdot480.
\]

Every directed W33 edge appears exactly three times, once in each scheduler slot.

## BT1809 — Page-Loader TD(4,3) Fusion

The safe-zone overlap law is constant:

\[
|\mathrm{Safe}(p)\cap\mathrm{Safe}(q)|=18
\]

for every ordered relocation \(p\to q\). The nine-point page bill is therefore universal, but the phase-block structure distinguishes moves:

- edge move: \(\{0:3,3:6\}\), meaning six phase triples survive whole and three rebuild whole;
- nonedge move: \(\{2:9\}\), meaning every phase triple keeps two points and rebuilds one.

Thus edge moves win on rays and preserve phase blocks.

## BT1810 — Hesse/Wigner TD(4,3) Coupling

Each defect fiber is exactly the nine-point Hesse/Wigner phase plane:

\[
TD(4,3)\cong AG(2,3).
\]

The four defect star-lines are the four striations, and every cheap quad selects one line from each striation. Safe triad and cheap quad are the two readings of the same phase point.

## BT1811 — Physical Interrupt Datasheet

The hardware-facing interrupt sheet now has fixed pins:

| Quantity | Value |
|---|---:|
| centers | 40 |
| safe points per center | 27 |
| phase rows per center | 9 |
| cheap exits per row | 4 |
| scheduler rows | 1440 |
| directed-edge exposure | 3 |
| relocation page bill | 9 |

## BT1812 — Sixth Ring Claim Firewall

BT1812 separates exact runtime/substrate results from physics-facing claims. The public rule is:

> Only executable or arithmetic claims may be stated as exact. External-physics links require comparison, speculation, or research-note language.

This protects the Holonet architecture while keeping the Sixth Ring useful as a research frontier.

## Net new architecture law

The defect is not merely movable. It is now a compiled object:

\[
\boxed{
\text{defect center}
\to TD(4,3)\text{ phase fiber}
\to 3\text{-slot directed-edge scheduler}
\to 9\text{-point page rekey law}
}
\]

Honest scope: BT1808--BT1811 are exact finite-incidence/runtime-interface claims. BT1812 is a tiering/firewall artifact, not a physics derivation.
