"""Full-byte provenance audit of commits and revised files since PR324."""
from __future__ import annotations
import ast,collections,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE="9e2f9b9e859ee4d7b39555c0052886653a90e3be"
def git(*args, binary=False):
    p=subprocess.run(["git","-C",str(ROOT),*args],capture_output=True)
    if p.returncode:raise RuntimeError((args,p.stderr.decode(errors="replace")[:500]))
    return p.stdout if binary else p.stdout.decode("utf-8",errors="replace").strip()
def classify(path,data):
    x={"path":path,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),
       "lines":data.count(b"\n")+int(not data.endswith(b"\n"))}
    try:
        s=data.decode("utf-8")
        if path.endswith(".json"):
            o=json.loads(s)
            x.update(kind="JSON",top_keys=list(o)[:25] if isinstance(o,dict) else [],length=len(o))
        elif path.endswith(".py"):
            t=ast.parse(s,path)
            x.update(kind="Python",functions=[z.name for z in t.body if isinstance(z,(ast.FunctionDef,ast.ClassDef))][:35])
        elif path.endswith(".md"):
            x.update(kind="Markdown",headings=[q for q in s.splitlines() if q.startswith("#")][:28])
        else:x["kind"]="Text"
    except UnicodeDecodeError:x["kind"]="Binary"
    except Exception as e:x["parse_error"]=str(e)[:160]
    return x
def main():
    head=git("rev-parse","HEAD")
    commits=git("rev-list","--reverse",BASE+".."+head).splitlines()
    lines=git("diff","--name-status",BASE,head).splitlines()
    paths=[x.split("\t")[-1] for x in lines if not x.startswith("D")]
    versions=[];failures=[];total=0;count=0
    for sha in commits:
        msg=git("show","-s","--format=%H%n%aI%n%B",sha)
        parents=git("rev-list","--parents","-n","1",sha).split()
        change=git("diff","--name-status",parents[1],sha).splitlines() if len(parents)>1 else []
        blobs=[]
        for line in change:
            if line.startswith("D"):continue
            path=line.split("\t")[-1]
            try:
                b=git("show",sha+":"+path,binary=True)
                total+=len(b);count+=1
                o=classify(path,b);blobs.append(o)
                if o.get("parse_error"):failures.append(sha[:9]+" "+path+" "+o["parse_error"])
            except Exception as e:failures.append(sha[:9]+" "+path+" "+str(e)[:100])
        versions.append({"sha":sha,"parents":parents[1:],"full_message":msg,"blobs":blobs})
    final=[]
    for path in sorted(paths):
        file=ROOT/path
        if file.is_file():
            o=classify(path,file.read_bytes());final.append(o)
            if o.get("parse_error"):failures.append("Final "+path+" "+o["parse_error"])
        else:failures.append("Final missing "+path)
    out={"schema":"w33.20261109.postpr324.fullbyte.change_audit.v1",
         "base":BASE,"head":head,"commits":len(commits),"versioned_file_reads":count,
         "revision_bytes_read":total,"whole_final_files_read":len(final),
         "final_file_bytes":sum(x["bytes"] for x in final),
         "versions":versions,"final_files":final,"failures":failures,
         "limit":"Machine-read and parsed all complete accessible changed blobs; not independent semantic mathematical validation."}
    (ROOT/"data/toe_20261109_postpr324_fullbyte_audit.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    c=collections.Counter(x["kind"] for z in versions for x in z["blobs"])
    md=["# Full-byte changed revision audit after PR324","",
        "Baseline: "+BASE,"HEAD: "+head,
        "Complete commit messages: "+str(len(versions))+". Full versioned blobs: "+str(count)+", "+str(total)+" bytes.",
        "Whole final changed files: "+str(len(final))+", "+str(out["final_file_bytes"])+" bytes.",
        "Full commit text and per-blob SHA256 hashes and Python/JSON parse checks in data/toe_20261109_postpr324_fullbyte_audit.json.",
        "Parsed revision classes: "+str(dict(c))+". Errors: "+str(len(failures))+".",
        "This is a lossless structural audit, not a semantic certification of mathematical or physical results.","",
        "## Entire intervening commit list",""]
    for x in versions:
        ls=x["full_message"].splitlines()
        title=ls[2] if len(ls)>2 else (ls[-1] if ls else "")
        md.append("- "+x["sha"][:12]+" | "+str(len(x["blobs"]))+" blobs | "+title[:240].rstrip())
    md+=["","## Every final changed file",""]
    for x in final:md.append("- "+x["path"]+" | "+str(x["bytes"])+" bytes | "+str(x["lines"])+" lines | "+x["sha256"][:20]+" | "+x["kind"])
    md+=["","## Structural parse failures",""]+ (["- "+x for x in failures] if failures else ["None"])
    (ROOT/"analysis/PASS20261109_POST_PR324_FULLBYTE_CHANGE_AUDIT.md").write_text("\n".join(md)+"\n",encoding="utf-8")
    print(json.dumps({k:out[k] for k in ("head","commits","versioned_file_reads","revision_bytes_read","whole_final_files_read","final_file_bytes","failures")},indent=2))
if __name__=="__main__":main()
