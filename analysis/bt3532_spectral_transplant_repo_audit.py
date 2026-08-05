#!/usr/bin/env python3
"""Repository-wide policy audit for W33 -> Gewirtz spectral transplantation.

The scanner records every textual context containing "Gewirtz" in source-like
files and classifies the context.  It fails closed only for explicit AUTO_PORT
annotations: such a claim must be polynomial-only.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

EXTENSIONS={".py",".md",".tex",".html",".json",".txt",".lean",".v"}
POLY=("x^2+2x-8","x^2 + 2*x - 8","a^2+2a-8i",
      "(a-2i)(a+4i)","u^2=i","functional calculus","adjacency polynomial")
MULT=("multiplicit","trace","determinant","rank","dimension","p-rank","smith")
GEOM=("line","incidence","symplectic","automorphism","clique","code",
      "descendant","intertwiner","subconstituent","projective")

def classify(text:str)->list[str]:
    s=" ".join(text.lower().split())
    cats=[]
    if any(token in s for token in POLY):
        cats.append("polynomial_only")
    if any(token in s for token in MULT):
        cats.append("multiplicity_sensitive")
    if any(token in s for token in GEOM):
        cats.append("geometry_sensitive")
    if not cats:
        cats.append("context_only")
    return cats

def scan(root:Path):
    rows=[]
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        if any(part in {".git","evidence","__pycache__"} for part in path.parts):
            continue
        try:
            lines=path.read_text(encoding="utf-8",errors="ignore").splitlines()
        except OSError:
            continue
        for i,line in enumerate(lines):
            if "gewirtz" not in line.lower():
                continue
            lo=max(0,i-3); hi=min(len(lines),i+4)
            context="\n".join(lines[lo:hi])
            cats=classify(context)
            if "AUTO_PORT" in context and cats != ["polynomial_only"]:
                raise AssertionError(f"unsafe AUTO_PORT at {path}:{i+1}: {cats}")
            rows.append({
                "path":str(path.relative_to(root)),
                "line":i+1,
                "categories":cats,
                "context":context[:1200],
            })
    return rows

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json",type=Path)
    args=parser.parse_args()
    rows=scan(args.root)
    counts={}
    for row in rows:
        for cat in row["categories"]:
            counts[cat]=counts.get(cat,0)+1
    result={
        "status":"PASS_SPECTRAL_TRANSPLANT_POLICY_AUDIT",
        "contexts":len(rows),
        "category_counts":counts,
        "rows":rows,
        "policy":{
            "automatic":"polynomial_only",
            "new_evidence_required":["multiplicity_sensitive","geometry_sensitive"],
        },
    }
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(result["status"],counts,"contexts",len(rows))

if __name__=="__main__":
    main()
