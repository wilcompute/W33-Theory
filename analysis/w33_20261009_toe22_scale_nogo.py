"""Exact finite-system scale nonidentifiability with native two-boson
W33 quantum Hamiltonian: energy scaling, Feynman-Hellmann response,
strong-coupling virtual pair hopping and absence of finite-size RG anomaly.
"""
import json,sys,math
from pathlib import Path
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe22_two_boson_quantum_selector import build
OUT=ROOT/'data/w33_20261009_toe22_scale_nogo.json'
def solve(H,k=2):
 v,e=eigsh(H,k=k,which='SA',tol=1e-10,maxiter=3500)
 i=np.argsort(v)
 return v[i],e[:,i]
def run():
 hop,dbl,basis=build()
 U=8.;H=hop-diags(U*dbl)
 eig,vec=solve(H)
 dU=.02
 m=solve(hop-diags((U+dU)*dbl))[0][0]
 p=solve(hop-diags((U-dU)*dbl))[0][0]
 deriv=(m-p)/(2*dU)
 occupancy=float(np.dot(dbl,abs(vec[:,0])**2))
 assert abs(deriv+occupancy)<2e-5
 ratios=[]
 for c in (.5,1.7,3):
  spec,_=solve(c*hop-diags(c*U*dbl))
  err=max(abs(spec-c*eig))
  assert err<1e-6
  ratios.append({'scale':c,'E0':float(spec[0]),'gap':float(spec[1]-spec[0]),'relative_error':float(err)})
 spec32,_=solve(hop-diags(32*dbl))
 gap=float(spec32[1]-spec32[0])
 pred=2*(4-math.sqrt(6))/32
 assert abs(gap/pred-1)<.03
 record={'status':'PASS','Hilbert_dimension':3240,'quantum_model':'fixed N=2 Bose Hubbard native 80-site Levi graph',
   'Feynman_Hellmann_U_8':{'central_difference_dE0_dU':deriv,'minus_doublon_probability':-occupancy,'difference':deriv+occupancy},
   'scale_covariance':ratios,
   'strong_coupling_U32':{'exact_gap':gap,'leading_2t2_over_U_gap':pred,'relative_difference':gap/pred-1},
   'scale_identifiability_nogo':'For H(t,U)=t H(1,U/t), multiplying both couplings by c>0 multiplies all finite-system energy eigenvalues and gaps by c while leaving eigenvectors, all dimensionless correlations and gap ratios unchanged. Graph incidence cannot determine t in eV or GeV. The quantum low-band gap ~2t²(4-sqrt6)/U supplies a TUNABLE emergent scale but not an absolute prediction.',
   'thermodynamic_limit_boundary':'The partition function Z(beta;t,U)=Tr exp[-beta H(t,U)] is real analytic in couplings and inverse temperature for every finite 3240-dimensional Hilbert space at finite beta. Hence a true nonanalytic critical point or universal continuum running beta function requires an additional limiting procedure; the finite W33 device alone cannot demonstrate it.',
   'scope':'No fitted Standard Model mass, no derived fundamental beta coefficient, no spontaneous vacuum or physical dimensional transmutation; a rigorously constrained non-identifiability test.'}
 OUT.write_text(json.dumps(record,indent=2)+'\n')
 print('SCALE FH derivative',deriv,'occupation',occupancy,'largeU gap',gap,flush=True)
 return record
if __name__=='__main__':run()
