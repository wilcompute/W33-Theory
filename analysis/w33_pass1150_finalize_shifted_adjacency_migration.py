#!/usr/bin/env python3
"""Pass 1150: transactionally close every pending shifted-adjacency descendant."""
from __future__ import annotations
import argparse, ast, json
from pathlib import Path
from typing import Iterable
ROOT=Path(__file__).resolve().parents[1]
MARKER="PASS1150_SHIFTED_ADJACENCY_RETRACTION"
PY_GUARD=f'''\n# {MARKER}\nimport os as _w33_retraction_os\nif _w33_retraction_os.environ.get("W33_ALLOW_RETRACTED_SHIFTED_ADJACENCY") != "1":\n    raise RuntimeError("This legacy module depends on the retracted D=A-I spectrum {{-7^6,-1^16,5^10}}. Use the canonical spectrum {{11^1,1^24,-5^15}} and analysis/w33_shifted_adjacency_spectral_audit.py instead. Set W33_ALLOW_RETRACTED_SHIFTED_ADJACENCY=1 only for historical archaeology.")\n'''
PYTEST_SKIP=f'''\n# {MARKER}\nimport pytest as _w33_retraction_pytest\npytestmark=_w33_retraction_pytest.mark.skip(reason="Legacy test depends on the retracted shifted-adjacency spectrum; Pass 1150 quarantine.")\n'''
MD_NOTICE=f'''> **Spectral erratum — {MARKER}.** This historical file contains a descendant of the retracted claim that `D=A-I` has spectrum `{{-7^6,-1^16,5^10}}`. The exact spectrum is `{{11^1,1^24,-5^15}}`. The historical formulas are retained only for provenance and are not active evidence.\n\n'''
TEX_NOTICE=rf'''\par\noindent\fbox{{\begin{{minipage}}{{0.94\linewidth}}\textbf{{Spectral erratum ({MARKER}).}} This historical section contains a descendant of the retracted claim that $D=A-I$ has spectrum $\{{-7^6,-1^{{16}},5^{{10}}\}}$. The exact spectrum is $\{{11^1,1^{{24}},(-5)^{{15}}\}}$. Historical formulas below are retained only for provenance.\end{{minipage}}}}\par\medskip
'''
def insertion_line(text:str)->int:
    tree=ast.parse(text); line=0; body=list(tree.body); i=0
    if body and isinstance(body[0],ast.Expr) and isinstance(getattr(body[0],"value",None),ast.Constant) and isinstance(body[0].value.value,str): line=body[0].end_lineno or body[0].lineno; i=1
    while i<len(body) and isinstance(body[i],ast.ImportFrom) and body[i].module=="__future__": line=body[i].end_lineno or body[i].lineno; i+=1
    return line
def insert_after(text:str,line:int,payload:str)->str:
    lines=text.splitlines(keepends=True); return "".join(lines[:line])+payload+"".join(lines[line:])
def transform(path:Path,text:str)->tuple[str,str]:
    if MARKER in text:
        if "tests" in path.parts: return text,"LEGACY_TEST_SKIP_MARKER:PASS1150"
        if path.suffix==".py": return text,"ACTIVE_FAIL_CLOSED_RETRACTION_GUARD:PASS1150"
        return text,"VISIBLE_ERRATUM_NOTICE:PASS1150"
    if path.suffix==".py":
        is_test="tests" in path.parts; return insert_after(text,insertion_line(text),PYTEST_SKIP if is_test else PY_GUARD),("LEGACY_TEST_SKIP_MARKER:PASS1150" if is_test else "ACTIVE_FAIL_CLOSED_RETRACTION_GUARD:PASS1150")
    if path.suffix==".tex":
        begin="\\begin{document}"
        return ((text[:text.index(begin)+len(begin)]+"\n"+TEX_NOTICE+text[text.index(begin)+len(begin):]) if begin in text else TEX_NOTICE+text),"VISIBLE_ERRATUM_NOTICE:PASS1150"
    if path.suffix in {".md",".txt"}: return MD_NOTICE+text,"VISIBLE_ERRATUM_NOTICE:PASS1150"
    raise ValueError(f"unsupported pending descendant type: {path}")
def run(root:Path=ROOT,apply:bool=False)->dict:
    ledger_path=root/"data/w33_shifted_adjacency_retraction_ledger.json"; ledger=json.loads(ledger_path.read_text(encoding="utf-8")); descendants=ledger["known_descendants"]
    pending=sorted(p for p,s in descendants.items() if "pending" in s.lower()); actions=[]; errors=[]
    for rel in pending:
        path=root/rel
        try:
            text=path.read_text(encoding="utf-8"); updated,status=transform(Path(rel),text); changed=updated!=text
            if apply and changed: path.write_text(updated,encoding="utf-8")
            if apply: descendants[rel]=status
            actions.append({"path":rel,"changed":changed,"stable_status":status})
        except Exception as exc: errors.append({"path":rel,"error":f"{type(exc).__name__}: {exc}"})
    if apply and not errors:
        ledger["schema"]="w33.shifted_adjacency.retraction_ledger.v4"; ledger["pass1150_completion"]={"pending_before":len(pending),"pending_after":0,"report":"data/w33_pass1150_shifted_adjacency_completion.json"}; ledger_path.write_text(json.dumps(ledger,indent=2)+"\n",encoding="utf-8")
    report={"schema":"w33.pass1150.shifted_adjacency_completion.v1","status":"PASS" if not errors else "FAIL","mode":"apply" if apply else "check","pending_before":len(pending),"pending_after":0 if apply and not errors else len(pending),"actions":actions,"errors":errors,"canonical_spectrum":{"11":1,"1":24,"-5":15},"historical_spectrum":{"-7":6,"-1":16,"5":10}}
    if apply: (root/"data/w33_pass1150_shifted_adjacency_completion.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    if errors: raise RuntimeError(json.dumps(errors,indent=2))
    print(f"PASS 1150 mode={report['mode']} pending={len(pending)}"); return report
def main(argv:Iterable[str]|None=None)->int:
    p=argparse.ArgumentParser(); p.add_argument("--root",type=Path,default=ROOT); p.add_argument("--apply",action="store_true"); a=p.parse_args(argv); run(a.root.resolve(),a.apply); return 0
if __name__=="__main__": raise SystemExit(main())
