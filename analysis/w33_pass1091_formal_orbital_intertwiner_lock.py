from __future__ import annotations
import hashlib,itertools,json,time
from pathlib import Path
import numpy as np
from w33_pass1081_1086_core import *

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1091_formal_orbital_intertwiner_lock.json'
INNER=[0,1,3,2,4,5,7,6,8,9,15,13,12,11,14,10,17,16,18,19,20,22,21,25,26,23,24,28,27,30,29,31]
FUSION=[0,1,3,2,4,5,7,6,8,9,11,10,14,15,12,13,16,17,19,18,20,22,21,23,28,25,27,26,24,30,29,31]
OUTER=[0,1,2,3,4,5,6,7,10,9,8,12,11,13,14,15,18,19,16,17,20,21]

def main():
    t=time.time();np.load(ROOT/'data'/'w33_pass1082_frame_coherent_configuration_tensor.npz');st=np.load(ROOT/'data'/'w33_pass1087_canonical_steinberg_parity.npz');Tplus=st['Tplus'];Tminus=st['Tminus'];K=st['K']
    meta=json.loads((ROOT/'data'/'w33_pass1082_frame_coherent_configuration.json').read_text());pts,pidx,lines,lidx,pl,frames,fidx,flags,flagidx=build_w33();spreads=all_spreads(lines)
    B=np.zeros((36,540),dtype=np.int64)
    for si,S in enumerate(spreads):
        for a,b in itertools.combinations(S,2):B[si,fidx[(a,b)]]=1
    D=np.zeros((80,160),dtype=np.int64)
    for e,(p,l) in enumerate(flags):D[p,e]=-1;D[40+l,e]=1
    gens=[transvection_perm(pts[i],pts,pidx) for i in [0,1,4,5,13]];inner_eq=[]
    for gp in gens:
        lp=line_perm(gp,lines,lidx);fp=np.array(frame_perm(lp,frames,fidx));fl=np.array(flag_perm(gp,lp,flags,flagidx));inner_eq.append(np.array_equal(Tplus[np.ix_(fp,fl)],Tplus) and np.array_equal(Tminus[np.ix_(fp,fl)],Tminus))
    op=outer_similitude_perm(pts,pidx);olp=line_perm(op,lines,lidx);ofp=np.array(frame_perm(olp,frames,fidx));ofl=np.array(flag_perm(op,olp,flags,flagidx));lean=(ROOT/'formal/W33/Pass1091FrameOrbitalIntertwiner.lean').read_text();plus_hash=hashlib.sha256(Tplus.tobytes()).hexdigest();minus_hash=hashlib.sha256(Tminus.tobytes()).hexdigest()
    checks={'inner_map_matches_tensor':INNER==meta['inner_transpose_map'],'fusion_map_matches_tensor':FUSION==meta['fusion_map'],'outer_map_matches_tensor':OUTER==meta['outer_transpose_map'],'inner_transpose_involution':all(INNER[INNER[i]]==i for i in range(32)),'inner_fixed12_nonfixed20':sum(INNER[i]==i for i in range(32))==12 and sum(INNER[i]!=i for i in range(32))==20,'ten_inner_transpose_pairs':sum(INNER[i]!=i for i in range(32))//2==10,'fusion_involution_has22_orbits':all(FUSION[FUSION[i]]==i for i in range(32)) and (32+sum(FUSION[i]==i for i in range(32)))//2==22,'outer_transpose_involution_fixed14':all(OUTER[OUTER[i]]==i for i in range(22)) and sum(OUTER[i]==i for i in range(22))==14,'plus_BT_zero':not np.any(B@Tplus),'minus_BT_zero':not np.any(B@Tminus),'plus_TDt_zero':not np.any(Tplus@D.T),'minus_TDt_zero':not np.any(Tminus@D.T),'plus_TK_160T':np.array_equal(Tplus@K,160*Tplus),'minus_TK_160T':np.array_equal(Tminus@K,160*Tminus),'inner_generator_equivariance':all(inner_eq),'outer_plus_minus_parity':np.array_equal(Tplus[np.ix_(ofp,ofl)],Tplus) and np.array_equal(Tminus[np.ix_(ofp,ofl)],-Tminus),'Lean_contains_exact_tensor_hashes':plus_hash in lean and minus_hash in lean,'Lean_contains_native_decide_locks':all(x in lean for x in ['innerSelfPaired_card','innerTransposePair_card','outerFusionOrbit_card','outerSelfPaired_card']),'Lean_contains_kernel_and_cycle_lemmas':all(x in lean for x in ['column_mem_leftKernel','cycleEigen_entry'])}
    assert all(checks.values()),checks
    out={'schema':'w33.pass1091.formal_orbital_intertwiner_lock.v1','status':'PASS','headline':'The corrected 32-orbital transpose map, the 22-orbit outer fusion, and the 22-orbital transpose map are frozen as explicit finite maps for Lean native_decide. The exact plus/minus Steinberg tensors are hash-locked, and their BT=0, TD^T=0, TK=160T, inner equivariance, and outer parity identities are reverified objectwise.','finite_maps':{'inner_transpose':INNER,'outer_fusion':FUSION,'outer_transpose':OUTER},'counts':{'inner_self_paired':12,'inner_nonself_paired':20,'inner_transpose_pairs':10,'outer_fusion_orbits':22,'outer_self_paired':14},'tensor_hashes':{'Steinberg_plus':plus_hash,'Steinberg_minus':minus_hash},'formal_module':'formal/W33/Pass1091FrameOrbitalIntertwiner.lean','formal_boundary':'The finite-map statements are designed for native_decide. The large integer tensors remain external hash-locked certificates; Lean proves the generic kernel and projector consequences from matrix identities rather than embedding 540x160 literals.','check_count':len(checks),'checks':{k:bool(v) for k,v in checks.items()},'seconds':time.time()-t}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
