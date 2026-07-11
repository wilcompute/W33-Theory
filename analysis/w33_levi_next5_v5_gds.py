#!/usr/bin/env python3
"""Generate the deterministic v5 hybrid 16-mode reference GDSII layout."""
from pathlib import Path
import argparse, hashlib, json
from w33_levi_next5_v5_hybrid import emit_gds, layout_manifest, validate_gds_records
from w33_levi_next5_v5_common import sha256_json

def main():
    ap=argparse.ArgumentParser();ap.add_argument('output',nargs='?',default='holonet_v5_hybrid.gds');args=ap.parse_args()
    p=Path(args.output);emit_gds(p);data=p.read_bytes();manifest=layout_manifest()
    validation=validate_gds_records(data,len(manifest['rectangles']))
    print(json.dumps({'path':str(p),'kind':'abstract deterministic placement sketch','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'manifest_digest':sha256_json(manifest),'interferometer_slots':len(manifest['interferometer_slots']),'validation':validation,'scope':manifest['scope']},sort_keys=True))
    if not validation['envelope_ok']:raise SystemExit(1)
if __name__=='__main__':main()
