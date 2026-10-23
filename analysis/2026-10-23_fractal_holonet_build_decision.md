# 2026-10-23 — Fractal Holonet hardware/software build and optical switching decision

## Decision and source scope

The Holonet recursion is **40-ary**: each W33 site carries a child network, with radix-40 leaf addresses. The full `holonet_machine_blueprint.pdf` (268 pages), `photonic_holonet.pdf` (351 pages), `holonet_practical_implications.pdf` (23 pages), `papers/forty_points/main.pdf` (203 pages in the inspected snapshot), and `docs/holonet_machine_blueprint.pdf` (38 pages) were scanned page-by-page for the fractal, routing, quantum, detector and hardware claims. Per-file SHA-256 hashes and term/page evidence are in `analysis/2026_10_23_fractal_source_pdf_audit.json`. Selected relevant passages were examined; this is *not* a claim of paragraph-by-paragraph manual reading of every page.

Previous work **already proved** W33's 40-line four-point bus partition and a 12-perfect-matching edge coloring: `analysis/w33_scheduler_os.py`. We did not discover that theorem here. Prior BT827 asserts an 8n chart-route bound in a different hop model, `docs/W33_FRACTAL_MICROVM_RUNTIME.md` implements an operational software model, and Holotrade's `analysis/w33_level2.js` compared Cartesian/lexicographic/hierarchical choices. Pass 2686 correctly withdrew the idea that an older 3-ary RTL circuit models the 40-ary Holonet.

**This pass's distinct implementation** freezes an independently verified matching certificate, compiles four-lane/three-slot inter-child scheduling, constructs a physically motivated sparse graph and a 3-mode MZI optical selector surrogate, and then lowers the existing 40 four-point buses into exact 4x4 XOR/permutation target matrices with a valid recursive portal-address graph.

## Verified logical hardware options

| Scheme (depth 2) | Physical interface *analogue* per parent | Leaf graph logical links | Exact diameter |
|---|---|---:|---:|
| Cartesian W33 power | 12 inter-level peers per coordinate (degree 24) | 19,200 | 4 |
| Matched 4-gateway, 4 link replicas/W33 parent edge | 960 peer-specific inter-child links = 1,920 terminations | 10,560 | 5 |
| Sparse 4-gateway, fixed colored port/W33 parent edge | 240 inter-child links = 480 terminations | 9,840 | 7 |
| **40 four-port W33 line-buses** | **40 four-port switching buses = 160 endpoint incidences** | 9,840 leaf graph edges | **6** |

The 40 four-port bus network uses optical *target transfer matrices*, not an actual fabricated layout. Its 160 endpoint incidences are not 160 demonstrated bidirectional optical ports or physical waveguides. The bus edges must allow **two independent pair exchanges per bus per slot**.

At depth 3: the Cartesian leaf graph has 1,152,000 edges, replicated four-gateway has 423,360, and sparse matched-gateway has 393,840. The 40-line-bus graph has the same 393,840 leaf-pair graph edges but inter-child connectivity is expressed using four-port hyperedges, a different physical-interconnect contract.

## Four-lane scheduling certificate

`analysis/w33_fractal_four_lane_scheduler_20261023.py` freezes 12 edge-disjoint 20-edge perfect matchings of the exact 40-point symplectic graph. Color (k) maps to lane (k\bmod4), slot (⌊k/4⌋). Every parent W33 neighbor edge is served exactly once in three slots; all 40 children use each gateway lane at most once per slot. This is the optimum 3 slots for the explicitly assumed four active per-child lanes and 12 neighbors; physical switching/latency/clock budgets remain unspecified. At level two the 240-edge parent sparse graph produces 9,840 total leaf graph edges and exact diameter 7 (all 1,600 BFS roots checked). The certified constructive upper bound on depth-n sparse routes is (5\cdot2^{n-1}-3), **not** BT827's separate chart hop bound.

## Four-point line-bus Klein permutation targets

For a line with ports labeled by ℝ2², define `P_m[k XOR m, k] = 1` for masks (m=0,1,2,3). The three nonzero masks produce the three pairwise perfect matchings of K4. The permutation matrices are real, unitary, determinant +1, commute, and satisfy `P_m P_n = P_(m XOR n)`: the Klein-four group (C_2\times C_2) inside SO(4).

All **40 buses** simultaneously operate two disjoint pair exchanges per slot, so 40 x 2 = 80 neighbor exchanges per slot and all 240 edges in three slots. Each child belongs to four incident parent lines and uses **four independently addressable optical bus ports** per slot. This avoids pretending the finite incidence buses must be fabricated as 240 independent waveguide links. It still requires a *real 4-port programmable crossbar*; a passive 4-way splitter is not enough. A generic programmable 4x4 mesh could use six two-mode MZIs/bus, 240 per 40-bus parent, but the special three XOR states may permit a simpler design. That count is **architecture-only**, not PDK extraction.

