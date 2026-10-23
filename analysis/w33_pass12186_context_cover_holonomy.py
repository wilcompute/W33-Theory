"""Exact context-compatible colour holonomies of the existing native4period graph.

All local interactions in the star-parent theorem are supplied. Finite binary
quadratic geometry is not a Lorentz metric or a derived physical vacuum.
"""
from pathlib import Path
import itertools,json,hashlib,math
from collections import deque
import numpy as np
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
from w33_20261015_toe82_native_H27_h1_character import mul
from w33_pass11980_heisenberg_fixed_holonomies import DIRECTIONS
from w33_pass12055_microscopic_tick_model import HS,ADJ,PROJ


def native_data():
    H=list(itertools.product(range(3),repeat=3));index={g:i for i,g in enumerate(H)}
    E=sorted({tuple(sorted((index[g],index[mul(g,d)]))) for g in H for d in list(DIRECTIONS)+[mul(d,d) for d in DIRECTIONS]})
    d=json.loads((ROOT/'data/w33_pass11991_native_four_period_cover.json').read_text());V=np.array(d['primitive_integer_edge_voltages'],int)
    A=np.zeros((27,27),int)
    for a,b in E:A[a,b]=A[b,a]=1
    assert len(E)==135 and V.shape==(135,4)
    return H,E,V,A,d


def colour_action(kind,c,gain,q=4):
    if kind=='identity':return c
    if kind=='C2':return c^gain if c<2 else c
    if kind=='C3':return (c+gain)%3 if c<3 else c
    if kind=='C4':return (c+gain)%4
    if kind=='V4':return c^gain
    if kind=='V4_nonregular':return c^((gain&1) if c<2 else ((gain>>1)&1))
    raise ValueError(kind)


def solve_colouring(E,gains,kind='V4',q=4,root=0):
    """Complete domain-propagating CSP, not a greedy nonexistence claim."""
    n=max(max(e) for e in E)+1;adj=[[]for _ in range(n)];mod={'C2':2,'C3':3,'C4':4}.get(kind)
    for (a,b),z in zip(E,gains):
        z=int(z);inv=(-z)%mod if mod else z;adj[a].append((b,inv));adj[b].append((a,z))
    nodes=0
    def propagate(dom,queue):
        for a in queue:
            c=dom[a].bit_length()-1
            for b,z in adj[a]:
                bad=colour_action(kind,c,z,q);mask=dom[b]&~(1<<bad)
                if mask==dom[b]:continue
                dom[b]=mask
                if not mask:return False
                if mask.bit_count()==1:queue.append(b)
        return True
    def rec(dom):
        nonlocal nodes;nodes+=1
        todo=[i for i,d in enumerate(dom) if d.bit_count()>1]
        if not todo:return [d.bit_length()-1 for d in dom]
        a=min(todo,key=lambda i:(dom[i].bit_count(),-len(adj[i])))
        for c in range(q):
            if not (dom[a]>>c)&1:continue
            nd=dom.copy();nd[a]=1<<c
            if propagate(nd,[a]):
                result=rec(nd)
                if result is not None:return result
        return None
    dom=[(1<<q)-1]*n;dom[0]=1<<root
    result=rec(dom) if propagate(dom,[0]) else None
    if result is not None:
        assert all(result[a]!=colour_action(kind,result[b],int(z),q) for (a,b),z in zip(E,gains))
    return result,nodes


def matrix_gain(V,s,kind):
    if kind in ('V4','V4_nonregular'):
        a=np.array(s).reshape(2,4);return V@a[0]%2+2*(V@a[1]%2)
    return V@np.array(s)%int(kind[-1])


def enumerate_holonomies(E,V):
    rows=[];summaries={}
    for kind,mod,dim,roots in [('C2',2,4,[0,2]),('C3',3,4,[0,3]),('C4',4,4,[0]),('V4',2,8,[0]),('V4_nonregular',2,8,[0,2])]:
        yes=0;nodes=0
        for s in itertools.product(range(mod),repeat=dim):
            gain=matrix_gain(V,s,kind);r=None
            for root in roots:
                attempt,nn=solve_colouring(E,gain,kind,root=root);nodes+=nn
                if attempt is not None:r=attempt;break
            if r is not None:yes+=1;rows.append(dict(kind=kind,coefficients=list(s),vertex_colours=r))
        summaries[kind]=dict(homomorphisms=mod**dim,successful=yes,search_nodes=nodes,root_orbit_representatives=roots)
    return summaries,rows


