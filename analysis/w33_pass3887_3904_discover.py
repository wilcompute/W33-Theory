#!/usr/bin/env python3
"""Discover exact Passes 3837-3854 exposed workspaces for Passes 3887-3904."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
parts=[ROOT/'analysis'/f'_w33_pass3837_3854_impl_part{i}.pyinc' for i in range(1,5)]
source=''.join(p.read_text(encoding='utf-8') for p in parts)
old='    return result\n\n\ndef main():'
new='    return result, locals()\n\n\ndef main():'
assert source.count(old)==1
ns={'__name__':'p3837_exposed','__file__':str(ROOT/'analysis/w33_pass3837_3854_ovoid_wedderburn_code_leech_triality.py')}
exec(compile(source.replace(old,new),ns['__file__'],'exec'),ns)
result,loc=ns['build']()
out={'result_hash':result['semantic_sha256'],'locals':{},'old_locals':{}}
for name,value in sorted(loc.items()):
    if name.startswith('__'): continue
    item={'type':type(value).__name__}
    if isinstance(value,np.ndarray): item['shape']=list(value.shape); item['dtype']=str(value.dtype)
    elif isinstance(value,(tuple,list,dict,set)): item['len']=len(value)
    out['locals'][name]=item
oldloc=loc.get('old',{})
for name,value in sorted(oldloc.items()):
    item={'type':type(value).__name__}
    if isinstance(value,np.ndarray): item['shape']=list(value.shape); item['dtype']=str(value.dtype)
    elif isinstance(value,(tuple,list,dict,set)): item['len']=len(value)
    out['old_locals'][name]=item
print(json.dumps(out,indent=2,sort_keys=True))
