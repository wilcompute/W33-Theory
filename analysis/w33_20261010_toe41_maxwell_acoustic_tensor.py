"""TOE41 W33 Maxwell low-k 3x3 harmonic acoustic tensor.

Linearize native plaquette P(k) around k=0. Harmonic H0 = ker P0
intersect ker B0^dag has dim3. Integrating out heavy P0-image gives
G_i=(I-Q_P0 Q_P0^dag) (dP/dk_i) H0 and
A(n)=sum_ij n_i n_j G_i^dag G_j. Its two positive eigenvalues are
the *squared* acoustic velocities and the zero is longitudinal.
"""
import sys,json
import numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
from w33_20261010_toe36_incidence_relativistic_walk import gradient
OUT=ROOT/"data/w33_20261010_toe41_maxwell_acoustic_tensor.json"
ed,volts,lookup,zero,comm,picked,fc=prep()
walks=zero+comm
def plaquettes(k):return np.asarray([cycle_row(w,ed,volts,lookup,np.asarray(k)) for w in walks])
P0=plaquettes([0,0,0])
B0=gradient(ed,volts,np.zeros(3))
U,s,Vh=np.linalg.svd(P0,full_matrices=False)
rankP=int(np.sum(s>1e-7));assert rankP==78
Q=U[:,:rankP]
joint=np.vstack((P0,B0.conj().T))
_u,ss,Vh=np.linalg.svd(joint,full_matrices=False)
rankJoint=int(np.sum(ss>1e-7));assert rankJoint==157
H0=Vh.conj().T[:,rankJoint:]
assert H0.shape==(160,3)
assert np.max(abs(P0@H0))<1e-10
assert np.max(abs(B0.conj().T@H0))<1e-10
eps=2e-5
G=[]
for axis in range(3):
 n=np.zeros(3);n[axis]=eps
 deriv=(plaquettes(n)-plaquettes(-n))/(2*eps)
 Z=deriv@H0
 G.append(Z-Q@(Q.conj().T@Z))
C=np.asarray([[G[i].conj().T@G[j] for j in range(3)] for i in range(3)])
# For any real direction n, A(n) must be Hermitian/positive.
cases={}
for key,vec in {"x":(1,0,0),"y":(0,1,0),"z":(0,0,1),
                "xy":(1,1,0),"xz":(1,0,1),"xyz":(1,1,1)}.items():
 n=np.array(vec,dtype=float);n/=np.linalg.norm(n)
 K=sum(n[i]*n[j]*C[i,j] for i in range(3) for j in range(3))
 H=(K+K.conj().T)/2
 vals=np.linalg.eigvalsh(H)
 assert abs(vals[0])<1e-7 and vals[1]>.1 and vals[2]>.1,vals
 speeds=np.sqrt(vals[1:]).real
 cases[key]={"acoustic_eigenvalues":vals.tolist(),"acoustic_velocities":speeds.tolist(),"polarization_ratio":float(speeds[1]/speeds[0])}
 print(key,cases[key],flush=True)
assert cases["x"]["polarization_ratio"]>1.03
maxspread=max(v["polarization_ratio"] for v in cases.values())-1
out={"status":"PASS_ACOUSTIC_TENSOR_NONDEGENERACY","P0_rank":rankP,
     "joint_P_and_divergence_rank":rankJoint,"harmonic_dim":3,
     "derivative_step":eps,"acoustic_speeds":cases,
     "acoustic_tensor_real_3x3x3x3":C.real.tolist(),
     "acoustic_tensor_imag_3x3x3x3":C.imag.tolist(),
     "max_polarization_speed_ratio_minus_1":float(maxspread),
     "acoustic_tensor_shape":"3x3x3x3 with A_ij=H0^dag P_i^dag(I-P0 P0^+) P_j H0",
     "claim":"The two positive acoustic eigenvalues remain nondegenerate in the leading k->0 tensor for fixed equal-weight plaquettes; this split is not merely finite k. Six directions tested; no proven emergent isotropy after tuning/renormalization.",
     "boundary":"This is the leading harmonic effective quadratic tensor, not a relativistic 4D Maxwell action or physical polarization splitting."}
OUT.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out))
