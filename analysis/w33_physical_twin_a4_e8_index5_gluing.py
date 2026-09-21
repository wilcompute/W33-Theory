#!/usr/bin/env python3
"""Physical twin-A4 index-5 E8 gluing theorem.

The flagship contains two already-certified, distinct type-A4 root systems in
the same physical E8 factor:
  C: the hypercharge-orthogonal A4 organizing the four extra U(1) directions;
  G: the non-Abelian SU(5) A4 selected by the Wilson line.

Holotrade already checked C perpendicular G. This verifier takes the exact
physical E8 root coordinates and extracts the stronger full-lattice result:
C+G is an index-5 A4 direct-sum A4 sublattice of E8, and the 240 roots realize
the full SU(5)xSU(5) branching with an explicit Z5 discriminant-gluing law.
"""
from __future__ import annotations
import itertools, json, math
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_physical_twin_a4_e8_index5_gluing.json"

# Hypercharge-orthogonal extra-U(1) organizer A4, alpha2..alpha5 of the
# physical A5 organizer (Holotrade w33_flagship_a5_hypercharge_organizer).
CENTER=(
 (F(0),F(0),F(0),F(-1),F(0),F(1),F(0),F(0)),
 (F(-1,2),F(1,2),F(1,2),F(1,2),F(-1,2),F(-1,2),F(-1,2),F(1,2)),
 (F(0),F(0),F(0),F(0),F(1),F(0),F(1),F(0)),
 (F(1,2),F(-1,2),F(-1,2),F(-1,2),F(-1,2),F(-1,2),F(-1,2),F(1,2)),
)
# Physical Wilson-line SU(5) roots, reordered into an A4 Dynkin chain.
GAUGE=(
 (F(0),F(1),F(-1),F(0),F(0),F(0),F(0),F(0)),
 (F(1),F(0),F(1),F(0),F(0),F(0),F(0),F(0)),
 (F(-1,2),F(-1,2),F(-1,2),F(1,2),F(-1,2),F(1,2),F(1,2),F(1,2)),
 (F(0),F(0),F(0),F(0),F(1),F(0),F(-1),F(0)),
)
CARTAN=(
 (2,-1,0,0),(-1,2,-1,0),(0,-1,2,-1),(0,0,-1,2)
)
CINV=tuple(tuple(F(x,5) for x in row) for row in
 ((4,3,2,1),(3,6,4,2),(2,4,6,3),(1,2,3,4)))

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def gram(B): return tuple(tuple(dot(a,b) for b in B) for a in B)
def rank(rows):
    A=[list(map(F,r)) for r in rows]; m=len(A); n=len(A[0]); rr=0
    for c in range(n):
        p=next((i for i in range(rr,m) if A[i][c]),None)
        if p is None: continue
        A[rr],A[p]=A[p],A[rr]; z=A[rr][c]
        A[rr]=[x/z for x in A[rr]]
        for i in range(m):
            if i!=rr and A[i][c]:
                z=A[i][c]; A[i]=[A[i][j]-z*A[rr][j] for j in range(n)]
        rr+=1
    return rr
def det(M):
    A=[list(map(F,r)) for r in M]; n=len(A); ans=F(1)
    for c in range(n):
        p=next((i for i in range(c,n) if A[i][c]),None)
        if p is None:return F(0)
        if p!=c:A[c],A[p]=A[p],A[c];ans=-ans
        z=A[c][c];ans*=z
        for j in range(c,n):A[c][j]/=z
        for i in range(c+1,n):
            z=A[i][c]
            for j in range(c,n):A[i][j]-=z*A[c][j]
    return ans
def matvec(M,v): return tuple(sum(F(M[i][j])*v[j] for j in range(len(v))) for i in range(len(M)))
def proj_norm(r,B):
    b=tuple(dot(a,r) for a in B)
    return sum(b[i]*CINV[i][j]*b[j] for i in range(4) for j in range(4))
def discr_class(r,B):
    labels=[int(dot(r,a)) for a in B]
    return sum((i+1)*labels[i] for i in range(4))%5
def roots_e8():
    out=[]
    for i,j in itertools.combinations(range(8),2):
        for a in (1,-1):
            for b in (1,-1):
                v=[F(0)]*8;v[i]=F(a);v[j]=F(b);out.append(tuple(v))
    for s in itertools.product((1,-1),repeat=8):
        if sum(x<0 for x in s)%2==0:out.append(tuple(F(x,2) for x in s))
    assert len(out)==len(set(out))==240
    return out

