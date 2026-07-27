#!/usr/bin/env python3
"""Pass 1151: canonical lock reconciling Pass 1139 with the occurrence guard."""
from __future__ import annotations
import json
from pathlib import Path
SPECIES=[{"tom":77,"tag":"point-nonedge","rank":25,"stabilizer":[48,33],"normalizer":96},{"tom":78,"tag":"double-six-nonincident","rank":28,"stabilizer":[48,48],"normalizer":96},{"tom":79,"tag":"gq42-arc","rank":27,"stabilizer":[48,49],"normalizer":96},{"tom":80,"tag":"outer-4c","rank":21,"stabilizer":[48,30],"normalizer":96},{"tom":81,"tag":"line-nonedge","rank":32,"stabilizer":[48,48],"normalizer":48}]
JOINT=[[25,16,15,15,16],[16,28,25,20,25],[15,25,27,20,25],[15,20,20,21,19],[16,25,25,19,32]]
def det(a):
    m=[r[:] for r in a]; prev=1; sign=1
    for k in range(len(m)-1):
        if not m[k][k]:
            i=next(i for i in range(k+1,len(m)) if m[i][k]); m[k],m[i]=m[i],m[k]; sign*=-1
        p=m[k][k]
        for i in range(k+1,len(m)):
            for j in range(k+1,len(m)): m[i][j]=(m[i][j]*p-m[i][k]*m[k][j])//prev
        prev=p
    return sign*m[-1][-1]
def main()->dict:
    d=det(JOINT); assert d==83712
    twins=[s for s in SPECIES if s["stabilizer"]==[48,48]]; assert {s["normalizer"] for s in twins}=={48,96}
    result={"schema":"w33.pass1151.degree540_taxonomy_lock.v1","status":"PASS","canonical_species":SPECIES,"compatibility_labels":["both","mixed","unrelated"],"joint_rank_matrix":JOINT,"joint_rank_determinant":d,"policy":"Cardinality 540 and abstract stabilizer type never identify a carrier."}
    out=Path("data/w33_pass1151_degree540_taxonomy_lock.json"); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8"); print("PASS 1151 determinant",d); return result
if __name__=="__main__": main()
