#!/usr/bin/env python3
"""Pure-vs-mixed F8 regulus lower bound falsifier.

Find an isotropic PAULI subgroup entirely outside the 567 covered operators.
The maximally mixed state on its common eigenspace has covered sum of
squared Pauli expectations exactly ZERO, even at nontrivial purity.
This cannot disprove a bound restricted to PURE 6-qubit states.
"""
import sys,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261115_F8_mixed_uncovered_stabilizer.json"
sys.path.insert(0,str(ROOT/"analysis"))
code=(ROOT/"analysis"/"w33_regulus_constants_q16_q32.py").read_text()
g={"__file__":str(ROOT/"analysis"/"w33_regulus_constants_q16_q32.py"),
   "__name__":"f8_field"}
exec(code[:code.index("def model(")],g)
q,mul,trace=g["field"](3); assert q==8
mask=7; v=np.arange(4096,dtype=np.int64)
x1,x2,z1,z2 = (v&mask,(v>>3)&mask,(v>>6)&mask,(v>>9)&mask)
M=np.array([[mul(a,b) for b in range(8)] for a in range(8)])
tr=np.array([trace(i) for i in range(8)])
covered=(M[x1,z1]^M[x2,z2])==0
assert covered.sum()==568 and covered[0]
uncovered=~covered
def symp(w):
    a,b,c,d=(int(w)&mask,(int(w)>>3)&mask,(int(w)>>6)&mask,(int(w)>>9)&mask)
    return tr[M[a,z1]^M[b,z2]^M[c,x1]^M[d,x2]]==0
def candidates(span,basis):
    good=uncovered.copy()
    for s in span:good &= uncovered[v^s]
    for b in basis:good &= symp(b)
    good[span]=False
    return np.flatnonzero(good)
