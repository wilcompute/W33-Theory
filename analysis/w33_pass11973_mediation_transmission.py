"""Actual leading gauge-mediated soft pattern on the11958 charged branch.

Uses the11966 exact D/F-flat curve and the FULL two-vector11958 mass
matrix. Equal-index X and Z messenger pairs avoid off-diagonal messenger
current correlators. Higgsed mediation, not massless-vector matching.
"""
from pathlib import Path
import json
import sys
import numpy as np
import mpmath as mp
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass11965_11966_cp_transmission_soft_modulus import high_norm,normalized_radial

RHO=1/32
SCALE=1e16*np.sqrt(high_norm(RHO))*RHO**11


def soft_function(x):
    p=RHO*x;d=(2*p+p*p)/12
    # T1,T2 charges1; P charge1; PhiMinus/Plus charges-12/+12.
    # Subtract the p=0 constant without changing stationarity.
    # Stable expression sqrt(4+d*d)-2 avoids cancellation at small p.
    return (2*p+p*p+144*d*d/(np.sqrt(4+d*d)+2))/RHO**2


def soft_slope(x):
    p=RHO*x;d=(2*p+p*p)/12;dp=(1+p)/6
    return (2+2*p+144*d*dp/np.sqrt(4+d*d))/RHO


def stationary(mz):
    k=mz/SCALE
    def derivative(x):
        z,dz=normalized_radial(x,RHO)
        return 2*(z-1)*dz+k*k*soft_slope(x)
    roots=[];grid=np.geomspace(1e-7,2,2500)
    for a,b in zip(grid,grid[1:]):
        if derivative(a)*derivative(b)<0:
            x=brentq(derivative,a,b,xtol=1e-14)
            curvature=(derivative(x+1e-5)-derivative(x-1e-5))/2e-5
            if curvature>0:
                z,_=normalized_radial(x,RHO)
                roots.append(dict(x=x,V_over_F0_squared=(z-1)**2+k*k*soft_function(x),curvature=curvature))
    return roots


