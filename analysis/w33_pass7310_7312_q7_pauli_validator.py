#!/usr/bin/env python3
"""Exact replay and EDA measurements for Passes 7310--7312.

The packet-owned source object is
``data/PART_W33_PASS7310_Q7_HARDWARE_WITNESS.json``: ``points`` is a 33-by-4
array of integer representatives in GF(7), snapshotted with provenance from the
upstream LNS search certificate.  Hardware checks only the finite symplectic
nonorthogonality predicate.  Nothing here prepares quantum states, proves
maximum cardinality, or models physical dynamics.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "PART_W33_PASS7310_Q7_HARDWARE_WITNESS.json"
FROZEN = ROOT / "data" / "PART_W33_PASS7310_7312_Q7_PAULI_VALIDATOR.json"
RTL = ROOT / "rtl" / "w33_pass7310_7312_q7_pauli_validator.sv"
TB = ROOT / "rtl" / "tb_w33_pass7310_7312_q7_pauli_validator.sv"
GAP_REPLAY = ROOT / "analysis" / "w33_pass7310_7312_q7_pauli_validator.g"
FORMAL_SCRIPT = ROOT / "analysis" / "w33_pass7310_q7_pair_equiv.ys"

POINTS_SHA256 = "c3f1ad38f1283fd4e29583c822aa1bbbd81799f03347e93ffaba25d9cb0647af"
CANONICAL_HISTOGRAM = [0, 88, 90, 94, 90, 90, 76]
RESCALED_HISTOGRAM = [0, 73, 120, 80, 81, 88, 86]
PACKED_HEX = [
    "a08", "648", "888", "a88", "6c8", "588", "881", "b41", "181",
    "889", "ac9", "949", "b49", "011", "059", "cd9", "359", "959",
    "d99", "621", "261", "a61", "4e1", "629", "269", "469", "6a9",
    "ca9", "1a9", "431", "471", "a71", "7b1",
]

EXPECTED_CELLS = {
    "w33_pass7310_pauli_pair_q7_naive": {"SB_CARRY": 262, "SB_LUT4": 528},
    "w33_pass7310_pauli_pair_q7": {"SB_CARRY": 40, "SB_LUT4": 129},
    "w33_pass7311_q7_serial": {
        "SB_CARRY": 63, "SB_DFF": 3, "SB_DFFE": 372,
        "SB_DFFESR": 425, "SB_DFFESS": 1, "SB_DFFSR": 12,
        "SB_DFFSS": 1, "SB_LUT4": 1637,
    },
    "w33_pass7311_q7_bram": {
        "SB_CARRY": 63, "SB_DFF": 5, "SB_DFFESR": 41,
        "SB_DFFESS": 1, "SB_DFFSR": 1, "SB_LUT4": 196,
        "SB_RAM40_4K": 1,
    },
    "w33_pass7311_q7_parallel": {"SB_CARRY": 21120, "SB_LUT4": 58462},
}

BOUNDARY = (
    "Finite GF(7) Weyl-Heisenberg commutator certificate validator only; "
    "not a maximality proof, quantum state preparation, quantum dynamics, "
    "energy or mass model, continuum theory, power measurement, or device result."
)


def temporary_directory(prefix: str) -> tempfile.TemporaryDirectory[str]:
    """Keep WSL EDA scratch off a Windows TEMP mount unless explicitly overridden."""
    requested = os.environ.get("W33_TMPDIR")
    scratch = Path(requested) if requested else (Path("/tmp") if os.name != "nt" else None)
    if scratch is not None:
        scratch.mkdir(parents=True, exist_ok=True)
    return tempfile.TemporaryDirectory(prefix=prefix, dir=str(scratch) if scratch else None)


def symplectic(x: list[int], y: list[int]) -> int:
    return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % 7


def histogram(points: list[list[int]]) -> list[int]:
    out = [0] * 7
    for i, x in enumerate(points):
        for y in points[i + 1 :]:
            out[symplectic(x, y)] += 1
    return out


def pack(point: list[int]) -> int:
    return sum(value << (3 * index) for index, value in enumerate(point))


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(value, separators=(",", ":"), ensure_ascii=True).encode()
    return hashlib.sha256(payload).hexdigest()


def validate_source() -> tuple[list[list[int]], dict[str, Any]]:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    points = source["points"]
    assert source["q"] == 7 and source["size"] == 33
    assert source["encoding"] == "GF(7)"
    assert len(points) == 33
    assert all(len(p) == 4 and any(p) and all(0 <= x < 7 for x in p) for p in points)
    assert canonical_json_sha256(points) == POINTS_SHA256
    canonical = histogram(points)
    rescaled = [
        [(((i % 6) + 1) * x) % 7 for x in point]
        for i, point in enumerate(points)
    ]
    scaled = histogram(rescaled)
    packed = [f"{pack(point):03x}" for point in points]
    assert canonical == CANONICAL_HISTOGRAM
    assert scaled == RESCALED_HISTOGRAM
    assert canonical[0] == scaled[0] == 0
    assert sum(canonical) == sum(scaled) == 528
    assert packed == PACKED_HEX
    result = {
        "source": str(SOURCE.relative_to(ROOT)),
        "source_points_sha256": canonical_json_sha256(points),
        "q": 7,
        "points": 33,
        "pairs": 528,
        "canonical_histogram": canonical,
        "rescaled_histogram": scaled,
        "packed_hex": packed,
        "zero_count_invariant": True,
    }
    return points, result


def validate_projective_stabilizer(points: list[list[int]]) -> dict[str, int]:
    """Apply Pass 7215's exhaustive scalar method to this exact snapshot."""
    analysis_path = str(ROOT / "analysis")
    if analysis_path not in sys.path:
        sys.path.insert(0, analysis_path)
    from w33_pass7187_q9_orbit_attack import Field, geometry
    from w33_pass7214_involution_real_fixed import LA, graph_autos
    from w33_pass7215_involution_exhaustive import realise_exhaustive

    field = Field(7)
    linear = LA(field)
    projective_points, index, adjacency, form = geometry(field)
    carrier = sorted(index[tuple(point)] for point in points)
    carrier_set = set(carrier)
    outside_counts = {
        x: len(adjacency[x] & carrier_set)
        for x in range(len(projective_points)) if x not in carrier_set
    }
    colours: dict[tuple[int, int], tuple[int, ...]] = {}
    for i in range(len(carrier)):
        for j in range(i + 1, len(carrier)):
            common = adjacency[carrier[i]] & adjacency[carrier[j]]
            colours[(i, j)] = tuple(sorted(outside_counts.get(x, -1) for x in common))
    automorphisms = graph_autos(len(carrier), colours)
    nontrivial = [
        permutation for permutation in automorphisms
        if any(permutation[i] != i for i in range(len(carrier)))
    ]
    fixed_selected = [
        sum(permutation[i] == i for i in range(len(carrier)))
        for permutation in nontrivial
    ]
    realised_matrices = [
        matrix for permutation in nontrivial
        if (matrix := realise_exhaustive(
            field, linear, projective_points, index, form, carrier,
            permutation, len(projective_points),
        )) is not None
    ]
    # PCSp is larger than PSp.  A projective similitude represented by M lies
    # in PSp exactly when its multiplier is a square, since a scalar rescaling
    # changes the multiplier by a square.  At q=7 the one realised involution
    # has nonsquare multiplier: it preserves commuting versus noncommuting but
    # is not a standard Clifford/PSp symmetry.
    gram = tuple(tuple(
        1 if (i, j) in ((0, 1), (2, 3)) else
        field.neg[1] if (i, j) in ((1, 0), (3, 2)) else 0
        for j in range(4)
    ) for i in range(4))
    transpose = lambda matrix: tuple(tuple(matrix[j][i] for j in range(4)) for i in range(4))
    nonzero_squares = {field.mul[a][a] for a in range(1, 7)}
    multiplier_is_square = []
    for matrix in realised_matrices:
        transformed = linear.mul(transpose(matrix), linear.mul(gram, matrix))
        multiplier_is_square.append(transformed[0][1] in nonzero_squares)
    psp_realised = sum(multiplier_is_square)
    result = {
        "coloured_graph_automorphism_order": len(automorphisms),
        "nontrivial_automorphisms": len(nontrivial),
        "pcsp_similitudes_realised": len(realised_matrices),
        "psp_clifford_symmetries_realised": psp_realised,
        "nontrivial_pcsp_multiplier_is_square": multiplier_is_square,
        "nontrivial_pcsp_fixed_selected_points": fixed_selected,
        "projective_psp_stabilizer_order": psp_realised + 1,
        "projective_pcsp_stabilizer_order": len(realised_matrices) + 1,
        "exact_pcsp_orbit_seeds_for_33_points": (33 + fixed_selected[0]) // 2,
    }
    assert result == {
        "coloured_graph_automorphism_order": 2,
        "nontrivial_automorphisms": 1,
        "pcsp_similitudes_realised": 1,
        "psp_clifford_symmetries_realised": 0,
        "nontrivial_pcsp_multiplier_is_square": [False],
        "nontrivial_pcsp_fixed_selected_points": [1],
        "projective_psp_stabilizer_order": 1,
        "projective_pcsp_stabilizer_order": 2,
        "exact_pcsp_orbit_seeds_for_33_points": 17,
    }
    return result


