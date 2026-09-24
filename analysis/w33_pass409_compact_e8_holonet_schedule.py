#!/usr/bin/env python3
"""Pass 409: compile the compact E8 pair into the Holonet microframe ABI."""
from __future__ import annotations

import importlib.util
import json
from fractions import Fraction
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_pass409_compact_e8_holonet_schedule.json"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(write=True):
    dw = load(ROOT / "analysis/w33_diagonal_weld_e8_lie_generation.py", "diag")
    ri = load(ROOT / "analysis/w33_e8_split_real_form_involution.py", "realform")
    compiler, bridge, table = dw.load_inputs()
    vectors = dw.source_generators(compiler, dw.backgrounds(bridge))
    compact = json.loads((ROOT / "data/w33_pass409_compact_e8_control.json").read_text())
    sc = json.loads((ROOT / "artifacts/e8_structure_constants_w33_discrete.json").read_text())
    microframe = json.loads((ROOT / "data/bt1407_microframe_transaction_composer.json").read_text())
    row_pulses = json.loads((ROOT / "data/bt1493_row_action_physical_pulse_compiler.json").read_text())
    universal = json.loads((ROOT / "data/bt1603_universal_computation_proof_closure.json").read_text())

    assert compact["status"] == "PASS_TWO_EXPLICIT_COMPACT_REAL_CONTROLS_GENERATE_E8"
    assert microframe["verified"] and all(microframe["checks"].values())
    assert row_pulses["verified"] and all(row_pulses["checks"].values())
    assert universal["verified"] and all(universal["checks"].values())

    roots = [tuple(map(int, root)) for root in sc["basis"]["roots"]]
    root_index = {root: 8+i for i, root in enumerate(roots)}
    negative = {8+i: root_index[tuple(-x for x in root)] for i, root in enumerate(roots)}
    phase = {
        i: (-1 if ri.killing(sc, i, negative[i]) > 0 else 1)
        for i in range(8, 248)
    }
    maps = compiler["coordinate_maps"]
    grade1_row = {int(source): row for row, source in enumerate(maps["grade1_source_indices"])}
    grade2_row = {int(source): row for row, source in enumerate(maps["grade2_source_indices"])}
    addresses = {
        int(i): tuple(map(int, h))
        for i, h in bridge["maps"]["e6id_to_current_H27_address"].items()
    }

    x = list(map(int, vectors[(1, "plus")]))
    atoms = {"A": [], "B": []}
    for source, coefficient in enumerate(x):
        if not coefficient:
            continue
        partner = negative[source]
        row = grade1_row[source]
        assert grade2_row[partner] == row
        eid, external = divmod(row, 3)
        common = {
            "atom": row,
            "row": row,
            "e6id": eid,
            "H27_address": list(addresses[eid]),
            "external_trit": external,
            "grade1_source": source,
            "grade2_source": partner,
            "grade1_coefficient": coefficient,
        }
        atoms["A"].append({
            **common,
            "quadrature": "real",
            "grade2_coefficient": phase[source]*coefficient,
        })
        atoms["B"].append({
            **common,
            "quadrature": "imaginary",
            "grade2_coefficient": -phase[source]*coefficient,
        })
    assert len(atoms["A"]) == len(atoms["B"]) == 81

    def sparse_bracket(left, right):
        out = {}
        for i, xco in left.items():
            for j, yco in right.items():
                if i == j:
                    continue
                sign = 1 if i < j else -1
                for k, structure in table.get((min(i, j), max(i, j)), ()):
                    out[k] = out.get(k, 0) + sign*xco*yco*structure
                    if out[k] == 0:
                        del out[k]
        return out

    def atom_vector(atom):
        return {
            atom["grade1_source"]: atom["grade1_coefficient"],
            atom["grade2_source"]: atom["grade2_coefficient"],
        }

    schedules = {}
    batch_vectors = []
    for control in ("A", "B"):
        graph = nx.Graph()
        graph.add_nodes_from(range(81))
        vectors81 = [atom_vector(atom) for atom in atoms[control]]
        for i in range(81):
            for j in range(i+1, 81):
                if sparse_bracket(vectors81[i], vectors81[j]):
                    graph.add_edge(i, j)
        coloring = nx.coloring.greedy_color(
            graph, strategy="largest_first", interchange=True
        )
        colors = sorted(set(coloring.values()))
        batches = []
        for color in colors:
            members = sorted(i for i, value in coloring.items() if value == color)
            for i, first in enumerate(members):
                for second in members[i+1:]:
                    assert not sparse_bracket(vectors81[first], vectors81[second])
            total = {}
            for member in members:
                for key, value in vectors81[member].items():
                    total[key] = total.get(key, 0) + value
            batch_vectors.append((control, color, total))
            batches.append({
                "local_batch": color,
                "atom_ids": members,
                "atom_count": len(members),
                "all_atoms_commute_exactly": True,
                "all_atoms_compact_fixed": True,
            })
        clique = max(nx.find_cliques(graph), key=len)
        assert len(colors) == 15 and len(clique) == 7
        schedules[control] = {
            "atoms": atoms[control],
            "conflict_edges": graph.number_of_edges(),
            "exact_clique_lower_bound": len(clique),
            "commuting_batch_upper_bound": len(colors),
            "chromatic_interval": [len(clique), len(colors)],
            "batch_sizes": [batch["atom_count"] for batch in batches],
            "batches": batches,
        }

    # The A and B conflict graphs are identical; the 15+15 batches fill one
    # 30-microframe E8 Coxeter bus exactly.
    assert schedules["A"]["conflict_edges"] == schedules["B"]["conflict_edges"]
    schedule = []
    for global_frame, (control, local, _) in enumerate(batch_vectors):
        schedule.append({
            "microframe": global_frame,
            "control": control,
            "local_batch": local,
            "tick_start": 72*global_frame,
            "tick_stop_exclusive": 72*(global_frame+1),
            "atom_ids": schedules[control]["batches"][local]["atom_ids"],
        })
    assert len(schedule) == 30 and schedule[-1]["tick_stop_exclusive"] == 2160

    # Exact first-order BCH coefficient in coefficient l1 norm for the chosen
    # 30-layer ordering. A batches are real and B batches imaginary, so only
    # the absolute coefficient sum is needed here.
    bch_sum = 0
    for i, (ci, _, vi) in enumerate(batch_vectors):
        for cj, _, vj in batch_vectors[i+1:]:
            bracket = sparse_bracket(vi, vj)
            # [i*vi,i*vj]=-[vi,vj], [vi,i*vj]=i[vi,vj]; absolute l1 is unchanged.
            bch_sum += sum(abs(value) for value in bracket.values())
    bch_half = Fraction(bch_sum, 2)

    out = {
        "schema": "w33.pass409.compact_e8_holonet_schedule.v1",
        "status": "PASS_COMPACT_E8_PAIR_FITS_ONE_30_MICROFRAME_COXETER_BUS",
        "source_control": "plus diagonal H27 compact pair A=x+sigma(x), B=i(x-sigma(x))",
        "compiler": {
            "compact_root_plane_atoms_per_control": 81,
            "commuting_batches_per_control": 15,
            "microframes_per_AB_cycle": 30,
            "ticks_per_microframe": 72,
            "ticks_per_AB_cycle": 2160,
            "AB_cycles_per_51840_tick_window": 24,
            "schedule": schedule,
            "A": schedules["A"],
            "B": schedules["B"],
        },
        "exact_alignment": {
            "E8_Coxeter_number": 30,
            "microframes_per_control_cycle": 30,
            "existing_E8_Coxeter_bus_ticks": 2160,
            "identity": "15 A batches + 15 B batches = 30 microframes; 30*72=2160; 24*2160=51840",
        },
        "robustness": {
            "compact_form_leakage_per_atom": 0,
            "compact_form_leakage_per_batch": 0,
            "reason": "Every scheduled atom is an opposite-root compact fixed-plane generator; every batch is a sum of fixed generators.",
            "exact_conflict_free_batches": True,
            "first_order_BCH_l1_coefficient": str(bch_half),
            "error_statement": "For dimensionless layer duration tau, the formal first-order product error has coefficient at most this value times tau^2 in Chevalley coefficient l1 norm, before higher orders.",
        },
        "architecture_reading": "The exact compact E8 control pair has a finite address schedule that lands on the pre-existing 30-frame E8 Coxeter bus without padding. This is a control-ABI theorem; it does not yet lower the new root-plane analog macro to calibrated optical components.",
        "boundary": "BT1493 supplies calibrated finite S4/D4 row actions, not analog exponentials of every E8 root plane. ROOT_PLANE_ANALOG remains a new macro whose amplitude, duration, loss, bandwidth, crosstalk, and laboratory error must be calibrated. The 15-color schedule is a certified upper bound, not a proof of chromatic optimality.",
        "parents": [
            "data/w33_pass409_compact_e8_control.json",
            "data/bt1407_microframe_transaction_composer.json",
            "data/bt1493_row_action_physical_pulse_compiler.json",
            "data/bt1603_universal_computation_proof_closure.json",
        ],
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
