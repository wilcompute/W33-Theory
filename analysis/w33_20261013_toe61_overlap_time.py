"""TOE61 native 320-component overlap: static temporal continuation.

A pointwise 320x320 signature is NOT a 4D spacetime index or Weyl measure.
We test necessary temporal gap/spectral flow controls without physical claims.
"""
from pathlib import Path
import json,sys,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'analysis'))
from w33_pass11977_native_overlap import kernel,clifford
rng=np.random.default_rng(6107);ph=rng.uniform(-.16,.16,size=160);k=[.17,-.21,.09]
g,g5=clifford();Ref=np.kron(1j*g[3]@g5,np.eye(80))
assert np.max(abs(Ref@Ref-np.eye(320)))<1e-13
rows=[]
for m0 in (.5,3.):
 for w in (0.,.3,.85,1.57,2.4,np.pi):
  Q,G=kernel(k,w,phases=ph,m0=m0)
  e=np.linalg.eigvalsh(Q)
  signature=int(round(np.sum(np.sign(e))))
  gap=float(np.min(abs(e)))
  Qneg,_=kernel(k,-w,phases=ph,m0=m0)
  refl=float(np.max(abs(Ref@Q@Ref+Qneg)))
  assert refl<1e-10
  if w in (0.,np.pi):
   assert abs(signature)==0
  rows.append(dict(Wilson_mass=m0,omega=float(w),Hermitian_gap=gap,
                   local_signature=signature,local_overlap_index=-signature//2,
                   reflection_pairing_error=refl))
  print('TOE61 overlap',m0,w,gap,signature,flush=True)
out={'status':'PASS_TOE61_STATIC_OVERLAP_TIME_REFLECTION_BOUNDARY',
'actual_W33_spinor_band_count':320,'sampled_random_gauge_phase_bound':.16,
'model':'Existing Pass11977 Hermitian Euclidean Wilson overlap kernel Q(k,omega) on 80 site/4 spinor graph, supplied mass and static site gauge phases.',
'rows':rows,
'exact_symmetry_test':"For static spatial link phases R Q(k,omega) R=-Q(k,-omega) where R=i gamma4 gamma5. Index signature at ±omega is opposite. At temporal corners0 andπ, self-pairing forces exact zero if gapped. A connected gapped fixed-spatial-phase omega sweep cannot generate a nonzero pointwise signature without gap closing. This is not a statement that all topologically nontrivial 4D overlap fields have zero index.",
'physics_boundary':"These are matrix signatures in a family parameterized by Euclidean frequency, NOT a Dirac index of a full discretized physical 4D gauge bundle, chiral gauge measure, SM generations, gravitational anomaly, or quantum TOE. No temporal gauge links on a 4-cell spatial completion were built.",
'prior':"Pass11977 already proves this reflection identity and static corner zero index; new mass/time scans are only regression and acceptance tests."}
(R/'data/w33_20261013_toe61_overlap_time.json').write_text(json.dumps(out,indent=2)+'\n')
