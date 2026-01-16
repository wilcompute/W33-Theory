# Quick WSL Sage Installation Guide

You have **two options** to install Sage inside your Ubuntu WSL:

## Option 1: APT (system package, requires sudo)

Open a WSL terminal (either via `wsl.exe` or Windows Terminal → Ubuntu tab):

```bash
sudo apt update
sudo apt install -y sagemath
sage -v
```

**Or** run the VS Code task: **WSL: Install Sage (Ubuntu apt)**

- It will prompt for your Ubuntu/WSL password
- Type it (won't show characters) and press Enter

---

## Option 2: Micromamba (user-level, no sudo)

From PowerShell in this repo:

```powershell
wsl.exe -d Ubuntu -e bash claude_workspace/install_sage_wsl_micromamba.sh
```

Then whenever you use Sage in WSL:

```bash
micromamba activate sage
sage -v
```

To make micromamba auto-activate, add to your `~/.bashrc` in WSL:

```bash
eval "$(micromamba shell hook --shell bash)"
micromamba activate sage
```

---

## After Sage is installed

Run the W33 pipeline:

```powershell
powershell -ExecutionPolicy Bypass -File claude_workspace\run_w33_sage_wsl.ps1
```

Or use VS Code tasks:
- **WSL: W33 Sage incidence + H1**
- **WSL: W33 Sage incidence + H1 (PySymmetry)**

Output: `claude_workspace/data/w33_sage_incidence_h1.json`