def main(write=True):
    assert gram(CENTER)==gram(GAUGE)==tuple(tuple(F(x) for x in r) for r in CARTAN)
    cross=tuple(tuple(dot(a,b) for b in GAUGE) for a in CENTER)
    assert all(x==0 for row in cross for x in row)
    combined=CENTER+GAUGE
    assert rank(combined)==8
    G=gram(combined)
    assert det(G)==25
    index=math.isqrt(int(det(G)));assert index==5 and index*index==det(G)

    R=roots_e8()
    table=Counter()
    for r in R:
        nc,ng=proj_norm(r,CENTER),proj_norm(r,GAUGE)
        assert nc+ng==2
        cc,cg=discr_class(r,CENTER),discr_class(r,GAUGE)
        table[(str(nc),str(ng),cc,cg)]+=1
    expected={
      ("2","0",0,0):20,("0","2",0,0):20,
      ("6/5","4/5",2,1):50,("6/5","4/5",3,4):50,
      ("4/5","6/5",4,2):50,("4/5","6/5",1,3):50}
    assert dict(table)==expected
    assert all(cg==(3*cc)%5 for (_,_,cc,cg),n in table.items())

    # A4 weight class k has minimal norm k(5-k)/5 and dimensions
    # 1/4 -> 5/bar5, 2/3 -> 10/bar10.
    reps={
      (2,1):"(10,5)",(3,4):"(10bar,5bar)",
      (4,2):"(5bar,10)",(1,3):"(5,10bar)"}
    branch={reps[(cc,cg)]:n for (nc,ng,cc,cg),n in table.items() if cc}
    assert set(branch.values())=={50} and len(branch)==4
    assert 24+24+sum(branch.values())==248

    out={
      "schema":"w33.physical_twin_a4_e8_index5_gluing.v1",
      "status":"PASS_PHYSICAL_TWIN_A4_INDEX5_E8_GLUING",
      "headline":"The physical Wilson-line SU(5) root A4 and the hypercharge-orthogonal extra-U(1) organizer A4 are orthogonal and together span an index-5 A4+A4 sublattice of the same E8. Exhaustive enumeration of all 240 E8 roots gives 20+20 internal roots and four 50-root mixed sectors. Their A4 discriminant classes obey c_gauge=3*c_center mod 5, explicitly reconstructing the Z5 gluing and the adjoint branching 248=(24,1)+(1,24)+(10,5)+(10bar,5bar)+(5bar,10)+(5,10bar).",
      "physical_A4s":{
        "center_organizer":"hypercharge-orthogonal A4 organizing four extra U(1)s",
        "gauge":"Wilson-line SU(5) non-Abelian A4",
        "each_cartan_determinant":5,"cross_gram_zero":True,
        "combined_rank":8,"combined_gram_determinant":25,
        "index_in_E8":5,"overlattice_quotient":"Z/5"},
      "root_projection_census":[
        {"center_norm2":k[0],"gauge_norm2":k[1],"center_class":k[2],"gauge_class":k[3],"count":v}
        for k,v in sorted(table.items())],
      "gluing":{"law":"c_gauge = 3*c_center (mod 5)",
        "nonzero_class_pairs":[[1,3],[2,1],[3,4],[4,2]]},
      "branching":{"internal_center_roots":20,"internal_gauge_roots":20,
        "mixed_rep_dimensions":branch,
        "adjoint_dimension_identity":"248=24+24+50+50+50+50"},
      "physics_reading":"The parallel S5 Weyl structures on the physical SU(5) and on the extra-U(1) organizer are not an accidental duplicate and are not the same Cartan. They are the two orthogonal A4 factors of an index-5 maximal-rank E8 lattice decomposition. Holonomy keeps the gauge A4 non-Abelian while the complementary factor is used here as an Abelian charge organizer; this theorem does not assert an unbroken second SU(5) gauge group.",
      "boundary":"Exact E8 lattice/root theorem from the recorded flagship bases. It does not solve D/F flatness, does not make the complementary SU(5) an unbroken gauge symmetry, and does not identify the FI mod-5 collision quotient with the E8 gluing quotient without a further map.",
      "provenance":[
        "Holotrade data/w33_flagship_a5_hypercharge_organizer.json",
        "Holotrade analysis/the_flagship_wilson_line_has_the_cz_spectrum.py",
        "Holotrade analysis/FLAGSHIP_SINGLET_INVARIANTS.md"],
      "checks":{"two_A4_cartans":True,"orthogonal":True,"rank8":True,
        "index5":True,"all240_roots_classified":True,"four_mixed_50_sectors":True,
        "Z5_gluing_law":True,"adjoint_248_branching":True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2));return out
if __name__=="__main__":main(True)
