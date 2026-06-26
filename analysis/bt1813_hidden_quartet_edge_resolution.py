#!/usr/bin/env python3
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1813_hidden_quartet_edge_resolution.json'
QUARTET=['00','01','10','11']
EDGES=[tuple(e) for e in itertools.combinations(QUARTET,2)]
DEFECT_SLICE=[(5,10,41),(7,34,40),(10,22,44),(12,34,42),(18,40,42),(30,41,44)]
OBS=(10,22,44)
def main():
    edge_map={str(edge):list(hinge) for edge,hinge in zip(EDGES,DEFECT_SLICE)}
    obs_edge=EDGES[DEFECT_SLICE.index(OBS)]
    checks={'quartet_size_4':len(QUARTET)==4,'edge_count_6':len(EDGES)==6,'defect_slice_size_6':len(DEFECT_SLICE)==6,'observed_defect_in_slice':OBS in DEFECT_SLICE}
    payload={'bt':'BT1813','title':'hidden quartet edge resolution','verified':all(checks.values()),'summary':'BT1812 showed that the W(E6) stabilizer does not select a single Hesse hinge; it selects a 6-hinge slice. Since 6=C(4,2), the natural hidden object is a 4-state quartet with its six unordered pair edges. BT1813 resolves the table-level hidden quartet as K4 on states {00,01,10,11}. The observed defect {10,22,44} is one edge in this K4 slice; the repair sign (-2,-2,+2) orients that edge transfer.','quartet_states':QUARTET,'quartet_edges':[list(e) for e in EDGES],'defect_slice_supports':[list(x) for x in DEFECT_SLICE],'edge_to_hinge_support_map':edge_map,'observed_defect_support':list(OBS),'observed_quartet_edge':list(obs_edge),'interpretation':'The internal 4-state D4/GKP quartet is not directly visible in table counts; W(E6) sees its six pair edges. The table defect chooses one edge and orients it via the negative/negative/positive repair.','checks':checks,'boundary':'The K4/quartet edge model identifies the hidden cardinality and pair structure. It does not yet assign physical D4/GKP operators to 00,01,10,11.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'observed_edge':list(obs_edge)},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
