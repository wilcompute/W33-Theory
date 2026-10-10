"""Round23: exact obstruction to naively truncating the sl9-graded E8
84+84 three-form sectors to 81+81. This is NOT an obstruction to
a nontrivial change of E8 grading to E6+A2+(27,3)+(27*,3*).
"""
from pathlib import Path
import json,itertools,sys,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass11681_e8_from_two_qutrits import TR,TI,psign,wedge_star
OUT=ROOT/'data/w33_20261009_toe23_e8_sector_leakage.json'
def run():
 excluded=[(0,1,2),(3,4,5),(6,7,8)]
 keep=[x for x in TR if x not in excluded]
 assert len(TR)==84 and len(keep)==81
 small={}
 outputs=set()
 for C in TR:
  S=tuple(i for i in range(9) if i not in C)
  witness=None
  for P in itertools.combinations(S,3):
   Q=tuple(j for j in S if j not in P)
   if P not in excluded and Q not in excluded:
    witness=(P,Q);break
  if witness is not None:
   outputs.add(C)
   if C in excluded:small[str(C)]=[list(witness[0]),list(witness[1])]
 assert len(outputs)==84 and len(small)==3
 # Check W33 canonical E8 graded bracket for three explicit
 # independent basis pairs with nonzero output in the EXCLUDED dual sector.
 numerical=[]
 for C in excluded:
  P,Q=(tuple(t) for t in small[str(C)])
  a=np.zeros(84,complex);b=np.zeros(84,complex)
  a[TI[P]]=1;b[TI[Q]]=1
  z=wedge_star(a,b)
  assert abs(z[TI[C]])>0 and np.count_nonzero(z)==1
  numerical.append(dict(missing_dual_channel=list(C),
     allowed_input_triples=[list(P),list(Q)],
     bracket_output_coefficient=[float(z[TI[C]].real),float(z[TI[C]].imag)]))
 # Mixed brackets span the ENTIRE sl9 zero grade as a linear vector space:
 # Offdiagonals E_ij: choose two-index P disjoint from {i,j},
 # with (P U {i}), (P U {j}) both in the 81 selected set.
 offdiag={}
 for i in range(9):
  for j in range(9):
   if i==j:continue
   pairs=[(a,b) for a,b in itertools.combinations([k for k in range(9) if k not in (i,j)],2)
      if tuple(sorted((a,b,i))) in keep and tuple(sorted((a,b,j))) in keep]
   assert pairs
   offdiag[f'{i},{j}']=[int(x) for x in pairs[0]]
 # Diagonal span: 81 triples' weight vectors 1_S in C^9,
 # modulo 1_all has full 8D; exact rank mod101.
 from w33_pass1081_1086_core import rank_mod
 diag=np.array([[int(i in S) for i in range(9)] for S in keep],dtype=np.int64)
 diag_rank=rank_mod(diag%101,101)
 assert diag_rank==9
 res=dict(status='PASS',origin='Existing validated E8=sl(9)+Lambda3(9)+Lambda3(9)* at Pass11681',
  source_grade_dimensions=[80,84,84],naive_target_dimensions=[86,81,81],
  truncated_positive_sector_basis=81,excluded_basis_triples=[list(x) for x in excluded],
  grade_plus_plus_output_rank=84,
  excluded_dual_grade_witnesses=numerical,
  mixed_to_sl9_offdiagonal_channels=len(offdiag),
  mixed_to_sl9_diagonal_full_rank=diag_rank,
  theorem='For this explicit, natural coordinate restriction from 84 to 81 trivectors, the original E8 bracket [81,81] produces ALL 84 dual trivector channels: every output complementary triple has an admissible disjoint pair of retained input triples. Hence the 81-subsector is NOT closed under the inherited E8 bracket. Mixed-sector pair brackets also generate all 80 sl9 channels (72 offdiagonal and 8 traceless diagonal). The E6+A2 86+81+81 grading cannot be obtained by simply dropping three 3-forms and relabeling the sl9 80-dimensional grade-zero sector.',
  limitation='Only refutes this straightforward coordinate truncation, not all possible embeddings or regradings. The actual E8 E6xA2 grading is known to exist, and an intertwining identification of its 81 matter pieces with the W33 Steinberg module remains unconstructed.')
 OUT.write_text(json.dumps(res,indent=2)+'\n')
 print('E8 81 input -> dual span',len(outputs),'and excluded 3',numerical,flush=True)
 return res
if __name__=='__main__':run()
