"""Exact Levi 8-cycle-weighted Cauchy lower bound on quantum Vopt
at a point where the old scalar Cauchy barrier V_CS is exactly ZERO.

U 160x80 oriented carrier edge incidence (integer 40U),
sum U_e=0. Any alternating oriented 8-cycle c obeys c^T U=0,
sum c=0. For a chosen factor zero z_e0=0, choose c_e0=+1,
w=ones-c; then w_e0=0, w^T U=0, sum w=160.

With q0=-a V_e0/||V_e0||² and z_e=a*t_e, exact rational
bound Vopt(q0) >= a^4*(sum w)^2 /sum_{z_e!=0}(w_e²/t_e²).
This is a *local* pointwise full-H energy barrier, does not
produce a global E0 lower bound. It is a new weighted dual witness.
"""
import sys,json
from pathlib import Path
from fractions import Fraction as F
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as H
import w33_20261008_5state_ritz as R
def certificate():
 g=H.geometry();u=np.rint(40*g['u']).astype(np.int64);v=np.rint(40*g['v']).astype(np.int64)
 edges,*_=R.geometry()
 assert len(edges)==160
 ix={frozenset(edge):j for j,edge in enumerate(edges)}
 e0=0;aa,bb=edges[e0]
 graph=nx.Graph();graph.add_nodes_from(range(80));graph.add_edges_from(edges)
 graph.remove_edge(aa,bb)
 path=nx.shortest_path(graph,aa,bb)
 assert len(path)==8,(len(path),path)
 cyc=[e0]+[ix[frozenset([path[i],path[i+1]])] for i in range(7)]
 c=np.zeros(160,dtype=np.int64)
 for i,j in enumerate(cyc):c[j]=1 if i%2==0 else -1
 # On path, initial edge aa->bb, last returns bb->aa, path orientation
 # must alternate at vertices. If dot fails, use overall alternating
 # edge sign parity (starting e0), which should still be a cycle.
 assert np.max(abs(c@u))==0,(cyc,c@u)
 assert c.sum()==0 and c[e0]==1
 w=np.ones(160,dtype=np.int64)-c
 assert w[e0]==0 and w.sum()==160
 assert np.max(abs(w@u))==0
 vv=int(v[e0]@v[e0])
 assert vv==3120 and all(int(row@row)==vv for row in v)
 t=[F(vv-int(z@v[e0]),vv) for z in v]
 zero=[i for i,x in enumerate(t) if x==0]
 assert zero==[e0],zero
 denominator=sum((F(int(w[i]*w[i]),1)/(t[i]*t[i]) for i in range(160) if w[i]!=0),F(0))
 lower=F(160*160,400)/denominator
 assert lower>F(1,4)
 # Numerical independent sharp pointwise least squares optimum
 a=1/np.sqrt(20);q=-a*g['v'][e0]/float(g['v'][e0]@g['v'][e0])
 z=a+g['v']@q
 U=z[:,None]*g['u']
 coeff,*_=np.linalg.lstsq(U,-a*z,rcond=1e-12)
 opt=float(np.linalg.norm(U@coeff+a*z)**2)
 assert float(lower)<opt+1e-11
 return dict(status='PASS',chosen_edge=edges[e0],eight_cycle_edges=cyc,
    exact_integer_left_null_weight_histogram={str(i):int(sum(w==i)) for i in (0,1,2)},
    exact_weighted_divergence_zero=True,exact_weight_sum=160,
    chosen_position='q=-a*V_e0/||V_e0||²; exactly one of 160 affine factors is zero',
    previously_zero_scalar_barrier='V_CS(q)=0, since z_e0=0',
    exact_new_lower_rational=str(lower),exact_new_lower_decimal=float(lower),
    numerical_optimal_local_potential=float(opt),
    finite_radius_support_caveat='Pointwise at one special q: by continuity the lower extends positively to some unspecified small neighborhood. It does NOT imply a uniform global mass gap or control other classical zeros.',
    proof='At every q, for any w with U^T w=0 and w_i=0 at vanishing z_i, weighted Cauchy yields Vopt(q)>=a² (sum w)^2/sum_i w_i²/z_i². The constructed alternating Levi 8-cycle c has U^Tc=0 and sum c=0, hence w=1-c works. q is chosen so z_i=a t_i and a^4=1/400; exact fraction lower produced above.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_weighted_cycle_local_quantum_bound.json').write_text(json.dumps(d,indent=2)+'\n')
 print('8 CYCLE WEIGHTED LOWER',d['exact_new_lower_decimal'],'opt',d['numerical_optimal_local_potential'])
