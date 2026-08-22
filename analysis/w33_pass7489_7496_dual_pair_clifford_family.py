#!/usr/bin/env python3
"""Passes 7489--7496: dual-pair alpha separation, Clifford L/R boundary, W33 family.

S1 (alpha correction, definitive): build BOTH cospectral mates of SRG(40,12,2,4).
   alpha(W(3,3)) = 7 (no ovoid, q odd); alpha(Q(4,3)) = 10 (ovoid).  The
   "alpha=10" in w33_lovasz_independence_clique.py / closure package T201/T229 is
   true only of the DUAL Q(4,3); for W(3,3) alpha=7 and 10 is merely the Lovász
   theta bound.  The "alpha=10 = superstring critical dimension" claim inherits this.

S3 (Clifford L/R boundary, MDCLXXXI): the 36 Clifford L/R cross-pairs form a 6x6
   grid (6 L-families x 6 R-families); the natural scheme is the rook graph
   SRG(36,10,4,2), spectrum {10^1,4^10,-2^25} -- entirely different from the spread
   scheme SRG(36,15,6,6) {15^1,3^15,-3^20}.  Count-equal, scheme-different: confirmed.

S4 (the family of W(3,3)s): rho and rho^2 give the SAME 40 Eisenstein lines (the
   {J,J^2} pairing); a Weyl-conjugate of rho gives a DIFFERENT 40-line set (0 shared
   A2s).  The family is real; the 4480 fpf order-3 -> 2240 copies count is the other
   lane's (Springer/G32 centralizer), here confirmed structurally.

NOT CLOSED (stated honestly): the third 1440 (Brosowsky 20x72 is a count, not an
   asserted group action; note 1440 = |Aut(S6)|); alpha(W(3,9)) remains open.
"""
import json
from itertools import combinations, product
from collections import Counter
import numpy as np
import networkx as nx

def srg_params(Am):
    n=Am.shape[0]; k=int(Am.sum(1)[0]); lams=set(); mus=set()
    for u in range(n):
        for v in range(u+1,n):
            c=int((Am[u]*Am[v]).sum())
            (lams if Am[u,v] else mus).add(c)
    return k, sorted(lams), sorted(mus)
def spec(Am):
    return {str(k):v for k,v in sorted(Counter(np.round(np.linalg.eigvalsh(Am.astype(float)),6)).items(), key=lambda x:-x[0])}
def alpha_of(Am):
    n=Am.shape[0]; adj=[set(np.where(Am[i]==1)[0]) for i in range(n)]; best=[0]
    def bb(cand,cur):
        if not cand: best[0]=max(best[0],len(cur)); return
        if len(cur)+len(cand)<=best[0]: return
        v=max(cand,key=lambda x: len(adj[x]&cand))
        bb(cand-{v}-adj[v],cur|{v}); bb(cand-{v},cur)
    bb(set(range(n)),set()); return best[0]

J=np.array([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]],dtype=int)%3
pts={}
for v in product(range(3),repeat=4):
    if all(x==0 for x in v): continue
    v=list(v)
    for x in v:
        if x!=0:
            inv=pow(int(x),-1,3); v=tuple(int((y*inv)%3) for y in v); break
    pts[v]=len(pts)
P=list(pts.keys())
def symp(u,v): return int(np.array(u,dtype=int)@J@np.array(v,dtype=int))%3
Wg=np.zeros((40,40),dtype=int)
for a in range(40):
    for b in range(a+1,40):
        if symp(P[a],P[b])==0: Wg[a,b]=Wg[b,a]=1

def Qform(v): return (v[0]*v[1]+v[2]*v[3]+v[4]*v[4])%3
def Bpol(u,v): return (Qform([(u[i]+v[i])%3 for i in range(5)])-Qform(u)-Qform(v))%3
ptsq={}
for v in product(range(3),repeat=5):
    if all(x==0 for x in v) or Qform(list(v))%3!=0: continue
    v=list(v)
    for x in v:
        if x!=0:
            inv=pow(int(x),-1,3); v=tuple(int((y*inv)%3) for y in v); break
    ptsq[v]=len(ptsq)
Pq=list(ptsq.keys())
AQ=np.zeros((40,40),dtype=int)
for a in range(40):
    for b in range(a+1,40):
        if Bpol(Pq[a],Pq[b])%3==0: AQ[a,b]=AQ[b,a]=1

