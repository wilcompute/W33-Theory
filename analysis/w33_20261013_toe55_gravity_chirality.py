"""TOE55 controlled spin-2 constraint benchmark and SM anomaly nonuniqueness.

Spin-2 is the STANDARD continuum linearized Fierz-Pauli comparison,
not a W33 gravitational construction.
"""
from pathlib import Path
import sympy as sp,json
from fractions import Fraction
R=Path(__file__).resolve().parents[1]
k=sp.Matrix(sp.symbols("k0 k1 k2",real=True))
pairs=[(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]
k2=sum(k[i]**2 for i in range(3))
# One scalar Hamiltonian constraint on symmetric spatial h_ab.
ham=sp.Matrix(1,6,lambda i,j:(k[pairs[j][0]]**2-k2) if j<3
              else 2*k[pairs[j][0]]*k[pairs[j][1]])
# Three momentum constraints C_i=k_j pi_ij, using canonical
# p=(pi_00,pi_11,pi_22,2pi_01,2pi_02,2pi_12).
mom=sp.zeros(3,6)
for i in range(3):
 for col,(a,b) in enumerate(pairs):
  if a==b==i:mom[i,col]=k[i]
  elif a!=b and a==i:mom[i,col]=k[b]/2
  elif a!=b and b==i:mom[i,col]=k[a]/2
bracket=sp.simplify(ham*mom.T)
assert bracket==sp.zeros(1,3)
# Whole 4x4 linearized constraint matrix zero, since H depends
# only on h and momentum constraints only on p.
for q in [[1,2,3],[2,-1,4],[1,0,0]]:
 c=[int(x) for x in q]
 kh=ham.subs(dict(zip(k,c)))
 km=mom.subs(dict(zip(k,c)))
 assert kh.rank()==1 and km.rank()==3
 # Gauge-fixed physical phase space = 12 - 2*4 = 4:
 # 2 independent configuration degrees of freedom.
# Geometric TT projector on spatial symmetric 3x3 tensors.
ks=sp.Matrix([1,2,3])
S=sp.eye(3)-ks*ks.T/(ks.dot(ks))
def tt(H):
 Q=S*H*S
 return sp.simplify(Q-S*sp.trace(Q)/2)
basis=[]
for a,b in pairs:
 H=sp.zeros(3);H[a,b]=1;H[b,a]=1
 basis.append(tt(H))
columns=sp.Matrix.hstack(*[sp.Matrix(list(M)) for M in basis])
assert columns.rank()==2
assert all((ks.T@M)==sp.zeros(1,3) and sp.trace(M)==0 for M in basis)
# Differentiate a gauge shift delta h_ab=k_a xi_b+k_b xi_a.
for i in range(3):
 x=sp.eye(3)[:,i]
 g=ks*x.T+x*ks.T
 assert tt(g)==sp.zeros(3)
grav={"status":"PASS_LINEARIZED_SPIN2_CONSTRAINT_POSITIVE_CONTROL",
"model":"Continuum massless spin2 linearized Fierz-Pauli; independent benchmark NOT derived from W33",
"canonical_spatial_h_components":6,"canonical_pi_components":6,
"linearized_H_constraint_gradient":str(list(ham)),
"momentum_constraint_gradient":"C_i=k_j*pi_ij; offdiagonal canonical p_ij=2*pi_ij",
"analytic_H_vs_momentum_poisson_bracket_matrix":str(bracket),
"constraint_classification":"4 linearly independent first-class constraints for every nonzero 3-vector k",
"phase_space_count":"12-2*4=4 physical real phase dimensions, two configuration polarizations",
"TT_projector_rank_at_k_1_2_3":int(columns.rank()),
"TT_gauge_shift_exactly_zero":True,
"native_W33_gravity_status":"NO map, action or Poisson-closed nonlinear Hamiltonian/diffeomorphism constraint algebra of this type exists in this certificate. TOE51 native Maxwell+160 metric scalar pairs still retains scalar oscillators and cannot be called gravity.",
"prior_art":"Standard massless Fierz-Pauli canonical linearized GR, not novel spin-two physics."}
(R/"data/w33_20261013_toe55_linear_spin2_constraints.json").write_text(json.dumps(grav,indent=2)+"\n")
print("GRAVITY",grav["status"],"TT",columns.rank(),flush=True)
# Anomaly audit all fields LEFT HANDED; verify continuous hypercharge
# Y + t(B-L) family with sterile right-neutrino conjugate nu^c.
t=sp.Symbol("t",real=True)
f=[
 ("Q",3,2,1,sp.Rational(1,6),sp.Rational(1,3)),
 ("u_c",3,1,-1,sp.Rational(-2,3),sp.Rational(-1,3)),
 ("d_c",3,1,-1,sp.Rational(1,3),sp.Rational(-1,3)),
 ("L",1,2,0,sp.Rational(-1,2),sp.Integer(-1)),
 ("e_c",1,1,0,sp.Integer(1),sp.Integer(1)),
 ("nu_c",1,1,0,sp.Integer(0),sp.Integer(1))
]
# sign nonabelian anomaly coefficient 3 -> +1, 3bar -> -1.
a3=sum(wk*sgn for _,col,wk,sgn,y,bl in f if col==3)
a32Y=sp.expand(sum(wk*sp.Rational(1,2)*(y+t*bl) for _,col,wk,sgn,y,bl in f if col==3))
a22Y=sp.expand(sum(col*sp.Rational(1,2)*(y+t*bl) for _,col,wk,sgn,y,bl in f if wk==2))
agrav=sp.expand(sum(col*wk*(y+t*bl) for _,col,wk,sgn,y,bl in f))
aY3=sp.expand(sum(col*wk*(y+t*bl)**3 for _,col,wk,sgn,y,bl in f))
counts=sum(col for _,col,wk,sgn,y,bl in f if wk==2)
assert (a3,a32Y,a22Y,agrav,aY3)==(0,0,0,0,0)
assert counts==4
# Check charge changes in low-energy scalar Higgs Y_H=+1/2,
# B-L(H)=0, so unbroken electric Q=T3+Y'.
neutrino_charge=sp.expand(sp.Rational(1,2)+sp.Rational(-1,2)-t)
assert neutrino_charge==-t
case=sp.Rational(1,7)
assert neutrino_charge.subs(t,case)==-sp.Rational(1,7)
# A deliberately perturbed single hypercharge ruins cancellation.
perturb=sp.Rational(1,6)
bad_22=sp.simplify(a22Y+3*perturb/2)
assert bad_22==sp.Rational(1,4)
anomalies={"status":"PASS_ANOMALY_FREE_HYPERCHARGE_CONTINUOUS_DEFORMATION",
"left_handed_fields":[{"field":name,"su3_dimension":col,"su2_dimension":wk,
 "su3_cubic_chirality":sgn,"hypercharge_Y":str(y),"B_minus_L":str(bl)}
 for name,col,wk,sgn,y,bl in f],
"hypercharge_family":"Y(t)=Y_SM+t*(B-L), with left-handed nu_c included",
"SU3_cubic_anomaly":str(a3),"SU3_sq_U1_anomaly":str(a32Y),
"SU2_sq_U1_anomaly":str(a22Y),"gravitational_U1_anomaly":str(agrav),
"U1_cubed_anomaly":str(aY3),
"SU2_Witten_doublet_count":counts,"SU2_Witten_even":counts%2==0,
"nonstandard_t":str(case),"nonstandard_neutrino_electric_charge":str(neutrino_charge.subs(t,case)),
"control_shift_only_Q_hypercharge":str(perturb),
"control_SU2_sq_U1_anomaly_nonzero":str(bad_22),
"result":"Anomaly cancellation plus this selected SM+nu_c representation list DOES NOT fix the physical hypercharges: continuous anomaly-free Y+t(B-L). Observational charge quantization and additional group/UV input must select t=0. This is not a new result about SM; it is a W33 project selection gate.",
"derivation_scope":"Source fields taken as known Standard Model+sterile nu_c, not derived from W33 40 graph. Chiral gauge lattice regulator or observed neutrino electric charge not derived here.",
"prior_art":"Textbook SM anomaly cancellation and anomaly-free B-L with three sterile neutrinos; global Witten SU2 even-doublet check."}
(R/"data/w33_20261013_toe55_anomaly_deformation.json").write_text(json.dumps(anomalies,indent=2)+"\n")
print("ANOMALY",anomalies["status"],"all polynomial zero, neutrino Q(t)=",neutrino_charge,flush=True)
