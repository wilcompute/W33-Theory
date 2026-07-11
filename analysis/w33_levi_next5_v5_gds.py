#!/usr/bin/env python3
"""Generate the deterministic v5 hybrid 16-mode reference GDSII layout."""
from pathlib import Path
import argparse, hashlib, json
from w33_levi_next5_v5_hybrid import emit_gds, layout_manifest
from w33_levi_next5_v5_common import sha256_json

def main():
    ap=argparse.ArgumentParser();ap.add_argument('output',nargs='?',default='holonet_v5_hybrid.gds');args=ap.parse_args()
    p=Path(args.output);emit_gds(p);data=p.read_bytes();manifest=layout_manifest()
    print(json.dumps({'path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'manifest_digest':sha256_json(manifest),'mzi_cells':len(manifest['mzi_cells'])},sort_keys=True))
if __name__=='__main__':main()
