#!/usr/bin/env python3
"""Exact rational proper self-crossing count of optimized 12-plane model.

The 12x3 coefficient strings saved by the optimizer are treated as exact
base-ten rational numbers; every triple-plane vertex is solved exactly
by two-by-two Cramer's rule. Proper crossing signs are then exact.
This only certifies the candidate's FAILURE to have 12 simple faces.
"""
import importlib.util,json
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis"/"toe_20261115_genus6_plane_optimization.py"
spec=importlib.util.spec_from_file_location("genus_optimizer_geometry",SRC)
geom=importlib.util.module_from_spec(spec);spec.loader.exec_module(geom)
IN=ROOT/"data"/"toe_20261115_genus6_12plane_optimized_necessary.json"
OUT=ROOT/"data"/"toe_20261115_genus6_12plane_exact_rational_crossings.json"

def run():
    obj=json.loads(IN.read_text())
    planes=[[Q(str(a)) for a in trip] for trip in obj["parameters"]]
    xy=[]
    for ii,jj,kk in geom.F:
        ai,bi,ci=planes[ii];aj,bj,cj=planes[jj];ak,bk,ck=planes[kk]
        a=ai-aj;b=bi-bj;d=cj-ci
        c=ai-ak;e=bi-bk;f=ck-ci
        det=a*e-c*b
        assert det!=0
        x=(d*e-f*b)/det
        y=(a*f-c*d)/det
        xy.append((x,y))
    assert len(xy)==44
    def orient(a,b,c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    counts=[]
    degeneracies=0
    for face in geom.B:
        poly=[xy[int(i)] for i in face]
        c=0
        for i,j in combinations(range(11),2):
            if j==i+1 or (i==0 and j==10):continue
            a,b=poly[i],poly[(i+1)%11];x,y=poly[j],poly[(j+1)%11]
            o1=orient(a,b,x);o2=orient(a,b,y)
            o3=orient(x,y,a);o4=orient(x,y,b)
            if 0 in (o1,o2,o3,o4):degeneracies+=1
            if o1*o2<0 and o3*o4<0:c+=1
        counts.append(c)
    assert sum(counts)==obj["best_total_face_self_crossings"]
    return {"status":"EXACT_RATIONAL_SIGN_CHECK_OF_NONEMBEDDED_12_PLANE_CANDIDATE",
      "optimization_candidate_planes":12,
      "exact_Fraction_parsing_of_input_decimal_strings":True,
      "dual_vertices_verified":len(xy),
      "face_boundary_length":11,
      "exact_proper_crossings_each_face":counts,
      "exact_total_proper_crossings":sum(counts),
      "nonadjacent_segment_orientation_zero_tests":degeneracies,
      "failure_of_local_face_simplicity":sum(counts)>0,
      "limits":"This exact arithmetic ONLY certifies crossings in a particular failed candidate. It proves neither genus-6 dual nonrealizability nor optimality of the local search."}
if __name__=="__main__":
    obj=run()
    OUT.write_text(json.dumps(obj,indent=2)+"\n")
    print("PASS",obj["status"],obj["exact_total_proper_crossings"],flush=True)
