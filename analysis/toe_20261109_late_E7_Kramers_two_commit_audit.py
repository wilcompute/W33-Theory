"""Full-byte late-commit addendum without modifying frozen initial 43-commit receipt."""
from __future__ import annotations
import ast,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE="3b8f728dd45289e77e11bc3196576077d7eb4643"
def run(*args,bytes_=False):
    p=subprocess.run(["git","-C",str(ROOT),*args],capture_output=True)
    assert p.returncode==0,p.stderr[:200]
    return p.stdout if bytes_ else p.stdout.decode(errors="replace").strip()
def main():
    head=run("rev-parse","HEAD")
    commits=run("rev-list","--reverse",BASE+".."+head).splitlines()
    out=[];fail=[];nbytes=0;filecount=0
    for sha in commits:
        parents=run("rev-list","--parents","-n","1",sha).split()
        paths=run("diff","--name-status",parents[1],sha).splitlines()
        files=[]
        for row in paths:
            if row.startswith("D"):continue
            path=row.split("\t")[-1]
            b=run("show",sha+":"+path,bytes_=True)
            nbytes+=len(b);filecount+=1
            x=dict(path=path,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
            try:
                txt=b.decode("utf-8")
                if path.endswith(".json"):json.loads(txt)
                if path.endswith(".py"):ast.parse(txt,filename=path)
                x["complete_utf8_parsed"]=True
            except Exception as e:
                x["complete_utf8_parsed"]=False;fail.append((path,str(e)))
            files.append(x)
        out.append(dict(sha=sha,full_commit_message=run("show","-s","--format=%B",sha),files=files))
    assert len(commits)==2 and not fail
    result=dict(baseline=BASE,head=head,commits=out,revision_count=filecount,
                revision_bytes=nbytes,errors=fail,
                scope="All added commit messages and complete modified file revisions read; not all physics claims semantically validated")
    dest=ROOT/"data/toe_20261109_late_E7_Kramers_two_commit_audit.json"
    dest.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(dict(head=head,commits=len(commits),files=filecount,bytes=nbytes,errors=fail)))
if __name__=="__main__":main()
