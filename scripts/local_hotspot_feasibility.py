#!/usr/bin/env python3
"""Check local feasibility for hotspot edges by forcing particular root assignments and solving a restricted CP-SAT model.

Usage: py -3 scripts/local_hotspot_feasibility.py --edges 37 38 --k 80 --radius 1 --time-limit 10
Writes checks/PART_CVII_local_hotspot_feasibility_<edges>_<ts>.json

New flags:
  --offset N    Start index into the pair list (deterministic, resumable batching)
  --limit N     Deterministic limit of tests to run starting at --offset (0 means no limit)

Notes:
  - The script will detect OR-Tools import/linker problems (e.g., missing helper DLLs such as utf8_validity.dll) and will write an explicit 'ERROR_MISSING_DLL' error into the output JSON when detected.
  - Use --dump-candidates to only write candidates and exit without running CP-SAT.
"""
from __future__ import annotations

import argparse
import importlib
import json
import logging
import os
import sys
import time
import traceback
from collections import defaultdict
from pathlib import Path

import numpy as np


def ortools_import_check():
    """Attempt to import OR-Tools CP-SAT. Returns (ok:bool, message:str)."""
    try:
        # Try importing the CP-SAT model to trigger any DLL/linker errors
        import ortools  # type: ignore
        from ortools.sat.python import cp_model  # type: ignore

        return True, None
    except Exception as exc:
        msg = str(exc)
        logging.exception("OR-Tools import failed: %s", msg)
        # Detect known missing helper DLL pattern (Windows wheels)
        low = msg.lower()
        if (
            "utf8_validity.dll" in low
            or ".libs" in low
            or "cannot find" in low
            or "dll" in low
        ):
            return False, f"MISSING_DLL: {msg}"
        return False, f"IMPORT_ERROR: {msg}"


# local helper copies (to avoid module import issues)


def generate_scaled_e8_roots() -> list:
    roots = set()
    for i in range(8):
        for j in range(i + 1, 8):
            for si in (-2, 2):
                for sj in (-2, 2):
                    v = [0] * 8
                    v[i] = si
                    v[j] = sj
                    roots.add(tuple(v))
    from itertools import product

    for signs in product((-1, 1), repeat=8):
        if sum(1 for s in signs if s < 0) % 2 == 0:
            roots.add(tuple(int(s) for s in signs))
    roots_list = sorted(list(roots))
    assert len(roots_list) == 240
    return roots_list


def build_w33_graph():
    F = 3
    all_vectors = [
        (a, b, c, d)
        for a in range(F)
        for b in range(F)
        for c in range(F)
        for d in range(F)
        if (a, b, c, d) != (0, 0, 0, 0)
    ]

    def canonical_rep(v):
        for i in range(4):
            if v[i] % F != 0:
                a = v[i] % F
                inv = 1 if a == 1 else 2
                return tuple(((x * inv) % F) for x in v)
        return None

    reps = set(canonical_rep(v) for v in all_vectors if canonical_rep(v))
    vertices = sorted(list(reps))

    def symp(x, y):
        return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % F

    n = len(vertices)
    adj = [[] for _ in range(n)]
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if symp(vertices[i], vertices[j]) == 0:
                adj[i].append(j)
                adj[j].append(i)
                edges.append((i, j))
    return n, vertices, adj, edges


def compute_embedding_matrix():
    n, vertices, adj, edges = build_w33_graph()
    A = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in adj[i]:
            A[i, j] = 1.0
    vals, vecs = np.linalg.eigh(A)
    idx = np.argsort(vals)[::-1]
    vals = vals[idx]
    vecs = vecs[:, idx]
    idxs_2 = [i for i, v in enumerate(vals) if abs(v - 2.0) < 1e-6]
    if len(idxs_2) >= 8:
        chosen = idxs_2[:8]
    else:
        chosen = list(range(1, 9))
    X = vecs[:, chosen]
    X = X - X.mean(axis=0)
    X = X / (X.std(axis=0) + 1e-12)
    return X, edges


def enumerate_triangles(n: int, adj):
    tris = []
    for a in range(n):
        for b in adj[a]:
            if b <= a:
                continue
            for c in adj[b]:
                if c <= b:
                    continue
                if a in adj[c]:
                    tri = tuple(sorted((a, b, c)))
                    if tri not in tris:
                        tris.append(tri)
    return tris


