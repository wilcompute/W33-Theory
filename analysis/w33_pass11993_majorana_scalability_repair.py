"""Native Spin6 gates as Majorana Gaussian controls, and a quartic repair.

Fermionic linear-optics limitations and quartic universality are classical
Bravyi--Kitaev prior art. Here the actual11987 gate carrier is built and its
block interface, encoded Lie closure and non-Gaussian witness are checked.
"""
import itertools,json
from pathlib import Path
import numpy as np
from scipy.linalg import schur,expm
from w33_pass11987_atlas_spin_gate_alphabet import gamma6

ROOT=Path(__file__).resolve().parents[1]


def pauli(x,z,n=4):
    I=np.eye(2);X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1]);out=np.ones((1,1),complex)
    for j in range(n):out=np.kron(out,(X if x>>j&1 else I)@(Z if z>>j&1 else I))
    return out*(1j**((x&z).bit_count()))


def anticommutes(a,b):
    x,z=a&15,a>>4;X,Z=b&15,b>>4
    return ((x&Z)^(z&X)).bit_count()%2


def lie_labels(seed):
    found=set(seed);queue=list(seed)
    for a in queue:
        for b in list(found):
            if anticommutes(a,b) and a^b not in found:found.add(a^b);queue.append(a^b)
    return sorted(found)


def gaussian_gate(U,gamma,selected):
    T,V=schur(U,output='complex');phi=np.angle(np.diag(T));phi[0]-=2*np.pi*round(sum(phi)/(2*np.pi))
    H=-(V*phi)@V.conj().T;assert abs(np.trace(H))<1e-9
    lifted=np.zeros((8,8),complex);coefficients=[]
    for i,j in itertools.combinations(range(6),2):
        B=1j*gamma[i]@gamma[j];b=B[np.ix_(selected,selected)]
        c=float((np.trace(b@H)/4).real);coefficients.append(dict(Majoranas=[i,j],coefficient=c));lifted+=c*B
    S=expm(-1j*lifted);error=float(np.max(abs(S[np.ix_(selected,selected)]-U)))
    assert error<1e-10
    R=np.array([[np.trace(g@S@h@S.conj().T).real/8 for h in gamma] for g in gamma])
    cover=max(np.max(abs(S@gamma[k]@S.conj().T-sum(R[i,k]*gamma[i] for i in range(6)))) for k in range(6))
    assert cover<1e-10 and np.max(abs(R.T@R-np.eye(6)))<1e-10 and abs(np.linalg.det(R)-1)<1e-10
    return dict(bilinear_Hamiltonian=coefficients,gate_reconstruction_error=error,Majorana_cover_error=float(cover),rotation_SO6=R.tolist())


