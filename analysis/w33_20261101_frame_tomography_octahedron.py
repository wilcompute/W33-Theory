"""Native27-frame tomography and exact symmetry-reduced octahedron energy.

The POVM/frame formalism is classical. The finite maps and integer energy
reduction below are on the repository's actual120 projector labels.
"""
import collections,itertools,json,pathlib,sys,hashlib
import numpy as np
import networkx as nx
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261031_tick_loop_rigidity import PI,exact_trace
from w33_pass12055_microscopic_tick_model import PTS,FORM,ADJ

def inputs():
    tetra=json.loads((ROOT/'data/w33_20261031_chiral_tetrahedron_strange_bridge.json').read_text())
    loop=json.loads((ROOT/'data/w33_20261031_tick_loop_rigidity.json').read_text())
    ts=tetra['oriented_tetrahedra']
    Q=np.array([np.eye(9)-sum(PI[a] for a in t)/2 for t in ts])
    return tetra,loop,Q

def closure(gens,n):
    I=tuple(range(n));seen={I};queue=[I]
    for p in queue:
        for g in gens:
            q=tuple(g[p[i]] for i in range(n))
            if q not in seen:seen.add(q);queue.append(q)
    return seen

def tomography(tetra,loop,Q):
    families=tetra['local_SIC_families'];planes=[tuple(f['plane']) for f in families]
    byplane={P:i for i,P in enumerate(planes)}
    factors=sorted({tuple(sorted((i,byplane[tuple(j for j,v in enumerate(PTS)
                      if all(FORM(v,PTS[k])==0 for k in P))]))) for i,P in enumerate(planes)})
    octets=[set(planes[a])|set(planes[b]) for a,b in factors]
    G=nx.Graph();G.add_nodes_from(range(45))
    G.add_edges_from((i,j) for i,j in itertools.combinations(range(45),2) if not octets[i]&octets[j])
    frames=sorted(tuple(sorted(c)) for c in nx.find_cliques(G) if len(c)==5)
    assert len(frames)==27
    ids=[tuple(sorted(k for f in frame for p in factors[f] for k in families[p]['tetrahedron_indices'])) for frame in frames]
    assert all(len(s)==len(set(s))==90 for s in ids)
    M=np.zeros((810,27),dtype=np.int64)
    for j,s in enumerate(ids):M[list(s),j]=1
    assert np.all(M.sum(1)==3)
    gram_frames=M.T@M;A=(gram_frames==18).astype(np.int64)
    assert np.array_equal(gram_frames,90*np.eye(27,dtype=int)+18*A)
    assert np.all(A.sum(1)==10) and np.array_equal(A@A,5*np.eye(27,dtype=int)-4*A+5*np.ones((27,27),dtype=int))
    expected=np.array([0]*6+[108]*20+[270])
    assert np.max(abs(np.linalg.eigvalsh(gram_frames)-expected))<1e-9
    rng=np.random.default_rng(27134900);reconstruction=[];channels=[];luders=[];dilations=[]
    for s in ids:
        F=Q[list(s)]
        assert np.max(abs(F.sum(0)/30-np.eye(9)))<1e-12
        gram=np.einsum('aij,bji->ab',F,F).real
        assert np.max(abs(np.linalg.eigvalsh(gram)-np.array([0]*9+[2.25]*80+[90])))<1e-9
        Z=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9));rho=Z@Z.conj().T;rho/=np.trace(rho)
        prob=np.einsum('aij,ji->a',F,rho).real/30
        recovered=(40/3)*np.einsum('a,aij->ij',prob,F)-(13/3)*np.eye(9)
        channel=np.einsum('a,aij->ij',prob,F)/3
        L=sum(P@rho@P for P in F)/30
        luders.append(float(np.max(abs(L-(13/40)*rho-(3/40)*np.eye(9)))))
        V=np.vstack([np.linalg.eigh(P)[1][:,-3:].conj().T for P in F])/np.sqrt(30)
        dilation_error=max(float(np.max(abs(V.conj().T@V-np.eye(9)))),
            max(float(np.max(abs(V[3*i:3*i+3].conj().T@V[3*i:3*i+3]-F[i]/30))) for i in range(90)))
        assert V.shape==(270,9) and dilation_error<1e-12;dilations.append(dilation_error)
        reconstruction.append(float(np.max(abs(recovered-rho))))
        channels.append(float(np.max(abs(channel-rho/40-(13/120)*np.eye(9)))))
        assert reconstruction[-1]<1e-11 and channels[-1]<1e-12 and luders[-1]<1e-12
    # Covariance as actual permutations of the810 outcomes and27 POVMs.
    index={tuple(sorted(t)):i for i,t in enumerate(tetra['oriented_tetrahedra'])};findex={frozenset(s):i for i,s in enumerate(ids)}
    frame_gens=[]
    for p in list(loop['Clifford_generator_permutations'].values())+[loop['antiunitary_permutation']]:
        q=[index[tuple(sorted(p[a] for a in t))] for t in tetra['oriented_tetrahedra']]
        frame_gens.append(tuple(findex[frozenset(q[k] for k in s)] for s in ids))
    unit=closure(frame_gens[:-1],27);extended=closure(frame_gens,27)
    assert len(unit)==25920 and len(extended)==51840
    # Shared triples are an actual canonical signed-E6-support dictionary.
    triples=sorted(tuple(i for i,f in enumerate(frames) if a in f) for a in range(45))
    native=json.loads((ROOT/'artifacts/canonical_su3_gauge_and_cubic.json').read_text())['solution']['d_triples']
    target=nx.Graph();target.add_nodes_from(range(27))
    target.add_edges_from(e for row in native for e in itertools.combinations(row['triple'],2))
    match=next(nx.isomorphism.GraphMatcher(nx.from_numpy_array(A),target).isomorphisms_iter())
    assert {tuple(sorted(match[i] for i in t)) for t in triples}=={tuple(sorted(r['triple'])) for r in native}
    return dict(status='PASS_27_NATIVE_TIGHT_IC_POVMS',frames=frames,frame_outcome_indices=ids,
       factor_plane_pairs=factors,each_outcome_in_frames=3,
       effect='E_i=Q_i/30;90 effects per frame, summing to I9.',
       exact_Q_Gram_spectrum={'0':9,'9/4':80,'90':1},
       reconstruction='rho=(40/3)sum_i p_i Q_i-(13/3)I9, p_i=Tr(rho Q_i)/30.',
       probability_error_bound='For sum_i delta_p_i=0, ||delta_rho||_F <=20||delta_p||_2.',
       maximum_reconstruction_error=max(reconstruction),
       common_measure_prepare_channel='Phi(rho)=sum_i p_i Q_i/3=rho/40+(13/120)I9 for trace-one rho. All27 choices give the same entanglement-breaking depolarizing channel.',
       maximum_channel_error=max(channels),frame_generator_permutations=frame_gens,
       common_Luders_channel='L(rho)=sum_i Q_i rho Q_i/30=(13/40)rho+(3/40)I9. Its normalized Choi partial transpose has eigenvalues2/45 (multiplicity45) and-1/36 (multiplicity36), so it is not entanglement breaking.',
       maximum_Luders_channel_error=max(luders),minimum_Naimark_dimension=270,maximum_Naimark_isometry_error=max(dilations),
       Naimark_construction='Choose W_i with three orthonormal columns spanning Q_i, and stack W_i dagger/sqrt30 into a270x9 isometry. Each three-rail outcome block realizes Q_i/30. Minimum270 follows from the90 effects each having rank3.',
       instrument_boundary='The entanglement-breaking statement is for the declared replace-by-Q_i/3 instrument only. The same POVM has the different non-EB Luders instrument. Geometry of outcome probabilities alone does not specify state dynamics; dilation/feedforward controls are supplied.',
       unitary_frame_image_order=len(unit),unitary_antiunitary_frame_image_order=len(extended),
       overlap_graph_parameters=[27,10,1,5],outcome_frame_Gram_spectrum={'0':6,'108':20,'270':1},
       cubic_support_frame_triples=triples,frame_to_native_cubic=[match[i] for i in range(27)],
       boundary='Finite POVMs using supplied Born probabilities and preparation instruments. Full51840 symmetry includes antiunitaries, not physical quantum channels. Incidence and E6 support are prior mathematics; no measured species, Yukawa coefficients, spacetime or Born-rule derivation.')

