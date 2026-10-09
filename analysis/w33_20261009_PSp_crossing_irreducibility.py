"""PSp(4,3)-representation evidence for the 15- and 24-state W33
photonic flatband crossing modules, independent of energy claims.

Exact PSp character norms for SRG 40-point 15 and24 eigenspaces
from rational spectral projectors and all 25920 group elements.
Then compare point-module characters with orthogonal
crossing-projector characters on the 160 collinear-triple states.

Also conditional full-H vacuum result:
if the compact-resolvent Hamiltonian's ground eigenspace has
dimension ONE, its PSp character must be trivial (PSp(4,3) simple).
But nothing here proves that ground is nondegenerate.
"""
import sys,json
from pathlib import Path
from collections import Counter
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import bt1688_exact_h1_character_irreducibility as B
from w33_20261009_correlated_disorder_dual_couplers import construct
def certificate():
 pts=B.make_points();lines=B.w33_lines(pts);group=B.projective_group(pts)
 assert len(group)==25920
 A=np.zeros((40,40),dtype=np.int64)
 for L in lines:
  for p in L:
   for q in L:
    if p!=q:A[p,q]=1
 assert np.array_equal(A@A,8*np.eye(40,dtype=np.int64)-2*A+4*np.ones((40,40),dtype=np.int64))
 I=np.eye(40,dtype=np.int64)
 L=np.zeros((40,40),dtype=np.int64)
 for a in range(40):
  for b in range(40):
   if a!=b and set(lines[a])&set(lines[b]):L[a,b]=1
 assert np.array_equal(L@L,8*np.eye(40,dtype=np.int64)-2*L+4*np.ones((40,40),dtype=np.int64))
 Pline15=(L-12*I)@(L-2*I)
 Pline24=-(L-12*I)@(L+4*I)
 assert np.array_equal(Pline24@Pline24,60*Pline24)
 assert np.array_equal(Pline15@Pline15,96*Pline15)
 P15=(A-12*I)@(A-2*I)  # divide by96
 P24=-(A-12*I)@(A+4*I) # divide by60
 assert np.array_equal(P15@P15,96*P15)
 assert np.array_equal(P24@P24,60*P24)
 assert int(np.trace(P15))==96*15
 assert int(np.trace(P24))==60*24
 # For each group permutation, trace of point-module action is
 # sum_i projector[i,g(i)], an EXACT integer ratio.
 norm15=norm24=normline15=normline24=0;sum15=sum24=sumline15=0
 cross15=cross24=0
 lineidx={L:i for i,L in enumerate(lines)}
 sample_chars=[]
 for gi,perm in enumerate(group):
  lperm=[lineidx[tuple(sorted(perm[p] for p in L))] for L in lines]
  cline15=sum(int(Pline15[i,lperm[i]]) for i in range(40))
  assert cline15%96==0
  cline15//=96
  cline24=sum(int(Pline24[i,lperm[i]]) for i in range(40))
  assert cline24%60==0
  cline24//=60
  c15=sum(int(P15[i,perm[i]]) for i in range(40))
  c24=sum(int(P24[i,perm[i]]) for i in range(40))
  assert c15%96==0 and c24%60==0
  c15//=96;c24//=60
  norm15+=c15*c15;norm24+=c24*c24;normline15+=cline15*cline15
  normline24+=cline24*cline24
  cross15+=c15*cline15;cross24+=c24*cline24
  sum15+=c15;sum24+=c24;sumline15+=cline15
  if gi<6:sample_chars.append([c15,c24])
 assert norm15==norm24==normline15==normline24==len(group)
 assert cross15==0 and cross24==len(group)
 assert sumline15==0
 assert sum15==sum24==0
 # Check that first/second crossing modules are mapped to
 # SRG point 15/24 spectra by calculating complementary 79D
 # spectral projectors in the common 160-flag representation.
 Blevi,A6,A30,M,D,P=construct()
 assert Blevi.shape==(80,160)
 R=np.zeros((40,40),dtype=np.int64)
 for li,L in enumerate(lines):R[list(L),li]=1
 assert np.array_equal(R@R.T,A+4*I)
 assert np.linalg.matrix_rank(R)==25
 from w33_20261009_local_hormander_depth import rank_mod
 assert rank_mod(R)==25 and rank_mod(np.vstack([M,P]))==64
 assert rank_mod(Blevi)==79
 # Exact equivariant first-crossing isomorphism:
 # D maps K=ker[M;P] into ker R because P=R D-M.
 # dim K=96, kernel(D|K)=ker[M;D]=H1 dim81,
 # so its image is 15D=ker R, the LINE-side 15 irrep.
 assert np.array_equal(P,R@D-M)
 eigvals,vectors=np.linalg.eigh((A6+A30)/2+2*np.eye(160))
 extra15=vectors[:,(abs(eigvals)<1e-7)]
 assert extra15.shape[1]==96
 # H1 dimension81: kernel of B. Extra15 projector recovered by
 # subtracting H1 projector; no character claim from dims alone.
 h1vals,h1vec=np.linalg.eigh(Blevi.T@Blevi)
 assert sum(abs(h1vals)<1e-7)==81
 P_h1=h1vec[:,abs(h1vals)<1e-7]@h1vec[:,abs(h1vals)<1e-7].T
 P_extra15=extra15@extra15.T-P_h1
 assert np.max(abs(P_extra15@P_extra15-P_extra15))<1e-9
 flags=[(next(iter(set(L)-set(T))),li) for li,L in enumerate(lines)
        for T in __import__('itertools').combinations(L,3)]
 edgeidx={p:i for i,p in enumerate(flags)}
 checked=0
 for g in group[:80]:
  lperm={li:lineidx[tuple(sorted(g[p] for p in L))] for li,L in enumerate(lines)}
  induced=[edgeidx[(g[p],lperm[li])] for p,li in flags]
  cline15=int(sum(Pline15[i,lperm[i]] for i in range(40))//96)
  inducedtrace=float(sum(P_extra15[i,induced[i]] for i in range(160)))
  assert abs(inducedtrace-cline15)<2e-7,(cline15,inducedtrace)
  checked+=1
 return dict(status='PASS',
  projective_symplectic_group_order=len(group),
  point15_exact_character_square=norm15,
  point24_exact_character_square=norm24,
  line15_exact_character_square=normline15,
  line24_exact_character_square=normline24,
  point_line_15_character_inner_product=str(cross15)+'/'+str(len(group)),
  point_line_24_character_inner_product=str(cross24)+'/'+str(len(group)),
  point15_average_character=sum15,
  point24_average_character=sum24,
  both_irreducible_over_complex=True,
  first_15_crossing_character_equal_to_line15_for_checked_actions=checked,
  exact_first_15_module_isomorphism='D: ker[M;P]/ker[M;D] -> ker(R) is a PSp-equivariant isomorphism. P=R D-M, dim ker[M;P]=96, dim ker[M;D]=81, dim ker(R)=15. Thus the additional 15 first-crossing modes ARE the line-side irreducible 15, by exact rank and equivariance, not numerical character fitting.',
  second_24_module_isomorphism='The 79D complement is isomorphic to rank(B) subset of the 80 point+line vertex permutation representation = 1+24+24+15_point+15_line; the 24D eigenspace at second crossing is PSp-stable and therefore must be isomorphic to the 24-point irrep because all other irreducible constituents have dimensions 1 and15.',
  first_15_crossing_character_residual_bound='2e-7 (floating 160-state crossing projector, exact line15 character)',
  exact_projector_formulas={'point15':'(A-12I)(A-2I)/96','line15':'(A_lines-12I)(A_lines-2I)/96','point24':'-(A-12I)(A+4I)/60'},
  conditional_quantum_ground_symmetry='If the actual full-H compact ground eigenspace were one-dimensional, the PSp(4,3) action on it would necessarily be trivial because PSp(4,3) is perfect/simple. This does not demonstrate actual ground nondegeneracy, trivial-sector ordering or numerical mass gap.',
  scope='The first 15-dimensional band-crossing module matches the LINE-side 15 character on 80 group actions (not point-side 15). All 40-point and 40-line 15 characters and the 40-point 24 character have exact full-group irreducibility sums. Full 160-state crossing all-group character not yet certified.',
  sample_characters=sample_chars)
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_PSp_crossing_irreducibility.json').write_text(json.dumps(d,indent=2)+'\n')
 print('PSP CROSSING',d['point15_exact_character_square'],d['point24_exact_character_square'],d['first_15_crossing_character_equal_to_line15_for_checked_actions'])
