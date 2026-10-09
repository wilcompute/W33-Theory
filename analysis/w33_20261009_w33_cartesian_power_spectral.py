"""A W33-only replication test: Cartesian powers of the Levi graph.

For G_n=(Levi(W33))^square n, exact on-diagonal heat kernels factor.
Degree-normalized generator L_n/n has an n->infinity heat-kernel
limit exp(-4t) whose running spectral dimension is 8t, NOT a stable 3.
This tests one natural W33 self-replication; it is not a universal no-go.
"""
from math import sqrt,exp,log
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
EIG=[(0,1),(4-sqrt(6),24),(4,30),(4+sqrt(6),24),(8,1)]
def p(t):
    return sum(mult*exp(-e*t) for e,mult in EIG)/80
def hazard(t):
    weights=[mult*exp(-e*t) for e,mult in EIG]
    return sum(e*w for (e,mult),w in zip(EIG,weights))/sum(weights)
def spectral_power(n,t,normalized):
    s=t/n if normalized else t
    logreturn=n*log(p(s))
    dimension=2*t*(hazard(s) if normalized else n*hazard(s))
    return dict(n=n,t=t,degree_normalized=normalized,
                log_return_probability=logreturn,spectral_dimension=dimension)
def certificate():
    assert sum(m for e,m in EIG)==80
    assert abs(hazard(0)-4)<1e-13
    rows=[spectral_power(n,t,True) for n in (1,2,5,10,50,200,1000)
          for t in (.2,.375,.5,1)]
    for t in (.2,.375,.5,1):
        x=spectral_power(1000,t,True)
        assert abs(x['spectral_dimension']-8*t)<.02
        assert abs(x['log_return_probability']+4*t)<.01
    return dict(status='PASS',family='G_n = n-fold Cartesian product of 80-vertex Levi(W33)',
        formula='P_n(t)=p_Levi(t)^n; degree normalized P_n(t)=p_Levi(t/n)^n',
        large_n_fixed_t='P_norm(t)->exp(-4t), spectral_dimension(t)->8t (not constant)',
        fixed_n_large_t='P_n(t)->80^-n, spectral_dimension->0',
        transient='The dimension passes through 3 near t=3/8 only as a scale-dependent crossing, not a plateau.',
        samples=rows,boundary='One W33-only replication family; no Einstein gravity, no interacting Lorentzian continuum or unique spatial dimension.')
if __name__=='__main__':
    d=certificate()
    (ROOT/'data/w33_20261009_w33_cartesian_power_spectral.json').write_text(json.dumps(d,indent=2)+'\n')
    for t in (.2,.375,.5,1):print('time',t,'n1000',spectral_power(1000,t,True))
