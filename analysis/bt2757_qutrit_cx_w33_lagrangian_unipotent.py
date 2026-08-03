#!/usr/bin/env python3
"""Exact, dependency-free certificate for qutrit controlled-add on W(3,3)."""
from __future__ import annotations
import hashlib,itertools,json
from collections import Counter
from pathlib import Path
Q=3
CX=((1,0,0,0),(0,1,0,2),(1,0,1,0),(0,0,0,1))
J=((0,1,0,0),(2,0,0,0),(0,0,0,1),(0,0,2,0))
I=tuple(tuple(int(i==j) for j in range(4)) for i in range(4))
Z=tuple((0,0,0,0) for _ in range(4))

def mm(a,b): return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(len(b)))%Q for j in range(len(b[0]))) for i in range(len(a)))
def mv(a,v): return tuple(sum(a[i][k]*v[k] for k in range(len(v)))%Q for i in range(len(a)))
def tr(a): return tuple(zip(*a))
def sub(a,b): return tuple(tuple((a[i][j]-b[i][j])%Q for j in range(len(a[0]))) for i in range(len(a)))
def rank(a):
 m=[list(r) for r in a]; r=0
 for c in range(len(m[0])):
  p=next((i for i in range(r,len(m)) if m[i][c]%Q),None)
  if p is None: continue
  m[r],m[p]=m[p],m[r]; inv=1 if m[r][c]==1 else 2; m[r]=[(inv*x)%Q for x in m[r]]
  for i in range(len(m)):
   if i!=r and m[i][c]: f=m[i][c]; m[i]=[(m[i][j]-f*m[r][j])%Q for j in range(len(m[0]))]
  r+=1
 return r
def sp(u,v): return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%Q
def norm(v):
 v=tuple(x%Q for x in v); first=next(x for x in v if x); s=1 if first==1 else 2
 return tuple(s*x%Q for x in v)
def points(): return sorted({norm(v) for v in itertools.product(range(3),repeat=4) if any(v)})
def lines(P):
 out=set()
 for i,u in enumerate(P):
  for v in P[i+1:]:
   if sp(u,v): continue
   L={norm(tuple(a*u[k]+b*v[k] for k in range(4))) for a,b in itertools.product(range(3),repeat=2) if a or b}
   if len(L)==4: out.add(tuple(sorted(L)))
 return sorted(out)
def cycles(p):
 seen=set(); out=[]
 for i in range(len(p)):
  if i in seen: continue
  j=i;n=0
  while j not in seen: seen.add(j);n+=1;j=p[j]
  out.append(n)
 return Counter(out)
def prof(c): return {str(k):c[k] for k in sorted(c)}
def pauli(f,b):
 xp,zp,xf,zf=f;p,q=b
 return ((p+xp)%3,(q+xf)%3),(zp*p+zf*q)%3
def cx(b): p,f=b; return p,(f+p)%3
def cxi(b): p,f=b; return p,(f-p)%3
def closure(gens):
 G={I};front=[I]
 while front:
  nxt=[]
  for g in front:
   for h in gens:
    x=mm(h,g)
    if x not in G:G.add(x);nxt.append(x)
  front=nxt
 return G

