#!/usr/bin/env python3
"""Route the optimized 240-qutrit linear Clifford onto the W33 edge line graph.

Physical carrier qutrits are the 240 W33 edges.  This compiler adopts one
explicit topological-locality contract: a primitive two-qutrit interaction is
local iff the two carrier edges share a W33 point.  Arbitrary SUM_ALPHA and
SWAP macros from the exact linear-Clifford encoder are lowered to shortest paths
in that 240-vertex line graph.

For a remote SUM, the control state is swapped along the path to the edge next
to the target, the SUM is applied locally, and the swaps are undone.  For a
remote SWAP, the standard forward/backward nearest-neighbour transposition
sequence swaps only the endpoints.  Every lowered macro is independently
replayed over GF(3) and checked against its intended linear action.

Macros that were already dependency-disjoint in a Holonet compiler frame are
partitioned into route-support-disjoint batches.  Each batch executes its local
programs in parallel cycle by cycle.  The result reports exact topological
routing depth and congestion under this interaction graph.  It is not yet a
calibrated photonic pulse schedule or a stochastic fault-propagation theorem.
"""
from __future__ import annotations

from collections import Counter, deque
from functools import lru_cache
import hashlib
import json

import numpy as np

import w33_qutrit_20_7_2_clifford_holonet_compiler as cliff
import w33_qutrit_20_7_2_multiminor_optimizer as multi
import w33_qutrit_20_7_2_sparse_symplectic as sparse


def shortest_path(adj, s, t):
    if s == t:
        return [s]
    prev = {s: None}
    q = deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v in prev:
                continue
            prev[v] = u
            if v == t:
                out = [t]
                while out[-1] != s:
                    out.append(prev[out[-1]])
                return list(reversed(out))
            q.append(v)
    raise RuntimeError("line graph route missing")


def local_swap(a, b, endpoints):
    shared = sorted(set(endpoints[a]) & set(endpoints[b]))
    if len(shared) != 1:
        raise RuntimeError("nearest-neighbour SWAP does not share exactly one W33 point")
    return {"op": "SWAP", "a": int(a), "b": int(b), "coupler_vertex": int(shared[0])}


def local_sum(c, t, alpha, endpoints):
    shared = sorted(set(endpoints[c]) & set(endpoints[t]))
    if len(shared) != 1:
        raise RuntimeError("nearest-neighbour SUM does not share exactly one W33 point")
    return {"op": "SUM_ALPHA", "control": int(c), "target": int(t), "alpha": int(alpha) % 3, "coupler_vertex": int(shared[0])}


def route_macro(g, adj, endpoints):
    if g["gate"] == "SCALE2":
        return [{"op": "SCALE2", "wire": int(g["wire"])}], [int(g["wire"])]
    if g["gate"] == "SUM_ALPHA":
        path = shortest_path(adj, int(g["control"]), int(g["target"]))
        if len(path) < 2:
            raise RuntimeError("SUM control and target collapsed")
        p = []
        for i in range(len(path) - 2):
            p.append(local_swap(path[i], path[i + 1], endpoints))
        p.append(local_sum(path[-2], path[-1], int(g["alpha"]), endpoints))
        for i in reversed(range(len(path) - 2)):
            p.append(local_swap(path[i], path[i + 1], endpoints))
        return p, path
    if g["gate"] == "SWAP":
        path = shortest_path(adj, int(g["a"]), int(g["b"]))
        if len(path) < 2:
            return [], path
        p = [local_swap(path[i], path[i + 1], endpoints) for i in range(len(path) - 1)]
        p.extend(local_swap(path[i], path[i + 1], endpoints) for i in reversed(range(len(path) - 2)))
        return p, path
    raise ValueError(f"unsupported compiler macro {g['gate']}")


def op_wires(op):
    if op["op"] == "SCALE2":
        return {int(op["wire"])}
    if op["op"] == "SWAP":
        return {int(op["a"]), int(op["b"])}
    return {int(op["control"]), int(op["target"])}


