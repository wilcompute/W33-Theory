#!/usr/bin/env python3
"""Review all reachable weekly commit diffs without touching the working tree."""
import collections, datetime, json, pathlib, re, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
SINCE="2026-11-14T00:00:00-05:00"
cmd=["git","log","master","--since="+SINCE,"--date=iso-strict","--no-ext-diff","--no-renames","--patch","--format=%x1e%H%x1f%aI%x1f%s"]
p=subprocess.Popen(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding="utf-8",errors="replace")
items=[]; curr=None; f=None; terms=("g2","hexagon","q(6,3)","w(5,3)","project","reflection","quadratic","tangent","secant","ramif","weyl","witting","clifford","pauli","qutrit","quantum","causal","chirality","spin","gravity","mass","anomal","no-go","obstruction","falsif","counterexample","fail","index","physical","tomograph","hodge","qutrit","mub","moduli","vacuum","continuum","lattice","einstein")
for line in p.stdout:
    if line.startswith("\x1e"):
        parts=line[1:].rstrip("\n").split("\x1f",2)
        if len(parts)==3:
            curr={"sha":parts[0],"date":parts[1],"subject":parts[2],"added":0,"deleted":0,"files":[],"diff_lines":0,"keywords":{},"key_lines":[]}
            items.append(curr);f=None
    elif curr is not None:
        if line.startswith("diff --git a/"):
            f=line.strip().split(" b/",1)[-1];curr["files"].append(f)
        elif line.startswith("+") and not line.startswith("+++"):
            curr["added"]+=1;curr["diff_lines"]+=1
        elif line.startswith("-") and not line.startswith("---"):
            curr["deleted"]+=1;curr["diff_lines"]+=1
        elif line.startswith((" ","@@")):
            curr["diff_lines"]+=1
        if line.startswith("+") and not line.startswith("+++"):
            low=line.lower()
            for term in terms:
                if term in low:curr["keywords"][term]=curr["keywords"].get(term,0)+1
            if len(curr["key_lines"])<9 and (("assert " in low or "theorem" in low or "obstruction" in low or "no-go" in low or "conclusion" in low) and len(line)<250):
                curr["key_lines"].append(line[1:].strip())
rc=p.wait()
if rc:raise RuntimeError(p.stderr.read()[-2000:])
group=collections.defaultdict(lambda:{"commits":0,"added":0,"deleted":0})
for x in items:
    day=x["date"][:10];group[day]["commits"]+=1;group[day]["added"]+=x["added"];group[day]["deleted"]+=x["deleted"]
names=collections.Counter(f for x in items for f in x["files"])
keywords=collections.Counter()
for x in items:keywords.update(x["keywords"])
out={"window_start":SINCE,"head":items[0]["sha"] if items else None,"count":len(items),"total_added":sum(x["added"] for x in items),"total_deleted":sum(x["deleted"] for x in items),"by_day":dict(sorted(group.items())),"file_extensions":dict(collections.Counter(pathlib.Path(f).suffix for f in names for _ in range(names[f]))),"most_changed_files":names.most_common(25),"keywords":keywords.most_common(),"commits":items}
dest=ROOT/"analysis"/"_audit_week_20261121_fullpatch_scan.json"
dest.write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps({k:v for k,v in out.items() if k!="commits"},indent=2))
print("FIRST_15",json.dumps(items[:15],indent=2)[:16000])
print("LAST_5",json.dumps(items[-5:],indent=2)[:7000])
print("AUDIT_FILE",dest)
