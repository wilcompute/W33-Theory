# Setting up a new machine

Three steps: clone, bootstrap, and (optionally) carry over the state that is not in git.

## 1. Clone

```powershell
git clone https://github.com/wilcompute/W33-Theory.git "C:\Repos\Theory of Everything"
```

Clone to the **same path** as on the old machine if you can. Claude Code keys its project memory on the folder path, so the same
path means the imported memory is found without renaming anything.

## 2. Bootstrap

```powershell
cd "C:\Repos\Theory of Everything"
pwsh -File scripts/bootstrap.ps1            # add -Optional for the rarely used packages
```

The bootstrap installs `requirements.txt` into `py -3`, installs the pre-commit hooks, adds the `origin-https` remote, and runs
the doctor. You can run the doctor on its own at any time:

```powershell
py -3 scripts/doctor.py                     # one screen; exit code 0 = ready
```

The doctor checks:

- Python and its packages;
- the external tools listed below;
- the WSL toolchain;
- the git hook;
- how old the generated indices are.

On Linux or WSL, `scripts/bootstrap_repo_env.sh` builds a virtualenv instead.

## 3. External tools (installed by hand, once)

| Tool | Needed for | Where the old machine had it |
|---|---|---|
| [tectonic](https://tectonic-typesetting.github.io) | Manuscript PDFs (`scripts/compile_sweep.py`) | `%USERPROFILE%\tools\tectonic\tectonic.exe` (not on PATH) |
| [PARI/GP](https://pari.math.u-bordeaux.fr) | Lattice and modular-form passes | `C:\tools\pari\gp.exe`, and `gp` in WSL |
| [elan / Lean 4](https://lean-lang.org) | `formal/` (`cd formal && lake build`) | `%USERPROFILE%\.elan` |
| WSL Ubuntu + `gap` | `*.g` certificates | `apt install gap` |
| WSL micromamba + Sage | Sage passes | `install_sage_wsl_micromamba.sh` |
| WSL orbifolder | Heterotic orbifold passes | `~/orb/nsostrict` (built with Ploger's Wilson-line conditions; see `reference_ploger_wilson_line_conditions` in the agent memory) |
| [continuity](https://www.npmjs.com/) CLI | The decision log that `CLAUDE.md` asks agents to keep | `npm install -g` (global binary) |
| GitHub CLI `gh` | CI logs, PRs | `winget install GitHub.cli` |

## 4. Carry over what git does not hold

```powershell
pwsh -File scripts/machine_transfer.ps1 export            # old machine -> %USERPROFILE%\toe_state_YYYYMMDD.zip
pwsh -File scripts/machine_transfer.ps1 import -In <zip>  # new machine, after step 2
```

The zip holds:

- **Claude's project memory:** about 80 fact files and the `MEMORY.md` index.
- **Codex configuration:** `config.toml` and `AGENTS.md` from WSL.
- **Orbifolder recipes:** the scripts from WSL `~/orb`. The binaries are rebuilt on the new machine.
- **A record of the old tool locations.**

The import never overwrites existing Codex or orbifolder files. Keep the zip out of the repository, because it contains machine
paths and private notes. The export was tested on 2026-10-30; the import is a straight copy in the other direction and has not
been run yet.

**Codex chat history.** Local Codex threads are stored only in WSL `~/.codex`. They do not sync between machines and are not
needed to resume work: the repository and the agent memory carry the state. Codex Cloud tasks live on OpenAI's servers and appear
on any machine you sign in from. On 2026-10-30 the old machine's local history was archived with `codex archive`, cutting it from
2.46 GB to 34 MB; any thread can be restored with `codex unarchive <id>`.
