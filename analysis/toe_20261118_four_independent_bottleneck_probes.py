"""Four independent TOE bottleneck probes with explicit acceptance/failure criteria.

(A) Z3 singular-orbit and E6 trinification local anomaly bookkeeping;
(B) intervention-complete qutrit quantum-memory witness;
(C) hypersurface-bracket diagnostic in a massless 1+1 scalar toy theory;
(D) exact [[5,1,3]]_3 stabilizer/syndrome decoder and SIC Wigner magic.
Each is an independent model/test, not a derivation of gravity or SM physics.
"""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import json
import numpy as np

ROOT=Path(__file__).resolve().parents[1]

def singular_orbifold_probe():
    A=np.array([[0,-1],[1,-1]],dtype=int)
    assert np.array_equal(np.linalg.matrix_power(A,3),np.eye(2,dtype=int))
    det=int(round(np.linalg.det(A-np.eye(2,dtype=int))))
    assert det==3
    fixed=[(a,b) for a,b in product(range(3),repeat=2)
           if np.all(((A-np.eye(2,dtype=int)) @ np.array([a,b]))%3==0)]
    assert fixed==[(0,0),(1,2),(2,1)]
    # The fixed-point numerator line has the orthogonal dual torsion-clock ray.
    def fixed_mod3_vectors(M):
        return [(a,b) for a,b in product(range(3),repeat=2)
                if np.all(((M-np.eye(2,dtype=int))@np.array([a,b]))%3==0)]
    charge=fixed_mod3_vectors(A)
    dual=fixed_mod3_vectors(A.T)
    assert charge==[(0,0),(1,2),(2,1)]
    assert dual==[(0,0),(1,1),(2,2)]
    assert (charge[1][0]*dual[1][0]+charge[1][1]*dual[1][1])%3==0
    # E6 27 under SU3^3: (3,3bar,1)+(3bar,1,3)+(1,3,3bar).
    # Each color SU3 anomaly multiplicity = dimensionality of other factor.
    reps=[("3,3bar,1",(3,-3,0)),("3bar,1,3",(-3,0,3)),("1,3,3bar",(0,3,-3))]
    cubic=[sum(v[1][j] for v in reps) for j in range(3)]
    assert cubic==[0,0,0]
    return {"order_three_lattice_matrix":A.tolist(),"det(A-I)":det,
            "torus_orbifold_fixed_points_numerators_mod3":fixed,
            "torus_orbifold_fixed_points":len(fixed),
            "H27_charge_fixed_line_mod3":charge,
            "H27_dual_torsion_clock_fixed_line_mod3":dual,
            "charge_dual_orthogonal_mod3":True,
            "underlying_quotient_topology":"topological S2 with three cone points of order 3",
            "E6_27_trinification_representations":[r[0] for r in reps],
            "per_family_SU3_cubic_anomaly_coefficients":cubic,
            "three_copies_SU3_cubic_anomaly_coefficients":[3*x for x in cubic],
            "limitation":"Three Z3 torus fixed points are NOT a calculation of three 4D families. This is no G2-holonomy solution, no localized Dirac index, no anomaly inflow, and no global chiral spectrum."}

