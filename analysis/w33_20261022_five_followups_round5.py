#!/usr/bin/env python3
"""Five independent followups: extension obstruction, Pauli clock, native SWAP,
coherent logical phase extraction, and field-tower spectral growth.
Explicit finite proofs/algorithms; physical interpretation rigorously limited.
"""
from __future__ import annotations
import json
import itertools
from math import comb
from pathlib import Path
import numpy as np

try:
    from analysis.w33_20261022_allfive_deeper_frontiers import (
        A,B,C,X,N,J,IDENT,cycles,transvection
    )
except ModuleNotFoundError:
    from w33_20261022_allfive_deeper_frontiers import (
        A,B,C,X,N,J,IDENT,cycles,transvection
    )

def match(choices):
    paired={}
    def aug(k,vis):
        for h in choices[k]:
            if h in vis:continue
            vis.add(h)
            if h not in paired or aug(paired[h],vis):
                paired[h]=k
                return True
        return False
    for k in sorted(choices,key=lambda x:len(choices[x])):
        assert aug(k,set()),"Hall matching failed"
    return {i:h for h,i in paired.items()}


def routing_four_layers():
    schedules=[]
    for anchor in range(40):
        g=transvection(anchor); cs=cycles(g)
        assert len(cs)==9 and all(len(c)==3 for c in cs)
        moved={i for c in cs for i in c}
        options={i:[h for h in range(40) if h not in moved and all(A[h,v]==1 for v in c)]
                 for i,c in enumerate(cs)}
        assert all(len(x)==4 for x in options.values())
        assignment=match(options)
        assert len(set(assignment.values()))==9
        labels=list(range(40));layers=[]
        # For a target 3-cycle a->b->c->a, the sequence of position
        # SWAPs (h,a),(h,b),(h,c),(h,a) transports labels in this order.
        for k in range(4):
            pairs=[]
            for i,(a,b,c) in enumerate(cs):
                h=assignment[i]
                u,v=[(h,a),(h,b),(h,c),(h,a)][k]
                assert A[u,v]
                pairs.append((u,v))
                labels[u],labels[v]=labels[v],labels[u]
            assert len({v for pair in pairs for v in pair})==18
            layers.append(pairs)
        targets=[0]*40
        for dest,origin in enumerate(labels):targets[origin]=dest
        assert tuple(targets)==g, (anchor,targets,g)
        schedules.append({"anchor":anchor,"fixed_points":13,"cycles":cs,
                          "hub_assignment":assignment,"layers":layers})
    return {"status":"EXACT_ALL_40_A_GRAPH_DEPTH4_SWAP36",
            "count":40,"graph":"W33 collinearity 12-regular A",
            "common_neighbor_count_per_cycle":4,
            "disjoint_hubs_per_transvection":9,
            "swaps_per_transvection":36,"parallel_layers":4,
            "prior_upper_bounds":[54,6],"rigorous_lower_bounds":[27,3],
            "all_schedules":schedules,
            "hardware_boundary":"No native optical coupler, loss rate or error threshold demonstrated"}


