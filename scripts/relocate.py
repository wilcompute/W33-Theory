"""Move files or directories AND rewrite every reference to them (2026-10-30).

    py -3 scripts/relocate.py plan  --batch root-md          # show what would move and how many references would change
    py -3 scripts/relocate.py apply --batch root-md          # git mv + rewrite references
    py -3 scripts/relocate.py plan  --move OLD NEW [--move OLD NEW ...]

Batches:
  root-md    root pass write-ups (PASS*, PART*, BREAKTHROUGH*, BT*, ... *.md) -> analysis/ (where ~3,000 others already live)

Reference rewriting (in every tracked text file except the ones listed in SKIP):
  * a markdown / HTML link target  ](t)  href="t"  src="t"  is resolved relative to the file that contains it; if it pointed at a
    moved path it is replaced by the new path relative to the same file;
  * any other occurrence of a moved path as a whole token (code such as ROOT / "PASS1147_X.md", workflow paths, prose) is treated as
    root-relative and replaced by the new root-relative path;
  * certificates and generated indices are NOT rewritten: data/**, *.json (their bytes are hashed or regenerated), .continuity/**,
    RESULTS_INDEX.md / KEY_VOCABULARY.md / TOPICAL_ALIASES.md (rebuild them afterwards).
Basenames never change, so scripts/find.py and every index keep finding a file by name.
"""
import argparse
import os
import posixpath
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT = (".md", ".py", ".tex", ".yml", ".yaml", ".toml", ".cfg", ".ini", ".sh", ".ps1", ".html", ".g", ".bib", ".txt", ".lean", ".rst")
SKIP_PREFIX = ("data/", ".continuity/", "archive/dirs/")
SKIP_FILES = {"RESULTS_INDEX.md", "KEY_VOCABULARY.md", "TOPICAL_ALIASES.md", "CODE_PARAMETER_INDEX_ALL_REPOS.md"}
KEEP_ROOT_MD = {"README.md", "CHANGELOG.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "LICENSE.md", "CLAUDE.md", "AGENTS.md",
                "GEMINI.md", "REPO_MAP.md", "RESULTS_INDEX.md", "KEY_VOCABULARY.md", "TOPICAL_ALIASES.md", "CODE_PARAMETER_INDEX_ALL_REPOS.md",
                "RESULTS_VOCABULARY.md", "CERTIFICATE_INDEX.md", "CERTIFICATE_RESULTS_INDEX.md", "HOLONET.md", "SESSION_HANDOFF.md"}


def git(*a):
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout


def batch(name):
    files = git("ls-files").splitlines()
    if name == "root-md":
        moves = []
        for f in files:
            if "/" in f or not f.endswith(".md") or f in KEEP_ROOT_MD:
                continue
            if re.match(r"(PASS|PART|BREAKTHROUGH|BT|AUDIT|ARXIV|PILLAR|W33_|W36_|RELEASE|NOTE|SUMMARY|SESSION)", f, re.I):
                moves.append((f, "analysis/" + f))
        return moves
    if name == "small-dirs":
        dirs = dict(SMALL_DIRS)
        moves = [(f, dirs[f.split("/")[0]] + f[len(f.split("/")[0]):]) for f in files if "/" in f and f.split("/")[0] in dirs]
        return moves
    raise SystemExit(f"unknown batch {name}")


# small top-level directories (no importable Python) -> their natural homes; NOTES/notes merge (they collide on Windows, which is
# case-insensitive), schema merges into schemas.
SMALL_DIRS = [("reports", "docs/reports"), ("NOTES", "docs/notes"), ("notes", "docs/notes"), ("presentations", "docs/presentations"),
              ("visualizations", "docs/visualizations"), ("figures", "docs/figures"), ("evidence", "docs/evidence"), ("specs", "docs/specs"),
              ("theory", "docs/theory"), ("submission", "papers/submission"), ("BT1613_arXiv_package", "papers/BT1613_arXiv_package"),
              ("V24_output", "archive/outputs/V24_output"), ("V24_output_v13", "archive/outputs/V24_output_v13"),
              ("V24_output_v13_full", "archive/outputs/V24_output_v13_full"), ("V29_output_q_stiffness", "archive/outputs/V29_output_q_stiffness"),
              ("V29_output_q_stiffness_validate", "archive/outputs/V29_output_q_stiffness_validate"),
              ("extracted_v15", "archive/outputs/extracted_v15"), ("extracted_v20", "archive/outputs/extracted_v20"),
              ("branch_audit", "archive/outputs/branch_audit"), ("dist", "archive/outputs/dist"), ("out", "archive/outputs/out"),
              ("build", "archive/outputs/build"), ("patches", "archive/outputs/patches"), ("results", "archive/outputs/results"),
              ("checks", "archive/outputs/checks"), ("schema", "schemas")]


DIR_MOVES = []          # set by main() for directory batches
DIR_ONLY = False
LINK = re.compile(r"(\]\(|href=\"|src=\")([^)\"\s#]+)")


