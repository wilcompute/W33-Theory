#!/usr/bin/env python3
"""Focused Holonet VM demo: universal computation, speedup boundary, and host-interface probes.

This is the presentation demo the VM actually deserves. It keeps three claims separate:

1. Exact runnable VM: W(3,3) routing, Clifford state, QEC, teleportation, self-reproduction.
2. Demonstrable efficiency: zero routing table and reduced abstraction/state overhead.
3. Frontier physical interface: ways a classical machine might drive/read a nearby photon/electron.

The third part is deliberately tiered. A bare CPU does not coherently entangle an optical photon in air
without an optical mode/coupler/detector. What a normal machine can do today is generate structured
current/thermal/EM side channels and read some built-in telemetry. That is an interface shadow, not a
photonic quantum computer. The viable route is CPU/VM -> electrical waveform -> electro-optic or
electroluminescent coupler -> photon/electron substrate -> detector/readout.
"""

from __future__ import annotations

import glob
import json
import os
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import holonet_bench as bench  # noqa: E402
import holonet_node as hn  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"


def vm_proof():
    src = hn.POINTS[0]
    dst = next(p for p in hn.POINTS if hn.symplectic(src, p) != 0)
    path = hn.route(src, dst)
    relays = hn.multipath(src, dst)

    reg = hn.CliffordRegister(2)
    reg.fourier(0)
    reg.sum(0, 1)
    qec = hn.qec_cycle(seed=7)
    tele = hn.teleport_state(seed=7)
    parent = hn.HolonetNode(src)
    child = parent.reproduce(dst)

    return {
        "nodes": len(hn.POINTS),
        "radix": len(hn.neighbors(src)),
        "route": [list(x) for x in path],
        "route_hops": len(path) - 1,
        "multipath_relays": len(relays),
        "clifford_stabilizers": reg.stabilizers(),
        "clifford_valid": reg.is_valid_state(),
        "qec_fidelity": qec["fidelity"],
        "teleport_fidelity": tele["fidelity"],
        "child_level": child.level,
        "honest_boundary": "Exact classical VM/proof-of-life. Quantum advantage still requires physical magic resource.",
    }


def rule110(bits):
    # Rule 110 outputs for neighborhoods 111,110,101,100,011,010,001,000.
    table = {
        (1, 1, 1): 0,
        (1, 1, 0): 1,
        (1, 0, 1): 1,
        (1, 0, 0): 0,
        (0, 1, 1): 1,
        (0, 1, 0): 1,
        (0, 0, 1): 1,
        (0, 0, 0): 0,
    }
    n = len(bits)
    return [table[(bits[(i - 1) % n], bits[i], bits[(i + 1) % n])] for i in range(n)]


def universal_computation_demo(steps=24):
    """Run a universal CA workload over the 40 Holonet nodes.

    Rule 110 is classically universal. This demo maps its 40 cells to W(3,3) points and uses Holonet
    routing as the communication fabric for nearest-neighbor updates. The host executes sequentially,
    but a physical 40-node fabric would update with synchronous depth `steps` and route depth <=2.
    """

    state = [0] * 40
    for i in [1, 2, 3, 6, 7, 11, 18, 27, 28, 31, 36]:
        state[i] = 1
    frames = ["".join("#" if b else "." for b in state)]
    total_messages = 0
    max_route_hops = 0
    for _ in range(steps):
        for i in range(40):
            for j in ((i - 1) % 40, (i + 1) % 40):
                p = hn.route(hn.POINTS[i], hn.POINTS[j])
                max_route_hops = max(max_route_hops, len(p) - 1)
                total_messages += 1
        state = rule110(state)
        frames.append("".join("#" if b else "." for b in state))

    return {
        "workload": "Rule 110 cellular automaton, a known universal classical computation model",
        "cells": 40,
        "steps": steps,
        "frames": frames,
        "total_neighbor_messages": total_messages,
        "max_route_hops": max_route_hops,
        "sequential_host_cell_updates": 40 * steps,
        "physical_fabric_depth_if_parallel": steps,
        "structural_parallelism_factor": 40,
        "boundary": "This proves a universal computation can be hosted on the Holonet VM/fabric model. It is not a quantum speedup on a single CPU.",
    }