def replay_linear(n, ops, wire_order=None):
    if wire_order is None:
        wire_order = list(range(n))
    pos = {w: i for i, w in enumerate(wire_order)}
    M = np.eye(len(wire_order), dtype=np.int64)
    for op in ops:
        if op["op"] == "SWAP":
            a, b = pos[int(op["a"])], pos[int(op["b"])]
            M[:, [a, b]] = M[:, [b, a]]
        elif op["op"] == "SCALE2":
            q = pos[int(op["wire"])]
            M[:, q] = (2 * M[:, q]) % 3
        elif op["op"] == "SUM_ALPHA":
            c, t = pos[int(op["control"])], pos[int(op["target"])]
            M[:, t] = (M[:, t] + int(op["alpha"]) * M[:, c]) % 3
        else:
            raise ValueError(op["op"])
    return M % 3


def verify_macro_program(g, program, path):
    wires = list(dict.fromkeys(path))
    if g["gate"] == "SCALE2":
        wires = [int(g["wire"])]
    M = replay_linear(len(wires), program, wires)
    E = np.eye(len(wires), dtype=np.int64)
    pos = {w: i for i, w in enumerate(wires)}
    if g["gate"] == "SCALE2":
        E[:, 0] = (2 * E[:, 0]) % 3
    elif g["gate"] == "SUM_ALPHA":
        c, t = pos[int(g["control"])], pos[int(g["target"])]
        E[:, t] = (E[:, t] + int(g["alpha"]) * E[:, c]) % 3
    elif g["gate"] == "SWAP":
        a, b = pos[int(g["a"])], pos[int(g["b"])]
        E[:, [a, b]] = E[:, [b, a]]
    return bool(np.array_equal(M, E % 3))


def program_support(program):
    return set(w for op in program for w in op_wires(op))


def partition_batches(items):
    batches = []
    for item in items:
        support = item["route_support"]
        placed = False
        for b in batches:
            if not (support & b["used"]):
                b["items"].append(item)
                b["used"].update(support)
                placed = True
                break
        if not placed:
            batches.append({"items": [item], "used": set(support)})
    return batches


def schedule_batches(batches):
    cycles = []
    for b in batches:
        depth = max((len(x["program"]) for x in b["items"]), default=0)
        for k in range(depth):
            ops = []
            origins = []
            used = set()
            for item in b["items"]:
                if k >= len(item["program"]):
                    continue
                op = dict(item["program"][k])
                ws = op_wires(op)
                if used & ws:
                    raise RuntimeError("route-support batch produced a physical conflict")
                used.update(ws)
                ops.append(op)
                origins.append(int(item["gate_index"]))
            cycles.append({"ops": ops, "gate_indices": origins})
    return cycles


