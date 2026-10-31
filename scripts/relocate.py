"""Move files or directories AND rewrite every reference to them (2026-10-30).

    py -3 scripts/relocate.py plan  --batch root-md          # show what would move and how many references would change
    py -3 scripts/relocate.py apply --batch root-md          # git mv + rewrite references
    py -3 scripts/relocate.py plan  --move OLD NEW [--move OLD NEW ...]

Batches:
  root-md    root pass write-ups (PASS*, PART*, BREAKTHROUGH*, BT*, ... *.md) -> analysis/ (where ~3,000 others already live)
  root-json  root certificates -> data/ (strict: only files whose every Python reference has an unambiguous repo-root base)
  small-dirs small top-level directories -> docs/, papers/, archive/outputs/, schemas/
  root-py    root modules -> analysis/; each is "lifted" so its __file__-relative paths still resolve to the repo root and it can
             still import the repo's packages when run as a script; root wrappers of pillars/ modules are retired

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
SKIP_FILES = {"relocate.py", "RESULTS_INDEX.md", "KEY_VOCABULARY.md", "TOPICAL_ALIASES.md", "CODE_PARAMETER_INDEX_ALL_REPOS.md"}
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
    if name == "root-json":
        return [(f, "data/" + f) for f in files if "/" not in f and f.endswith(".json") and not f.startswith(".")]
    if name == "small-dirs":
        dirs = dict(SMALL_DIRS)
        moves = [(f, dirs[f.split("/")[0]] + f[len(f.split("/")[0]):]) for f in files if "/" in f and f.split("/")[0] in dirs]
        return moves
    if name == "root-py":
        # every root module -> analysis/ (conftest.py APPENDS analysis/ to sys.path, so `import X` keeps working and can never shadow
        # an installed or earlier module); root wrappers of pillars/ modules are retired, their references pointed at pillars/
        moves = []
        # setup.py installs py_modules from the root (holonet_cmd -> the `holonet` console command): those must stay
        installed = set(re.findall(r"[\"']([A-Za-z_][A-Za-z0-9_]*)[\"']", (re.search(r"py_modules\s*=\s*\[([^\]]*)\]", (
            ROOT / "setup.py").read_text(encoding="utf-8")) or re.match("", "")).group(1) or ""))
        for f in files:
            if "/" in f or not f.endswith(".py") or f in ("setup.py", "conftest.py") or f[:-3] in installed:
                continue
            pil = "pillars/" + f
            if (ROOT / pil).exists() and "Wrapper to run pillars/" in (ROOT / f).read_text(encoding="utf-8", errors="ignore"):
                RETIRE.add(f)
                moves.append((f, pil))
            else:
                moves.append((f, "analysis/" + f))
        return moves
    raise SystemExit(f"unknown batch {name}")


RETIRE = set()          # root-py: wrappers whose real module already lives at the target -> git rm, references -> target
# A moved root module located the repo through its own folder; one level down, the same expressions must climb one more level, so
# every path it reads or writes stays exactly where it was (census 2026-10-30: these forms cover all 221 uses of __file__).
UP = "os.path.dirname(os.path.dirname(os.path.abspath(__file__)))"
FILE_FORMS = [
    (re.compile(r"os\.path\.dirname\(\s*os\.path\.abspath\(\s*__file__\s*\)\s*\)"), "@@UP@@"),
    (re.compile(r"os\.path\.dirname\(\s*__file__\s*\)"), "@@UP@@"),
    (re.compile(r"\bPath\(\s*__file__\s*\)\.resolve\(\)\.parent(?![A-Za-z_\[])"), "Path(__file__).resolve().parents[1]"),
    (re.compile(r"\bPath\(\s*__file__\s*\)\.parent(?![A-Za-z_\[])"), "Path(__file__).resolve().parents[1]"),
]
# analysis/exploration/pillars too: four moved modules import `analysis.X`, which needs the root on sys.path (found by the script rerun)
LOCAL_PKG = re.compile(r"^([ \t]*)(?:from|import)[ \t]+(?:scripts|w33|src|lib|tools|utils|analysis|exploration|pillars)\b", re.M)


def lift_module(path):
    """Rewrite a root module moved one folder down so that it still resolves the repo root (FILE_FORMS) and, when run as a script,
    can still import the repo's packages (sys.path[0] is now its own folder, not the root).  Returns the number of edits."""
    p = ROOT / path
    raw = p.read_bytes()
    t = raw.decode("utf-8")
    n = 0
    for rx, rep in FILE_FORMS:
        t, k = rx.subn(lambda m: rep, t)
        n += k
    t = t.replace("@@UP@@", UP)
    m = LOCAL_PKG.search(t)
    if m and "sys.path" not in t[:m.start()]:
        eol = "\r\n" if b"\r\n" in raw else "\n"
        boot = (m.group(1) + "import os as _os, sys as _sys; _sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))"
                "  # relocated from the root (2026-10-30)" + eol)
        t = t[:m.start()] + boot + t[m.start():]
        n += 1
    if n:
        p.write_bytes(t.encode("utf-8"))
    return n