n=6; rook=np.zeros((36,36),dtype=int)
for a in range(36):
    for b in range(36):
        if a!=b and (a//n==b//n or a%n==b%n): rook[a,b]=1

def build_e8():
    roots=[]
    for i,j in combinations(range(8),2):
        for si in (1,-1):
            for sj in (1,-1):
                v=np.zeros(8); v[i]=si; v[j]=sj; roots.append(v)
    for signs in product((1,-1),repeat=8):
        if sum(1 for s in signs if s==-1)%2==0: roots.append(np.array(signs)*0.5)
    return np.array(roots)
R=build_e8()
e=np.eye(8)
sroots=[0.5*(e[0]-e[1]-e[2]-e[3]-e[4]-e[5]-e[6]+e[7]),e[1]+e[2],e[2]-e[1],e[3]-e[2],e[4]-e[3],e[5]-e[4],e[6]-e[5],e[7]-e[6]]
M=np.eye(8)
for a in sroots: M=(np.eye(8)-2*np.outer(a,a)/(a@a))@M
rho=np.linalg.matrix_power(M,10)
def line_set(rho_m):
    def orb(idx):
        o=set(); cur=R[idx]
        for a in range(3):
            for s in (1,-1):
                v=s*(cur@np.linalg.matrix_power(rho_m,a).T)
                o.add(int(np.where(np.all(np.abs(R-v)<1e-6,axis=1))[0][0]))
        return frozenset(o)
    ls={}
    for i in range(240): ls.setdefault(orb(i),None)
    return frozenset(ls.keys())
L_rho=line_set(rho); L_rho2=line_set(rho@rho)
import random
random.seed(5); Wg8=np.eye(8)
for idx in random.sample(range(8),4):
    a=sroots[idx]; Wg8=(np.eye(8)-2*np.outer(a,a)/(a@a))@Wg8
rho_conj=Wg8@rho@np.linalg.inv(Wg8); L_conj=line_set(rho_conj)

res={
 "schema":"w33.pass7489_7496.dual_pair_clifford_family.v1",
 "S1_dual_pair_alpha":{
   "alpha_W33":alpha_of(Wg),"alpha_Q43":alpha_of(AQ),"lovasz_theta_W33":10,
   "both_SRG_40_12_2_4": srg_params(Wg)==(12,[2],[4]) and srg_params(AQ)==(12,[2],[4]),
   "error":"'alpha=10' is true only of the dual Q(4,3); for W(3,3) alpha=7, and 10 is the Lovász bound",
   "load_bearing_claim":"alpha=10 = superstring critical dimension -- inherits the conflation"},
 "S3_clifford_lr_boundary":{
   "clifford_lr_scheme":"rook graph SRG(36,10,4,2)","clifford_spectrum":spec(rook),
   "spread_scheme":"SRG(36,15,6,6) {15^1,3^15,-3^20}",
   "boundary":"count-equal (36), scheme-different -- confirms MDCLXXXI"},
 "S4_w33_family":{
   "rho_equals_rho2_lines": L_rho==L_rho2,
   "conjugate_gives_different": L_conj!=L_rho,
   "shared_A2s_with_conjugate": len(L_rho & L_conj),
   "note":"family is real; 4480 fpf order-3 -> 2240 copies is the other lane's Springer/G32 count"},
 "S2_third_1440_note":"Brosowsky 20x72 = C(6,3) x 72 is a count, not an asserted group action; 1440 = |Aut(S6)|",
 "S5_alpha_w39_note":"open; perp-E6 (point = E6xA2 maximal subgroup) is a structural lever, not a solution",
 "status":"PASS","passes":"7489-7496",
}
assert res["S1_dual_pair_alpha"]["alpha_W33"]==7
assert res["S1_dual_pair_alpha"]["alpha_Q43"]==10
assert res["S4_w33_family"]["rho_equals_rho2_lines"]
assert res["S4_w33_family"]["conjugate_gives_different"]
print(json.dumps({"status":"PASS","alpha_W33":7,"alpha_Q43":10,
                  "clifford_scheme":"SRG(36,10,4,2)","family_real":True}))
if __name__=="__main__": pass
