#!/usr/bin/env python3
"""Read every commit patch in a date window and produce a compact provenance inventory.
Does not modify the repository's tracked contents or depend on third-party packages.
This is a machine digest, not a substitute for scientific peer review of each proof.
"""
import collections, datetime, hashlib, json, pathlib, re, subprocess, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
def git(*args):
    p=subprocess.run(["git","-C",str(ROOT),*args],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
    return p.stdout
def main():
    since="2026-11-12T00:00:00"
    shas=git("rev-list","--since="+since,"master").decode().splitlines()
    categories={
      "causality_gravity":r"causal|lorentz|gravity|einstein|spacetime|dirac|overlap|spin.c|topolog|AdS|BDG|fermion|hodge",
      "matter_gauge":r"anomal|flavor|yukawa|mass|Higgs|Spin10|SU5|E6|E8|G2|Wilson|holonom|vacuum",
      "quantum_information":r"photon|qutrit|qubit|Bell|CHSH|SIC|Clifford|coheren|memory|quantum|Pauli|CSS",
      "empirical_consistency":r"DESI|ACT|BAO|CMB|neutrin|cosmolog|experiment|observ|constraint|likelihood|falsif|benchmark",
      "combinatorial":r"W33|graph|finite|geometry|group|project|Steinberg|code|polytope",
    }
    compiled={name:re.compile(p,re.I) for name,p in categories.items()}
    all_files=collections.Counter();daily=collections.Counter();hits=collections.Counter()
    res=[]; total_bytes=total_lines=0
    for j,sha in enumerate(shas):
      raw=git("show","--no-ext-diff","--format=","--find-renames","--unified=0",sha)
      total_bytes+=len(raw);total_lines+=raw.count(b"\n")
      info=git("show","-s","--format=%cI%n%s",sha).decode("utf-8","replace").splitlines()
      date=info[0][:10];title=info[1] if len(info)>1 else ""
      daily[date]+=1
      files=[]; heads=[]; functions=[]; n_add=n_del=0
      for line in raw.decode("utf-8","replace").splitlines():
        if line.startswith("+++ b/"):
          name=line[6:];files.append(name);all_files[name]+=1
        elif line.startswith("+") and not line.startswith("+++"):
          n_add+=1;s=line[1:].strip()
          if s.startswith("# ") or s.startswith("## "):
             if len(heads)<5:heads.append(s[:125])
          if re.match(r"(?:async )?def [a-zA-Z_]|class [A-Za-z_]",s):
             if len(functions)<7:functions.append(s[:100])
        elif line.startswith("-") and not line.startswith("---"):n_del+=1
      joined=title+" "+" ".join(files)+" "+" ".join(heads)
      cats=[name for name,pattern in compiled.items() if pattern.search(joined)]
      for cat in cats:hits[cat]+=1
      res.append(dict(sha=sha,date=date,title=title,files=files,add=n_add,delete=n_del,patch_sha256=hashlib.sha256(raw).hexdigest(),categories=cats,headings=heads,functions=functions))
      if (j+1)%50==0:print("READ_PATCHES",j+1,"/",len(shas),flush=True)
    out=dict(range="2026-11-12 through 2026-11-19",head=git("rev-parse","master").decode().strip(),
             commit_count=len(shas),total_patch_bytes=total_bytes,total_patch_lines=total_lines,
             daily=dict(sorted(daily.items())),category_occurrences=dict(hits),
             unique_changed_paths=len(all_files),
             frequently_changed_paths=all_files.most_common(25),commits=res)
    path=ROOT/"analysis"/"2026-11-19_weekly_commit_audit_v2.json"
    path.write_text(json.dumps(out,indent=2),encoding="utf-8")
    print("AUDIT_OUTPUT",path,"size",path.stat().st_size)
    print("SUMMARY",json.dumps({k:v for k,v in out.items() if k!="commits"},indent=2),flush=True)
    print("LATEST_12",json.dumps(res[:12],indent=2)[:9000],flush=True)
if __name__=="__main__":main()
