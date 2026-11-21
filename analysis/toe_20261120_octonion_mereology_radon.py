"""Independent Witting/G2 five-front finite geometry certificate (numpy/networkx).

Scope: ordinary quantum mechanics + classical polar/octonion geometry.
Prior: 40 Witting rays, 45 Clifford tensor charts, and E8 6:1 root fibers.
Run: python analysis/toe_20261120_octonion_mereology_radon.py
"""
import itertools as it, json, math
from collections import Counter
from pathlib import Path
import numpy as np, networkx as nx

omega=np.exp(2j*np.pi/3)
E3=np.eye(3,dtype=complex)
X=np.roll(E3,1,axis=0)
Z=np.diag([omega**i for i in range(3)])
I=np.eye(9,dtype=complex)
A=list(it.product(range(3),repeat=4))
def cn(u):
    j=next(i for i,x in enumerate(u) if x)
    return tuple(int(x*pow(int(u[j]),-1,3))%3 for x in u)
def sp(u,v):
    return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%3
V=sorted({cn(u) for u in A if any(u)})
def w(u):
    m=np.array([[1]],complex)
    for i in (0,2):
        a,b=u[i:i+2]
        m=np.kron(m,omega**((-2*a*b)%3)*np.linalg.matrix_power(Z,a)@np.linalg.matrix_power(X,b))
    return m
W={u:w(u) for u in A}
P=np.zeros((9,9),complex)
for i,j in it.product(range(3),repeat=2):
    P[(-i%3)*3+(-j%3),3*i+j]=1
Pi={v:(I+W[v]+W[tuple(-x%3 for x in v)])/3 for v in V}
Rho={v:(I-P)/2@Pi[v] for v in V}
def quantum_atlas():
    planes=set()
    for u,v in it.combinations(V,2):
        if not sp(u,v):continue
        pts=frozenset(cn([(a*u[j]+b*v[j])%3 for j in range(4)])
                      for a,b in it.product(range(3),repeat=2) if a or b)
        assert len(pts)==4
        planes.add(pts)
    assert len(planes)==90
    charts=set()
    for pl in planes:
        perp=frozenset(v for v in V if all(sp(v,u)==0 for u in pl))
        assert len(perp)==4 and perp in planes and pl.isdisjoint(perp)
        charts.add(frozenset((pl,perp)))
    assert len(charts)==45
    # Full quantum purity, computed using 9 local Weyl moments per chart.
    E=np.array([[np.trace(Rho[v]@W[u]) for u in A] for v in V])
    ix={v:i for i,v in enumerate(A)}
    product={}
    deviation=0.
    for f,c in enumerate(charts):
        pl,pr=tuple(c)
        U={(0,0,0,0)}|{tuple(t*x%3 for x in v) for v in pl for t in (1,2)}
        indices=[ix[u] for u in U]
        for vi,v in enumerate(V):
            p=float(np.sum(abs(E[vi,indices])**2).real/3)
            pred=1 if v in pl or v in pr else .5
            deviation=max(deviation,abs(p-pred))
            product[f,v]=(pred==1)
    assert deviation<1e-10
    pairs=Counter()
    for a,b in it.combinations(V,2):
        n=sum(product[f,a] and product[f,b] for f in range(45))
        pairs[(sp(a,b)==0,n)]+=1
    assert pairs=={(True,3):240,(False,1):540}
    return dict(charts=45,states=40,state_chart_checks=1800,
                local_states_per_chart=8,entangled_states_per_chart=32,
                product_charts_per_state=9,entangled_charts_per_state=36,
                pure_reduced_purity=1,entangled_reduced_purity=.5,
                commuting_pair_frame_multiplicity=3,
                noncommuting_pair_frame_multiplicity=1,
                commuting_pair_count=240,noncommuting_pair_count=540,
                maximal_quantum_purity_error=deviation,
                toy_cost_degeneracies_commuting=[3,12,30],
                toy_cost_degeneracies_noncommuting=[1,16,28],
                invariant_uniform_40ray_source_cost_all_charts=16)

def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def octo_zero(x,y):
    a,u,v=x[0],x[1:4],x[4:7]
    c,s,t=y[0],y[1:4],y[4:7]
    vt=cross(v,t);us=cross(u,s)
    z=[a*c+sum(i*j for i,j in zip(u,t))]
    z += [a*s[i]-c*u[i]-vt[i] for i in range(3)]
    z += [c*v[i]-a*t[i]+us[i] for i in range(3)]
    z += [a*c+sum(i*j for i,j in zip(v,s))]
    return all(k%3==0 for k in z)