def payload():
    gamma,chir,selected=gamma6();P=-chir
    assert np.array_equal(np.diag(P),[(-1)**j.bit_count() for j in range(8)])
    E=np.eye(8)[:,selected];assert np.array_equal(E.T@P@E,-np.eye(4))
    bilinear=[1j*gamma[i]@gamma[j] for i,j in itertools.combinations(range(6),2)]
    restricted=[E.T@b@E for b in bilinear]
    gram=np.array([[np.trace(a@b).real/4 for b in restricted] for a in restricted])
    assert np.array_equal(gram,np.eye(15))
    rows=[]
    for row in json.loads((ROOT/'data/w33_pass11987_atlas_spin_gate_alphabet.json').read_text())['gates']:
        U=np.array(row['gate_real'])+1j*np.array(row['gate_imag'])
        rows.append(dict(word=row['even_word'],**gaussian_gate(U,gamma,selected)))
    # Twelve literal Jordan--Wigner Majoranas, not commuting copies.
    big=[np.kron(g,np.eye(8)) for g in gamma]+[np.kron(P,g) for g in gamma]
    PA=np.kron(P,np.eye(8));PB=np.kron(np.eye(8),P);C=np.kron(E,E)
    commuting=0;cross=0
    for i,j in itertools.combinations(range(12),2):
        H=1j*big[i]@big[j]
        if np.array_equal(H@PA,PA@H) and np.array_equal(H@PB,PB@H):commuting+=1
        else:
            cross+=1;assert not np.any(C.T@H@C)
    assert (commuting,cross)==(30,36)
    A=1j*big[0]@big[1];B=1j*big[6]@big[7];quartic=A@B
    assert np.array_equal(quartic,-big[0]@big[1]@big[6]@big[7])
    assert np.array_equal(quartic@PA,PA@quartic) and np.array_equal(quartic@PB,PB@quartic)
    encoded=C.T@quartic@C;assert np.array_equal(encoded,pauli(0,5))
    gate=expm(-1j*np.pi*quartic/4)
    leakage=float(np.linalg.norm((np.eye(64)-C@C.T)@gate@C));assert leakage<1e-12
    local=np.array([1,0,1,0])/np.sqrt(2);psi=gate@C@np.kron(local,local)
    state=(C.T@psi).reshape(4,4);schmidt=np.linalg.svd(state,compute_uv=False)**2
    assert np.allclose(schmidt,[.5,.5,0,0],atol=1e-12)
    # Find the actual Majorana bilinear realizing virtual Y0 on block A.
    Y=np.kron(np.array([[0,-1j],[1j,0]]),np.eye(2));pairs=list(itertools.combinations(range(6),2))
    k=next(k for k,b in enumerate(restricted) if np.allclose(b,Y) or np.allclose(b,-Y))
    a,b=pairs[k];c,d=6,7
    expect=lambda M:np.vdot(psi,M@psi)
    four=expect(big[a]@big[b]@big[c]@big[d])
    wick=expect(big[a]@big[b])*expect(big[c]@big[d])-expect(big[a]@big[c])*expect(big[b]@big[d])+expect(big[a]@big[d])*expect(big[b]@big[c])
    defect=float(abs(four-wick));assert defect>1-1e-12
    local_labels=[x|(z<<4) for x in range(16) for z in range(16) if (x or z) and ((x|z)&12==0 or (x|z)&3==0)]
    assert len(local_labels)==30 and len(lie_labels(local_labels))==30
    Q=5<<4
    # A FIXED quartic angle pi/4 suffices: conjugate continuous local
    # generators, then close exact Pauli commutators. No tunable Q assumed.
    seed=set(local_labels)|{a^Q if anticommutes(a,Q) else a for a in local_labels}
    closure=lie_labels(seed);assert len(closure)==255
    dimensions=[dict(blocks=m,Majoranas=6*m,Gaussian_group_dimension=18*m*m-3*m,encoded_SU_dimension=16**m-1) for m in range(1,7)]
    assert all(r['Gaussian_group_dimension']<r['encoded_SU_dimension'] for r in dimensions[1:])
    return dict(status='PASS',reservation='b49bfed2d867b7997fa82490d22bc9bb151278cf',
        carrier='The11987 gamma6 matrices are sixMajoranas ofthree fermionicmodes. Its selectedpositivechirality C4 is ODD fermionparity, not the full8DFockspace andnot physicalspacetime spin by dimension.',
        selected_Fock_basis_indices=selected.tolist(),bilinear_restricted_Gram=gram.tolist(),native_five_gate_Hamiltonians=rows,
        Gaussian_scalability_dimension_controls=dimensions,
        exact_dimension_induction='d(m)=16^m-1-(18m^2-3m); d(1)=0; d(m+1)-16d(m)=27m(10m-3)>0, so everym>=2 has an exact Gaussian dimension deficit.',
        unitary_no_go='For a fixed6mMajorana architecture and m independent4Dparitycodeblocks, Gaussianunitaries form a compactSpin6m group ofdimension18m²-3m. The subgroupthatpreserves thecode anditsimageonit cannot havelargerLie dimension, hencecannotbedenseinSU(4^m) form>=2. Ancilla/postselection/nonGaussianmeasurement resources are outside this bound.',
        two_blocks=dict(full_Fock_dimension=64,encoded_dimension=16,all_quadratic_generators=66,individual_block_parity_preserving_quadratics=commuting,cross_block_quadratics_that_leave_code=cross),
        exact_added_operator='Q=(i gamma0 gamma1)(i gamma6 gamma7)=-gamma0 gamma1 gamma6 gamma7; encoded Q=Z_virtual0 Z_virtual2. Add the fixed gate exp(-i pi Q/4).',
        quartic_code_leakage=leakage,quartic_product_input_squared_Schmidt_values=schmidt.tolist(),four_point_Wick_defect=defect,
        exact_Pauli_Lie_seed_count=len(seed),exact_Pauli_Lie_closure=closure,exact_SU16_Lie_dimension=255,
        scalable_repair='DenseSU4 within eachnativeblock plus thedisplayedfixedquartic gateonconnectedblockpairs givesfull encodedunitaryuniversality. Two-blockSU16 iscertifiedby255 exactPauli commutatorlabels. The quartic is an additional physicalinteraction, not suppliedby11983 polartransport alone.',
        possible_mediator='A supplied heavyreal boson x with V=M²x²/2+g x(nA+nB) eliminates to -g²(nA+nB)²/(2M²). Since n²=n, this contains -g² nA nB/M² pluslocalshifts; nA nB=(Q+2nA+2nB-1)/4. This is a lowenergy matching possibility, not a derivednative mediator or dynamicalbus implementation.',
        physics_connection='11988 localJ can be read as a Majorana particle/hole polarization; its nonparalleltransport can actasBogoliubov mixing inthisdeclaredFockmodel. Such mixingneednotbe a failureofquantumcomplexHilbertspace. A chargedfamily3 interpretation still needscharge/gauge/complexstructure compatibility; no particlesorvacuumactionarederived.',
        scope='Exact nativegate realization, scoped unitaryGaussian scalability no-go and explicitnonGaussian repair. No experimentallyavailable Majoranas/quarticcoupler, scalablefaulttolerant hardware, physicalfermionidentification orTOE.',
        prior=['11987 actualSpin6 gatealphabet','11988 projectivetangentJ andnonparallelholonomy','11990 alternative9level/4rail suppliedcontrols','priorHolonetmagic/nonClifforduniversality is notsuperseded'],
        primary=['https://arxiv.org/abs/quant-ph/0003137','https://arxiv.org/abs/1112.2184'])


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11993_majorana_scalability_repair.json').write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['exact_SU16_Lie_dimension'],d['four_point_Wick_defect'])