def kernel_indices(A):
    vec=np.array(list(itertools.product(range(2),repeat=4)));return tuple(map(int,np.flatnonzero(np.all(vec@np.asarray(A).T%2==0,axis=1))))


def quadric(Arows,d):
    vec=np.array(list(itertools.product(range(2),repeat=4)));idx={tuple(v):i for i,v in enumerate(vec)};kernels=sorted({kernel_indices(np.array(r['coefficients']).reshape(2,4)) for r in Arows});zeros={x for K in kernels for x in K};truth=np.array([int(i not in zeros) for i in range(16)]);anf=truth.copy()
    for bit in range(4):
        for mask in range(16):
            if mask&(1<<bit):anf[mask]^=anf[mask^(1<<bit)]
    assert list(np.flatnonzero(anf))==[4,5,8,10,12]
    polar=np.array([[truth[idx[tuple(a^b)]]^truth[idx[tuple(a)]]^truth[idx[tuple(b)]] for b in np.eye(4,dtype=int)]for a in np.eye(4,dtype=int)])
    assert round(np.linalg.det(polar))%2==1 and len(zeros)==10
    allplanes={kernel_indices(np.array(s).reshape(2,4)) for s in itertools.product(range(2),repeat=8) if len(kernel_indices(np.array(s).reshape(2,4)))==4}
    isotropic=sorted(K for K in allplanes if all(truth[i]==0 for i in K));assert kernels==isotropic and len(kernels)==6
    mats=[np.array(g['matrix'],int)%2 for g in d['exact_deck_actions']];assert all(all(truth[idx[tuple(v@M%2)]]==truth[i] for i,v in enumerate(vec))for M in mats)
    orbits=[];remaining=set(kernels)
    while remaining:
        K=min(remaining);orbit={tuple(sorted(idx[tuple(v)]for v in vec[list(K)]@M%2))for M in mats};assert orbit<=set(kernels);orbits.append(sorted(orbit));remaining-=orbit
    # Independently enumerate all homogeneous quadratic forms (linear terms allowed in F2).
    features=np.array([[*v,*(v[i]*v[j]for i in range(4)for j in range(i+1,4))]for v in vec]);invariant=[]
    for coeff in itertools.product(range(2),repeat=10):
        values=features@coeff%2
        if all(all(values[idx[tuple(v@M%2)]]==values[i] for i,v in enumerate(vec))for M in mats):
            B=np.array([[values[idx[tuple(a^b)]]^values[idx[tuple(a)]]^values[idx[tuple(b)]]for b in np.eye(4,dtype=int)]for a in np.eye(4,dtype=int)])
            invariant.append(dict(coefficients=list(coeff),nonsingular=bool(round(np.linalg.det(B))%2)))
    assert len(invariant)==4 and sum(x['nonsingular']for x in invariant)==1
    clock=set(map(tuple,d['parallel_polarization_Lorentz_repair']['selected_subgroup']));stabilizers=[];completion=[]
    for O in orbits:
        K=O[0];st=[tuple(g['h']) for g in d['exact_deck_actions'] if tuple(sorted(idx[tuple(x)]for x in vec[list(K)]@np.array(g['matrix'])%2))==K]
        assert len(st)==9 and not clock<=set(st)
        generator=next(g for g in d['exact_deck_actions']if tuple(g['h'])in st and g['h'][:2]!=[0,0]);MM=np.array(generator['matrix'],int)
        assert np.array_equal(MM@MM+MM+np.eye(4,dtype=int),np.zeros((4,4),int))
        assert round(np.linalg.det(MM-np.eye(4)))!=0
        stabilizers.append(dict(subgroup=[list(x)for x in st],generator=generator['h'],deck_matrix=MM.tolist(),fixed_real_vectors=0,contains_prior_clock_subgroup=False))
        clock_orbit={tuple(sorted(idx[tuple(x)]for x in vec[list(K)]@np.array(g['matrix'])%2))for g in d['exact_deck_actions']if tuple(g['h'])in clock}
        intersection=set.intersection(*(set(k)for k in clock_orbit));assert len(clock_orbit)==3 and intersection=={0}
        completion.append(dict(clock_orbit=[list(k)for k in sorted(clock_orbit)],intersection=sorted(intersection),completed_binary_cover_index=16))
    return dict(polynomial='Q(x)=x0+x1+x0*x1+x0*x2+x1*x3 overF2',zero_vectors=sorted(zeros),polar_matrix=polar.tolist(),Arf_invariant=0,maximal_singular_planes=[list(K)for K in kernels],H27_orbits=[[list(K)for K in O]for O in orbits],all_rank2_kernels=len(allplanes),H27_invariant_quadratic_forms=invariant,cover_stabilizers=stabilizers,prior_clock_subgroup=[list(g)for g in sorted(clock)],clock_symmetry_completion=completion,
        real_clock_obstruction='Each selected index4cover has order9 native H27 stabilizer generated on the real period4space by M with M2+M+I=0. It fixes no real nonzero vector. Every M-invariant nondegenerate real metric is Hermitian for J=(2M+I)/sqrt3 and hence has even positive/negative indices: no invariant(1,3) metric. The prior11991 clock subgroup cycles3quotient kernels; their common refinement has16sheets. A finite binary split quadric is not a real Lorentz cone. This refers to the native address H27 period action, not an asserted identification with E6/operator H27.',
        identification='Exactly the6 maximal singular2planes of the unique nonsingular H27-invariant quadratic form; two reguli of3planes. This is finiteQplus(3,2), not a real Lorentz signature.')


