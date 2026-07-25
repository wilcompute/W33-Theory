Push instructions — run locally in your repo root

Observed issue here: SSH to github.com timed out when attempting to push from this environment.

The following commands will commit the new files and push `master` to origin.
Run them in PowerShell (Windows) or a POSIX shell in your repo root.

# 1) Preview status

```bash
git status --porcelain
```

# 2) Stage the new/modified files

```bash
git add .github/workflows/build-pdf.yml RELEASE_CHECKLIST.md scripts/release_prepare.py scripts/debug_mckay.py exploration/w33_mckay_thompson_eta_quotients.py
```

# 3) Commit

```bash
git commit -m "Add release automation script, release checklist, and CI PDF build workflow"
```

# 4) Push (SSH remote)

```bash
git push origin master
```

If SSH fails (common if SSH keys or agent are not available), force HTTPS remote for this push:

```bash
# set HTTPS remote (one-time)
git remote set-url origin https://github.com/wilcompute/W33-Theory.git

# then push; this will prompt for credentials if required
git push origin master
```

# 5) Optional: create annotated tag and push tags (required to mint Zenodo DOI)

```bash
git tag -a v1.0.0 -m "ArXiv submission — April 2026"
git push origin master --tags
```

# 6) Use the release preparer to insert ARXIV-ID and optionally push (recommended flow)

```bash
# dry-run preview
python scripts/release_prepare.py --arxiv YOUR.ARXIV.ID

# apply changes, commit, tag (interactive unless --yes)
python scripts/release_prepare.py --arxiv YOUR.ARXIV.ID --apply --yes

# to push as well (requires network/auth)
python scripts/release_prepare.py --arxiv YOUR.ARXIV.ID --apply --push --yes
```

# Troubleshooting
- If `git push` fails: check SSH keys (`ssh -T git@github.com`) or switch to HTTPS as above.
- If your CI uses a required branch protection rule, ensure you have permission to push directly to `master` or create a PR instead.

If you'd like, I can:
- attempt the push again if you enable Docker/SSH/PT access here,
- or prepare a git-format patch bundle for manual application (I can create `release_changes.patch`).

Tell me which you prefer and I'll proceed.
