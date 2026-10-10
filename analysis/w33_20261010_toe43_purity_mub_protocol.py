"""TOE43 front 2: native W33 ten-setting unbiased purity witness.

Construct 10 MUB stabilizer bases from a symplectic line spread of W(3,3).
Two independent outcomes per setting give a collision (U-statistic) unbiased
for Tr rho^2. Calibrated uniform 9-outcome readout model included.
"""
from pathlib import Path
import itertools,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261010_toe43_purity_shots.json"
w=np.exp(2j*np.pi/3);I3=np.eye(3,dtype=complex);I9=np.eye(9,dtype=complex)
X=np.roll(I3,1,axis=0);Z=np.diag([1,w,w*w])
F=range(3);vs=list(itertools.product(F,repeat=4))
canon=lambda v:min(v,tuple(-t%3 for t in v))
pts=sorted({canon(v) for v in vs if any(v)});lookup={v:i for i,v in enumerate(pts)}
symp=lambda a,b:(a[0]*b[2]+a[1]*b[3]-a[2]*b[0]-a[3]*b[1])%3
W=[np.kron(np.linalg.matrix_power(X,v[0])@np.linalg.matrix_power(Z,v[2]),
           np.linalg.matrix_power(X,v[1])@np.linalg.matrix_power(Z,v[3])) for v in pts]
lines=set()
for i,p in enumerate(pts):
 for j,q in enumerate(pts[i+1:],start=i+1):
  if symp(p,q):continue
  line=frozenset(lookup[canon(tuple((a*p[k]+b*q[k])%3 for k in range(4))) ]
                 for a,b in itertools.product(F,repeat=2) if a or b)
  assert len(line)==4
  lines.add(tuple(sorted(line)))
lines=sorted(lines);assert len(lines)==40
bypt={k:[i for i,L in enumerate(lines) if k in L] for k in range(40)}
def findspread(used,ids):
 if len(ids)==10:return ids if used==(1<<40)-1 else None
 for p in range(40):
  if not used>>p&1:
   break
 for k in bypt[p]:
  mask=sum(1<<v for v in lines[k])
  if used&mask:continue
  ans=findspread(used|mask,ids+[k])
  if ans is not None:return ans
 return None
spread=findspread(0,[])
assert len(spread)==10
def proj(A,lab):
 return (I9+sum(w**(-lab*k)*np.linalg.matrix_power(A,k) for k in (1,2)))/3
POV=[];EVAL=[]
for line_no in spread:
 L=lines[line_no]
 a=pts[L[0]]
 b=next(pts[i] for i in L[1:] if pts[i]!=a and pts[i]!=canon(tuple(-x%3 for x in a)))
 # Four canonical points: ANY two distinct span line over F3
 A=W[L[0]]
 B=W[lookup[b]]
 assert np.max(abs(A@B-B@A))<1e-10
 ops=np.stack([proj(A,j)@proj(B,k) for j,k in itertools.product(F,repeat=2)])
 assert np.max(abs(np.sum(ops,axis=0)-I9))<1e-10
 assert max(abs(np.trace(P)-1) for P in ops)<1e-10
 ev=np.array([[np.trace(W[p]@M) for M in ops] for p in L])
 assert np.max(abs(abs(ev)-1))<1e-10
 POV.append(ops);EVAL.append(ev)
for i,j in itertools.combinations(range(10),2):
 assert np.max(abs(np.einsum("aij,bji->ab",POV[i],POV[j]).real-1/9))<1e-9
rng=np.random.default_rng(43002)
psi=np.zeros(9,dtype=complex);psi[0]=1
rho=np.outer(psi,psi.conj())
mix=np.eye(9)/9
states={"stabilizer":rho,"maximally_mixed":mix,
        "half_depolarized":.5*rho+.5*mix}
