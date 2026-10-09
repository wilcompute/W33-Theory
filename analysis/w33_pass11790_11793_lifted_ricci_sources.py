"""Exact centered null Ricci/source obstruction for the actual Gaussian lift.

This computes curvature of a named variational metric; it does not identify
that80D Bargmann manifold with observed spacetime or supply physical gravity.
"""
from pathlib import Path
import hashlib,json,sys
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as V
from w33_pass11786_certified_spectral_transitions import I,parameters
OUT=ROOT/'data/w33_pass11790_11793_lifted_ricci_sources.json'

def ricci(metric,coordinates):
    n=len(coordinates);inverse=metric.inv()
    gamma=[[[sp.simplify(sum(inverse[a,d]*(sp.diff(metric[d,c],coordinates[b])+sp.diff(metric[d,b],coordinates[c])-sp.diff(metric[b,c],coordinates[d])) for d in range(n))/2)
             for c in range(n)] for b in range(n)] for a in range(n)]
    answer=sp.zeros(n)
    for b in range(n):
        for c in range(n):
            answer[b,c]=sp.simplify(sum(sp.diff(gamma[a][b][c],coordinates[a])-sp.diff(gamma[a][b][a],coordinates[c])+
                sum(gamma[a][a][d]*gamma[d][b][c]-gamma[a][c][d]*gamma[d][b][a] for d in range(n)) for a in range(n)))
    return answer,gamma

def differential_controls():
    x,y,u,v=sp.symbols('x y u v',real=True);B,mu=sp.symbols('B mu',real=True)
    a1,a2=-B*y/2,B*x/2;potential=mu*(x*x+y*y)/2
    metric=sp.Matrix([[1,0,a1,0],[0,1,a2,0],[a1,a2,-2*potential,1],[0,0,1,0]])
    r,gamma=ricci(metric,(x,y,u,v))
    assert r[2,2]==2*mu+B*B/2
    assert all(gamma[a][b][3]==0 for a in range(4) for b in range(4))
    assert all(r[3,i]==0 for i in range(4))
    assert r.subs(mu,-B*B/4)==sp.zeros(4)
    metric1=sp.Matrix([[1+x*x,0,0],[0,-mu*x*x,1],[0,1,0]])
    r1,_=ricci(metric1,(x,u,v))
    assert sp.simplify(r1[1,1]-mu/(1+x*x)**2)==0
    return dict(flat_magnetic_Ruu=str(r[2,2]),
        rotating_flat_control='mu=-B^2/4 cancels the magnetic null Ricci contribution; positive confinement instead adds to it.',
        nonconstant_target_Ruu=str(r1[1,1]),parallel_null_vector=True)

def actual_curvature():
    geo=V.geometry();pw40=np.rint(40*geo['pw']).astype(np.int64)
    adj10=np.rint(10*geo['g']).astype(np.int64)
    # 16P_W-Adj^2 expressed over exact common denominator100.
    tidal100=40*pw40-adj10@adj10
    assert int(np.trace(tidal100))==96000
    assert np.array_equal(tidal100@(tidal100-1000*pw40//40)@(tidal100-1600*pw40//40),np.zeros((80,80),dtype=np.int64))
    m,t,f,e=parameters();b=sp.Rational(1,20)
    vx=t*m;vy=m/t+f*f*t*m;c=f*t*m
    alpha=4*((vx+I('1/20'))*(vy+I('1/20'))-4*(c+I('1/20'))**2)
    assert alpha.lo>0
    ruu=960*alpha
    return dict(status='PASS',
        metric='g=G_ij(q)dq_i*dq_j+2du[dv+A_i(q)dq_i-Veff(q)du], G=P(q)^(-1).',
        parallel_null='All g_vA are constants and every coefficient is v-independent; Gamma^A_Bv=0. Thus partial_v is covariantly constant, not only Killing, and Ric_vA=0 globally.',
        stationary_Ruu='For stationary G,A,Veff, Ric_uu=Delta_G Veff+(1/4)*F_ij*F^ij. At q=0, A=0,F=0,grad Veff=0; hence Ric_uu(0)=tr(P0*Hess Veff).',
        centered_hessian='Hess Veff(0)=2*[(vy+b)-4*(c+b)^2/(vx+b)]*(4P_W-Adj); b=1/20. This is the Schur complement of the11771 exact Gaussian energy Hessian.',
        tidal_endomorphism='P0*Hess Veff=alpha*(16P_W-Adj^2), alpha=4*[(vx+b)*(vy+b)-4*(c+b)^2]>0.',
        alpha_interval=alpha.data(),null_ricci_interval=ruu.data(),
        exact_trace=960,tidal_eigenvalues=[dict(value='10*alpha',multiplicity=48),dict(value='16*alpha',multiplicity=30)],
        geodesic_connection='The positive geodesic tidal eigenvalues reproduce the squared centered Gaussian normal frequencies already owned by11771. This supplies a geometric reading of those frequencies, not new particle masses.',
        no_vacuum_einstein='If Ric_AB=lambda*g_AB, the uv component gives lambda=0 because Ric_uv=0 and g_uv=1. But Ric_uu(0)=960*alpha>0. Therefore this exact lift fails vacuum Einstein equations for EVERY cosmological constant.',
        required_null_source='At q=0 let L=partial_u+Veff(0)*partial_v, so g(L,L)=0. Einstein equations with any cosmological constant require T(L,L)=960*alpha/(8*pi*G_N)>0. This null contraction is independent of scalar-curvature and cosmological terms. G_N is supplied; other stress components require the rest of Ricci(G,A,Veff).',
        constant_energy_shift='Veff->Veff+Lambda changes the null-coordinate choice v_new=v-Lambda*u but not the invariant null Ricci/source contraction. The lift does not solve the physical cosmological constant problem.',
        field_equation_boundary='The force-geometrizing metric is not a gravitational vacuum. One may define a conserved effective stress tensor from its Einstein tensor, but that alone is a tautological source assignment, not a derived matter action or gravitational dynamics. A self-consistent coupled solution and physical dimensional reduction remain open.',
        differential_controls=differential_controls(),
        prior='11781/11784/11785 own G,A,Veff and the standard lift;11771 owns alpha and48+30 normal-frequency multiplicities.',
        literature=['https://arxiv.org/abs/1605.01932','https://arxiv.org/abs/1901.03699'])

def certificate():
    return dict(schema='w33.pass11790_11793.v1',source_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),pass11790_11793=actual_curvature())
if __name__=='__main__':
    x=certificate();OUT.write_text(json.dumps(x,indent=2)+'\n')
    print('11790/11793 exact null Ricci960alpha and required source PASS')
