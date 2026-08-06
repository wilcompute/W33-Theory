#!/usr/bin/env python3
"""Pass 3992: exact central fusion lattice of the seven primitive blocks."""
from __future__ import annotations
import hashlib, itertools, json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FOURIER=ROOT/"data/PART_3983_ORBITAL_CENTRAL_FOURIER.json"

def partitions(n):
    out=[]
    def rec(i,blocks):
        if i==n:
            out.append(tuple(tuple(b) for b in blocks)); return
        for j in range(len(blocks)):
            blocks[j].append(i); rec(i+1,blocks); blocks[j].pop()
        blocks.append([i]); rec(i+1,blocks); blocks.pop()
    rec(0,[])
    return out

def canon(part):
    return tuple(sorted(tuple(sorted(b)) for b in part))

def apply(part,p):
    return canon(tuple(tuple(p[i] for i in block) for block in part))

def canonical_sha(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def main():
    if not FOURIER.exists():
        raise SystemExit("Run analysis/w33_pass3983_orbital_central_fourier.py first")
    fourier=json.loads(FOURIER.read_text())
    assert fourier["status"]=="PASS"
    degrees=list(map(int,fourier["simple_degrees"]))
    assert sorted(degrees)==[1,1,2,2,2,3,5]
    parts=partitions(7)
    assert len(parts)==877
    count_by_blocks=Counter(len(p) for p in parts)
    assert dict(sorted(count_by_blocks.items()))=={1:1,2:63,3:301,4:350,5:140,6:21,7:1}
    eq_group=[]
    one_indices=[i for i,d in enumerate(degrees) if d==1]
    two_indices=[i for i,d in enumerate(degrees) if d==2]
    fixed=[i for i,d in enumerate(degrees) if d not in (1,2)]
    for p1 in itertools.permutations(one_indices):
        for p2 in itertools.permutations(two_indices):
            p=list(range(7))
            for src,dst in zip(one_indices,p1): p[src]=dst
            for src,dst in zip(two_indices,p2): p[src]=dst
            for i in fixed: p[i]=i
            eq_group.append(tuple(p))
    assert len(eq_group)==12
    orbit_reps={}
    for part in parts:
        c=min(apply(part,p) for p in eq_group)
        orbit_reps.setdefault(c,0)
        orbit_reps[c]+=1
    assert len(orbit_reps)==198
    orbit_count_by_blocks=Counter(len(p) for p in orbit_reps)
    assert dict(sorted(orbit_count_by_blocks.items()))=={1:1,2:23,3:68,4:66,5:31,6:8,7:1}
    records=[]
    for rep,orbit_size in sorted(orbit_reps.items(),key=lambda kv:(len(kv[0]),kv[0])):
        blocks=[]
        for block in rep:
            ds=[degrees[i] for i in block]
            blocks.append({
                "primitive_indices":list(block),
                "simple_degrees":ds,
                "regular_rank":sum(d*d for d in ds),
            })
        records.append({
            "central_dimension":len(rep),
            "equal_degree_relabeling_orbit_size":orbit_size,
            "blocks":blocks,
        })
    result={
        "schema":"w33.pass3992.central_fusion_lattice.v1",
        "status":"PASS_EXACT_CENTRAL_FUSION_LATTICE",
        "primitive_simple_degrees":degrees,
        "primitive_regular_ranks":[d*d for d in degrees],
        "all_set_partitions":877,
        "count_by_central_dimension":dict(sorted(count_by_blocks.items())),
        "equal_degree_relabeling_group_order":12,
        "inequivalent_central_fusions":198,
        "inequivalent_count_by_central_dimension":dict(sorted(orbit_count_by_blocks.items())),
        "orbit_representatives":records,
        "fourier_character_table_sha256":fourier["character_table_sha256"],
        "fourier_idempotent_sha256":fourier["idempotent_sha256"],
        "boundary":"Every record is an exact unital subalgebra of the seven-dimensional center obtained by summing primitive central idempotents. This does not claim that every central partition lifts to a combinatorial fusion of the 48 orbital relations.",
    }
    result["semantic_sha256"]=canonical_sha(result)
    out=ROOT/"data/PART_3992_CENTRAL_FUSION_LATTICE.json"
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("PASS_CENTRAL_FUSION_LATTICE",877,198,result["semantic_sha256"])
if __name__=="__main__":
    main()
