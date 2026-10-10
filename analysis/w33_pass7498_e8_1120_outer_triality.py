#!/usr/bin/env python3
"""Pass7498 wrapper after collision-safe renumbering of the original branch producer."""
import json
from pathlib import Path
import w33_pass7491_e8_1120_outer_triality as core
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7498_E8_1120_OUTER_TRIALITY.json'
def main():
    core.main();src=ROOT/'data'/'PART_W33_PASS7491_E8_1120_OUTER_TRIALITY.json';d=json.loads(src.read_text());d['schema']='w33.pass7498.e8_1120_outer_triality.v1';d['pass']=7498;d['renumbered_from_transient_branch_label']=7491;OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','pass':7498,'outer_type_group':d['outer_type_group']}))
if __name__=='__main__':main()
