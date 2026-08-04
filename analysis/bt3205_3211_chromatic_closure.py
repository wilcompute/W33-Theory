#!/usr/bin/env python3
"""Passes 3205-3211: exact port geometry for the W33 ten-colour frontier.

Reuses the independently tested Pass-3187 geometry constructor, then freezes the
45-block support factorisation, 135-cell association scheme, complete deficit
profile census, Smith/p-adic audit, graph-uncertainty spectra, and a deterministic
proof-producing ten-colour CNF. It does not claim SAT or UNSAT.
"""
from __future__ import annotations
import argparse, collections, hashlib, importlib.util, itertools, json, math
from fractions import Fraction
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_BT3205_BT3211_CHROMATIC_CLOSURE_results.json'
SPEC=importlib.util.spec_from_file_location('bt3187',ROOT/'analysis/bt3187_3192_chromatic_defect_block_filter.py')
BASE=importlib.util.module_from_spec(SPEC); assert SPEC.loader; SPEC.loader.exec_module(BASE)


def cells_of(h,blocks):
 out=[]; by=[]
 for block in blocks:
  local=h[np.ix_(block,block)]; comp=np.ones((12,12),dtype=np.int8)-np.eye(12,dtype=np.int8)-local
  unseen=set(range(12)); cc=[]
  while unseen:
   seed=min(unseen); unseen.remove(seed); q=[seed]; part={seed}
   while q:
    x=q.pop()
    for y in list(unseen):
     if comp[x,y]: unseen.remove(y);part.add(y);q.append(y)
   cc.append(sorted(block[x] for x in part))
  cc.sort(); assert tuple(sorted(map(len,cc)))==(4,4,4);by.append(cc);out+=cc
 return out,by


def rank_mod(a,p):
 a=np.array(a,dtype=np.int64)%p;m,n=a.shape;r=0
 for c in range(n):
  q=next((i for i in range(r,m) if a[i,c]),None)
  if q is None:continue
  a[[r,q]]=a[[q,r]];a[r]=a[r]*pow(int(a[r,c]),-1,p)%p
  for i in range(m):
   if i!=r and a[i,c]:a[i]=(a[i]-a[i,c]*a[r])%p
  r+=1
  if r==m:break
 return r


def profiles(total=60,parts=10,top=None):
 if parts==0:
  if total==0:yield ()
  return
 top=min(total if top is None else top,total,59);bottom=max(0,total-59*(parts-1))
 for x in range(top,bottom-1,-1):
  for rest in profiles(total-x,parts-1,x):yield (x,)+rest


def fracspec(a):return [str(Fraction(float(x)).limit_denominator(10000)) for x in np.linalg.eigvalsh(a.astype(float))]
def coloring11():return BASE.load_coloring()
load_coloring11=coloring11


def verify_ten_coloring(colors):
 _,_,_,_,_,m,h=BASE.build_geometry();colors=np.asarray(colors,dtype=np.int64)
 checks={'length_540':len(colors)==540,'colors_0_to_9':len(colors)==540 and set(map(int,colors))<=set(range(10))}
 hist=collections.Counter()
 if all(checks.values()):
  checks['proper']=all(colors[u]!=colors[v] for u,v in zip(*np.where(np.triu(h,1))))
  missing=[]
  for e in range(240):
   x=sorted(set(range(10))-set(map(int,colors[np.where(m[:,e])[0]])));missing.append(x)
  checks['one_missing_color_per_W33_edge']=all(len(x)==1 for x in missing)
  hist=collections.Counter(x[0] for x in missing if len(x)==1)
 else:checks.update(proper=False,one_missing_color_per_W33_edge=False)
 return {'valid':all(checks.values()),'checks':checks,'class_sizes':dict(sorted(collections.Counter(map(int,colors)).items())) if len(colors)==540 else {},'missing_color_histogram':dict(sorted(hist.items()))}


def cnf_shape_hash(h,m):
 k=10;xvars=5400;nvars=7800;nclauses=146289;sha=hashlib.sha256();sha.update(f'p cnf {nvars} {nclauses}\n'.encode())
 x=lambda v,c:1+v*k+c; miss=lambda e,c:1+xvars+e*k+c
 def emit(xs):sha.update((' '.join(map(str,xs))+' 0\n').encode())
 for v in range(540):
  emit([x(v,c) for c in range(k)])
  for a,b in itertools.combinations(range(k),2):emit([-x(v,a),-x(v,b)])
 for u,v in zip(*np.where(np.triu(h,1))):
  for c in range(k):emit([-x(int(u),c),-x(int(v),c)])
 inc=[list(map(int,np.where(m[:,e])[0])) for e in range(240)];assert all(len(z)==9 for z in inc)
 for e,fs in enumerate(inc):
  emit([miss(e,c) for c in range(k)])
  for a,b in itertools.combinations(range(k),2):emit([-miss(e,a),-miss(e,b)])
  for c in range(k):
   for v in fs:emit([-miss(e,c),-x(v,c)])
   emit([x(v,c) for v in fs]+[miss(e,c)])
 for c,v in enumerate(inc[0]):emit([x(v,c)])
 return nvars,nclauses,sha.hexdigest()


