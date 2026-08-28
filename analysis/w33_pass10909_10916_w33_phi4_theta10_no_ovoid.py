#!/usr/bin/env python3
"""Pass10909-10916: Phi4(3)=10 is a spectral W33 shadow, not a 10-point ovoid.

Reconstruct W(3,3) as the 40 projective points of F3^4 with symplectic
collinearity.  Exhaust the complement graph by exact bitset Bron-Kerbosch.
The maximum independent set has size7, with 2880 maximum cocliques.  Hence
there is no 10-point W33 ovoid/coclique.

At the same time the SRG parameters (40,12,2,4) give nontrivial eigenvalues
2^24 and (-4)^15.  The ratio/Lovasz bound is

  -v*s/(k-s) = 40*4/16 = 10 = Phi4(3).

For the complement, parameters/eigenvalues give the corresponding bound4.
W33 is vertex-transitive, so theta(G)theta(Gbar)=40; the two ratio bounds
therefore force theta(W33)=10 and theta(Gbar)=4 exactly.

Thus the HJ10/P1(F9) carrier cannot be a literal ten-point W33 geometry.  The
natural W33 occurrence of ten is the unattained spectral capacity relaxation.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10909_10916_W33_PHI4_THETA10_NO_OVOID.json'
P=3

def canon(v):
    v=[x%P for x in v]
    for x in v:
      if x:
        u=pow(x,-1,P);return tuple(u*y%P for y in v)
    raise ValueError

def main():
    pts=sorted({canon(v) for v in itertools.product(range(P),repeat=4) if any(v)})
    assert len(pts)==40
    J=((0,1,0,0),(2,0,0,0),(0,0,0,1),(0,0,2,0))
    def pair(a,b):return sum(a[i]*J[i][j]*b[j] for i in range(4) for j in range(4))%3
    adj=[]
    for i,a in enumerate(pts):
      m=0
      for j,b in enumerate(pts):
        if i!=j and pair(a,b)==0:m|=1<<j
      adj.append(m)
    assert {x.bit_count() for x in adj}=={12}
    # Verify SRG lambda/mu.
    lam=set();mu=set()
    for i in range(40):
      for j in range(i+1,40):
        c=(adj[i]&adj[j]).bit_count()
        (lam if ((adj[i]>>j)&1) else mu).add(c)
    assert lam=={2} and mu=={4}

    # Max independent sets = max cliques in complement, exact bitset BK.
    full=(1<<40)-1
    comp=[full^(1<<i)^adj[i] for i in range(40)]
    best=[0,0]
    def bk(r,Pm,Xm):
      if not Pm and not Xm:
        if r>best[0]:best[:]=[r,1]
        elif r==best[0]:best[1]+=1
        return
      if r+Pm.bit_count()<best[0]:return
      U=Pm|Xm
      if U:
        us=[i for i in range(40) if (U>>i)&1]
        u=max(us,key=lambda z:(Pm&comp[z]).bit_count())
        cand=Pm&~comp[u]
      else:cand=Pm
      while cand:
        b=cand&-cand;v=b.bit_length()-1
        bk(r+1,Pm&comp[v],Xm&comp[v])
        Pm&=~b;Xm|=b;cand&=~b
        if r+Pm.bit_count()<best[0]:return
    bk(0,full,0)
    assert best==[7,2880]

    v,k,la,mm=40,12,2,4
    # SRG polynomial x^2+(mu-lambda)x+(mu-k)=x^2+2x-8.
    eig={'12':1,'2':24,'-4':15}
    assert 12+2*24-4*15==0
    theta_bound=v*4//(k+4);assert theta_bound==10
    # complement has degree27 and least eigen -3.
    theta_comp_bound=40*3//(27+3);assert theta_comp_bound==4
    assert theta_bound*theta_comp_bound==40

    old=json.loads((ROOT/'data/PART_W33_PASS10877_10884_HJ10_SPLIT_P1F9_GEOMETRY.json').read_text())
    assert old['HJ']['inner_C6_quotient_states']==10
    out={
      'schema':'w33.pass10909_10916.w33_phi4_theta10_no_ovoid.v1','status':'PASS','passes':'10909-10916',
      'W33':{'parameters':[40,12,2,4],'spectrum':eig,'independence_number':7,'maximum_cocliques':2880,'ten_point_ovoid_exists':False},
      'spectral_capacity':{
        'Phi4_3':10,'Hoffman_ratio_bound':10,
        'complement_degree':27,'complement_least_eigenvalue':-3,'complement_theta_bound':4,
        'vertex_transitive_theta_product':'theta(G) theta(Gbar)=40','theta_W33':10,'theta_complement':4,
        'gap':'theta(W33)-alpha(W33)=3'},
      'HJ10_consequence':{'states':10,'literal_W33_point_ovoid':False,'surviving_W33_interpretation':'spectral/Lovasz capacity shadow at Phi4(3)=10 rather than a ten-point incidence subset'},
      'theorem':'W33 has independence number7, not10, so its Phi4(3)=10 cannot be a ten-point ovoid/coclique. Nevertheless the exact vertex-transitive SRG spectral bounds force Lovasz theta(W33)=10. Therefore the HJ10/P1(F9) carrier matches the natural W33 ten at the spectral-capacity level, not as a literal W33 point subset.',
      'boundary':'W33 reconstruction and alpha=7 census are exhaustive finite computations. The theta equality uses the standard Lovasz product theorem for vertex-transitive graphs together with exact ratio bounds. No operator intertwiner between HJ10 and the W33 theta SDP is constructed here.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','alpha':7,'max_cocliques':2880,'theta':10,'HJ10':'spectral not pointwise'}))
if __name__=='__main__':main()
