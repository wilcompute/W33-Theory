"""Round25: exact 45-sector superselection and symmetry-invariant tunneling
quotient for native W33 apartments. Determine which selection is forbidden
only by an ASSUMED conserved E6 tritangent-sector charge.
"""
from pathlib import Path
import json,sys
import numpy as np
from scipy.sparse.csgraph import connected_components
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe23_dynamic_apartment_frame import build
OUT=ROOT/'data/w33_20261009_toe25_e6_sector_tunneling_quotient.json'
def run():
 apt,A3,A2=build()
 n,lab=connected_components(A3,directed=False)
 assert n==45 and np.all(np.bincount(lab)==36)
 P=np.eye(45,dtype=np.int64)[lab]
 counts=P.T@A2@P
 Q=counts/36.0
 deg=np.asarray(A2.sum(axis=1)).ravel()
 exact=A2@P
 equitable=np.allclose(exact,P@Q)
 print('E6 QUOTIENT equitable',equitable,'entries',np.unique(Q,return_counts=True),
  'diagonal',np.unique(np.diag(Q)),'degrees',np.unique(Q.sum(axis=1)),flush=True)
 # Projected onto normalized 36-frame sector-uniform states, the
 # tunneling matrix equals 18I + 9/4 times a 45-vertex SRG adjacency.
 B=np.rint((Q-18*np.eye(45))/(9/4)).astype(np.int64)
 assert np.allclose(Q,18*np.eye(45)+(9/4)*B)
 assert np.array_equal(B,B.T) and np.all(np.diag(B)==0)
 assert set(np.unique(B))=={0,1} and np.all(B.sum(axis=1)==32)
 assert np.array_equal(B@B,32*np.eye(45,dtype=np.int64)+22*B+24*(np.ones((45,45),dtype=np.int64)-np.eye(45,dtype=np.int64)-B))
 lam=np.linalg.eigvalsh(Q.astype(float))
 uq,counts=np.unique(np.round(lam,8),return_counts=True)
 print('E6 QUOTIENT SPEC',list(zip(uq,counts)),flush=True)
 # Commutator with each component projection. Select a witness inter-fiber hopping edge.
 c0=np.flatnonzero(lab==0)
 cut=A2[c0,:][:,np.flatnonzero(lab!=0)]
 assert cut.nnz>0
 cross_links=int(sum(lab[r]!=lab[c] for r,c in zip(*A2.nonzero()))//2)
 assert cross_links>0
 # A3 lies exactly block diagonal. A2 breaks the charge conservation.
 assert np.all(lab[np.array(A3.nonzero())[0]]==lab[np.array(A3.nonzero())[1]])
 out=dict(status='PASS',apartment_hilbert_space=1620,sector_count=45,
  frame_states_per_sector=36,
  overlap_three_degree=8,overlap_two_degree=90,
  quotient_exact_equitability=equitable,
  quotient_matrix_entries={str(float(k)):int(v) for k,v in zip(*np.unique(Q,return_counts=True))},
  quotient_adjacency_eigenvalues={str(float(k)):int(v) for k,v in zip(uq,counts)},
  quotient_degree=float(Q.sum(axis=1)[0]),nonzero_cross_sector_overlap_two_edges=cross_links,
  projected_45_e6_SRG='45-vertex graph SRG(45,32,22,24), with quotient = 18 I + (9/4) A_45, exact verified matrix identity',
  caution_non_equitable='The uniform sector subspace is NOT invariant under A2: the 45x45 matrix is a compression, not an exact isolated dynamics. In particular 9/4 off-diagonal entries are averaged amplitudes; the full 1620x1620 system couples to intrafiber excitations.',
  exact_charge_conservation='For each tritangent-label r the orthogonal projector P_r onto its 36 apartment states commutes with A3. The full family P_r defines a conserved E6-tritangent label (superselection) for H=-t A3 or any Hamiltonian block diagonal in this partition.',
  symmetry_no_go='Overlap-two A2 is ALSO PSp-invariant but has nonzero matrix elements between different tritangent sectors, so [A2,P_r] != 0. Thus PSp alone does NOT enforce their superselection; forbidding A2 requires an extra physical conservation law, locality principle or fundamental charge, not supplied by W33 symmetry.',
  physical_status='A precise structural test and conditional sector symmetry. Physical gauge origin of the 45-valued charge and stability under generic interactions are not established.')
 OUT.write_text(json.dumps(out,indent=2)+'\n')
 return out
if __name__=='__main__':run()