def lifted_graph(E,V,A,r):
    a=np.asarray(A).reshape(2,4);gain=V@a[0]%2+2*(V@a[1]%2);edges=[];colours=[]
    for x in range(4):
        colours.extend([int(c)^x for c in r])
        for (u,v),z in zip(E,gain):edges.append((27*x+u,27*(x^int(z))+v))
    assert len(set(tuple(sorted(e))for e in edges))==540
    assert all(colours[u]!=colours[v]for u,v in edges)
    G=nx.Graph();G.add_nodes_from(range(108));G.add_edges_from(edges);assert nx.is_connected(G)
    return edges,colours


def period_affine_group(d,Q):
    vec=[tuple(v)for v in itertools.product(range(2),repeat=4)];M={tuple(g['h']):np.rint(np.linalg.inv(np.array(g['matrix'],int))).astype(int).T%2 for g in d['exact_deck_actions']};H=list(M);zero=(0,0,0,0);unit=(zero,(0,0,0))
    assert all(np.array_equal(M[mul(g,h)],M[g]@M[h]%2)for g in H for h in H)
    def product(a,b):
        x,g=a;y,h=b
        return tuple(map(int,(np.array(x)+M[g]@y)%2)),mul(g,h)
    census={};center=[];gens=[(v,(0,0,0))for v in vec]+[(zero,(1,0,0)),(zero,(0,1,0))]
    for a in itertools.product(vec,H):
        power=unit
        for order in range(1,7):
            power=product(power,a)
            if power==unit:break
        assert power==unit;census[order]=census.get(order,0)+1
        if all(product(a,g)==product(g,a)for g in gens):center.append(a)
    assert sum(census.values())==432 and 4 not in census and len(center)==3
    W1=[v for v in vec if np.array_equal(M[(0,1,0)]@v%2,v)];W2=[v for v in vec if np.array_equal(M[(1,0,0)]@v%2,v)]
    assert len(W1)==len(W2)==4 and set(W1)&set(W2)=={zero}
    decomposition={tuple(np.array(a)^b):(a,b)for a in W1 for b in W2};assert len(decomposition)==16
    zeros=set(Q['zero_vectors']);index={v:i for i,v in enumerate(vec)};assert all(index[v]not in zeros for v in W1[1:]+W2[1:])
    nonzero1=W1[1:];nonzero2=W2[1:];pairings=[]
    for K in Q['maximal_singular_planes']:
        pairs=dict(decomposition[vec[i]]for i in K);assert set(pairs)==set(W1) and set(pairs.values())==set(W2)
        perm=[nonzero2.index(pairs[a])for a in nonzero1];parity=sum(perm[i]>perm[j]for i in range(3)for j in range(i+1,3))%2
        pairings.append(dict(kernel=K,permutation=perm,parity=parity))
    assert sorted(x['parity']for x in pairings)==[0,0,0,1,1,1]
    affine_pairs=set()
    for x,g in itertools.product(vec,H):
        x1,x2=decomposition[x]
        p1=tuple(W1.index(tuple((np.array(x1)+M[g]@w)%2))for w in W1)
        p2=tuple(W2.index(tuple((np.array(x2)+M[g]@w)%2))for w in W2)
        affine_pairs.add((p1,p2))
    assert len(affine_pairs)==144 and len({p[0]for p in affine_pairs})==len({p[1]for p in affine_pairs})==12
    return dict(group='G=(F2)^4 semidirect H27 using the contragredient R_g=M_g^(-T) of the stored11991 deck matrices',order=432,element_orders={str(k):v for k,v in sorted(census.items())},center=[dict(translation=list(x),H27=list(g))for x,g in center],normal_Sylow2='elementary abelian C2^4, exponent2',
        faithful_period_affine_image='A4 x A4, order144; kernel is the H27 centerC3',binary_character_planes=[list(map(list,W1)),list(map(list,W2))],six_GL2_pairings=pairings,
        connection='The six selected maximal singular planes are graphs of all6linear isomorphisms between the two binary2planes. The two reguli are even/odd permutations of their three nonzero vectors; nativeC3xC3 rotations preserve that parity.',
        clock_group_nonisomorphism='Pass12058 clock stabilizer also has order432, but quotient2xQ8 forces elements of order4. This explicit period affine group has no order4 element. Equal group order and centralC3 do not identify the groups or address/operator H27 roles.',
        scope='Explicit semidirect group multiplication and faithful affine action on period coordinates, not an asserted map into E8 clock stabilizers or a separately constructed permutation lift on every cover vertex.')

