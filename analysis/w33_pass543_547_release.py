#!/usr/bin/env python3
from __future__ import annotations
import argparse,importlib.util,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data'/'w33_pass543_547_icosahedral_fourier_recurrence.json'
sys.path.insert(0,str(ROOT/'analysis'))
def load(name):
 p=ROOT/'analysis'/name;s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
FILES=[
 ('pass543','w33_pass543_q5_icosahedral_association_image.py'),
 ('pass544','w33_pass544_binary_switch_spectral_fibre.py'),
 ('pass545','w33_pass545_triality_antiunitary_lift.py'),
 ('pass546','w33_pass546_z9_kernel_fourier_image.py'),
 ('pass547','w33_pass547_q5_recurrence_families.py')]
def payload():
 parts={k:load(f).payload() for k,f in FILES}
 checks={k:v['status']=='PASS' for k,v in parts.items()}
 return {'schema':'w33.pass543_547.icosahedral_fourier_recurrence.release.v1','status':'PASS' if all(checks.values()) else 'FAIL','parts':parts,'checks':checks,'total_exact_checks':sum(len(v['checks']) for v in parts.values()),'boundary':'Five exact workstreams; no full q5 or Z/9 image classification.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 543-547 release drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'parts':sum(p['checks'].values()),'total_parts':len(p['checks']),'exact_checks':p['total_exact_checks']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
