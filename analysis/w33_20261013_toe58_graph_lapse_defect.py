"""TOE58 front3: W33 scalar gravitational-bracket defect on low graph harmonics.

Extends prior11976 delta-source obstruction to normalized low-eigenvalue
graph lapse profiles and nonconstant canonical spatial metric slice.
Not a constructed Einstein gravity continuum constraint.
"""
from pathlib import Path
import json,sys,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_pass11976_metric_lapse_bracket import data,matrices
from w33_20261010_toe36_incidence_relativistic_walk import gradient
ed,Ds=data();D=[np.asarray(x,float) for x in Ds]
B=np.rint(gradient(ed,np.zeros((160,3)),np.zeros(3)).real)
lap=B.T@B
e,U=np.linalg.eigh(lap)
assert e[0]<1e-10
# Real low graph harmonics: normalized nonconstant eigenvectors on
# the native graph, not continuum smooth physical lapse functions.
def norm(x):return x/max(abs(x))
N=1+.25*norm(U[:,1]);M=1+.23*norm(U[:,2]);a=1+.1*norm(U[:,3])
assert min(N)>0 and min(M)>0 and min(a)>0
A,T=matrices(D,a,N,M)
defect=A-T
flat=matrices(D,np.ones(80),N,M)
assert max(abs(defect.ravel()))>1e-7
assert max(abs((flat[0]-flat[1]).ravel()))>1e-7
# At lapses proportional, both exact canonical bracket and ADM
# target vanish, confirming not a false numerical nonskew artifact.
Ac,Tc=matrices(D,a,N,2*N)
assert max(abs(Ac.ravel()))<1e-10 and max(abs(Tc.ravel()))<1e-10
rng=np.random.default_rng(5803)
q,p=rng.normal(size=(2,80))
witness=float(p@defect@q)
assert abs(witness)>1e-5
# D are exact skew-adjoint from J harmonic current normalization.
assert max(float(np.max(abs(x+x.T))) for x in D)<1e-10
out={"status":"PASS_TOE58_SMOOTH_GRAPH_LAPSE_GRAVITY_DEFECT",
"native_graph_eigenvalues_first_four":e[:4].tolist(),
"lapses":"N=1+.25 normalized first nonconstant graph eigenvector, M=1+.23 next eigenvector. Conformal metric a=1+.1 third eigenvector, g_ab=a² delta_ab.",
"max_actual_minus_target":float(np.max(abs(defect))),
"max_flat_metric_defect":float(np.max(abs(flat[0]-flat[1]))),
"random_p_q_bracket_witness":witness,
"proportional_lapses_actual_max":float(max(abs(Ac.ravel()))),
"proportional_lapses_target_max":float(max(abs(Tc.ravel()))),
"exact_D_skew_max":max(float(np.max(abs(x+x.T))) for x in D),
"conclusion":"The prior11976 canonical matter hypersurface-bracket closure defect persists even for low-eigenvalue native graph lapse profiles and positive smoothly varying graph metric samples, not merely delta-sourced lapses. It remains a failure of specified derivative/product/constraint maps only.",
"physics_boundary":"Low graph Laplacian modes are not a controlled 3+1D smooth refinement. This neither supplies a gravity theory nor proves any general no-go for discrete or emergent gravity; suitable perfect/coarse actions may restore diffeomorphisms."}
(R/"data/w33_20261013_toe58_graph_lapse_defect.json").write_text(json.dumps(out,indent=2)+"\n")
print("TOE58 GR",out["max_actual_minus_target"],out["max_flat_metric_defect"])