def stabilizer_contexts():
    contexts={}
    for a in range(40):
        for b in range(a+1,40):
            if not ADJ[a,b]:continue
            for i,j in itertools.product(range(3),repeat=2):
                rho=PROJ[a][i]@PROJ[b][j];labels=tuple(map(int,np.flatnonzero(np.linalg.norm(HS@rho,axis=(1,2))<1e-10)));assert len(labels)==4;contexts[labels]=rho
    assert len(contexts)==360
    return contexts


def star_certificate(edges,colours):
    contexts=stabilizer_contexts();labels=next(iter(contexts));rho=contexts[labels];nn=[[]for _ in colours]
    for u,v in edges:nn[u].append(v);nn[v].append(u)
    energy=0.;min_positive=1e9
    for v,neighbors in enumerate(nn):
        K=sum(((HS[labels[colours[v]]]+HS[labels[colours[u]]])/2 for u in neighbors),np.zeros((9,9),complex));ev=np.linalg.eigvalsh(K);assert abs(ev[0])<1e-10 and sum(abs(ev)<1e-9)==1;energy+=np.trace(K@rho).real;min_positive=min(min_positive,float(ev[1]))
    states=np.array(list(contexts.values()));overlaps=np.einsum('aij,bji->ab',states,states).real;np.fill_diagonal(overlaps,0);maximum=float(overlaps.max());assert abs(maximum-1/3)<1e-12
    return dict(ground_energy_error=float(abs(energy)),minimum_site_gap_for_displayed_cover=min_positive,distinct_stabilizer_overlap_max=maximum,
        parent='H_star=sum_{edges uv}[(h_a(u)+h_a(v))/2]_u+[(h_a(u)+h_a(v))/2]_v+kappa sum_edges delta_{a(u),a(v)} I, kappa>0; h_a=I-Pi_a.',
        ground_theorem='For any connected graph with an edge: exact zero-energy dimension360*P_G(4). Every ground label word is a proper4colouring in one pure stabilizer context, with quantum product state rho_context^tensor_vertices.',
        gap_lower_bound='min{kappa,(1-1/sqrt3)/2}',gap_scope='A true gap above zero when the frustration-free kernel exists. Otherwise only an energy floor above zero, not a spacing bound above the frustrated ground energy.',
        proof=['All terms are positive. Equal neighbouring labels costkappa. Incompatible neighbour ticks give local energy at least(1-1/sqrt3)/2 (or1/2 for different outcomes of the same direction).',
               'Otherwise each edge has a unique rank1 stabilizer kernel rho_e and K_e>=(I-rho_e)/2.',
               'If two incident edge kernels disagree, their two constraints act on the SAME vertex: K_e+K_f>=(2I-rho_e-rho_f)/2, whose minimum is at least(1-1/sqrt3)/2.',
               'If all incident kernels agree, graph connectivity propagates a single global rho. The block is a sum of onsite operators with unique product ground state and gap>=1/2. Distinct proper words determine their context uniquely.',
               'The full Hamiltonian is block diagonal in classical labels. After summing at each quantum vertex, different onsite terms commute. No SWAP exchange or entangled ground state is asserted.'],
        scope='Supplied dimensionless classical-quantum parent interaction. No derived UV coefficient, finite-temperature phase, relativistic matter, physical mass, causal clock, GR or TOE follows.')


