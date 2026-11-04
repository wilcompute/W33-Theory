#!/usr/bin/env python3
"""Historical five-front keyword census across tracked text, not semantic review.

Produces full *path* hit lists and bounded inspection priorities, avoids implying
that code search catches all related concepts or proves novelty. Git history
subjects are independently searched through git log.
"""
from __future__ import annotations
import json,subprocess,re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261104_corpus_archaeology.json"
FRONTS={
    "dimension":r"causal.set|causal.growth|spectral.dimension|Hausdorff.dimension|Pachner|Regge|Lorentzian|4D.spacetime|dimensional.flow",
    "symmetry":r"apartment|Steinberg|spectral.sparsif|tight.frame|symplectic.transvection|C3.equivarian|cycle.Hamiltonian",
    "gravity":r"hypersurface.deformation|first.class|constraint.algebra|ADM.constraint|spin.2|perfect.action|Regge",
    "flavor":r"Nelson.Barr|strong.CP|vector.like|vectorlike|Yukawa|Jarlskog|CKM|fermion.generation",
    "hardware":r"Lindblad|Ramsey|Trotter|synthetic.flux|photonic.circuit|signed.hopping|pulse.compilation|homodyne",
}
SUBTREES=["analysis/","papers/","tests/","docs/"]
def git(*args,timeout=240):
    p=subprocess.run(["git","-C",str(ROOT),*args],text=True,stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,errors="replace",timeout=timeout)
    if p.returncode:raise RuntimeError(f"{args} => {p.returncode}: {p.stderr[:600]}")
    return p.stdout
def rank(path,front):
    txt=path.lower()
    key={
        "dimension":("causal","spacetime","regge","h4","pachner","dimension","topology"),
        "symmetry":("apartment","steinberg","cycle","spars","equivarian","frame"),
        "gravity":("constraint","adm","spin2","spin_2","gravity","regge"),
        "flavor":("nelson","strong_cp","vectorlike","flavor","yukawa","chirality","ckm"),
        "hardware":("lindblad","ramsey","trotter","photonic","hopping","hardware","optics"),
    }[front]
    return sum(4 for t in key if t in txt)+(5 if txt.endswith(".py") else 2 if txt.endswith(".md") else 0)+(2 if "/pass" in txt or "w33_pass" in txt else 0)
def main():
    out={"status":"PASS_TRACKED_PATH_CENSUS_NOT_EXHAUSTIVE_SEMANTIC_READ",
         "repo_files":len(git("ls-files").splitlines()),
         "head_sha":git("rev-parse","HEAD").strip(),
         "commit_count":int(git("rev-list","--count","HEAD").strip()),
         "searched_subtrees":SUBTREES,"fronts":{}}
    for front,pattern in FRONTS.items():
        print("SEARCH",front,flush=True)
        paths=sorted(set(p for p in git("grep","-l","-i","-E","-e",pattern,"--",*SUBTREES,timeout=300).splitlines() if p))
        by_ext=Counter(Path(p).suffix.lower() for p in paths)
        by_root=Counter(p.split("/")[0] for p in paths)
        ranking=sorted(paths,key=lambda p:(-rank(p,front),p))
        before=git("log","--all","-i","--extended-regexp","--before=2026-10-01",
                   "--grep",pattern,"--date=short","--format=%h %ad %s",timeout=180).splitlines()
        recent=git("log","--all","-i","--extended-regexp","--since=2026-10-01",
                   "--grep",pattern,"--date=short","--format=%h %ad %s",timeout=180).splitlines()
        out["fronts"][front]={
            "regexp":pattern,
            "tracked_text_path_hits":len(paths),
            "by_extension":dict(by_ext),
            "by_top_dir":dict(by_root),
            "all_matching_paths":paths,
            "top_ranked_filename_hints":ranking[:100],
            "commit_subject_matches_before_october_count":len(before),
            "commit_subject_matches_since_october_count":len(recent),
            "earlier_commit_subject_samples":before[:40],
            "recent_commit_subject_samples":recent[:25],
            "search_limitations":"Path hits are broad keyword occurrences; not unique substantive prior art. Commit subjects may omit material inside commit diffs. No semantic novelty inference."
        }
        print("MATCHED",front,len(paths),"older commits",len(before),"recent commits",len(recent),flush=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("WROTE",OUT,flush=True)
if __name__=="__main__":main()
