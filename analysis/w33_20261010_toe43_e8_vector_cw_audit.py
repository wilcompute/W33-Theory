"""TOE43 front 5: independent gauge-boson one-loop shape audit, SU(9) Lambda^3 84.

The numerical potential is VECTOR-ONLY Coleman-Weinberg shape, without
scalar/fermion/gauge fixing, and NOT a full quantum effective potential.
"""
from pathlib import Path
import sys,json,itertools
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_pass11681_e8_from_two_qutrits as E
OUT=ROOT/"data/w33_20261010_toe43_e8_one_loop_audit.json"
rng=np.random.default_rng(43118)
H=np.array(E.cartan_trivectors())
def generators():
 g=[]
 for i,j in itertools.combinations(range(9),2):
  a=np.zeros((9,9),complex);a[i,j]=1/np.sqrt(2);a[j,i]=-1/np.sqrt(2);g.append(a)
  b=np.zeros((9,9),complex);b[i,j]=1j/np.sqrt(2);b[j,i]=1j/np.sqrt(2);g.append(b)
 for k in range(1,9):
  c=np.zeros((9,9),complex)
  for j in range(k):c[j,j]=1j/np.sqrt(k*(k+1))
  c[k,k]=-1j*k/np.sqrt(k*(k+1))
  g.append(c)
 return np.asarray(g)
G=generators()
assert G.shape==(80,9,9)
# Explicitly verify orthonormal anti-Hermitian generator metric.
metric=np.einsum("aij,bij->ab",G.conj(),G).real
assert np.max(abs(metric-np.eye(80)))<1e-10
def mass(c):
 T=E.full(c@H)
 T=T/np.linalg.norm(T)
 tangent=np.array([E._act(g,T).ravel() for g in G])
 Q=(tangent.conj()@tangent.T).real
 assert np.max(abs(Q-Q.T))<1e-10
 eig=np.linalg.eigvalsh(Q)
 assert min(eig)>-1e-8
 eig=np.maximum(eig,0)
 squares=eig**2
 cw=float(np.sum(np.where(eig>1e-12,squares*np.log(np.maximum(eig,1e-300)),0.)))
 return eig,{"unbroken_gauge_bosons":int(sum(eig<1e-9)),
             "trace_mass_squared_proxy":float(sum(eig)),
             "trace_mass_fourth_proxy":float(sum(squares)),
             "cw_vector_log_shape":cw,
             "positive_gap":float(min(eig[eig>1e-9])),
             "smallest_eigenvalues":eig[:5].tolist(),
             "largest_eigenvalues":eig[-5:].tolist()}
basis=[np.eye(4,dtype=complex)[i] for i in range(4)]
generic=[(rng.normal(size=4)+1j*rng.normal(size=4)) for i in range(8)]
cases={}
for i,c in enumerate(basis+generic):
 vals,row=mass(c)
 cases[("witting_"+str(i)) if i<4 else ("generic_"+str(i-4))]=row
 print("CW",list(cases)[-1],row["unbroken_gauge_bosons"],
       round(row["trace_mass_fourth_proxy"],9),
       round(row["cw_vector_log_shape"],9),flush=True)
ref=list(cases.values())[0]
trace_spread_2=max(x["trace_mass_squared_proxy"] for x in cases.values())-min(x["trace_mass_squared_proxy"] for x in cases.values())
trace_spread_4=max(x["trace_mass_fourth_proxy"] for x in cases.values())-min(x["trace_mass_fourth_proxy"] for x in cases.values())
cw_spread=max(x["cw_vector_log_shape"] for x in cases.values())-min(x["cw_vector_log_shape"] for x in cases.values())
assert trace_spread_2<1e-8 and trace_spread_4<1e-8
assert all(cases["witting_"+str(i)]["unbroken_gauge_bosons"]==24 for i in range(4))
assert all(cases["generic_"+str(i)]["unbroken_gauge_bosons"]==0 for i in range(8))
assert cw_spread>1e-6
out={"status":"PASS_VECTOR_ONLY_ONE_LOOP_SHAPE_VARIES",
"representation":"su(9) compact gauge generators acting on Lambda^3 C^9, normalized Cartan vevs",
"generator_count":80,"cartan_dimension_complex":4,
"mass_matrix":"Q_ab=Re <A_a . T, A_b . T>, generator norm Tr(A_a^dag A_b)=delta_ab",
"witting_massless_gauge_bosons":24,"generic_massless_gauge_bosons":0,
"trace_Q_spread_across_samples":trace_spread_2,
"trace_Q2_spread_across_samples":trace_spread_4,
"cw_log_shape_spread":cw_spread,"cases":cases,
"one_loop_vector_only_formula":"V1_vector=(3/(64 pi^2))*sum_a m_a^4*(log(m_a^2/mu^2)-5/6) with m_a^2=proportional_to g^2 |v|^2 e_a. Shape variation from sum e_a^2 log(e_a) even when sum e_a^2 is constant.",
"interpretation":"The degree-12 lowest holomorphic invariant does not prohibit radiative vector-loop dependence on the genus-two Cartan modulus at effective dimension four (logs). Claimed generic physical phase stays flat until dimension12 requires an extra cancellation or symmetry.",
"boundary":"This is vector-boson shape only; not an SU9+84 complete Coleman-Weinberg potential. Gauge dependence, scalar/ghost terms, RG running, fermions, dark-vs-visible embedding, CP selection and vacuum metastability remain unproved."}
OUT.write_text(json.dumps(out,indent=2)+"\n")
print("SUMMARY",json.dumps({k:out[k] for k in ("status","cw_log_shape_spread","trace_Q2_spread_across_samples")}),flush=True)