def _read_int(path):
    try:
        return int(Path(path).read_text().strip())
    except Exception:
        return None


def read_host_observables():
    rapl = {}
    for path in glob.glob("/sys/class/powercap/intel-rapl*/energy_uj"):
        val = _read_int(path)
        if val is not None:
            rapl[path] = val
    temps = {}
    for path in glob.glob("/sys/class/thermal/thermal_zone*/temp"):
        val = _read_int(path)
        if val is not None:
            temps[path] = val
    freqs = {}
    for path in glob.glob("/sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq")[:8]:
        val = _read_int(path)
        if val is not None:
            freqs[path] = val
    return {
        "time_ns": time.perf_counter_ns(),
        "rapl_energy_uj": rapl,
        "thermal_millic": temps,
        "cpu_freq_khz_sample": freqs,
    }


def route_workload(rounds):
    acc = 0
    pts = hn.POINTS
    for _ in range(rounds):
        for a in pts:
            for b in pts:
                acc += hn.symplectic(a, b)
    return acc


def host_interface_probe():
    """Use only built-in host observables to see whether a Holonet workload leaves a shadow."""

    probes = []
    for name, rounds in [
        ("idle", 0),
        ("low_route_current", 300),
        ("high_route_current", 3000),
    ]:
        before = read_host_observables()
        if rounds == 0:
            time.sleep(0.15)
            acc = 0
        else:
            acc = route_workload(rounds)
        after = read_host_observables()
        dt = (after["time_ns"] - before["time_ns"]) / 1e9
        energy_delta = {
            k: after["rapl_energy_uj"].get(k, 0) - v
            for k, v in before["rapl_energy_uj"].items()
            if k in after["rapl_energy_uj"]
        }
        temp_delta = {
            k: after["thermal_millic"].get(k, 0) - v
            for k, v in before["thermal_millic"].items()
            if k in after["thermal_millic"]
        }
        probes.append(
            {
                "pattern": name,
                "rounds": rounds,
                "elapsed_s": dt,
                "accumulator": acc,
                "rapl_energy_delta_uj": energy_delta,
                "thermal_delta_millic": temp_delta,
                "observable_channels": {
                    "rapl": bool(energy_delta),
                    "thermal": bool(temp_delta),
                    "timing": True,
                },
            }
        )
    return {
        "claim": "A classical host can emit and sometimes self-read workload-dependent timing/power/thermal shadows without extra lab sensors.",
        "probes": probes,
        "boundary": "This is not photon-state readout. It is a built-in side-channel/control-shadow primitive that could drive a real coupler.",
    }


def speedup_boundary():
    compare, ok = bench.run_compare()
    magic = []
    for t in [0, 1, 2, 5, 10, 20, 30]:
        magic.append({"magic_gates": t, "classical_emulation_factor": 9**t})
    return {
        "table_free_compare_ok": ok,
        "table_free_compare": compare,
        "magic_dial": magic,
        "boundary": (
            "The demo proves exact architecture/overhead wins on this machine. It does not prove a "
            "quantum speedup on this CPU; physical speedup requires the non-Clifford/magic resource in "
            "a photonic/electronic substrate."
        ),
    }


