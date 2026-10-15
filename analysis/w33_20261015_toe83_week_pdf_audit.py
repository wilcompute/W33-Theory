"""Audit every page of forty_points/main.pdf and every week's commit file change.

Requires Poppler pdftotext on the authorized local Windows machine.
This is a completeness/index audit, not an endorsement of each physical claim.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import datetime,hashlib,json,re,subprocess,sys

ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/"papers/forty_points/main.pdf"
EXE=Path(r"C:\Users\wiljd\AppData\Local\Microsoft\WinGet\Packages\oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe\poppler-25.07.0\Library\bin\pdftotext.exe")
def run():
    assert PDF.is_file() and EXE.is_file()
    raw=subprocess.run([str(EXE),"-layout","-enc","UTF-8",str(PDF),"-"],
                       capture_output=True,check=True).stdout.decode("utf8")
    pages=raw.split("\f")
    if not pages[-1].strip():pages.pop()
    assert len(pages)==182,(len(pages),PDF)
    tokens=("W(3,3)","qutrit","self-entanglement","Heisenberg","CSS",
            "Steinberg","E_8","E_6","Lorentz","falsif","proton","open")
    page_data=[]
    for i,page in enumerate(pages,1):
        lines=[x.strip() for x in page.splitlines() if x.strip()]
        page_data.append({"page":i,"characters":len(page),
            "sha256":hashlib.sha256(page.encode()).hexdigest(),
            "lead":lines[:2],
            "topics":{w:len(re.findall(re.escape(w),page,re.I)) for w in tokens if re.search(re.escape(w),page,re.I)}})
    assert all(x["characters"]>40 for x in page_data)
    since="2026-10-08 00:00:00"
    log=subprocess.run(["git","log",f"--since={since}","--format=COMMIT:%H|%aI|%s","--name-status"],
                       cwd=ROOT,capture_output=True,check=True).stdout.decode("utf8",errors="replace")
    commits=[];cur=None;ext=Counter()
    for line in log.splitlines():
        if line.startswith("COMMIT:"):
            if cur:commits.append(cur)
            sha,date,subject=line[7:].split("|",2)
            cur={"sha":sha,"date":date,"subject":subject,"files":[]}
        elif cur and re.match(r"^[AMDRC]\d*\s+",line):
            name=line.split("\t")[-1]
            cur["files"].append(name)
            ext[Path(name).suffix.lower() or "(none)"]+=1
    if cur:commits.append(cur)
    assert len(commits)>=630,len(commits)
    names=Counter(c["date"][:10] for c in commits)
    risk=re.compile(r"correction|refut|no.go|firewall|fail|withdraw|retract",re.I)
    flagged=[{"sha":c["sha"][:12],"subject":c["subject"]} for c in commits if risk.search(c["subject"])]
    # All commit metadata and every changed path are scanned; the full patch
    # is separately indexed by local Git. No claims of manual 635-diff proof.
    summary={
      "status":"PAGE_AND_COMMIT_COMPLETENESS_AUDIT",
      "date":"2026-10-15",
      "pdf":{"path":"papers/forty_points/main.pdf","pages":len(pages),
             "characters":len(raw),"sha256":hashlib.sha256(PDF.read_bytes()).hexdigest(),
             "all_pages_nonempty":True,
             "topic_page_counts":{w:sum(w in p["topics"] for p in page_data) for w in tokens},
             "pages":page_data},
      "git":{"since":since,"commits":len(commits),"by_day":dict(sorted(names.items())),
             "changed_file_occurrences":sum(len(c["files"]) for c in commits),
             "changed_extension_counts":dict(ext.most_common()),
             "risk_subjects":flagged[:80],
             "first_sha":commits[0]["sha"],"last_sha":commits[-1]["sha"],
             "full_metadata_paths_scanned":True,
             "manual_line_by_line_diff_verification":False},
      "limitation":"PDF full text/page digest and every commit metadata/path indexed; this is not peer review of every equation, line of code, or physics claim."}
    dest=ROOT/"data/w33_20261015_toe83_week_pdf_audit.json"
    dest.write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    print("PDF pages",len(pages),"chars",len(raw),"commits",len(commits),"files",summary["git"]["changed_file_occurrences"])
    print("TOPICS",summary["pdf"]["topic_page_counts"])
    print("RECENT",names.most_common(8))
    print("FLAGGED",len(flagged))
    return summary
if __name__=="__main__":run()
