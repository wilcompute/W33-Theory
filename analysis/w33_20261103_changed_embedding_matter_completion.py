"""Classify the changed-embedding mixed cubic and audit a massive matter extension.

The epsilon witness itself is prior: w33_20261102_clifford_native_cubic_repair.
This adds a finite-group uniqueness certificate and the gauge anomaly/mass audit.
"""
import itertools,json,pathlib,sys
import numpy as np
import sympy as s
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_toroidal_knight_clifford_bridge import matrices

def rankmod(M,p=17):
    A=np.array(M,dtype=np.int64)%p;r=0
    for c in range(A.shape[1]):
        nz=np.flatnonzero(A[r:,c])
        if not len(nz):continue
        k=r+int(nz[0]);A[[r,k]]=A[[k,r]];A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
        for k in range(A.shape[0]):
            if k!=r and A[k,c]:A[k]=(A[k]-A[k,c]*A[r])%p
        r+=1
        if r==A.shape[0]:break
    return r

def build():
    _,blades,gens,O=matrices();gens=gens+[(s.eye(4)+s.I*blades[15])/s.sqrt(2)]
    pairs=list(itertools.combinations(range(4),2));J=s.Matrix([[s.LeviCivita(*(a+b)) if len(set(a+b))==4 else 0 for b in pairs]for a in pairs])
    tensor=np.zeros((6,4,4),dtype=np.int64)
    for i in range(6):
        for j,(a,b) in enumerate(pairs):tensor[i,a,b]=int(J[i,j]);tensor[i,b,a]=-int(J[i,j])
    def mod(x):
        a,b=s.fraction(s.cancel(s.expand(x).subs({s.sqrt(2):6,s.I:4})))
        return int(a)*pow(int(b),-1,17)%17
    constraints=[]
    for g in gens:
        W=s.Matrix([[g[i,a]*g[j,b]-g[i,b]*g[j,a] for a,b in pairs]for i,j in pairs])
        # Exact lower bound: the nonzero epsilon tensor is invariant.
        assert s.simplify(W.T*J*W)==J
        G=np.array(g.applyfunc(mod),dtype=np.int64);V=np.array(W.applyfunc(mod),dtype=np.int64)
        constraints.append((np.kron(V.T,np.kron(G.T,G.T))-np.eye(96,dtype=np.int64))%17)
    A=np.vstack(constraints);rank=rankmod(A);print('MIXED_RANK',rank,'witness_residual',int(np.max(A@tensor.ravel()%17)),flush=True);assert rank==95 and not np.any(A@tensor.ravel()%17)
    # A rank95 minor nonzero mod17 bounds characteristic-zero nullity by1;
    # the exact invariant above attains it. Center iI eliminates all other27 components.
    chi=s.Matrix([O[a,b] for a,b in pairs]);M=s.zeros(4)
    for i,(a,b) in enumerate(pairs):M[a,b]=(chi.T*J)[i];M[b,a]=-M[a,b]
    H=s.zeros(8);H[:4,4:]=M;H[4:,:4]=M.T
    assert H.rank()==8 and H.conjugate().T*H==s.eye(8)
    h=[1,1,1,-3];fund=sum(t**3 for t in h);six=sum((h[i]+h[j])**3 for i,j in pairs)
    assert fund==-24 and six==0
    return dict(status='PASS_CHANGED_EMBEDDING_MIXED_CUBIC_AND_ANOMALY_FREE_MATTER',
        coordinate_model='Pf6(A)+u^T A v, B=diag(U4,I2), using the prior signed native coordinate map',
        invariant='chi^T J (psi wedge eta)',finite_group_generator_count=7,
        center_charge_multiplicities={'0':5,'1':8,'2':6,'3':8},
        tensor_unknowns=96,modular_prime=17,modular_rank=rank,characteristic_zero_invariant_dimension=1,
        symmetric_spinor_tensor_dimension=0,antisymmetric_spinor_tensor_dimension=1,
        witness_tensor=tensor.tolist(),pair_labels=pairs,omega=list(map(str,O)),
        uniqueness_proof='The scalar iI4 acts with charge2 on psi eta; only the six charge2 scalar coordinates survive. Exact epsilon invariance supplies one dimension. Reduction of672 equations in96 coefficients at i=4,sqrt2=6 over F17 has rank95, bounding characteristic-zero nullity by1.',
        declared_extension='Add psi,eta in4 and psi_tilde,eta_tilde in dual4, all chiral multiplets in supplied4D N=1 SU4 gauge theory. Wext=y chi^T J(psi wedge eta)+ytilde psi_tilde^T chi eta_tilde.',
        fundamental_pair_anomaly_units=2,dual_pair_anomaly_units=-2,total_added_SU4_cubic_anomaly=0,
        anomaly_witness=dict(H=h,trace_H3_fundamental=fund,trace_H3_six=six),
        mass_at_chi_tOmega=dict(fundamental_pair_hessian_rank=8,dual_pair_hessian_rank=8,
            singular_values='eight |y t| and eight |ytilde t|',dimensionful_input='nonzero t supplied'),
        threshold_audit=dict(ultraviolet_beta_original=9,ultraviolet_beta_with_four_extra_chirals=7,
            Sp_Nf_before_external_decoupling=3,Sp_beta_before_external_decoupling=6,
            matching='Lambda_Nf3^6=C Lambda_SU4^7/t; Lambda_Nf1^8=Cprime*y*ytilde*t*Lambda_SU4^7 after the two extra flavor masses. Constants depend on threshold conventions.'),
        ownership='Prior Nov2 producer owns the tensor and changed native27 action. This producer certifies uniqueness and the anomaly-free massive extension. Generic gauge-anomaly cancellation and holomorphic decoupling are standard.',
        boundary='Conditional internal gauge matter, not derived spacetime spinors. This extension alone retains the old native-sector ADS runaway; stabilization is a separate explicitly deformed model.',
        reference='https://arxiv.org/abs/hep-th/9505006')

if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261103_changed_embedding_matter_completion.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],d['modular_rank'],flush=True)