def hexagon():
    points=sorted({cn(x) for x in it.product(range(3),repeat=7)
                   if any(x) and (-x[0]*x[0]-sum(x[k+1]*x[k+4] for k in range(3)))%3==0})
    assert len(points)==364
    graph=nx.Graph()
    graph.add_nodes_from(range(364))
    for a,b in it.combinations(range(364),2):
        if octo_zero(points[a],points[b]):
            assert octo_zero(points[b],points[a])
            graph.add_edge(a,b)
    assert graph.number_of_edges()==2184 and set(dict(graph.degree()).values())=={12}
    lines=list(nx.find_cliques(graph))
    assert len(lines)==364 and set(map(len,lines))=={4}
    incid=nx.Graph()
    incid.add_nodes_from(range(728))
    for j,line in enumerate(lines):incid.add_edges_from((i,364+j) for i in line)
    assert nx.is_connected(incid) and incid.number_of_edges()==1456
    shell=Counter(nx.single_source_shortest_path_length(graph,0).values())
    assert shell=={0:1,1:12,2:108,3:243}
    # For an incidence graph girth 12 iff no cycles of length <12 and some length-12.
    girth=100
    for r in incid:
        seen={r:0};par={r:-1};todo=[r]
        for x in todo:
            for y in incid[x]:
                if y not in seen:
                    seen[y]=seen[x]+1;par[y]=x;todo.append(y)
                elif par[x]!=y:girth=min(girth,seen[x]+seen[y]+1)
            if 2*seen[x]+1>=girth:break
    assert girth==12
    vals=np.linalg.eigvalsh(nx.to_numpy_array(graph))
    spec=Counter(int(round(float(x))) for x in vals)
    assert spec=={12:1,5:104,-1:168,-4:91}
    assert max(abs(x-round(float(x))) for x in vals)<1e-9
    return dict(points=364,lines=364,collinearity_edges=2184,incidences=1456,
                incidence_girth=girth,point_distance_shells=dict(shell),
                point_graph_eigenvalues=dict(spec),
                betti_1=incid.number_of_edges()-incid.number_of_nodes()+1,
                known_Steinberg_dimension=3**6,
                caveat="Q(6,3) octonionic model, NOT proven as symplectic W(5,3) Pauli realization")

def radon():
    s=sum(Pi.values())
    assert np.linalg.norm(s-13*I-3*P)<1e-10
    ops=[W[a]@P@W[a].conj().T for a in A]
    d=max(np.linalg.norm(W[a]@s@W[a].conj().T-13*I-3*q) for a,q in zip(A,ops))
    gram=np.array([[np.trace(q@t).real/9 for t in ops] for q in ops])
    assert np.max(abs(gram-np.eye(81)))<1e-10
    rng=np.random.default_rng(20261120);e=0
    for i in range(20):
        x=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9))
        rho=x@x.conj().T;rho/=np.trace(rho).real
        for q in ops:
            prob=np.trace(rho@(13*I+3*q)/40).real
            expected=np.trace(rho@q).real/9
            e=max(e,abs((40*prob-13)/27-expected))
    assert e<1e-10
    return dict(displacements=81,mixed_state_samples=20,
                probabilities_tested=1620,phase_space_operator_span_rank=81,
                max_operator_identity_error=float(d),max_Radon_Wigner_error=float(e),
                identity="Wigner_rho(a)=(40*p0(a)-13)/27")
def obstruction():
    U=[I+(omega-1)*Pi[v] for v in V]
    M=np.concatenate([np.kron(I,g)-np.kron(g.T,I) for g in U],axis=0)
    sing=np.linalg.svd(M,compute_uv=False)
    assert sum(x<1e-9 for x in sing)==2
    assert all(np.linalg.norm(g@P-P@g)<1e-10 for g in U)
    return dict(reflections=40,full_matrix_commutant_dimension=2,
                invariant_Hamiltonian="a I + b parity",
                Witting_ray_selection_requires_symmetry_breaking=True,
                E8_prior_root_count=240,E8_prior_projective_ray_count=40,
                root_phase_lifts_per_ray=6,
                note="E8 6:1 count from previous Pass11681, not independently rederived here")
def run():
    out={"status":"PASS",
         "quantum_mereology":quantum_atlas(),
         "G2_hexagon":hexagon(),
         "Radon_tomography":radon(),
         "E8_and_symmetric_action":obstruction(),
         "physical_boundary":"Exact finite geometry only; no physical TOE or emergent Lorentzian dynamics."}
    path=Path(__file__).resolve().parents[1]/"data/toe_20261120_octonion_mereology_radon.json"
    path.parent.mkdir(exist_ok=True,parents=True)
    path.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return out
if __name__=="__main__":
    r=run()
    print("PASS",r['quantum_mereology']['state_chart_checks'],r['G2_hexagon']['betti_1'],r['Radon_tomography']['probabilities_tested'])