def memory_probe():
    d=3
    phi=np.zeros(9,dtype=complex)
    for a in range(d):phi[3*a+a]=1/np.sqrt(d)
    target=np.outer(phi,phi.conj())
    # Reference R, system S, quantum memory E; initialize |Phi>_RS tensor |0>_E.
    psi=np.zeros(27,complex)
    for a in range(d):psi[9*a+3*a]=1/np.sqrt(d)
    swap=np.zeros((27,27),complex)
    for r,s,e in product(range(3),repeat=3):
        src=9*r+3*s+e; dst=9*r+3*e+s
        swap[dst,src]=1
    rho=swap @ np.outer(psi,psi.conj()) @ swap.conj().T
    rng=np.random.default_rng(198732)
    z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
    unit,qr=np.linalg.qr(z)
    phases=np.diag(qr)
    unit=unit@np.diag(phases/np.abs(phases))
    assert np.max(np.abs(unit@unit.conj().T-np.eye(3)))<1e-12
    probs=[]
    maxerr=0.0
    for b in range(3):
        projector=np.zeros((3,3));projector[b,b]=1
        K=projector@unit
        instrument=np.kron(np.kron(np.eye(3),K),np.eye(3))
        after=swap @ (instrument @ rho @ instrument.conj().T) @ swap.conj().T
        rs=np.trace(after.reshape(3,3,3,3,3,3),axis1=2,axis2=5).reshape(9,9)
        pr=float(np.trace(rs).real)
        err=float(np.max(np.abs(rs-pr*target)))
        maxerr=max(maxerr,err)
        assert err<1e-11
        probs.append(pr)
    assert abs(sum(probs)-1)<1e-12 and min(probs)>1e-6
    noise=0.2
    fidelity=1-8*noise/9
    assert fidelity>1/3
    shot_n=2000
    counts=int(rng.binomial(shot_n,fidelity))
    obs=counts/shot_n
    alpha=0.001
    hoeffding_lower=float(obs-np.sqrt(np.log(1/alpha)/(2*shot_n)))
    assert hoeffding_lower>1/3
    return {"dimension":3,"arbitrary_instrument_example_conditional_probabilities":probs,
            "max_conditional_input_output_error":maxerr,
            "causal_break_classical_memory_fidelity_upper_bound":1/3,
            "depolarizing_memory_noise_probability":noise,
            "predicted_entangled_fidelity":fidelity,
            "sample_shots":shot_n,"sample_successes":counts,
            "sample_fidelity":obs,"hoeffding_99p9pct_lower":hoeffding_lower,
            "noise_threshold_for_witness_violation":0.75,
            "qualification":"The classical-memory bound assumes no hidden coherent input-to-output bypass and no unrestricted quantum side channel. A terminal entangled witness under a causal break does not certify every arbitrary process tensor solely from a GHZ fringe."}

def bracket_probe():
    def center(f):
        h=2*np.pi/len(f)
        return (np.roll(f,-1)-np.roll(f,1))/(2*h)
    def spectral(f):
        n=len(f)
        k=np.fft.fftfreq(n,d=1/n)
        return np.fft.ifft(1j*k*np.fft.fft(f)).real
    def defect(n,modes,D):
        x=np.arange(n)*2*np.pi/n
        a,b,c=modes
        lapse1=np.sin(a*x)+0.3*np.cos(a*x)
        lapse2=np.sin(b*x)+0.2*np.cos(b*x)
        field=np.sin(c*x)+0.3*np.cos(c*x)
        fp=D(field)
        # {H[N],H[M]} = integral pi [N D(M Dphi)-M D(N Dphi)]
        lhs=lapse1*D(lapse2*fp)-lapse2*D(lapse1*fp)
        rhs=(lapse1*D(lapse2)-lapse2*D(lapse1))*fp
        return float(np.linalg.norm(lhs-rhs)/np.linalg.norm(rhs))
    table=[{"sites":n,"centered_difference_relative_defect":defect(n,(2,3,4),center),
            "spectral_relative_defect":defect(n,(2,3,4),spectral)}
           for n in (32,64,128,256)]
    assert all(t["spectral_relative_defect"]<1e-10 for t in table)
    ratios=[table[i]["centered_difference_relative_defect"]/
            table[i+1]["centered_difference_relative_defect"] for i in range(3)]
    assert min(ratios)>3
    aliased=defect(32,(8,10,12),spectral)
    assert aliased>0.1
    return {"theory":"fixed-background massless scalar in 1+1 dimensions, not GR",
            "target_bracket":"{H[N],H[M]}=P[N Mprime-M Nprime]",
            "discretization_comparison":table,"centered_defect_halving_ratios":ratios,
            "32_site_spectral_high_frequency_alias_defect":aliased,
            "interpretation":"Spectral differentiation realizes the continuum product rule exactly in the alias-free bandlimited triads; high frequency aliasing breaks closure. Does not solve full field-dependent GR hypersurface-deformation algebra, gauge flow closure, or discrete Einstein equations."}