def payload():
    def coexist(x):
        z,dz=normalized_radial(x,RHO)
        k2=-2*(z-1)*dz/soft_slope(x)
        return (z-1)**2+k2*soft_function(x)-1
    xcrit=brentq(coexist,.7,.999999)
    z,dz=normalized_radial(xcrit,RHO)
    kcrit=np.sqrt(-2*(z-1)*dz/soft_slope(xcrit))
    mzcrit=SCALE*kcrit
    gy=.36;gh=.1;mvis=1000.;mess=1e7
    # One messenger pair, charge magnitude1, leading small-F/M² matching.
    # Each Abelian charge+/-1 vectorlike pair has sum charges²=2.
    # Thus mvis²=4(gY²/(16pi²))²(F/M)², also Eq7 of1201.2179.
    F=mvis*mess*16*np.pi**2/(2*gy**2)
    # Eq13 of1201.2179 applies: hidden messenger current trace is I2.
    u=high_norm(RHO)
    moment=np.array([[4*RHO,2*RHO],[2*RHO,2*RHO+RHO**2+144*(u+1/u)]])
    ev,O=np.linalg.eigh(moment)
    vector_mass=np.sqrt(2*gh*gh*ev)*1e16
    delta=(vector_mass/mess)**2
    def suppression(d):
        with mp.workdps(100):
            d=mp.mpf(str(d));alpha=(mp.sqrt(d/4)+mp.sqrt(d/4-1))**(-2)
            omega=mp.sqrt(d*(d-4))*(2*mp.zeta(2)+mp.log(alpha)**2+4*mp.polylog(2,-alpha))
            exact=(2*d*(4-d)*((4-d)+(d+2)*mp.log(d))+2*(d-1)*omega)/(d*(4-d)**3)
            asym=2*(mp.log(d)-1)/d
            assert exact>0 and abs(exact/asym-1)<mp.mpf('1e-12')
            return float(exact)
    fs=np.array([suppression(d) for d in delta])
    q=np.array([[-1,0],[-1,0],[1,1],[1,1],[0,1],[0,-12],[0,12]])
    soft2=mvis*mvis*(gh/gy)**4*np.sum((q@O)**2*fs,axis=1)
    # Matching coefficients frozen at the selected SUSY home. This is a
    # local soft-response diagnostic, not a global CW potential to origin.
    def localV(x):
        p=RHO*x;up=high_norm(p);z,_=normalized_radial(x,RHO)
        soft=(sum(soft2[:4])*(p-RHO)+soft2[4]*(p*p-RHO*RHO)+
              soft2[5]*(up-u)+soft2[6]*(1/up-1/u))
        return (z-1)**2+soft/(1e32*u*RHO**24)
    # The induced masses are tiny: characterize the perturbative shift
    # from the analytic positive SUSY radial curvature instead of resolving
    # a1e-16 shift in binary floating point with root finding.
    _,dr=normalized_radial(1.,RHO)
    du=(1+RHO)/(6*(1+1/u**2))
    soft_slope_at_home=(sum(soft2[:4])*RHO+2*soft2[4]*RHO**2+
                        (soft2[5]-soft2[6]/u**2)*du*RHO)/(1e32*u*RHO**24)
    predicted_shift=-soft_slope_at_home/(2*dr*dr)
    assert max(np.sqrt(soft2))<1e-4
    assert F/mess**2<1
    return dict(status='PASS',visible_model='Three vectorlike messenger pairs: one Y-only, one X-only, one Z-only, unit integer charges, same spurionX=M+theta²F. Supplied gY=.36,gX=gZ=.1, M=1e7GeV; visible unit-hypercharge scalar mass1TeV. The hidden messenger current trace is proportional to I2, permitting exact two-vector mass-basis matching.',
        leading_matching='m_visible²=4(gY²/(16pi²))²(F/M)² for one charge+/-1 Abelian pair (messenger index2). For charge q=(X,Z), m_q²/m_visible²=(gH/gY)^4 sum_a[(q O)_a² f(MVa²/M²)], with O diagonalizing the FULL11958 moment matrix;1201.2179 Eq13.',
        F_GeV_squared=F,F_over_M_squared=F/mess**2,
        gravity_scale_GeV=F/(np.sqrt(3)*2.435e18),
        charge_order=['S1','S2','T1','T2','P','PhiMinus','PhiPlus'],soft_masses_GeV=np.sqrt(soft2).tolist(),
        hidden_vector_masses_GeV=vector_mass.tolist(),delta=delta.tolist(),suppression_f=fs.tolist(),
        suppression_formula='f(delta) from Eq8 with exact dilogarithm Omega, computed at100digits; agrees with2(log(delta)-1)/delta to relative1e-12 at these enormous deltas.',
        local_response='All7 matched soft coefficients included on11966 curve, frozen at selected home. A positive nearby radial curvature and tiny induced scale are supported. Neither this fixed-coefficient expansion nor the massless negative control is a global softly broken vacuum proof.',
        predicted_radial_shift_numeric=predicted_shift,
        massless_Z_only_negative_control=dict(coexistence_x=xcrit,critical_unit_Z_soft_GeV=mzcrit,explanation='The threshold0.0342GeV assumes a supplied Z-charge-squared soft pattern with no Higgsed suppression. It is NOT a bound on the actual messenger model.'),
        technical_sequestering='No bi-charged messenger in this model: Tr(YX)=Tr(YZ)=Tr(XZ)=0 at messenger1loop. Complete E6 multiplets also have TrY=0; split component thresholds need a separate audit. Gravity/Kahler portals, A terms and tadpoles remain allowed.',
        scope='Leading small-F/M² Higgsed two-vector matching for a specified toy messenger model and local restricted-curve response. Supplied scales and couplings. No full softly broken Hessian, D-response off curve, finite-F corrections, A terms, tadpoles, full supergravity vacuum or physical prediction.',
        prior=['11958 protected gauge branch','11966 canonical light mass and P-only soft response'],
        primary='https://arxiv.org/abs/1201.2179')


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11973_mediation_transmission.json').write_text(json.dumps(d,indent=2)+'\n')
    print('PASS',d['hidden_vector_masses_GeV'],d['soft_masses_GeV'])
