"""TOE62 exact continuous U(1) high-temperature flux theorem.

THEOREM: the *leading beta^7* fermion free-energy term has a unique
GLOBAL minimum on the entire continuous three-holonomy torus at
(pi,pi,pi), not merely the eight Z2 corners. An analytic positive
Hessian + compact uniform remainder proves same for all sufficiently
small beta>0 (not explicit beta cutoff).
"""
from pathlib import Path
import ast,json,sys,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'analysis'))
from w33_20261010_toe38_local_maxwell_2complex import prep
cert=json.loads((R/'data/w33_20261013_toe59_eight_cycle_census.json').read_text())
counts={ast.literal_eval(k):int(v) for k,v in cert['integral_voltage_winding_counts'].items()}
counts.pop((0,0,0))
# Sign/orientation of winding does not matter to cos.
def folded_key(w):
 w=tuple(w)
 return min(w,tuple(-x for x in w))
freq={}
for w,n in counts.items():
 key=folded_key(w);freq[key]=freq.get(key,0)+n
# Nonzero 8-cycle winding Fourier polynomial:
# 79 cos phi0 +77 cos phi1 +77 cos phi2 +
# 1 cos(phi0+phi1)+1 cos(phi0+phi2)+3 cos(phi1-phi2).
expected={(1,0,0):79,(0,1,0):77,(0,0,1):77,
          (1,1,0):1,(1,0,1):1,(0,1,-1):3}
assert sum(freq.values())==238
assert freq=={folded_key(k):n for k,n in expected.items()},(freq,expected)
def S(phi):
 return float(sum(v*np.cos(np.dot(w,phi)) for w,v in freq.items()))
pi=np.full(3,np.pi)
S_pi=S(pi);S_0=S(np.zeros(3))
assert np.isclose(S_pi,-228) and np.isclose(S_0,238)
# Proof: δ=phi-pi, for any +/-,
# 1-cos(δi±δj) <=2(1-cosδi)+2(1-cosδj).
# Singles cost (79,77,77) times (1-cosδ).
# Cross harmonics weights 1 on (0,1),(0,2),3 on (1,2).
# Each crossed term can reduce cost by at most 2*w per end.
lower_coeff=np.array([79-2*(1+1),77-2*(1+3),77-2*(1+3)])
assert lower_coeff.tolist()==[75,69,69]
rng=np.random.default_rng(62062)
min_margin=1e10
for phi in rng.uniform(-np.pi,np.pi,size=(3000,3)):
 delta=phi-pi;L=float(lower_coeff@(1-np.cos(delta)))
 margin=S(phi)-S_pi-L
 min_margin=min(min_margin,margin)
 assert margin>-1e-10,(phi,margin)
# Check actual native 80x80 trace-H8 matches 16*(Sphi-S0).
ed,v,*_=prep();E=np.asarray(ed,int);V=np.asarray(v,int)
def trace8(phi):
 H=np.zeros((80,80),complex)
 z=np.exp(1j*(V@phi))
 for k,(a,b) in enumerate(E):
  H[a,b]=-z[k];H[b,a]=-np.conj(z[k])
 H2=H@H;H4=H2@H2
 return float(np.trace(H4@H4).real)
t0=trace8(np.zeros(3))
tests=[]
for theta in [pi,rng.uniform(-np.pi,np.pi,3),rng.uniform(-np.pi,np.pi,3)]:
 observed=trace8(theta)-t0
 expectedtrace=16*(S(theta)-S_0)
 assert abs(observed-expectedtrace)<1e-6,(observed,expectedtrace)
 tests.append({'theta':theta.tolist(),'trace8_delta':observed,'Fourier_predicted_delta':expectedtrace})
coef=17/40320
assert abs(coef*(S_pi-S_0)-(-.1964781746031746))<1e-13
out={'status':'PASS_TOE62_GLOBAL_CONTINUOUS_U1_LEADING_BETA7_MINIMUM',
'exact_integer_winding_Fourier_coefficients':{str(k):v for k,v in sorted(freq.items())},
'S_pi_pi_pi':S_pi,'S_zero':S_0,'rigorous_cosine_distance_lower_coefficients':lower_coeff.tolist(),
'trace_H8_crosschecks':tests,
'leading_deltaF_beta7_pi_vs_zero':coef*(S_pi-S_0),
'theorem':"For the native 80-site spinless nearest-neighbor free fermion with flat harmonic U1 parameters phi∈(R/2πZ)^3, the winding-dependent eighth adjacency moment is TrH(phi)^8=const+16 S(phi). Native octagon census gives S=79cos(phi0)+77cos(phi1)+77cos(phi2)+cos(phi0+phi1)+cos(phi0+phi2)+3cos(phi1-phi2). Writing δ=phi-(pi,pi,pi), use 1-cos(x±y)<=2[(1-cos x)+(1-cos y)] to obtain S(phi)-S(pi,pi,pi)>=75(1-cosδ0)+69(1-cosδ1)+69(1-cosδ2)>=0, equality only at the three-pi corner modulo2π. Fermion F_beta(phi)=-beta^-1 Tr log[2cosh(beta Hphi/2)] and its first phi-dependent term is +(17 beta^7/40320) S(phi). Thus the leading beta7 term is globally, uniquely minimized on the ENTIRE continuous U1 harmonic torus at three-pi.",
'qualifier_small_beta':"The finite-dimensional spectral high-temperature expansion and its first two phi-derivatives converge uniformly for sufficiently small beta. The leading cost has a nondegenerate Hessian at pi and a positive gap outside each neighborhood; pi is a stationary point at every beta by conjugation/periodicity. A standard compactness + C²-perturbation argument therefore gives existence of an unspecified beta0>0 for which pi is the UNIQUE global minimizer for all 0<beta<beta0. This does NOT determine beta0 or prove all-temperature continuous U1 minimization.",
'numeric_random_cosine_lower_bound_min_slack':min_margin,
'model_boundary':"This is an exact theorem for the high-temperature leading term of ONE supplied static bipartite 80-site hopping Hamiltonian and native 3-holonomy family. It is NOT a theorem for arbitrary U1 gauge connections (with local curvature), finite beta all-temperature continuum flux, interacting fermions, gauge dynamics, physical CKM CP, or measured parameters. TOE61 already owns an all-beta theorem ONLY among eight Z2 corners."}
(R/'data/w33_20261013_toe62_leading_flux_theorem.json').write_text(json.dumps(out,indent=2)+'\n')
print('TOE62 global beta7',freq,'lower',lower_coeff,'coef',out['leading_deltaF_beta7_pi_vs_zero'],flush=True)
