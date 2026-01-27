# Sage + PySymmetry notes (Windows)

This repo includes:

- `external/sage/` — an optional SageMath tree whose launcher is a **bash script** (`external/sage/bin/sage`).
- `external/pysymmetry/` — **PySymmetry**, a SageMath-based package (it expects `sage.all`).

## Linux/container quickstart

From the repo root:

```bash
./scripts/setup_sage_pysymmetry.sh
```

That script installs micromamba + Sage (conda-forge) and clones PySymmetry into
`external/pysymmetry`, then runs a smoke test.

## Docker quickstart (recommended if you already have Docker)

From the repo root:

```bash
./scripts/setup_sage_pysymmetry_docker.sh
```

This will:
1. Pull `sagemath/sagemath:10.7`
2. Clone PySymmetry into `external/pysymmetry`
3. Run a Sage + PySymmetry smoke test inside the container

After that, `./run_sage.sh ...` will automatically use Docker if no local Sage
is found.

## Why `external/sage/bin/sage` won’t run in PowerShell

On Windows, `external/sage/bin/sage` is a `#!/usr/bin/env bash` script. It requires a POSIX shell (`bash`) + the usual Linux userland.

So from plain PowerShell you’ll typically need either:

- WSL (recommended), or
- Git Bash / MSYS2 (if the Sage tree is compatible), or
- A native Sage installation available as `sage` on your PATH.

## New Sage script added

- `w33_sage_incidence_and_h1.py`

What it does under Sage:

1. Loads W33 lines from `data/_workbench/02_geometry/W33_line_phase_map.csv` (or `claude_workspace/data/...` if you keep a separate workspace layout).
2. Builds the **bipartite incidence graph** (40 points + 40 lines).
3. Computes the **bipartition-preserving automorphism group** using Sage/nauty.
4. Builds the simplicial complex (edges + triangles + tetrahedra from each line).
5. Computes $H_1$ and the induced **action on $H_1$** for the automorphism generators.
6. Optionally runs a **PySymmetry** isotypic analysis (gated by group order).

Output:

- `data/w33_sage_incidence_h1.json` (or `claude_workspace/data/...` if you keep a separate workspace layout)

## How to run (recommended: WSL + Sage)

Inside WSL, from the repo root:

```bash
bash ./run_sage.sh w33_sage_incidence_and_h1.py
```

Optional flags:

```bash
bash ./run_sage.sh w33_sage_incidence_and_h1.py --pysymmetry
bash ./run_sage.sh w33_sage_incidence_and_h1.py --field=GF --prime=1000003
```

If you prefer launching from Windows (PowerShell), you can use:

- `run_w33_sage_wsl.ps1`

Or run the VS Code tasks:

- “WSL: W33 Sage incidence + H1”
- “WSL: W33 Sage incidence + H1 (PySymmetry)”

## If you want to try the bundled `external/sage` under WSL

From WSL, you can try running the repo’s launcher directly:

```bash
./external/sage/bin/sage -v
./external/sage/bin/sage -python w33_sage_incidence_and_h1.py
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
micromamba create -n sage -c conda-forge sage
micromamba activate sage
sage -v
```

Note: the Windows micromamba env in `external/micromamba/` is separate from WSL; only use it if you decide to run non-Sage Python tooling on Windows.

## Troubleshooting

If the VS Code task “WSL: Smoke test Sage” exits with code 1 or 2:

1. Run the VS Code task “WSL: Diagnostics” to confirm your distro boots.
2. If `sage` is missing, install it inside WSL (APT or conda-forge).
3. Re-run “WSL: Smoke test Sage”, then run the W33 tasks.
