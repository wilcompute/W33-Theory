#!/usr/bin/env python3
"""Run an iterative campaign of local CP-SAT patches to incrementally increase triangle exact matches.

Workflow:
 - Start from a base bijection JSON
 - Create a seed from it
 - For each start vertex (or random sample), run local CP-SAT
 - If it produces an assignment that increases overall exact triangle count, apply it and update bijection/seed
 - Repeat until a full pass yields no improvements or max_iter reached
"""
from __future__ import annotations

import argparse
import json
import os
import random
import subprocess
import time
from pathlib import Path

from e8_embedding_group_theoretic import build_w33, generate_e8_roots
from optimize_bijection_cocycle import build_triangles, triangle_exact


def run_local(seed_json, start_vertex, edge_limit, k, time_limit, seed, seed_reward):
    cmd = [
        "py",
        "-3",
        "-X",
        "utf8",
        "-u",
        "scripts/solve_e8_embedding_cpsat_local.py",
        "--seed-json",
        seed_json,
        "--start-vertex",
        str(start_vertex),
        "--edge-limit",
        str(edge_limit),
        "--k",
        str(k),
        "--time-limit",
        str(time_limit),
        "--seed",
        str(seed),
        "--seed-reward",
        str(seed_reward),
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bij", default="checks/PART_CVII_e8_bijection.json")
    parser.add_argument("--edge-limit", type=int, default=24)
    parser.add_argument(
        "--edge-sizes",
        type=str,
        default="24",
        help='Comma-separated list of edge sizes to try, e.g., "24,48,72"',
    )
    parser.add_argument("--k", type=int, default=40)
    parser.add_argument("--time-limit", type=float, default=60.0)
    parser.add_argument("--seed", type=int, default=202)
    parser.add_argument("--seed-reward", type=float, default=10000.0)
    parser.add_argument("--max-iter", type=int, default=3)
    parser.add_argument("--random-seed", type=int, default=42)
    parser.add_argument(
        "--auto-commit",
        action="store_true",
        help="Auto-commit intermediate bijection + seed when a patch is applied",
    )
    parser.add_argument(
        "--commit-branch",
        type=str,
        default=None,
        help="Branch name used if push is requested",
    )
    parser.add_argument(
        "--push-commits",
        action="store_true",
        help="Push commits to remote when --auto-commit is used",
    )
    parser.add_argument(
        "--check-collaborator",
        action="store_true",
        help="Run collaborator activity check at end of each iteration",
    )
    args = parser.parse_args()

    bij_path = Path(args.bij)
    if not bij_path.exists():
        raise SystemExit("Bijection file not found")

    n, vertices, adj, edges = build_w33()
    tri_list = build_triangles(n, adj)
    roots = generate_e8_roots()

    # load initial bijection
    current_bij = json.loads(bij_path.read_text(encoding="utf-8"))["bijection"]
    current_bij = {int(k): int(v) for k, v in current_bij.items()}
    current_exact = sum(
        1 for t in tri_list if triangle_exact(roots, current_bij, edges, t)
    )
    print("Initial exact triangles:", current_exact)

    # write initial seed
    seed_file = (
        Path.cwd()
        / "checks"
        / f"PART_CVII_e8_bijection_seed_campaign_{int(time.time())}.json"
    )
    seed_obj = {
        "seed_edges": [
            {"edge_index": int(k), "root_index": int(v)} for k, v in current_bij.items()
        ],
        "rotation": None,
    }
    seed_file.write_text(json.dumps(seed_obj, indent=2), encoding="utf-8")

    start_vertices = list(range(n))
    random.Random(args.random_seed).shuffle(start_vertices)

    iter_no = 0
    improved = True
    expand_sizes = [int(x) for x in args.edge_sizes.split(",")]
    while iter_no < args.max_iter and improved:
        iter_no += 1
        improved = False
        print(f"=== Iter {iter_no} starting, current_exact={current_exact} ===")
        for sv in start_vertices:
            applied = False
            for size in expand_sizes:
                try:
                    run_local(
                        str(seed_file),
                        sv,
                        size,
                        args.k,
                        args.time_limit,
                        args.seed,
                        args.seed_reward,
                    )
                except subprocess.CalledProcessError:
                    print("Local run failed for start vertex", sv, "size", size)
                    continue

                # find latest local result
                from glob import glob

                latest = sorted(
                    glob("checks/PART_CVII_e8_bijection_local_seed_*.json"),
                    key=os.path.getmtime,
                )[-1]
                res = json.loads(open(latest, encoding="utf-8").read())
                status = res.get("status")
                if status != "OPTIMAL" and status != "FEASIBLE":
                    print(
                        "No assignment from local run at vertex",
                        sv,
                        "size",
                        size,
                        "status",
                        status,
                    )
                    continue

                # apply patch
                # update current_bij
                for k, v in res["assignments"].items():
                    current_bij[int(k)] = int(v)

                # recompute exact
                new_exact = sum(
                    1 for t in tri_list if triangle_exact(roots, current_bij, edges, t)
                )
                delta = new_exact - current_exact
                if delta > 0:
                    print(
                        f"Applied local patch at vertex {sv}, size {size}: delta={delta} ({current_exact}->{new_exact})"
                    )
                    current_exact = new_exact
                    improved = True
                    applied = True
                    # update seed file to reflect new bijection
                    seed_obj = {
                        "seed_edges": [
                            {"edge_index": int(k), "root_index": int(v)}
                            for k, v in current_bij.items()
                        ],
                        "rotation": None,
                    }
                    seed_file.write_text(
                        json.dumps(seed_obj, indent=2), encoding="utf-8"
                    )
                    # write an intermediate bijection file
                    stamp = int(time.time())
                    outpath = (
                        Path.cwd()
                        / "checks"
                        / f"PART_CVII_e8_bijection_intermediate_{stamp}.json"
                    )
                    outpath.write_text(json.dumps(
                            {
                                "bijection": {
                                    str(k, encoding="utf-8"): int(v) for k, v in current_bij.items()
                                }
                            },
                            indent=2,
                        ),
                        encoding="utf-8",
                    )

                    # Mirror to tracked artifacts/ to avoid git-ignored checks/
                    artifact_out = Path.cwd() / "committed_artifacts" / outpath.name
                    artifact_out.parent.mkdir(parents=True, exist_ok=True)
                    artifact_out.write_text(json.dumps(
                            {
                                "bijection": {
                                    str(k, encoding="utf-8"): int(v) for k, v in current_bij.items()
                                }
                            },
                            indent=2,
                        ),
                        encoding="utf-8",
                    )
                    print(
                        "Wrote intermediate to",
                        outpath,
                        "and committed artifact",
                        artifact_out,
                    )

                    if getattr(args, "auto_commit", False):
                        try:
                            import git_auto_keep

                            # ensure seed_file exists (it was just re-written above)
                            # write an artifact copy of the seed as well
                            artifact_seed = (
                                Path.cwd() / "committed_artifacts" / seed_file.name
                            )
                            artifact_seed.parent.mkdir(parents=True, exist_ok=True)
                            artifact_seed.write_text(
                                seed_file.read_text(encoding="utf-8"), encoding="utf-8"
                            )

                            files_to_commit = [str(artifact_out), str(artifact_seed)]
                            commit_msg = f"Local patch applied: vertex {sv} size {size} delta {delta} iter {iter_no}"
                            ok, msg = git_auto_keep.git_add_commit(
                                files_to_commit,
                                commit_msg,
                                branch=args.commit_branch,
                                push=args.push_commits,
                            )
                            print("Auto-commit:", ok, msg)
                        except Exception as e:
                            print("Auto-commit failed:", e)

                    break
                else:
                    print(
                        f"Patch at vertex {sv}, size {size} made no improvement (delta={delta})"
                    )
            if applied:
                # move to next start vertex
                continue

        print(f"=== Iter {iter_no} done, current_exact={current_exact} ===")

        if getattr(args, "check_collaborator", False):
            try:
                subprocess.run(
                    ["py", "-3", "-X", "utf8", "scripts/check_collaborator_edits.py"],
                    check=False,
                )
            except Exception as e:
                print("check_collaborator_edits failed:", e)

    # Final write
    stamp = int(time.time())
    outpath = (
        Path.cwd() / "checks" / f"PART_CVII_e8_bijection_campaign_result_{stamp}.json"
    )
    out = {
        "bijection": {str(k): int(v) for k, v in current_bij.items()},
        "final_exact": int(current_exact),
    }
    outpath.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("Wrote campaign result to", outpath)


if __name__ == "__main__":
    main()
