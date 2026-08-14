#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(helper_name:str,out_name:str,new_pass:int,src_name:str|None=None):
    path=ROOT/'analysis'/'collision_clean_helpers'/helper_name
    spec=importlib.util.spec_from_file_location(f'_w33_cc_{new_pass}',path)
    mod=importlib.util.module_from_spec(spec);assert spec and spec.loader;spec.loader.exec_module(mod)
    out=ROOT/'data'/out_name;mod.OUT=out
    if src_name is not None:mod.SRC=ROOT/'data'/src_name
    mod.main()
    d=json.loads(out.read_text());d['pass']=new_pass
    d['collision_clean_source']=str(path.relative_to(ROOT))
    out.write_text(json.dumps(d,indent=2)+'\n')
    return d
