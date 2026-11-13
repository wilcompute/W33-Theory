"""Reproducible, read-only audit of recent W33 commits and Forty Points PDF."""
from pathlib import Path
import collections, datetime, hashlib, json, re, subprocess, sys
import fitz

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "papers" / "forty_points" / "main.pdf"
OUT = ROOT / "data" / "toe_20261113_week_pdf_audit.json"
SINCE = "2026-11-06T00:00:00-05:00"

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, stderr=subprocess.DEVNULL)

pdf = fitz.open(PDF)
pages = []
body_sha = hashlib.sha256()
for idx, page in enumerate(pdf):
    s = page.get_text(sort=True)
    body_sha.update(s.encode("utf-8"))
    lines = [re.sub(r"\s+", " ", z).strip() for z in s.splitlines()]
    lines = [z for z in lines if z]
    pages.append({
        "page": idx + 1, "chars": len(s), "sha256": hashlib.sha256(s.encode("utf-8")).hexdigest(),
        "head": lines[:5],
        "badge_counts": {k:len(re.findall(r"\b"+k+r"\b",s,re.I)) for k in ("THEOREM","COMPUTATION","BRIDGE","OPEN","REFUTED")},
        "script_mentions": sorted(set(re.findall(r"w33_pass\d{4,6}_[A-Za-z_0-9]+\.py",s)))[:24]
    })
shas = git("rev-list", "--since="+SINCE, "master").decode().splitlines()
commits=[]
tokens=collections.Counter()
paths=collections.Counter()
part_ext=collections.Counter()
date_count=collections.Counter()
corrections=[]
for i, sha in enumerate(shas):
    raw=git("show","-s","--format=%aI%x1f%B",sha).decode("utf-8","replace")
    timestamp,message=raw.split("\x1f",1)
    files=git("diff-tree","--root","--no-commit-id","--name-only","-r",sha).decode("utf-8","replace").splitlines()
    for path in files:
        paths[path]+=1
        part_ext[Path(path).suffix.lower() or "[none]"]+=1
    date_count[timestamp[:10]]+=1
    msg=re.sub(r"\s+"," ",message).strip()
    for w in re.findall(r"[A-Za-z][A-Za-z0-9_-]{4,}",msg.lower()):
        tokens[w]+=1
    if any(w in msg.lower() for w in ("withdraw", "correct", "failed", "refut", "no-go","invalid","not proved","unsupported")):
        corrections.append({"sha":sha[:12],"date":timestamp[:10],"message":msg[:390]})
    commits.append({"sha":sha,"date":timestamp,"subject":msg[:280],"files":files})
    if (i+1)%50==0:
        print("indexed_commits",i+1,flush=True)
result={
 "audit_scope":{"since":SINCE,"head":git("rev-parse","master").decode().strip(),"commit_count":len(shas)},
 "pdf":{"path":str(PDF),"pages":len(pdf),"bytes_sha256":hashlib.sha256(PDF.read_bytes()).hexdigest(),
        "all_page_text_sha256":body_sha.hexdigest(),"all_pages":pages},
 "commit_dates":dict(date_count),"extensions":part_ext.most_common(),
 "most_touched_files":paths.most_common(65),
 "frequent_subject_words":tokens.most_common(65),
 "correction_subjects":corrections[:75],
 "all_commits":commits
}
OUT.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding="utf-8")
print("PDF_PAGES",len(pdf),"TEXT_CHARS",sum(x["chars"] for x in pages),"PDF_SHA256",result["pdf"]["bytes_sha256"])
print("COMMITS",len(commits),"DATE_COUNTS",dict(date_count))
print("TOP_PATHS",paths.most_common(15))
print("CORRECTION_MESSAGES",len(corrections))
print("OUTPUT",OUT)