def run(seed=908):
    rng=np.random.default_rng(seed)
    result=None;hist={}
    for trial in range(500):
        span=np.array([0],dtype=np.int64)
        basis=[]
        for k in range(6):
            opts=candidates(span,basis)
            if not len(opts):break
            t=int(rng.choice(opts))
            basis.append(t)
            span=np.concatenate((span,span^t))
            assert all(uncovered[s] for s in span if s)
            assert all(symp(b)[c] for b in basis for c in basis)
        hist[len(basis)]=hist.get(len(basis),0)+1
        if result is None or len(basis)>len(result[0]):
            result=(basis,span.copy(),trial)
            print("BEST ISOTROPIC DIMENSION",len(basis),"trial",trial,flush=True)
        if len(basis)>=5:break
    basis,span,trial=result
    rank=len(basis)
    # Independent actual 64x64 density-matrix check (not just a label
    # subspace): commuting Hermitian six-qubit Pauli generators project
    # onto a two-dimensional code. Tr(rho P)^2 is evaluated directly.
    def physical_binary_masks(w):
        x=int(w)&63
        z1=(int(w)>>6)&7;z2=(int(w)>>9)&7
        dual1=sum(int(tr[M[1<<j,z1]])<<j for j in range(3))
        dual2=sum(int(tr[M[1<<j,z2]])<<j for j in range(3))
        # Trace-dual conversion: parity(x&zmask) =
        # Tr_F8(x1*z1+x2*z2). Raw F8 coordinates are NOT a
        # self-dual qubit Z coordinate basis.
        return x,dual1|(dual2<<3)
    def hermitian_pauli(w):
        x,z=physical_binary_masks(w)
        ph=1j if (int(x&z).bit_count()%2) else (1+0j)
        H=np.zeros((64,64),dtype=complex)
        for k in range(64):
            H[k^x,k]=ph*((-1)**((z&k).bit_count()))
        assert np.allclose(H,H.conj().T)
        return H
    projector=np.eye(64,dtype=complex)
    for b in basis:
        projector=projector@(np.eye(64,dtype=complex)+hermitian_pauli(b))/2
    assert np.allclose(projector@projector,projector,atol=1e-12)
    assert abs(np.trace(projector)-64/(1<<rank))<1e-12
    rho=projector/np.trace(projector)
    assert abs(np.trace(rho@rho).real-(1<<rank)/64)<1e-12
    def pauli_exp(w,rho_):
        x,z=physical_binary_masks(w)
        ph=1j if ((x&z).bit_count()%2) else (1+0j)
        return ph*sum(rho_[i,i^x]*(-1)**((z&i).bit_count())
                      for i in range(64))
    covered_list=[int(w) for w in v if int(w) and covered[w]]
    moments=[abs(pauli_exp(w,rho))**2 for w in covered_list]
    assert max(moments)<1e-22
    logical_counts=[]
    logical_reps=[]
    if rank==5:
        commutes=np.ones(4096,dtype=bool)
        for b in basis:commutes &= symp(b)
        assert int(commutes.sum())==128
        seen=set()
        for rep in np.flatnonzero(commutes):
            if int(rep) in seen:continue
            coset=[int(rep)^int(s) for s in span]
            seen.update(coset)
            if rep not in span:
                logical_reps.append(int(rep))
                logical_counts.append(int(sum(covered[x] for x in coset)))
        assert len(logical_counts)==3 and len(seen)==128
        assert min(logical_counts)>=3  # prior exact stabilizer exclusion
        assert logical_counts==[3,3,3]
        for bloch in (0,.25,.6,1):
            pure_logical=hermitian_pauli(logical_reps[0])
            state=rho@(np.eye(64,dtype=complex)+bloch*pure_logical)
            assert abs(np.trace(state)-1)<1e-12
            target_purity=(1+bloch*bloch)/2
            assert abs(np.trace(state@state).real-target_purity)<1e-11
            c_value=sum(abs(pauli_exp(w,state))**2 for w in covered_list)
            assert abs(c_value-3*bloch*bloch)<1e-11
    if rank>=5:
        assert len(span)==1<<rank and len(set(span))==(1<<rank)
        assert not any(covered[s] for s in span if s)
        # Projector onto one +1 common eigenspace has dimension 2^(6-r).
        rank_density=64//(1<<rank)
        purity=1/rank_density
    else:rank_density=64//(1<<rank);purity=1/rank_density
    data={
     "status":"EXACT_UNCOVERED_ISOTROPIC_SUBSPACE_CONSTRUCTION",
     "seed":seed,"trials_executed":sum(hist.values()),
     "best_isotropic_dimension":rank,
     "basis":basis,"all_labels_in_span":list(map(int,span)),
     "covered_nonidentity_labels":int(covered.sum()-1),
     "uncovered_nonidentity_labels":int(uncovered.sum()),
     "all_nonzero_subspace_labels_uncovered":True,
     "trace_dual_field_basis_conversion":True,
     "direct_64x64_stabilizer_projector_verified":True,
     "max_squared_covered_moment_in_rank2_mixed_state":float(max(moments)),
     "matrix_level_bloch_radii_verified":[0,.25,.6,1],
     "logical_coset_representatives":logical_reps,
     "covered_Pauli_counts_in_three_logical_cosets":logical_counts,
     "exact_purity_dependent_objective_in_this_code":"C(r)=cx*rx^2+cy*ry^2+cz*rz^2; Tr(rho^2)=(1+rx^2+ry^2+rz^2)/2",
     "minimal_C_at_fixed_purity_in_code":"(2*purity-1)*min(logical_coset_covered_counts) for purity between 1/2 and 1",
     "maximally_mixed_stabilizer_code_rank":rank_density,
     "state_purity_Tr_rho_squared":purity,
     "covered_Pauli_expectation_square_sum":0,
     "exact_pure_vs_mixed_scope":"The state is mixed unless rank=6. For pure stabilizers q8 prior Pass12661 proves covered count >=3. A mixed state with covered expectation sum zero does not contradict the pure-state c8 upper witness.",
     "search_limits":"Random constructive search; does not prove no higher-dimensional isotropic subgroup if rank <6."
    }
    OUT.write_text(json.dumps(data,indent=2)+"\n")
    return data
if __name__=="__main__":
    print(json.dumps(run(),indent=2))