def executable(*names: str) -> str:
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    roots = [os.environ.get("W33_EDA_ROOT"), str(Path.home() / ".local" / "eda")]
    for root_string in roots:
        if not root_string:
            continue
        root = Path(root_string)
        for name in names:
            candidate = root / "usr" / "bin" / name
            if candidate.is_file():
                return str(candidate)
    raise RuntimeError(f"required executable not found: {' or '.join(names)}")


def tool_environment(exe: str) -> tuple[dict[str, str], Path | None]:
    env = os.environ.copy()
    path = Path(exe).resolve()
    root = None
    if path.parent.name == "bin" and path.parent.parent.name == "usr":
        root = path.parent.parent.parent
        lib = root / "usr" / "lib" / "x86_64-linux-gnu"
        share = root / "usr" / "share" / "yosys"
        env["LD_LIBRARY_PATH"] = str(lib) + (
            ":" + env["LD_LIBRARY_PATH"] if env.get("LD_LIBRARY_PATH") else ""
        )
        if share.is_dir():
            env["YOSYS_DATDIR"] = str(share)
    return env, root


def run(command: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
        timeout: int = 900) -> str:
    completed = subprocess.run(
        command, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if completed.returncode:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n"
            f"{completed.stdout[-8000:]}"
        )
    return completed.stdout


