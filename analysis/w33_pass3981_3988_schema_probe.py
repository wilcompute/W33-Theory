#!/usr/bin/env python3
"""Schema probe for the content-addressed Passes 3973-3980 exact objects."""
from __future__ import annotations
import base64, importlib.util, json, zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def unpack(parts):
    encoded=''.join((ROOT/p).read_text(encoding='ascii').strip() for p in parts)
    return json.loads(zlib.decompress(base64.b64decode(encoded)))

def shape(x, depth=0):
    if depth>=3: return type(x).__name__
    if isinstance(x,dict):
        return {str(k):shape(v,depth+1) for k,v in list(x.items())[:20]}
    if isinstance(x,list):
        return {'type':'list','len':len(x),'sample':[shape(v,depth+1) for v in x[:3]]}
    return {'type':type(x).__name__,'repr':repr(x)[:160]}

def main():
    manifest=json.loads((ROOT/'data/PART_3973_3980_EXTREMAL_MESH_PHOTON_TENSOR_manifest.json').read_text())
    cert=unpack(manifest['certificate']['parts'])
    tensor=unpack([manifest['rank48_tensor']['path']])
    src=ROOT/'analysis/w33_pass3973_3980_extremal_mesh_photon_tensor_monster.py'
    spec=importlib.util.spec_from_file_location('p3973',src); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    ns=mod.namespace
    result={
      'schema':'w33.pass3981_3988.schema_probe.v1',
      'certificate_keys':sorted(cert),
      'certificate_shape':shape(cert),
      'tensor_keys':sorted(tensor),
      'tensor_shape':shape(tensor),
      'namespace_keys':sorted(k for k in ns if not k.startswith('__')),
    }
    out=ROOT/'data/PART_3981_3988_SCHEMA_PROBE.json'
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS_SCHEMA_PROBE',len(result['namespace_keys']),len(result['tensor_keys']))
if __name__=='__main__': main()
