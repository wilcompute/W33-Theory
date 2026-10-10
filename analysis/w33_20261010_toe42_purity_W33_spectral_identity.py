"""TOE42: exact W33 adjacency spectral formula for all-frame two-qutrit purity variance.

This refines TOE41's constant mean by deriving the nonconstant variance
via the *actual* W(3,3) point graph, with exact integer Gram identity:
90x40 incidence H of nondegenerate symplectic planes satisfies
H^T H = 8 I + J - A_W33.

For pure two-qutrit |psi>, projective Pauli powers q_p=2 |<psi|W_p|psi>|²,
sum(q)=8. The variance over all 90 virtual one-qutrit factors is
Var purity = [||P_{lambda=2} q||²+2||P_{lambda=-4} q||²]/135.
"""
import itertools,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261010_toe40_four_controls import theta
OUT=ROOT/"data/w33_20261010_toe42_w33_purity_variance_spectral.json"
F=range(3)
V=list(itertools.product(F,repeat=4))
neg=lambda v:tuple(-t%3 for t in v)
canon=lambda v:min(v,neg(v))
sp=lambda x,y:(x[0]*y[2]+x[1]*y[3]-x[2]*y[0]-x[3]*y[1])%3
pts=sorted({canon(v) for v in V if any(v)});pos={v:i for i,v in enumerate(pts)}
assert len(pts)==40
A=np.array([[int(i!=j and sp(x,y)==0) for j,y in enumerate(pts)] for i,x in enumerate(pts)],dtype=np.int64)
J=np.ones((40,40),dtype=np.int64);I=np.eye(40,dtype=np.int64)
assert np.all(A.sum(1)==12)
assert np.array_equal(A@A,12*I+2*A+4*(J-I-A))
planes=set()
for i,p in enumerate(pts):
 for q in pts[i+1:]:
  if sp(p,q)==0:continue
  pl=frozenset(canon(tuple((a*p[t]+b*q[t])%3 for t in range(4)))
               for a,b in itertools.product(F,repeat=2) if a or b)
  assert len(pl)==4
  planes.add(tuple(sorted(pos[v] for v in pl)))
planes=sorted(planes);assert len(planes)==90
H=np.zeros((90,40),dtype=np.int64)
for j,p in enumerate(planes):H[j,list(p)]=1
assert np.array_equal(H.T@H,8*I+J-A)
assert np.array_equal(H.sum(axis=1),np.full(90,4))
assert np.array_equal(H.sum(axis=0),np.full(40,9))
P2=-((A-12*I)@(A+4*I))/60
Pm=((A-12*I)@(A-2*I))/96
Pconst=J/40
assert np.max(abs(P2@P2-P2))<1e-12
assert np.max(abs(Pm@Pm-Pm))<1e-12
assert np.max(abs(P2@Pm))<1e-12
assert np.max(abs(P2+Pm+Pconst-I))<1e-12
assert round(np.trace(P2))==24 and round(np.trace(Pm))==15
w=np.exp(2j*np.pi/3);single=np.eye(3,dtype=complex)
X=np.roll(single,1,axis=0);Z=np.diag([1,w,w*w])
W=[np.kron(np.linalg.matrix_power(X,v[0])@np.linalg.matrix_power(Z,v[2]),
           np.linalg.matrix_power(X,v[1])@np.linalg.matrix_power(Z,v[3])) for v in pts]
def eval_case(C):
 psi=np.array(C,dtype=complex).reshape(9)
 psi/=np.linalg.norm(psi)
 q=np.array([2*abs(np.vdot(psi,M@psi))**2 for M in W])
 assert abs(sum(q)-8)<1e-10
 pur=(1+H@q)/3
 direct=float(np.var(pur))
 v2=float(np.dot(q,P2@q))
 vm=float(np.dot(q,Pm@q))
 spectral=(v2+2*vm)/135
 assert abs(spectral-direct)<1e-12,(spectral,direct)
 assert abs(float(np.mean(pur))-.6)<1e-12
 return dict(mean=float(np.mean(pur)),variance=direct,
   variance_from_W33_eigenspaces=float(spectral),norm_squared_lambda2=v2,
   norm_squared_lambda_minus4=vm,pauli_power_min=float(min(q)),pauli_power_max=float(max(q)))
