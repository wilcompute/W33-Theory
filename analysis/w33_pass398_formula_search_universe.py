#!/usr/bin/env python3
"""Pass 398: freeze the repository-wide numerical physics formula universe.

The output is the multiplicity denominator required before a numerical match
can receive out-of-sample credit. It records exact and structural families,
source locations, nearby status language, and all numerical literals.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import tempfile
import unicodedata
from collections import Counter,defaultdict
from dataclasses import dataclass
from pathlib import Path

SCHEMA="w33.formula-search-universe.v1"
DEFAULT_GLOBS=["docs/index.html","*.tex","analysis/*.md","analysis/*.py","analysis/*.g","passes/*.md","passes/*.py","passes/*.g","exploration/*.py","exploration/*.g","scripts/*.py","scripts/*.g","PASS*.md","AUDIT*.md","BT*.md","PART*.md","formal/**/*.lean","manuscripts/**/*.tex","papers/**/*.tex"]
SKIP_DIRS={".git",".venv","venv","node_modules","data","artifacts","__pycache__",".pytest_cache","build","dist"}
SKIP_FILES={"RESULTS_INDEX.md","w33_formula_search_universe_v1.json"}
PHYSICS_MARKERS=re.compile(r"(?i)(?:alpha|fine[- ]structure|weinberg|cabibbo|ckm|pmns|koide|mixing|mass(?:es)?|yukawa|neutrino|lepton|quark|fermion|boson|proton|decay|lifetime|coupling|gauge|standard model|electroweak|strong angle|weak angle|theta|sin|cos|tan|vev|higgs|cosmolog|hubble|dark energy|dark matter|vacuum|seesaw|observable|experimental|measured|pdg|gev|mev|tev|ev\b|visibility|choi|chern|conductance|temperature|entropy|\bG_F\b|\bV_[a-zA-Z]|m_[a-zA-Z]|\\alpha|\\theta|\\sin|\\cos)")
RELATION_MARKERS=re.compile(r"(?:=|≈|≃|~|\\approx|\\simeq|\\sim|\\equiv|<|>)")
NUMBER=re.compile(r"(?<![A-Za-z_])[-+]?(?:\d+(?:\.\d+)?(?:[eE][-+]?\d+)?|\.\d+)")
MATH_PATTERNS=[("tex_display",re.compile(r"\\\[(.{1,1600}?)\\\]",re.S)),("tex_paren",re.compile(r"\\\((.{1,1200}?)\\\)",re.S)),("tex_environment",re.compile(r"\\begin\{(?:equation\*?|align\*?|gather\*?)\}(.{1,2400}?)\\end\{(?:equation\*?|align\*?|gather\*?)\}",re.S)),("inline_math",re.compile(r"(?<!\$)\$(?!\$)(.{1,800}?)(?<!\$)\$(?!\$)",re.S))]
STATUS_RULES=[("killed_or_retracted",re.compile(r"(?i)\b(killed|withdrawn|retracted|refuted|false|dead end|tautolog)\b")),("preregistered",re.compile(r"(?i)\b(preregister\w*|prospective|holdout|out[- ]of[- ]sample)\b")),("open_or_conditional",re.compile(r"(?i)\b(open|conjectur|conditional|ansatz|hypothes)\b")),("certified_or_theorem",re.compile(r"(?i)\b(theorem|proved|proven|certificate|certified|verified exact)\b")),("retrospective_fit",re.compile(r"(?i)\b(fit|matches data|measured|observed|pdg|empirical|numerolog)\b"))]

@dataclass(frozen=True)
class Occurrence:
    path:str; line:int; category:str; raw:str; context:str; status:str


def sha256_text(text): return hashlib.sha256(text.encode()).hexdigest()
def normalize_space(text): return " ".join(text.split())

def normalize_formula(raw):
    text=unicodedata.normalize("NFKC",html.unescape(raw))
    for old,new in {"\\left":"","\\right":"","\\,":"","\\;":"","\\!":"","\\approx":"≈","\\simeq":"≈","\\sim":"~","\\equiv":"≡","**":"^","==":"=","{,}":"","&":""}.items(): text=text.replace(old,new)
    text=re.sub(r"%.*","",text); text=re.sub(r"\s+","",text)
    return text.strip("`$.,;:")[:2000]

def structural_formula(normalized): return NUMBER.sub("#",normalized)
def status_from_context(context):
    for status,rule in STATUS_RULES:
        if rule.search(context): return status
    return "unclassified"
def line_number(text,offset): return text.count("\n",0,offset)+1
def candidate(raw,context): return bool(NUMBER.search(raw) and RELATION_MARKERS.search(raw) and PHYSICS_MARKERS.search(raw+" "+context))


def extract_occurrences(path,root):
    text=path.read_text(encoding="utf-8",errors="ignore"); rel=path.relative_to(root).as_posix(); found={}
    for category,pattern in MATH_PATTERNS:
        for match in pattern.finditer(text):
            raw=match.group(1); start=max(0,match.start()-320); end=min(len(text),match.end()+320); context=normalize_space(text[start:end])[:1200]
            line_start=text.rfind("\n",0,match.start())+1; line_end=text.find("\n",match.end()); line_end=len(text) if line_end<0 else line_end
            if candidate(raw,context):
                occurrence=Occurrence(rel,line_number(text,match.start()),category,normalize_space(raw)[:1000],context,status_from_context(text[line_start:line_end]))
                found[(occurrence.line,normalize_formula(occurrence.raw))]=occurrence
    offset=0
    for number,raw_line in enumerate(text.splitlines(keepends=True),start=1):
        line=raw_line.rstrip("\r\n"); balanced=bool(re.search(r"(?<!\$)\$(?!\$).{1,800}(?<!\$)\$(?!\$)",line))
        if len(line)<=2000 and not balanced and candidate(line,line):
            context=normalize_space(text[max(0,offset-320):min(len(text),offset+len(raw_line)+320)])[:1200]
            occurrence=Occurrence(rel,number,"relation_line",normalize_space(line)[:1000],context,status_from_context(context))
            found.setdefault((number,normalize_formula(occurrence.raw)),occurrence)
        offset+=len(raw_line)
    return sorted(found.values(),key=lambda item:(item.line,item.category,item.raw))


def corpus_files(root):
    files=set()
    for glob in DEFAULT_GLOBS:
        for path in root.glob(glob):
            if path.is_file() and path.name not in SKIP_FILES and not any(part in SKIP_DIRS for part in path.relative_to(root).parts): files.add(path)
    return sorted(files)


def build_universe(root,repository_head,frozen_at):
    files=corpus_files(root); exact=defaultdict(list); structural=defaultdict(set); scanned_bytes=occurrence_count=0
    for path in files:
        scanned_bytes+=path.stat().st_size
        for occurrence in extract_occurrences(path,root):
            normalized=normalize_formula(occurrence.raw)
            if normalized:
                exact[normalized].append(occurrence); structural[structural_formula(normalized)].add(normalized); occurrence_count+=1
    families=[]
    for normalized,occurrences in sorted(exact.items()):
        structure=structural_formula(normalized); statuses=Counter(item.status for item in occurrences); paths=sorted({item.path for item in occurrences})
        families.append({"formula_id":sha256_text(normalized),"structural_family_id":sha256_text(structure),"normalized_formula":normalized,"structural_formula":structure,"numeric_literals":sorted(set(NUMBER.findall(normalized))),"occurrence_count":len(occurrences),"file_count":len(paths),"source_files":paths,"source_locations":[{"path":item.path,"line":item.line,"category":item.category,"status":item.status,"raw":item.raw} for item in occurrences],"status_profile":dict(sorted(statuses.items())),"prospective_credit_default":"ineligible_until_registry_entry_freezes_data_and_null_family"})
    structural_families=[{"structural_family_id":sha256_text(structure),"structural_formula":structure,"exact_member_count":len(members),"exact_formula_ids":[sha256_text(member) for member in sorted(members)]} for structure,members in sorted(structural.items())]
    status_totals=Counter()
    for family in families: status_totals.update(family["status_profile"])
    payload={"schema":SCHEMA,"pass":398,"title":"Frozen repository-wide numerical physics formula universe","repository_head":repository_head,"frozen_at":frozen_at,"scanner_policy":{"globs":DEFAULT_GLOBS,"skip_dirs":sorted(SKIP_DIRS),"required_features":["physics marker","numerical literal","relation operator"],"principle":"Broad inclusion: false positives are retained; absent formulas cannot receive prospective credit until regeneration and multiplicity accounting."},"summary":{"files_scanned":len(files),"bytes_scanned":scanned_bytes,"formula_occurrences":occurrence_count,"exact_formula_families":len(families),"structural_families":len(structural_families),"status_occurrences":dict(sorted(status_totals.items()))},"exact_families":families,"structural_families":structural_families}
    payload["universe_sha256"]=sha256_text(json.dumps(payload,sort_keys=True,separators=(",",":")))
    return payload


def self_test():
    with tempfile.TemporaryDirectory() as temporary:
        root=Path(temporary); (root/"analysis").mkdir()
        (root/"analysis"/"one.md").write_text("The retrospective fit gives $\\alpha^{-1}=137.036$ from measured data.\nA preregistered target is $V(F_3)=1/3$.\n")
        (root/"analysis"/"two.py").write_text("# killed formula: sin^2(theta_W) = 3/13\n")
        first=build_universe(root,"fixture-head","2026-07-17T00:00:00Z"); second=build_universe(root,"fixture-head","2026-07-17T00:00:00Z")
    checks={"deterministic":first==second,"three_formula_families_found":first["summary"]["exact_formula_families"]==3,"retrospective_status_detected":any("retrospective_fit" in f["status_profile"] for f in first["exact_families"]),"preregistered_status_detected":any("preregistered" in f["status_profile"] for f in first["exact_families"]),"killed_status_detected":any("killed_or_retracted" in f["status_profile"] for f in first["exact_families"])}
    return {"pass":398,"status":"PASS" if all(checks.values()) else "FAIL","checks":checks,"fixture_summary":first["summary"]}


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--root",type=Path,default=Path(".")); parser.add_argument("--output",type=Path,default=Path("data/w33_formula_search_universe_v1.json")); parser.add_argument("--repository-head",default="UNSPECIFIED"); parser.add_argument("--frozen-at",default="UNSPECIFIED"); parser.add_argument("--check",action="store_true"); parser.add_argument("--self-test",action="store_true"); args=parser.parse_args()
    if args.self_test:
        payload=self_test(); print(json.dumps(payload,sort_keys=True)); raise SystemExit(0 if payload["status"]=="PASS" else 1)
    payload=build_universe(args.root.resolve(),args.repository_head,args.frozen_at); text=json.dumps(payload,indent=2,sort_keys=True)+"\n"
    if args.check:
        if not args.output.exists() or args.output.read_text()!=text: raise SystemExit("Pass 398 formula-universe drift")
    else:
        args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(text)
    print(json.dumps({"status":"PASS",**payload["summary"],"universe_sha256":payload["universe_sha256"]},sort_keys=True))


if __name__=="__main__": main()