def exact_tensor(tetra):
    B=np.zeros((120,120,120),dtype=np.int8)
    count=0
    for f in tetra['local_SIC_families']:
        for p,q,r in itertools.permutations(f['plane'],3):
            for x,y,z in itertools.product(range(3),repeat=3):
                t=(3*p+x,3*q+y,3*r+z);B[t]=exact_trace(t)[1];count+=1
    assert count==58320
    return B

def pair_orbits(loop):
    unseen=set(itertools.product(range(120),repeat=2));orbits=[]
    generators=list(loop['Clifford_generator_permutations'].values())
    while unseen:
        root=min(unseen);seen={root};queue=[root]
        for a,b in queue:
            for p in generators:
                q=(p[a],p[b])
                if q not in seen:seen.add(q);queue.append(q)
        unseen-=seen;orbits.append((root,len(seen)))
    assert sorted(n for _,n in orbits)==[120,240,4320,9720]
    return orbits

def scaled_pair():
    d=np.arange(120)//3
    return np.where(np.eye(120,dtype=bool),0,np.where(d[:,None]==d[None,:],18,
                    np.where(ADJ[d[:,None],d[None,:]],12,-4))).astype(np.int16)

def oct_energy(labels,E,B):
    a,b,c,d,e,f=labels
    cross=sum(int(E[x,y]) for g,h in [((a,b),(c,d)),((a,b),(e,f)),((c,d),(e,f))] for x in g for y in h)
    chir=sum((-1)**(i+j+k)*int(B[x,y,z]) for i,x in enumerate((a,b)) for j,y in enumerate((c,d)) for k,z in enumerate((e,f)))
    return cross-3*chir,chir

