"""Nonquadratic, dynamical metric-variable extension of prior11306 clocks.

This repairs a declared two-clock model exactly, not the GR Dirac algebra.
"""
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[1]


def payload():
    q,p,a,pi,t,u,P,Q=s.symbols('q p a pi t u P Q',real=True)
    pairs=((q,p),(a,pi),(t,P),(u,Q))
    def pb(f,g):return s.expand(sum(s.diff(f,x)*s.diff(g,y)-s.diff(f,y)*s.diff(g,x) for x,y in pairs))
    h1=a*p**2/2
    potential=(a-1)**2/2+(a-1)**4/4
    h2=q**2/(2*a)+q**4/(4*a**3)+pi**2/2+potential
    dressed=(q-a*p*t)**2/(2*a)+(q-a*p*t)**4/(4*a**3)+(pi+p**2*t/2)**2/2+potential
    c1=P+h1;c2=Q+dressed
    assert s.simplify(pb(c1,c2))==0
    bare=s.simplify(pb(P+h1,Q+h2));assert bare!=0
    z0=(q-a*p*t,p,a,pi+p**2*t/2)
    assert all(s.simplify(pb(f,c1))==0 for f in z0)
    assert s.simplify(pb(z0[0],z0[1]))==1
    assert s.simplify(pb(z0[2],z0[3]))==1
    return dict(status='PASS',native_interpretation='q=q_v-q_w, p=(p_v-p_w)/2 on a chosen native Levi edge; a>0 is an added metric coefficient with canonical momentum pi.',
        h1=str(h1),bare_h2=str(h2),bare_clock_bracket=str(bare),
        dressed_h2=str(s.expand(dressed)),exact_dressed_clock_bracket='0',
        constraint_count=2,extended_real_phase_dimension=8,physical_real_phase_dimension=4,
        original_physical_pairs=['q,p','a,pi'],
        input_metric_is_dynamical=True,quartic_metric_potential=True,quartic_matter_interaction=True,
        analytic_flow='q(t)=q0+a*p0*t; p(t)=p0; a(t)=a0; pi(t)=pi0-p0^2*t/2',
        exact_native_lapse_obstruction_not_retracted='11976 tests a different pointwise hypersurface bracket; no metric-only potential repair is claimed here.',
        prior=['analysis/w33_pass11306_relational_graph_clock_constraints.py owns quadratic80clock dressing and Maurer-Cartan method','11976 native scalar metric lapse failure'],
        scope='Exact nonlinear canonical metric-clock prototype. Clock constraints are Abelian and retain the original two physical pairs; this is NOT nonlinear GR, a derived spacetime metric, or the gravitational hypersurface-deformation algebra.',
        primary='https://arxiv.org/abs/1011.2463')


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11985_nonlinear_metric_clock.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['bare_clock_bracket'],d['exact_dressed_clock_bracket'])
