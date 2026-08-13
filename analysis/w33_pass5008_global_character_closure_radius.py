#!/usr/bin/env python3
"""Pass5008: compile the low-shell observables into the full dual-character closure."""
from __future__ import annotations
import itertools,json,sys
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis.w33_pass4992_4999_common import build_base,gf2_rank_int
OUT=ROOT/'data/PART_W33_PASS5008_GLOBAL_CHARACTER_CLOSURE_RADIUS_COMPILER.json'

def det(A):
 n=len(A);s=Fraction(0)
 for p in itertools.permutations(range(n)):
  z=Fraction(-1 if sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))&1 else 1)
  for i in range(n):z*=A[i][p[i]]
  s+=z
 return s

def main():
 b=build_base();H=b['H36'];E=b['E'];ei=b['ei'];tri=b['tri_masks'];res=[m for m,_ in b['residual']]
 sigma=sum(int(x)<<i for i,x in enumerate(b['sigma']))
 stars=[]
 for v in range(36):
  m=0
  for u in H.neighbors(v):m|=1<<ei[tuple(sorted((u,v)))]
  stars.append(m)
 assert gf2_rank_int(stars)==35 and gf2_rank_int(stars+[sigma])==36
 assert gf2_rank_int(tri)==324
 assert all((s&t).bit_count()%2==0 for s in stars+[sigma] for t in tri)
 obs=tri+res;assert len(obs)==1890 and gf2_rank_int(obs)==324
 total_rel=1890-324;assert total_rel==1566
 ti={m:i for i,m in enumerate(tri)};qi={m:i for i,m in enumerate(res)}
 local=[];tops=[]
 for (a,q),items in sorted(b['pair_to_res'].items()):
  U=[d for d in range(36) if b['M'][a,d]==b['M'][q,d]==0]
  ev=[]
  for t in itertools.combinations(U,3):
   if all(H.has_edge(*e) for e in itertools.combinations(t,2)):
    m=0
    for e in itertools.combinations(t,2):m|=1<<ei[tuple(sorted(e))]
    if m in ti:ev.append(m)
  eq=[m for m,_ in items];assert (len(ev),len(eq))==(4,3)
  z=0;zq=0
  for m in ev:z^=m
  for m in eq:zq^=m
  assert z==zq and z.bit_count()==12;tops.append(z)
  r=0
  for m in ev:r|=1<<ti[m]
  for m in eq:r|=1<<(1080+qi[m])
  local.append(r)
 assert gf2_rank_int(local)==270 and gf2_rank_int(tops)==90
 missing=total_rel-270;assert missing==1296
 # Full closure forces the parity character at T3=-1080; degree-7 localizer rejects it.
 A3,A4,A5,A6,A7=1080,10530,127656,2329680,37193040
 T3,T4,T5,T6,T7=-A3,A4,-A5,A6,-A7
 m=[Fraction(1),Fraction(0),Fraction(90),-Fraction(3,4)*T3,
    Fraction(24255)+Fraction(3,2)*T4,
    -Fraction(2685,4)*T3-Fraction(15,4)*T5,
    Fraction(10874340)+2010*T4+Fraction(45,4)*T6,
    -Fraction(5037081,8)*T3-Fraction(56175,8)*T5-Fraction(315,8)*T7]
 M=[[m[i+j] for j in range(4)] for i in range(4)]
 L=[[m[i+j+1]+7*m[i+j] for j in range(4)] for i in range(4)]
 mp=[det([r[:k] for r in M[:k]]) for k in range(1,5)]
 lp=[det([r[:k] for r in L[:k]]) for k in range(1,5)]
 assert all(x>0 for x in mp) and lp[2]<0
 out={'pass':5008,'code':'K=[360,36,20]_2',
  'prior_art':{'Pass4859':'owns sigma and the switching-coset construction','Pass4867':'owns the exact cut/full-code enumerator','Pass4976':'owns A3 span(K^perp)=324'},
  'primal_structure':{'cut_rank':35,'cut_plus_sigma_rank':36,'orthogonal_to_A3_span':True,'reading':'K=Cut(H36)+<sigma>, repackaging earlier switching/cut results'},
  'global_character_compiler':{'A3':1080,'residual_A4':810,'observables':1890,'rank':324,'independent_XOR_relations':1566},
  'octahedron_local_closure':{'independent_relations':270,'top_weight12_span_rank':90,'missing_cross_octahedron_relations':1296},
  'distance173':{'third_moment_requires':'T3<=-704','parity_extreme_forced_T4':10530,'parity_extreme_moments':[str(x) for x in m],'moment_minors':[str(x) for x in mp],'X_plus_7_minors':[str(x) for x in lp],'parity_extreme_rejected':True,'full_324_bit_UNSAT_certificate':False,'exact_Ising_formulation':'distance173 iff both switching maxima for w and w+sigma are <=14, with one attaining14'},
  'covering_radius':{'interval':[134,173],'improved':False},
  'theorem':'The 1890 low-shell observables are functions of exactly324 character bits and obey1566 independent XOR closures. The270 octahedral identities account for only270, leaving1296 genuinely global cross-octahedron closures. Full closure kills the parity extreme, but no complete UNSAT certificate for all distance173 characters is produced; rho remains134..173.',
  'boundary':'This executes the exact full-character compiler/decision formulation, not an unobserved exhaustive 2^324 solve.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
