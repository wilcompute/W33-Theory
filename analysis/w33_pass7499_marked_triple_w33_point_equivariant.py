#!/usr/bin/env python3
"""Pass7499 wrapper after collision-safe renumbering of the original branch producer."""
import json
from pathlib import Path
import w33_pass7492_marked_triple_w33_point_equivariant as core
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7499_MARKED_TRIPLE_W33_POINT_EQUIVARIANT.json'
def main():
    core.main();src=ROOT/'data'/'PART_W33_PASS7492_MARKED_TRIPLE_W33_POINT_EQUIVARIANT.json';d=json.loads(src.read_text());d['schema']='w33.pass7499.marked_triple_w33_point_equivariant.v1';d['pass']=7499;d['renumbered_from_transient_branch_label']=7492;OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','pass':7499,'stabilizer':d['double_six_stabilizer_order']}))
if __name__=='__main__':main()
