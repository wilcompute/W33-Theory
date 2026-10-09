"""Exact Fortuin-Kasteleyn finite-grid census for the 40-state
line-context alignment model at ZERO hopping.
1D never orders at finite T; imposed 2D square interaction is the
ordinary q=40 ferromagnetic Potts model, not an emergent space dimension.
"""
from pathlib import Path
from math import log,exp,sqrt
import json,itertools
ROOT=Path(__file__).resolve().parents[1]
def edges(rows,cols):
   E=[]
   for r in range(rows):
      for c in range(cols):
        i=r*cols+c
        if c+1<cols:E.append((i,i+1))
        if r+1<rows:E.append((i,i+cols))
   return E
def polynomial(rows,cols,q=40):
  N=rows*cols;E=edges(rows,cols)
  assert len(E)<=12
  terms={}
  for mask in range(1<<len(E)):
    parent=list(range(N))
    def root(x):
      while parent[x]!=x:x=parent[x]
      return x
    for ei,(a,b) in enumerate(E):
      if mask>>ei&1:
        a=root(a);b=root(b);parent[b]=a
    comps=len(set(root(x) for x in range(N)))
    k=mask.bit_count()
    terms[k]=terms.get(k,0)+q**comps
  assert sum(terms.values())>q**N
  return terms
def results(rows,cols,temps):
  E=edges(rows,cols)
  coeff=polynomial(rows,cols)
  vals=[]
  for K in temps:
    v=exp(K)-1
    terms=[n*v**k for k,n in sorted(coeff.items())]
    Z=sum(terms)
    EA=sum(k*n*v**k for k,n in coeff.items())/Z
    expected_equal=EA*(1+v)/v/len(E)
    vals.append(dict(betaJ=K,mean_equal_bond_probability=expected_equal,
                     FK_mean_open_bonds=EA,log_partition=log(Z)))
  return dict(rows=rows,cols=cols,edges=len(E),
     coefficient_by_open_edge_count={str(k):str(v) for k,v in coeff.items()},data=vals)
def certificate():
  q=40;critical=log(1+sqrt(q))
  grids=[results(1,9,(.5,critical,3.)),results(2,3,(.5,critical,3.)),
         results(3,3,(.5,critical,3.))]
  for x in grids:
    for y in x['data']:
      K=y['betaJ']
      assert 0<y['mean_equal_bond_probability']<=1
      if x['rows']==1:
        p=exp(K)/(exp(K)+q-1)
        assert abs(p-y['mean_equal_bond_probability'])<1e-11
  return dict(status='PASS',q=q,imposed_square_lattice_critical_betaJ=critical,
    grids=grids,
    exact_1D_transfer_eigenvalues='lambda0=e^K+39, lambda1=e^K-1',
    exact_1D_correlation_length='xi = 1/log((exp(K)+39)/(exp(K)-1)) for 0<K<infinity',
    first_order_2D_fact='For square lattice q>4, the standard ferromagnetic Potts model has a first-order thermal transition at betaJ=log(1+sqrt(q)); prior statistical-mechanics result, NOT proved here.',
    source='F.Y. Wu, The Potts model Rev.Mod.Phys.54,235 (1982); also PTEP 2024 013A04.',
    exact_FK_polynomial='Z=sum_A q^{k(A)}(exp(K)-1)^|A| on finite open grid. Enumerated all 2^12 edge subsets for 3x3.',
    critical_boundary='At h=0, the selector model is exactly ordinary q40 Potts with full S40 relabeling symmetry; W33-specific line-incidence structure disappears. Square spatial connectivity and dimension are SUPPLIED, not dynamically derived. Adding h>0 restores W33 line graph, but transition line at finite h not computed.',
    scope='Small finite grids/analytic q=40 Potts reduction. No thermodynamic finite-h many-body quantum SSB, no Lorentzian causal metric or Einstein dynamics.')
if __name__=='__main__':
  d=certificate()
  (ROOT/'data/w33_20261009_selector_potts_dimension_firewall.json').write_text(json.dumps(d,indent=2)+'\n')
  print('POTTS q40 Tc',d['imposed_square_lattice_critical_betaJ'],'grids',[(x['rows'],x['cols'],[round(z['mean_equal_bond_probability'],5) for z in x['data']]) for x in d['grids']])
