"""One-loop coupled Abelian UV test of the declared Dirac B-L sectors.

Gauge-kinetic matrix conventions keep kinetic mixing explicit. Standard RG
framework: Basso-Moretti-Pruna1004.3039; no new generic RG theorem claimed.
"""
import hashlib,json,math,pathlib
import numpy as np
import sympy as s
ROOT=pathlib.Path(__file__).resolve().parents[1]

def build():
    parent='data/toe_20261103_sterile_anomaly_operators.json';raw=(ROOT/parent).read_bytes();old=json.loads(raw)
    # multiplicity, hypercharge, B-L; three observed SM generations.
    sm=[(18,s.Rational(1,6),s.Rational(1,3)),(9,-s.Rational(2,3),-s.Rational(1,3)),
        (9,s.Rational(1,3),-s.Rational(1,3)),(6,-s.Rational(1,2),-1),(3,1,1)]
    F=sum((n*s.Matrix([y,b])*s.Matrix([[y,b]])for n,y,b in sm),s.zeros(2))
    assert F[0,0]==10 and F[0,1]==8 and F[1,1]==13
    scalars=s.Matrix([[s.Rational(1,2),0],[0,9]]) # one SM doublet, one Phi(B-L=3)
    rows=[];gy=.36;matching=3000.;epsilon=.05/174e9;logcut=math.log(1/epsilon);cutoff=matching/epsilon
    for charges in old['all_quark_normalized_integer_sectors']:
        FF=F+s.diag(0,sum(s.Rational(q,3)**2 for q in charges))
        B=s.Rational(2,3)*FF+s.Rational(1,3)*scalars
        assert B[0,0]==s.Rational(41,6) and B[0,1]==s.Rational(16,3)
        BB=np.array(B,dtype=float);a=logcut/(8*math.pi**2);kyy=1/gy**2-a*BB[0,0];assert kyy>0
        cap=1/math.sqrt(a*BB[1,1]+a*a*BB[0,1]**2/kyy)
        scans=[]
        for gb in [.1,.2,.4]:
            K0=np.diag([1/gy**2,1/gb**2]);Kcut=K0-a*BB
            G=np.diag([gy,gb]);largest=np.linalg.eigvalsh(G@BB@G)[-1]
            lp=8*math.pi**2/largest
            # Independent determinant polynomial and a nonorthogonal gauge basis.
            T=np.array([[1.,0.],[-1.,1.]])
            assert abs(np.linalg.det(T@Kcut@T.T)-np.linalg.det(Kcut))<1e-10
            Kpole=K0-lp/(8*math.pi**2)*BB;assert abs(np.linalg.det(Kpole))<2e-12
            scans.append(dict(gBL_input=gb,log_Landau_scale_over_matching=lp,one_loop_Landau_scale_GeV=matching*math.exp(lp),
                inverse_kinetic_eigenvalues_at_operator_cutoff=np.linalg.eigvalsh(Kcut).tolist(),positive_kinetic_through_operator_cutoff=bool(np.linalg.eigvalsh(Kcut)[0]>0)))
        rows.append(dict(sterile_Q=charges,beta_matrix=[[str(z)for z in row]for row in B.tolist()],
            gBL_upper_bound_no_one_loop_pole_through_cutoff=cap,scans=scans))
    standard=next(r for r in rows if r['sterile_Q']==[3,3,3]);exotic=next(r for r in rows if r['sterile_Q']==[-15,12,12])
    assert s.sympify(standard['beta_matrix'][1][1])==s.Rational(41,3)
    assert s.sympify(exotic['beta_matrix'][1][1])==s.Rational(149,3)
    assert s.Rational(2,3)*16+s.Rational(1,3)*4==12 # usual Phi(B-L=2) control
    # X=5(B-L)-4Y is orthogonal to Y on complete SM+sterile fermions.
    # A lone light Higgs doublet breaks this cancellation in the full beta trace.
    T=s.Matrix([[1,0],[-4,5]])
    fermion_cross=(T*F*T.T)[0,1];scalar_cross=(T*scalars*T.T)[0,1]
    assert fermion_cross==0 and scalar_cross==-2
    triplet=3*s.Matrix([-s.Rational(1,3),-s.Rational(2,3)])*s.Matrix([[-s.Rational(1,3),-s.Rational(2,3)]])
    assert (T*(scalars+triplet)*T.T)[0,1]==0
    return dict(status='PASS_COUPLED_ABELIAN_UV_AND_SCALAR_THRESHOLD_CONTROLS',rows=rows,
        parent_input={parent:hashlib.sha256(raw).hexdigest()},kinetic_convention='D=partial-i q_a A_a, Lkin=-1/4 F_a K_ab F_b. K(matching)=diag(gY^-2,gBL^-2) is a supplied zero-mixing boundary condition.',
        exact_one_loop_running='K(mu)=K(matching)-B*log(mu/matching)/(8pi^2), B_ab=(2/3)Tr_Weyl(q_a q_b)+(1/3)Tr_complex_scalar(q_a q_b). The offdiagonal is retained; independent diagonal running would be incomplete.',
        input_spectrum='Three SM generations, one Higgs doublet, the indicated three singlets, and Phi of B-L=3, all active above the common matching scale. No intermediate thresholds are assumed.',
        spectrum_controls=dict(SM_fermion_trace_Y2=10,SM_fermion_trace_Y_BL=8,SM_fermion_trace_BL2=13,
            bY='41/6',bY_BL='16/3',bBL_standard_Phi3='41/3',bBL_exotic_Phi3='149/3',usual_standard_Phi2_bBL='12'),
        operator_scale_example=dict(matching_scale_GeV=matching,gY_input=gy,heavy_neutrino_mass_input_eV=.05,vH_eV=174e9,
            epsilon_estimate=epsilon,operator_cutoff_GeV=cutoff),
        physical_scope='Positive K up to the cutoff is a one-loop no-pole criterion, weaker than a full perturbativity, scalar-stability or UV-completion proof. Couplings and thresholds are inputs. New gauge structure below a pole or a different spectrum changes the test.',
        orthogonality_control=dict(generator='X=5(B-L)-4Y',fermion_Y_X_trace=0,light_Higgs_Y_X_scalar_trace=-2,
            total_mixed_one_loop_trace_coefficient='-2/3',complete_Higgs5_scalar_trace=0,
            explanation='Complete fermion multiplets alone do not prevent mixing below scalar thresholds. The light Higgs doublet has X=-2. A color triplet with Y=-1/3,B-L=-2/3,X=-2 restores the scalar trace cancellation when both are active. X is used as a charge diagnostic; no primitive global charge-lattice relabeling is assumed.'),
        basis_control='An explicit nonorthogonal gauge-field basis change with determinant1 preserves det K and the pole. The charge lattice and all kinetic entries are carried together; this is not a silent change of global gauge group.',
        source='https://arxiv.org/abs/1004.3039',
        ownership='Standard B-L running and kinetic-mixing thresholds are prior physics. This tests the actual single-Phi9 Dirac operator sectors with their different sterile charges, rather than using anomaly cancellation as a UV-completion claim.',
        boundary='Declared one-loop EFT consistency check, not gauge unification, selected couplings, quantum-gravity fixed point or a complete TOE.')

if __name__=='__main__':
    d=build();(ROOT/'data/toe_20261103_abelian_uv_matching.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],[(r['sterile_Q'],r['gBL_upper_bound_no_one_loop_pole_through_cutoff'])for r in d['rows']],flush=True)
