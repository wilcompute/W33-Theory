"""TOE62 front5: quantitative NONUNIFORM finite graph Leibniz obstruction.

The same W33 derivative admits O(a) error on constant-fiber low Bloch
plane waves but O(1/a) error on localized vertex idempotents. Therefore
a low-Bloch calculation CANNOT establish uniform gravitational constraint
closure. This is a negative control, not a gravity/TOE solution.
"""
from pathlib import Path
import numpy as np,json,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'analysis'))
from w33_pass11970_native_wilson_dirac import construction
ed,volt,J,*_=construction();E=np.asarray(ed,int);J=np.asarray(J,float)
B=np.zeros((160,80));C=np.zeros((160,80))
for e,(a,b) in enumerate(E):
 B[e,a]=-1;B[e,b]=1;C[e,a]=C[e,b]=.5
D=np.asarray([C.T@(J[:,i,None]*B) for i in range(3)])
assert np.max(abs(D+D.transpose(0,2,1)))<1e-12
assert np.max(abs(np.diagonal(D,axis1=1,axis2=2)))<1e-12
# For pointwise product f*g, R_D(f,g)=D(f*g)-f*Dg-g*Df.
# e_v*e_v=e_v, and D_vv=0 for skew D, so R_D(e_v,e_v)=D e_v.
column=np.linalg.norm(D,axis=(0,1))
peak=int(np.argmax(column)); minnorm=float(min(column)); maxnorm=float(max(column))
assert minnorm>1e-7
checks=[]
for v in (0,peak,79):
 u=np.zeros(80);u[v]=1
 err=D@(u*u)-2*u[None,:]*(D@u)
 assert np.max(abs(err-D[:,:,v]))<1e-12
 checks.append({'vertex':v,'pointwise_Leibniz_residual_RMS':float(np.linalg.norm(err)/np.sqrt(3*80)),
                'stacked_column_norm':float(np.linalg.norm(err))})
scales=[]
for a in (.2,.1,.05,.025):
 vertex_err=maxnorm/a
 # previously measured O(a) low-Bloch error, from TOE60.
 prior=json.loads((R/'data/w33_20261013_toe60_leibniz_coefficient.json').read_text())
 rec=next(r for r in prior['rms_records'] if abs(r['a']-a)<1e-10)
 scales.append({'a':a,'vertex_idempotent_worst_defect_after_1_over_a_scaling':vertex_err,
                'restricted_low_Bloch_RMS_defect':rec['rms_error'],
                'high_over_low_ratio':vertex_err/rec['rms_error']})
assert scales[-1]['high_over_low_ratio']>scales[0]['high_over_low_ratio']*30
out={'status':'PASS_TOE62_NONUNIFORM_NATIVE_LEIBNIZ_NO_GO',
'native_derivative_shape':list(D.shape),'D_skew_error':float(np.max(abs(D+D.transpose(0,2,1)))),
'exact_unscaled_idempotent_column_norm_min':minnorm,
'exact_unscaled_idempotent_column_norm_max':maxnorm,'worst_vertex':peak,
'vertex_controls':checks,'spacing_sweep':scales,
'mathematical_theorem':"For pointwise finite vertex function algebra R^80 and ANY linear operator D obeying exact Leibniz, apply to minimal idempotent e_v^2=e_v: D e_v =2e_v·D e_v. At u!=v this forces D_uv=0 and at u=v forces D_vv=0, hence D=0. For the actual nonzero skew W33 D_i, R_i(e_v,e_v)=D_i e_v exactly. Therefore under physical 1/a scaling, the worst such localized Leibniz defect is ||D e_v||/a, diverging as a→0 even while the prior restricted Bloch-sector defect goes like O(a). No full-space uniform continuum derivation follows from restricted bandwise convergence.",
'gravity_boundary':"This proves only the failure of the EXACT pointwise product derivation and a particular uniform finite-graph normalization. It does NOT rule out weak/coarse-grained continuum fields, different noncommutative or edge algebra, improved canonical constraints, Einstein gravity, or interacting universal Lorentz restoration. Pass11976 separately computed a concrete gravitational scalar bracket defect.",
'field_strength_scope':"No new physical speed-of-light prediction, spin-2 graviton, time-dependent Einstein constraints, renormalized interacting photon/fermion beta function, or SI-scale gravitational constant."}
(R/'data/w33_20261013_toe62_gravity_nonuniform.json').write_text(json.dumps(out,indent=2)+'\n')
print('TOE62 gravity',minnorm,maxnorm,'amplification',scales[-1]['high_over_low_ratio'],flush=True)