def coupler_catalog():
    ideas = [
        (
            "RAPL/thermal/timing shadow",
            "Use built-in energy/time/thermal counters as no-extra-sensor readout of route-coded workloads.",
            "A",
            "works today as host shadow, not photon readout",
        ),
        (
            "CPU current loop -> EOM",
            "Drive an electro-optic modulator with a route-coded waveform; photon phase/polarization is the real substrate.",
            "A-",
            "needs coupler/detector",
        ),
        (
            "USB/NIC/GPIO RF line -> resonant EOM",
            "Use commodity I/O as the electrical driver for a resonant optical modulator.",
            "B+",
            "needs optical path",
        ),
        (
            "Electroluminescent diode rail",
            "Use controlled current through a diode/LED junction to emit photons: practical reverse-photoelectric route.",
            "B+",
            "photon source, not entanglement by itself",
        ),
        (
            "On-board LED/display pixel",
            "Use existing photons from LEDs/screen as a crude optical carrier for route-coded pulses.",
            "B",
            "classical light unless quantum source added",
        ),
        (
            "DRAM rowhammer electron medium",
            "Use repeated memory access to manipulate charge/leakage/bit flips as an electron-state substrate.",
            "B",
            "classical/stochastic electron readout",
        ),
        (
            "Flash/SSD charge trap",
            "Use existing nonvolatile charge states as slow electron memory for a Holonet-addressed substrate.",
            "B-",
            "slow and controller-mediated",
        ),
        (
            "PLL/clock jitter readout",
            "Encode route patterns into clock-load jitter and read timing variance.",
            "B",
            "side-channel shadow only",
        ),
        (
            "CPU RF/TEMPEST emission",
            "Route-coded current patterns leak RF; a receiver could observe them.",
            "B",
            "external receiver normally required",
        ),
        (
            "No-sensor acoustic coil",
            "Use speaker/coil/inductor current as a route-coded field, read back via timing or microphone if present.",
            "B-",
            "not photon-native",
        ),
        (
            "Wi-Fi/Bluetooth carrier",
            "Use commodity RF as the physical carrier for Holonet-coded waveforms.",
            "B",
            "RF classical, but available",
        ),
        (
            "LCD polarization modulator",
            "Use a screen pixel as a slow polarization/intensity modulator for a photon path.",
            "B-",
            "slow, lossy, needs detector",
        ),
        (
            "Camera rolling shutter feedback",
            "Use built-in camera as detector for display/LED photonic shadows.",
            "B-",
            "uses built-in sensor",
        ),
        (
            "Thermal lensing in package air",
            "Drive heat gradients to modulate refractive index near a beam path.",
            "C+",
            "very slow/noisy",
        ),
        (
            "Fan tachometer feedback",
            "Route-coded CPU heat changes fan response; read tach as a built-in macroscopic sensor.",
            "C",
            "classical thermal channel",
        ),
        (
            "Piezo/acousto-optic coupler",
            "Use electrical route pattern to drive acoustic waves that modulate light.",
            "B",
            "needs AOM/piezo medium",
        ),
        (
            "Magneto-optic Faraday cell",
            "Use current-induced magnetic field to rotate polarization.",
            "B-",
            "needs material and optical path",
        ),
        (
            "NV center near motherboard",
            "Microwave/current/thermal fields drive electron spin defects as a quantum substrate.",
            "B",
            "needs defect sample/readout",
        ),
        (
            "Trapped electron/ion interface",
            "CPU generates waveform; actual computation in electron/ion trap.",
            "C",
            "not commodity machine",
        ),
        (
            "Silicon photonic ring on PCIe card",
            "Classical host supplies digital control; ring resonator supplies photon qudit.",
            "A",
            "best engineering route",
        ),
        (
            "Integrated SiC/LN Pockels modulator",
            "Use foundry-compatible EO platform for low-voltage photon phase control.",
            "A",
            "requires photonic chip",
        ),
        (
            "CMOS avalanche/electroluminescence",
            "Leverage weak light emission from semiconductor junctions under stress.",
            "C",
            "unreliable and potentially damaging",
        ),
        (
            "Power-supply coil optical pickup",
            "Inductor EM fields encode current waveforms that a nearby EO crystal samples.",
            "B-",
            "needs pickup medium",
        ),
        (
            "Memory-bus antenna",
            "Use DRAM bus activity as high-speed RF source for a nearby resonator.",
            "C+",
            "compliance/noise issues",
        ),
        (
            "Cache-conflict oscillator",
            "Construct a route-coded timing oscillator from cache conflicts.",
            "B",
            "software-only shadow",
        ),
        (
            "Branch predictor metronome",
            "Use predictor state as hidden classical memory carrying W33 address patterns.",
            "B-",
            "fragile, not quantum",
        ),
        (
            "GPU shader optical carrier",
            "Use GPU power/display output as a wide parallel modulator.",
            "B",
            "good classical interface",
        ),
        (
            "Network of laptops as one VM",
            "Each host runs a Holonet node; route=gate messages build a distributed universal CA.",
            "A",
            "software network, no quantum speedup",
        ),
        (
            "FPGA ternary front end",
            "Classical PC initiates; FPGA implements mod-3 ALU and waveform driver.",
            "A",
            "near-term hardware demo",
        ),
        (
            "Photonic lab kit",
            "PC controls source/EOM/analyzer; photon is the compute substrate; PC is only interface.",
            "A",
            "honest full route",
        ),
    ]
    rows = []
    for idea, text, score, boundary in ideas:
        rows.append(
            {
                "idea": idea,
                "concept": text,
                "score": score,
                "boundary": boundary,
            }
        )
    return {
        "core_physics_boundary": (
            "A normal CPU in air cannot coherently self-entangle an optical photon merely by bit flips. "
            "CPU fields are mostly near-field RF/thermal/IR and lack a confined optical mode plus detector. "
            "Use the CPU as waveform generator/interface; put the quantum state in an EOM, diode, defect, "
            "ring resonator, or other real coupling medium."
        ),
        "top_three": rows[:3],
        "rows": rows,
        "sources": [
            "RP Photonics EOM overview: electrical signals control optical phase/power/polarization.",
            "Intel RAPL advisory: processors expose accumulated energy reporting and it can leak data-dependent power information.",
            "DOE electroluminescent semiconductor note: adding charge carriers can make semiconductors emit photons.",
            "J. Appl. Phys. electro-optic modulation review: integrated modulators are central to photonic communications and exploit multiple physical mechanisms.",
        ],
    }


