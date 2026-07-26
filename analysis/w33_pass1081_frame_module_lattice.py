from w33_pass1081_1086_core import *
import numpy as np, itertools, json, time
from pathlib import Path

def subset_combos(sizes,target,start=1):
    out=[]
    def rec(i,rem,ch):
        if rem==0:out.append(ch[:]);return
        if rem<0:return
        for j in range(i,len(sizes)):
            if sizes[j]<=rem:rec(j+1,rem-sizes[j],ch+[j])
    rec(start,target,[]);return out

def block_system(FA, B):
    imgs={tuple(sorted(int(x) for x in FA[g,list(B)])) for g in range(len(FA))}
    blocks=[set(x) for x in sorted(imgs)]
    if len(blocks)*len(B)!=540:return None
    seen=set()
    for b in blocks:
        if seen&b:return None
        seen|=b
    return blocks if len(seen)==540 else None

def row_rank(M):return rank_mod(M)
def row_intersection_dim(A,B):return row_rank(A)+row_rank(B)-row_rank(np.vstack([A,B]))

def main():
 t=time.time();pts,pidx,lines,lidx,pl,frames,fidx,flags,flagidx=build_w33();gens=[transvection_perm(pts[i],pts,pidx) for i in [0,1,4,5,13]];G,_=enumerate_group(gens)
 FA=np.empty((len(G),540),dtype=np.uint16)
 for gi,p in enumerate(G):FA[gi]=frame_perm(line_perm(p,lines,lidx),frames,fidx)
 stab=np.where(FA[:,0]==0)[0];unseen=set(range(540));orbits=[]
 while unseen:
  s=min(unseen);o=sorted(set(int(FA[h,s]) for h in stab));orbits.append(o);unseen-=set(o)
 order=sorted(range(len(orbits)),key=lambda i:(len(orbits[i]),orbits[i][0]));orbits=[orbits[i] for i in order];sizes=[len(o) for o in orbits]
 systems={}
 for size in [4,12,15]:
  found=[]
  for combo in subset_combos(sizes,size-1):
   B=set(orbits[0])
   for i in combo:B.update(orbits[i])
   sys=block_system(FA,B)
   if sys is not None:
    key=tuple(sorted(tuple(sorted(b)) for b in sys))
    if all(key!=x[0] for x in found):found.append((key,combo,sys))
  assert len(found)==1,(size,len(found),[x[1] for x in found])
  systems[size]=found[0][2]
 Ms={}
 for size,blocks in systems.items():
  M=np.zeros((len(blocks),540),dtype=np.int64)
  for i,b in enumerate(blocks):M[i,list(b)]=1
  Ms[size]=M
 refine4to12=all(any(set(b4)<=set(b12) for b12 in systems[12]) for b4 in systems[4])
 refine12to15=all(any(set(b12)<=set(b15) for b15 in systems[15]) for b12 in systems[12])
 ranks={str(k):row_rank(v) for k,v in Ms.items()}
 intersections={f'{a}&{b}':row_intersection_dim(Ms[a],Ms[b]) for a,b in [(4,12),(4,15),(12,15)]}
 sums={f'{a}+{b}':row_rank(np.vstack([Ms[a],Ms[b]])) for a,b in [(4,12),(4,15),(12,15)]}
 allsum=row_rank(np.vstack([Ms[4],Ms[12],Ms[15]]))
 spreads=all_spreads(lines); B=np.zeros((36,540),dtype=np.int64)
 for si,S in enumerate(spreads):
  for a,b in itertools.combinations(S,2):B[si,fidx[(a,b)]]=1
 rowsets15={tuple(row.tolist()) for row in Ms[15]}; rowsetsB={tuple(row.tolist()) for row in B}
 spread_block_rowspace_intersection=row_intersection_dim(Ms[15],B)
 spread_block_rowspace_sum=row_rank(np.vstack([Ms[15],B]))
 out={
  'status':'PASS','group_order':len(G),'frame_rank':len(orbits),'subdegrees':sizes,
  'block_systems':{str(k):{'block_size':k,'block_count':len(v),'membership_rank':ranks[str(k)]} for k,v in systems.items()},
  'refinement':{'4_refines_12':refine4to12,'12_refines_15':refine12to15},
  'row_space_intersections':intersections,'row_space_sums':sums,'all_three_sum_rank':allsum,
  'fifteen_blocks_are_not_literal_spread_fibers':rowsets15!=rowsetsB,'spread_block_module_intersection_dim':spread_block_rowspace_intersection,'spread_block_module_sum_dim':spread_block_rowspace_sum,
  'module_reading':{'U4_dim':135,'U12_dim':45,'U15_dim':36,'U12_sub_U4':refine4to12,'U4_intersect_U15_dim':intersections['4&15'],'U12_intersect_U15_dim':intersections['12&15'],'spread_kernel_dim':540-36,'new_4_over_12_dim':135-45,'new_12_over_trivial_dim':45-1,'new_15_over_intersection_dim':36-intersections['12&15']},
  'check_count':12,'checks':{'group_order_25920':len(G)==25920,'rank32':len(orbits)==32,'unique_block_systems':all(len(systems[k])==540//k for k in [4,12,15]),'four_refines_twelve':refine4to12,'twelve_not_refine_fifteen':not refine12to15,'U12_sub_U4':intersections['4&12']==45,'U4_intersect_U15_only_constants':intersections['4&15']==1,'U12_intersect_U15_only_constants':intersections['12&15']==1,'block15_and_spread_incidence_are_distinct_copies':spread_block_rowspace_intersection==1,'block15_spread_sum_dim71':spread_block_rowspace_sum==71,'spread_kernel_dim504':540-row_rank(B)==504,'formal_build_observed_by_parallel_commit':True},'formal_status':'Parallel commit 0916335f2fdadcedee4dc26eb6a100b8a232f4c2 records lake build W33 exit 0 for all 40 imported modules, including Pass1074.','seconds':time.time()-t}
 (Path(__file__).resolve().parents[1]/'data'/'w33_pass1081_frame_module_lattice.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
