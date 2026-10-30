"""Content digest of the frozen formula universe (data/w33_formula_search_universe_v1.json).

The universe file also records volatile bookkeeping (frozen_at, repository_head, bytes/files scanned, source line numbers) that changes
on every push.  The digest covers only what a search depends on: each exact family's formula_id, normalized formula, occurrence and
file counts and source files, and each structural family's id and members.

Usage:
  py -3 scripts/formula_universe_digest.py FILE                 print the digest
  py -3 scripts/formula_universe_digest.py --compare-head FILE  exit 0 if FILE has the same digest as the committed HEAD version, 1 otherwise
"""
import hashlib
import json
import subprocess
import sys


def digest(text):
    d = json.loads(text)
    ex = sorted((f["formula_id"], f.get("normalized_formula"), f.get("occurrence_count"), f.get("file_count"), tuple(sorted(f.get("source_files", []))))
                for f in d.get("exact_families", []))
    st = sorted((f["structural_family_id"], tuple(sorted(f.get("exact_formula_ids", [])))) for f in d.get("structural_families", []))
    return hashlib.sha256(json.dumps([ex, st]).encode()).hexdigest()


def main():
    args = sys.argv[1:]
    if args and args[0] == "--compare-head":
        path = args[1]
        try:
            old = subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True, check=True).stdout.decode("utf-8")
        except subprocess.CalledProcessError:
            return 1
        new = open(path, encoding="utf-8").read()
        same = digest(old) == digest(new)
        print("formula digest unchanged" if same else "formula digest changed")
        return 0 if same else 1
    print(digest(open(args[0], encoding="utf-8").read()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
