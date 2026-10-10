"""TOE question: does the full PSp(4,3) Steinberg-81 action allow an
alternating cubic tensor as required for E8 Z3-graded [81,81]->81*?
Exact finite-group character computation, not a construction of E8.
"""
from pathlib import Path
from collections import Counter
import json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass1081_1086_core import build_w33,transvection_perm,enumerate_group,compose,line_perm,outer_similitude_perm

def run():
 pts,ix,lines,li,pl,frames,fidx,flags,flagidx=build_w33()
 gens=[transvection_perm(pts[i],pts,ix) for i in (0,1,4,5,13)]
 G,_=enumerate_group(gens)
 assert len(G)==25920
 def chi(g):
  lperm=line_perm(g,lines,li)
  pfix=[k==g[k] for k in range(40)]
  lfix=[k==lperm[k] for k in range(40)]
  return 1-sum(pfix)-sum(lfix)+sum(pfix[p] and lfix[l] for p,l in flags)
 sums=Counter();examples={}
 for g in G:
  g2=compose(g,g);g3=compose(g2,g)
  a,b,c=chi(g),chi(g2),chi(g3)
  sym=(a**3+3*a*b+2*c)//6
  ext=(a**3-3*a*b+2*c)//6
  mix=(a**3-c)//3  # S_(2,1) V character, not invariant bracket itself
  assert (a**3+3*a*b+2*c)%6==0 and (a**3-3*a*b+2*c)%6==0
  sums['sym3']+=sym;sums['exterior3']+=ext;sums['S21']+=mix
  sums['wedge2_times_V']+=a*(a*a-b)//2
  sums['V_squared']+=a*a
  sums['V_trace']+=a
  if a not in examples:examples[a]=dict(chi=a,chi2=b,chi3=c)
 assert all(v%len(G)==0 for v in sums.values()),sums
 dims={k:int(v//len(G)) for k,v in sums.items()}
 # The natural outer symplectic SIMILITUDE doubles projective PSp.
 # Its action remains type-preserving on the Levi incidence graph.
 outer=outer_similitude_perm(pts,ix)
 assert outer not in set(G)
 assert compose(outer,outer)==tuple(range(40))
 Gset=set(G)
 assert all(compose(outer,compose(gen,outer)) in Gset for gen in gens)
 extended=Counter(sums)
 for g in G:
  h=compose(outer,g);h2=compose(h,h);h3=compose(h2,h)
  a,b,c=chi(h),chi(h2),chi(h3)
  extended['sym3']+=(a*a*a+3*a*b+2*c)//6
  extended['exterior3']+=(a*a*a-3*a*b+2*c)//6
  extended['S21']+=(a*a*a-c)//3
  extended['wedge2_times_V']+=a*(a*a-b)//2
  extended['V_squared']+=a*a
  extended['V_trace']+=a
 assert all(v%(2*len(G))==0 for v in extended.values()),extended
 extended_dims={k:int(v//(2*len(G))) for k,v in extended.items()}
 print('E8 INVARIANTS',dims,'EXTENDED GSp',extended_dims,flush=True)
 result=dict(status='PASS',group_order=len(G),representation='W33 Levi 81D irreducible Steinberg over characteristic zero',
   invariant_dimensions=dims,projective_similitude_group_order=2*len(G),extended_similitude_invariant_dimensions=extended_dims,character_examples=examples,
   exact_formulas={'Sym3':'(chi(g)^3+3 chi(g)chi(g²)+2 chi(g³))/6',
       'Lambda3':'(chi(g)^3-3 chi(g)chi(g²)+2 chi(g³))/6',
       'Hom_G(Lambda2 V,V)':'average chi(g)*(chi(g)^2-chi(g²))/2 for self-dual V'},
   physical_bridge='E8 complex Z3 grading under E6xA2 has 248=(78+8)+81+81. Bare dimension equality is not an E8 bracket. The PSp invariant alternating cubic space has dimension five, but extending to projective GSp similitudes of order 51840 leaves EXACTLY ONE invariant alternating cubic up to scale. This gives a UNIQUE metric-compatible antisymmetric candidate on the Steinberg 81 under extended symmetry; it has not been constructed explicitly or tested for Jacobi, E6xA2 interaction grading, real form, or physical locality.',
   prior_art='Existing analysis/w33_pass11681_e8_from_two_qutrits.py already builds E8 via sl9+Lambda3(9)+Lambda3(9)*; we do not re-claim this. The present representation is the DIFFERENT 81D Levi Steinberg, not an identified E8 E6xA2 matter 81.')
 (ROOT/'data/w33_20261009_toe21_steinberg_cubic_invariants.json').write_text(json.dumps(result,indent=2)+'\n')
 return result
if __name__=='__main__':run()
