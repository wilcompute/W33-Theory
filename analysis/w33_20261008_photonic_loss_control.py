"""Exact loss-and-Gaussian-noise continuation of single-edge homodyne control.

No quantum hardware claim. Stable pure-loss channel and independent Gaussian
electronic noise only. Mixed Gaussian shot variances are adversarial controls.
"""
from fractions import Fraction as Q
import math, json
from pathlib import Path
A=Q(618440,6591)
B=Q(5207,3042)
def signal(tau,eta,electronic_variance=0):
    tau=float(tau);eta=float(eta);noise=float(electronic_variance)
    assert tau>=0 and 0<=eta<=1 and noise>=0
    theta=(39/20)**2*tau
    k4=float(A)*theta**4*eta**2
    variance=.5+float(B)*theta**2*eta+noise
    excess=k4/variance**2
    null_shots=600/excess**2 if excess else math.inf
    drift_std_threshold=math.sqrt(k4/3) if k4 else 0.
    return dict(tau=tau,transmission=eta,electronic_variance=noise,
        theta=theta,variance=variance,cumulant4=k4,
        excess_kurtosis=excess,
        optimistic_5sigma_gaussian_null_shots=null_shots,
        variance_drift_std_at_equal_cumulant=drift_std_threshold)
def certificate():
    rows=[signal(tau,eta,.01) for tau in (.02,.03,.05) for eta in (1,.8,.5,.2)]
    for tau in (.02,.03,.05):
        a=signal(tau,1,0);b=signal(tau,.5,0)
        assert abs(b['cumulant4']-a['cumulant4']/4)<1e-12
    return dict(status='PASS',schema='w33.cv.single_edge_loss.v1',
        exact_kappa4='eta^2*(618440/6591)*((39/20)^2*tau)^4',
        exact_variance='1/2+eta*(5207/3042)*((39/20)^2*tau)^2+sigma_e^2',
        null_drift_warning='A Gaussian variance mixture has kappa4=3 Var(v_shot), so uncontrolled variance drift fakes this signal.',
        significance_warning='600/gamma2^2 uses asymptotic normal-null standard error sqrt(24/N), not robust power under the quartic alternative.',
        controls=rows)
if __name__=='__main__':
    report=certificate()
    path=Path(__file__).resolve().parents[1]/'data/w33_20261008_photonic_loss_control.json'
    path.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS optical loss rows',len(report['controls']))
    for x in report['controls']:
        if x['tau']==.05:print(x)
