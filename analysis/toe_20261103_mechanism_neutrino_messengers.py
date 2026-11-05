"""Renormalizable fermion-chain UV realization of the prior Dirac operators.

All Weyl charges are LEFT-handed. This is an illustrative tree-level UV model,
not a claimed unique completion or measured flavor prediction.
"""
import json,pathlib,math
import numpy as np
import sympy as s
ROOT=pathlib.Path(__file__).resolve().parents[1]

def effective(Y,lam,kappa,xi,eta,scalar,heavy=1.,Bmass=1.,v=1.):
    n=Y.shape[1];K=np.zeros((n+1,n+1),complex)
    K[:n,:n]=np.eye(n)*heavy;K[:n,n]=kappa*scalar;K[n,:n]=xi*scalar.conjugate();K[n,n]=Bmass
    A=np.column_stack([v*Y,np.zeros(3)]);B=np.zeros((n+1,3),complex)
    B[:n,:2]=lam*scalar.conjugate();B[n,2]=eta*scalar
    full=np.block([[np.zeros((3,3)),A],[B,K]])
    return -A@np.linalg.solve(K,B),full,K

def build():
    old=json.loads((ROOT/'data/toe_20261103_sterile_anomaly_operators.json').read_text())
    assert [-15,12,12]in old['all_quark_normalized_integer_sectors']
    # All symmetry-allowed one-scalar Yukawas relevant to this chain included.
    # xi is often omitted in hand-drawn triangular messenger diagrams.
    charges={'L':-1,'H':0,'nA':4,'nB':4,'nC':-5,'Phi':3,
        'N':-1,'Nc':1,'B':-2,'Bc':2}
    vertices={'LH_Nc':['L','H','Nc'],'N_Phistar_nA':['N','nA'],'N_Phi_B':['N','Phi','B'],
        'Bc_Phistar_Nc':['Bc','Nc'],'Bc_Phi_nC':['Bc','Phi','nC'],'N_Nc':['N','Nc'],'B_Bc':['B','Bc']}
    sums={k:sum(charges[x]for x in f)+(-3 if 'Phistar'in k else 0)for k,f in vertices.items()}
    assert set(sums.values())=={0}
    Y=np.array([[1,2,1],[2,1,3],[1,1,1]],complex)
    lam=np.array([[1,0],[0,1],[1,1]],complex);kap=np.array([1,2,4],complex);xi=np.array([.1,-.2,.3],complex)
    assert abs(np.linalg.det(np.column_stack([lam,kap])))>0
    rows=[]
    for eps in [1e-2,1e-3,1e-4]:
        m,full,K=effective(Y,lam,kap,xi,1.,complex(eps),v=1e-3)
        sing=np.linalg.svd(m,compute_uv=False);allm=np.linalg.svd(full,compute_uv=False)
        # Compare exact full singular masses to low-energy Schur matrix, allowing
        # the known O(v²/M²,epsilon²) kinetic-normalization corrections.
        light=np.sort(allm)[:3];schur=np.sort(sing)
        error=float(np.max(abs(light/schur-1)));assert error<.002
        rows.append(dict(scalar_over_heavy=eps,mass_singular_values=sing.tolist(),full_light_singular_values=light.tolist(),
            full_vs_Schur_relative_error=error,lightest_over_eps_squared_v=float(sing[-1]/(eps**2*1e-3)),rank=int(np.linalg.matrix_rank(m))))
    # Exact rational witness with generic nonzero reverse xi couplings.
    e=s.symbols('epsilon');Ys=s.Matrix(Y.real.astype(int));Ls=s.Matrix(lam.real.astype(int));ks=s.Matrix(kap.real.astype(int))
    xis=s.Matrix([[s.Rational(1,10),-s.Rational(1,5),s.Rational(3,10)]])
    Sch=s.eye(3)-e**2*ks*xis
    exact=-Ys*Sch.inv()*Ls.row_join(-e*ks)*e
    determinant=s.factor(exact.det());assert determinant!=0
    # Repeated stochastic controls are about rank in the specified tree topology.
    ranktwo=[];rng=np.random.default_rng(803)
    for _ in range(12):
        y=rng.normal(size=(3,2));l=rng.normal(size=(2,2));k=rng.normal(size=2);x=rng.normal(size=2)
        m,_,_=effective(y,l,k,x,1.,.02+0j)
        ranktwo.append(int(np.linalg.matrix_rank(m,tol=1e-12)))
    assert set(ranktwo)=={2}
    # Messenger states are SM singlets: all mixed anomalies vanish and pairwise
    # U1_BL gravity/cubic anomalies cancel. Their one-loop BL beta cost is real.
    new_charges=[-1,1]*3+[-2,2]
    assert sum(new_charges)==sum(q**3 for q in new_charges)==0
    extra_beta=s.Rational(2,3)*sum(q*q for q in new_charges);assert extra_beta==s.Rational(28,3)
    # Electroweak naturalness diagnostic for a non-supersymmetric O(1) heavy N.
    MN=1e16;mh=125.;trace=float(np.sum(abs(Y)**2));threshold=trace*MN**2/(8*math.pi**2)
    return dict(status='PASS_EXPLICIT_DIRAC_MESSENGER_COMPLETION_WITH_RANK_AND_COST_CONTROLS',
        left_handed_BL_charges=charges,vertex_charge_sums=sums,three_N_pairs_plus_one_B_pair=True,
        exact_dimensionless_Dirac_matrix=[[str(s.factor(z))for z in row]for row in exact.tolist()],exact_determinant=str(determinant),
        rows=rows,two_entry_messenger_random_ranks=ranktwo,new_fermion_linear_anomaly=0,new_fermion_cubic_anomaly=0,
        extra_BL_one_loop_beta=str(extra_beta),above_all_thresholds_total_BL_beta=str(s.Rational(149,3)+extra_beta),
        Higgs_threshold_input_MN_GeV=MN,Higgs_threshold_trace_YdagY=trace,
        illustrative_absolute_Higgs_mass_squared_threshold_GeV2=threshold,
        illustrative_threshold_over_125GeV_squared=threshold/mh**2,
        renormalizable_Lagrangian='Y_ia (L_i H) Nc_a + MN_ab N_a Nc_b + lambda_ar N_a Phi^dag n_r + kappa_a N_a Phi B + xi_a Bc Phi^dag Nc_a + MB B Bc + eta Bc Phi nC + h.c.; r=A,B; nA,nB=4,nC=-5; a=1..3. Ordinary non-supersymmetric Weyl Yukawas allow Phi^dag; this is NOT asserted to be a holomorphic superpotential.',
        matching='Let Kheavy=[[MN,kappa Phi],[xi Phi^dag,MB]], A=[vH Y,0], B=[[lambda Phi^dag,0],[0,eta Phi]]. The zero-momentum tree Dirac mass is -A Kheavy^-1 B. S=MN-kappa*xi*|Phi|²/MB gives mnu=-vH*Y*S^-1*[lambda Phi^dag, -kappa*eta Phi²/MB]. The allowed reverse xi vertex changes higher orders but not the column powers.',
        rank='For n entry N messengers rank(mnu)<=rank(Y)<=n at tree level, regardless of extra downstream B chains. Two cannot give three nonzero masses in this topology. Three N pairs and one B pair suffice generically; full-rank is witnessed with all allowed displayed vertices nonzero. This is not a theorem over scalar-mediated UV completions or radiative flavor structures.',
        residual_symmetry='All new singlets have Q=3(B-L) divisible3. Phi has Q9; Z9 of the declared direct product remains, before optional color-center quotient. Active/sterile Majorana operators remain forbidden just as in the prior certificate. Vectorlike heavy masses do not break this symmetry.',
        ultraviolet_cost='New SM-singlet pairs add28/3 to b_BL ABOVE their masses, so the previous exotic149/3 becomes59 there. Applying59 below a 1e16GeV messenger threshold would be incorrect. O(1) nonsupersymmetric Yukawas at that scale create a severe Higgs threshold naturalness issue; the displayed estimate is Tr(YdagY)MN²/(8pi²), a conditional order-one/scheme-dependent diagnostic, not an observed fine-tuning measurement.',
        flavor='Arbitrary complex Y,lambda,kappa and masses remain free. Their freedom permits fitting masses/mixing; the model does not predict PMNS angles, CP phase, ordering or absolute mass. The epsilon hierarchy is conditional on generic O(1) coefficients and input scalar/M.',
        prior_art='The exotic charges and Dirac seesaw are established prior physics (Ma/Srivastava2014/2015). The recent2609.06494 alternative has scalar BL1 and residualZ2, and radiative Majorana/inverse-seesaw structure; it is a different hypothesis, not a replacement for our PhiBL3 Dirac protection.',
        sources=['https://arxiv.org/abs/1411.5042','https://arxiv.org/abs/1504.00111','https://arxiv.org/abs/2609.06494'],
        boundary='Tree renormalizable nongravitational messenger model; no common SUSY/quantum-gravity completion, loop flavor protection, threshold-matched full RG flow or experimental viability fit is supplied.')

if __name__=='__main__':
    d=build();(ROOT/'data/toe_20261103_mechanism_neutrino_messengers.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],d['exact_determinant'],flush=True)
