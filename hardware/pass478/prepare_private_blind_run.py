#!/usr/bin/env python3
"""Operator-side generator for a genuinely blind balanced optical acquisition.

Run this outside the public repository. Keep the private run plan and reveal
private until measured_predictions.json is committed. The operator supplies a
fresh 32-byte random salt; this program never invents or stores one.
"""
from __future__ import annotations
import argparse,csv,hashlib,hmac,json
from pathlib import Path

SAMPLES=96
PHASES=16

def digest(salt:bytes,message:str)->bytes:return hmac.new(salt,message.encode(),hashlib.sha256).digest()
def commitment(salt_hex:str,sample_id:int,label:str)->str:return hashlib.sha256(f'{salt_hex}|{sample_id}|{label}'.encode()).hexdigest()

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--output-dir',type=Path,required=True)
    ap.add_argument('--samples',type=int,default=SAMPLES)
    ap.add_argument('--salt-hex',required=True,help='fresh 32-byte random salt encoded as 64 hex characters')
    args=ap.parse_args()
    if args.samples<2 or args.samples%2:raise SystemExit('samples must be a positive even integer')
    salt_hex=args.salt_hex.lower()
    if len(salt_hex)!=64 or any(c not in '0123456789abcdef' for c in salt_hex):raise SystemExit('salt must be 32 bytes in hex')
    salt=bytes.fromhex(salt_hex)
    scored=sorted(range(args.samples),key=lambda i:digest(salt,f'label-order|{i}'))
    field=set(scored[:args.samples//2])
    labels={i:('field' if i in field else 'ring') for i in range(args.samples)}
    order=sorted(range(args.samples),key=lambda i:digest(salt,f'run-order|{i}'))
    private=[];public=[];truth=[]
    for run_index,sample_id in enumerate(order):
        phase_order=sorted(range(PHASES),key=lambda phase:digest(salt,f'phase-order|{sample_id}|{phase}'))
        label=labels[sample_id]
        private.append({'run_index':run_index,'sample_id':sample_id,'configuration':label,'phase_order':' '.join(map(str,phase_order))})
        public.append({'run_index':run_index,'sample_id':sample_id,'commitment':commitment(salt_hex,sample_id,label)})
        truth.append({'sample_id':sample_id,'label':label})
    args.output_dir.mkdir(parents=True,exist_ok=True)
    with (args.output_dir/'private_run_plan.csv').open('w',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=private[0].keys());writer.writeheader();writer.writerows(private)
    with (args.output_dir/'public_commitments.csv').open('w',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=public[0].keys());writer.writeheader();writer.writerows(public)
    reveal={'salt':salt_hex,'truth':sorted(truth,key=lambda row:row['sample_id']),'prediction_sha256':''}
    (args.output_dir/'reveal.json').write_text(json.dumps(reveal,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'samples':args.samples,'field':args.samples//2,'ring':args.samples//2,'private_files':2,'public_files':1}))
    return 0
if __name__=='__main__':raise SystemExit(main())
