#!/usr/bin/env python3
"""Machine-auditable whole-paper + whole-week source inventory; read-only inputs.
All PDF page text and every git patch are consumed, hashed, and indexed.
This is source inventory, not a proof that all claims are true.
"""
import collections, datetime, hashlib, json, re, subprocess
from pathlib import Path
import fitz

ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/"papers"/"forty_points"/"main.pdf"
DEST=ROOT/"data"/"toe_20261119_paper_week_full_audit.json"
CONCEPTS=("H27","SIC","D-flat","F-flat","G2","G_2","E6","E_6","E8","E_8",
          "photon","localiz","chiral","proton","vacuum","M-theory","fermion",
          "index","time","Lorentz","Einstein","qutrit","flux","anomal")
def git(*args):
    r=subprocess.run(["git",*args],cwd=ROOT,capture_output=True,check=True)
    return r.stdout

doc=fitz.open(PDF)
page_info=[]
text_digest=hashlib.sha256()
for i,page in enumerate(doc):
    txt=page.get_text("text",sort=True)
    text_digest.update(txt.encode("utf-8"))
    lines=[x.strip() for x in txt.splitlines() if x.strip()]
    counts={c:len(re.findall(re.escape(c),txt,re.I)) for c in CONCEPTS}
    page_info.append(dict(page=i+1,characters=len(txt),sha256=hashlib.sha256(txt.encode()).hexdigest(),
                          start=" ".join(lines[:3])[:220],
                          active_terms={k:v for k,v in counts.items() if v},
                          flags={k:len(re.findall(r"\\b"+k+r"\\b",txt)) for k in ("OPEN","THEOREM","COMPUTATION","INTERPRETATION","BRIDGE")}))
commits=git("log","master","--since=2026-11-11T00:00:00-05:00",
            "--until=2026-11-19T00:00:00-05:00","--format=%H").decode().splitlines()
changed=collections.Counter()
theme=collections.Counter()
rows=[]
for ix,sha in enumerate(commits):
    meta=git("show","-s","--format=%cI%n%s",sha).decode("utf-8","replace").splitlines()
    patch=git("show","--format=","--no-ext-diff","--unified=0",sha)
    # this consumes the COMPLETE unified diff, including all changed-file hunks.
    text=patch.decode("utf-8","replace")
    paths=re.findall(r"(?m)^diff --git a/(.*?) b/(.*?)$",text)
    by_path=[b for a,b in paths]
    changed.update(by_path)
    concepts={c:len(re.findall(re.escape(c),text,re.I)) for c in CONCEPTS}
    theme.update({c:v for c,v in concepts.items() if v})
    rows.append(dict(sha=sha,date=meta[0] if meta else "",title=meta[1] if len(meta)>1 else "",
                     patch_bytes=len(patch),patch_sha256=hashlib.sha256(patch).hexdigest(),
                     files=by_path,hot_topics={k:v for k,v in concepts.items() if v}))
    if (ix+1)%50==0: print("SCANNED",ix+1,"of",len(commits),flush=True)
result=dict(pdf_path=str(PDF),pdf_sha256=hashlib.sha256(PDF.read_bytes()).hexdigest(),
            pdf_page_count=len(doc),pdf_text_characters=sum(x["characters"] for x in page_info),
            pdf_extracted_text_sha256=text_digest.hexdigest(),
            pdf_pages=page_info,commit_count=len(commits),head=git("rev-parse","master").decode().strip(),
            total_patch_bytes=sum(x["patch_bytes"] for x in rows),
            top_changed_files=changed.most_common(50),term_frequency=theme.most_common(),
            weekly_commits=rows)
DEST.parent.mkdir(parents=True,exist_ok=True)
DEST.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"pdf_pages":len(doc),"pdf_characters":result["pdf_text_characters"],
                  "commits":len(commits),"patch_megabytes":round(result["total_patch_bytes"]/1000000,3),
                  "head":result["head"],"output":str(DEST)},indent=2))
