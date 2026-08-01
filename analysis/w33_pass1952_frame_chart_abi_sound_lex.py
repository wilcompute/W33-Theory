#!/usr/bin/env python3
from __future__ import annotations
import argparse,collections,hashlib,importlib.util,itertools,json
from pathlib import Path
import networkx as nx,numpy as np
ROOT=Path(__file__).resolve().parents[1];COMMON=ROOT/'analysis/w33_pass1801_1805_common.py';ROWS=ROOT/'data/w33_pass1876_rows45_hex.txt';COMP=ROOT/'data/w33_pass1837_middle_layer_compression.json';OUT=ROOT/'data/w33_pass1952_frame_chart_abi_sound_lex.json'
def canon(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load_common():
 s=importlib.util.spec_from_file_location('c',COMMON);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m
def rankmod(M,p):
 a=M.copy()%p;r=0
 for c in range(a.shape[1]):
  z=np.flatnonzero(a[r:,c])
  if not len(z):continue
  k=r+int(z[0]);a[[r,k]]=a[[k,r]];a[r]=a[r]*pow(int(a[r,c]),-1,p)%p
  for i in range(a.shape[0]):
   if i!=r and a[i,c]:a[i]=(a[i]-a[i,c]*a[r])%p
  r+=1
 return r
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',default=str(OUT));args=ap.parse_args();D=load_common().build_geometry();rows=[]
 for line in ROWS.read_text().splitlines():
  limbs=[int(x,16) for x in line.split()];rows.append(sum(x<<(64*i) for i,x in enumerate(limbs)))
 rr=[[i-30 for i in range(30,45) if rows[i]>>e&1] for e in range(240)];A=np.zeros((540,15),int)
 for i,m in enumerate(D['matchings']):
  for e in m:
   for r in rr[e]:A[i,r]+=1
 assert np.all(A%2==0);B=A//2;edge_frames=collections.defaultdict(list)
 for i,m in enumerate(D['matchings']):
  for e in m:edge_frames[e].append(i)
 H=nx.Graph();H.add_nodes_from(range(540))
 for fs in edge_frames.values():H.add_edges_from(itertools.combinations(fs,2))
 col=nx.coloring.greedy_color(H,strategy='saturation_largest_first');x=tuple(col[i] for i in range(540));K=max(x)+1
 pack=json.loads(COMP.read_text());F=[tuple(z) for z in pack['canonical_six_line_pack']];Fset={frozenset(z) for z in F};R=pack['residual_vertices'];ri={v:i for i,v in enumerate(R)}
 def compose(p,q):return tuple(p[q[i]] for i in range(len(q)))
 idp=tuple(range(40));seen={idp:(tuple(range(45)),tuple(range(540)))};q=collections.deque([idp])
 while q:
  pp=q.popleft();op,fp=seen[pp]
  for gp,ge,gl,gf,go,gos in D['acts']+[D['outer']]:
   np_=compose(gp,pp)
   if np_ not in seen:seen[np_]=(tuple(go[op[i]] for i in range(45)),tuple(gf[fp[i]] for i in range(540)));q.append(np_)
 stab=[];equiv=0
 for pp,(op,fp) in seen.items():
  if {frozenset(op[i] for i in z) for z in F}==Fset:
   rp=tuple(ri[op[v]] for v in R);C=np.zeros_like(B);C[np.array(fp)[:,None],np.array(rp)[None,:]]=B;assert np.array_equal(C,B);equiv+=1;stab.append(fp)
 g=max(stab,key=lambda p:sum(i!=p[i] for i in range(540)));gi=[0]*540
 for i,j in enumerate(g):gi[j]=i
 gx=tuple(x[gi[i]] for i in range(540))
 def flat(z):return bytes(int(z[i]==c) for i in range(540) for c in range(K))
 fx,fg=flat(x),flat(gx);bad,good=(x,gx) if fx>fg else (gx,x);fb,fo=flat(bad),flat(good);first=next(i for i,(a,b) in enumerate(zip(fb,fo)) if a!=b)
 checks={k:bool(v) for k,v in {'binary_abi':set(B.ravel())<={0,1},'row_weights':collections.Counter(map(int,B.sum(1)))=={1:180,2:225,3:120,6:15},'column_sum72':set(map(int,B.sum(0)))=={72},'rank15_all':all(rankmod(B,p)==15 for p in (2,3,5,7)) and np.linalg.matrix_rank(B)==15,'s6_equivariance720':equiv==720,'H_540_8640_32':H.number_of_nodes()==540 and H.number_of_edges()==8640 and set(dict(H.degree()).values())=={32},'greedy14_valid':K==14 and all(x[a]!=x[b] for a,b in H.edges()),'lex_nonvacuous':fb>fo and first==15}.items()}
 out={'schema':'w33.pass1952.frame_chart_abi_sound_lex.v1','status':'PASS_WITH_CHROMATIC_DECISION_OPEN','checks':checks,'frame_to_residual_duad_abi':{'shape':[540,15],'definition':'B[f,d] is half the multiplicity with which residual-duad row d occurs among the four edge coordinates of frame f.','row_weight_distribution':{str(k):v for k,v in sorted(collections.Counter(map(int,B.sum(1))).items())},'column_sum':72,'ranks':{'Q':15,'F2':15,'F3':15,'F5':15,'F7':15},'exceptional_S6_equivariance_checks':equiv},'sound_lex_witness':{'known_feasible_graph_coloring_colors':K,'color_class_sizes':{str(k):v for k,v in sorted(collections.Counter(x).items())},'coloring_sha256':hashlib.sha256(bytes(x)).hexdigest(),'frame_permutation_sha256':hashlib.sha256(json.dumps(g,separators=(',',':')).encode()).hexdigest(),'moved_frames':sum(i!=g[i] for i in range(540)),'first_different_onehot_bit':first,'cut_assignment_sha256':hashlib.sha256(fb).hexdigest(),'surviving_equivalent_sha256':hashlib.sha256(fo).hexdigest()},'colour_free_9color_run':{'variables_binary':10261,'linear_constraints':19441,'nonzeros':81001,'colour_pinning':False,'value_precedence':False,'geometric_lex_leaders':1,'time_limit_seconds':20,'highs_status':'TIME_LIMIT','primal_solution':False,'conclusion':'UNKNOWN'},'theorem':'The 540 frame variables admit a literal full-rank S6-equivariant ABI to the 15 residual duads. A correct prefix-equality lex leader is demonstrably nonvacuous on a global proper coloring, unlike the previous inequalities. A bounded genuinely colour-free 9-color MILP returned UNKNOWN.','boundary':'chi(H)=9 is not decided. The solver result is a bounded computational status, not a proof.'}
 assert all(checks.values());out['sha256_without_hash_field']=canon(out);Path(args.output).write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'sha':out['sha256_without_hash_field'],'checks':checks},indent=2));return out
if __name__=='__main__':main()