def exact(state):
 p=np.array([np.real(np.einsum("aij,ji->a",ops,state)) for ops in POV])
 assert np.max(abs(np.sum(p,axis=1)-1))<1e-10
 collisions=np.sum(p*p,axis=1)
 pur=float(np.trace(state@state).real)
 assert abs(np.sum(collisions)-1-pur)<1e-10
 return p,collisions,pur
# Draw independent pairs m per measurement setting. Each setting m pairs => 20*m shots total.
m=160;repeats=1500;noise=.05
results={}
for label,state in states.items():
 probs,collisions,purity=exact(state)
 cases={}
 for eps in (0.,noise):
  probs_obs=np.clip((1-eps)*probs+eps/9,0,None)
  probs_obs=probs_obs/np.sum(probs_obs,axis=1,keepdims=True)
  coll_obs=np.sum(probs_obs*probs_obs,axis=1)
  cv=1/9
  t=(1-eps)**2
  values=np.zeros(repeats)
  for j,p in enumerate(probs_obs):
   A=rng.choice(9,size=(repeats,m),p=p)
   B=rng.choice(9,size=(repeats,m),p=p)
   values+=np.mean(A==B,axis=1)
  est=(values-10*cv)/t+cv
  predicted_var=float(np.sum(coll_obs*(1-coll_obs))/m/t**2)
  observed_var=float(np.var(est,ddof=1))
  cases[str(eps)]={
    "mean":float(np.mean(est)),"true_purity":purity,
    "predicted_standard_error":float(np.sqrt(predicted_var)),
    "monte_carlo_standard_error":float(np.sqrt(observed_var)),
    "calibration":"9-outcome symmetric white-confusion eps; known eps required",
    "pairs_per_basis":m,"number_of_bases":10,"total_copies":20*m,
    "mean_error":float(np.mean(est)-purity),
    "ideal_entangling_swap_test_se_same_copy_budget":float(np.sqrt((1-purity**2)/(10*m))) if eps==0 else None}
  assert abs(np.mean(est)-purity)<.02
  assert .7<observed_var/predicted_var<1.3
 results[label]=cases
# Identity linking all four projective Pauli q's and the collision event.
for j,(ops,ev) in enumerate(zip(POV,EVAL)):
 for k in range(9):
  for l in range(9):
   val=float(np.sum(2*(ev[:,k]*ev[:,l].conj()).real))
   assert abs(val-(9*int(k==l)-1))<1e-9
out={"status":"PASS_UNBIASED_TEN_MUB_PURITY_EXPERIMENT_SIMULATOR",
"complete_W33_line_count":len(lines),"projective_paulis":40,
"chosen_symplectic_spread_line_indices":spread,
"line_point_sets":[list(lines[i]) for i in spread],
"counts":{"MUB_settings":10,"projective_pauli_classes_per_setting":4,"outcomes_per_setting":9},
"simulator":{"m_pairs_per_setting":m,"Monte_Carlo_repetitions":repeats,"readout_confusion_epsilon":noise,
"total_copies_per_trial":20*m},"states":results,
"unbiased_pairwise_estimator":"P_hat=sum_{b=1}^{10} mean_{pairs} 1[outcome1==outcome2] -1 at eps=0",
"calibrated_estimator":"P_hat=1/9+(sum_b pair_collision_mean_b -10/9)/(1-eps)^2",
"state_purity_identity":"sum_{b,j}p_{bj}^2=1+Tr(rho^2); sum_{p in line}q_p=9*collision_probability-1",
"variance_model":"For independent disjoint pairs: Var(P_hat)=sum_b c_b(1-c_b)/(m*(1-eps)^4).",
"boundary":"Assumes trusted MUB implementation, calibrated symmetric classical readout and independent copies. No lab hardware, SPAM drift or uncalibrated noise immunity."}
OUT.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"spread":spread,
 "stabilizer_clean":results["stabilizer"]["0.0"],"mixed_clean":results["maximally_mixed"]["0.0"]}))