def qutrit_code_magic_probe():
    words=["XZZXI","IXZZX","XIXZZ","ZXIXZ"]
    generators=np.array([[int(c=="X") for c in s]+[int(c=="Z") for c in s]
                          for s in words],dtype=int)
    def sym(e,f):
        return int((np.dot(e[:5],f[5:])-np.dot(e[5:],f[:5]))%3)
    assert all(sym(a,b)==0 for a in generators for b in generators)
    stabilizers={tuple((np.array(cs,dtype=int)@generators)%3)
                 for cs in product(range(3),repeat=4)}
    assert len(stabilizers)==81
    def wt(v):
        return int(np.count_nonzero((v[:5]!=0)|(v[5:]!=0)))
    assert Counter(wt(np.array(s)) for s in stabilizers)=={0:1,4:40,5:40}
    single=[]
    for site in range(5):
        for a,b in product(range(3),repeat=2):
            if not(a or b):continue
            e=np.zeros(10,dtype=int);e[site]=a;e[5+site]=b
            single.append(tuple(sym(e,g) for g in generators))
    assert len(single)==40 and len(set(single))==40 and (0,0,0,0) not in single
    cent3=[]
    for sites in combinations(range(5),3):
        for pairs in product([(a,b) for a,b in product(range(3),repeat=2) if a or b],repeat=3):
            e=np.zeros(10,dtype=int)
            for pos,(a,b) in zip(sites,pairs):
                e[pos]=a;e[5+pos]=b
            if all(sym(e,g)==0 for g in generators):
                cent3.append(e)
    assert len(cent3)==80 and all(tuple(e) not in stabilizers for e in cent3)
    logical_pair=next((a,b) for a in cent3 for b in cent3 if sym(a,b)==1)
    # Exact minimum-weight syndrome decoding under iid depolarizing Pauli noise.
    errors=[]
    for pairs in product(list(product(range(3),repeat=2)),repeat=5):
        e=np.array([a for a,b in pairs]+[b for a,b in pairs],dtype=int)
        synd=tuple(sym(e,g) for g in generators)
        errors.append((wt(e),tuple(e),synd))
    errors.sort()
    decoder={}
    for weight,e,synd in errors:
        decoder.setdefault(synd,np.array(e,dtype=int))
    assert len(decoder)==81
    failures=Counter()
    totals=Counter()
    for weight,e,synd in errors:
        residual=(np.array(e,dtype=int)-decoder[synd])%3
        totals[weight]+=1
        if tuple(residual) not in stabilizers:
            failures[weight]+=1
    assert totals[1]==40 and failures[0]==0 and failures[1]==0
    assert failures[2]==593
    p=0.01
    logical_error=sum(failures[w]*(p/8)**w*(1-p)**(5-w) for w in range(6))
    # Gross qutrit Wigner negativity of the actual Hesse fiducial.
    omega=np.exp(2j*np.pi/3)
    v=np.array([0,1,-1],complex)/np.sqrt(2)
    X=np.roll(np.eye(3),1,axis=0)
    Z=np.diag([1,omega,omega**2])
    parity=np.array([[1,0,0],[0,0,1],[0,1,0]])
    W=[]
    for a,b in product(range(3),repeat=2):
        D=np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b)
        W.append(float(np.vdot(v,D@parity@D.conj().T@v).real/3))
    assert abs(sum(W)-1)<1e-10
    assert abs(min(W)+1/3)<1e-10
    assert sum(abs(x-1/6)<1e-10 for x in W)==8
    return {"code":"[[5,1,3]]_3","stabilizer_generators":words,
            "independent_generator_count":4,"stabilizer_elements":81,
            "distinct_weight_one_nonzero_syndromes":40,
            "weight_three_normalizer_nonstabilizer_count":80,
            "logical_X_vector":logical_pair[0].tolist(),"logical_Z_vector":logical_pair[1].tolist(),
            "logical_symplectic_pair":sym(*logical_pair),
            "decoder_syndromes":81,
            "total_pauli_error_counts_by_weight":dict(totals),
            "uncorrectable_pauli_error_counts_by_weight":dict(failures),
            "iid_nonidentity_Pauli_probability_per_site":p,
            "exact_decoded_logical_failure_probability":logical_error,
            "SIC_Hesse_Wigner":W,"SIC_mana_ln_sum_abs_W":float(np.log(sum(abs(t) for t in W))),
            "limitation":"Both five-qutrit stabilizer codes and Hesse SIC magic states have prior art. We have not built a logical SIC magic injection or a non-Clifford fault-tolerant gate; error probability is for a specified Pauli decoder, not a threshold."}

def main():
    r={"singular_index_candidate":singular_orbifold_probe(),
       "three_time_memory":memory_probe(),
       "discrete_bracket":bracket_probe(),
       "qutrit_code_and_magic":qutrit_code_magic_probe()}
    path=ROOT/"data"/"toe_20261118_four_independent_bottleneck_probes.json"
    path.write_text(json.dumps(r,indent=2)+"\n",encoding="utf8")
    for k,v in r.items():
        print("PASS",k, json.dumps(v)[:900])
    print(path)
    return r

if __name__=="__main__":
    main()
