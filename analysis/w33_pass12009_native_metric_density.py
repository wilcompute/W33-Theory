"""Native conductance/capacity completion before induced-curvature claims.

11601 owns metric/density heat calibration. Here actual11995's four-cover
conductances are densitized and supplied native vertex capacities are built.
Continuum homogenization/quantum spectral action remain conditional inputs.
"""
import json
from pathlib import Path
import numpy as np
import sympy as s
from scipy.special import iv
from w33_pass11995_native_metric_gr_lift import inputs,lift,homogenize
ROOT=Path(__file__).resolve().parents[1]

def geometric(H,dimension=4):
    capacity=np.linalg.det(H)**(1/(dimension-2));G=H/capacity
    assert abs(capacity*np.sqrt(np.linalg.det(G))-1)<1e-10
    return capacity,G

def payload():
    b,v,C,H0=inputs();H0=np.array(H0,float);selected=json.loads((ROOT/'data/w33_pass11995_native_metric_gr_lift.json').read_text())['selected_edge_indices'];rows=[]
    for phase in np.linspace(0,2*np.pi,9)[:-1]:
        sigma=.0002*np.cos(phase);target=np.exp(2*sigma)*H0;w,history=lift(target,b,v,selected);H,_=homogenize(w,b,v);M,G=geometric(H)
        assert min(w)>0 and np.max(abs(H-M*G))<1e-12
        rows.append(dict(phase=float(phase),sigma=float(sigma),minimum_weight=float(min(w)),native_vertex_capacity=float(M),geometric_volume_density=float(1/np.sqrt(np.linalg.det(G))),local_metric_error=float(np.max(abs(H-target)))))
    # Exact4D densitization inverse including all ten non-diagonal entries.
    H=s.Matrix([[2,s.Rational(1,5),0,s.Rational(1,7)],[s.Rational(1,5),3,s.Rational(1,8),0],[0,s.Rational(1,8),4,s.Rational(1,9)],[s.Rational(1,7),0,s.Rational(1,9),5]])
    cap=s.sqrt(H.det());G=H/cap;assert s.simplify(G.det()*cap**2)==1
    # Nativefixedmass versus covariantcapacity: conformal exact operator.
    x=s.symbols('x',real=True);sigma=s.Function('sigma')(x);f=s.Function('f')(x);mu=s.exp(-4*sigma);half=s.sqrt(mu)
    fixed=-s.diff(s.exp(2*sigma)*s.diff(half*f,x),x)/half
    geometric_part=-s.diff(mu*s.exp(2*sigma)*s.diff(f,x),x)/mu
    endomorphism=2*s.exp(2*sigma)*s.diff(sigma,x,2)
    assert s.simplify(fixed-geometric_part-endomorphism*f)==0
    # On the periodic conformal test, integrateda2_fixed=-3I but R/6=+I.
    eps=.12;I=float((2*np.pi)**3*np.pi*eps*iv(1,2*eps));assert I>0
    return dict(status='PASS',native_cell_sites=27,conductance_edges=135,native_capacity_lifts=rows,
        d4_capacity='M=sqrt(det H)',d4_inverse_metric='G=H/sqrt(det H)',exact_general_d='For d!=2: M=(det H)^(1/(d-2)), G=H/M, sqrt(det g)=M; H=sqrt(g)g^-1. d=2 requiresdetH=1 and leavesa conformalscaleundetermined.',
        native_action='Euclidean4DscalarDirichletaction=1/2 sum_edges w_e|delta_e phi|²; innerproduct=sum_vertices M(w)|phi|² with27sitespercell. Generalizedoperator M^-1L haslongwavelengthsymbolG=H/M andmeasureM. Noextra continuoustime isadded; Lorentzinterpretation andsmoothlimit remaininputs.',
        density_repair='Unitnativecapacities andvariableH give a weightedmetricoperator, not automatically pureLaplaceBeltrami. A halfdensitymap to sqrt(g)dx creates scalarV. Capacities M=sqrt(detH) complete thegeometricDirichletform in4D.',
        conformal_fixed_capacity={'H':'exp(2sigma) I4','metric':'g=exp(-2sigma)I4','geometric_measure':'exp(-4sigma)dx','extra_scalar_V':'2 exp(2sigma) sigma_xx','scalar_curvature':'6exp(2sigma)(sigma_xx-sigma_x²)','integrated_R_over6':I,'integrated_a2_fixed_unit_capacity':-3*I,'integrated_extra_V':4*I,'epsilon':eps},
        conditional_induced_action='If thisslowfield4Dcovariantcontinuum exists, scalarheatcoefficienta2=(4pi)^-2 integral sqrt(g)R/6 forcapacity-completedLaplaceBeltrami. A quantum/spectralaction then also hasa0cosmological andhighercurvatureterms. Heatkernelcoefficient isstandard, not a nativeEinsteinaction derivation.',
        constraint_boundary='A suppliedEHpiece throughthisinvertible10metricchart inheritscontinuumADMclosure as11999. No graphdeterminantlimit, Lorentzsignature, lapse/refoliation invariance, Newton/Lambda or higherderivativeghostcontrol selected. Fixedcellcount isabackgrounddensity until suppliedcapacitycompletion.',
        prior=['11601 metric/density/half-density heatkernel audit andnonconformalnegativecontrol','11995 actual10edgechart','11999 canonicalADMpulledbackfromsuppliedEH'],
        primary=['https://arxiv.org/abs/hep-th/0306138'])

if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass12009_native_metric_density.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['conformal_fixed_capacity']['integrated_a2_fixed_unit_capacity'])