def write_markdown(payload):
    lines = []
    lines.append("# Holonet VM Demonstration And Classical-Interface Frontier\n")
    lines.append(
        "This is the focused demo path: run the VM, show universal computation, quantify the speedup boundary, then discuss physical couplers honestly.\n"
    )
    lines.append("## Live Commands\n")
    lines.append(
        "```bash\n.venv/bin/python analysis/holonet_vm_interface_demo.py\n.venv/bin/python analysis/holonet_physical_substrate_stub.py\n.venv/bin/python analysis/holonet_sidechannel_suite.py\n.venv/bin/python analysis/holonet_node.py\n.venv/bin/python analysis/holonet_cli.py verify\n.venv/bin/python analysis/holonet_cli.py bench --compare\n```\n"
    )
    lines.append("## What The VM Actually Demonstrates\n")
    vm = payload["vm"]
    lines.append(
        f"- {vm['nodes']} nodes, radix {vm['radix']}, route hops {vm['route_hops']}, multipath relays {vm['multipath_relays']}.\n"
    )
    lines.append(
        f"- Clifford valid: {vm['clifford_valid']}; QEC fidelity {vm['qec_fidelity']:.6f}; teleport fidelity {vm['teleport_fidelity']:.6f}; child level {vm['child_level']}.\n"
    )
    lines.append("## Universal Computation Demo\n")
    uni = payload["universal_rule110"]
    lines.append(f"- Workload: {uni['workload']}.\n")
    lines.append(
        f"- {uni['cells']} cells for {uni['steps']} steps over the W(3,3) fabric; max route depth {uni['max_route_hops']}.\n"
    )
    lines.append(
        "```text\n"
        + "\n".join(uni["frames"][:12])
        + "\n...\n"
        + "\n".join(uni["frames"][-4:])
        + "\n```\n"
    )
    lines.append("## Speedup Boundary\n")
    sp = payload["speedup"]
    cmp = sp["table_free_compare"]
    lines.append(f"- Table-free compare pass: {sp['table_free_compare_ok']}.\n")
    lines.append(
        f"- Classical routing state: {cmp['baseline_table_routed']['routing_table_bytes']} bytes; Holonet routing state: {cmp['holonet_address_routed']['routing_table_bytes']} bytes.\n"
    )
    lines.append(
        f"- Magic dial example: 30 non-Clifford gates have classical emulation factor {sp['magic_dial'][-1]['classical_emulation_factor']}.\n"
    )
    lines.append(
        "- Exact speedup here is state/setup/abstraction overhead. Quantum speedup still requires a physical non-Clifford substrate.\n"
    )
    lines.append("## Classical Machine As Interface\n")
    probe = payload["host_probe"]
    for row in probe["probes"]:
        lines.append(
            f"- {row['pattern']}: {row['elapsed_s']:.6f}s; channels={row['observable_channels']}.\n"
        )
    lines.append("\n## Physical Coupler Top Ideas\n")
    for row in payload["coupler_catalog"]["rows"][:10]:
        lines.append(
            f"- **{row['idea']}** ({row['score']}): {row['concept']} Boundary: {row['boundary']}.\n"
        )
    lines.append("\n## Hard Boundary\n")
    lines.append(payload["coupler_catalog"]["core_physics_boundary"] + "\n")
    lines.append("\n## New Focused Artifacts\n")
    lines.append(
        "- `docs/holonet_vm_live_demo.html`: browser page for route, Rule 110, magic dial, and interface demo.\n"
    )
    lines.append(
        "- `analysis/holonet_physical_substrate_stub.py`: CPU waveform -> EOM/ring -> photon qutrit mock detector.\n"
    )
    lines.append(
        "- `docs/holonet_physical_substrate_stub.svg`: visual waveform/detector summary from the stub.\n"
    )
    lines.append(
        "- `analysis/holonet_sidechannel_suite.py`: no-extra-sensor host observability report.\n"
    )
    lines.append(
        "- `docs/holonet_sidechannel_report.md`: machine-local report of timing/resource/RAPL/thermal/frequency/perf availability.\n"
    )
    lines.append(
        "- `analysis/holonet_wrap.py`: wrap any classical command in a Holonet control envelope.\n"
    )
    lines.append(
        "- `analysis/holonet_vm_demo_launcher.py`: one-command launcher for VM, physical stub, side-channel suite, and wrapper demo.\n"
    )
    lines.append(
        "- `docs/holonet_physical_substrate_interactive.html`: browser sliders for visibility/loss/ring-Q.\n"
    )
    (DOCS / "holonet_vm_demo_and_interface_frontier.md").write_text(
        "".join(lines), encoding="utf-8"
    )


