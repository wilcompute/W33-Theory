"""CP-real theta homes WITH one matched vectorlike quark: compatibility witness.

11951 owns the general Barr inverse construction. Here the REAL bare m is
constrained to11942's theta family rather than freely inverse reconstructed.
All parameters are fitted; no vacuum selection or radiative protection claim.
"""
import json
from pathlib import Path
import numpy as np
from w33_pass11942_hypercharge_wilson_leptons import theta,normalised,DATA
ROOT=Path(__file__).resolve().parents[1]
Y=.8744698731421595
EU=.005520606513514881
FIT=np.array([-.8404552787929092,.08087153936666885,.0677453432123109,
              6.942570225348479,6.847783916520845,-8.247969957747468,-.44792758573762237,-13.009011874237432])

def bare_matrices():
    tau=1+1j*Y;yd=np.exp(FIT[0]);ed=FIT[1];zi=FIT[2]
    Ou=np.array([[tau,1j*EU],[1j*EU,tau]]);Od=np.array([[tau,1j*ed],[1j*ed,1j*yd]])
    phases=np.exp(1j*np.pi*np.arange(3)**2/3)
    rawu=theta(Ou);rawd=normalised(Od,(0,1j*zi))
    u=phases.conj()[:,None]*rawu*phases.conj()[None,:]
    d=phases.conj()[:,None]*rawd
    assert max(abs(u.imag).max(),abs(d.imag).max())<1e-12
    u=u.real/np.linalg.norm(u);d=d.real/np.linalg.norm(d)
    # Real right-handed sign choices give the stated positive-det CP branch.
    su=np.diag([np.sign(np.linalg.det(u)),1,1]);sd=np.diag([np.sign(np.linalg.det(d)),1,1])
    u=u@su;d=d@sd
    b=np.array([FIT[3],FIT[4]+1j*FIT[5],FIT[6]+1j*FIT[7]])@sd
    assert np.linalg.det(u)>0 and np.linalg.det(d)>0
    return u,d,b,Ou,Od

def observables(u,m,b):
    Uu,su,_=np.linalg.svd(u);K=np.eye(3)-np.outer(b.conj(),b)/(1+np.vdot(b,b).real)
    ev,O=np.linalg.eigh(K);A=(O*np.sqrt(ev))@O.conj().T
    Ud,sd,_=np.linalg.svd(m@A);V=(Uu.conj().T@Ud)[::-1,::-1]
    J=float((V[0,0]*V[1,1]*V[0,1].conj()*V[1,0].conj()).imag)
    q=dict(mc_mt=su[1]/su[0],mu_mc=su[2]/su[1],ms_mb=sd[1]/sd[0],md_ms=sd[2]/sd[1],Vus=abs(V[0,1]),Vcb=abs(V[1,2]),Vub=abs(V[0,2]),J=J)
    return q,V,sd,K

