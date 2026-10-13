"""TOE62 front3: genuine temporal-link flat gauge consistency, not a 4D index.

Show how apparent electric field from time-dependent spatial link phases
vanishes when compatible time-directed gauge links are supplied.
"""
from pathlib import Path
import json,sys
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'analysis'))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
from w33_pass11977_native_overlap import kernel
ed,vs,lk,octs,comm,*_=prep();E=np.asarray(ed,int);V=np.asarray(vs,int)
P=np.rint(np.asarray([cycle_row(x,ed,vs,lk,np.zeros(3)).real for x in octs+comm])).astype(int)
Nt=12; rng=np.random.default_rng(6203)
amplitudes=rng.uniform(-.7,.7,80);phi=np.pi*np.ones(3)
theta=np.asarray([amplitudes*np.sin(2*np.pi*t/Nt) for t in range(Nt)])
base=V@phi
A=np.asarray([base+theta[t,E[:,1]]-theta[t,E[:,0]] for t in range(Nt)])
Usp=np.exp(1j*A)
Utm=np.asarray([np.exp(1j*(theta[(t+1)%Nt]-theta[t])) for t in range(Nt)])
spaterr=float(np.max(abs(np.exp(1j*(A@P.T))-1)))
flaterr=0.
fake=[]
for t in range(Nt):
 nxt=(t+1)%Nt
 a=E[:,0];b=E[:,1]
 temporal_plaquette=Utm[t,a]*Usp[nxt]*np.conj(Utm[t,b])*np.conj(Usp[t])
 flaterr=max(flaterr,float(max(abs(temporal_plaquette-1))))
 fake.extend(np.angle(Usp[nxt]*np.conj(Usp[t])).tolist())
fake_rms=float(np.linalg.norm(fake)/np.sqrt(len(fake)))
assert spaterr<1e-12 and flaterr<1e-12 and fake_rms>.04
# Native overlap Hermitian kernel at one time: gauge covariance vs
# an explicitly curved, but PURE-GAUGE spacetime link history.
Q0,G=kernel(np.zeros(3),.37,phases=base)
rows=[]
for t in (0,3,6,9):
 Qt,_=kernel(np.zeros(3),.37,phases=A[t])
 u=np.tile(np.exp(1j*theta[t]),4)
 difference=Qt-u.conj()[:,None]*Q0*u[None,:]
 err=float(np.max(abs(difference)))
 assert err<1e-10
 rows.append({'time_slice':t,'kernel_gauge_covariance_max':err})
out={'status':'PASS_TOE62_TIME_LINK_4D_GAUGE_COVARIANCE_GATE',
'actual_sites':80,'actual_links':160,'native_local_plaquette_rows':1385,'temporal_slices':Nt,
'fake_electric_F0e_when_temporal_links_omitted_rms':fake_rms,
'true_mixed_temporal_spatial_plaquette_error_with_temporal_links':flaterr,
'spatial_plaquette_U1_flatness_max':spaterr,
'native_320_band_kernel_slice_covariance':rows,
'derivation':"On actual W33 links let U_e(t)=exp(i[V_e·(π,π,π)+θ_b(t)-θ_a(t)]), U_0(t,v)=exp(i[θ_v(t+1)-θ_v(t)]). Then all space-space and mixed time-space plaquettes equal1 exactly. Omitting U0 creates a spurious temporal electric field even for this pure-gauge time dependence. The preexisting native320 overlap kernel is unitarily gauge-covariant on each tested slice.",
'physical_limit':"This is an explicit time-link gauge-completion and null control on a 80-site graph × discrete time, NOT a full spatial three-manifold with 4-cells, an index-bearing gauge bundle, a nonzero Weyl index, SM chirality, or interacting quantum dynamics. Native spatial 2-complex × S1 still has H4=0."}
(R/'data/w33_20261013_toe62_time_links.json').write_text(json.dumps(out,indent=2)+'\n')
print('TOE62 temporal',fake_rms,flaterr,rows,flush=True)
