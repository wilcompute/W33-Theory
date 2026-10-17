"""Joint CP-real theta/Barr quark and charged-lepton witness.

Prior11942 owns charge rule6;11955 owns common5bar matching;11960
owns real-Majorana texture fitting. No independent charged-lepton parameters.
All fitted numbers are supplied, with no RG/vacuum/uniqueness claim.
"""
import json
from pathlib import Path
import numpy as np
from w33_pass11942_hypercharge_wilson_leptons import theta,normalised,DATA,LEPTONS
from w33_pass12005_cp_real_theta_barr import Y,EU,observables
ROOT=Path(__file__).resolve().parents[1]
FIT=np.array([-.3497011260666278,.09754766874005429,.04188033188719437,11.279482901951425,8.059823963649515,-1.904101410788516,-6.844437562070213,-11.79584423547314])

def inputs(p=FIT):
    tau=1+1j*Y;Ou=np.array([[tau,1j*EU],[1j*EU,tau]]);Od=np.array([[tau,1j*p[1]],[1j*p[1],1j*np.exp(p[0])]])
    phase=np.exp(1j*np.pi*np.arange(3)**2/3)
    u=phase.conj()[:,None]*theta(Ou)*phase.conj()[None,:]
    d=phase.conj()[:,None]*normalised(Od,(0,1j*p[2]))
    e=phase.conj()[:,None]*normalised(Od,(0,6j*p[2]))
    assert max(abs(z.imag).max()/np.linalg.norm(z) for z in (u,d,e))<1e-12
    u=u.real/np.linalg.norm(u);norm=np.linalg.norm(d);d=d.real/norm;e=e.real/norm
    b=np.array([p[3],p[4]+1j*p[5],p[6]+1j*p[7]])
    K=np.eye(3)-np.outer(b.conj(),b)/(1+np.vdot(b,b).real);ev,O=np.linalg.eigh(K);A=(O*np.sqrt(ev))@O.conj().T
    return u,d,e,b,A

def joint_observables(p=FIT):
    u,d,e,b,A=inputs(p);q,_,_,_=observables(u,d,b);charged=A.T@e.T;se=np.linalg.svd(charged,compute_uv=False)
    lep=dict(mmu_mtau=float(se[1]/se[0]),me_mmu=float(se[2]/se[1]))
    return q,lep,charged,A

def residual(p,leptons=True):
    q,e,_,_=joint_observables(p);keys=['ms_mb','md_ms','Vus','Vcb','Vub'];r=np.r_[[np.log(q[k]/DATA[k]) for k in keys],(q['J']-DATA['J'])/DATA['J']]
    return np.r_[r,[np.log(e[k]/LEPTONS[k]) for k in ('mmu_mtau','me_mmu')]] if leptons else r

def jacobian(p,leptons=True,step=1e-5):
    return np.column_stack([(residual(p+step*v,leptons)-residual(p-step*v,leptons))/(2*step) for v in np.eye(8)])

NEUTRINO_FIT=np.array([-.20255586369293455,-.8307011736471974,.6056483156983711,-.4519628526592277,-.3915948554934204])
NEUTRINO_TARGET=np.array([.304,.573,.02219,7.42e-5/.002511])

def neutrino(p=NEUTRINO_FIT,conjugate=False):
    _,_,charged,A=joint_observables()
    if conjugate:charged=charged.conj();A=A.conj()
    L=np.array([[np.exp(p[0]),0,0],[p[2],np.exp(p[1]),0],[p[3],p[4],1.]])
    n=L@L.T;nu=A.T@n@A
    _,ue=np.linalg.eigh(charged.conj()@charged.T)
    _,singular,vh=np.linalg.svd(nu);order=np.argsort(singular);ss=singular[order];U=ue.conj().T@vh.conj().T[:,order];Q=abs(U)**2
    s13=Q[0,2];s12=Q[0,1]/(1-s13);s23=Q[1,2]/(1-s13)
    o=np.array([s12,s23,s13,(ss[1]**2-ss[0]**2)/(ss[2]**2-ss[0]**2)])
    J=float((U[0,0]*U[1,1]*U[0,1].conj()*U[1,0].conj()).imag)
    sind=J/(np.sqrt(s12*(1-s12)*s23*(1-s23)*s13)*(1-s13))
    cosd=(Q[1,0]-s12*(1-s23)-(1-s12)*s23*s13)/(2*np.sqrt(s12*(1-s12)*s23*(1-s23)*s13))
    m3=np.sqrt(.002511/(1-(ss[0]/ss[2])**2))
    return o,dict(real_bare_Majorana=n.tolist(),PMNS_abs_squared=Q.tolist(),J=J,delta_deg=float(np.degrees(np.arctan2(sind,cosd))%360),masses_eV=(ss/ss[2]*m3).tolist())

