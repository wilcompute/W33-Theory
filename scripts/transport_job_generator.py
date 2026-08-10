"""Generate CNF/OR-Tools job artifacts for the transport CSP solver farm.

This small helper automates exporting CNF files for a list of seeds and
emits a PowerShell runner script that will invoke the repo OR-Tools runner
for each seed with the provided time/workers budget. Run locally inside the
repo venv.

Usage (example):

  python scripts/transport_job_generator.py --seeds 0-7 --time_limit 300 --workers 8

This will produce CNF files under `data/` and a `run_transport_jobs.ps1`
script you can run on Windows. For cluster use, inspect the produced CNFs and
submit them to your preferred SAT farm; a .meta.json file is written by the
CNF exporter for mapping solver output back to assignment variables.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import List


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
DATA = ROOT / "data"


def run_cmd(cmd: List[str]) -> None:
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\nstdout:\n{out}\nstderr:\n{err}")


def export_cnf_for_seed(seed: int, out_base: Path, lexleader: bool = False, lexleader_strong: bool = False, lexleader_prefix_length: int = 8) -> Path:
    outfn = out_base / f"transport_seed{seed}.cnf"
    cmd = [sys.executable, str(SCRIPTS / "transport_csp_cnf_export.py"), "--out", str(outfn), "--seeds", str(seed)]
    if lexleader:
        cmd.append("--lexleader")
    if lexleader_strong:
        cmd.append("--lexleader-strong")
        cmd.extend(["--lexleader-prefix-length", str(lexleader_prefix_length)])
    print("Exporting CNF for seed", seed)
    run_cmd(cmd)
    # exporter may emit file with _seed suffix; try common names
    candidates = [outfn, out_base / f"{outfn.stem}_seed{seed}.cnf", out_base / f"transport_seed{seed}_seed{seed}.cnf"]
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError(f"CNF not found for seed {seed}; checked: {candidates}")


def generate_powershell_runner(seeds: List[int], time_limit: int, workers: int, out_path: Path) -> None:
    lines = [
        "# Auto-generated transport job runner (PowerShell)",
        "param($seedStart=0, $seedEnd=0)",
        "$python = '" + str(sys.executable) + "'",
        "$script = '" + str(SCRIPTS / 'transport_csp_or_tools_larger.py') + "'",
        "Write-Host \"Starting transport OR-Tools runs\"",
    ]
    for s in seeds:
        lines.append(f"Write-Host 'Running seed {s}'")
        lines.append(f"& $python $script --seed {s} --time_limit {time_limit} --workers {workers}")
    out_path.write_text("\n".join(lines, encoding="utf-8"))
    try:
        out_path.chmod(0o755)
    except Exception:
        # chmod may fail on Windows in some contexts; ignore
        pass


def generate_slurm_runner(seeds: List[int], time_limit: int, workers: int, out_path: Path) -> None:
    # simple SLURM array job that runs one seed per task
    lines = [
        "#!/bin/bash",
        "# Auto-generated SLURM runner for transport OR-Tools",
        "#SBATCH --job-name=transport_csp",
        "#SBATCH --output=transport_csp_%A_%a.out",
        "#SBATCH --error=transport_csp_%A_%a.err",
        f"#SBATCH --time=0-{int(time_limit/60)}:00",
        "#SBATCH --cpus-per-task=1",
        "#SBATCH --mem=2G",
        f"SEEDS=({ ' '.join(str(s) for s in seeds) })",
        "IDX=$SLURM_ARRAY_TASK_ID",
        "SEED=${SEEDS[$IDX]}",
        f"PY={str(sys.executable)}",
        f"SCRIPT={str(SCRIPTS / 'transport_csp_or_tools_larger.py')}",
        "echo Running seed $SEED",
        "$PY $SCRIPT --seed $SEED --time_limit {0} --workers {1}".format(time_limit, workers),
    ]
    out_path.write_text("\n".join(lines, encoding="utf-8"))
    try:
        out_path.chmod(0o755)
    except Exception:
        pass


def parse_seed_range(s: str) -> List[int]:
    if "," in s:
        parts = s.split(",")
        out = []
        for p in parts:
            out.extend(parse_seed_range(p))
        return out
    if "-" in s:
        a, b = s.split("-", 1)
        return list(range(int(a), int(b) + 1))
    return [int(s)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="0", help="Seed or seed range, e.g. 0 or 0-7 or 0,2,5-7")
    parser.add_argument("--time_limit", type=int, default=300)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--out_dir", default=str(DATA))
    parser.add_argument("--slurm", action="store_true", help="Generate a SLURM array runner script")
    parser.add_argument("--bundle", action="store_true", help="Create a tar.gz bundle of the generated CNFs")
    parser.add_argument("--lexleader", action="store_true", help="Pass --lexleader to the CNF exporter to add lex-leader symmetry breaking")
    parser.add_argument("--lexleader-strong", action="store_true", help="Pass --lexleader-strong to enable stronger prefix lex-leader canonicalization in the CNF exporter")
    parser.add_argument("--lexleader-prefix-length", type=int, default=8, help="Prefix length to compare when using --lexleader-strong")
    args = parser.parse_args()

    seeds = parse_seed_range(args.seeds)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = {"seeds": [], "cnfs": {}, "ps1": None}
    for s in seeds:
        try:
            cnf = export_cnf_for_seed(s, out_dir, lexleader=args.lexleader, lexleader_strong=args.lexleader_strong, lexleader_prefix_length=args.lexleader_prefix_length)
            manifest["seeds"].append(s)
            manifest["cnfs"][str(s)] = str(cnf)
        except Exception as exc:
            print(f"Warning: failed to export seed {s}: {exc}")

    runner = out_dir / "run_transport_jobs.ps1"
    generate_powershell_runner(manifest["seeds"], args.time_limit, args.workers, runner)
    manifest["ps1"] = str(runner)

    if args.slurm:
        slurm_path = out_dir / "run_transport_jobs.slurm"
        generate_slurm_runner(manifest["seeds"], args.time_limit, args.workers, slurm_path)
        manifest["slurm"] = str(slurm_path)

    if args.bundle:
        # create a tar.gz of the CNF files for transfer to a solver farm
        import shutil

        archive_base = out_dir / "transport_cnfs_bundle"
        shutil.make_archive(str(archive_base), "gztar", root_dir=str(out_dir), base_dir=".")
        manifest["bundle"] = str(archive_base) + ".tar.gz"

    manifest_path = out_dir / "transport_jobs_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print("Wrote manifest:", manifest_path)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