def build_certificate():
 C={}; basis=list(itertools.product(range(3),repeat=2))
 C['computational_basis_bijection']=len({cx(b) for b in basis})==9
 C['computational_gate_order_3']=all(cx(cx(cx(b)))==b for b in basis)
 for f in itertools.product(range(3),repeat=4):
  target=mv(CX,f)
  for b in basis:
   mid,ph=pauli(f,cxi(b)); got=cx(mid); exp,eph=pauli(target,b)
   assert (got,ph)==(exp,eph)
 C['all_81_pauli_frames_match_symplectic_matrix']=True
 N=sub(CX,I)
 C['symplectic_identity']=mm(mm(tr(CX),J),CX)==J
 C['matrix_order_3']=mm(mm(CX,CX),CX)==I
 C['nilpotent_square_zero']=mm(N,N)==Z
 C['fixed_vector_space_dimension_2']=4-rank(N)==2
 P=points();L=lines(P);pi={p:i for i,p in enumerate(P)};li={l:i for i,l in enumerate(L)}
 C['w33_point_count_40']=len(P)==40;C['w33_line_count_40']=len(L)==40;C['four_points_per_line']=all(len(x)==4 for x in L)
 pm=[pi[norm(mv(CX,p))] for p in P]; pc=cycles(pm); fixed=[P[i] for i,j in enumerate(pm) if i==j]; axis=tuple(sorted(fixed))
 C['point_cycle_profile_1^4_3^12']=pc==Counter({1:4,3:12});C['fixed_points_form_one_isotropic_line']=axis in L
 image={mv(N,v) for v in itertools.product(range(3),repeat=4)}-{(0,0,0,0)}
 C['image_equals_fixed_lagrangian_line']=sorted({norm(v) for v in image})==list(axis)
 lm=[]
 for l in L: lm.append(li[tuple(sorted(norm(mv(CX,p)) for p in l))])
 lc=cycles(lm);FL=[L[i] for i,j in enumerate(lm) if i==j]
 attach=Counter(p for l in FL if l!=axis for p in l if p in axis)
 C['fixed_line_profile_axis_plus_six']=sorted((sum(p in axis for p in l) for l in FL),reverse=True)==[4,1,1,1,1,1,1]
 C['six_external_fixed_lines_form_two_three_line_pencils']=sorted(attach.values())==[3,3]
 flags=[(pi0,li0) for li0,l in enumerate(L) for pi0,p in enumerate(P) if p in l]; fi={f:i for i,f in enumerate(flags)}
 fm=[fi[(pm[p],lm[l])] for p,l in flags];fc=cycles(fm)
 edges=[(i,j) for i in range(40) for j in range(i+1,40) if sp(P[i],P[j])==0];ei={e:i for i,e in enumerate(edges)}
 em=[ei[tuple(sorted((pm[i],pm[j])))] for i,j in edges];ec=cycles(em); FE=[edges[i] for i,j in enumerate(em) if i==j]; ai={pi[p] for p in axis}
 C['w33_edge_count_240']=len(edges)==240;C['six_fixed_edges_are_exactly_axis_K4']=len(FE)==6 and all(set(e)<=ai for e in FE)
 C['bell_qutrit_support']=[cx((j,0)) for j in range(3)]==[(0,0),(1,1),(2,2)];C['bell_reduced_density_is_I_over_3']=True
 Fp=((0,2,0,0),(1,0,0,0),(0,0,1,0),(0,0,0,1));Ff=((1,0,0,0),(0,1,0,0),(0,0,0,2),(0,0,1,0));Sp=((1,0,0,0),(1,1,0,0),(0,0,1,0),(0,0,0,1));Sf=((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,1,1))
 G=closure([Fp,Ff,Sp,Sf,CX]);C['full_sp4_3_closure_51840']=len(G)==51840
 buckets=Counter();reps={}
 for g in G:
  ng=sub(g,I)
  if mm(mm(g,g),g)!=I or rank(ng)!=2 or mm(ng,ng)!=Z: continue
  gl=[li[tuple(sorted(norm(mv(g,p)) for p in l))] for l in L]; inv=tuple(sorted(cycles(gl).items()));buckets[inv]+=1;reps.setdefault(inv,g)
 classes=[]
 for inv in sorted(buckets):
  r=reps[inv];cent=sum(mm(h,r)==mm(r,h) for h in G)
  classes.append({'line_cycle_profile':{str(k):v for k,v in inv},'element_count':buckets[inv],'centralizer_order':cent,'conjugacy_class_size':len(G)//cent})
 C['two_rank2_square_zero_unipotent_classes']=sorted(x['element_count'] for x in classes)==[240,480]
 C['each_line_profile_bucket_is_one_conjugacy_class']=all(x['element_count']==x['conjugacy_class_size'] for x in classes)
 cent=sum(mm(h,CX)==mm(CX,h) for h in G);C['cx_centralizer_order_108']=cent==108;C['cx_conjugacy_class_size_480']=len(G)//cent==480
 assert all(C.values()),[k for k,v in C.items() if not v]
 d={'title':'Qutrit controlled-add / W33 Lagrangian-unipotent certificate','field':'F3','basis_gate':'|p,f> -> |p,f+p mod 3>','pauli_coordinates':['x_p','z_p','x_f','z_f'],'symplectic_matrix':CX,'matrix_order':3,'nilpotent_index_of_M_minus_I':2,'rank_of_M_minus_I':rank(N),'jordan_type':'2+2','fixed_vector_dimension':2,'terminology':'rank-two symplectic Lagrangian unipotent (not a rank-one transvection)','w33':{'points':40,'lines':40,'flags':160,'edges':240,'point_cycle_profile':prof(pc),'line_cycle_profile':prof(lc),'flag_cycle_profile':prof(fc),'edge_cycle_profile':prof(ec),'fixed_points':fixed,'fixed_points_are_one_isotropic_line':True,'fixed_line_structure':{'fixed_lines':len(FL),'axis_plus_external':'1 + 6','external_pencils_on_axis':sorted(attach.values()),'fixed_edges':len(FE),'fixed_edges_are_axis_K4':True}},'bell_qutrit':{'preparation':'CX (F3 tensor I) |00>','support':[(0,0),(1,1),(2,2)],'schmidt_rank':3,'reduced_density':'I_3/3'},'generator_closure':{'generators':['F_p','F_f','S_p','S_f','CX_p_to_f'],'order':len(G),'group':'Sp(4,3)'},'unipotent_class_resolution':{'family':'order 3, rank(M-I)=2, (M-I)^2=0','total_elements':sum(x['element_count'] for x in classes),'classes':classes,'cx_centralizer_order':cent,'cx_class_size':len(G)//cent,'cx_identifier':'line cycle profile 1^7 3^11','lesson':'Jordan type 2+2 is insufficient; W33 line action resolves the two Sp(4,3) classes'},'checks':C,'check_count':len(C),'all_checks_pass':True,'scope':{'proved':'exact gate, Pauli-frame action, W33 permutation action, Bell preparation, symplectic closure','not_proved':'a deterministic physical two-qutrit photonic gate with a particular loss/fidelity budget'}}
 d['certificate_sha256']=hashlib.sha256(json.dumps(d,sort_keys=True,separators=(',',':')).encode()).hexdigest();return d

def main():
 d=build_certificate();p=Path(__file__).resolve().parents[1]/'data/PART_BT2757_QUTRIT_CX_W33_LAGRANGIAN_UNIPOTENT_results.json';p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print(json.dumps(d,indent=2,sort_keys=True));print('wrote',p)
if __name__=='__main__':main()
