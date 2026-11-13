#!/usr/bin/env python3
"""Fail-closed root-vs-archived signed E6 cubic source provenance:
byte-level difference is NOT semantic difference.

Check full parsed JSON equality, ordered 45 signed cubic triads,
and exact rephased det(A)+det(B)+det(C)-trace(ABC) coefficient mapping
using independently generated 3x3 determinant parity and trace
supports. Never claim byte identity when hashes disagree.
"""
from pathlib import Path
import json,hashlib
from itertools import permutations
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261113_E6_cubic_two_source_semantic_and_Albert_audit.json"

def load(p):
    raw=p.read_bytes()
    return hashlib.sha256(raw).hexdigest(),len(raw),json.loads(raw)

def main():
    p=ROOT/"artifacts/canonical_su3_gauge_and_cubic.json"
    q=ROOT/"extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json"
    h1,n1,a=load(p)
    h2,n2,b=load(q)
    assert h1!=h2 and n1!=n2
    assert a==b
    raw={tuple(sorted(map(int,x["triple"]))):(1 if int(x["sign"])%3==1 else -1)
         for x in a["solution"]["d_triples"]}
    assert len(raw)==45
    d=json.loads((ROOT/"data/toe_20261113_h27_albert_cubic_coordinate_reconstruction.json").read_text())
    cmap={int(i):tuple(map(int,v)) for i,v in d["explicit_E6_index_to_sector_matrix_coordinate"].items()}
    flip=set(d["signed_rephasing_negative_E6_indices"])
    assert len(cmap)==27
    exp={}
    for term in raw:
        transformed=[cmap[z] for z in term]
        sector=[z[0] for z in transformed]
        if len(set(sector))==1:
            rows={r:c for sector,r,c in transformed}
            assert sorted(rows)==[0,1,2]
            c=[rows[r] for r in range(3)]
            sign=(-1)**sum(c[i]>c[j] for i in range(3) for j in range(i+1,3))
        else:
            assert sorted(sector)==[0,1,2]
            A,B,C=[next(v for v in transformed if v[0]==z) for z in (0,1,2)]
            assert A[2]==B[1] and B[2]==C[1] and C[2]==A[1]
            sign=-1
        assert raw[term]*(-1)**sum(i in flip for i in term)==sign
        exp[term]=sign
    assert len(exp)==45
    out={
       "status":"PASS_TWO_JSON_SOURCES_BYTE_DIFFERENT_BUT_SEMANTICALLY_EQUAL_SIGNED_ALBERT",
       "root_path":str(p.relative_to(ROOT)).replace("\\","/"),
       "root_sha256":h1,"root_bytes":n1,
       "archive_path":str(q.relative_to(ROOT)).replace("\\","/"),
       "archive_sha256":h2,"archive_bytes":n2,
       "raw_bytes_identical":False,
       "parsed_JSON_objects_equal":True,
       "signed_45_triads_equal":True,
       "seven_coordinate_rephasing_Albert_45_terms_exact":True,
       "all_45_produced_exact_det3_plus_det3_plus_det3_minus_trace_ABC":True,
       "scope":"Corrects the other assistant's byte-identity claim at this local checked version. All relevant 45 signed cubic coefficients are identical across files; the difference is JSON serialization/formatting. Git bytes are NOT identical."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:out[k] for k in ("status","root_sha256","archive_sha256","root_bytes","archive_bytes")},indent=2),flush=True)
    return out
if __name__=="__main__":main()