def main():
    DATA.mkdir(exist_ok=True)
    DOCS.mkdir(exist_ok=True)
    payload = {
        "vm": vm_proof(),
        "universal_rule110": universal_computation_demo(),
        "speedup": speedup_boundary(),
        "host_probe": host_interface_probe(),
        "coupler_catalog": coupler_catalog(),
    }
    (DATA / "holonet_vm_interface_demo.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    write_markdown(payload)

    print("HOLONET VM INTERFACE DEMO")
    print("-------------------------")
    print(
        f"VM: {payload['vm']['nodes']} nodes, route hops {payload['vm']['route_hops']}, mu={payload['vm']['multipath_relays']}, Clifford valid={payload['vm']['clifford_valid']}"
    )
    print(
        f"Proof of life: QEC fidelity={payload['vm']['qec_fidelity']:.6f}, teleport fidelity={payload['vm']['teleport_fidelity']:.6f}, child level={payload['vm']['child_level']}"
    )
    uni = payload["universal_rule110"]
    print(
        f"Universal computation: Rule 110 on {uni['cells']} Holonet nodes for {uni['steps']} steps, max route hops={uni['max_route_hops']}"
    )
    cmp = payload["speedup"]["table_free_compare"]
    print(
        f"Speedup boundary: table-free routing {cmp['baseline_table_routed']['routing_table_bytes']} bytes -> {cmp['holonet_address_routed']['routing_table_bytes']} bytes; setup {cmp['baseline_table_routed']['setup_bfs_edge_relaxations']} -> {cmp['holonet_address_routed']['setup_ops']}"
    )
    print(
        f"Magic dial boundary: 30 non-Clifford gates imply classical emulation factor {payload['speedup']['magic_dial'][-1]['classical_emulation_factor']:,}; physical speedup needs a real magic substrate"
    )
    print("Host-interface probe:")
    for row in payload["host_probe"]["probes"]:
        print(
            f"  {row['pattern']}: {row['elapsed_s']:.6f}s channels={row['observable_channels']}"
        )
    print("Top physical-interface candidates:")
    for row in payload["coupler_catalog"]["top_three"]:
        print(f"  {row['score']} {row['idea']}: {row['concept']}")
    print("\nHard boundary: " + payload["coupler_catalog"]["core_physics_boundary"])
    print("\nwrote data/holonet_vm_interface_demo.json")
    print("wrote docs/holonet_vm_demo_and_interface_frontier.md")


if __name__ == "__main__":
    main()