rng=np.random.default_rng(42)
cases=dict(
 stabilizer_00=eval_case(np.eye(3,dtype=complex)[0][:,None]@np.eye(3,dtype=complex)[0][None,:]),
 theta_product=eval_case(theta(.173+1.07j,.286+1.29j,0)),
 theta_coupled=eval_case(theta(.173+1.07j,.286+1.29j,.12)),
 random_pure=eval_case(rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))))
assert abs(cases["stabilizer_00"]["variance"]-8/75)<1e-12
max_pminus_norm=0.;max_pure_graph_defect=0.
for _ in range(50):
 z=rng.normal(size=9)+1j*rng.normal(size=9);z/=np.linalg.norm(z)
 q=np.array([2*abs(np.vdot(z,M@z))**2 for M in W])
 max_pminus_norm=max(max_pminus_norm,float(np.linalg.norm(Pm@q)))
 max_pure_graph_defect=max(max_pure_graph_defect,float(np.max(abs(A@q-2*q-2))))
assert max_pminus_norm<1e-10,max_pminus_norm
assert max_pure_graph_defect<1e-10,max_pure_graph_defect
# A genuinely mixed diagonal ensemble need not obey rank-one identities.
rho=np.diag([.6,.4]+[0]*7)
q_mixed=np.array([2*abs(np.trace(rho@M))**2 for M in W])
mixed_minus_norm=float(np.linalg.norm(Pm@q_mixed))
mixed_residual=A@q_mixed-2*q_mixed-2
assert np.max(mixed_residual)<1e-10
assert abs(np.sum(mixed_residual)-90*(np.trace(rho@rho).real-1))<1e-10
assert mixed_minus_norm>.1
q_stab=np.array([2*abs(Wp[0,0])**2 for Wp in W])
assert abs(np.sum(q_stab**2)-16)<1e-12
print("PURE FORBIDDEN MINUS",max_pminus_norm,"MIXED FORBIDDEN MINUS",mixed_minus_norm,flush=True)
out=dict(status="EXACT_INTEGER_INCIDENCE_AND_NUMERIC_PURITY_SPECTRAL_CERTIFIED",
 incidence_shape=[90,40],
 W33_A_spectrum={"12":1,"2":24,"-4":15},
 gram_formula="H.T@H=8I+J-A_W33",
 mean_purity="3/5",
 exact_variance_formula="Pure-state: (sum_p q_p^2 - 8/5)/135 = ||q-(1/5)1||^2/135; general 40-vector variance is (||P_2 q||^2+2||P_-4 q||^2)/135 if sum q=8",
 forbidden_minus_pure_max_norm_from_50_random=max_pminus_norm,
 pure_graph_identity_max_residual_50_random=max_pure_graph_defect,
 mixed_example_minus_norm=mixed_minus_norm,
 mixed_example_tr_rho2=float(np.trace(rho@rho).real),
 mixed_example_all_40_graph_deficits_nonpositive=True,
 mixed_exact_deficit_sum_minus_90_one_minus_tr_rho2=float(np.sum(mixed_residual)),
 pure_max_variance_bound="8/75, attained iff four q_p=2 and other q_p=0 (a two-qutrit stabilizer state)",
 pure_min_variance_bound="0, attained iff all 40 q_p=1/5 (a SIC fiducial for the elementary-abelian two-qutrit Pauli group IF such a fiducial exists)",
 state_purity_theorem="For every density matrix rho, (Aq-2q-2)_p=9 sum_j [Tr((Pi_j rho Pi_j)^2)-(Tr Pi_j rho)^2] <=0, where Pi_j are three rank-3 spectral projectors of W_p; equality for all 40 p iff rho is pure. Sum of all 40 deficits = 90(Tr rho^2-1).",
 projective_pauli_q="q_p=2*abs(<psi|W_p|psi>)**2; sum_p q_p=8 for every pure two-qutrit state",
 cases=cases,
 interpretation="The first nonconstant full-Clifford-frame purity statistic is exactly a weighted two-eigenspace W33 graph Fourier energy. Not a complete Siegel invariant; not a physical vacuum or magic monotone proof.",
 prior="TOE41 averaged 90 virtual factor purities to 3/5 and observed varying variance, but did not identify the exact W33 adjacency functional.",
 boundary="Cannot identify unmarked theta moduli as physical vacua or claim that this functional is invariant under full Sp(4,Z) with automorphy multipliers.")
OUT.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out))
