#!/usr/bin/env python3
from __future__ import annotations
import itertools, json
from collections import Counter, defaultdict
from pathlib import Path
from fractions import Fraction
import numpy as np, sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from analysis.w33_pass7509_7516_steinberg_global_intertwiner import build_T
from analysis import w33_pass7501_7564_common as E
OUT=ROOT/'data/PART_W33_PASS7621_7628_FUSIONFRAME_V20_TRANSPORT.json'

def span_rank(R,ids): return np.linalg.matrix_rank(np.asarray([R[i] for i in ids],float))
def center_quads(W):
    nbr=[set(np.flatnonzero(W[i])) for i in range(40)];Q=set()
    for a,b,c in itertools.combinations(range(40),3):
        if W[a,b] or W[a,c] or W[b,c]: continue
        x=frozenset(nbr[a]&nbr[b]&nbr[c])
        if len(x)==4:Q.add(x)
    assert len(Q)==90
    return sorted(Q,key=lambda x:tuple(sorted(x))),nbr

def build_geometry():
    R,A2,J,base,bl,AO,lab,edges,L,P,T,maps=build_T();W=AO[np.ix_(bl,bl)];bp={a:i for i,a in enumerate(bl)}
    D=defaultdict(list)
    for j in np.flatnonzero(np.any(T!=0,axis=0)):D[tuple(int(x) for x in T[:,j])].append(int(j))
    V=np.asarray(list(D),dtype=np.int64).T;fibres=list(D.values());G=V.T@V
    comp=[]
    for F in fibres:
        cand=[]
        for a in bl:
            roots=set(A2[a])
            for f in F: roots.update(A2[f])
            if len(roots)!=24 or span_rank(R,roots)!=4:continue
            B=np.asarray([R[i] for i in roots],float);rr=np.linalg.matrix_rank(B)
            if sum(np.linalg.matrix_rank(np.vstack([B,np.asarray(r,float)]))==rr for r in R)==24:cand.append(a)
        assert len(cand)==1;comp.append(cand[0])
    A=(G==-3840);np.fill_diagonal(A,False);seen=set();tets=[]
    for i in range(360):
        if i in seen:continue
        S={i};q=[i];seen.add(i)
        while q:
            u=q.pop()
            for v in np.flatnonzero(A[u]):
                v=int(v)
                if v not in S:S.add(v);seen.add(v);q.append(v)
        assert len(S)==4;tets.append(tuple(sorted(S)))
    supports=[frozenset(bp[comp[i]] for i in Q) for Q in tets]
    quads,nbr=center_quads(W);assert set(supports)==set(quads);qid={Q:i for i,Q in enumerate(quads)};tb={S:i for i,S in enumerate(supports)}
    pairing={}
    for i,Q in enumerate(quads):
        c=set(range(40))
        for v in Q:c&=nbr[v]
        pairing[i]=qid[frozenset(c)]
    qp=[];seen=set()
    for i in range(90):
        p=tuple(sorted((i,pairing[i])))
        if p not in seen:seen.add(p);qp.append(p)
    assert len(qp)==45
    qsup=[quads[a]|quads[b] for a,b in qp]
    qlines=[]
    for ids in itertools.combinations(range(45),5):
        U=set();ok=True
        for q in ids:
            if U&qsup[q]:ok=False;break
            U|=qsup[q]
        if ok and len(U)==40:qlines.append(ids)
    assert len(qlines)==27
    Qnum=[]
    for a,b in qp:
        inds=list(tets[tb[quads[a]]])+list(tets[tb[quads[b]]])
        M=V[:,inds];Qnum.append(M@M.T)
    assert all(np.array_equal(Q@P,P@Q) for Q in Qnum)
    return R,A2,base,bl,AO,W,P,V,tets,quads,qp,qlines,Qnum

