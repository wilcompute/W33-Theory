"""Couple the actual11978 soft singlet sector to11981's CP flavour fields.

A gauge-invariant composite replaces the independent11989 source. Scales and
couplings are supplied. Local stationarity/stability are checked, not a full
E6 vacuum, global minimum, predicted hierarchy or radiative strong CP.
"""
import json,itertools
from pathlib import Path
import mpmath as mp
import numpy as np
from w33_pass11978_full_singlet_soft_vacuum import potential_core,home
from w33_pass11989_joint_source_barr import weak_cp,barr_matching,args_of
from w33_pass11981_cubic_mediator_cp import determinant_energy_gradient
from w33_pass11952_11955_threshold_vacuum_loop_leptons import b0
ROOT=Path(__file__).resolve().parents[1]


def setup():
    mp.mp.dps=100
    old=json.loads((ROOT/'data/w33_pass11978_full_singlet_soft_vacuum.json').read_text())
    med=json.loads((ROOT/'data/w33_pass11973_mediation_transmission.json').read_text())
    prior=next(r for r in json.loads((ROOT/'data/w33_pass11981_cubic_mediator_cp.json').read_text())['third_triplet_determinant_probe']['draws'] if r['trial']==3)
    conv=lambda a:mp.mpf(str(a))
    rho=mp.mpf(1)/32;Lambda=mp.mpf('1e16');vf=mp.mpf('1e3');eps=(vf/Lambda)**4
    mg=conv(med['gravity_scale_GeV']);soft=[(conv(m)**2+mg**2)/Lambda**2 for m in med['soft_masses_GeV']]
    delta=(2*rho+rho*rho)/12;rm=mp.sqrt((mp.sqrt(delta**2+4)+delta)/2);f0=rm*rho**12
    M=list(map(conv,prior['M']));weights=[list(map(conv,w)) for w in prior['weights']]
    constants=list(map(conv,prior['constants']));couplings=list(map(conv,prior['lambdas']));g=conv(prior['g']);mu=conv(prior['mu'])
    omega=mp.exp(2*mp.pi*mp.j/3);weyl=[]
    for a,b in [(0,1),(1,0),(1,1),(1,2)]:
        D=mp.matrix(3)
        for j in range(3):D[(j+a)%3,j]=omega**((2*a*b+b*j)%3)
        weyl.append(D)
    def flavour(x,tau):
        z=[mp.matrix([x[6*k+i]+mp.j*x[6*k+3+i] for i in range(3)]) for k in range(3)]
        norms=[sum(abs(a)**2 for a in v) for v in z]
        current=[sum(weights[k][a]*(z[k].H*weyl[a]*z[k])[0] for k in range(3)) for a in range(4)]
        value=-sum(abs(v)**2/m**2 for v,m in zip(current,M))
        for k,v in enumerate(z):
            inv=[sum(a**3 for a in v),mp.fprod(v)]
            value-=sum(abs(constants[2*k+i]+couplings[2*k+i]*inv[i])**2 for i in range(2))
        h,f,t=z;cross=mp.matrix([h[1]*f[2]-h[2]*f[1],h[2]*f[0]-h[0]*f[2],h[0]*f[1]-h[1]*f[0]])
        source=g*cross+mp.j*mu*tau*t.conjugate()
        value-=sum(abs(v)**2 for v in source)
        return value+sum(10*(n-1)**2+mp.mpf('.01')*n**4 for n in norms)
    def tau(z):return mp.im(z[0]*mp.conj(z[1]))/rho
    def V(*a):return potential_core(home(a[:7]),soft,mp.mpf('.1'),f0)+eps*flavour(a[7:],tau(home(a[:7])))
    def equations(*a):
        # Row scaling removes the tiny flavour energy scale from Newton's
        # equations, not from the underlying physical potential.
        return mp.matrix([mp.diff(V,a,tuple(int(i==j) for i in range(25)))/(eps if j>=7 else 1) for j in range(25)])
    start=list(map(mp.mpf,old['selected_real_coordinates']))+list(map(conv,prior['x']))
    return old,med,prior,rho,Lambda,vf,eps,soft,f0,flavour,tau,V,equations,start


