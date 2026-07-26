from __future__ import annotations
import hashlib,json,time
from pathlib import Path
import numpy as np
from w33_pass1081_1086_core import *

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1087_canonical_steinberg_parity.json'
P=1000003

def coeff_solver(basis):
    B=np.stack([x.reshape(-1)%P for x in basis],axis=0)
    piv=None
    for a in range(B.shape[1]):
        for b in range(a+1,B.shape[1]):
            M=B[:,[a,b]].T%P
            det=(int(M[0,0])*int(M[1,1])-int(M[0,1])*int(M[1,0]))%P
            if det:piv=(a,b);break
        if piv:break
    assert piv is not None
    def solve(v):
        v=v.reshape(-1)%P;M=B[:,list(piv)].T%P;y=v[list(piv)]
        det=(int(M[0,0])*int(M[1,1])-int(M[0,1])*int(M[1,0]))%P;di=pow(det,-1,P)
        c0=(int(y[0])*int(M[1,1])-int(M[0,1])*int(y[1]))*di%P
        c1=(int(M[0,0])*int(y[1])-int(y[0])*int(M[1,0]))*di%P
        assert np.all((c0*B[0]+c1*B[1]-v)%P==0)
        return [c0,c1]
    return solve

def main():
    t=time.time();z=np.load(ROOT/'data'/'w33_pass1083_levi_frame_intertwiner.npz');Ts=z['allT'];K=z['K']
    pts,pidx,lines,lidx,pl,frames,fidx,flags,flagidx=build_w33();gens=[transvection_perm(pts[i],pts,pidx) for i in [0,1,4,5,13]]
    op=outer_similitude_perm(pts,pidx);olp=line_perm(op,lines,lidx);ofp=np.array(frame_perm(olp,frames,fidx));oflag=np.array(flag_perm(op,olp,flags,flagidx))
    basis_idx=[];basis=[]
    for i,T in enumerate(Ts):
        if np.any(T) and rank_mod(np.stack([x.reshape(-1) for x in basis+[T]]))>len(basis):basis_idx.append(i);basis.append(T)
    assert basis_idx==[1,2]
    solve=coeff_solver(basis)
    action=np.array([solve(T[np.ix_(ofp,oflag)]) for T in basis],dtype=np.int64).T%P
    expected=np.array([[1,P-1],[0,P-1]],dtype=np.int64)
    assert np.array_equal(action,expected)
    Tplus=basis[0];Tminus=basis[0]+2*basis[1]
    plus_outer=np.array_equal(Tplus[np.ix_(ofp,oflag)],Tplus);minus_outer=np.array_equal(Tminus[np.ix_(ofp,oflag)],-Tminus)
    inner_checks=[]
    for gp in gens:
        lp=line_perm(gp,lines,lidx);fp=np.array(frame_perm(lp,frames,fidx));fl=np.array(flag_perm(gp,lp,flags,flagidx))
        inner_checks.append(np.array_equal(Tplus[np.ix_(fp,fl)],Tplus) and np.array_equal(Tminus[np.ix_(fp,fl)],Tminus))
    rplus=rank_mod(Tplus);rminus=rank_mod(Tminus);rsum=rank_mod(np.concatenate([Tplus,Tminus],axis=1));Gp=Tplus.T@Tplus;Gm=Tminus.T@Tminus
    def gram_scalar(G):
        a,b=next((int(G[i,j]),int(K[i,j])) for i,j in zip(*np.nonzero(K)) if K[i,j] and G[i,j]);assert a%b==0 and np.array_equal(G,(a//b)*K);return a//b
    gp=gram_scalar(Gp);gm=gram_scalar(Gm);source_outer_trace=sum(int(K[j,oflag[j]]) for j in range(160))//160
    np.savez_compressed(ROOT/'data'/'w33_pass1087_canonical_steinberg_parity.npz',Tplus=Tplus,Tminus=Tminus,K=K)
    checks={'hom_space_basis_relations_1_2':basis_idx==[1,2],'outer_action_matrix_exact':np.array_equal(action,expected),'outer_action_is_involution':np.array_equal(action@action%P,np.eye(2,dtype=np.int64)),'plus_map_outer_even':plus_outer,'minus_map_outer_odd':minus_outer,'both_inner_equivariant':all(inner_checks),'plus_rank81':rplus==81,'minus_rank81':rminus==81,'images_direct_sum_rank162':rsum==162,'plus_gram_is_scalar_Levi_projector':gp>0,'minus_gram_is_scalar_Levi_projector':gm>0,'source_outer_trace_is_3':source_outer_trace==3}
    assert all(checks.values()),checks
    out={'schema':'w33.pass1087.canonical_steinberg_parity.v1','status':'PASS','headline':'The two 81-dimensional frame-kernel copies are canonically resolved by the outer similitude. On the two-dimensional inner intertwiner space the outer action is [[1,-1],[0,-1]] in the relation-(1,2) basis. Its + and - eigenmaps have direct-sum images and extend the same inner Steinberg module to two inequivalent projective-similitude modules differing by the multiplier sign character.','basis_relations':basis_idx,'outer_action_matrix_mod_1000003':action.tolist(),'canonical_maps':{'Steinberg_plus':{'formula':'T1','rank':rplus,'outer_parity':1,'outer_trace':source_outer_trace,'sha256_int64':hashlib.sha256(Tplus.tobytes()).hexdigest(),'gram_scalar_over_K':gp},'Steinberg_minus':{'formula':'T1 + 2*T2','rank':rminus,'outer_parity':-1,'outer_trace':-source_outer_trace,'sha256_int64':hashlib.sha256(Tminus.tobytes()).hexdigest(),'gram_scalar_over_K':gm}},'combined_image_rank':rsum,'representation_reading':'Both images are stable under the full projective similitude action. They restrict to the same 81-dimensional PSp(4,3) Steinberg module, but the outer multiplier-two element has traces +3 and -3 respectively; equivalently St_minus = St_plus tensor epsilon on the outer C2 quotient.','negative_findings':['the outer similitude does not swap the two images','no signed-E8-sheet or chirality identification is asserted without an additional equivariant map'],'check_count':len(checks),'checks':{k:bool(v) for k,v in checks.items()},'seconds':time.time()-t}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