def replay_gap() -> dict[str, Any]:
    gap = executable("gap")
    output = run([gap, "-q", str(GAP_REPLAY)])
    record = json.loads(next(line for line in output.splitlines() if line.startswith("{")))
    assert record["canonical_histogram"] == CANONICAL_HISTOGRAM
    assert record["rescaled_histogram"] == RESCALED_HISTOGRAM
    assert record["pairs"] == 528 and record["all_pass"] is True
    return record


def simulate() -> dict[str, Any]:
    iverilog = executable("iverilog")
    vvp = executable("vvp")
    env, root = tool_environment(iverilog)
    with temporary_directory(prefix="w33_pass7310_sim_") as temp:
        image = Path(temp) / "validator.vvp"
        compile_command = [
            iverilog, "-g2012", "-s", "tb_w33_pass7310_7312_q7_pauli_validator",
            "-o", str(image), str(RTL), str(TB),
        ]
        vvp_command = [vvp, str(image)]
        if root is not None:
            ivl_dirs = list((root / "usr" / "lib").glob("*/ivl"))
            if ivl_dirs:
                compile_command[1:1] = ["-B", str(ivl_dirs[0])]
                vvp_command[1:1] = ["-M", str(ivl_dirs[0])]
        run(compile_command, env=env)
        output = run(vvp_command, env=env)
    marker = "PASS7310-7312: exact accepted, duplicate rejected, 528 pairs, cycles 562/1618"
    assert marker in output
    return {"marker": marker, "register_cycles": 562, "bram_cycles": 1618}


def synthesize(tops: list[str]) -> tuple[dict[str, dict[str, int]], dict[str, Path], str]:
    yosys = executable("yosys")
    env, _ = tool_environment(yosys)
    version = run([yosys, "-V"], env=env).strip()
    results: dict[str, dict[str, int]] = {}
    json_paths: dict[str, Path] = {}
    # The caller consumes the temporary JSONs before this context exits.
    temp = temporary_directory(prefix="w33_pass7310_synth_")
    setattr(synthesize, "_temp", temp)
    temp_path = Path(temp.name)
    for top in tops:
        netlist = temp_path / f"{top}.json"
        # Yosys tokenizes the -p script itself, so an absolute repository path
        # containing spaces would be split even though subprocess received one argv.
        rtl_relative = RTL.relative_to(ROOT).as_posix()
        command = (
            f"read_verilog -sv {rtl_relative}; synth_ice40 -top {top} -json {netlist}"
        )
        run([yosys, "-Q", "-q", "-p", command], env=env, timeout=900)
        module = json.loads(netlist.read_text(encoding="utf-8"))["modules"][top]
        cells = collections.Counter(cell["type"] for cell in module.get("cells", {}).values())
        results[top] = dict(sorted(cells.items()))
        assert results[top] == EXPECTED_CELLS[top], (top, results[top])
        json_paths[top] = netlist
    return results, json_paths, version