def scalar_portal_threshold(x,tau,prior,matching):
    """11954 standard matching, now using the actual flavour vacuum/Hessian.

    A separate19real-scalar non-SUSY EFT slice: singlet and mediator loop
    fluctuations, colored/gauge loops and tadpoles are not included.
    """
    args=args_of(prior);x=np.array(x,float)
    H=np.column_stack([(determinant_energy_gradient(x+2e-5*v,*args,tau=tau)[1]-determinant_energy_gradient(x-2e-5*v,*args,tau=tau)[1])/4e-5 for v in np.eye(18)]);H=(H+H.T)/2
    m=np.array(matching['real_m']);C=np.array(matching['real_C']);mass=np.zeros((4,4),complex)
    mass[:3,:3]=m;mass[3,:3]=C@(x[:3]+1j*x[3:6]);mass[3,3]=matching['mu']
    vertices=np.zeros((19,4,4),complex);vertices[0,:3,:3]=m
    for i in range(3):vertices[i+1,3,:3]=C[:,i];vertices[i+4,3,:3]=1j*C[:,i]
    def run(kappa,cp=False,scale=1.):
        tangent=np.r_[2*kappa*x[:6],np.zeros(12)]
        K=np.block([[np.array([[25.]]),tangent[None,:]],[tangent[:,None],H+np.outer(tangent,tangent)/25]])
        M=mass.copy()
        if cp:
            signs=np.r_[1,[(-1 if (i%6)>=3 else 1) for i in range(18)]]
            K=signs[:,None]*K*signs[None,:];M=M.conj()
        ev,O=np.linalg.eigh(K);assert min(ev)>0
        U,mm,Vh=np.linalg.svd(M);V=Vh.conj().T;delta=np.zeros((4,4),complex);div=0j
        for j,squared in enumerate(ev):
            Y=np.einsum('i,ijk->jk',O[:,j],vertices)
            delta+=Y@((V*(mm*b0(mm**2,squared,scale)))@U.conj().T)@Y/(16*np.pi**2)
            div+=np.trace(np.linalg.solve(M,Y@M.conj().T@Y))/(16*np.pi**2)
        theta=float(np.trace(np.linalg.solve(M,delta)).imag)
        return dict(kappa=kappa,theta_one_loop=theta,minimum_scalar_mass_squared=float(min(ev)),theta_divergent_coefficient=float(div.imag))
    rows=[run(k) for k in (0.,.1,.01,.001,1e-5)]
    opposite=run(.1,True);scale=run(.1,False,3.)
    assert abs(rows[0]['theta_one_loop'])<1e-12
    assert abs(rows[1]['theta_one_loop'])>1e-5
    assert abs(opposite['theta_one_loop']+rows[1]['theta_one_loop'])<1e-11
    assert abs(scale['theta_one_loop']-rows[1]['theta_one_loop'])<1e-11
    slope=rows[-1]['theta_one_loop']/rows[-1]['kappa']
    return dict(scan=rows,CP_partner=opposite,scale3=scale,small_kappa_slope=slope,
        illustrative_kappa_for_abs_theta_below_1e_minus10=1e-10/abs(slope),
        supplied_portal='DeltaV=1/2 [5 H+(kappa/5)(|h|²-|h0|²)]². Its value/first derivatives vanish at H=0,h=h0; its Hessian is a positive-square completion, so the prior local minimum is retained. H is a real neutral Higgs fluctuation with Yukawa derivativeYH=m; B=C h supplies the six real h vertices.',
        boundary='Finite neutral-scalar one-loop self-energy in a separately declared19scalar EFT slice using actual18D flavour Hessian and fittedBarrvertices. Not total72scalar/SUSY/E6 theta: singlet/mediator/colored/gauge loops, RG and tadpole shifts omitted. Input portal coefficient and fittedquark masses; suppression bound is a conditional matching diagnostic, not a prediction or proof of no cancellation.',
        prior='11954 owns the neutral-scalar B0 matching method and separateportal counterexample; new here is its application to11996 actualjointflavourvacuum and scalarcurvature.',
        primary='https://arxiv.org/abs/2105.09122')


