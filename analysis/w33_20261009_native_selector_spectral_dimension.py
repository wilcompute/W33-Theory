"""Native W33 line-context and collinear-triple spatial couplers:
no imposed Euclidean lattice. Exact finite graph geometry, return
probability, spectral dimension and adjacency spectrum.

Line graph: SRG(40,12,2,4), Laplacian 0^1+10^24+16^15.
Selector graph: 160 collinear triples, edges share 1 or 2 points,
degree 30. Both are transitive finite graphs; their heat-kernel
dimension tends to zero at short AND long times, so an intrinsic
asymptotic three-dimensional continuum is NOT obtained without
a separately justified infinite cover / thermodynamic limit.
"""
from itertools import combinations
from pathlib import Path
import sys,json
import numpy as np
import networkx as nx
from scipy.optimize import minimize_scalar
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import bt1688_exact_h1_character_irreducibility as B
def spectrum_geom(A):
 n=A.shape[0]
 G=nx.from_numpy_array(A)
 assert nx.is_connected(G)
 deg=int(A[0].sum());assert np.all(A.sum(axis=1)==deg)
 ev=np.linalg.eigvalsh(np.eye(n)*deg-A)
 assert abs(ev[0])<1e-8
 def p(t):
  z=np.exp(-t*ev)
  return float(z.mean()),float(2*t*sum(ev*z)/sum(z))
 tgrid=np.logspace(-3,2,41)
 data=[dict(t=float(t),return_probability=p(t)[0],effective_dimension=p(t)[1]) for t in tgrid]
 res=minimize_scalar(lambda logt:-p(np.exp(logt))[1],bounds=(-9,4),method='bounded',
   options={'xatol':1e-11})
 max_ds=-res.fun
 # Count times within 10% of 3 (not a claim of scaling plateau).
 close=[float(t) for t in np.logspace(-4,3,601) if abs(p(t)[1]-3)<.3]
 exact_round={}
 for x in ev:
  k=f'{float(0 if abs(x)<1e-8 else x):.9f}'
  exact_round[k]=exact_round.get(k,0)+1
 return dict(vertices=n,degree=deg,edges=int(A.sum()/2),
    diameter=nx.diameter(G),ball_shells_from_vertex_0=dict(__import__('collections').Counter(nx.single_source_shortest_path_length(G,0).values())),
    laplacian_approx_eigenmultiplicities=exact_round,
    maximum_effective_spectral_dimension=max_ds,at_time=float(np.exp(res.x)),
    time_points_near_dimension3_count=len(close),first_and_last_near3_times=[min(close),max(close)] if close else None,
    sampled_heat_trace=data)
def certificate():
 lines=B.w33_lines(B.make_points())
 lineA=np.array([[int(i!=j and bool(set(a)&set(b))) for j,b in enumerate(lines)] for i,a in enumerate(lines)],dtype=int)
 assert np.all(lineA.sum(axis=1)==12)
 A2=lineA@lineA
 assert np.array_equal(A2,8*np.eye(40,dtype=int)-2*lineA+4*np.ones((40,40),dtype=int))
 line=spectrum_geom(lineA)
 assert line['diameter']==2 and line['ball_shells_from_vertex_0']=={0:1,1:12,2:27}
 assert line['laplacian_approx_eigenmultiplicities']=={'0.000000000':1,'10.000000000':24,'16.000000000':15}
 triples=[tuple(x) for L in lines for x in combinations(L,3)]
 triA=np.array([[int(i!=j and len(set(a)&set(b)) in (1,2)) for j,b in enumerate(triples)] for i,a in enumerate(triples)],dtype=int)
 tri=spectrum_geom(triA)
 assert tri['vertices']==160 and tri['degree']==30
 return dict(status='PASS',line_context=line,collinear_triples=tri,
    native_line_L_spectrum={'0':1,'10':24,'16':15},
    exact_line_return='P_line(t)=(1+24e^{-10t}+15e^{-16t})/40',
    exact_line_dim='d_s(t)=2t*(240e^{-10t}+240e^{-16t})/(1+24e^{-10t}+15e^{-16t})',
    theorem='At finite graph size, heat return P(t)->1 as t->0 and P(t)->1/N as t->infinity, so local spectral dimension -2 dlogP/dlogt->0 at BOTH ends. No fixed finite graph has an asymptotic d=3 heat-kernel power law.',
    observed_scope='The W33 line coupler is strictly native (line intersection), and triple coupler is native overlap, no supplied square lattice. Finite spectral dimensions are scale-dependent transients; a physical 3D continuum requires a justified infinite cover or coupled limit, dimensional stability and Lorentzian microdynamics.')
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_native_selector_spectral_dimension.json').write_text(json.dumps(d,indent=2)+'\n')
 print('NATIVE SPACE',[(k,d[k]['diameter'],d[k]['maximum_effective_spectral_dimension']) for k in ('line_context','collinear_triples')])
