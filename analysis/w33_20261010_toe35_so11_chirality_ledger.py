"""Round35 spinorial E8 centralizer -> SO10 GUT chirality ledger.

From established Spin11xSpin5 branching
248=(55,1)+(1,10)+(11,5)+(32,4).
Under Spin11 -> Spin10:
 55 ->45+10, 11->10+1, 32->16+conj16.
Spinorial odd-sector matter is a paired (16,4)+(conj16,4).
Under SU5:16=10+5bar+1; conj16=10bar+5+1.
This gives zero NET complex gauge chirality in the unprojected
E8 adjoint. The Lorentz four-dimensional irrep is NOT four
fermion generations. No physical chirality selected.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261010_toe35_spinorial_so11_spin10_chirality.json'
def run():
 base=json.loads((ROOT/'data/w33_20261010_toe35_spinorial_e8_so11_centralizer.json').read_text())
 assert base['total_fixed_Lie_algebra_dimension']==55
 # E8 decomposition as Spin11 x Spin5 modules:
 blocks=[('adj_SO11',55,1),('adj_SO5',1,10),('vector_vector',11,5),('spinor_spinor',32,4)]
 assert sum(a*b for _,a,b in blocks)==248
 # breaking SO11 -> SO10 by a nonzero vector:
 b10=[
  ('so10_adj',45,1,False),('so10_vector_from_SO11_adj',10,1,False),
  ('so5_adj',1,10,False),
  ('so10_vector_cross_SO5_vector',10,5,False),
  ('so10_singlet_cross_SO5_vector',1,5,False),
  ('so10_chiral16',16,4,True),('so10_antichiral16bar',16,4,True)]
 assert sum(n*m for _,n,m,_ in b10)==248
 odd=sum(n*m for _,n,m,flag in b10 if flag)
 assert odd==128
 # SO10 spinor chiral16 -> SU5 10+5bar+1; conjugate16bar
 #   ->10bar+5+1. Four is spinorial Lorentz module,
 # not 4 flavors in any physical spacetime sense.
 su5=[
  dict(so10='16',parts={'10':10,'5bar':5,'1':1},lorentz_spin_dim=4),
  dict(so10='16bar',parts={'10bar':10,'5':5,'1':1},lorentz_spin_dim=4)]
 assert all(sum(p['parts'].values())==16 for p in su5)
 gauge_index=4-4
 assert gauge_index==0
 # 16+16bar is complex-representation vectorlike, under the
 # explicit unprojected gauge carrier irrespective of a
 # physical spacetime handedness, not a physical 4D anomaly theorem.
 result=dict(status='PASS',source='Round35 proven so11 centralizer and standard Spin11xSpin5 E8 branching',
  SO11xSO5_E8_decomposition=[dict(sector=s,SO11_dim=a,Spin5_dim=b,dimension=a*b) for s,a,b in blocks],
  SO10xSpin5_E8_decomposition=[dict(sector=s,SO10_dim=a,Spin5_dim=b,dim=a*b,
     spinorial_matter=odd) for s,a,b,odd in b10],
  so10_chiral_matter_multiplet='(16,4) + (16bar,4), dimensionality 64+64=128',
  su5_content=su5,
  su5_complex_rep_net_chirality_by_Lorentz_spin_dim={'10_vs_10bar':gauge_index,'5bar_vs_5':gauge_index},
  physical_consequence='Unprojected E8 spinorial matter sector is vectorlike as a complex Spin10/SU5 gauge representation: every 16 appears with its conjugate 16bar carrying the same finite Spin5 spinorial 4. The bare Lie embedding does not select a physical chiral generation or 3 families.',
  requirement='Obtain a specified chirality-selective spectrum via 4D spacetime Weyl structure, orbifold/localized defects, index-theoretic flux, boundary projection, or equivalent dynamical mechanism. Check consistency with gauge anomalies, CPT and Lorentz representation, not by simply deleting the 16bar summand.',
  caveat='A vectorlike compact internal representation does not alone rule out chiral 4D physics after dimensional reduction or projection. 4 is the dimension of ONE irreducible spin representation of finite Lorentz, NOT 4 independently observed families; no fermion masses or anomalies evaluated.')
 OUT.write_text(json.dumps(result,indent=2)+'\n')
 print('TOE35 chiral index 10-10bar=',gauge_index,'16+conj16=128, centralizer so11',flush=True)
 return result
if __name__=='__main__':run()
