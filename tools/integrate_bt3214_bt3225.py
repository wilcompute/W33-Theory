#!/usr/bin/env python3
"""Idempotently integrate Passes 3214-3225 into the three papers and site."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TEX_INSERT=ROOT/'analysis/BT3214_BT3225_runtime_reset_sheaf_insert.tex'
HTML_INSERT=ROOT/'analysis/BT3214_BT3225_runtime_reset_sheaf_index_insert.html'
TEX_BEGIN='% BEGIN PASS 3214-3225 RUNTIME RESET SHEAF CLOSURE'
TEX_END='% END PASS 3214-3225 RUNTIME RESET SHEAF CLOSURE'
HTML_BEGIN='<!-- BEGIN PASS 3214-3225 RUNTIME RESET SHEAF CLOSURE -->'
HTML_END='<!-- END PASS 3214-3225 RUNTIME RESET SHEAF CLOSURE -->'

def decode(data):return data.decode('utf-8',errors='surrogateescape')
def encode(text):return text.encode('utf-8',errors='surrogateescape')
def newline_for(text):return '\r\n' if text.count('\r\n')>text.count('\n')/2 else '\n'
def normalize(text,nl):return text.replace('\r\n','\n').replace('\r','\n').replace('\n',nl)

def splice(path,insert_path,begin,end,anchor):
 original_bytes=path.read_bytes();original=decode(original_bytes);nl=newline_for(original)
 insert=normalize(insert_path.read_text(encoding='utf-8'),nl).strip()+nl
 bp=original.find(begin);ep=original.find(end)
 if (bp>=0)!=(ep>=0):raise RuntimeError(f'partial marker in {path}')
 if bp>=0:
  endline=original.find(nl,ep)
  if endline<0:endline=len(original)
  else:endline+=len(nl)
  updated=original[:bp]+insert+original[endline:];action='replaced'
 else:
  pos=original.rfind(anchor)
  if pos<0:raise RuntimeError(f'anchor {anchor!r} missing in {path}')
  prefix=original[:pos]
  if prefix and not prefix.endswith(('\n','\r')):prefix+=nl
  updated=prefix+nl+insert+nl+original[pos:];action='inserted'
 updated_bytes=encode(updated);path.write_bytes(updated_bytes)
 return {'path':str(path.relative_to(ROOT)),'action':action,
  'before_sha256':hashlib.sha256(original_bytes).hexdigest(),
  'after_sha256':hashlib.sha256(updated_bytes).hexdigest(),
  'outside_region_byte_preservation':True}

def integrate():
 rows=[]
 for name in ('w33_paper.tex','photonic_holonet.tex','holonet_machine_blueprint.tex'):
  path=ROOT/name
  if not path.exists():raise FileNotFoundError(name)
  rows.append(splice(path,TEX_INSERT,TEX_BEGIN,TEX_END,'\\end{document}'))
 site=ROOT/'docs/index.html'
 if not site.exists():site=ROOT/'index.html'
 if not site.exists():raise FileNotFoundError('docs/index.html or index.html')
 rows.append(splice(site,HTML_INSERT,HTML_BEGIN,HTML_END,'</body>'))
 assert len(rows)==4
 return {'schema':'w33.pass3214_3225.integration.v1','files':rows}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path);a=ap.parse_args()
 result=integrate()
 if a.report:
  a.report.parent.mkdir(parents=True,exist_ok=True)
  a.report.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
