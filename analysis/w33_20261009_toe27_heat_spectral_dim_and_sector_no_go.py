"""Round27: finite graph Lorentzian/spacetime-emergence firewall.
Compute EXACT normalized Levi spectral heat traces across W(3,q) and
show the natural q->infinity limit lacks any fixed-time d_s=4 plateau.
Separate exact graph spectrum from physical causal dynamics.
"""
from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261009_toe27_heat_spectral_dim_and_sector_no_go.json'
TIMES=[.5,1.,2.,4.,8.]
def params(q,t):
 m=(q+1)*(q*q+1)
 mr=q*(q+1)**2//2
 ms=q*(q*q+1)//2
 assert 1+mr+ms==m
 r=math.sqrt(2*q)/(q+1)
 e=math.exp
 vals=[(0,1),(2,1),(1-r,mr),(1+r,mr),(1,2*ms)]
 ht=sum(mult*e(-t*x) for x,mult in vals)/(2*m)
 weighted=sum(mult*x*e(-t*x) for x,mult in vals)/(2*m)
 ds=2*t*weighted/ht
 return dict(q=q,Levi_sites=2*m,normalized_adjacency_nontrivial_r=r,
  normalized_Laplacian_spectrum=[{'lambda':v,'mult':num} for v,num in vals],
  time=t,normalized_heat_trace=ht,discrete_spectral_dimension=ds,
  limiting_heat_trace=math.exp(-t),limiting_spectral_dimension=2*t)
def run():
 cases={}
 for q in (2,3,5,7,11,31,101,1009):
  data=[params(q,t) for t in TIMES]
  assert all(abs(x['normalized_heat_trace']-math.exp(-x['time']))<.15 for x in data) if q>=31 else True
  cases[str(q)]=data
  print('HEAT q',q,'dimension at t1,2,4:',
        *(round(data[i]['discrete_spectral_dimension'],5) for i in (1,2,3)),flush=True)
 assert abs(cases['1009'][2]['discrete_spectral_dimension']-4)<.2
 limit={str(t):{'H':math.exp(-t),'spectral_dimension':2*t} for t in TIMES}
 result=dict(status='PASS',geometry='W(3,q) incidence Levi graph, q prime power',
  graph_diameter=4,
  exact_graph_adjacency_spectrum='+(q+1)^1, -(q+1)^1, +sqrt(2q)^mr, -sqrt(2q)^mr, 0^(2ms), where mr=q(q+1)^2/2, ms=q(q^2+1)/2',
  normalized_graph_laplacian='L=I-A/(q+1)',
  heat_trace='H_q(t)=Tr(exp(-tL))/[2(q+1)(q²+1)]',
  heat_density_limit_at_each_fixed_positive_t='exp(-t)',
  spectral_dimension_limit='d_s(t)=-2d(log H)/d(log t) -> 2t',
  no_4d_plateau='The limiting d_s(t)=2t equals four ONLY at isolated t=2 and cannot remain near 4 across a scale range. Graph diameter remains four for all q, while normalized nontrivial adjacency eigenvalues collapse sqrt(2q)/(q+1)->0. This is an exact obstruction to interpreting the raw normalized Levi graph large-q family as a 4-dimensional diffusion continuum; it does not rule out additional dynamics, long-range interpolating constructions, or physics beyond adjacency.',
  e6_sector_charge='For W33 q3 1620-frame apartments, the prior Round26 exact model has 45 connected E6 labels at A3 and a symmetry-allowed A2 that creates a positive first-order 67.5 epsilon tunneling gap. Therefore PSp symmetry alone does not protect an emergent 45-valued gauge charge. Imposing U(1)^45 (one independent number for each sector) would forbid tunneling as an EXTRA ASSUMPTION, but without a microscopic gauge principle this is engineering, not a derivation.',
  data=cases,limiting_data=limit,
  physical_scope='A falsifiable mathematical no-go for the simplest normalized adjacency diffusion as 3+1D spacetime and an explicit superselection symmetry gap. Does not produce Einstein equations, a Lorentz cone, effective field equations or a protected physical frame vacuum.')
 OUT.write_text(json.dumps(result,indent=2)+'\n')
 return result
if __name__=='__main__':run()