def build_local_model(hot_edges, radius, K):
    try:
        from ortools.sat.python import cp_model
    except Exception as exc:
        err = f"Error importing ortools.cp_model: {exc}\n" + traceback.format_exc()
        print(err, flush=True)
        logging.exception("Failed to import ortools.cp_model")
        raise
    X, edges = compute_embedding_matrix()
    roots = generate_scaled_e8_roots()
    roots_arr = np.array(roots, dtype=int)
    roots_unit = roots_arr.astype(float) / np.linalg.norm(
        roots_arr.astype(float), axis=1, keepdims=True
    )
    N_edges = len(edges)
    # compute candidate roots for each edge
    cost = np.linalg.norm(
        build_edge_vectors(X, edges)[:, None, :] - roots_unit[None, :, :], axis=2
    )
    candidates = {e: list(np.argsort(cost[e])[:K]) for e in range(N_edges)}
    # build involved edges (BFS over vertices)
    edge_to_vertices = {i: edges[i] for i in range(N_edges)}
    involved_edges = set()
    involved_vertices = set()
    for e in hot_edges:
        involved_edges.add(e)
        i, j = edge_to_vertices[e]
        involved_vertices.add(i)
        involved_vertices.add(j)
    if radius > 0:
        # include edges incident to vertices within radius steps
        # simple radius expansion: add edges sharing vertices
        frontier = set(involved_vertices)
        for _ in range(radius):
            new_frontier = set(frontier)
            for ei, (a, b) in edge_to_vertices.items():
                if a in frontier or b in frontier:
                    involved_edges.add(ei)
                    new_frontier.add(a)
                    new_frontier.add(b)
            frontier = new_frontier
    # build model
    model = cp_model.CpModel()
    bvars = {}
    for e in sorted(involved_edges):
        for r in candidates[e]:
            bvars[(e, r)] = model.NewBoolVar(f"b_e{e}_r{r}")
    # per-edge assign
    for e in sorted(involved_edges):
        model.Add(sum(bvars[(e, r)] for r in candidates[e]) == 1)
    # root uniqueness
    root_map = defaultdict(list)
    for (e, r), v in bvars.items():
        root_map[r].append(v)
    for r, vs in root_map.items():
        model.Add(sum(vs) <= 1)
    # triangle constraints restricted to edges subset
    n, vertices, adj, edges_all = build_w33_graph()
    triangles = enumerate_triangles(n, adj)
    edge_index = {edges_all[i]: i for i in range(len(edges_all))}
    for a, b, c in triangles:
        e_ab = (
            edge_index.get((a, b)) if (a, b) in edge_index else edge_index.get((b, a))
        )
        e_bc = (
            edge_index.get((b, c)) if (b, c) in edge_index else edge_index.get((c, b))
        )
        e_ac = (
            edge_index.get((a, c)) if (a, c) in edge_index else edge_index.get((c, a))
        )
        if e_ab in involved_edges and e_bc in involved_edges and e_ac in involved_edges:
            for t in range(8):
                expr = []
                for r in candidates[e_ab]:
                    if (e_ab, r) in bvars:
                        expr.append((bvars[(e_ab, r)], int(roots[r][t])))
                for r in candidates[e_bc]:
                    if (e_bc, r) in bvars:
                        expr.append((bvars[(e_bc, r)], int(roots[r][t])))
                for r in candidates[e_ac]:
                    if (e_ac, r) in bvars:
                        expr.append((bvars[(e_ac, r)], -int(roots[r][t])))
                if expr:
                    model.Add(sum(coeff * var for (var, coeff) in expr) == 0)
    return model, bvars, candidates, sorted(involved_edges)


def build_edge_vectors(X, edges):
    E = []
    for i, j in edges:
        v = X[i] - X[j]
        nv = np.linalg.norm(v)
        if nv > 0:
            E.append(v / nv)
        else:
            E.append(v)
    return np.vstack(E)


def slice_pairs(pairs, offset=0, limit=0):
    """Return deterministic slice of pairs for batching/resume."""
    total = len(pairs)
    start = int(offset)
    if start >= total:
        return []
    end = None if int(limit) == 0 else start + int(limit)
    return pairs[start:end]


