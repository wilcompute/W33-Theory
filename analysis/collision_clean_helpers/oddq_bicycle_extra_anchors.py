#!/usr/bin/env python3
"""Pass5136: independent q=9/q=13 cross-characteristic anchors for the odd-q bicycle theorem.

Master Pass5130 already promotes the all-odd-prime-power bicycle formula using
the established binary incidence-rank theorem.  This collision-clean pass does
not re-own that theorem.  It supplies two independent large exact anchors,
including the nonprime field F9, by rebuilding W(3,q) and row-reducing its
point-line incidence matrix over F2.
"""
from __future__ import annotations
import argparse,itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5136_ODDQ_BICYCLE_EXTRA_ANCHORS.json'
class PrimeField:
    def __init__(self,p):self.q=p
    def add(self,a,b):return(a+b)%self.q
    def sub(self,a,b):return(a-b)%self.q
    def mul(self,a,b):return(a*b)%self.q
    def inv(self,a):return pow(a,-1,self.q)
class GF9:
    q=9
    def add(self,u,v):return((u%3+v%3)%3)+3*((u//3+v//3)%3)
    def sub(self,u,v):return((u%3-v%3)%3)+3*((u//3-v//3)%3)
    def mul(self,u,v):
        a,b=u%3,u//3;c,d=v%3,v//3
        return((a*c+b*d)%3)+3*((a*d+b*c+b*d)%3) # w^2=w+1
    def inv(self,u):
        for v in range(1,9):
            if self.mul(u,v)==1:return v
        raise ZeroDivisionError

def incidence(F):
    q=F.q;add,sub,mul,inv=F.add,F.sub,F.mul,F.inv
    def smul(a,v):return tuple(mul(a,x) for x in v)
    def vadd(x,y):return tuple(add(a,b) for a,b in zip(x,y))
    def norm(v):
        for a in v:
            if a:return smul(inv(a),v)
        raise ValueError
    pts=sorted({norm(v) for v in itertools.product(range(q),repeat=4) if any(v)});pi={p:i for i,p in enumerate(pts)}
    def sp(x,y):return add(sub(mul(x[0],y[2]),mul(x[2],y[0])),sub(mul(x[1],y[3]),mul(x[3],y[1])))
    lines=set()
    for i,x in enumerate(pts):
      for j in range(i+1,len(pts)):
        y=pts[j]
        if sp(x,y):continue
        L={norm(vadd(x,smul(t,y))) for t in range(q)};L.add(norm(y));lines.add(frozenset(pi[z] for z in L))
    P=(q+1)*(q*q+1);assert len(pts)==len(lines)==P
    return P,lines

def rank2(lines):
    piv={}
    for L in lines:
        r=sum(1<<i for i in L)
        while r:
            p=r.bit_length()-1
            if p in piv:r^=piv[p]
            else:piv[p]=r;break
    return len(piv)
def anchor(q):
    P,L=incidence(GF9() if q==9 else PrimeField(q));r=rank2(L);target=1+q*(q+1)**2//2
    assert r==target
    null=P-r;bike=2*null-1;assert bike==q**3+q-1
    return {'q':q,'points_lines':P,'rank_F2':r,'theorem_rank':target,'rank_drop':0,'nullity_F2':null,'bicycle_dimension':bike}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--heavy',action='store_true');a=ap.parse_args()
    rows={'9':anchor(9)}
    if a.heavy:rows['13']=anchor(13)
    frozen13={'q':13,'points_lines':2380,'rank_F2':1275,'theorem_rank':1275,'rank_drop':0,'nullity_F2':1105,'bicycle_dimension':2209}
    out={'pass':5136,'status':'INDEPENDENT_ODDQ_BICYCLE_THEOREM_ANCHORS','master_theorem_owner':'Pass5130 of the independently landed Pass5126-5133 packet','anchors':rows,'frozen_q13_heavy_anchor':frozen13,
         'novelty':'q=9 is an extension-field F9 reconstruction; q=13 is a larger independent prime-field anchor. Both verify the cross-characteristic binary incidence rank used by the master theorem.',
         'boundary':'This pass is an independent verification extension, not a second claim of ownership for the all-odd-q theorem.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
