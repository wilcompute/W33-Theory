# Git Repair Notes (Jan 26, 2026)

This repo has two issues that can cause "lock file" errors and "duplicate repo" confusion.

## 1) Stale index lock

The file `.git/index.lock` exists and blocks git operations.

Delete it:

- WSL/Linux:
```
rm -f .git/index.lock
```

- PowerShell:
```
del .git\\index.lock
```

## 2) Nested repo in `data/` (broken submodule)

There is a nested `.git` in `data/`, and the main repo has `data` recorded as a
gitlink (mode 160000), but there is **no `.gitmodules`** file. This makes Git
think `data` is a submodule without configuration, which can look like a second
repo on GitHub.

If `data/` should just be a normal folder (recommended unless you intended a submodule):

- WSL/Linux:
```
rm -rf data/.git
git rm --cached data
git add data
```

- PowerShell:
```
Remove-Item -Recurse -Force data\\.git
git rm --cached data
git add data
```

If `data/` should be a real submodule:

1) Provide the correct GitHub URL for the submodule.
2) Recreate `.gitmodules` and re‑add the submodule properly.

## Status check

After fixing, verify:
```
git status -sb
git submodule status
```
