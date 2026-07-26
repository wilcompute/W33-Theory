from w33_pass1081_1086_core import *
import numpy as np, json, time, hashlib, itertools
from collections import deque
from pathlib import Path

def levi_cycle_kernel(flags):
    n=len(flags);adj=[set() for _ in range(n)]
    for i,(p,l) in enumerate(flags):
        for j,(q,m) in enumerate(flags):
            if i!=j and (p==q or l==m):adj[i].add(j)
    dist=np.full((n,n),99,dtype=np.int8)
    for s in range(n):
        dist[s,s]=0;q=deque([s])
        while q:
            x=q.popleft()
            for y in adj[x]:
                if dist[s,y]==99:dist[s,y]=dist[s,x]+1;q.append(y)
    vals={0:81,1:-27,2:9,3:-3,4:1};return np.vectorize(vals.get,otypes=[np.int64])(dist),dist

def main():
 t=time.time();pts,pidx,lines,lidx,pl,frames,fidx,flags,flagidx=build_w33();spreads=all_spreads(lines);gens=[transvection_perm(pts[i],pts,pidx) for i in [0,1,4,5,13]];G,gindex=enumerate_group(gens)
 FA=np.empty((len(G),540),dtype=np.uint16);LA=np.empty((len(G),160),dtype=np.uint16)
 for gi,p in enumerate(G):
  lp=line_perm(p,lines,lidx);FA[gi]=frame_perm(lp,frames,fidx);LA[gi]=flag_perm(p,lp,flags,flagidx)
 base=0;stab=np.where(LA[:,base]==base)[0];assert len(stab)==162
 unseen=set(range(540));orbits=[]
 while unseen:
  s=min(unseen);o=sorted(set(int(FA[h,s]) for h in stab));orbits.append(o);unseen-=set(o)
 order=sorted(range(len(orbits)),key=lambda i:(len(orbits[i]),orbits[i][0]));orbits=[orbits[i] for i in order];lab=np.empty(540,dtype=np.int16)
 for i,o in enumerate(orbits):lab[o]=i
 trans=[None]*160
 for gi in range(len(G)):
  x=int(LA[gi,base])
  if trans[x] is None:trans[x]=gi
 inv=[gindex[inverse(G[g])] for g in trans];C=np.empty((160,540),dtype=np.uint8)
 for x in range(160):C[x]=lab[FA[inv[x]]]
 for gp in gens:
  lp=line_perm(gp,lines,lidx);fp=frame_perm(lp,frames,fidx);flp=flag_perm(gp,lp,flags,flagidx);assert np.array_equal(C[np.array(flp)],C[:,np.array(inverse(fp))])
 D=np.zeros((80,160),dtype=np.int64)
 for e,(p,l) in enumerate(flags):D[p,e]=-1;D[40+l,e]=1
 K,dist=levi_cycle_kernel(flags);assert np.array_equal(K@K,160*K);assert not np.any(D@K);assert np.linalg.matrix_rank(K.astype(float))==81
 B=np.zeros((36,540),dtype=np.int64)
 for si,S in enumerate(spreads):
  for a,b in itertools.combinations(S,2):B[si,fidx[(a,b)]]=1
 Gs=B@B.T;A=((Gs>0)&(~np.eye(36,dtype=bool))).astype(np.int64);R=639*np.eye(36,dtype=np.int64)-90*A+4*(A@A);assert np.array_equal(R@Gs,25515*np.eye(36,dtype=np.int64))
 ranks=[];records=[];selected=None;Ts=[]
 for r,o in enumerate(orbits):
  M=(C==r).T.astype(np.int64);Y=M@K;T=25515*Y-B.T@(R@(B@Y));rk=rank_mod(T);left_zero=not np.any(B@T);right_zero=not np.any(T@D.T);eig_right=np.array_equal(T@K,160*T);Ts.append(T)
  rec={'relation':r,'cross_valency':len(o),'rank_mod_1000003':rk,'spread_kernel':left_zero,'kills_levi_cut':right_zero,'right_cycle_eigen':eig_right,'sha256_int64':hashlib.sha256(T.tobytes()).hexdigest(),'nnz':int(np.count_nonzero(T)),'max_abs':int(np.max(np.abs(T)))};records.append(rec);ranks.append(rk)
  if selected is None and rk==81 and left_zero and right_zero and eig_right:selected=(r,T,rec)
 sample=np.stack([T.reshape(-1) for T in Ts],axis=0);map_span_rank=rank_mod(sample);nonzero_idx=[i for i,T in enumerate(Ts) if np.any(T)];pair_image_ranks={}
 for aa in range(len(nonzero_idx)):
  for bb in range(aa+1,len(nonzero_idx)):
   i,j=nonzero_idx[aa],nonzero_idx[bb];pair_image_ranks[f'{i},{j}']=rank_mod(np.concatenate([Ts[i],Ts[j]],axis=1))
 scalar_relations=[];baseT=next(T for T in Ts if np.any(T));pivot=int(np.flatnonzero(baseT)[0]);q=1000003;bp=int(baseT.flat[pivot])%q
 for i,T in enumerate(Ts):
  if not np.any(T):scalar_relations.append({'relation':i,'scalar_mod_1000003':0});continue
  a=int(T.flat[pivot])%q*pow(bp,-1,q)%q;scalar_relations.append({'relation':i,'scalar_mod_1000003':a,'verified':bool(np.all((T-a*baseT)%q==0))})
 assert selected is not None;r,T,rec=selected
 for gp in gens:
  lp=line_perm(gp,lines,lidx);fp=np.array(frame_perm(lp,frames,fidx));flp=np.array(flag_perm(gp,lp,flags,flagidx));assert np.array_equal(T[np.ix_(fp,flp)],T)
 tensor_path=Path(__file__).resolve().parents[1]/'data'/'w33_pass1083_levi_frame_intertwiner.npz';np.savez_compressed(tensor_path,T=T,K=K)
 out={'status':'PASS','group_order':len(G),'flag_stabilizer_order':len(stab),'cross_orbit_count':len(orbits),'cross_orbit_sizes':[len(o) for o in orbits],'relation_records':records,'map_span_rank_mod_1000003':map_span_rank,'scalar_relations':scalar_relations,'pair_image_ranks':pair_image_ranks,'selected_relation':r,'selected_rank':81,'selected_sha256_int64':rec['sha256_int64'],'selected_nnz':rec['nnz'],'selected_max_abs':rec['max_abs'],'identities':['B*T=0','T*D^T=0','T*K_Levi=160*T','G-equivariant for all five transvection generators'],'interpretation':'An explicit integer G-intertwiner carries the 81-dimensional Levi cycle/Steinberg module into the 504-dimensional spread-incidence kernel. This is a map-level identification, not a dimension coincidence.','seconds':time.time()-t}
 out['tensor_sha256']=hashlib.sha256(tensor_path.read_bytes()).hexdigest();out['check_count']=14;out['checks']={'group_order25920':len(G)==25920,'flag_stabilizer162':len(stab)==162,'ten_cross_orbits':len(orbits)==10,'cross_sizes_27x5_81x5':[len(o) for o in orbits]==[27]*5+[81]*5,'cycle_kernel_rank81':np.linalg.matrix_rank(K.astype(float))==81,'cycle_projector_identity':np.array_equal(K@K,160*K),'selected_rank81':rec['rank_mod_1000003']==81,'selected_in_spread_kernel':rec['spread_kernel'],'selected_kills_cut':rec['kills_levi_cut'],'selected_right_cycle_eigen':rec['right_cycle_eigen'],'intertwiner_space_rank2':map_span_rank==2,'some_pairs_same_image':any(v==81 for v in pair_image_ranks.values()),'generic_pairs_direct_sum162':any(v==162 for v in pair_image_ranks.values()),'all_generator_equivariance_checks_passed':True};out['checks']={k:bool(v) for k,v in out['checks'].items()};(Path(__file__).resolve().parents[1]/'data'/'w33_pass1083_levi_frame_steinberg_intertwiner.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
