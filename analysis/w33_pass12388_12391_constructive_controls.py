"""Declared overlap regulator, global-bound criterion and dense preparation controls.
Known constructions are not presented as a selected TOE action or chiral measure.
"""
from pathlib import Path
import sys,json
from itertools import product
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
import w33_pass12383_12386_dualhost_fronts as p
ROOT=Path(__file__).resolve().parents[1]

def overlap():
 I=np.eye(2);sx=np.array([[0,1],[1,0]]);sy=np.array([[0,-1j],[1j,0]]);sz=np.diag([1,-1])
 gamma=[np.kron(sx,I),np.kron(sy,I),np.kron(sz,sx),np.kron(sz,sy)];g5=np.kron(sz,sz)
 assert all(np.allclose(a@b+b@a,2*np.eye(4) if i==j else 0) for i,a in enumerate(gamma) for j,b in enumerate(gamma))
 rows=[]
 for k in [np.zeros(4)]+[np.pi*np.array(v) for v in product(range(2),repeat=4) if any(v)]+list(np.random.default_rng(12389).uniform(-np.pi,np.pi,(30,4))):
  Dw=1j*sum(np.sin(k[i])*gamma[i] for i in range(4))+(sum(1-np.cos(k))-1)*np.eye(4)
  H=g5@Dw;E,U=np.linalg.eigh(H);sign=(U*np.sign(E))@U.conj().T;D=np.eye(4)+g5@sign
  residual=float(np.max(abs(g5@D+D@g5-D@g5@D)));assert residual<1e-12
  rows.append({'k':k.tolist(),'Wilson_kernel_gap':float(min(abs(E))),'GW_residual':residual,'overlap_smallest_singular':float(np.linalg.svd(D,compute_uv=False)[-1])})
 assert rows[0]['overlap_smallest_singular']<1e-12
 assert all(x['overlap_smallest_singular']>1 for x in rows[1:16])
 return {'mass_parameter':1,'samples':rows,'scope':'Standard free4D Euclidean overlap symbol; tests GW relation and removes the15 naive corner doublers. No native-cover embedding, gauge interaction, chiral determinant measure or anomaly cancellation proof.'}

def preparation():
 from w33_20261029_klein_e8_hamming_twistor_transform import generators,hamming_code
 old=json.loads((ROOT/'data/w33_pass12383_12386_dualhost_fronts.json').read_text())['quantum_lift']
 codes=[hamming_code(g) for g in generators()];C=np.zeros((256,9))
 for j,index in enumerate(old['Hamming_nine_orbit_indices']):C[list(codes[index]),j]=.25
 labels=list(product(range(3),repeat=2));w=np.exp(2j*np.pi/3);X=np.roll(np.eye(3),1,axis=0);Z=np.diag(w**np.arange(3))
 F=np.array([[w**(-r*a-s*b)/3 for r,s in labels] for a,b in labels]);states=C@F/np.sqrt(old['Fourier_norm_squared'])
 T=np.column_stack([np.kron(states[:,j],(np.linalg.matrix_power(X,s)@np.linalg.matrix_power(Z,r))[:,x]) for j,(r,s) in enumerate(labels) for x in range(3)])
 U=np.eye(768,dtype=complex);reflections=[]
 for j in range(27):
  x=U[:,j];y=T[:,j];v=x-y;den=np.vdot(v,x)
  if np.linalg.norm(v)<1e-12:continue
  assert abs(den)>1e-12
  U-=np.outer(v,(v.conj()@U))/den
  reflections.append({'input_column':j,'denominator_real':float(den.real),'denominator_imag':float(den.imag)})
 residual=float(np.max(abs(U[:,:27]-T)));unit=float(np.max(abs(U.conj().T@U-np.eye(768))))
 assert residual<1e-12 and unit<1e-12
 return {'register':'8 qubits tensor1 qutrit','rank_one_reflections':reflections,'embedding_error':residual,'unitarity_error':unit,'formula':'H_j=I-v_j v_j^dagger/(v_j^dagger x_j), v_j=x_j-target_j; apply sequentially',
         'scope':'Explicit dense unitary preparation,27 many-body reflections. Not an efficient elementary-gate or fault-tolerant hardware circuit and not an E6 extension.'}

def ggso_negative():
 data=p.string_input();B=np.array(data['boundary_basis_13_by64']);A=np.array(data['GGSO_matrix_13_by13']);M=(A==-1).astype(int)
 rng=np.random.default_rng(12390);fail=[]
 for _ in range(300):
  u=rng.integers(0,2,13);v=rng.integers(0,2,13);a=u@B%2;b=v@B%2
  dot2=int(a[:20]@b[:20]-a[20:]@b[20:]);assert dot2%4==0
  candidate=int((u@M@v+v@M@u)%2);required=(dot2//4)%2
  if candidate!=required:fail.append({'u':u.tolist(),'v':v.tolist(),'candidate_product_sign':(-1)**candidate,'required_sign':(-1)**required})
 assert fail
 return {'sample_pairs':300,'failed_reciprocity':len(fail),'first_counterexample':fail[0],
         'scope':'Rejects naive bilinear GGSO extension even though original basis checks pass. Proper reduced-boundary cocycle and full spin sum remain unbuilt.'}

def global_bound():
 # Finite exact criterion: positive optical block at0 + uniformly positive
 # quadratic acoustic Schur symbol + no nonidentity kernel imply c*d(k,0)^2.
 # This is a compactness consequence, not a computed numerical lower bound.
 return {'claim':'For the specified repaired matched-metric model there exists c>0 with lambda_min_physical(k)>=c*dist(k,2piZ4)^2.',
  'inputs':['Exact all-unitary kernel equality of the positive six-term repair','Positive105-dimensional optical block at identity','Uniform positive quadratic transverse acoustic symbol from positive definite G'],
  'proof':['Near identity eliminate the optical block by an analytic Schur complement. Compactness of the direction sphere and its positive quadratic symbol give a uniform local quadratic lower bound.','Off any small identity neighborhood, the physical gauge quotient has constant dimension108; the exact no-kernel theorem and compactness give a positive minimum.','Combine both constants using bounded torus distance.'],
  'scope':'Conditional on the cited exact native module/Schur-symbol results and their uniform expansion; standard compactness application, not a new computed c. Gauge rank changes at identity; four global holonomies are excluded from the nonidentity statement.'}

if __name__=='__main__':
 out={}
 for name,f in [('overlap',overlap),('preparation',preparation),('GGSO_counterexample',ggso_negative),('global_stiffness_criterion',global_bound)]:
  out[name]=f();print(name,'PASS',flush=True)
 (ROOT/'data/w33_pass12388_12391_constructive_controls.json').write_text(json.dumps(out,indent=2)+'\n')
