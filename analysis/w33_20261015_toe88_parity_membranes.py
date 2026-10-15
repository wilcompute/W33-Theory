"""TOE88 explicit 2-torsion parity membranes without integral SNF.

A mod-2 closed face chain with integer boundary 2*y defines Bockstein
class [y] in H1(F2). Its nonzero rank detects 2-primary torsion.
Find sparse integer 2-chain lifts for geometric orbit-pair examples.
"""
from __future__ import annotations
import itertools, json
from analysis.w33_20261015_toe85_h2_relation_module import ROOT,nullspace,rank_and_basis
from analysis.w33_20261015_toe87_modular_bockstein_triples import (
    geometry_data,geometry_for_orbits
)

def rank(rows,p=2):
    return len(rank_and_basis(rows,p))

def cert_for_pair(G,pair):
    rows,cycles,action,sq=geometry_for_orbits(pair,G)
    cols=len(rows);edgecount=len(rows[0])
    A=[[rows[j][i] for j in range(cols)] for i in range(edgecount)]
    kernel,free,rankA=nullspace(A,2)
    boundary_rank=rank(rows,2)
    assert boundary_rank==rankA
    def bock(v):
        boundary=[sum(a*x for a,x in zip(row,v)) for row in A]
        assert all(t%2==0 for t in boundary)
        return [(t//2)%2 for t in boundary]
    baseline=rank(rows,2)
    ranklift=baseline
    witnesses=[]
    # For kernel dimension 4, exhaustive 15 nonzero 2-membranes.
    # For dimension 16, enumerate just the supplied kernel basis.
    candidates=[list(v) for v in kernel]
    if len(kernel)<=6:
        candidates=[]
        for m in range(1,1<<len(kernel)):
            v=[sum(kernel[i][j] for i in range(len(kernel)) if m>>i&1)%2
               for j in range(cols)]
            candidates.append(v)
        candidates.sort(key=lambda v:(sum(v),v))
    for v in candidates:
        w=bock(v)
        x=rank(rows+[w]+[x["bockstein_edge_vector"] for x in witnesses],2)
        if x>baseline+len(witnesses):
            active=[i for i,z in enumerate(v) if z]
            edge_nonzero=[i for i,z in enumerate(w) if z]
            # The integral lift's even boundary is checked exactly above.
            witnesses.append({
                "face_count":len(active),
                "triangle_face_count":sum(i<45 for i in active),
                "square_face_count":sum(i>=45 for i in active),
                "nonzero_faces":active,
                "Bockstein_edge_support":edge_nonzero,
                "bockstein_edge_vector":w})
    expected=rank(rows+[bock(v) for v in kernel],2)-baseline
    assert len(witnesses)==expected
    assert expected==sum(d%2==0 for d in json.loads(
        (ROOT/"data/w33_20261015_toe86_pair_integral.json").read_text()
        )["classes"][next(i for i,c in enumerate(json.loads(
        (ROOT/"data/w33_20261015_toe86_pair_integral.json").read_text()
        )["classes"]) if c["representative"]==list(pair))]["nonunit_smith_factors"])
    return {"orbit_pair":list(pair),"face_count":cols,"binary_rank":rankA,
            "mod2_face_2cycle_dimension":len(kernel),
            "mod2_Bockstein_image_rank":expected,
            "integer_membrane_witnesses":witnesses}

def certificate():
    G=geometry_data()
    reps=((0,10),(1,2),(1,31),(1,36))
    records=[]
    for pair in reps:
        x=cert_for_pair(G,pair)
        print("PARITY",pair,"Bockstein",x["mod2_Bockstein_image_rank"],
              "face supports",[w["face_count"] for w in x["integer_membrane_witnesses"]],flush=True)
        records.append(x)
    assert [x["mod2_Bockstein_image_rank"] for x in records]==[0,0,2,2]
    return {"method":"Exact F2 parity membranes in the native oriented integer face boundary; integer SNF not used to find witnesses. Independent precomputed SNF factors are checked afterward.",
            "Bockstein_definition":"For mod2 face cycle v, choose coefficient lifts in {0,1}. Its exact integer boundary equals 2*y, so beta([v])=[y modulo 2] in H1(F2).",
            "negative_local_overlap_result":"A square-orbit pairwise shared-edge histogram [675,54,0,0,0] occurs in both torsion-free (0,10) and [6,6]-torsion (1,31)/(1,36) classes.",
            "representatives":records}

if __name__=="__main__":
    x=certificate()
    f=ROOT/"data/w33_20261015_toe88_parity_membranes.json"
    f.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf8")
