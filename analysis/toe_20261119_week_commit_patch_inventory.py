"""Full-patch machine inventory of the seven-day W33 master history.
This is an exhaustive input scan, NOT a human proof review of every changed line.
"""
from pathlib import Path
from collections import Counter
import hashlib, json, re, subprocess

ROOT=Path(__file__).resolve().parents[1]
CUTOFF="2026-11-11 22:49:00 -0500"
def git(*args):
    return subprocess.run(["git","-C",str(ROOT),*args],capture_output=True,check=True).stdout
log=git("log","master",f"--since={CUTOFF}","-p","--no-color","--no-ext-diff","--format=__AUDIT_COMMIT__%H|%aI|%s")
parts=log.split(b"__AUDIT_COMMIT__")
records=[]
topic_counts=Counter()
for part in parts[1:]:
    line,sep,patch=part.partition(b"\n")
    fields=line.decode("utf-8","replace").split("|",2)
    if len(fields)!=3: continue
    sha,when,title=fields
    paths=[x.decode("utf-8","replace") for x in re.findall(rb"^diff --git a/(.*?) b/.*?$",patch,re.M)]
    low=patch.lower()
    hits=[key for key,regex in {
      "G2_holonomy":rb"g_?2|torsion.free|spin.?7",
      "E8_E6_group":rb"e_?8|e_?6|albert|freudenthal",
      "qutrit_SIC":rb"qutrit|sic.povm|h27|hesse",
      "quantum_geometry":rb"clifford|contextuality|qudit|tqft",
      "spacetime_gravity":rb"einstein|ads4|m.theory|flux|dirac",
      "phenomenology":rb"yukawa|mass|proton|higgs|vacuum",
      "computing":rb"photoni|holonet|memory|circuit|process.tensor",
    }.items() if re.search(regex,low)]
    topic_counts.update(hits)
    records.append({
      "sha":sha,"datetime":when,"title":title,
      "patch_bytes":len(patch),"patch_sha256":hashlib.sha256(patch).hexdigest(),
      "changed_files":paths,"topic_flags":hits,
      "added_lines":len(re.findall(rb"^\+(?!\+)",patch,re.M)),
      "deleted_lines":len(re.findall(rb"^-(?!-)",patch,re.M)),
    })
assert len(records)==len(git("rev-list","master",f"--since={CUTOFF}").splitlines())
tot=sum(z["patch_bytes"] for z in records)
repo_head=git("rev-parse","master").decode().strip()
output={
 "cutoff_local":CUTOFF,
 "master_head":repo_head,
 "commit_count":len(records),
 "total_patch_bytes_read":tot,
 "full_log_sha256":hashlib.sha256(log).hexdigest(),
 "topic_counts":dict(topic_counts),
 "top_patch_sizes":[{"sha":x["sha"],"title":x["title"],"bytes":x["patch_bytes"]} for x in sorted(records,key=lambda x:x["patch_bytes"],reverse=True)[:15]],
 "recent_20":records[:20],
 "all_commits":records
}
target=ROOT/"data"/"toe_20261119_week_commit_patch_inventory.json"
target.write_text(json.dumps(output,indent=2)+"\n",encoding="utf-8")
print("PASS",len(records),"commits",tot,"patch bytes",len(set(f for r in records for f in r["changed_files"])),"unique paths")
print("TOPICS",dict(topic_counts))
print("HEAD",repo_head,"DIGEST",output["full_log_sha256"])
print("LARGEST",[(x["sha"][:8],x["patch_bytes"],x["title"][:52]) for x in sorted(records,key=lambda r:r["patch_bytes"],reverse=True)[:10]])
