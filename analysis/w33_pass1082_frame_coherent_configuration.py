from w33_pass1081_1086_core import *
import numpy as np, json, time, itertools, hashlib
from pathlib import Path

def main():
 t=time.time(); pts,pidx,lines,lidx,pl,frames,fidx,flags,flagidx=build_w33()
 gensp=[transvection_perm(pts[i],pts,pidx) for i in [0,1,4,5,13]]
 G,_=enumerate_group(gensp)
 FA=np.empty((len(G),540),dtype=np.uint16)
 for gi,p in enumerate(G):
  lp=line_perm(p,lines,lidx); FA[gi]=frame_perm(lp,frames,fidx)
 base=0; stab=np.where(FA[:,base]==base)[0]; assert len(stab)==48
 unseen=set(range(540)); orbits=[]; label=np.empty(540,dtype=np.int16)
 while unseen:
  s=min(unseen); orb=set(int(FA[h,s]) for h in stab); orbits.append(sorted(orb)); unseen-=orb
 order=sorted(range(len(orbits)),key=lambda i:(len(orbits[i]),orbits[i][0]));orbits=[orbits[i] for i in order]
 for i,o in enumerate(orbits):
  for x in o:label[x]=i
 gindex={g:i for i,g in enumerate(G)}; trans=[None]*540
 for gi in range(len(G)):
  x=int(FA[gi,base])
  if trans[x] is None:trans[x]=gi
 inv_idx=[gindex[inverse(G[gi])] for gi in trans]
 C=np.empty((540,540),dtype=np.uint8)
 for x in range(540):C[x]=label[FA[inv_idx[x]]]
 transpose_map=[int(C[orbits[i][0],base]) for i in range(32)]
 vals=[int(np.sum(C[0]==i)) for i in range(32)]
 assert all(np.array_equal((C==i).T,(C==transpose_map[i])) for i in range(32))
 bitrows=[[0]*540 for _ in range(32)]
 for x in range(540):
  buckets=[0]*32
  for y in range(540):buckets[int(C[x,y])]|=1<<y
  for i in range(32):bitrows[i][x]=buckets[i]
 P=np.zeros((32,32,32),dtype=np.int16); representatives=[o[0] for o in orbits]
 for k,y in enumerate(representatives):
  for i in range(32):
   a=bitrows[i][base]
   for j in range(32):P[i,j,k]=(a & bitrows[transpose_map[j]][y]).bit_count()
 for k,o in enumerate(orbits):
  for y in o:
   for i in range(32):
    a=bitrows[i][base]
    for j in range(32):assert (a & bitrows[transpose_map[j]][y]).bit_count()==int(P[i,j,k])
 op=outer_similitude_perm(pts,pidx);olp=line_perm(op,lines,lidx);ofp=frame_perm(olp,frames,fidx);sb=int(ofp[base]);ugi=next(gi for gi in range(len(G)) if int(FA[gi,sb])==base);tperm=tuple(int(FA[ugi,int(ofp[y])]) for y in range(540));assert tperm[base]==base
 fusion_map=[int(label[tperm[o[0]]]) for o in orbits];fusion_orbits=[];seen=set()
 for i in range(32):
  if i not in seen:
   z=sorted({i,fusion_map[i]});fusion_orbits.append(z);seen.update(z)
 assert len(fusion_orbits)==22
 fmap={i:k for k,o in enumerate(fusion_orbits) for i in o};FC=np.vectorize(fmap.get,otypes=[np.uint8])(C);outer_transpose_map=[int(FC[next(y for y in range(540) if FC[0,y]==k),0]) for k in range(22)];fvals=[int(np.sum(FC[0]==i)) for i in range(22)]
 fbit=[[0]*540 for _ in range(22)]
 for x in range(540):
  buckets=[0]*22
  for y in range(540):buckets[int(FC[x,y])]|=1<<y
  for i in range(22):fbit[i][x]=buckets[i]
 FP=np.zeros((22,22,22),dtype=np.int16);freps=[next(y for y in range(540) if FC[0,y]==k) for k in range(22)]
 for k,y in enumerate(freps):
  for i in range(22):
   a=fbit[i][0]
   for j in range(22):FP[i,j,k]=(a & fbit[outer_transpose_map[j]][y]).bit_count()
 for k in range(22):
  for y in np.where(FC[0]==k)[0]:
   for i in range(22):
    a=fbit[i][0]
    for j in range(22):assert (a&fbit[outer_transpose_map[j]][int(y)]).bit_count()==int(FP[i,j,k])
 spreads=all_spreads(lines);fsp=[set() for _ in range(540)]
 for si,S in enumerate(spreads):
  for a,b in itertools.combinations(S,2):fsp[fidx[(a,b)]].add(si)
 graphrels=[]
 for i,o in enumerate(orbits):
  if i and fsp[0]&fsp[o[0]]:graphrels.append(i)
 assert sum(vals[i] for i in graphrels)==117
 tensor_path=Path(__file__).resolve().parents[1]/'data'/'w33_pass1082_frame_coherent_configuration_tensor.npz';np.savez_compressed(tensor_path,color=C,intersection=P,fused_color=FC,fused_intersection=FP)
 out={'status':'PASS','group_order':len(G),'frame_stabilizer':len(stab),'inner_rank':32,'outer_rank':22,'inner_valencies':vals,'outer_valencies':fvals,'fusion_map':fusion_map,'fusion_orbits':fusion_orbits,'frame_graph_inner_relations':graphrels,'frame_graph_relation_valencies':[vals[i] for i in graphrels],'inner_transpose_map':transpose_map,'inner_self_paired_count':sum(i==transpose_map[i] for i in range(32)),'inner_nonself_paired_count':sum(i!=transpose_map[i] for i in range(32)),'outer_fusion_equals_transpose_closure':fusion_map==transpose_map,'outer_transpose_map':outer_transpose_map,'outer_self_paired_count':sum(i==outer_transpose_map[i] for i in range(22)),'outer_nonself_paired_count':sum(i!=outer_transpose_map[i] for i in range(22)),'inner_intersection_tensor_shape':list(P.shape),'outer_intersection_tensor_shape':list(FP.shape),'inner_intersection_nonzero':int(np.count_nonzero(P)),'outer_intersection_nonzero':int(np.count_nonzero(FP)),'seconds':time.time()-t}
 out['tensor_sha256']=hashlib.sha256(tensor_path.read_bytes()).hexdigest();out['check_count']=14;out['checks']={'group_order_25920':len(G)==25920,'frame_stabilizer48':len(stab)==48,'inner_rank32':len(orbits)==32,'transpose_involution':all(transpose_map[transpose_map[i]]==i for i in range(32)),'only12_inner_self_paired':sum(i==transpose_map[i] for i in range(32))==12,'twenty_nonself_orbitals':sum(i!=transpose_map[i] for i in range(32))==20,'ten_transpose_pairs':sum(i!=transpose_map[i] for i in range(32))//2==10,'outer_rank22':len(fusion_orbits)==22,'outer_fusion_differs_from_transpose':fusion_map!=transpose_map,'outer_has14_self_paired':sum(i==outer_transpose_map[i] for i in range(22))==14,'inner_intersection_tensor_complete':P.shape==(32,32,32),'outer_intersection_tensor_complete':FP.shape==(22,22,22),'frame_graph_degree117':sum(vals[i] for i in graphrels)==117,'all_intersection_numbers_nonnegative':bool(np.all(P>=0) and np.all(FP>=0))}
 (Path(__file__).resolve().parents[1]/'data'/'w33_pass1082_frame_coherent_configuration.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
