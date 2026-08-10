#!/usr/bin/env python3
import os
import subprocess
import tempfile
from pathlib import Path

import scripts.git_auto_keep as gak


def run(cmd, cwd):
    return subprocess.run(
        cmd,
        check=True,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def main():
    with tempfile.TemporaryDirectory() as td:
        repo = Path(td) / "repo"
        repo.mkdir()
        # initialize git repo
        run(["git", "init"], cwd=repo)
        # set user config
        run(["git", "config", "user.email", "test@example.com"], cwd=repo)
        run(["git", "config", "user.name", "Test"], cwd=repo)

        # create a file and write
        f = repo / "foo.txt"
        f.write_text("hello", encoding="utf-8")

        # call git_add_commit inside the repo
        cwd = os.getcwd()
        try:
            os.chdir(repo)
            ok, msg = gak.git_add_commit(
                [str(f)], "test commit", branch=None, push=False
            )
        finally:
            os.chdir(cwd)

        print("ok", ok, msg)
        # confirm commit exists
        res = run(["git", "log", "--oneline"], cwd=repo)
        print(res.stdout)


if __name__ == "__main__":
    main()
