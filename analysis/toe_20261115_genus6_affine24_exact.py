#!/usr/bin/env python3
"""Exact affine gauge fixing of 12-plane genus-six dual from 36 to
24 parameters. Replays all 44 vertices and 12 face crossing counts in
Q with no floating-point or numpy dependency.
"""
import ast,json
from itertools import combinations
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
IN=ROOT/"data"/"toe_20261115_genus6_12plane_optimized_necessary.json"
OUT=ROOT/"data"/"toe_20261115_genus6_affine24_exact_certificate.json"
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def det3(a,b,c):
 return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def solve(rows,rhs):
 d=det3(*rows);assert d!=0
 cols=[tuple(rhs),tuple(rhs),tuple(rhs)]
 return (det3(rhs,[r[1] for r in rows],[r[2] for r in rows])/d,
         det3([r[0] for r in rows],rhs,[r[2] for r in rows])/d,
         det3([r[0] for r in rows],[r[1] for r in rows],rhs)/d)
def run():
 obj=json.loads(IN.read_text())
 co=[[F(str(z)) for z in line] for line in obj["parameters"]]
 normals=[(-a,-b,F(1)) for a,b,c in co]
 rhs=[row[2] for row in co]
 def point(indices):
  return solve([normals[i] for i in indices],[rhs[i] for i in indices])
 X0=point((1,2,3)); X1=point((0,2,3))
 X2=point((0,1,3)); X3=point((0,1,2))
 B=(sub(X1,X0),sub(X2,X0),sub(X3,X0))
 assert det3(*B)!=0
 form=[]
 for i in range(12):
  n=normals[i]; h=rhs[i]-dot(n,X0)
  row=tuple(dot(n,b) for b in B)
  if i==0:
   assert h!=0 and all(z==h for z in row);form.append(((F(1),F(1),F(1)),F(1)))
  elif i in (1,2,3):
   expect=tuple(F(int(j==i-1)) for j in range(3))
   assert h==0 and row[i-1]!=0 and all(row[j]==0 for j in range(3) if j!=i-1)
   form.append((expect,F(0)))
  else:
   assert h!=0
   form.append((tuple(z/h for z in row),F(1)))
 # Source facets are the 44 selected primal triangles.
 tree=ast.parse((ROOT/"analysis"/"w33_genus_six_execution.py").read_text())
 raw=next(ast.literal_eval(v.value) for v in tree.body if isinstance(v,ast.Assign)
          and any(isinstance(q,ast.Name) and q.id=="FACETS_ONE" for q in v.targets))
 faces=sorted(tuple(sorted(x-1 for x in f)) for f in raw)
 assert len(faces)==44 and len(set(faces))==44
 tid={f:i for i,f in enumerate(faces)}
 vertices=[]
 for ijk in faces:
  y=solve([form[i][0] for i in ijk],[form[i][1] for i in ijk])
  original=point(ijk)
  assert original==add(X0,tuple(sum(B[j][k]*y[j] for j in range(3)) for k in range(3)))
  vertices.append(y)
 # Intrinsic link around each primal vertex gives ordered dual 11-gon.
 bounds=[]
 for i in range(12):
  nbr={}
  for f in faces:
   if i not in f:continue
   x,y=(a for a in f if a!=i)
   nbr.setdefault(x,set()).add(y);nbr.setdefault(y,set()).add(x)
  assert len(nbr)==11 and all(len(v)==2 for v in nbr.values())
  cycle=[min(nbr),min(nbr[min(nbr)])]
  while len(cycle)<11:
   cycle.append(next(iter(nbr[cycle[-1]]-{cycle[-2]})))
  assert cycle[0] in nbr[cycle[-1]]
  bounds.append([tid[tuple(sorted((i,cycle[j],cycle[(j+1)%11])))] for j in range(11)])
 def orient(a,b,c,n):return dot(cross(sub(b,a),sub(c,a)),n)
 crossings=[]
 for i,seq in enumerate(bounds):
  n=form[i][0];p=[vertices[j] for j in seq]
  count=0
  for j,k in combinations(range(11),2):
   if k==j+1 or (j==0 and k==10):continue
   a,b=p[j],p[(j+1)%11];c,d=p[k],p[(k+1)%11]
   o=(orient(a,b,c,n),orient(a,b,d,n),orient(c,d,a,n),orient(c,d,b,n))
   assert all(x!=0 for x in o)
   if o[0]*o[1]<0 and o[2]*o[3]<0:count+=1
  crossings.append(count)
 assert sum(crossings)==8
 return {
  "status":"EXACT_36_TO_24_PARAMETER_AFFINE_GENUS6_DUAL_GAUGE",
  "original_planar_faces":12,"original_continuous_parameters":36,
  "affine_gauge_dimensions":12,"canonical_residual_plane_parameters":24,
  "four_reference_planes":["x+y+z=1","x=0","y=0","z=0"],
  "canonical_remaining_eight_plane_normalized_coefficients":
    [[str(x) for x in normal] for normal,h in form[4:]],
  "reference_tetrahedron_det_nonzero":True,
  "all_44_vertices_reconstructed_exactly":True,
  "dual_faces":12,"dual_edges":66,"dual_vertices":44,
  "face_crossings_each_in_3d_affine_chart":crossings,
  "exact_total_proper_face_crossings":sum(crossings),
  "scope":"Affine gauge changes do not alter the existence of an embedded planar-faced polyhedron, but a failed 8-crossing example remains failed. Exact 24-parameter reduction does not establish realizability or nonrealizability of this or the other 58 genus-six duals."
 }
if __name__=="__main__":
 d=run();OUT.write_text(json.dumps(d,indent=2)+"\n")
 print("PASS",d["status"],"crossings",d["exact_total_proper_face_crossings"],flush=True)