The recursive port map chooses a bijection from each child's four incident **parent lines** to four **child gateway addresses** on one line. These are distinct mathematical objects; in particular an inter-child optical hop may change both the parent child-index and the gateway address. This produces a concrete, undirected depth-2 leaf graph with **diameter 6**, fully checked by BFS from all 1,600 vertices.

## Optical circuit component boundary

`analysis/w33_fractal_optical_switch_budget_20261023.py` separately models the **pairwise-link sparse 1-of-3 design**, using two ideal MZI transformations as a three-mode tree. It verifies lossless ideal port selection, attenuation, wrong-port leakage, and route-level loss accumulation. With **illustrative assumptions only** (0.2 dB/MZI, 0.1 dB link, 0.05 dB local graph hop, 0.05 rad phase error), 20 sampled depth-three routes show selected-path losses from ~1.11 to ~5.87 dB, mean ~4.15 dB. These numbers are **not measurements** and must **not** be assigned to the 40-bus XOR crossbar unless separately derived.

The existing 16-mode Halmos compiler (`analysis/w33_photonic_control_netlist_20261023.py`) and its 256 gauge-reduced logical control coordinates are a **separate subsystem**. It does not automatically supply a 4x4 bus switch, a 3-mode binary MZI tree, or a PDK electrode netlist. A real interface requires waveguide port types, a scattering-matrix convention, drive electrode mapping, electrical settling time, optical loss, wavelength plan, switching contention, clock domains, detector readout, optical LVS and foundry DRC.

## Complete verification run

```powershell
py -m pytest -q tests/test_w33_fractal_port_fabric_20261023.py tests/test_w33_fractal_four_lane_scheduler_20261023.py tests/test_w33_fractal_optical_switch_budget_20261023.py tests/test_w33_fractal_linebus_switch_matrix_20261023.py
# 28 passed (2026-10-23)
```

Further exact exhaustiveness:
- gateway4 depth-two diameter 5 (1,600 BFS roots);
- Cartesian depth-two diameter 4;
- sparse 4-lane depth-two diameter 7;
- line-bus depth-two diameter 6.
- 240 W33 edges, 40 lines of 4 points, 160 point-line incidences;
- 12 matching colors covering exactly 240 edges;
- 3 all-neighbor service slots, no logical lane contention in specified schedules;
- 4x4 XOR matrices form a finite group of exact unitary permutations.

## Work products

- `analysis/w33_fractal_port_fabric_20261023.py`, `data/w33_fractal_port_fabric_20261023.json`;
- `analysis/w33_fractal_four_lane_scheduler_20261023.py`, `data/w33_fractal_four_lane_schedule_20261023.json`;
- `analysis/w33_fractal_optical_switch_budget_20261023.py`, `data/w33_fractal_optical_switch_budget_20261023.json`;
- `analysis/w33_fractal_linebus_switch_matrix_20261023.py`, `data/w33_fractal_linebus_switch_matrix_20261023.json`;
- matching regression files in `tests/`;
- `papers/fractal_holonet_architecture_20261023.tex` and `papers/fractal_holonet_four_lane_addendum_20261023.tex` and `papers/fractal_holonet_40bus_optical_addendum_20261023.tex`;
- `analysis/2026_10_23_fractal_source_pdf_audit.json`.

## Five independent next frontiers

1. **PDK-backed four-port XOR exchange:** implement the three 4x4 permutation states in a valid process library, with exact port orientation, electrical pads, DRC and extracted optical loss. Compare a restricted permutation switch with a generic six-MZI 4x4 mesh.
2. **Hierarchical graph/cut optimization:** search for 4-port-to-parent-line assignments that improve the depth-three and higher diameter without increasing 160 child-to-bus endpoints per parent; prove a non-exponential route bound or a lower bound showing why it's impossible.
3. **Quantum process benchmark:** propagate one- and two-photon Fock inputs through the actual 4-mode exchange model, quantify spectral distinguishability, HOM outcomes, heralding and postselection; separate unitary permutation errors from detector SPAM.
4. **Fault-tolerant routing admission:** formalize gateway/bus failures and a deterministic alternate path, plus congestion/starvation tests. A valid finite route under healthy components is not a resilient network.
5. **Time-frequency multimode fabric:** investigate replacing spatial 4-port crossbars with coherent time-/frequency-bin multiplexed XOR ports, retaining typed source/detector timing and assessing whether it reduces crossings or merely relocates them to RF and dispersion budgets.

The candidate physical blueprint is the 40 four-port line-bus architecture. It lowers the `W(3,3)` adjacency to an experimentally falsifiable optical interface without silently promoting the graph results to a manufactured universal photonic machine.