def test_forced_pairs(edges, pairs_to_test, radius, K, time_limit, num_workers=8):
    try:
        from ortools.sat.python import cp_model
    except Exception as exc:
        err = (
            f"Error importing ortools.cp_model in test_forced_pairs: {exc}\n"
            + traceback.format_exc()
        )
        print(err, flush=True)
        logging.exception("Failed to import ortools.cp_model in test_forced_pairs")
        raise
    model, bvars, candidates, involved_edges = build_local_model(edges, radius, K)
    results = []
    for e, r in pairs_to_test:
        # clone model? CP-SAT doesn't support cloning; rebuild model each time (cheap for small graphs)
        try:
            model2, bvars2, candidates2, involved_edges2 = build_local_model(
                edges, radius, K
            )
        except Exception:
            results.append(
                {
                    "edge": e,
                    "root": r,
                    "status": "ERROR_BUILD_MODEL",
                    "error": traceback.format_exc(),
                }
            )
            continue
        if (e, r) not in bvars2:
            results.append({"edge": e, "root": r, "status": "UNVERIFIED_NOT_IN_CAND"})
            continue
        model2.Add(bvars2[(e, r)] == 1)
        try:
            solver = cp_model.CpSolver()
            solver.parameters.max_time_in_seconds = float(time_limit)
            solver.parameters.num_search_workers = int(num_workers)
            st = solver.Solve(model2)
            status_name = solver.StatusName(st)
            results.append({"edge": e, "root": r, "status": status_name})
        except Exception:
            results.append(
                {
                    "edge": e,
                    "root": r,
                    "status": "ERROR",
                    "error": traceback.format_exc(),
                }
            )
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--edges", type=int, nargs="+", required=True)
    parser.add_argument("--k", type=int, default=80)
    parser.add_argument("--radius", type=int, default=1)
    parser.add_argument("--time-limit", type=int, default=10)
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Number of OR-Tools search workers to use",
    )
    parser.add_argument(
        "--max-tests",
        type=int,
        default=0,
        help="Limit number of pair tests; 0 means no limit (random sampling)",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Start index into pairs list for deterministic, resumable batches",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Deterministic limit of tests to run starting at offset; 0 means no limit",
    )
    parser.add_argument(
        "--dump-candidates",
        action="store_true",
        help="Write candidates to checks file for inspection",
    )
    parser.add_argument(
        "--log-dir", default="checks", help="Directory to write logs/results"
    )
    parser.add_argument("--seed", type=int, default=212)
    parser.add_argument(
        "--check-ortools",
        action="store_true",
        help="Only check ortools cp_model import and exit",
    )
    args = parser.parse_args()

    ts = int(time.time())
    out_dir = Path(args.log_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    logfile = (
        out_dir
        / f'PART_CVII_local_hotspot_feasibility_{"_".join(map(str,args.edges))}_{ts}.log'
    )
    logging.basicConfig(
        filename=str(logfile),
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s: %(message)s",
    )
    # also log to stdout for interactive debugging
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
    logging.getLogger().addHandler(ch)
    print(
        f"Starting local_hotspot_feasibility with edges={args.edges} k={args.k} radius={args.radius} time_limit={args.time_limit} (ts={ts})",
        flush=True,
    )
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Working dir: {os.getcwd()}")
    logging.info("Starting local_hotspot_feasibility with args=%s", args)
    if args.check_ortools:
        try:
            from ortools.sat.python import cp_model

            print("ortools import OK", flush=True)
            logging.info("ortools import OK")
            sys.exit(0)
        except Exception as exc:
            print("ortools import FAILED:", exc, flush=True)
            logging.exception("ortools import FAILED in --check-ortools")
            sys.exit(2)

    # Defer the OR-Tools import check until after candidate generation and slicing so
    # offset-only invocations that produce empty batches can exit successfully
    # compute candidates and iterate over candidate pairs for the hotspot edges
    X, edges_list = compute_embedding_matrix()
    roots = generate_scaled_e8_roots()
    # build candidates (same as build_local_model uses)
    E_mat = build_edge_vectors(X, edges_list)
    roots_arr = np.array(roots, dtype=int)
    roots_unit = roots_arr.astype(float) / np.linalg.norm(
        roots_arr.astype(float), axis=1, keepdims=True
    )
    cost = np.linalg.norm(E_mat[:, None, :] - roots_unit[None, :, :], axis=2)
    candidates = {
        e: list(np.argsort(cost[e])[: args.k]) for e in range(len(edges_list))
    }

    # report candidate counts for hotspot edges
    for e in args.edges:
        print(f"edge {e} candidates: {len(candidates.get(e, []))}", flush=True)
    if args.dump_candidates:
        cand_file = (
            out_dir
            / f'PART_CVII_local_hotspot_candidates_{"_".join(map(str,args.edges))}_{ts}.json'
        )
        # ensure indices are native Python ints for JSON serialization
        cand_dump = {
            str(e): [int(x) for x in candidates.get(e, [])] for e in args.edges
        }
        cand_file.write_text(json.dumps(cand_dump, indent=2), encoding="utf-8")
        print(f"Wrote candidates to {cand_file}", flush=True)
        logging.info("Wrote candidates to %s", cand_file)
        print("Dump-only: exiting without running CP-SAT tests", flush=True)
        sys.exit(0)

    # build list of pairs to test: cartesian product of candidate roots for each hotspot edge
    import random
    from itertools import product

    random.seed(args.seed)
    first_edge = args.edges[0]
    if len(args.edges) == 1:
        pairs = [(first_edge, r) for r in candidates[first_edge]]
    else:
        second_edge = args.edges[1]
        pairs = [
            (first_edge, r1, second_edge, r2)
            for r1, r2 in product(candidates[first_edge], candidates[second_edge])
        ]
    # deterministic slicing (offset, limit) for resumable batches
    start = int(args.offset)
    if start >= len(pairs):
        print(
            f"Offset {start} >= number of pairs {len(pairs)}; nothing to test",
            flush=True,
        )
        pairs = []
    else:
        end = None if int(args.limit) == 0 else start + int(args.limit)
        pairs = pairs[start:end]
        print(
            f"Using deterministic slice offset={start} limit={args.limit} -> {len(pairs)} pairs",
            flush=True,
        )

    # apply max-tests limit if requested (random sampling)
    if args.max_tests and len(pairs) > args.max_tests:
        import random

        pairs = random.sample(pairs, args.max_tests)
        print(
            f"Truncated pairs to {len(pairs)} using --max-tests={args.max_tests}",
            flush=True,
        )

    outp_stem = f'PART_CVII_local_hotspot_feasibility_{"_".join(map(str,args.edges))}'
    if args.offset or args.limit:
        outp = out_dir / f"{outp_stem}_offset{args.offset}_limit{args.limit}_{ts}.json"
    else:
        outp = out_dir / f"{outp_stem}_{ts}.json"
    results = {
        "edges": args.edges,
        "k": args.k,
        "radius": args.radius,
        "time_limit": args.time_limit,
        "batch_offset": int(args.offset),
        "batch_limit": int(args.limit),
        "tests": [],
    }

    # quick ortools import check to fail fast on missing helper DLLs (avoid long runs)
    if pairs:
        try:
            from ortools.sat.python import cp_model  # type: ignore
        except Exception as exc:
            msg = str(exc)
            err_type = (
                "ERROR_MISSING_DLL"
                if ("utf8_validity.dll" in msg or ".libs" in msg)
                else "ERROR_IMPORT"
            )
            err = f"{err_type}: {msg}\n{traceback.format_exc()}"
            print("Ortools import failed:", err, flush=True)
            logging.exception("Ortools import failed before testing pairs")
            results["error"] = err
            try:
                outp.write_text(json.dumps(_make_json_serializable(results, encoding="utf-8"), indent=2),
                    encoding="utf-8",
                )
                print("Wrote error results to", outp, flush=True)
            except Exception:
                logging.exception(
                    "Failed to write error outp for ortools import failure"
                )
            sys.exit(2)
    else:
        print(
            "No pairs to test after slicing; skipping OR-Tools import check", flush=True
        )

    if len(args.edges) == 1:
        try:
            single_results = test_forced_pairs(
                [first_edge],
                [(first_edge, r) for r in candidates[first_edge]],
                args.radius,
                args.k,
                args.time_limit,
                num_workers=args.workers,
            )
            results["tests"] = single_results
        except Exception:
            err = traceback.format_exc()
            print("test_forced_pairs failed:", err, flush=True)
            logging.exception("test_forced_pairs failed")
            results["error"] = err
    else:
        # test each pair
        total = len(pairs)
        for idx, (e1, r1, e2, r2) in enumerate(pairs, start=1):
            if idx % 50 == 0 or idx == 1:
                print(
                    f"Testing pair {idx}/{total} (edge {e1} root {r1}  vs edge {e2} root {r2})",
                    flush=True,
                )
                logging.info("Testing pair %d/%d: %s", idx, total, (e1, r1, e2, r2))
            try:
                model, bvars, cand, involved = build_local_model(
                    args.edges, args.radius, args.k
                )
                # ensure both edges are present in model
                if (e1, r1) not in bvars or (e2, r2) not in bvars:
                    results["tests"].append(
                        {"pair": [e1, r1, e2, r2], "status": "NOT_IN_MODEL"}
                    )
                    continue
                model.Add(bvars[(e1, r1)] == 1)
                model.Add(bvars[(e2, r2)] == 1)
                try:
                    from ortools.sat.python import cp_model
                except Exception as exc:
                    msg = str(exc)
                    if "utf8_validity.dll" in msg or ".libs" in msg:
                        err = f"ERROR_MISSING_DLL: {msg}\n" + traceback.format_exc()
                        print("Ortools missing DLL detected:", err, flush=True)
                        logging.exception("Ortools missing DLL in pair loop")
                        results["tests"].append(
                            {
                                "pair": [e1, r1, e2, r2],
                                "status": "ERROR_MISSING_DLL",
                                "error": err,
                            }
                        )
                        # Stop further testing to avoid repeating errors
                        break
                    else:
                        err = (
                            f"Error importing ortools.cp_model in pair loop: {exc}\n"
                            + traceback.format_exc()
                        )
                        print(err, flush=True)
                        logging.exception("ortools import failed in pair loop")
                        results["tests"].append(
                            {
                                "pair": [e1, r1, e2, r2],
                                "status": "ERROR_IMPORT",
                                "error": err,
                            }
                        )
                        continue
                solver = cp_model.CpSolver()
                solver.parameters.max_time_in_seconds = float(args.time_limit)
                solver.parameters.num_search_workers = int(args.workers)
                try:
                    st = solver.Solve(model)
                    status_name = solver.StatusName(st)
                    results["tests"].append(
                        {"pair": [e1, r1, e2, r2], "status": status_name}
                    )
                except Exception as exc:
                    err = traceback.format_exc()
                    print(
                        f"Exception during solver.Solve for pair {e1,r1,e2,r2}: {err}",
                        flush=True,
                    )
                    logging.exception(
                        "Solver.Solve failed for pair %s: %s", (e1, r1, e2, r2), exc
                    )
                    lower = str(exc).lower()
                    if (
                        "utf8_validity.dll" in lower
                        or ".libs" in lower
                        or "cannot find" in lower
                        or "dll" in lower
                    ):
                        results["tests"].append(
                            {
                                "pair": [e1, r1, e2, r2],
                                "status": "ERROR_MISSING_DLL",
                                "error": err,
                            }
                        )
                        outp.write_text(json.dumps(_make_json_serializable(results, encoding="utf-8"), indent=2),
                            encoding="utf-8",
                        )
                        print(
                            "ORTOOLS MISSING DLL detected during Solve; wrote partial results to",
                            outp,
                            flush=True,
                        )
                        logging.error(
                            "ORTOOLS MISSING DLL detected during Solve; aborting pair tests"
                        )
                        sys.exit(2)
                    else:
                        results["tests"].append(
                            {
                                "pair": [e1, r1, e2, r2],
                                "status": "ERROR_SOLVE",
                                "error": err,
                            }
                        )
            except Exception:
                err = traceback.format_exc()
                print(
                    f"Exception building model or testing pair {e1,r1,e2,r2}: {err}",
                    flush=True,
                )
                logging.exception("Error in pair test for %s", (e1, r1, e2, r2))
                results["tests"].append(
                    {"pair": [e1, r1, e2, r2], "status": "ERROR", "error": err}
                )

    def _make_json_serializable(o):
        # Recursively convert numpy types to Python built-ins suitable for json.dumps
        if isinstance(o, dict):
            return {
                (str(k) if not isinstance(k, str) else k): _make_json_serializable(v)
                for k, v in o.items()
            }
        if isinstance(o, list):
            return [_make_json_serializable(v) for v in o]
        if isinstance(o, tuple):
            return tuple(_make_json_serializable(v) for v in o)
        try:
            import numpy as _np

            if isinstance(o, _np.integer):
                return int(o)
            if isinstance(o, _np.floating):
                return float(o)
            if isinstance(o, _np.bool_):
                return bool(o)
            if isinstance(o, _np.ndarray):
                return _make_json_serializable(o.tolist())
        except Exception:
            pass
        return o

    try:
        safe_results = _make_json_serializable(results)
        outp.write_text(json.dumps(safe_results, indent=2), encoding="utf-8")
        print("Wrote", outp, flush=True)
    except Exception:
        err = traceback.format_exc()
        print("Failed to write results file:", err, flush=True)
        logging.exception("Failed to write results file")
        # attempt to write to a fallback file in current dir
        try:
            fallback = Path(f"local_hotspot_fallback_{ts}.json")
            fallback.write_text(json.dumps(_make_json_serializable(results, encoding="utf-8"), indent=2), encoding="utf-8"
            )
            print("Wrote fallback results to", fallback, flush=True)
        except Exception:
            print("Also failed to write fallback results", flush=True)


if __name__ == "__main__":
    main()
