#!/usr/bin/env python3
"""All 40 W(3,3) lines are explicit Cartan subalgebras of the two-qutrit sl9 Pauli grading."""
import itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pauli_cartans.json'
def symp(v,w):
    x,z,u,t=v;y,s,r,k=w;return (z*y-s*x+t*r-k*u)%3
def canon(v):
    v=tuple(x%3 for x in v);j=next(i for i,x in enumerate(v) if x);iv=1 if v[j]==1 else 2;return tuple(iv*x%3 for x in v)
def add(a,b):return tuple((x+y)%3 for x,y in zip(a,b))
def mul(c,a):return tuple(c*x%3 for x in a)
def main(write=True):
    V=[v for v in itertools.product(range(3),repeat=4) if any(v)]
    P=sorted({canon(v) for v in V});assert len(P)==40
    lines=set()
    for a,b in itertools.combinations(P,2):
        if symp(a,b):continue
        L=frozenset(canon(add(mul(i,a),mul(j,b))) for i,j in itertools.product(range(3),repeat=2) if i or j)
        if len(L)==4:lines.add(L)
    lines=sorted(lines,key=lambda L:sorted(L));assert len(lines)==40
    cartans=[]
    for L in lines:
        D=sorted({v for q in L for v in (q,tuple((-x)%3 for x in q))})
        assert len(D)==8 and all(symp(a,b)==0 for a,b in itertools.combinations(D,2)); cartans.append(D)
    c=Counter();adj=[set() for _ in range(40)]
    for i,j in itertools.combinations(range(40),2):
        d=len(set(cartans[i])&set(cartans[j]));c[d]+=1;assert d in (0,2)
        if d==2:adj[i].add(j);adj[j].add(i)
    assert c==Counter({0:540,2:240}) and {len(a) for a in adj}=={12}
    lam=set();mu=set()
    for i,j in itertools.combinations(range(40),2):
        q=len(adj[i]&adj[j]);(lam if j in adj[i] else mu).add(q)
    assert lam=={2} and mu=={4}
    out={'schema':'w33.pauli_cartan_system.v1','status':'PASS',
      'headline':'Every W(3,3) line lifts to an 8-dimensional Cartan subalgebra of sl(9,C): its four projective points are eight nonzero F3^4 Pauli degrees, all commute, and their finite-order Pauli matrices are semisimple. The 40 Cartans reproduce W33 again under nonzero intersection.',
      'counts':{'W33_projective_points':40,'W33_lines':40,'oriented_nonzero_degrees_per_line':8,'sl9_rank':8,'intersecting_cartan_pairs_dimension2':240,'disjoint_cartan_pairs':540},
      'cartan_argument':{'abelian':'symplectic form vanishes on each 2D Lagrangian, so all eight Pauli homogeneous generators commute','semisimple':'each Pauli generator has finite order 3 up to scalar and is diagonalizable over C','maximal':'the commuting semisimple subalgebra has dimension 8 = rank(sl9), hence is a Cartan subalgebra'},
      'intersection_graph':{'vertices':40,'adjacent_iff':'Cartan intersection has dimension 2, equivalently the two W33 lines share one projective point','srg':[40,12,2,4],'isomorphic_to':'W(3,3) point/line graph by self-duality'},
      'cartans':[{'index':i,'projective_points':[list(x) for x in sorted(lines[i])],'oriented_degrees':[list(x) for x in cartans[i]]} for i in range(40)],
      'checks':{'40_lines':len(lines)==40,'each_support_has_8_degrees':all(len(x)==8 for x in cartans),'all_cartans_isotropic':all(all(symp(a,b)==0 for a,b in itertools.combinations(D,2)) for D in cartans),'pair_census_240_540':c==Counter({0:540,2:240}),'intersection_graph_SRG_40_12_2_4':lam=={2} and mu=={4} and {len(a) for a in adj}=={12}}}
    assert all(out['checks'].values())
    if write: OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['headline','counts','cartan_argument','intersection_graph','checks']},indent=2));return out
if __name__=='__main__':main(True)