def prove_formal() -> dict[str, Any]:
    yosys = executable("yosys")
    env, _ = tool_environment(yosys)
    output = run([yosys, "-Q", "-s", str(FORMAL_SCRIPT)], env=env, timeout=300)
    assert "SAT proof finished - no model found: SUCCESS!" in output
    matches = re.findall(r"Solving problem with (\d+) variables and (\d+) clauses", output)
    assert matches
    variables, clauses = map(int, matches[-1])
    return {
        "unconstrained_input_bits": 24,
        "assignments_covered": 1 << 24,
        "variables": variables,
        "clauses": clauses,
        "status": "SUCCESS",
    }


def place_and_route(json_paths: dict[str, Path]) -> dict[str, Any]:
    nextpnr = executable("nextpnr-ice40", "yowasp-nextpnr-ice40")
    version = run([nextpnr, "--version"]).strip()
    results: dict[str, Any] = {"tool": version, "device": "iCE40HX8K-CT256", "seed": 7310}
    for top in ("w33_pass7311_q7_serial", "w33_pass7311_q7_bram"):
        netlist = json_paths[top]
        asc = netlist.parent / f"{top}.asc"
        output = run([
            nextpnr, "--hx8k", "--package", "ct256", "--json", netlist.name,
            "--asc", asc.name, "--pcf-allow-unconstrained", "--seed", "7310",
            "--freq", "12",
        ], cwd=netlist.parent, timeout=600)
        lc = int(re.search(r"ICESTORM_LC:\s+(\d+)/", output).group(1))
        ram = int(re.search(r"ICESTORM_RAM:\s+(\d+)/", output).group(1))
        frequencies = re.findall(r"Max frequency .*?: ([0-9.]+) MHz", output)
        assert frequencies and "Program finished normally." in output
        results[top] = {
            "logic_cells": lc,
            "block_rams": ram,
            "final_fmax_mhz": float(frequencies[-1]),
        }
    assert results["w33_pass7311_q7_serial"] == {
        "logic_cells": 2439, "block_rams": 0, "final_fmax_mhz": 31.80,
    }
    assert results["w33_pass7311_q7_bram"] == {
        "logic_cells": 230, "block_rams": 1, "final_fmax_mhz": 41.31,
    }
    return results


def validate_frozen(result: dict[str, Any]) -> None:
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert frozen["schema"] == "w33.pass7310_7312.q7_pauli_validator.v1"
    exact = frozen["exact_certificate"]
    for key in (
        "source", "source_points_sha256", "q", "points", "pairs",
        "canonical_histogram", "rescaled_histogram", "packed_hex",
        "zero_count_invariant",
    ):
        assert exact[key] == result[key], key
    assert frozen["boundary"] == BOUNDARY


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gap", action="store_true", help="run native GAP replay")
    parser.add_argument("--simulate", action="store_true", help="run Icarus replay")
    parser.add_argument("--formal", action="store_true", help="run universal Yosys SAT proof")
    parser.add_argument("--stabilizer", action="store_true", help="replay typed PSp and PCSp stabilizers")
    parser.add_argument("--synthesize", action="store_true", help="rerun four quick iCE40 syntheses")
    parser.add_argument("--place-route", action="store_true", help="run seeded HX8K place and route")
    parser.add_argument("--full-synthesis", action="store_true", help="also synthesize the 528-core parallel endpoint")
    parser.add_argument("--all", action="store_true", help="run GAP, simulation, formal, synthesis, and place-route")
    args = parser.parse_args()
    if args.all:
        args.gap = args.simulate = args.formal = args.stabilizer = args.synthesize = args.place_route = True
    if args.full_synthesis:
        args.synthesize = True

    points, exact = validate_source()
    validate_frozen(exact)
    result: dict[str, Any] = {"exact_certificate": exact, "boundary": BOUNDARY}
    if args.gap:
        result["gap"] = replay_gap()
    if args.simulate:
        result["simulation"] = simulate()
    if args.stabilizer:
        result["projective_stabilizer"] = validate_projective_stabilizer(points)
    json_paths: dict[str, Path] = {}
    if args.synthesize or args.place_route:
        tops = [
            "w33_pass7310_pauli_pair_q7_naive",
            "w33_pass7310_pauli_pair_q7",
            "w33_pass7311_q7_serial",
            "w33_pass7311_q7_bram",
        ]
        if args.full_synthesis:
            tops.append("w33_pass7311_q7_parallel")
        result["synthesis"], json_paths, result["yosys_version"] = synthesize(tops)
    if args.formal:
        result["formal"] = prove_formal()
    if args.place_route:
        result["place_and_route"] = place_and_route(json_paths)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
