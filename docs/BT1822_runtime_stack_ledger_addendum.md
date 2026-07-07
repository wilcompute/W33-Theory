# BT1822 — Runtime Stack Paper/Ledger Addendum

## Machine-paper insertion block

The defect-control stack is now a compiled runtime object. The exact chain is:

\[
TD(4,3)\to 3\text{-slot edge scheduler}\to \lceil L/3\rceil\text{ fixed-edge run law}\to 9\text{-point cache churn law}\to aperture readout skeleton.
\]

The stack separates exact architecture from physical claims:

- BT1818 gives the compiled selector used by the packet-kernel path.
- BT1819 records the seeded-vs-compiled replay contract; full host replay remains a run target.
- BT1820 gives the aperture-to-magic shot estimator; it is a readout plan, not a measured experiment.
- BT1821 gives a locality metric derived from exact churn profiles; it is not a latency benchmark.

## Ledger rows to add

| Claim | Tier | Witness | Output | Pass condition | Boundary |
|---|---:|---|---|---|---|
| Compiled packet-kernel controller | E | `analysis/bt1818_compiled_packet_kernel_controller.py` | `data/PART_BT1818_COMPILED_PACKET_KERNEL_CONTROLLER_summary.json` | 480 directed edges, 3 phase rows per edge, 1440 compiled rows | Selector integration, not full CI. |
| Seeded-vs-compiled packet replay contract | E/S | `analysis/bt1819_packet_trace_replay_compiled_vs_seeded.py` | `data/PART_BT1819_PACKET_TRACE_REPLAY_COMPILED_VS_SEEDED_results.json` | semantic path unchanged; expected zero mismatches | Replay contract; not executed in this connector pass. |
| Aperture-to-magic estimator | P | `analysis/bt1820_aperture_magic_estimator.py` | `data/PART_BT1820_APERTURE_MAGIC_ESTIMATOR_results.json` | 1440 apertures and CF target 1/10 | Future physical readout estimator. |
| Cache locality score | E/S | `analysis/bt1821_cache_locality_score.py` | `data/PART_BT1821_CACHE_LOCALITY_SCORE_results.json` | edge score exceeds nonedge score with same 9-point churn | Derived metric, not measured latency. |

## Firewall language

Only exact finite-incidence/runtime statements are labelled exact. Shot-level magic claims remain pending until physical data exist. Locality scores are derived accounting, not hardware timing.
