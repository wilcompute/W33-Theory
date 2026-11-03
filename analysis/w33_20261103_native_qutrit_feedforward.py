"""Repair all outcomes of the three native holonomic Clifford generators.

Exact integer arithmetic in Q(sqrt3,i), with independent channel checks.
General projection holonomies: Oi2014; native postselected matrices: prior Nov3.
"""
import collections,itertools,json,pathlib,sys
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261031_tick_loop_rigidity import PI

def build():
    old=json.loads((ROOT/'data/w33_20261103_native_projector_holonomic_qutrit.json').read_text())
    A=np.rint(6*PI.real).astype(np.int64);B=np.rint(6*PI.imag/np.sqrt(3)).astype(np.int64)
    support=[0,3,6];w=np.exp(2j*np.pi/3);X=np.array([[0,0,1],[1,0,0],[0,1,0]],complex);Z=np.diag([1,w,w*w])
    Ds=[np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b)for a,b in itertools.product(range(3),repeat=2)]
    roots=[(2,0),(-1,1),(-1,-1)];gates=[]
    for idx in old['selected_holonomy_indices']:
        row=old['holonomies'][idx];b,c=row['pair'];RH=np.array(row['real_sqrt3_numerator']).reshape(3,3);IH=np.array(row['imaginary_times3_numerator']).reshape(3,3)
        H=(np.sqrt(3)*RH+3j*IH)/12;branches=[];choi=np.zeros((9,9),complex);tp=np.zeros((3,3),complex)
        for ra,rb,rc in itertools.product(range(3),repeat=3):
            bb=3*(b//3)+rb;cc=3*(c//3)+rc;ix=np.ix_([ra,3+ra,6+ra],support)
            R=(A[bb]@A[cc]-3*B[bb]@B[cc])[ix];I=(A[bb]@B[cc]+B[bb]@A[cc])[ix]
            assert np.array_equal(R@R.T+3*I@I.T,48*np.eye(3,dtype=int)) and np.array_equal(I@R.T,R@I.T)
            QA=R@RH.T+3*I@IH.T;QB=I@RH.T-R@IH.T
            G=(np.sqrt(3)*R+3j*I)/12;Q=(QA+1j*np.sqrt(3)*QB)/48
            byproduct=None
            for a,z in itertools.product(range(3),repeat=2):
                pa,pb=int(QA[a,0]),int(QB[a,0]);ok=pa*pa+3*pb*pb==48*48
                for j,k in itertools.product(range(3),repeat=2):
                    if j!=(k+a)%3:ok &= QA[j,k]==0 and QB[j,k]==0
                    else:
                        u,v=roots[z*k%3];ok &= 2*QA[j,k]==pa*u-3*pb*v and 2*QB[j,k]==pa*v+pb*u
                if ok:byproduct=(a,z,pa,pb);break
            assert byproduct is not None
            a,z,pa,pb=byproduct;K=Ds[3*a+z].conj().T@G/np.sqrt(27)
            assert np.max(abs(K-(pa+1j*np.sqrt(3)*pb)/48*H/np.sqrt(27)))<3e-14
            flat=K.ravel();choi+=np.outer(flat,flat.conj());tp+=K.conj().T@K
            branches.append(dict(outcomes=[ra,rb,rc],logical_byproduct=[a,z],phase_numerator=[pa,pb],phase_denominator=48,
                real_sqrt3_numerator=R.ravel().tolist(),imaginary_times3_numerator=I.ravel().tolist()))
        target=np.outer(H.ravel(),H.ravel().conj());err=float(np.max(abs(choi-target)));assert err<2e-13 and np.max(abs(tp-np.eye(3)))<2e-13
        # Readout-only error model. Wrong final trit moves the output outside the reference code.
        counts=collections.Counter()
        for true,report in itertools.product(branches,repeat=2):
            k=sum(a!=b for a,b in zip(true['outcomes'],report['outcomes']))
            if true['outcomes'][0]==report['outcomes'][0] and true['logical_byproduct']==report['logical_byproduct']:counts[k]+=1
        assert counts[0]==27
        gates.append(dict(parent_holonomy_index=idx,measurement_direction_order=[c//3,b//3,0],branches=branches,
            exact_normalized_branch_unitaries=27,branch_probability='1/27 independent of logical input',
            correction='Apply I3 tensor X^(-rA) to align the final code, then logical (X^a Z^b)^dagger on the first qutrit using this outcome lookup.',
            Choi_max_error=err,readout_fidelity_counts_by_wrong_trits={str(k):counts[k]for k in range(4)},
            readout_entanglement_fidelity='sum_k n_k/27*(1-epsilon)^(3-k)*(epsilon/2)^k',readout_code_leak_probability='epsilon'))
    return dict(status='PASS_ALL_81_NATIVE_QUTRIT_BRANCHES_CORRECTED',gates=gates,
        deterministic_projective_gate_group=216,total_measurement_branches=81,postselection_required=False,
        exact_arithmetic='Integer projector numerators (A+i sqrt3 B)/6; exact unitarity and byproduct equalities for every branch. The floating Choi sum is an additional independent check.',
        noise_assumptions='Each trit independently misreported with probability epsilon, each other value epsilon/2. True quantum projective measurements and Pauli corrections ideal. Code leakage and entanglement fidelity use the full9D output.',
        ownership='Native120 projector and postselected28-holonomy owners are imported, not rediscovered. General degenerate-projection holonomies: Oi2014.',
        reference='https://arxiv.org/abs/1402.1104',
        boundary='Deterministic ideal Clifford channel with physical Pauli feedforward as an added control resource. No non-Clifford universality, loss tolerance, fault-tolerance threshold or experimental realization.')

if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261103_native_qutrit_feedforward.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],[g['readout_fidelity_counts_by_wrong_trits']for g in d['gates']],flush=True)