def payload():
    old,med,prior,rho,Lambda,vf,eps,soft,f0,flavour,tau,V,equations,start=setup()
    root=mp.matrix(start);hist=[]
    for it in range(9):
        residual=equations(*root);err=max(abs(x) for x in residual);hist.append(mp.nstr(err,12))
        if err<mp.mpf('1e-75'):break
        J=mp.matrix(25)
        for j in range(25):
            col=mp.diff(lambda q:equations(*[q if k==j else root[k] for k in range(25)]),root[j])
            for i in range(25):J[i,j]=col[i]
        step=mp.lu_solve(J,-residual);assert max(abs(x) for x in step)<mp.mpf('.001')
        root+=step
    assert max(abs(x) for x in equations(*root))<mp.mpf('1e-70')
    z=home(root[:7]);x=list(root[7:]);tauvalue=tau(z)
    point=list(map(mp.re,z))+list(map(mp.im,z))+x
    def total(*a):
        zz=[a[i]+mp.j*a[i+7] for i in range(7)]
        return potential_core(zz,soft,mp.mpf('.1'),f0)+eps*flavour(a[14:],tau(zz))
    gradient=[mp.diff(total,point,tuple(int(i==j) for i in range(32))) for j in range(32)]
    assert max(abs(v)/(eps if j>=14 else 1) for j,v in enumerate(gradient))<mp.mpf('1e-70')
    Hess=mp.matrix(32);scale=[mp.mpf(1)]*14+[mp.sqrt(eps)]*18
    for i in range(32):
        for j in range(i,32):
            h=mp.diff(total,point,tuple(int(k==i)+int(k==j) for k in range(32)))/(scale[i]*scale[j])
            Hess[i,j]=Hess[j,i]=h
    ev,_=mp.eigsy(Hess);positive=[a for a in ev if a>mp.mpf('1e-65')];zeros=[a for a in ev if abs(a)<=mp.mpf('1e-65')]
    assert len(positive)==30 and len(zeros)==2 and min(ev)>-mp.mpf('1e-65')
    # Multipliers and spectators remain exactly zero: their parity is
    # unbroken by the composite portal. Check their actual mass blocks.
    s1,s2,t1,t2,p,rm,rp=z
    J=mp.matrix([[t1,0,s1,0,-1,0,0],[0,2*t2,0,2*s2,-2,0,0],[3*t2,3*t1,3*s2,3*s1,0,0,0],[0,0,0,0,0,rp,rm],[0,0,0,0,12*rm*p**11,p**12,0]])
    dz=abs(t1)**2+abs(t2)**2+abs(p)**2-12*abs(rm)**2+12*abs(rp)**2
    mg=mp.mpf(str(med['gravity_scale_GeV']));K=J.conjugate()*J.T
    for i in range(5):K[i,i]+=([soft[4]]*3+[(mg/Lambda)**2]*2)[i]-(mp.mpf('.01')*dz if i<3 else 0)
    lag,_=mp.eighe(K);spec=abs(rm*p**10)**2+mp.mpf('.01')*dz+soft[4]
    assert min(lag)>0 and spec>0
    # CP changes singlet and triplet complex conjugates together.
    partner=list(map(mp.re,z))+[-mp.im(a) for a in z]+[(-a if (i%6)>=3 else a) for i,a in enumerate(x)]
    cp_error=abs(total(*point)-total(*partner));assert cp_error<mp.mpf('1e-85')
    yy=np.array(list(map(float,x)));weak=weak_cp(yy);assert abs(weak)>1e-5
    match=barr_matching(np.r_[yy,float(tauvalue)])
    return dict(status='PASS',precision_digits=100,singlet_cutoff_GeV=str(Lambda),supplied_flavour_scale_GeV=str(vf),flavour_energy_ratio=str(eps),
        composite_source='tau=Im(S1 conj(S2))/rho, rho=1/32. Both Si have X=-1,Z=0, so tau is gauge invariant and CP odd. No independent tau double well remains.',
        potential='V=Lambda^4 V11978_soft_singlet + vf^4 V11981_flavour(x,tau(S)); supplied scale matching and frozen coefficients.',
        singlet_chart_coordinates=[mp.nstr(a,80) for a in root[:7]],triplet_coordinates=list(map(float,x)),triplet_coordinates_decimal=[mp.nstr(a,80) for a in x],
        scaled_core_flavour_Hessian_decimal=[[mp.nstr(Hess[i,j],75) for j in range(32)] for i in range(32)],source_value=mp.nstr(tauvalue,50),
        maximum_singlet_displacement_from_frozen11978=mp.nstr(max(abs(root[i]-mp.mpf(old['selected_real_coordinates'][i])) for i in range(7)),20),
        Newton_scaled_residual_history=hist,full32_scaled_gradient_max=mp.nstr(max(abs(v)/(eps if j>=14 else 1) for j,v in enumerate(gradient)),15),
        mixed_Hessian_congruence_scaling='S=diag(I14,sqrt(eps) I18); check S^-1 H S^-1, which has exactly the same inertia as H. Its eigenvalues are NOT physical particle masses.',
        positive_core_and_flavour_modes=30,gauge_zero_modes=2,minimum_positive_congruence_Hessian_eigenvalue=mp.nstr(min(positive),20),
        congruence_Hessian_eigenvalues=[mp.nstr(a,25) for a in ev],positive_multiplier_modes=10,positive_spectator_modes=4,
        total_light_real_fields=46,total_positive_physical_light_modes=44,restored_positive_mediator_real_modes=26,total_scalar_real_fields_with_mediators=72,
        mediator_stability='The13complex flavour mediators have positive heavy Hessian; completing squares makes full72D Hessian congruent to solved46D Hessian plus26positive modes. Singlet multiplier/spectator blocks remain positive and stationary0.',
        weak_CP_J=weak,CP_partner_energy_error=mp.nstr(cp_error,15),Barr_matching=match,
        actual_flavour_scalar_portal_threshold=scalar_portal_threshold(yy,float(tauvalue),prior,match),
        source_boundary='This uses the actual11978 soft-mass-only singlet model, NOT its separate canonical pinned-hidden SUGRA root. The new portal is a gauge-invariant nonholomorphic scalar EFT interaction, not a supplied supersymmetric superpotential completion.',
        physics_boundary='A numerical local joint72-real-scalar witness, not full E6/orbifold vacuum, a global minimum, observed Yukawa predictions, a protected zero block, or radiative strong CP. The arbitrary vf/Lambda hierarchy controls portal backreaction and is not generated.',
        prior=['11978 actual softly-broken singlet vacuum and positive multiplier/spectator blocks','11981 pinned-source flavour potential','11989 independent-source model and fitted Barr map','11953 gauge-invariant CP-odd singlet and allowed leakage operator','11965 singlet-to-Barr CP transmission'],
        primary=['https://arxiv.org/abs/1802.08109','https://arxiv.org/abs/hep-ph/9709356'])

if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11996_joint_singlet_flavour.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['source_value'],d['positive_core_and_flavour_modes'])
