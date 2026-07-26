from __future__ import annotations
import itertools, json, time
from collections import Counter
from pathlib import Path
import numpy as np
from w33_pass1060_1064_core import build_w33

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1076_spread_frame_incidence_algebra.json'

def all_spreads(lines,npts=40):
    onpt=[[li for li,L in enumerate(lines) if p in L] for p in range(npts)];sol=[]
    def rec(ch,used):
        if len(used)==npts:sol.append(tuple(sorted(ch)));return
        p=next(x for x in range(npts) if x not in used)
        for li in onpt[p]:
            if set(lines[li])&used:continue
            rec(ch+[li],used|set(lines[li]))
    rec([],set());return sorted(set(sol))

def eig_mult(M):
    vals=np.linalg.eigvalsh(M.astype(float));C=Counter()
    for x in vals:
        y=int(round(float(x))) if abs(x-round(float(x)))<1e-7 else round(float(x),9);C[str(y)]+=1
    return dict(sorted(C.items(),key=lambda kv:float(kv[0])))
def relation_matrices(C):return [(v,(C==v).astype(np.int64)) for v in sorted(set(int(x) for x in C.flat))]
def span_coeff(M,basis):
    X=np.stack([B.reshape(-1) for B in basis],axis=1).astype(float);y=M.reshape(-1).astype(float);coef,_,_,_=np.linalg.lstsq(X,y,rcond=None)
    return [round(float(c),10) for c in coef],float(np.max(np.abs(X@coef-y)))
def main():
    started=time.time();w=build_w33();spreads=all_spreads(w.lines);frames=[(a,b) for a in range(40) for b in range(a+1,40) if not(set(w.lines[a])&set(w.lines[b]))];fidx={f:i for i,f in enumerate(frames)}
    B=np.zeros((36,540),dtype=np.int8)
    for si,S in enumerate(spreads):
        for a,b in itertools.combinations(S,2):B[si,fidx[(a,b)]]=1
    Gs=B@B.T;Gf=B.T@B;As=((Gs>0)&(~np.eye(36,dtype=bool))).astype(np.int8)
    common_off=Counter(int(Gf[i,j]) for i in range(540) for j in range(540) if i!=j);rel=relation_matrices(Gf);relvals=[v for v,_ in rel];relation_valencies={str(v):sorted(set(int(x) for x in R.sum(axis=1))) for v,R in rel};basis=[R for _,R in rel]
    closure=[];closed=True
    for vi,Ri in rel:
        for vj,Rj in rel:
            coef,err=span_coeff(Ri@Rj,basis);closed&=err<=1e-7;closure.append({'left':vi,'right':vj,'coefficients':coef,'max_residual':err})
    sing=np.linalg.svd(B.astype(float),compute_uv=False);sC=Counter(round(float(x*x),9) for x in sing);BB=np.block([[np.zeros((36,36),dtype=np.int8),B],[B.T,np.zeros((540,540),dtype=np.int8)]])
    checks={'objects_are_36_by_540':B.shape==(36,540),'row_degree45':set(map(int,B.sum(axis=1)))=={45},'column_degree3':set(map(int,B.sum(axis=0)))=={3},'incidence_total1620':int(B.sum())==1620,'spread_gram_is_45I_plus_6A':np.array_equal(Gs,45*np.eye(36,dtype=int)+6*As),'spread_graph_spectrum_is_15_3_minus3':eig_mult(As)=={'-3':20,'3':15,'15':1},'incidence_squared_singular_spectrum_is_135_63_27':sC==Counter({27.0:20,63.0:15,135.0:1}),'incidence_rank36':np.linalg.matrix_rank(B.astype(float))==36,'frame_gram_nonzero_spectrum_matches_spread_gram':all(abs(x-y)<1e-7 for x,y in zip(sorted(np.linalg.eigvalsh(Gs.astype(float))),sorted(np.linalg.eigvalsh(Gf.astype(float)))[-36:])),'coarse_common_spread_relations_are_not_closed':not closed}
    checks={k:bool(v) for k,v in checks.items()};assert all(checks.values()),(checks,common_off,relvals,relation_valencies)
    out={'schema':'w33.pass1076.spread_frame.incidence_algebra.v1','status':'PASS','headline':'The 36 x 540 spread-frame incidence has an exact three-singular-value algebra on the spread side, but the coarse frame relations defined only by the number of common spreads are not closed under multiplication. Thus the spread side is rank-3, while the frame side genuinely requires the finer rank-32/22 orbital structure found in Passes 1072 and 1075.','incidence':{'shape':[36,540],'row_degree':45,'column_degree':3,'total':1620},'spread_gram_identity':'B B^T = 45 I + 6 A, where A is the checked PSp(4,3) valency-15 spread orbital.','spread_graph_spectrum':eig_mult(As),'spread_gram_spectrum':eig_mult(Gs),'frame_gram_spectrum':eig_mult(Gf),'bipartite_incidence_spectrum':eig_mult(BB),'squared_singular_values':{str(k):v for k,v in sorted(sC.items())},'frame_pair_common_spread_profile':dict(sorted(common_off.items())),'coarse_relation_values':relvals,'coarse_relation_valencies':relation_valencies,'coarse_relation_algebra_closed':closed,'first_nonclosure_witness':next(x for x in closure if x['max_residual']>1e-7),'interpretation':{'spread_embedding':'The 36 incidence rows span a 36-dimensional module decomposing as 1 + 15 + 20, with squared singular values 135, 63, and 27.','frame_kernel':'The 540-dimensional frame carrier has a 504-dimensional incidence kernel.','association_scheme_boundary':'The common-spread count alone does not define an association scheme on frames; the full group orbitals are essential.'},'check_count':len(checks),'checks':checks,'scope':'Exact finite incidence and linear algebra. This consumes, rather than reclaims, Pass 1071 tactical regularity and Pass 1072 orbital identification.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','common_profile':dict(common_off),'relation_values':relvals,'seconds':round(time.time()-started,3)},indent=2))
if __name__=='__main__':main()
