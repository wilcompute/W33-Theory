"""Remove the unwanted PW mirror critical pair by a harmonic linear tilt.

Reuses d7280e023's exact L2 argument and the explicit mirror-lift operator.
Local noncompact BPS model only; no generation-number or vacuum selection.
"""
import json
from pathlib import Path
import numpy as np
import sympy as s
from scipy import sparse as sp
from scipy.sparse.linalg import eigsh
from toe_20261118_PW_instanton_mirror_lift import scalar_hamiltonian, rectangular_partner

ROOT=Path(__file__).resolve().parents[1]


def geometry():
    x,y,z,a=s.symbols('x y z a',real=True)
    f=(x**4-6*x*x*y*y+y**4)/4-(x*x+y*y)/2+z*z-a*x
    g=s.Matrix([s.diff(f,t) for t in (x,y,z)])
    assert sum(s.diff(f,t,2) for t in (x,y,z))==0
    assert s.expand(g[1]-y*(y*y-3*x*x-1))==0
    assert s.expand(g[0].subs(y*y,3*x*x+1))==-8*x**3-4*x-a
    axis=s.Poly(x**3-x-a,x)
    assert s.discriminant(axis.as_expr(),x)==4-27*a*a
    for av in (s.Rational(1,5),s.Rational(1,3)):
        assert s.Poly(axis.as_expr().subs(a,av),x).count_roots(-s.oo,s.oo)==3
    assert s.Poly(x**3-x-1,x).count_roots(-s.oo,s.oo)==1
    assert s.Poly(8*x**3+4*x+1,x).count_roots(-s.oo,s.oo)==1
    rho=float(s.nroots(x**3-x-1)[0])
    u=float(s.nroots(8*x**3+4*x+1)[0])
    v=np.sqrt(3*u*u+1)
    points=[(rho,0.,0.),(u,v,0.),(u,-v,0.)]
    records=[]
    for p in points:
        H=np.array(s.hessian(f,(x,y,z)).subs({x:p[0],y:p[1],z:0,a:1}),dtype=float)
        ev=np.linalg.eigvalsh(H)
        assert sum(ev<0)==1
        records.append({'point':list(p),'Hessian_eigenvalues':ev.tolist()})
    # Generic complex linear tilt A+iB: no critical point can lie inside
    # r<=1/sqrt(3) once |A+iB| > 4/(3sqrt(3)). Degree then forces three.
    return {'harmonic':True,'real_axis_fold_threshold':'2/(3*sqrt(3))',
            'arbitrary_complex_tilt_sufficient_bound':'abs(A+iB)>4/(3*sqrt(3))',
            'critical_circle_radius':'1/sqrt(3)',
            'caustic_parameter':'exp(-3i*theta)/(3sqrt(3))-exp(i*theta)/sqrt(3)',
            'caustic_rotated_astroid':'a(phi+pi/4)=-exp(i*pi/4)*4/(3sqrt(3))*(cos(phi)^3+i*sin(phi)^3)',
            'tilt1_critical_points':records,'critical_count':3,'all_Morse_index':1,
            'L2_betti_positive_charge':[0,3,0,0],
            'planar_H2_large_q_coefficient':float(min(6*(p[0]**2+p[1]**2)-2 for p in points)),
            'general_source':'degree minus3 + strict concavity inside critical disk; linear term does not change infinity winding'}


def hamiltonian(n,q,tilt,width_ratio=1.):
    omega=max(3.,q)*width_ratio
    B=rectangular_partner(n,q,omega)
    m=n+3
    J=sp.eye(m,format='csc')[:,:n]
    J2=sp.kron(J,J,format='csc')
    zero=sp.csc_matrix(J2.shape)
    B=B-q*tilt*sp.vstack([zero,J2],format='csc')
    return (B.T@B).tocsc()


def spectrum(n,q,tilt,width_ratio=1.):
    H=hamiltonian(n,q,tilt,width_ratio)
    ev,vec=eigsh(H,k=2,sigma=-1e-6,which='LM',tol=1e-10,
                 v0=np.random.default_rng(34).normal(size=n*n))
    order=np.argsort(ev);ev=ev[order];vec=vec[:,order]
    N=n+6;v=np.zeros((N,N));v[:n,:n]=vec[:,0].reshape(n,n)
    res=np.linalg.norm(hamiltonian(N,q,tilt,width_ratio)@v.ravel()-ev[0]*v.ravel())
    assert min(ev)>0
    return {'tilt':tilt,'q':q,'n':n,'width_ratio':width_ratio,
            'H2_lowest':float(ev[0]),'H2_second':float(ev[1]),
            'H2_lowest_over_q':float(ev[0]/q),
            'estimated_full3D_first_positive':float(min(ev[0],4*q)),
            'full_operator_L2_residual':float(res)}


def run():
    out={'scope':'harmonic tilt removes extra local mirror critical pair; no global G2 or SM completion',
         'geometry':geometry(),'spectral':[]}
    for q in (4.,12.,24.):
        for tilt in (0.,.2,.38,.4,.6,1.):
            row=spectrum(56,q,tilt)
            out['spectral'].append(row)
            print(q,tilt,row['H2_lowest'],row['H2_lowest_over_q'],flush=True)
    out['controls']=[spectrum(88,q,1.,.75) for q in (12.,24.)]
    for row in out['controls']:
        base=next(r for r in out['spectral'] if r['q']==row['q'] and r['tilt']==1.)
        assert abs(base['H2_lowest']/row['H2_lowest']-1)<.001
    out['high_resolution_control']=spectrum(144,24.,1.)
    assert out['high_resolution_control']['full_operator_L2_residual']<1e-7
    out['limitations']=['tilt and quartic supplied, not dynamically selected',
        'C4 broken; no previous C4 quotient interpretation',
        'noncompact infinite-energy background and gauge constants not L2',
        'native E6 anomalies/rank/Yukawas unchanged','no physical compactification scale']
    path=ROOT/'data/toe_20261118_PW_tilt_perfect_Morse.json'
    path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print('PASS',path,flush=True)
    return out


if __name__=='__main__':run()