def emit_cnf(path,h,m):
 k=10;xvars=5400;nvars,nclauses,expected=cnf_shape_hash(h,m);inc=[list(map(int,np.where(m[:,e])[0])) for e in range(240)]
 x=lambda v,c:1+v*k+c;miss=lambda e,c:1+xvars+e*k+c
 with path.open('w',encoding='ascii') as out:
  out.write(f'p cnf {nvars} {nclauses}\n')
  clause=lambda z:out.write(' '.join(map(str,z))+' 0\n')
  for v in range(540):
   clause([x(v,c) for c in range(k)])
   for a,b in itertools.combinations(range(k),2):clause([-x(v,a),-x(v,b)])
  for u,v in zip(*np.where(np.triu(h,1))):
   for c in range(k):clause([-x(int(u),c),-x(int(v),c)])
  for e,fs in enumerate(inc):
   clause([miss(e,c) for c in range(k)])
   for a,b in itertools.combinations(range(k),2):clause([-miss(e,a),-miss(e,b)])
   for c in range(k):
    for v in fs:clause([-miss(e,c),-x(v,c)])
    clause([x(v,c) for v in fs]+[miss(e,c)])
  for c,v in enumerate(inc[0]):clause([x(v,c)])
 assert hashlib.sha256(path.read_bytes()).hexdigest()==expected


