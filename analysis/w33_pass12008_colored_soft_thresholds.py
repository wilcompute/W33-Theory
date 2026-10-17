"""Full4-flavour colored one-loop benchmark on the matched theta/Barr block.

Universal soft masses and LR=aM are supplied, not derived. Exact SVD
alignment removes both quark and gluino mass phases in this channel.
Misalignment controls and the earlier neutral-scalar portal remain decisive.
"""
import json
from pathlib import Path
import numpy as np
from w33_pass12007_shared_theta_leptons import inputs
from w33_pass11952_11955_threshold_vacuum_loop_leptons import b0
ROOT=Path(__file__).resolve().parents[1]

def full_mass():
    u,m,e,b,A=inputs();M=np.zeros((4,4),complex);M[:3,:3]=m;M[3,:3]=b;M[3,3]=1
    return M

def threshold(M,epsilon=0.,alpha=.1,mg=.7,a=.3,soft2=4.):
    n=len(M);pattern=np.arange(n*n).reshape(n,n)/7-1
    LR=a*M+epsilon*pattern*M
    Sq=np.block([[M@M.conj().T+soft2*np.eye(n),LR],[LR.conj().T,M.conj().T@M+soft2*np.eye(n)]])
    val,Z=np.linalg.eigh(Sq);assert min(val)>0
    F=(Z*np.array([b0(np.array([mg*mg]),v)[0] for v in val]))@Z.conj().T
    delta=(2*alpha/(3*np.pi))*mg*F[:n,n:]
    tq=float(np.trace(np.linalg.solve(M,delta)).imag)
    U,s,Vh=np.linalg.svd(M);V=Vh.conj().T;ZL=U.conj().T@Z[:n];ZR=V.conj().T@Z[n:]
    dg=0j
    for i,m in enumerate(s):dg+=(alpha/(2*np.pi))*m*np.sum(ZL[i]*ZR[i].conj()*np.array([b0(np.array([m*m]),v)[0] for v in val]))
    tg=float(-3*dg.imag/mg)
    return dict(epsilon=epsilon,minimum_squark_mass_squared=float(min(val)),theta_quark=tq,theta_gluino=tg,theta_colored_sum=tq+tg,delta_gluino_real=float(dg.real),delta_gluino_imag=float(dg.imag),max_quark_correction=float(np.max(abs(delta))))

def payload():
    M=full_mass();aligned=threshold(M);assert abs(aligned['theta_quark'])<1e-11 and abs(aligned['theta_gluino'])<1e-11
    rows=[threshold(M,e) for e in [1e-2,1e-3,1e-4,1e-5]]
    assert abs(rows[0]['theta_colored_sum'])>1e-10
    cp=threshold(M.conj(),1e-3);assert abs(cp['theta_colored_sum']+rows[1]['theta_colored_sum'])<1e-12
    # Overall scaling of all dimensionful input leaves the phase diagnostic.
    scale=3.;scaled=threshold(scale*M,epsilon=scale*1e-3,mg=.7*scale,a=.3*scale,soft2=4*scale**2)
    assert abs(scaled['theta_colored_sum']-rows[1]['theta_colored_sum'])<1e-12
    safe=[]
    m=M[:3,:3];b=M[3,:3]
    for r in [0.,.0005,.001]:
        c=r*m@b.conj();trial=M.copy();trial[:3,3]=c;det=np.linalg.det(trial);expected=np.linalg.det(m)*(1-r*np.vdot(b,b).real)
        assert expected>0 and abs(det/expected-1)<1e-11
        safe.append(dict(r=r,determinant_real=float(det.real),determinant_imag=float(det.imag),upper_block_norm=float(np.linalg.norm(c))))
    return dict(status='PASS',safe_nonzero_upper_block=safe,safe_leak_identity='c=r m Bdag withrealr gives det[[m,c],[B,mu]]=det(m)(mu-r|B|²),realpositiveifmu>r|B|². Thisalignmentisnotprotected/derived here, wouldrequirejointrefit, andmustnotbeconfusedwithgenericallowedleak. PositiveHermitianfieldnormalizationphaseinvariance isprior11950.',aligned=aligned,real_A_nonuniversality_scan=rows,CP_partner=cp,common_scale3=scaled,
        exact_alignment_proof='IfM=U diag(s)Vdag, rotate squarks bydiag(U,V). UniversalLL/RRsoft masses andLR=aM become four REAL2x2blocks [[s²+msoft²,a s],[a s,s²+msoft²]]. Real loop spectral functions give deltaM=U diag(real)Vdag, soImTr(M^-1deltaM)=0. Quarkbasisgluinomass loop mixingproducts arereal, soImdeltaMg=0. No expansioninB/mu ormassinsertions isused.',
        declared_matching='Zeroexternalmomentum finiteB0 MSbar coloredbenchmark:deltaM=(2alpha_s/3pi)mg[B0(mg²,Sq)]LR;deltaMg=(alpha_s/2pi)sum_i,a s_i ZL_ia ZR_ia* B0(s_i²,lambda_a). theta_colored=ImTr(M^-1deltaM)-3Im(deltaMg/mg). Scalar tadpoles, EW/Higgs/neutral-scalar andhigherloop terms excluded.',
        supplied_soft_structure='M includesall4quarks andheavycomplexBarrrow. SqLL=M Mdag+4I, SqRR=MdagM+4I, SqLR=.3M. A mismatch isepsilon*realpatternHadamardM; realcouplings neednotbeuniversal.',
        boundary='SeparateSUSYcoloredsoftbenchmark, not aunifiedSUSYcompletionof11996nonSUSYscalarpotential. Alignedcoloredone-loopchannel vanishes, NOT totalradiativestrongCP. Gauge/softmediation must enforcealignment, running/messenger/Bsectorcorrections mustbe matched, and12001neutralportal persists. Raisingallmassscales doesnotremove dimensionlessmisalignment.',
        prior=['11954/11996 neutral-scalar loops doNOTinclude thiscoloredchannel','11973/11978 mediationwithoutcoloredthresholdmatrices','12005/12007 constrainedthetaBarrmatrices'],
        primary=['https://arxiv.org/abs/2002.04204','https://arxiv.org/abs/hep-ph/9709356'])

if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass12008_colored_soft_thresholds.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['real_A_nonuniversality_scan'][0]['theta_colored_sum'])
