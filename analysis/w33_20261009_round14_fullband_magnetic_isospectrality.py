"""EXACT no-go: all 86,400 optimal W33 3-flag selectors
are *FULL-BAND MAGNETIC ISOSPECTRAL* for ANY three independent
edge Peierls phases k1,k2,k3 on the selected flags.

This resolves a major ambiguity in apparent emergent 3D:
The 5 inequivalent PSp flag-triple orbits are different
combinatorial geometries, and a local motif Hamiltonian can
select different orbits, BUT ANY SINGLE-PARTICLE flux hopping
measurement on the native 80-vertex W33 Levi graph has exactly
the SAME 80 Bloch eigenvalues for all 86,400 optimal triples.

Rigorous proof: let A0 be 80x80 Levi adjacency, A0 satisfies
A0*(A0²-16I)*(A0²-6I)=0 (degree5). Let S_T be the 80x6
selector matrix for the endpoints p1,p2,p3,l1,l2,l3 of the
three selected flags. For each of the five full-group orbit
representatives, verify EXACT INTEGER equality of the 6x6
restricted moments S.T A0^m S for m=0,1,2,3,4.
By Cayley/minimal polynomial every matrix resolvent
S.T (lambda I-A0)^(-1) S is thereby IDENTICAL for all
five representatives, as a rational matrix in lambda.

A phased hopping perturbation on just those 3 flags is a rank6
matrix S C(k) S.T with identical 6x6 C(k) for all
representatives. Matrix determinant lemma yields identical
characteristic polynomial
det(lambda I-A0-SCS.T) = det(lambda I-A0)
      det(I-C*S.T*(lambda I-A0)^(-1)*S)
for all k (rational identity continued across eigenvalues).
PSp invariance carries result to every one of the 86400 triples.

Therefore the five orbit labels are spectrally invisible to
ALL one-particle native-photon flux bands, not just quadratic
or quartic expansions; detecting them needs interactions,
multi-photon correlations, external label measurements or a
coupler outside this rank6 local Peierls model.

This is purely graph-theoretic, NOT evidence for relativity.
"""
import json,sys
from pathlib import Path
import numpy as np
from scipy.linalg import eigvalsh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261008_5state_ritz import geometry
def certificate():
 edges,*_=geometry()
 orbit=json.loads((ROOT/'data/w33_20261009_PSp_orbits_isotropic_triplets.json').read_text())['orbits']
 N=np.zeros((80,80),dtype=np.int64)
 for p,l in edges:N[p,l]=1;N[l,p]=1
 I=np.eye(80,dtype=np.int64)
 N2=N@N
 assert np.array_equal(N@(N2-16*I)@(N2-6*I),np.zeros((80,80),dtype=np.int64))
 moments=[]
 for o in orbit:
  tri=o['representative']
  vs=[edges[f][0] for f in tri]+[edges[f][1] for f in tri]
  assert len(set(vs))==6
  proj=[]
  power=I.copy()
  for m in range(5):
   proj.append(power[np.ix_(vs,vs)].tolist())
   power=power@N
  moments.append(proj)
 assert all(moments[j]==moments[0] for j in range(1,len(moments)))
 # Entire sorted 80-eigenvalue vectors under generic PHASE vectors;
 # numerical check supplements the EXACT determinant proof.
 rng=np.random.default_rng(201014)
 probes=[]
 for k in ([0.,0.,0.],[.2,.3,-.17],[1.1,-.7,.3],
           [2.2,.9,-1.3],rng.uniform(-3,3,size=3).tolist()):
  bands=[]
  for o in orbit:
   H=N.astype(complex).copy()
   for f,phase in zip(o['representative'],k):
    p,l=edges[f]
    H[p,l]=np.exp(1j*phase)
    H[l,p]=np.exp(-1j*phase)
   bands.append(eigvalsh(H))
  err=float(max(np.max(abs(bands[j]-bands[0])) for j in range(1,5)))
  assert err<1e-11
  probes.append(dict(k=list(k),max_full_80_band_difference=err))
 return dict(status='PASS',normal_carrier_vertices=80,
    optimal_flag_triples=86400,full_group_orbits=5,
    exact_Levi_adjacency_minimal_polynomial='A(A^2-16I)(A^2-6I)=0',
    identical_restricted_moments_m0_to_m4=True,
    common_six_by_six_moments=moments[0],
    exact_magnetic_isospectrality_all_k=True,
    numerical_full80band_probes=probes,
    exact_proof='All five 6x6 endpoint-restricted powers S.T A^m S for 0<=m<=4 are identical by integer arithmetic. Minimal polynomial degree5 implies equality of endpoint-restricted resolvents for all complex spectral parameters outside spec A. Matrix determinant lemma with equal six-by-six phase update C(k) gives identical full characteristic polynomials for all three phases k, and PSp transitivity on each of the five orbit representatives extends to all 86400 selectors.',
    physical_falsifier='No native SINGLE-PHOTON Peierls-flux band measurement, at any k, distinguishes the five inequivalent W33 optimal selector orbits in this graph model. Detect orbit identity requires another observable, nonlinear interactions or nonlocal coupler modifications, not just improved optical precision.',
    boundary='A finite graph exact identity; the 3D voltage assignment is externally imposed, and no physical spacetime, Lorentz symmetry, quantum matter interactions or unification follows.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_round14_fullband_magnetic_isospectrality.json').write_text(json.dumps(d,indent=2)+'\n')
 print('FULL BAND EXACT',d['identical_restricted_moments_m0_to_m4'],
  [(x['k'],x['max_full_80_band_difference']) for x in d['numerical_full80band_probes']])