# generic names (build, dist, out, results, checks, patches) are deliberately NOT here: workflows and code use them for runtime
# scratch paths and operators ('out/=' in numpy code), so a textual rewrite cannot tell them apart from the tracked folders.
# small top-level directories (no importable Python) -> their natural homes; docs/notes/notes merge (they collide on Windows, which is
# case-insensitive), schema merges into schemas.
SMALL_DIRS = [("reports", "docs/reports"), ("NOTES", "docs/notes"), ("notes", "docs/notes"), ("presentations", "docs/presentations"),
              ("visualizations", "docs/visualizations"), ("figures", "docs/figures"), ("evidence", "docs/evidence"), ("specs", "docs/specs"),
              ("theory", "docs/theory"), ("submission", "papers/submission"), ("BT1613_arXiv_package", "papers/BT1613_arXiv_package"),
              ("V24_output", "archive/outputs/V24_output"), ("V24_output_v13", "archive/outputs/V24_output_v13"),
              ("V24_output_v13_full", "archive/outputs/V24_output_v13_full"), ("V29_output_q_stiffness", "archive/outputs/V29_output_q_stiffness"),
              ("V29_output_q_stiffness_validate", "archive/outputs/V29_output_q_stiffness_validate"),
              ("extracted_v15", "archive/outputs/extracted_v15"), ("extracted_v20", "archive/outputs/extracted_v20"),
              ("branch_audit", "archive/outputs/branch_audit"), ("schema", "schemas")]


GENERIC_NAMES = {"main.tex", "index.html", "index.md", "README.md", "__init__.py", "setup.py", "conftest.py", "Makefile",
                 "requirements.txt", "config.json", "manifest.json", "results.json", "report.md", "notes.md"}
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
        rxd = re.compile(r"(?<![A-Za-z0-9_./\\-])" + re.escape(od) + r"/(?=[A-Za-z0-9_.*{$-])")   # a path must follow, never 'out/='
        text, k = rxd.subn(nd + "/", text); n += k
        # quoted bare names ONLY for distinctive directory names (a digit or an underscore): "notes", "schema", "evidence" are
        # everyday dict keys -- this rule once turned ~2,500 "schema" keys into "schemas" before the audit caught it (2026-10-30)
        if re.search(r"[0-9_]", od):          # a digit or underscore: V24_output, BT1613_arXiv_package -- never NOTES or notes
            rxq = re.compile(r"([\"'])" + re.escape(od) + r"\1")
            text, k = rxq.subn(lambda m: m.group(1) + nd + m.group(1), text); n += k
    # root-relative tokens (not part of a longer path or name); skip those already rewritten as links above
    names = sorted(old2new, key=len, reverse=True) if not DIR_ONLY else []
    if names:
        rx = re.compile(r"(?<![A-Za-z0-9_./\\-])(" + "|".join(re.escape(x) for x in names) + r")(?![A-Za-z0-9_])")

        def tok_sub(m):
            nonlocal n
            before = m.string[max(0, m.start() - 24):m.start()]
            if re.search(r"[\"'][A-Za-z0-9_.-]+[\"']\s*/\s*[\"']?$|[A-Za-z0-9_]/$", before):
                return m.group(0)            # ROOT / "data" / "x.json" or a sub-path: points somewhere else already
            n += 1
            return old2new[m.group(1)]
        # do not touch link targets (already handled): split on links, rewrite only the non-link spans
        parts = re.split(r"(\]\([^)]*\)|href=\"[^\"]*\"|src=\"[^\"]*\")", text)
        text = "".join(p if i % 2 else rx.sub(tok_sub, p) for i, p in enumerate(parts))
    return text, n


ROOT_BASE = re.compile(r"(?:\b(?:ROOT|REPO_ROOT|ROOT_DIR|repo_root|PROJECT_ROOT)\s*/\s*|\b(?:open|Path|exists|isfile)\(\s*)[\"']$")
MESSAGE = re.compile(r"(?:saved to|written to|[Ww]rote\]?|Results ->)\s*[\"']?\s*$")


