# Sage + PySymmetry notes (Windows)

This repo includes:

- `external/sage/` — a SageMath tree whose launcher is a **bash script** (`external/sage/bin/sage`).
- `external/pysymmetry/` — **PySymmetry**, which is a SageMath-based package (it expects `sage.all`).

## Why `external/sage/bin/sage` won’t run in PowerShell

On Windows, `external/sage/bin/sage` is a `#!/usr/bin/env bash` script. It requires a POSIX shell (`bash`) + the usual Linux userland.

So from plain PowerShell you’ll typically need either:

- WSL (recommended), or
- Git Bash / MSYS2 (if the Sage tree is compatible), or
- A native Sage installation available as `sage` on your PATH.

## New Sage script added

- `claude_workspace/w33_sage_incidence_and_h1.py`

What it does under Sage:

1. Loads W33 lines from `claude_workspace/data/_workbench/02_geometry/W33_line_phase_map.csv`.
2. Builds the **bipartite incidence graph** (40 points + 40 lines).
3. Computes the **bipartition-preserving automorphism group** using Sage/nauty.
4. Builds the simplicial complex (edges + triangles + tetrahedra from each line).
5. Computes $H_1$ and the induced **action on $H_1$** for the automorphism generators.
6. Optionally runs a **PySymmetry** isotypic analysis (gated by group order).

Output:

- `claude_workspace/data/w33_sage_incidence_h1.json`

## How to run (recommended: WSL + Sage)

Inside WSL, from the repo root:

```bash
bash ./claude_workspace/run_sage.sh claude_workspace/w33_sage_incidence_and_h1.py
```

Optional flags:

```bash
bash ./claude_workspace/run_sage.sh claude_workspace/w33_sage_incidence_and_h1.py --pysymmetry
bash ./claude_workspace/run_sage.sh claude_workspace/w33_sage_incidence_and_h1.py --field=GF --prime=1000003
```

If you prefer launching from Windows (PowerShell), you can use:

- `claude_workspace/run_w33_sage_wsl.ps1`

Or run the VS Code tasks:

- “WSL: W33 Sage incidence + H1”
- “WSL: W33 Sage incidence + H1 (PySymmetry)”

## If you want to try the bundled `external/sage` under WSL

From WSL, you can try running the repo’s launcher directly:

```bash
./external/sage/bin/sage -v
./external/sage/bin/sage -python claude_workspace/w33_sage_incidence_and_h1.py
```

(If it fails, your best path is installing Sage inside WSL and using that `sage`.)

## Installing Sage inside WSL (two common options)

Option A (simple, slower):

```bash
sudo apt update
sudo apt install -y sagemath
```

Option B (conda/mamba inside WSL):

If you’re already using micromamba/mamba/conda in WSL, installing Sage from conda-forge is often easier to manage:

```bash
micromamba create -n sage -c conda-forge sagemath
micromamba activate sage
sage -v
```

Note: the Windows micromamba env in `external/micromamba/` is separate from WSL; only use it if you decide to run non-Sage Python tooling on Windows.

## Troubleshooting

If the VS Code task “WSL: Smoke test Sage” exits with code 1 or 2:

1. Run the VS Code task “WSL: Diagnostics” to confirm your distro boots.
2. If `sage` is missing, install it inside WSL (APT or conda-forge).
3. Re-run “WSL: Smoke test Sage”, then run the W33 tasks.