def digest_json(v):
    return "sha256:" + hashlib.sha256(json.dumps(v, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


@lru_cache(maxsize=None)
def compile_routes(candidate_count=multi.DEFAULT_CANDIDATES):
    hx, hz, h, T, A0, dist, candidates, winner = multi.selected_witness(int(candidate_count))
    A, B = winner["A"], winner["B"]
    F, Finv = cliff.build_full_linear(A, B)
    gates = cliff.reduce_columns_to_identity(F)
    frames = cliff.pack_microframes(gates)
    endpoints, adj = multi.edge_graph(hx)

    physical_cycles = []
    macro_records = []
    physical_load = Counter()
    coupler_load = Counter()
    logical_exposure = Counter()
    route_lengths = []
    local_twoq = 0
    local_oneq = 0
    verified = True

    for frame in frames:
        items = []
        for slot in frame["slots"]:
            gi = int(slot["gate_index"])
            g = slot["gate"]
            program, path = route_macro(g, adj, endpoints)
            ok = verify_macro_program(g, program, path)
            verified = verified and ok
            support = program_support(program)
            if g["gate"] != "SCALE2":
                route_lengths.append(len(path) - 1)
            for q in cliff.wires(g):
                if int(q) < 20:
                    logical_exposure[int(q)] += len(program)
            for op in program:
                ws = op_wires(op)
                for w in ws:
                    physical_load[int(w)] += 1
                if len(ws) == 2:
                    local_twoq += 1
                    coupler_load[int(op["coupler_vertex"])] += 1
                else:
                    local_oneq += 1
            item = {
                "gate_index": gi,
                "gate": g,
                "program": program,
                "path": list(map(int, path)),
                "route_support": support,
                "verified": ok,
            }
            items.append(item)
            macro_records.append(item)
        batches = partition_batches(items)
        physical_cycles.extend(schedule_batches(batches))

    for cyc in physical_cycles:
        used = set()
        for op in cyc["ops"]:
            ws = op_wires(op)
            if used & ws:
                raise RuntimeError("physical cycle has conflicting carrier edges")
            used.update(ws)
            if len(ws) == 2:
                a, b = sorted(ws)
                if b not in adj[a]:
                    raise RuntimeError("nonlocal primitive escaped route compiler")

    flat_ops = [op for c in physical_cycles for op in c["ops"]]
    sample = []
    if macro_records:
        longest = max(macro_records, key=lambda x: len(x["program"]))
        for x in macro_records[:2] + [longest] + macro_records[-2:]:
            sample.append({
                "gate_index": x["gate_index"],
                "gate": x["gate"],
                "path": x["path"],
                "local_program": x["program"],
                "verified": bool(x["verified"]),
            })
    return {
        "hx": hx, "hz": hz, "A": A, "B": B, "F": F, "Finv": Finv,
        "winner": winner, "gates": gates, "frames": frames, "endpoints": endpoints,
        "adj": adj, "cycles": physical_cycles, "flat_ops": flat_ops,
        "metrics": {
            "compiler_macros": int(len(gates)),
            "holonet_frames": int(len(frames)),
            "local_two_qutrit_ops": int(local_twoq),
            "local_one_qutrit_ops": int(local_oneq),
            "topological_depth_cycles": int(len(physical_cycles)),
            "max_shortest_path_edges": int(max(route_lengths, default=0)),
            "mean_shortest_path_edges": float(sum(route_lengths) / len(route_lengths)) if route_lengths else 0.0,
            "max_physical_edge_qutrit_load": int(max(physical_load.values(), default=0)),
            "max_w33_point_coupler_load": int(max(coupler_load.values(), default=0)),
            "logical_input_exposure_first20": [int(logical_exposure[i]) for i in range(20)],
            "schedule_sha256": digest_json(physical_cycles),
        },
        "sample": sample,
        "all_macro_programs_verified": bool(verified),
    }


def verify(candidate_count=multi.DEFAULT_CANDIDATES):
    c = compile_routes(int(candidate_count))
    adj = c["adj"]
    checks = {
        "all_compiler_macros_lowered": len(c["gates"]) > 0,
        "all_macro_programs_replay_exactly": c["all_macro_programs_verified"],
        "every_two_qutrit_primitive_is_line_graph_local": all(
            len(op_wires(op)) != 2 or max(op_wires(op)) in adj[min(op_wires(op))]
            for op in c["flat_ops"]
        ),
        "every_physical_cycle_is_conflict_free": all(
            sum(len(op_wires(op)) for op in cyc["ops"]) == len(set(w for op in cyc["ops"] for w in op_wires(op)))
            for cyc in c["cycles"]
        ),
        "symplectic_embedding_still_exact": np.array_equal((c["A"] @ c["B"].T) % 3, np.eye(20, dtype=np.int64)),
        "finite_topological_depth": c["metrics"]["topological_depth_cycles"] > 0,
    }
    checks = {k: bool(v) for k, v in checks.items()}
    return {
        "schema": "w33.qutrit-20-7-2-w33-route-compiler.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "interaction_contract": "primitive two-qutrit operation is local iff its two 240-edge carrier qutrits share a W33 point",
        "optimizer_winner": {
            "label": c["winner"]["label"],
            "fixed_minor_columns_0_indexed": c["winner"]["fixed_minor"],
            "score": c["winner"]["metrics"]["score"],
        },
        "routing": c["metrics"],
        "sample_macro_routes": c["sample"],
        "theorem": "Every two-qutrit SUM_ALPHA/SWAP macro in the selected exact Clifford encoder is replaced by a finite nearest-neighbour program on the W33 edge line graph; every replacement replays to the original GF(3) linear action and the reported cycle schedule is carrier-conflict-free.",
        "boundary": "This closes topological routing on the explicit W33 edge-interaction graph only. It does not prove that a specific optical coupler realizes every shared-point primitive with bounded error, loss, crosstalk, or fault spread.",
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2))
    raise SystemExit(0 if out["status"] == "PASS" else 1)