def payload():
    q,lep,charged,A=joint_observables();assert max(abs(q[k]/DATA[k]-1) for k in DATA)<1e-7
    assert max(abs(lep[k]/LEPTONS[k]-1) for k in LEPTONS)<1e-7
    sv=np.linalg.svd(jacobian(FIT),compute_uv=False);qsv=np.linalg.svd(jacobian(FIT,False),compute_uv=False)
    assert sv[-1]>1e-6 and qsv[-1]>1e-6
    u,d,e,b,A=inputs();_,_,downsv,K=observables(u,d,b)
    # Shared5bar mixing must appear on LEFT charged Weyl index.
    wrong=np.linalg.svd(e.T@A,compute_uv=False);right=np.linalg.svd(A.T@e.T,compute_uv=False)
    assert max(abs(wrong/right-1))>.01
    nu,nudata=neutrino();assert max(abs(nu/NEUTRINO_TARGET-1))<1e-7
    nuc,nucdata=neutrino(conjugate=True);assert max(abs(nuc-nu))<1e-12 and abs(nucdata['J']+nudata['J'])<1e-12
    return dict(status='PASS',neutrino_observables=nu.tolist(),neutrino_fit_parameters=NEUTRINO_FIT.tolist(),neutrino= nudata,neutrino_CP_partner=nucdata,neutrino_boundary='RealpositiveMajorana5shapeparameters fit4oscillationcomparators withsamecomplexA. No newCPphase; neutrino1localparameterfree, so displayedmassscale/delta areconditionalwitnessvalues notpredictions. Fourparameterzero23texture search stalled atlogresidual0.13845, not a globalno-go.',fitted_down_parameters=FIT.tolist(),up_height=Y,up_entangler=EU,
        quark_comparators_matched=q,charged_lepton_ratios=lep,shared_A_real=A.real.tolist(),shared_A_imag=A.imag.tolist(),real_bare_down=d.tolist(),real_bare_charged_transpose=e.tolist(),
        all_eight_down_plus_charged_residual=residual(FIT).tolist(),local_joint_Jacobian_singular_values=sv.tolist(),quark_only_Jacobian_singular_values=qsv.tolist(),
        local_fit_fibre='Quark-only6x8 Jacobian hasrank6:two localfree directions. Adding2chargedratios gives8x8rank8 inthismarkedparameterization; implicitfunctiontheorem gives locallyisolated fits, not a scalarvacuum or globaluniqueness.',
        common_matching='K=I-bdag b/(1+|b|²),A=sqrt(K);Md=md A and chargedWeylMe=A^T me_bare, me_bare=[Theta(Omega_d,z_e=6z_d) in sameCPbasis]^T. No separate chargedlepton fitparameters.',
        supplied_scales='Allquark andchargedlepton ratios compared at prior11942suppliedMZvalues. Overallup/downcouplings arefree. The absolute b/tau relation requires RG/threshold matching; it is not inferred from separatelynormalized fields.',
        direct_yb_over_ytau_same_normalization=float(downsv[0]/right[0]),heldout_MZ_b_over_tau=2.86/1.74624,heldout_b_tau_fractional_error=float((downsv[0]/right[0])/(2.86/1.74624)-1),heldout_boundary='AtthesameMZcomparison scale theunifiednormalizationgivesb/tau about1.002 vs1.638:FAIL. Fourteenratio/mixingcomparatorsdonotinclude thisadditionalabsoluteintersectorratio. RG and/or threshold/gaugeembeddingchanges mustbe explicitlycomputed, not assumed.',
        field_convention='Holomorphic11942 convention for signedquarkJ. ConjugationflipsJ; physicalWeyl convention requires consistentconjugationofallcharged/neutrino matrices.',
        scope='Numericaljointcompatibility, not predictedmasses,globalfitcensus,fieldvacuum,RGunification or strongCPprotection. Actualmodulistabilization remainsopen. The classallows8downparameters tofit8down/chargedobservables.',
        prior=['11942 gaugeinvariantcharge6 andbarethetafit','11955 commonSU5heavy5barmatching','11960 realMajorana4parametertexture','12005 CP-realtheta plusBarrquarkwitness'])

if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass12007_shared_theta_leptons.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['local_joint_Jacobian_singular_values'][-1])
