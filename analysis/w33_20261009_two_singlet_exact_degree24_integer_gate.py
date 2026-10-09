"""EXACT finite-degree holomorphic monomial gate for 8 promising
two-even-singlet alternatives. Unlike permissive R^2_+ charge-cone
masks, this requires integer powers and the old support's known
hidden-SU2 *gauge-invariant* ring.

Pass11797 proves the 13-field support invariant ring is FI-five
positive fields times charge-ZERO mesons x,y,M_ij. For hidden-singlet
Yukawa/mass target operators, any invariant support insertion with
nonzero U1 charge uses ONLY five FI fields plus the two new fully
gauge-singlet fields; neutral mesons may multiply but never change U1.

Search ALL nonnegative integer exponents of 2 new singlets through
total degree bound 24, then solve the unique 5 FI exponents exactly.
R/CFT couplings still unresolved. Not an unrestricted all-order claim.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from math import lcm
import json,sys
import sympy as S
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11797_11801_five_physical_fronts as P
FI=['n_17','n_47','n_50','n_80','n_82']
def certificate():
 raw,prior,fields,support,q=P.load()
 parent=json.load(open(ROOT/'data/w33_20261009_two_even_singlets_exact_27729.json'))
 combos=parent['exact_double_rank_repair_pairs']
 assert len(combos)==8
 basis=json.load(open(ROOT/'data/w33_pass11793_order_four_matter_action.json'))['candidate_three_family_Higgs_basis']
 UP=[(a,b,basis['H_u'][0]) for a in basis['Q'] for b in basis['u_c']]
 down=json.load(open(ROOT/'data/w33_pass11797_11801_five_physical_fronts.json'))['pass11799']['mass_sectors']['d']
 DD=[(a,b) for a in down['rows'] for b in down['columns']]
 assert all(fields[n]['dim'].split(',')[2:] == ['1','1'] for x in UP+DD for n in x)
 targets=UP+DD
 B=S.Matrix.hstack(*(S.Matrix(q[n]) for n in FI))
 assert B.rank()==5
 piv=list(B.T.rref()[1]);inv=B.extract(piv,list(range(5))).inv()
 annihilator=B.T.nullspace()
 assert len(annihilator)==4
 scale=lcm(*(x.denominator for ns in targets+[(x,) for pair in combos for x in pair] for n in ns for x in q[n]))
 def ints(names):return tuple(int(scale*sum(q[n][j] for n in names)) for j in range(9))
 rows=[]
 for v in annihilator:
  den=lcm(*(x.q for x in v));r=(den*v).applyfunc(int)
  rows.append(tuple(int(x) for x in r))
 def project(k):return tuple(sum(row[i]*k[i] for i in range(9)) for row in rows)
 candidates=[]
 max_degree=24
 tgt=[tuple(-x for x in ints(t)) for t in targets]
 for aa,bb in combos:
  qa,qb=ints([aa]),ints([bb])
  ra,rb=project(qa),project(qb)
  pool=[]
  for ea in range(max_degree+1):
   for eb in range(max_degree-ea+1):
    x=tuple(qa[j]*ea+qb[j]*eb for j in range(9))
    pool.append((ea,eb,x,project(x)))
  found=[]
  for it,Y in enumerate(tgt):
   residual=project(Y)
   candidatesolutions=[]
   for ea,eb,v,rv in pool:
    if rv!=residual:continue
    rhs=[F(Y[i]-v[i],scale) for i in range(9)]
    coeff=inv*S.Matrix([rhs[i] for i in piv])
    if B*coeff!=S.Matrix(rhs):continue
    if not all(y.q==1 and y>=0 for y in coeff):continue
    total=int(sum(coeff))+ea+eb
    if total>max_degree:continue
    candidatesolutions.append((total,ea,eb,[int(y) for y in coeff]))
   if candidatesolutions:
    best=min(candidatesolutions)
    found.append(dict(target=list(targets[it]),index=it,total_insertion_degree=best[0],
       extra_singlet_exponents=[best[1],best[2]],
       five_FI_exponents=best[3]))
  yes={z['index'] for z in found}
  mu=[[int(j+3*i in yes) for j in range(3)] for i in range(3)]
  mc=[[int(9+j+10*i in yes) for j in range(10)] for i in range(7)]
  candidates.append(dict(pair=[aa,bb],bounded_degree=max_degree,
    up_integer_U1_matching_rank=P.matching_rank(mu),
    colored_integer_U1_matching_rank=P.matching_rank(mc),
    up_integer_U1_mask=mu,colored_integer_U1_mask=mc,
    monomial_charge_witnesses=found))
 hist={str(t):n for t,n in Counter((x['up_integer_U1_matching_rank'],x['colored_integer_U1_matching_rank']) for x in candidates).items()}
 return dict(status='PASS',max_total_insertion_degree=max_degree,
   number_passing_previous_REAL_cone_both_ranks=8,
   exact_integer_exponent_candidate_pairs=candidates,
   integer_rank_histogram=hist,
   proof_scope='Integer U1 charge-neutral monomials composed of all five FI-base VEV fields + two new parity-even true singlets, with arbitrary old charge-ZERO meson factors excluded from charge search (they cannot create new charge solutions). All nonnegative exponents of the 2 extras up to degree24 are enumerated and unique FI exponents solved exactly. Target SM bilinear/trilinear is hidden non-Abelian singlet, consistent with using old SU2 singlet invariants.',
   limit='No complete all-orders Hilbert basis for unrestricted degree; R/nonR/space-group/oscillator constraints and nonzero string coefficients not yet applied. A VEV support with these extra fields is only infinitesimally D-flat, not F-flat.')
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_two_singlet_exact_degree24_integer_gate.json').write_text(json.dumps(d,indent=2)+'\n')
 print('INTEGER MONOMIAL GATE',d['integer_rank_histogram'],[(x['pair'],len(x['monomial_charge_witnesses'])) for x in d['exact_integer_exponent_candidate_pairs']])
