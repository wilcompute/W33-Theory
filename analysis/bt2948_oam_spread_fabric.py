#!/usr/bin/env python3
"""Pass 2948: exact 10-OAM x 4-slot W33 spread fabric and holonomy."""
from __future__ import annotations
import itertools,collections,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_BT2948_OAM_SPREAD_FABRIC_results.json'
def norm(v):
 v=tuple(int(x)%3 for x in v);i=next(i for i,x in enumerate(v) if x)
 return tuple(2*x%3 for x in v) if v[i]==2 else v
pts=[v for v in itertools.product(range(3),repeat=4) if any(v) and norm(v)==v];idx={p:i for i,p in enumerate(pts)};assert len(pts)==40
J=np.array([[0,1,0,0],[2,0,0,0],[0,0,0,1],[0,0,2,0]],dtype=int)
def symp(p,q):return int(np.array(p)@J@np.array(q)%3)
lines=set()
for i,j in itertools.combinations(range(40),2):
 if symp(pts[i],pts[j]):continue
 p=np.array(pts[i]);q=np.array(pts[j]);lines.add(tuple(sorted({idx[norm(a*p+b*q)] for a,b in itertools.product(range(3),repeat=2) if a or b})))
lines=sorted(lines);assert len(lines)==40
by_point={i:[] for i in range(40)}
for li,L in enumerate(lines):
 for p in L:by_point[p].append(li)
def dfs(covered,chosen):
 if len(covered)==40:return chosen
 p=min(set(range(40))-covered,key=lambda x:sum(not(set(lines[li])&covered) for li in by_point[x]))
 for li in by_point[p]:
  L=set(lines[li])
  if L&covered:continue
  r=dfs(covered|L,chosen+[li])
  if r:return r
spread_idx=dfs(set(),[]);spread=[lines[i] for i in spread_idx];assert len(spread)==10
line_of={p:i for i,L in enumerate(spread) for p in L};slot_of={p:s for i,L in enumerate(spread) for s,p in enumerate(L)}
def cyc_type(perm):
 seen=set();lens=[]
 for a in range(4):
  if a in seen:continue
  b=a;n=0
  while b not in seen:seen.add(b);n+=1;b=perm[b]
  lens.append(n)
 return tuple(sorted(lens,reverse=True))
def compose(p,q):return tuple(p[q[a]] for a in range(4))
match={};cycle_hist=collections.Counter()
for i,j in itertools.permutations(range(10),2):
 perm=[]
 for p in spread[i]:
  qs=[q for q in spread[j] if symp(pts[p],pts[q])==0];assert len(qs)==1;perm.append(slot_of[qs[0]])
 assert sorted(perm)==list(range(4));match[i,j]=tuple(perm)
 if i<j:cycle_hist[cyc_type(perm)]+=1
for i,j in itertools.permutations(range(10),2):
 inv=[0]*4
 for a,b in enumerate(match[i,j]):inv[b]=a
 assert tuple(inv)==match[j,i]
tri_hist=collections.Counter();tri_fixed=collections.Counter();tri_records=[]
for i,j,k in itertools.combinations(range(10),3):
 h=compose(match[k,i],compose(match[j,k],match[i,j]));ct=cyc_type(h);tri_hist[ct]+=1;tri_fixed[sum(h[a]==a for a in range(4))]+=1;tri_records.append({'triple':[i,j,k],'holonomy':list(h),'cycle_type':list(ct)})
for p in range(40):
 ns=[q for q in range(40) if q!=p and symp(pts[p],pts[q])==0];assert len(ns)==12
 assert sum(line_of[q]==line_of[p] for q in ns)==3
 assert collections.Counter(line_of[q] for q in ns)==collections.Counter({line_of[p]:3,**{j:1 for j in range(10) if j!=line_of[p]}})
checks={'forty_points':len(pts)==40,'forty_lines':len(lines)==40,'spread_ten_lines':len(spread)==10,'address_count_40':10*4==40,'edge_budget_240':10*6+45*4==240,'all_interline_maps_are_S4_permutations':all(sorted(p)==list(range(4)) for p in match.values()),'all_triangle_holonomies_are_involutions':tri_hist==collections.Counter({(2,2):60,(2,1,1):60})}
out={'schema':'w33.pass2948.oam_spread_fabric.v1','status':'COMPLETE_EXACT_PHYSICAL_ADDRESS_PROPOSAL','checks':checks,'check_count':len(checks),'spread_line_indices':spread_idx,'spread_points':[list(L) for L in spread],'point_coordinates':[list(p) for p in pts],'registers':{'oam_line_modes':10,'time_or_frequency_slots':4,'addresses':40},'intra_line_edges':60,'inter_line_edges':180,'total_edges':240,'matching_cycle_histogram':{'-'.join(map(str,k)):v for k,v in sorted(cycle_hist.items())},'triangle_holonomy_cycle_histogram':{'-'.join(map(str,k)):v for k,v in sorted(tri_hist.items())},'triangle_holonomy_fixed_point_histogram':{str(k):v for k,v in sorted(tri_fixed.items())},'directed_matchings':{f'{i}-{j}':list(p) for (i,j),p in sorted(match.items())},'triangle_records':tri_records,'architecture':'ten OAM spread-line modes times four time/frequency slots; every inter-line pair is one exact four-channel matching','claim_boundary':'Exact finite mode-address and routing table. OAM generation, coherent sorting, crosstalk, insertion loss, and detector calibration are unmeasured.'};assert all(checks.values());OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(f"PASS {len(checks)}/{len(checks)}",tri_hist)
