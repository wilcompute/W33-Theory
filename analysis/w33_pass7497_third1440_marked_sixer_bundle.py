#!/usr/bin/env python3
"""Pass7497 wrapper after collision-safe renumbering of the original branch producer."""
import json
from pathlib import Path
import w33_pass7489_third1440_marked_sixer_bundle as core
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7497_THIRD1440_MARKED_SIXER_BUNDLE.json'
def main():
    core.main();src=ROOT/'data'/'PART_W33_PASS7489_THIRD1440_MARKED_SIXER_BUNDLE.json';d=json.loads(src.read_text());d['schema']='w33.pass7497.third1440_marked_sixer_bundle.v1';d['pass']=7497;d['renumbered_from_transient_branch_label']=7489;OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','pass':7497,'marked':d['cubic_surface_counts']['marked_sixer_triples']}))
if __name__=='__main__':main()