def payload():
    H,E,V,A,d=native_data();assert np.array_equal(A@A,5*np.eye(27,dtype=int)-4*A+5*np.ones((27,27),int))
    # Exact independent set enumeration plus an explicit6colour witness.
    G=nx.from_numpy_array(A);ind=list(nx.find_cliques(nx.complement(G)));alpha=max(map(len,ind));greedy=nx.coloring.greedy_color(G,strategy='DSATUR');five,nodes=solve_colouring(E,[0]*135,'identity',q=5)
    assert alpha==6 and five is None and max(greedy.values())==5
    summaries,solutions=enumerate_holonomies(E,V);assert [summaries[k]['successful']for k in ['C2','C3','C4','V4','V4_nonregular']]==[0,0,0,36,0]
    Q=quadric(solutions,d);row=solutions[0];edges,cols=lifted_graph(E,V,row['coefficients'],row['vertex_colours']);star=star_certificate(edges,cols)
    return dict(status='EXACT_FINITE_CLASSIFICATION_AND_CONDITIONAL_PARENT_THEOREM',source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),native_input_sha256=hashlib.sha256((ROOT/'data/w33_pass11991_native_four_period_cover.json').read_bytes()).hexdigest(),
        base=dict(vertices=27,edges=135,SRG=[27,10,1,5],independence_number=alpha,maximal_independent_sets=len(ind),chromatic_number=6,five_colour_exhaustive_search_nodes=nodes,six_colour_witness=[greedy[i]for i in range(27)]),
        colour_equivariance='c(v,x)=rho(x) r_v on the actualZ4 deck cover; adjacent native edge(v,w,V_e) requires r_v!=rho(V_e)r_w. Every abelian subgroup ofS4 is conjugate intoC2,C3,C4,regularV4 or nonregularV4, all enumerated with root-orbit representatives.',
        action_classification=summaries,binary_successful_maps=solutions,binary_quadric=Q,
        minimal_equivariant_quotient='Only regularV4 colour action succeeds; six kernels of index4 inZ4. Cyclic covers cannot support any deck-equivariant4colouring. Non-equivariant colourings and covers outside this givenZ4 period quotient are not classified.',
        period_affine_group=period_affine_group(d,Q),example_cover=dict(deck='Z2xZ2',vertices=108,edges=540,coefficients=row['coefficients'],base_vertex_colours=row['vertex_colours'],lifted_colours=cols,connected=True),star_parent=star,
        prior=['11991 actual fourperiod native voltage cover','12055 native tick projectors','Local20261021 exchange_context_lock_candidate (separate unpublished Hamiltonian)','Standard graph-colouring and finite hyperbolic quadric geometry; not globally novel mathematical methods'],
        boundary='A conditional local parent and an exact finite context/cover compatibility result. No selection of one of6covers, absolute scale, spacetime dimension, continuum action or physical TOE. The fourperiod input and positive couplings are supplied.')

if __name__=='__main__':
    data=payload();out=ROOT/'data/w33_pass12186_context_cover_holonomy.json';out.write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2))