def certificate():
 points,a,lines,edges,frames,m,h=BASE.build_geometry();_,blocks,pairorbits=BASE.canonical_blocks(points,a,lines,frames);cells,by=cells_of(h,blocks)
 d=np.zeros((540,45),dtype=np.int64)
 for j,b in enumerate(blocks):d[b,j]=1
 n=((d.T@m)>0).astype(np.int64);g=(n@n.T==1).astype(np.int64);np.fill_diagonal(g,0)
 cellok=portok=k33=oa=True
 for bi,local in enumerate(by):
  for cell in local:cellok&=np.array_equal(m[cell].sum(0),n[bi])
  maps=[{v:j for j,v in enumerate(cell)} for cell in local];mult=collections.Counter()
  for e in np.where(n[bi])[0]:
   selected=[v for v in blocks[bi] if m[v,e]];portok&=len(selected)==3 and all(sum(v in cell for v in selected)==1 for cell in local)
   word=tuple(maps[c][next(v for v in selected if v in local[c])] for c in range(3));mult[word]+=int(sum(n[bj,e] for bj in range(45) if bj!=bi))
  words=sorted(mult);oa&=len(words)==16 and set(mult.values())=={2} and all(len({(w[i],w[j]) for w in words})==16 for i,j in itertools.combinations(range(3),2))
 for i,j in itertools.combinations(range(45),2):
  shared=list(map(int,np.where(n[i]&n[j])[0]));cross=h[np.ix_(blocks[i],blocks[j])]
  if not shared:k33&=int(cross.sum())==0
  elif len(shared)==1:
   e=shared[0];left=[v for v in blocks[i] if m[v,e]];right=[v for v in blocks[j] if m[v,e]];k33&=len(left)==len(right)==3 and int(cross.sum())==9 and bool(np.all(h[np.ix_(left,right)]==1))
  else:k33=False
 b=np.zeros((540,135),dtype=np.int64)
 for j,c in enumerate(cells):b[c,j]=1
 c=b.T@h@b;s=(c==1).astype(np.int64);l=(c==16).astype(np.int64);np.fill_diagonal(s,0);np.fill_diagonal(l,0);z=np.ones((135,135),dtype=np.int64)-np.eye(135,dtype=np.int64)-s-l;rels=[np.eye(135,dtype=np.int64),l,s,z]
 inter=[];scheme=True
 for ri in rels:
  row=[]
  for rj in rels:
   prod=ri@rj;coef=[]
   for rel in rels:
    vals=prod[rel.astype(bool)];coef.append(int(vals[0]));scheme&=len(set(map(int,vals)))==1
   scheme&=np.array_equal(prod,sum(x*rel for x,rel in zip(coef,rels)));row.append(coef)
  inter.append(row)
 from sympy import Matrix,ZZ
 from sympy.matrices.normalforms import smith_normal_form
 snf=smith_normal_form(Matrix(n),domain=ZZ);diag=[abs(int(snf[i,i])) for i in range(min(snf.shape)) if snf[i,i]!=0]
 prof=list(profiles());tr=collections.Counter(3600-sum(x*x for x in q) for q in prof);maxhist=collections.Counter(max(q) for q in prof)
 colors=coloring11();sizes=collections.Counter(map(int,colors));covercolor=next(c for c,v in sizes.items() if v==60);cover=sorted(map(int,np.where(colors==covercolor)[0]));coverok=all(h[u,v]==0 for u,v in itertools.combinations(cover,2));padic=True
 for deficit in range(60):
  delta=m[cover[:deficit]].sum(0);padic&=set(map(int,delta))<={0,1} and int(delta.sum())==4*deficit
 edgeprofile=collections.Counter((len(fs:=np.where(m[:,e])[0]),len(set(map(int,colors[fs])))) for e in range(240))
 def surj4(k):return sum((-1)**j*math.comb(k,j)*(k-j)**4 for j in range(k+1))
 localcount=localtypes=0
 for aa in range(1,5):
  for bb in range(1,5):
   for cc in range(1,5):
    if aa+bb+cc<=10:localtypes+=1;localcount+=math.comb(10,aa)*math.comb(10-aa,bb)*math.comb(10-aa-bb,cc)*surj4(aa)*surj4(bb)*surj4(cc)
 u,sv,vt=np.linalg.svd(m.astype(float),full_matrices=False);r=int(sum(sv>1e-9));pf=np.eye(540)-u[:,:r]@u[:,:r].T;pe=np.eye(240)-vt[:r].T@vt[:r]
 fspec={tuple(fracspec(pf[np.ix_(block,block)])) for block in blocks};espec={tuple(fracspec(pe[np.ix_(np.where(n[i])[0],np.where(n[i])[0])])) for i in range(45)}
 vars_,clauses,cnfhash=cnf_shape_hash(h,m)
 checks={'w33_counts':(len(points),len(lines),len(edges),len(frames))==(40,40,240,540),'frame_graph_540_8640_32':int(h.sum()//2)==8640 and set(map(int,h.sum(1)))=={32},'H_plus_4I_equals_MMT':np.array_equal(h+4*np.eye(540,dtype=np.int16),m@m.T),'canonical_blocks':len(blocks)==45 and all(len(x)==12 for x in blocks) and pairorbits==[540,3240,3240,4320,12960],'support_incidence_45x240_16x3':n.shape==(45,240) and set(map(int,n.sum(1)))=={16} and set(map(int,n.sum(0)))=={3},'block_graph_SRG_45_32_22_24':set(map(int,g.sum(1)))=={32} and {int((g@g)[i,j]) for i,j in itertools.combinations(range(45),2) if g[i,j]}=={22} and {int((g@g)[i,j]) for i,j in itertools.combinations(range(45),2) if not g[i,j]}=={24},'each_cell_exact_cover_of_block_support':bool(cellok),'shared_support_edge_is_K33':bool(k33),'ports_are_OA_16_3_4_2':bool(portok and oa),'cell_rank4_association_scheme':bool(scheme),'support_Smith_1pow44_times3':collections.Counter(diag)==collections.Counter({1:44,3:1}),'all_195490_deficit_profiles':len(prof)==195490,'unique_balanced_profile':tr[3240]==1 and (6,)*10 in prof,'p_adic_linear_filter_vacuous_all_weights':bool(coverok and padic),'frozen_11_coloring_has_nine_distinct_colors_at_each_edge':edgeprofile==collections.Counter({(9,9):240}),'frame_uncertainty_spectrum':fspec=={('2/9',)+('43/81',)*9+('1',)*2},'edge_uncertainty_spectrum':espec=={('0',)*10+('1/6',)*6},'cnf_shape':(vars_,clauses)==(7800,146289)};assert all(checks.values()),[k for k,v in checks.items() if not v]
 data={'schema':'w33.pass3205_3211.chromatic_closure.v1','status':'PASS_EXACT_STRUCTURAL_REDUCTION_WITHOUT_TEN_COLOR_DECISION','live_boundary':'10 <= chi(H) <= 11','pass3205_defect_gram_outer_quotient':{'sorted_deficit_profiles':len(prof),'definition':'d_i=60-s_i, 0<=d_i<=59, sum d_i=60','trace_K':'3600-sum_i d_i^2','trace_K_min':min(tr),'trace_K_max':max(tr),'distinct_trace_values':len(tr),'unique_trace_maximizer':[6]*10,'maximum_deficit_histogram':{str(k):v for k,v in sorted(maxhist.items())},'boundary':'This exhausts the diagonal/class-size quotient, not all 45 off-diagonal colour-pair edge counts.'},'pass3206_proof_solver':{'encoding':'ten frame colours plus the unique missing colour at every one of the 240 W33 edges','variables':vars_,'clauses':clauses,'dimacs_sha256':cnfhash,'symmetry_break':'one canonical nine-frame clique fixed to colours 0..8','local_K444_labeled_assignments':localcount,'local_colour_usage_types':localtypes,'status':'INSTANCE_AND_CHECKER_READY_NO_SAT_OR_UNSAT_CERTIFICATE'},'pass3207_delsarte_terwilliger':{'cell_scheme_order':135,'relations':['identity','same-block-other-cell','one-frame cross-edge','empty'],'valencies':[1,2,96,36],'multiplicities':[1,24,20,90],'P':[[1,2,96,36],[1,2,6,-9],[1,2,-12,9],[1,-1,0,0]],'Q':[['1','24','20','90'],['1','24','20','-45'],['1','3/2','-5/2','0'],['1','-6','5','0']],'intersection_coefficients':inter,'krein_parameters_nontrivial':{'11':['24','21/2','15','0'],'12':['0','25/2','9','0'],'13':['0','0','0','24'],'22':['20','15/2','10','0'],'23':['0','0','0','20'],'33':['90','90','90','45']},'ordinary_ratio_bound_on_singleton_relation':9,'ordinary_ratio_bound_on_45_block_graph':9,'conclusion':'The complete commutative scheme stalls at nine; a stronger bound must use split port/triple data.'},'pass3208_p_adic':{'support_incidence_smith_diagonal':{'1':44,'3':1},'support_incidence_ranks':{'Q':45,'F2':rank_mod(n,2),'F3':rank_mod(n,3),'F5':rank_mod(n,5)},'consequence':'exactly one 3-primary invariant factor and no 5-primary torsion','linear_defect_filter':'vacuous for every possible weight 4d, 0<=d<=59, by deleting d frames from a frozen exact cover','conclusion':'Any p-adic obstruction must include nonlinear matching/port compatibility.'},'pass3209_A4_D4_cut_factorisation':{'block_support_incidence':'N is 45x240 with row sum 16 and column sum 3','gram_identity':'N N^T = 16 I + A_SRG(45,32,22,24)','cell_factorisation':'each of the three K4 cells in a block is an exact cover of the same 16 W33 edges','cross_block_factorisation':'two blocks are nonadjacent or share one W33 edge; the induced frame bipartite graph is respectively empty or K3,3','triangle_decomposition':'the 720 block-graph edges decompose into 240 triangles, one per W33 edge','port_code':'each block has OA(16,3,4,2) ports, each used by exactly two neighbouring blocks','interpretation':'H is the line graph of the 4-uniform linear hypergraph with 240 W33-edge vertices and 540 frame hyperedges; a ten-colouring is a ten-edge-colouring with one missing colour at every degree-nine vertex.'},'pass3210_tropical_profile':{'profiles':len(prof),'energy':'sum d_i^2','energy_min':360,'energy_max':3600-min(tr),'energy_levels':len(tr),'conclusion':'strict convexity isolates the balanced 54^10 profile but does not exclude unbalanced profiles.'},'pass3211_uncertainty':{'frame_Eminus4_block_localisation_eigenvalues':sorted(next(iter(fspec)),key=lambda x:float(Fraction(x))),'edge_kernel_block_support_localisation_eigenvalues':sorted(next(iter(espec)),key=lambda x:float(Fraction(x))),'frame_conclusion':'two exact E_-4 directions are fully localised in every 12-frame block, so a naive frame uncertainty obstruction fails','edge_conclusion':'the 15-dimensional edge kernel has maximum concentration 1/6 on any 16-edge block support'},'checks':checks,'claim_boundary':'No ten-colouring and no checked UNSAT proof was obtained. Time-bounded MILP and local-search failures are diagnostics only.'};data['sha256_without_hash_field']=hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest();return data


def main():
 p=argparse.ArgumentParser();p.add_argument('--emit-cnf',type=Path);p.add_argument('--verify-model',type=Path);args=p.parse_args()
 if args.verify_model:
  tok=list(map(int,args.verify_model.read_text().split()));tok=tok[1:] if len(tok)==541 and tok[0]==10 else tok;verdict=verify_ten_coloring(tok);print(json.dumps(verdict,indent=2,sort_keys=True));raise SystemExit(0 if verdict['valid'] else 1)
 data=certificate();OUT.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
 if args.emit_cnf:
  *_,m,h=BASE.build_geometry();emit_cnf(args.emit_cnf,h,m)
 print(json.dumps({'status':data['status'],'sha256':data['sha256_without_hash_field']},sort_keys=True))
if __name__=='__main__':main()
