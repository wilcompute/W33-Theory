#!/usr/bin/env python3
"""Pass5216: exact spectra of the connected odd-q L-chart graphs at q=3,5.

Vertices are L/opposite-line charts; two charts are adjacent when they share an
apartment.  At q=3 and q=5 this graph is connected (unlike the P side).  We
verify a square-free integer annihilator on delta at one chart.  Chart
transitivity then promotes it to an operator annihilator.  Exact closed-walk
moments at the same chart recover the displayed irreducible-sector
multiplicities.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5216_ODDQ_CONNECTEDL_EXACT_SPECTRUM.json'

def pmul(a,b):
    z=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):z[i+j]+=x*y
    return z

def Lgraph(q):
    G=build_W(q);L=[loc for t,loc in G['charts'] if t=='L'];own=[[] for _ in G['apartments']]
    for i,loc in enumerate(L):
        for a in loc.values():own[a].append(i)
    assert set(map(len,own))=={2}
    adj=[set() for _ in L]
    for u,v in own:adj[u].add(v);adj[v].add(u)
    d={len(x) for x in adj};assert d=={q*(q+1)//2}
    # Connected and triangle free.
    seen={0};Q=[0]
    while Q:
        u=Q.pop()
        for v in adj[u]:
            if v not in seen:seen.add(v);Q.append(v)
    assert len(seen)==len(L)
    assert all(not (adj[u]&adj[v]) for u in range(len(L)) for v in adj[u] if u<v)
    return [sorted(x) for x in adj]

def apply(v,adj):
    z=[0]*len(v)
    for i,x in enumerate(v):
        if x:
            for j in adj[i]:z[j]+=x
    return z

def poly_power_sums(coeff,K):
    # coeff low-to-high, monic degree d. Newton sums for roots.
    d=len(coeff)-1;a=[coeff[d-k] for k in range(1,d+1)] # x^d+a1 x^(d-1)+...
    s=[d]
    for k in range(1,K+1):
        val=0
        for i in range(1,min(k,d)+1):val+=a[i-1]*s[k-i]
        if k<=d:val+=k*a[k-1]
        s.append(-val)
    return s

def anchor(q,factors):
    adj=Lgraph(q);n=len(adj);p=[1]
    for f,m in factors:p=pmul(p,f)
    deg=len(p)-1
    v=[0]*n;v[0]=1;pows=[];mom=[]
    for k in range(deg+1):
        pows.append(v);mom.append(n*v[0])
        if k<deg:v=apply(v,adj)
    residual=[0]*n
    for k,c in enumerate(p):
        if c:
            for i,x in enumerate(pows[k]):residual[i]+=c*x
    assert not any(residual)
    # predicted traces from irreducible-factor power sums
    pred=[]
    for k in range(deg+1):
        z=0
        for f,m in factors:z+=m*poly_power_sums(f,k)[k]
        pred.append(z)
    assert pred==mom
    dim=sum((len(f)-1)*m for f,m in factors);assert dim==n
    return {'q':q,'vertices':n,'degree':len(adj[0]),'connected':True,'triangle_free':True,
      'annihilator_coefficients_low_to_high':p,'annihilator_degree':deg,
      'annihilator_delta_residual_l1':0,'trace_moments_0_to_degree':mom,
      'irreducible_factors':[{'coefficients_low_to_high':f,'multiplicity':m,'degree':len(f)-1} for f,m in factors]}

def main():
    q3=[([-6,1],1),([-3,1],60),([-2,1],84),([-1,1],81),([1,1],120),([3,1],116),([-9,-2,1],24),([-18,1,1],15)]
    q5=[([-15,1],1),([-6,1],130),([-5,1],1235),([-3,1],520),([-1,1],1899),([0,1],520),([2,1],520),([3,1],625),([4,1],520),([5,1],1534),([-50,-3,1],90),([-75,2,1],65),([-30,2,1],104),([40,-12,-4,1],576)]
    A={'3':anchor(3,q3),'5':anchor(5,q5)}
    out={'pass':5216,'status':'THEOREM_EXACT_CONNECTED_ODDQ_L_CHART_SPECTRA_Q3_Q5',
      'definition':'Vertices are L/opposite-line charts; an apartment joining its two L owners is an edge.',
      'q3_spectrum':'6^1,3^60,2^84,1^81,(-1)^120,(-3)^116; roots of x^2-2x-9 each mult 24; roots of x^2+x-18 each mult 15.',
      'q5_spectrum':'15^1,6^130,5^1235,3^520,1^1899,0^520,(-2)^520,(-3)^625,(-4)^520,(-5)^1534; roots of x^2-3x-50 each mult 90; x^2+2x-75 each 65; x^2+2x-30 each 104; roots of x^3-4x^2-12x+40 each mult 576.',
      'anchors':A,
      'connection':'The odd-q L-side obstruction is a connected triangle-free chart graph with a nontrivial rational representation decomposition, not the P-side disjoint tensor graph. These exact factors provide the spectral/module target for L-heavy equality-shell inequalities.',
      'boundary':'This is an exact q3/q5 diagonalization. An all-odd-q closed spectrum formula and identification of every irreducible sector with a named group representation remain open.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
