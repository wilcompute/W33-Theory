from pathlib import Path
from itertools import product
from math import gcd
import sys,json,hashlib
import sympy as s
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12346_torsion_repair_certificate as c

def test_direction_search_against_independent_small_integer_directions():
 found=set()
 for v in product(range(-3,4),repeat=4):
  if not any(v) or gcd(*v)!=1 or next(x for x in v if x)<0:continue
  counts={}
  for e in c.exps:
   k=sum(x*y for x,y in zip(e,v));counts[k]=counts.get(k,0)+1
  if min(counts.values())>=2:found.add(v)
 assert found==set(c.directions()) and len(found)==17

def test_forbidden_unit_circle_polynomials():
 x=s.symbols('x')
 for p in (x-6,5*x*x+6,6*x*x+6*x+5):
  reciprocal=s.expand(x**s.degree(p,x)*p.subs(x,1/x))
  assert s.degree(s.gcd(p,reciprocal),x)==0
 assert len(c.coset_certificate())==17

def test_minor_bound_and_repair_witnesses():
 b=c.determinant_bound();assert len(b['necessary_orders'])==464
 assert max(b['necessary_orders'])==480480 and 17 not in b['necessary_orders']
 assert abs(s.Matrix(b['maximal_minor_witness']).det())==16
 assert len(c.repair_witnesses()['coordinate_pairs'])==6

def test_source_bound_data():
 p=ROOT/'data/w33_pass12346_torsion_repair_certificate.json';d=json.loads(p.read_text())
 assert d['source_sha256']==hashlib.sha256(Path(c.__file__).read_bytes()).hexdigest()