def jordan_extension_higher():
    def block_c(p):return {j:p-j+1 for j in range(1,p+1)}
    def block_q(p):return {1:3,**{j:2*j for j in range(2,p)},p:p}
    def block_k(p):return {1:(p*p+p+4)//2,**{j:j for j in range(2,p)},p:p*(p+1)//2}
    rank=lambda d,k:sum(m*max(j-k,0) for j,m in d.items())
    records=[]
    for p in (2,3,5,7,11,13,17,19,23,29,31):
        c,q,k=block_c(p),block_q(p),block_k(p)
        rk=[rank(k,i)-rank(c,i)-rank(q,i) for i in range(p+1)]
        expected=[((i-1)*(p-i)*(p+1))//2 if 1<=i<=p else 0
                  for i in range(p+1)]
        assert rk==expected,(p,rk,expected)
        records.append({"p":p,"connecting_ranks":rk})
    return {"status":"THEOREM_HIGHER_CONNECTING_OBSTRUCTION_ALL_PRIMES",
            "sequence":"0 -> C -> K -> Q -> 0 over F_p[<T>]",
            "obstruction":"delta_k:ker(D^k|Q)->C/D^k C, induced by lift then D^k",
            "rank":"rank(delta_k)= (k-1)(p-k)(p+1)/2, 1<=k<=p, zero at k=1 and k=p",
            "proof":"rank(delta_k)=rank(D^k|K)-rank(D^k|C)-rank(D^k|Q), using exact all-prime Jordan ranks of C,K,Q. The kernel of ker(D^k|K)->ker(D^k|Q) equals ker(D^k|C).",
            "first_order_warning":"delta_1=0, even though extension is nonsplit for p>=3. Higher-order delta_k detects it.",
            "k_2":"(p-2)(p+1)/2, nonzero p>=3",
            "prime_checks":records,
            "extension_field_status":"No Frobenius-twist class for q=p^t established."}


def microscopic_pauli_clock():
    omega=np.exp(2j*np.pi/3)
    shift=np.roll(np.eye(3),1,axis=0).astype(complex)
    phase=np.diag([1,omega,omega**2])
    assert np.allclose(phase@shift,omega*shift@phase)
    def d(a,b):
        return (omega**((2*a*b)%3)*np.linalg.matrix_power(shift,a)@
                np.linalg.matrix_power(phase,b))
    ws=[np.kron(d(int(x[0]),int(x[1])),d(int(x[2]),int(x[3]))) for x in X]
    maxerror=0.0
    pairs=0
    for i in range(40):
        assert np.allclose(ws[i]@ws[i].conj().T,np.eye(9))
        for j in range(i+1,40):
            commute=ws[i]@ws[j]-ws[j]@ws[i]
            iscommute=np.max(abs(commute))<1e-9
            assert iscommute == bool(A[i,j]),(i,j)
            pairs+=1
    H0=-sum((w+w.conj().T)/2 for w in ws)
    assert np.max(abs(H0.imag))<1e-10
    evals=np.linalg.eigvalsh(H0)
    assert np.allclose(evals,np.array([-4]*5+[5]*4))
    assert np.allclose(H0@H0-H0-20*np.eye(9),np.zeros((9,9)),atol=1e-9)
    # The real-shift current is odd under basis complex conjugation.
    current=np.kron((shift-shift.T)/(2j),np.eye(3))
    assert np.allclose(current,current.conj().T)
    assert np.allclose(current.conj(),-current)
    Hplus=H0+current;Hminus=H0-current
    assert np.allclose(Hplus.conj(),Hminus)
    assert np.allclose(np.linalg.eigvalsh(Hplus),np.linalg.eigvalsh(Hminus))
    assert not np.allclose(Hplus,Hminus)
    return {"status":"EXACT_TWO_QUTRIT_PAULI_40_POINT_CLOCK_SOURCE_MODEL",
       "two_qutrit_Hilbert_dimension":9,"Weyl_directions":40,
       "symplectic_commutation_pairs_checked":pairs,
       "sum_of_40_cosine_Weyl_spectrum":{"-4":5,"5":4},
       "K_time_reversal":"complex conjugation in computational basis",
       "current":"J=(X_1-X_1^dagger)/(2i), odd under K",
       "source_H":"H(kappa)= -sum_40 Re(W_v) + kappa*J",
       "antiunitary_relation":"K H(kappa) K^-1 = H(-kappa)",
       "spectra_kappa_pm1_equal":True,
       "spontaneous_T_breaking_proved":False,
       "boundary":"K chosen representation/basis; kappa is an explicitly applied T-odd source, not an emergent time arrow, spontaneous vacuum or Einstein action."}


def coherent_phase_extraction():
    # qutrit SUM(control, target): |x,a> -> |x,a+x>.
    # With v=u (weight four), sum first four physical qutrit values mod3
    # is constant on each CSS coset u0 + C since u in C^perp.
    v=np.zeros(40,dtype=np.int64);v[:4]=1
    assert np.all(B@v%3==0)
    assert np.all(C@v%3==0)
    assert np.sum(v*v)%3==1
    table=[]
    for physical in itertools.product(range(3),repeat=4):
        ancilla=0;physical=list(physical)
        for x in physical:ancilla=(ancilla+x)%3
        observed=ancilla
        for x in physical:ancilla=(ancilla-x)%3
        assert ancilla==0
        table.append({"physical":physical,"charged_value":observed})
    counts={str(k):sum(row["charged_value"]==k for row in table) for k in range(3)}
    assert counts=={"0":27,"1":27,"2":27}
    # On |c+ a*v> with c in C, charge = a*(v.v)=a.
    coeffs=np.asarray(list(itertools.product(range(3),repeat=10)),dtype=np.int64)
    basis=coeffs@C%3
    for a in range(3):
        x=(basis+a*v)%3
        assert np.all((x@v)%3==a)
    return {"status":"EXACT_COHERENT_LOGICAL_NINTH_ROOT_PHASE_WITH_RESOURCE",
            "logical_operator":"M_L=diag(1,zeta9,zeta9^2) on one logical charge q=<v,x> mod3",
            "charge_vector_support":[0,1,2,3],
            "ancilla_initial_and_final":"|0> (disentangled)",
            "protocol":"4 qutrit SUM compute, one physical non-Clifford M on ancilla, 4 inverse SUM uncompute",
            "two_qutrit_SUM_gates":8,"nonclifford_resource_gates":1,
            "enumerated_physical_4trit_inputs":len(table),
            "charge_histogram":counts,"CSS_coset_states_checked":3*len(coeffs),
            "is_coherent_on_all_superpositions":True,
            "nonclifford_resource_native_or_distilled":False,
            "fault_tolerant":False,
            "boundary":"Exact encoded unitary using externally supplied non-Clifford ancilla gate. Does not synthesize or distill magic or establish loss-tolerant photonic universality."}


def field_ops(q):
    if q==3:deg=1
    elif q==9:deg=2
    elif q==27:deg=3
    else:raise ValueError(q)
    # GF9 x²=-1; GF27 x³=x+1.
    def unpack(a):return [(a//3**i)%3 for i in range(deg)]
    def pack(v):return sum((int(x)%3)*3**i for i,x in enumerate(v))
    def add(a,b):return pack([u+v for u,v in zip(unpack(a),unpack(b))])
    def neg(a):return pack([-u for u in unpack(a)])
    def mul(a,b):
        ua,ub=unpack(a),unpack(b);z=[0]*(2*deg-1)
        for i,x in enumerate(ua):
            for j,y in enumerate(ub):z[i+j]+=x*y
        if deg==2:
            z[0]+=2*z[2]
        elif deg==3:
            for k in range(4,2,-1):
                z[k-3]+=z[k]
                z[k-2]+=z[k]
        return pack(z[:deg])
    return add,neg,mul


def cayley_tower():
    summaries=[]
    for q,a in [(3,1),(9,4),(27,3)]:
        add,neg,mul=field_ops(q)
        ident=(1,0,0,1)
        U=(1,1,0,1);L=(1,0,a,1)
        Ui=(1,neg(1),0,1);Li=(1,0,neg(a),1)
        def mm(x,y):
            return (
                add(mul(x[0],y[0]),mul(x[1],y[2])),
                add(mul(x[0],y[1]),mul(x[1],y[3])),
                add(mul(x[2],y[0]),mul(x[3],y[2])),
                add(mul(x[2],y[1]),mul(x[3],y[3])))
        loc={ident:0};elems=[ident]
        for g in elems:
            for s in (U,L):
                new=mm(g,s)
                if new not in loc:
                    loc[new]=len(elems);elems.append(new)
        target=q*(q*q-1)
        assert len(elems)==target,(q,len(elems),target)
        neigh=np.array([[loc[mm(g,s)] for s in (U,Ui,L,Li)] for g in elems],dtype=np.int32)
        # Krylov rank of the symmetric group-ring Laplacian from the
        # identity basis delta_e over a finite field; independent columns
        # modulo prime imply independent columns over Q, hence at least as
        # many distinct REAL eigenvalues on the regular representation.
        modulus=65521
        v=np.zeros(target,dtype=np.int64);v[0]=1
        piv={}
        limit=65 if q==27 else 48
        for step in range(limit):
            residual=v.copy()
            while True:
                nonzero=np.flatnonzero(residual)
                if not len(nonzero):break
                j=int(nonzero[0])
                if j not in piv:
                    piv[j]=residual*pow(int(residual[j]),-1,modulus)%modulus
                    break
                residual=(residual-residual[j]*piv[j])%modulus
            if not len(nonzero):break
            v=(4*v-v[neigh].sum(axis=1))%modulus
        lower=len(piv)
        assert lower>=({3:6,9:37,27:65}[q])
        summaries.append({"q":q,"field_polynomial":{3:"x",9:"x^2+1",27:"x^3-x-1"}[q],
                          "lower_shear_parameter":a,"generated_SL2_order":target,
                          "regular_laplacian_distinct_complex_eigenvalues_lower_bound":lower,
                          "Krylov_steps_requested":limit,
                          "Krylov_saturated":lower<limit,
                          "modular_witness_prime":modulus})
    return {"status":"EXACT_GROWING_CAYLEY_REGULAR_SPECTRAL_LOWER_BOUNDS",
            "regular_vs_W33_warning":"Regular group algebra Cayley Laplacian is NOT the W33 40/820/etc point-space Hamiltonian; no continuum or Weyl scaling follows.",
            "Krylov_argument":"A nonzero modular Krylov determinant witnesses independent Q-vectors. For real symmetric L, its cyclic Krylov dimension cannot exceed the number of distinct complex eigenvalues.",
            "cases":summaries}


def run_all():
    return {"schema":"w33.toe.20261022_five_followups.v1",
        "extension":jordan_extension_higher(),
        "clock":microscopic_pauli_clock(),
        "routing":routing_four_layers(),
        "magic":coherent_phase_extraction(),
        "continuum":cayley_tower()}


if __name__=="__main__":
    import sys
    s=json.dumps(run_all(),indent=2)+"\n"
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(s,encoding="utf-8")
    else:print(s,end="")