def main():
    R,A2,base,bl,AO,W,P,V,tets,quads,qp,qlines,Qnum=build_geometry()
    assert np.array_equal(sum(Qnum),80*P)
    B=np.zeros((45,27),dtype=np.int64)
    for j,L in enumerate(qlines):B[list(L),j]=1
    Apoint=B@B.T-3*np.eye(45,dtype=np.int64);assert set(map(int,Apoint.sum(1)))=={12}
    den=15360**2;trnum=np.zeros((45,45),dtype=object)
    for i in range(45):
        for j in range(45):trnum[i,j]=int(np.sum(Qnum[i]*Qnum[j]))
    vals=Counter(Fraction(int(trnum[i,j]),den) for i in range(45) for j in range(i+1,45))
    assert vals==Counter({Fraction(5,16):720,Fraction(1,3):270}) and all(Fraction(int(trnum[i,i]),den)==6 for i in range(45))
    K=[[Fraction(int(trnum[i,j]),den)-Fraction(4,9) for j in range(45)] for i in range(45)]
    for i in range(45):
        for j in range(45):
            rhs=Fraction(91,16)*(i==j)+Fraction(1,48)*int(Apoint[i,j])-Fraction(19,144);assert K[i][j]==rhs
    Qb=[]
    for Q in Qnum:
        ev,U=np.linalg.eigh(Q.astype(float));idx=np.where(ev>1e-6)[0];assert len(idx)==6;Qb.append(U[:,idx])
    pats={'adj':Counter(),'non':Counter()}
    for i,j in itertools.combinations(range(45),2):
        ss=tuple(round(float(x),8) for x in sorted(np.linalg.svd(Qb[i].T@Qb[j],compute_uv=False),reverse=True));pats['adj' if Apoint[i,j] else 'non'][ss]+=1
    assert pats['adj']=={(0.33333333,0.33333333,0.33333333,0.0,0.0,0.0):270}
    assert pats['non']=={(0.25,0.25,0.25,0.25,0.25,0.0):720}
    rR=int(np.linalg.matrix_rank(B.astype(float)));r2=E.rank_mod(B,2);assert (rR,r2)==(21,21)
    Beven=(B[:,1:]+B[:,[0]])%2;assert E.rank_mod(Beven,2)==20
    Y=B.astype(float)-np.ones((45,27))/9;GY=Y.T@Y;Al=B.T@B-5*np.eye(27,dtype=np.int64)
    assert Counter(round(float(x),8) for x in np.linalg.eigvalsh(Al.astype(float)))=={-5.0:6,1.0:20,10.0:1}
    Kf=np.array([[float(x) for x in row] for row in K]);LK=B.T@Kf@B
    assert np.allclose(LK,(23/4)*GY,atol=1e-8) and Counter(round(float(x),8) for x in np.linalg.eigvalsh(LK))=={0.0:7,34.5:20}
    out={'schema':'w33.pass7621_7628.fusionframe_v20_transport.v1','status':'PASS','passes':'7621-7628','fusion_frame':{'subspaces':45,'ambient_dimension':81,'subspace_dimension':6,'tight_bound':'10/3','exact_tight_identity':'sum_i Q_i = 80 P_HodgeNumerator, where projector_i=Q_i/15360 and H1_projector=P_HodgeNumerator/640','classification':'chordally biangular tight fusion frame (two chordal distances), with two principal-angle patterns rather than equi-isoclinic','principal_cosines_adjacent':['1/3','1/3','1/3','0','0','0'],'principal_cosines_nonadjacent':['1/4','1/4','1/4','1/4','1/4','0'],'index_graph':'the canonical dual-GQ(4,2) point graph SRG(45,12,3,3)'},'centered_projector_gram_formula':'K = (91/16) I + (1/48) A_45 - (19/144) J','centered_projector_spectrum':{'23/4':20,'45/8':24,'0':1},'line_incidence':{'matrix':'B in Z^{45x27}','real_rank':rR,'F2_rank':r2,'even_binary_image_rank':20,'line_graph_spectrum':'10^1 + 1^20 + (-5)^6','centered_real_incidence_gram':'Y^T Y = 6 E20','centered_line_operator_gram':'L^T L = (69/2) E20 = (23/4) Y^T Y'},'V20_bridge':'The 27 columns are exactly the intrinsic 27 ten-D4/dual-GQ lines used in Pass7184. Over F2 their span is [45,21,5]=<1>+V20 and the even subcode is the canonical tritangent V20. Over R the centered columns and centered Steinberg line operators are the same 20D W(E6) coefficient module, with Gram forms differing by 23/4.','literature_boundary':'The standard descriptive term is a chordally biangular tight fusion frame. No external source located an independently named/classified 45xGr(6,81) object with these exact principal-angle patterns; the exact E6/W33 realization is established here rather than inferred from nomenclature.','claim_boundary':'Exact fusion-frame/operator/module theorem. Pass7184 remains the prior source for the binary V20 identification.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','tight':'10/3','classification':'chordally biangular TFF','V20_real_binary_bridge':True}))
if __name__=='__main__':main()
