#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
import w33_pass1801_1805_five_frontiers as core
from w33_pass1801_1805_common import build_geometry,build_bockstein
ROOT=Path(__file__).resolve().parents[1]
def run(number:int):
 data=build_geometry()
 if number in (1801,1802):bock=build_bockstein(data)
 result={1801:lambda:core.pass1801(data,bock),1802:lambda:core.pass1802(data,bock),1803:lambda:core.pass1803(data),1804:lambda:core.pass1804(data),1805:lambda:core.pass1805(data)}[number]()
 payload={'schema':f'w33.pass{number}.component.v1','status':'PASS','result':result}
 raw=json.dumps(payload,sort_keys=True,separators=(',',':'));payload['sha256']=hashlib.sha256(raw.encode()).hexdigest();return payload
def main():
 ap=argparse.ArgumentParser();ap.add_argument('number',type=int,choices=range(1801,1806));ap.add_argument('--check',action='store_true');args=ap.parse_args();out=ROOT/'data'/f'w33_pass{args.number}_component.json';payload=run(args.number);text=json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n'
 if args.check:
  if not out.exists() or out.read_text()!=text:raise SystemExit(f'Pass {args.number} drift')
 else:out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text)
 print(json.dumps({'pass':args.number,'status':'PASS','sha256':payload['sha256']}))
if __name__=='__main__':main()