def payload():
    u,m,b,Ou,Od=bare_matrices();q,V,sd,K=observables(u,m,b)
    assert max(abs(q[k]/DATA[k]-1) for k in DATA)<1e-7
    bare=observables(u,m,np.zeros(3))[0];partner=observables(u,m,b.conj())[0];real=observables(u,m,b.real)[0]
    assert abs(bare['J'])<1e-14 and abs(real['J'])<1e-14 and abs(partner['J']+q['J'])<1e-14
    # Exact algebraic criterion: C=I-m^-1 H m^-T is PSD rank1 with eigenvalue<1.
    H=m@K@m.T
    C=np.eye(3)-np.linalg.solve(m,H)@np.linalg.inv(m.T)
    ce=np.linalg.eigvalsh((C+C.conj().T)/2);assert max(abs(ce[:2]))<1e-8 and 0<ce[2]<1
    rows=[];Uu=np.linalg.svd(u)[0]
    for scale in [10.,100.,1000.]:
        full=np.zeros((4,4),complex);full[:3,:3]=m;full[3,:3]=scale*b;full[3,3]=scale
        Uf,sf,_=np.linalg.svd(full);light=sf[1:];Vf=(Uu.conj().T@Uf[:3,1:])[::-1,::-1]
        determinant=np.linalg.det(full);assert determinant.real>0 and abs(determinant.imag)<1e-12
        rows.append(dict(mu=scale,light_singular_values=light.tolist(),max_relative_spectrum_error=float(max(abs(light/sd-1))),left_mixing_nonunitarity=float(np.linalg.norm(Vf@Vf.conj().T-np.eye(3))),determinant_real=float(determinant.real),determinant_imag=float(determinant.imag)))
    assert rows[-1]['max_relative_spectrum_error']<1e-7 and rows[-1]['max_relative_spectrum_error']<rows[0]['max_relative_spectrum_error']/500
    # Independent direct theta evaluation at two cutoffs, no real projection.
    def direct(O,z,N):
        n=np.arange(-N,N+1);xx,yy=np.meshgrid(n,n,indexing='ij');A=np.empty((3,3),complex)
        for a in range(3):
            for c in range(3):
                x=xx+a/3;y=yy+c/3
                A[a,c]=np.exp(3j*np.pi*(O[0,0]*x*x+2*O[0,1]*x*y+O[1,1]*y*y)+6j*np.pi*y*z).sum()
        return A/np.linalg.norm(A)
    errors=[]
    for O,z in [(Ou,0),(Od,1j*FIT[2])]:errors.append(float(np.max(abs(direct(O,z,12)-direct(O,z,20)))))
    assert max(errors)<1e-13
    return dict(status='PASS',up_height=Y,up_imaginary_entangler=EU,down_height=float(np.exp(FIT[0])),down_imaginary_entangler=float(FIT[1]),down_imaginary_Wilson_argument=float(FIT[2]),
        fitted_B_over_mu=[[float(z.real),float(z.imag)] for z in b],real_bare_up=u.tolist(),real_bare_down=m.tolist(),matched_quark_observables={k:float(v) for k,v in q.items()},supplied_quark_comparators=DATA,
        bare_no_B_observables={k:float(v) for k,v in bare.items()},CP_partner_J=partner['J'],real_B_J=real['J'],max_relative_comparator_error=float(max(abs(q[k]/DATA[k]-1) for k in DATA)),
        rank_one_defect_eigenvalues=ce.tolist(),right_metric_eigenvalues=np.linalg.eigvalsh(K).tolist(),finite_heavy_scale_controls=rows,theta_cutoff_12_20_errors=errors,
        exact_tree_mass_identity='det[[m,0],[B,mu]]=mu det(m)>0; real positive-det up matrix. In an independently supplied CP-adapted UV theta3=0 branch, mass-sector tree theta is0.',
        phase_convention='Holomorphic left-SVD comparator convention of11942, Jpositive. Conjugating the entire physical mass convention flips J; conjugate B restores positiveJ in the Weyl convention. Common left thetaCP phase diag(exp(i*pi*a²/3)) is removed from both sectors. Anomalous rephasings must also transform theta3; this is not a proof the UV gauge angle iszero in the original theta coordinates.',
        criterion='For FIXED invertible real barem and desired positiveH, one Barr row exists iff C=I-m^-1 H m^-T is positive semidefinite, rank<=1, and lambda_max(C)<1. If C=c cdag, Bdag/mu=c/sqrt(1-cdag c). Forr rows replace rank<=1 by rank<=r. This is standardSchur matching, applied here to a constrained thetafamily.',
        fit_scope='Eight supplied quark comparators are fitted, not predicted. Up2parameters solve its2ratios; down3theta parameters and5realBarr parameters fit6downobservables. Overallup/down Yukawa scales supplied. No global uniqueness or naturalness.',
        physics_boundary='Compatibility of bareCP-real theta family plus one complexvectorlike row at the heavy-decoupling limit, with finite-scalecontrols. Doesnot preserve11942 old lepton predictions automatically: commonSU5 mixingmustbe reapplied. No modulus/flavon vacuum selection, H27 alignment, E6-toSM completion, upperblock protection, RG running or radiative theta protection. Barefit failure alone isnot an exclusion oftheextendedmodel.',
        prior=['11942 theta homes andsuppliedcomparators','11951 generalBarrinverse andSchurmatching; herebaremrestrictedtothetafamily','11955 commonSU5down/leptonmatching','11989 fitsfreebarem toactualCPvacuum; heretheta m retained','12004 Claude bareCPthetafit exploratorycontext, not a certifiedgeneralno-go','12001 radialthreshold protectionboundary'],
        primary=['https://arxiv.org/abs/2103.04798','https://doi.org/10.1140/epjc/s10052-018-6388-6'])

if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass12005_cp_real_theta_barr.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['max_relative_comparator_error'])
