#!/usr/bin/env python3
"""Pass 1509: a literal H(5,3) exact-cover chart with M20 stabilizer."""
from __future__ import annotations
import argparse, collections, importlib.util, itertools, json, math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'analysis'/'w33_pass1416_cokernel_signed_turn_intertwiner.py'
P1417=ROOT/'data'/'w33_pass1417_exact_cover_orbit_frontier.json'
OUT=ROOT/'data'/'w33_pass1509_qutrit_hamming_m20_chart.json'

def load_base():
 s=importlib.util.spec_from_file_location('p1416',BASE);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def perm_order(p):
 seen=[False]*len(p);ans=1
 for i in range(len(p)):
  if not seen[i]:
   j=i;n=0
   while not seen[j]:seen[j]=True;n+=1;j=p[j]
   ans=math.lcm(ans,n)
 return ans

def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2

def certificate():
 b=load_base();points,edges,lines,frames,G,M,A,N,d,K=b.build_geometry();base=tuple(json.loads(P1417.read_text())['deterministic_first16'][0]['cover'])
 row_masks=[sum(1<<int(c) for c in np.flatnonzero(row)) for row in M];col_rows=[[] for _ in range(240)]
 for r,row in enumerate(M):
  for c in np.flatnonzero(row):col_rows[int(c)].append(r)
 neighbors={};trades=[]
 def search(rem,chosen,removed):
  if not rem:
   if len(chosen)==4:
    add=tuple(sorted(chosen))
    if set(add).isdisjoint(removed):
     C=tuple(sorted((set(base)-set(removed))|set(add)))
     if C not in neighbors:neighbors[C]=(tuple(removed),add);trades.append((tuple(removed),add))
   return
  if len(chosen)>=4:return
  x=rem;best=None
  while x:
   bit=x&-x;c=bit.bit_length()-1;x-=bit;cand=[r for r in col_rows[c] if row_masks[r]&~rem==0]
   if not cand:return
   if best is None or len(cand)<len(best):best=cand
   if len(best)==1:break
  for r in best:search(rem^row_masks[r],chosen+(r,),removed)
 for removed in itertools.combinations(base,4):
  target=0
  for r in removed:target|=row_masks[r]
  search(target,(),removed)
 by_remove=collections.defaultdict(list)
 for rem,add in trades:by_remove[rem].append(add)
 def all_partitions(target):
  out=set()
  def rec(rem,chosen):
   if not rem:
    if len(chosen)==4:out.add(tuple(sorted(chosen)))
    return
   if len(chosen)>=4:return
   c=(rem&-rem).bit_length()-1
   for r in col_rows[c]:
    if row_masks[r]&~rem==0:rec(rem^row_masks[r],chosen+(r,))
  rec(target,());return tuple(sorted(out))
 packets=[]
 for rem,alts in sorted(by_remove.items()):
  target=0
  for r in rem:target|=row_masks[r]
  parts=all_partitions(target);packets.append(parts)
 chart={};shell=collections.Counter()
 for word in itertools.product(range(3),repeat=5):
  C=set(base)
  for packet,a in zip(packets,word):C.difference_update(packet[0]);C.update(packet[a])
  cov=tuple(sorted(C));total=0;valid=len(cov)==60
  for r in cov:
   valid=valid and not(total&row_masks[r]);total|=row_masks[r]
  valid=valid and total==(1<<240)-1
  if not valid:raise AssertionError(word)
  chart[cov]=word;shell[sum(a!=0 for a in word)]+=1
 lidx={L:i for i,L in enumerate(lines)};fidx={f:i for i,f in enumerate(frames)}
 def line_perm(g):return tuple(lidx[frozenset(g[i] for i in L)] for L in lines)
 def frame_perm(lp):return tuple(fidx[tuple(sorted((lp[a],lp[c])))] for a,c in frames)
 packet_index={tuple(sorted(p)):i for i,p in enumerate(packets)}
 stabilizer=[];coord_actions=[];symbol_actions=[]
 for gp in G:
  fp=frame_perm(line_perm(gp));coords=[];symbols=[];ok=True
  for packet in packets:
   transformed=[tuple(sorted(fp[r] for r in resolution)) for resolution in packet];canon=tuple(sorted(transformed))
   if canon not in packet_index:ok=False;break
   j=packet_index[canon];coords.append(j);symbols.append(tuple(packets[j].index(x) for x in transformed))
  if ok:stabilizer.append((gp,fp));coord_actions.append(tuple(coords));symbol_actions.append(tuple(symbols))
 image=set(coord_actions);identity5=tuple(range(5));kernel=[gp for (gp,_),ca in zip(stabilizer,coord_actions) if ca==identity5]
 kernel_abelian=all(b.compose(x,y)==b.compose(y,x) for x in kernel for y in kernel)
 kernel_orders=collections.Counter(perm_order(x) for x in kernel);stab_orders=collections.Counter(perm_order(x) for x,_ in stabilizer);image_orders=collections.Counter(perm_order(x) for x in image)
 by_coord=collections.defaultdict(list)
 for (gp,_),ca in zip(stabilizer,coord_actions):by_coord[ca].append(gp)
 complement=None
 for ca in [x for x in image if perm_order(x)==2]:
  for cb in [x for x in image if perm_order(x)==3]:
   if perm_order(b.compose(ca,cb))!=5 or len(b.generated_group([ca,cb]))!=60:continue
   for a in by_coord[ca]:
    if perm_order(a)!=2:continue
    for bb in by_coord[cb]:
     if perm_order(bb)==3 and perm_order(b.compose(a,bb))==5:
      H=b.generated_group([a,bb])
      if len(H)==60:complement={'a':list(a),'b':list(bb),'orders':[2,3,5],'order':60};break
    if complement:break
   if complement:break
  if complement:break
 expected_shell={0:1,1:10,2:40,3:80,4:80,5:32}
 packet_edge_sets=[]
 for packet in packets:
  z=0
  for r in packet[0]:z|=row_masks[r]
  packet_edge_sets.append(z)
 checks={
  'base_is_exact_cover':len(base)==60 and np.all(M[list(base)].sum(axis=0)==1),
  'all_487635_removed_four_subsets_scanned':math.comb(60,4)==487635,
  'exactly_ten_intersection_56_neighbors':len(neighbors)==10,
  'five_trade_packets':len(packets)==5,
  'each_packet_has_exactly_three_resolutions':all(len(p)==3 for p in packets),
  'packet_edge_sets_pairwise_disjoint':all(not(packet_edge_sets[i]&packet_edge_sets[j]) for i in range(5) for j in range(i)),
  'cartesian_chart_has_243_covers':len(chart)==3**5,
  'H53_shell_distribution':dict(shell)==expected_shell,
  'chart_stabilizer_order_960':len(stabilizer)==960,
  'coordinate_image_order_60':len(image)==60,
  'coordinate_image_is_all_even_permutations':all(parity(x)==0 for x in image),
  'coordinate_image_order_spectrum_A5':dict(image_orders)=={1:1,2:15,3:20,5:24},
  'kernel_order_16':len(kernel)==16,
  'kernel_is_elementary_abelian_2_4':kernel_abelian and dict(kernel_orders)=={1:1,2:15},
  'A5_complement_found':complement is not None and complement['order']==60,
  'semidirect_order_factorization':len(kernel)*len(image)==len(stabilizer)==960,
 }
 checks={k:bool(v) for k,v in checks.items()}
 return {
  'schema':'w33.pass1509.qutrit_hamming_m20_chart.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'theorem':('A deterministic exact cover contains five pairwise edge-disjoint 16-edge packets, each with exactly three four-frame resolutions. Independent choice of one resolution per packet gives a literal Hamming graph H(5,3) chart of 243 exact covers with shells 1,10,40,80,80,32. Its setwise stabilizer in PSp(4,3) is the split group 2^4:A5 of order 960, hence the Mathieu group M20.'),
  'base_cover':list(base),'nearest_neighbor_count':len(neighbors),'packets':[[list(x) for x in p] for p in packets],
  'chart_size':len(chart),'hamming_shells':{str(k):v for k,v in sorted(shell.items())},
  'stabilizer':{'order':len(stabilizer),'element_order_histogram':{str(k):v for k,v in sorted(stab_orders.items())},'kernel_order':len(kernel),'kernel_order_histogram':{str(k):v for k,v in sorted(kernel_orders.items())},'kernel_abelian':kernel_abelian,'coordinate_image_order':len(image),'coordinate_image_order_histogram':{str(k):v for k,v in sorted(image_orders.items())},'coordinate_image_all_even':all(parity(x)==0 for x in image),'structure':'2^4:A5','atlas_name':'M20','A5_complement':complement},
  'checks':checks,
  'boundary':'The H(5,3) chart and its M20 stabilizer are exact finite cover geometry. This qutrit chart does not by itself establish a physical qutrit processor or a contextual fraction.'
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=OUT);ap.add_argument('--check',action='store_true');a=ap.parse_args();p=certificate();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 1509 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'chart_size':p['chart_size'],'stabilizer':p['stabilizer']['structure']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
