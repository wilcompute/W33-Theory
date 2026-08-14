#!/usr/bin/env python3
"""Pass5074: exact gauge/local-test reduction and chamber-star saturation checks."""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5074_GAUGE_ACTIVE_CHART.json'

class PrimeField:
    def __init__(self,q): self.q=q
    def add(self,a,b): return (a+b)%self.q
    def mul(self,a,b): return (a*b)%self.q
    def inv(self,a): return pow(a,-1,self.q)
class GF4:
    q=4
    @staticmethod
    def add(a,b): return a^b
    @staticmethod
    def mul(a,b):
        a0,a1=a&1,(a>>1)&1; b0,b1=b&1,(b>>1)&1
        c0=a0*b0; c1=(a0*b1)^(a1*b0); c2=a1*b1
        return (c0^c2)|((c1^c2)<<1)
    def inv(self,a):
        return next(b for b in range(1,4) if self.mul(a,b)==1)

def build_W(q):
    F=GF4() if q==4 else PrimeField(q); add,mul,inv=F.add,F.mul,F.inv
    def smul(a,v): return tuple(mul(a,x) for x in v)
    def vadd(x,y): return tuple(add(a,b) for a,b in zip(x,y))
    def norm(v):
        for x in v:
            if x:return smul(inv(x),v)
        raise ValueError
    pts=sorted({norm(v) for v in itertools.product(range(q),repeat=4) if any(v)}); pidx={p:i for i,p in enumerate(pts)}
    def symp(x,y):
        if q==4:return add(add(mul(x[0],y[2]),mul(x[2],y[0])),add(mul(x[1],y[3]),mul(x[3],y[1])))
        return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%q
    def span(x,y):
        out={norm(vadd(x,smul(t,y))) for t in range(q)};out.add(norm(y));return frozenset(out)
    n=len(pts);nbr=[set() for _ in pts];lineset=set()
    for i,j in itertools.combinations(range(n),2):
        if symp(pts[i],pts[j])==0:
            nbr[i].add(j);nbr[j].add(i);lineset.add(frozenset(pidx[z] for z in span(pts[i],pts[j])))
    lines=sorted(lineset,key=lambda s:tuple(sorted(s)));pair_line={}
    for li,L in enumerate(lines):
        for a,b in itertools.combinations(sorted(L),2):pair_line[(a,b)]=li
    flags=[(p,li) for li,L in enumerate(lines) for p in sorted(L)];fidx={f:i for i,f in enumerate(flags)}
    aptset=set();oppP=[]
    for p,r in itertools.combinations(range(n),2):
        if r not in nbr[p]:
            common=sorted(nbr[p]&nbr[r]);assert len(common)==q+1;oppP.append((p,r,common))
            for a,b in itertools.combinations(common,2):aptset.add(frozenset((p,r,a,b)))
    apartments=sorted(aptset,key=lambda s:tuple(sorted(s)));aidx={A:i for i,A in enumerate(apartments)};apt_lines=[];apt_edges=[]
    for A in apartments:
        es=[]
        for a,b in itertools.combinations(sorted(A),2):
            if b in nbr[a]:
                li=pair_line[(a,b)];es.extend([(a,li),(b,li)])
        assert len(es)==8;apt_edges.append(tuple(fidx[e] for e in es));apt_lines.append(frozenset(li for _,li in es))
    laidx={A:i for i,A in enumerate(apt_lines)};lnbr=[set() for _ in lines]
    for i,j in itertools.combinations(range(len(lines)),2):
        if lines[i]&lines[j]:lnbr[i].add(j);lnbr[j].add(i)
    oppL=[]
    for l,m in itertools.combinations(range(len(lines)),2):
        if m not in lnbr[l]:oppL.append((l,m,sorted(lnbr[l]&lnbr[m])))
    charts=[]
    for p,r,common in oppP:
        charts.append(('P',{(i,j):aidx[frozenset((p,r,common[i],common[j]))] for i,j in itertools.combinations(range(q+1),2)}))
    for l,m,common in oppL:
        charts.append(('L',{(i,j):laidx[frozenset((l,m,common[i],common[j]))] for i,j in itertools.combinations(range(q+1),2)}))
    return {'q':q,'pts':pts,'lines':lines,'flags':flags,'apartments':apartments,'apt_edges':apt_edges,'charts':charts}

def chamber_stars(G):
    s=[0]*len(G['flags'])
    for a,edges in enumerate(G['apt_edges']):
        for e in edges:s[e]|=1<<a
    return s

def star_profile(q):
    G=build_W(q);s=chamber_stars(G);z=s[0];assert z.bit_count()==q**4;h=Counter();active=0
    for typ,loc in G['charts']:
        w=sum((z>>a)&1 for a in loc.values())
        if w:active+=1;h[(typ,w)]+=1
    assert active==4*q**3 and h[('P',q)]==h[('L',q)]==2*q**3
    return {'q':q,'points':len(G['pts']),'lines':len(G['lines']),'chambers':len(G['flags']),'apartments':len(G['apartments']),'charts':len(G['charts']),'star_weight':z.bit_count(),'star_active_charts':active,'point_active':h[('P',q)],'line_active':h[('L',q)]}

def main():
    out={'pass':5074,'status':'PASS','theorem':'4 wt(c_y)=sum_O wt(c_y|_O)>=q A(y); A(y)>=4q^3 would imply d>=q^4.',
         'chamber_star_formula':{'weight':'q^4','active_charts':'4q^3','point_active':'2q^3','line_active':'2q^3','local_weight':'q'},
         'checks':{str(q):star_profile(q) for q in (2,3,4,5)},
         'boundary':'Exact reformulation and saturation family; the universal active-chart lower bound remains open.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
