"""One-screen health check for a working copy of this repository (2026-10-30).

    py -3 scripts/doctor.py            # everything: python, packages, external tools, git wiring, generated indices
    py -3 scripts/doctor.py --json     # the same as JSON (for CI or another agent)

Exit code 0 when every REQUIRED item is present; optional items only warn.  Nothing is installed or changed -- run
scripts/bootstrap.ps1 (Windows) or scripts/bootstrap_repo_env.sh (Linux/WSL) to install what is missing.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = Path.home()

# import name -> pip name.  CORE = requirements.txt (imported by hundreds of files); OPTIONAL = requirements-optional.txt
CORE = {"numpy": "numpy", "scipy": "scipy", "sympy": "sympy", "networkx": "networkx", "mpmath": "mpmath", "pandas": "pandas",
        "matplotlib": "matplotlib", "ortools": "ortools", "igraph": "python-igraph", "pysat": "python-sat", "cdd": "pycddlib",
        "yaml": "pyyaml", "jsonschema": "jsonschema", "requests": "requests", "pytest": "pytest", "xdist": "pytest-xdist",
        "pytest_timeout": "pytest-timeout", "pre_commit": "pre-commit"}
OPTIONAL = {"numba": "numba", "cvxpy": "cvxpy", "qiskit_aer": "qiskit-aer", "pycryptosat": "pycryptosat", "ripser": "ripser",
            "persim": "persim", "mmgroup": "mmgroup", "flint": "python-flint", "jax": "jax", "thewalrus": "thewalrus", "pulp": "pulp",
            "pynauty": "pynauty", "psutil": "psutil", "sklearn": "scikit-learn", "galois": "galois", "pypdf": "pypdf"}

# external tools: name -> (required?, candidate locations beyond PATH, what needs it)
TOOLS = {
    "git": (True, [], "everything"),
    "gh": (False, [], "PRs, CI logs"),
    "continuity": (False, [HOME / "AppData/Roaming/npm/continuity.cmd"], "decision log (CLAUDE.md contract)"),
    "tectonic": (False, [HOME / "tools/tectonic/tectonic.exe", Path("C:/tools/tectonic/tectonic.exe")], "manuscript PDFs"),
    "lake": (False, [HOME / ".elan/bin/lake.exe", HOME / ".elan/bin/lake"], "formal/ Lean library"),
    "gp": (False, [Path("C:/tools/pari/gp.exe")], "PARI/GP lattice and modular-form passes"),
    "wsl": (False, [], "GAP, Sage, orbifolder (run inside WSL)"),
}
WSL_TOOLS = {"gap": "group theory certificates (*.g)", "gp": "PARI/GP", "micromamba": "Sage environment",
             "~/orb/nsostrict": "orbifolder with Ploger Wilson-line conditions"}
INDICES = ["RESULTS_INDEX.md", "REPO_MAP.md", "KEY_VOCABULARY.md", "CERTIFICATE_INDEX.md"]


def find_tool(name, extra):
    p = shutil.which(name)
    if p:
        return p
    for c in extra:
        if Path(c).exists():
            return str(c)
    return None


def run(cmd, timeout=20):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace")
        return r.returncode, (r.stdout or "").replace("\x00", "").strip()
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, str(e)


def check():
    rep = {"python": {"executable": sys.executable, "version": sys.version.split()[0], "ok": sys.version_info >= (3, 10)}}
    rep["core"] = {m: bool(importlib.util.find_spec(m)) for m in CORE}
    rep["optional"] = {m: bool(importlib.util.find_spec(m)) for m in OPTIONAL}
    rep["tools"] = {n: find_tool(n, extra) for n, (_, extra, _) in TOOLS.items()}
    rep["wsl"] = {}
    if rep["tools"]["wsl"]:
        probe = "; ".join(f'printf "%s=%s\\n" "{t}" "$( [ -e {t} ] && echo {t} || command -v {t} || echo -)"' for t in WSL_TOOLS)
        code, out = run(["wsl", "-e", "bash", "-lc", probe], timeout=40)
        for line in out.splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                rep["wsl"][k] = None if v in ("-", "") else v
    hooks = ROOT / ".git" / "hooks"
    if (ROOT / ".git").is_file():                            # a worktree: .git is a pointer file
        code, common = run(["git", "-C", str(ROOT), "rev-parse", "--git-common-dir"])
        hooks = Path(common) / "hooks" if code == 0 else hooks
    rep["git"] = {
        "pre_commit_hook": (hooks / "pre-commit").exists() and "pre-commit" in (hooks / "pre-commit").read_text(errors="ignore"),
        "remotes": run(["git", "-C", str(ROOT), "remote"])[1].split(),
        "branch": run(["git", "-C", str(ROOT), "branch", "--show-current"])[1],
    }
    now = time.time()
    rep["indices"] = {i: (round((now - (ROOT / i).stat().st_mtime) / 86400, 1) if (ROOT / i).exists() else None) for i in INDICES}
    rep["ok"] = rep["python"]["ok"] and all(rep["core"].values()) and all(
        rep["tools"][n] for n, (req, _, _) in TOOLS.items() if req)
    return rep


def show(rep):
    mark = lambda b: "ok  " if b else "--  "
    py = rep["python"]
    print(f"python   {mark(py['ok'])}{py['version']}  {py['executable']}")
    miss = [CORE[m] for m, b in rep["core"].items() if not b]
    print(f"core     {mark(not miss)}{len(rep['core']) - len(miss)}/{len(rep['core'])} packages" +
          (f"   missing: {' '.join(miss)}  ->  py -3 -m pip install -r requirements.txt" if miss else ""))
    miss = [OPTIONAL[m] for m, b in rep["optional"].items() if not b]
    print(f"optional      {len(rep['optional']) - len(miss)}/{len(rep['optional'])} packages" +
          (f"   (pip install -r requirements-optional.txt for: {' '.join(miss)})" if miss else ""))
    for n, (req, _, why) in TOOLS.items():
        p = rep["tools"][n]
        print(f"tool     {mark(p) if req or p else '    '}{n:11s} {p or ('MISSING' if req else 'not found')}   [{why}]")
    for n, why in WSL_TOOLS.items():
        if rep["wsl"]:
            p = rep["wsl"].get(n)
            print(f"wsl           {n:16s} {p or 'not found'}   [{why}]")
    g = rep["git"]
    print(f"git      {mark(g['pre_commit_hook'])}pre-commit hook" + ("" if g["pre_commit_hook"] else
          "   ->  py -3 -m pre_commit install") + f";  branch {g['branch']};  remotes {', '.join(g['remotes'])}")
    ages = ", ".join(f"{k} {v}d" if v is not None else f"{k} MISSING" for k, v in rep["indices"].items())
    print(f"indices       {ages}   (refresh: py -3 analysis/build_results_index.py)")
    print("\nREADY" if rep["ok"] else "\nNOT READY: install the items marked --")


if __name__ == "__main__":
    r = check()
    if "--json" in sys.argv:
        print(json.dumps(r, indent=1, default=str))
    else:
        show(r)
    sys.exit(0 if r["ok"] else 1)