def strict_filter(moves):
    """For file batches whose references live in Python: keep a move only if EVERY Python reference to it has an unambiguous
    repo-root base (ROOT / "x", REPO_ROOT / "x", open("x"), Path("x")).  `out_dir / "x"`, `repo / "x"` (a variable that may be a
    subfolder), zip member names and the like make the move ambiguous, so that file stays where it is (2026-10-30: the root-json batch
    first rewrote three zip members and a test's subfolder variable)."""
    names = {o: nw for o, nw in moves}
    rx = re.compile(r"(?<![A-Za-z0-9_./\\-])(" + "|".join(re.escape(x) for x in sorted(names, key=len, reverse=True)) + r")(?![A-Za-z0-9_])")
    pat = ROOT / ".git_relocate_patterns.txt"
    pat.write_text("\n".join(sorted(names)) + "\n", encoding="utf-8")
    try:
        files = git("grep", "-I", "-l", "-F", "-f", str(pat), "--", "*.py").splitlines()
    finally:
        pat.unlink(missing_ok=True)
    bad = set()
    for f in files:
        try:
            t = (ROOT / f).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for m in rx.finditer(t):
            before = t[max(0, m.start() - 40):m.start()]
            # Path("x.json") in a test or producer is relative to the working directory, which is the repo root for pytest, CI and
            # `py -3 analysis/X.py` run from the root, so it is rewritten like ROOT / "x.json" (2026-10-30, after the root-py move);
            # a message naming the output ("Results saved to x.json") is prose and is rewritten too
            if f == m.group(1) or not (ROOT_BASE.search(before) or MESSAGE.search(before)):
                bad.add(m.group(1))
    kept = [(o, nw) for o, nw in moves if o not in bad]
    print(f"strict: {len(bad)} of {len(moves)} files have an ambiguous Python reference and stay put")
    return kept


def run(moves, apply):
    names = {o for o, _ in moves}
    changed = {}
    probe = re.compile("|".join(re.escape(os.path.basename(o)) for o in names)) if names else None
    # prefilter with git grep (one pass over the index, seconds) instead of reading all ~42k files in Python
    pat = ROOT / ".git_relocate_patterns.txt"
    # directory batches must also find files that mention the directory but none of the moved files (2026-10-30: batch 2 first
    # prefiltered on moved file names only and missed 73 files, e.g. workflows writing evidence/<pass>/)
    pats = {os.path.basename(o.rstrip("/")) for o in names}
    pats |= {d + "/" for d, _ in DIR_MOVES} | {'"' + d + '"' for d, _ in DIR_MOVES} | {"'" + d + "'" for d, _ in DIR_MOVES}
    pat.write_text("\n".join(sorted(pats)) + "\n", encoding="utf-8")
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
        if o in RETIRE:
            subprocess.run(["git", "-C", str(ROOT), "rm", "-q", o], check=True)
            changed.pop(o, None)
            continue
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
    lifted = [(nw, lift_module(nw)) for o, nw in moves if "/" not in o and o.endswith(".py") and o not in RETIRE]
    if lifted:
        print(f"lifted {sum(1 for _, k in lifted if k)} moved modules ({sum(k for _, k in lifted)} __file__ / sys.path edits)")
    print("applied")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["plan", "apply"])
    ap.add_argument("--batch")
    ap.add_argument("--move", nargs=2, action="append", metavar=("OLD", "NEW"))
    a = ap.parse_args()
    moves = batch(a.batch) if a.batch else [tuple(m) for m in (a.move or [])]
    if a.batch == "root-json":
        moves = strict_filter(moves)
    if a.batch == "small-dirs":
        DIR_MOVES.extend(SMALL_DIRS)
        # file-level token rewriting is redundant for directory batches (the D/ rule covers it) and slow: rewrite links + dir tokens only
        global DIR_ONLY
        DIR_ONLY = True
    generic = [o for o, _ in moves if os.path.basename(o) in GENERIC_NAMES]
    if generic:
        # a generic basename (main.tex lives in every paper folder) cannot be rewritten textually without hitting the others
        print(f"refusing {len(generic)} generic basename(s): {generic}")
        moves = [(o, nw) for o, nw in moves if os.path.basename(o) not in GENERIC_NAMES]
    taken = [nw for o, nw in moves if (ROOT / nw).exists() and o not in RETIRE]
    if taken:
        print(f"target collisions ({len(taken)}; skipped, and their references are left alone):", taken[:10])
        moves = [(o, nw) for o, nw in moves if not (ROOT / nw).exists() or o in RETIRE]
    if RETIRE:
        print(f"retiring {len(RETIRE)} root wrapper(s) whose module already lives at the target: {sorted(RETIRE)}")
    return run(moves, a.mode == "apply")


if __name__ == "__main__":
    sys.exit(main())
