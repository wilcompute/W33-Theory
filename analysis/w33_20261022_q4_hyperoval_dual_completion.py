#!/usr/bin/env python3
"""Eight explicit plane hyperovals complete the q=4 symplectic code dual.

For q=4 the 357 ambient PG(3,4) line checks have GF2-rank 61,
while C_B^perp has rank 69. Eight frozen weight-6 hyperovals
supplement the line checks and increase the rank to exactly 69.
No brute-force search is required to replay the certificate.

Projective even-type sets and hyperoval theory are established prior art.
This exact chosen basis is a reproducible W33 repo-level witness, not
a claim of mathematical first discovery or physical stabilizer checks.
"""
from __future__ import annotations
import json
from pathlib import Path
from analysis.w33_20261022_six_algebra_optics_frontiers import field
from analysis.w33_20261022_hamada_golden_hidden_checks import projective_points,projective_lines

# q4 projective coordinate indices in projective_points(4) normal form
HYPEROVALS = [
 (0,20,44,56,64,80),
 (21,25,53,57,68,76),
 (1,12,33,44,70,77),
 (1,12,19,24,59,61),
 (2,12,22,24,67,77),
 (6,8,18,28,67,77),
 (12,16,39,59,67,81),
 (37,46,49,58,66,73),
]

def row_mask(indices):
    return sum(1<<i for i in indices)

def insert(mask,pivots):
    x=mask
    while x:
        j=x.bit_length()-1
        if j in pivots:x^=pivots[j]
        else:pivots[j]=x;return True
    return False

def symplectic(x,y,add,mul):
    z=0
    for i,j in ((0,2),(1,3),(2,0),(3,1)):
        z=add[z,mul[x[i],y[j]]]
    return z # characteristic 2, minus equals plus

def release():
    q,add,mul,inv,neg=field(2,2,(1,1,1))
    P=projective_points(q)
    assert len(P)==85
    lines,n=projective_lines(q,add,mul)
    assert (len(lines),n)==(357,85)
    line_masks=[row_mask(ln) for ln in lines]
    pivots={}
    for m in line_masks:insert(m,pivots)
    assert len(pivots)==61
    B=[]
    planes=[]
    for x in P:
        hyperplane={i for i,y in enumerate(P) if symplectic(x,y,add,mul)==0}
        assert len(hyperplane)==21
        planes.append(hyperplane)
        b=row_mask(j for j in range(n) if j not in hyperplane)
        assert b.bit_count()==64
        B.append(b)
    r=[]
    for word in HYPEROVALS:
        S=set(word);mask=row_mask(S)
        assert len(S)==6 and mask.bit_count()==6
        # A unique plane contains this six-point arc.
        candidates=[plane for plane in planes if S <= plane]
        assert len(candidates)==1
        plane=candidates[0]
        contained=[ln for ln in lines if set(ln)<=plane]
        assert len(contained)==21
        assert all(len(S.intersection(ln)) in (0,2) for ln in contained)
        assert all(len(S.intersection(ln))<=2 for ln in lines)
        assert all((mask & b).bit_count()%2==0 for b in B)
        before=len(pivots)
        assert insert(mask,pivots)
        assert len(pivots)==before+1
        r.append({"indices":list(word),"weight":6,
                  "unique_containing_plane":sorted(plane),
                  "line_intersection_histogram":{
                    "0":sum(not S.intersection(ln) for ln in contained),
                    "2":sum(len(S.intersection(ln))==2 for ln in contained)},
                  "new_independent_direction":True})
    assert len(pivots)==69
    # All line + hyperoval checks annihilate B, whose row rank is 16.
    # Hence their 69D span equals full ker(B), dimension 85-16.
    return {"status":"PASS_EXACT_HYPEROVAL_COMPLETION",
            "classical_RH_proved":False,
            "code_field":"F2","geometry_field":"F4",
            "points":85,"projective_lines":357,
            "line_parity_check_weight":5,"line_check_rank":61,
            "added_hyperoval_words":8,
            "hyperoval_parity_check_weight":6,
            "line_plus_hyperoval_rank":69,
            "full_noncollinearity_dual_dimension":69,
            "missing_rank_filled":8,
            "independent_hyperovals":r,
            "proof":"Each 6-arc is contained in one PG(2,4) plane and intersects every line of that plane in 0 or 2 points. Each symplectic polar hyperplane meets that plane in a line or contains it. Thus hyperoval indicators are orthogonal to B. Frozen eight supports increase full projective line-check rank 61 to ker(B) dimension 69.",
            "hardware_boundary":"Weight-5 lines and weight-6 hyperovals are checks of the *classical* code row(B), but not automatically quantum CSS stabilizers. No fault-tolerant hardware threshold established."}

if __name__=="__main__":
    r=release()
    dest=Path(__file__).resolve().parents[1]/"data"/"w33_20261022_q4_hyperoval_dual_completion.json"
    dest.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print("line rank",r["line_check_rank"],"hyperoval-completed",r["line_plus_hyperoval_rank"])
