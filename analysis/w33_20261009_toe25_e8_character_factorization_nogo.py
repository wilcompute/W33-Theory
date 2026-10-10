"""Round25 exact PSp4(3) Steinberg character counterexample to
an 81=27 x3 with trivial 3-factor, independent of which 27 module.
Classification of finite simple subgroups of PGL3(C) separately
rules out ANY nontrivial three-dimensional projective action of PSp.
"""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass1081_1086_core import build_w33,transvection_perm,enumerate_group,compose,line_perm
OUT=ROOT/'data/w33_20261009_toe25_e8_character_factorization_nogo.json'
def run():
 pts,idx,lines,lidx,pl,frames,fidx,flags,fi=build_w33()
 gens=[transvection_perm(pts[i],pts,idx) for i in (0,1,4,5,13)]
 G,_=enumerate_group(gens)
 assert len(G)==25920
 ident=tuple(range(40))
 order5=None
 for g in G:
  g2=compose(g,g);g3=compose(g,g2);g4=compose(g,g3);g5=compose(g,g4)
  if g5==ident and g!=ident:
   order5=g
   break
 assert order5
 lp=line_perm(order5,lines,lidx)
 fixpoint=sum(i==x for i,x in enumerate(order5))
 fixline=sum(i==x for i,x in enumerate(lp))
 fixflag=sum(order5[p]==p and lp[l]==l for p,l in flags)
 trace81=fixflag-fixpoint-fixline+1
 print('E8 TRACE order5',fixpoint,fixline,fixflag,trace81,flush=True)
 assert (fixpoint,fixline,fixflag,trace81)==(0,0,0,1)
 # trace on PermFlag-PermPoint-PermLine+1 is Steinberg81,
 # not only a numerical character coincidence (prior BT1688).
 # If St81 = R27 ⊗ C3_triv, chi_St = 3 chi_R at EVERY g.
 # At order 5, chi_R is an algebraic integer (sum roots of unity),
 # so chi_R=1/3 impossible. In particular any 27D rep R ruled out.
 out=dict(status='PASS',group_order=25920,group_PSp_identification='PSp(4,3) = U4(2)',
  selected_order5_point_permutation=[int(x) for x in order5],
  order5_fixed_points=fixpoint,order5_fixed_lines=fixline,
  order5_fixed_flags=fixflag,Steinberg81_order5_character=trace81,
  degree_27_tensor_trivial_3_impossible_for_any_27D_rep=True,
  exact_character_contradiction='At explicit order5 PSp element, chi_St81=0 flags-0 pts-0 lines+1=1. If St81 were R27 tensor 3 trivial singlets, chi_R27 would equal 1/3, impossible since character values of a finite-group representation are algebraic integers. No 27D candidate module can repair this.',
  projective_3_factor_obstruction='Classical classification of finite simple subgroups of PGL3(C) lists A5 (order60), PSL2(7) (168), A6 (360); PSp4(3) has order25920 and cannot inject into PGL3(C). Any projective 3D action of simple PSp4(3) is therefore trivial. Under the added ASSUMPTION that the G-action factors through an E6xSL3 (or compatible projective) subgroup preserving its factors, the 3-factor cannot carry nontrivial PSp dynamics.',
  boundaries='Not a no-go for E8 itself, for non-factor-preserving embeddings, for acting via a different group/central extension, or for symmetry breaking. Explicit mixed E8 intertwiner not constructed.',
  classification_sources=['https://archive.mpim-bonn.mpg.de/id/eprint/3662/1/preprint_2009_76.pdf','https://www.math.rwth-aachen.de/homes/sam/ctbllib/doc2/chap11_mj.html'],
  repo_prior='BT1688 Steinberg irreducibility; Pass4659 27 Schlaefli and tritangent; Round24 permutation27 trivial3 obstruction. The explicit order5 trace1 is a simpler obstruction for EVERY 27 candidate with trivial A2.')
 OUT.write_text(json.dumps(out,indent=2)+'\n')
 return out
if __name__=='__main__':run()