def energies(tetra,loop,B):
    E=scaled_pair();orbits=pair_orbits(loop)
    for p in loop['Clifford_generator_permutations'].values():
        assert np.array_equal(E,E[np.ix_(p,p)]) and np.array_equal(B,B[np.ix_(p,p,p)])
    best=10**9;witness=None;maximum=-1;maxw=None;cases=[];dos=collections.Counter();dos_witness={}
    for (a,b),size in orbits:
        cbest=10**9;cmax=-1
        # All c,d choices at once, then independently optimize e,f.
        V=(B[a].astype(np.int16)-B[b].astype(np.int16))
        vv=V[:,None,:]-V[None,:,:]
        L=E[a][None,None,:]+E[b][None,None,:]+E[:,None,:]+E[None,:,:]
        XY=E[a][:,None]+E[a][None,:]+E[b][:,None]+E[b][None,:]
        low=(L-3*vv);high=(L+3*vv)
        values=XY+low.min(2)+high.min(2)
        c,d=np.unravel_index(np.argmin(values),values.shape)
        cbest=int(values[c,d]);e=int(np.argmin(low[c,d]));f=int(np.argmin(high[c,d]))
        if cbest<best:best=cbest;witness=(a,b,int(c),int(d),e,f)
        ranges=vv.max(2)-vv.min(2);cmax=int(ranges.max())
        c,d=np.unravel_index(np.argmax(ranges),ranges.shape)
        if cmax>maximum:
            maximum=cmax;maxw=(a,b,int(c),int(d),int(np.argmax(vv[c,d])),int(np.argmin(vv[c,d])))
        multiplicities=(low==low.min(2)[:,:,None]).sum(2)*(high==high.min(2)[:,:,None]).sum(2)
        degeneracy=int(multiplicities[values==cbest].sum())*size
        cases.append(dict(pair=[a,b],orbit_size=size,minimum_six_energy=cbest,maximum_chirality_integer=cmax,
                          ordered_minimum_count_in_pair_orbit=degeneracy))
        # Independent full tetrahedral density of states, at the same couplings.
        T=B[a,b,:].astype(np.int16)[:,None]-B[a,b,:].astype(np.int16)[None,:]+B[a].astype(np.int16)-B[b].astype(np.int16)
        vals=int(E[a,b])+XY+E-3*T
        for value,n in zip(*np.unique(vals,return_counts=True)):
            dos[int(value)]+=int(n)*size
            if int(value) not in dos_witness:
                c,d=np.argwhere(vals==value)[0];dos_witness[int(value)]=(a,b,int(c),int(d))
    assert oct_energy(witness,E,B)[0]==best
    assert oct_energy(maxw,E,B)[1]==maximum
    assert best==-75 and maximum==9 and oct_energy(witness,E,B)[0]+3*maximum==-48
    assert sum(dos.values())==120**4 and dos[min(dos)]==9720
    levels=sorted(dos);gap=(levels[1]-levels[0])/6
    return dict(status='PASS_EXACT_OCTAHEDRON_AND_TETRA_DOS',
       scaled_energy_convention='6E at J=1,K=2,lambda=sqrt3; pair costs0,18,12,-4; each oriented face contributes -3b with ImTr=b/(2sqrt3).',
       pair_orbit_cases=cases,octahedron_minimum_six_energy=best,octahedron_minimum_energy=best/6,
       ground_witness=witness,ground_witness_chirality_integer=oct_energy(witness,E,B)[1],
       octahedron_ordered_ground_degeneracy=sum(c['ordered_minimum_count_in_pair_orbit'] for c in cases if c['minimum_six_energy']==best),
       maximum_octahedron_chirality_integer=maximum,maximum_chirality_witness=maxw,
       general_negative_bond_ground_law='For J>0,K>3J/2: E_min(octahedron)=12(2J-4K/3)-(3sqrt3/2)|lambda|. The integer chirality sum is at most9, and one witness also minimizes every bond. Both signs follow by interchanging the last opposite pair.',
       frustration_at_reference_couplings='At J=1,K=2,lambda=sqrt3 the unattainable separate-face lower bound is-16; the exact minimum is-25/2, a frustration defect7/2.',
       tetrahedron_density_of_states=[dict(six_energy=x,count=dos[x],witness=dos_witness[x]) for x in levels],tetrahedron_exact_gap=gap,
       tensor_sha256=hashlib.sha256(B.tobytes()).hexdigest(),exact_nonzero_direction_entries_evaluated=58320,
       proof='Pauli trace orthogonality makes all remaining imaginary triples zero. Exact tensor and pair costs are invariant under the nine generators. Their four ordered-pair orbits cover all14400 pairs. For each representative and all14400 c,d choices, the e,f minimization separates: min_e(L_e-3v_e)+min_f(L_f+3v_f). Thus all120^6 assignments are covered without enumerating them individually.',
       boundary='Exact finite supplied models, not thermodynamic phases or a derived physical coupling. The DOS is exact120^4 coverage by pair-orbit weights.')

def build():
    tetra,loop,Q=inputs();T=tomography(tetra,loop,Q);print(T['status'],flush=True)
    B=exact_tensor(tetra);E=energies(tetra,loop,B);print(E['status'],E['octahedron_minimum_energy'],E['maximum_octahedron_chirality_integer'],flush=True)
    return dict(status='PASS_FRAME_TOMOGRAPHY_AND_OCTAHEDRON',tomography=T,energies=E)

if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261101_frame_tomography_octahedron.json').write_text(json.dumps(d,indent=2)+'\n')