def rewrite_text(path, text, moves):
    """Return (new_text, n_changes)."""
    d = posixpath.dirname(path)
    old2new = dict(moves)
    n = 0

    def link_sub(m):
        nonlocal n
        tgt = m.group(2)
        if tgt.startswith(("http:", "https:", "mailto:")):
            return m.group(0)
        resolved = posixpath.normpath(posixpath.join(d, tgt)) if d else posixpath.normpath(tgt)
        if resolved in old2new:
            new = posixpath.relpath(old2new[resolved], d or ".")
            n += 1
            return m.group(1) + new
        return m.group(0)
    text = LINK.sub(link_sub, text)
    # absolute GitHub URLs to a moved file (docs/index.html links to the corpus this way)
    if old2new:
        rxg = re.compile(r"((?:github\.com/[^/\s\"')]+/[^/\s\"')]+/(?:blob|tree|raw)/[^/\s\"')]+/|raw\.githubusercontent\.com/[^/\s\"')]+/[^/\s\"')]+/[^/\s\"')]+/))("
                         + "|".join(re.escape(x) for x in sorted(old2new, key=len, reverse=True)) + r")(?![A-Za-z0-9_])")

        def gh_sub(m):
            nonlocal n
            n += 1
            return m.group(1) + old2new[m.group(2)]
        text = rxg.sub(gh_sub, text)
    # directory moves: rewrite path-shaped references 'D/...' and quoted bare 'D' / "D" (never the bare word in prose)
    for od, nd in DIR_MOVES:
        rxd = re.compile(r"(?<![A-Za-z0-9_./\\-])" + re.escape(od) + r"/")
        text, k = rxd.subn(nd + "/", text); n += k
        rxq = re.compile(r"([\"'])" + re.escape(od) + r"\1")
        text, k = rxq.subn(lambda m: m.group(1) + nd + m.group(1), text); n += k
    # root-relative tokens (not part of a longer path or name); skip those already rewritten as links above
    names = sorted(old2new, key=len, reverse=True) if not DIR_ONLY else []
    if names:
        rx = re.compile(r"(?<![A-Za-z0-9_./\\-])(" + "|".join(re.escape(x) for x in names) + r")(?![A-Za-z0-9_])")

        def tok_sub(m):
            nonlocal n
            n += 1
            return old2new[m.group(1)]
        # do not touch link targets (already handled): split on links, rewrite only the non-link spans
        parts = re.split(r"(\]\([^)]*\)|href=\"[^\"]*\"|src=\"[^\"]*\")", text)
        text = "".join(p if i % 2 else rx.sub(tok_sub, p) for i, p in enumerate(parts))
    return text, n


def run(moves, apply):
    names = {o for o, _ in moves}
    changed = {}
    probe = re.compile("|".join(re.escape(os.path.basename(o)) for o in names)) if names else None
    # prefilter with git grep (one pass over the index, seconds) instead of reading all ~42k files in Python
    pat = ROOT / ".git_relocate_patterns.txt"
    pat.write_text("\n".join(sorted({os.path.basename(o.rstrip("/")) for o in names})) + "\n", encoding="utf-8")
    try:
        files = git("grep", "-I", "-l", "-F", "-f", str(pat)).splitlines()
    finally:
        pat.unlink(missing_ok=True)
    for f in files:
        if f.startswith(SKIP_PREFIX) or f.endswith(".json") or os.path.basename(f) in SKIP_FILES or not f.endswith(TEXT):
            continue
        p = ROOT / f
        try:
            if p.stat().st_size > 3_000_000:
                continue
            raw = p.read_bytes()
            text = raw.decode("utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if probe is not None and not DIR_MOVES and not probe.search(text):
            continue
        new, n = rewrite_text(f, text, moves)
        if n:
            changed[f] = (new, n, raw)
    print(f"{len(moves)} paths to move; {sum(v[1] for v in changed.values())} references in {len(changed)} files to rewrite")
    if not apply:
        for o, nw in moves[:15]:
            print(f"  {o} -> {nw}")
        top = sorted(changed.items(), key=lambda kv: -kv[1][1])[:12]
        for f, (_, n, _) in top:
            print(f"  rewrite {n:4d}  {f}")
        return 0
    for o, nw in moves:
        (ROOT / nw).parent.mkdir(parents=True, exist_ok=True)
        if (ROOT / nw).exists():
            print(f"  SKIP (target exists) {o} -> {nw}")
            continue
        subprocess.run(["git", "-C", str(ROOT), "mv", o, nw], check=True)
    for f, (new, n, raw) in changed.items():
        target = f
        for o, nw in moves:
            if f == o:
                target = nw
        p = ROOT / target
        crlf = b"\r\n" in raw
        data = new.replace("\r\n", "\n")
        if crlf:
            data = data.replace("\n", "\r\n")
        p.write_bytes(data.encode("utf-8"))
    print("applied")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["plan", "apply"])
    ap.add_argument("--batch")
    ap.add_argument("--move", nargs=2, action="append", metavar=("OLD", "NEW"))
    a = ap.parse_args()
    moves = batch(a.batch) if a.batch else [tuple(m) for m in (a.move or [])]
    if a.batch == "small-dirs":
        DIR_MOVES.extend(SMALL_DIRS)
        # file-level token rewriting is redundant for directory batches (the D/ rule covers it) and slow: rewrite links + dir tokens only
        global DIR_ONLY
        DIR_ONLY = True
    taken = [nw for _, nw in moves if (ROOT / nw).exists()]
    if taken:
        print("target collisions (these will be skipped):", taken[:10])
    return run(moves, a.mode == "apply")


if __name__ == "__main__":
    sys.exit(main())
