"""TOE93: explicit Heisenberg 27-orbit Witting -> Schlaefli chain interface.

W33 PG(3,3) with polar hyperplane x_f1=0 splits 40=27+13.
The unipotent symplectic Heisenberg radical H27 fixes the hyperplane's
polar point and acts freely/transitively on the 27-point affine sector.
Construct exact group isomorphism to native cubic H27; route 108
affine W33 edges equivariantly to 1- or 2-edge Schlaefli paths.
This is an F3 graph chain map, NOT a CSS chain map or physical CPTP gate.
"""
from __future__ import annotations
import json,re,collections
from itertools import product
from analysis.w33_20261015_toe90_vlasov_ququart_design import ROOT
from analysis.w33_20261015_toe86_geometry_integral_routing import H,IDENTITY,D,mul
from tools.witting_graph_isomorphism import construct_f3_points,omega_symp
def symplectic_matrix_apply(x,g):
    a,b,c=g
    x0,x1,x2,x3=x
    return ((x0+a*x1+c*x2+b*x3)%3,
            (x1+b*x2)%3,x2,
            (x3-a*x2)%3)
def norm(x):
    for i,v in enumerate(x):
        if v%3:
            inv=pow(v,-1,3)
            return tuple((a*inv)%3 for a in x)
    raise ValueError
def group_law(u,v):
    a,b,c=u;A,B,C=v
    return ((a+A)%3,(b+B)%3,(c+C+a*B-b*A)%3)
def phi(u):
    a,b,c=u
    return (a,b,2*(c-a*b)%3)
def inv(x):
    a,b,c=x
    return ((-a)%3,(-b)%3,(-c-a*b)%3)
def graph():
    points=construct_f3_points()
    mapping={int(a):int(b) for a,b in re.findall(
      r'(?m)^(\d+) -> (\d+)$',(ROOT/'docs/witting_graph_isomorphism.md').read_text())}
    assert len(mapping)==40
    by_point={tuple(p):i for i,p in enumerate(points)}
    f3_to_ray={p:ray for ray,p in mapping.items()}
    affine={i for i,p in enumerate(points) if p[2]!=0}
    polar=set(range(40))-affine
    assert len(affine)==27 and len(polar)==13
    affine_ray={i:f3_to_ray[i] for i in affine}
    # Each H27 unipotent sends f1 to a distinct affine point.
    addresses={}
    for g in H:
        p=norm(symplectic_matrix_apply((0,0,1,0),g))
        addr=phi(g)
        assert p in by_point
        addresses[by_point[p]]=addr
    assert len(addresses)==27 and set(addresses.values())==set(H)
    edge_pairs=[(i,j) for i in range(40) for j in range(i+1,40)
                if omega_symp(points[i],points[j])==0]
    internal=[(i,j) for i,j in edge_pairs if i in affine and j in affine]
    crossing=[(i,j) for i,j in edge_pairs if (i in affine)!=(j in affine)]
    outside=[(i,j) for i,j in edge_pairs if i in polar and j in polar]
    assert (len(edge_pairs),len(internal),len(crossing),len(outside))==(240,108,108,24)
    return points,addresses,internal,crossing,outside,mapping
def signed_path(path):
    z=collections.Counter()
    for a,b in zip(path,path[1:]):
        edge=tuple(sorted((a,b)))
        z[edge]+= 1 if a<b else -1
    return {k:int(v%3) for k,v in z.items() if v%3}
def boundary(chain):
    out=collections.Counter()
    for (a,b),coeff in chain.items():
        out[a]-=coeff;out[b]+=coeff
    return {v:int(s%3) for v,s in out.items() if s%3}
def certificate():
    points,address,internal,crossing,outside,raymap=graph()
    for x in H:
        for y in H:
            lhs=phi(group_law(x,y))
            rhs=mul(phi(x),phi(y))
            assert lhs==rhs
    for g in H:
        for i,addr in address.items():
            dst=construct_dst(points,i,g)
            assert dst in address and address[dst]==mul(phi(g),addr)
    adj={g:set() for g in H}
    for g in H:
        for d in D:
            h=mul(g,d)
            adj[g].add(h);adj[h].add(g)
    assert all(len(v)==10 for v in adj.values())
    rset={mul(inv(address[i]),address[j]) for i,j in internal}
    assert len(rset)==8 and IDENTITY not in rset
    routes={}
    for delta in sorted(rset):
        back=inv(delta)
        if delta in routes:continue
        if delta in adj[IDENTITY]:
            route=[IDENTITY,delta]
        else:
            middle=min(adj[IDENTITY]&adj[delta])
            route=[IDENTITY,middle,delta]
        routes[delta]=route
        # Reverse path then left-translate by delta^{-1}; this is
        # necessary for signed orientation consistency.
        routes[back]=[mul(back,h) for h in reversed(route)]
        assert routes[back][0]==IDENTITY and routes[back][-1]==back
    def send_arc(a,b):
        x,y=address[a],address[b]
        delta=mul(inv(x),y)
        path=[mul(x,k) for k in routes[delta]]
        return signed_path(path)
    sch_edges={tuple(sorted((u,v))) for u in H for v in adj[u]}
    assert len(sch_edges)==135
    for i,j in internal:
        f=send_arc(i,j)
        assert all(edge in sch_edges for edge in f)
        assert boundary(f)=={address[i]:2,address[j]:1}
        reverse=send_arc(j,i)
        assert all((f.get(k,0)+reverse.get(k,0))%3==0 for k in f.keys()|reverse.keys())
        for g in H:
            u=construct_dst(points,i,g);v=construct_dst(points,j,g)
            actual=send_arc(u,v)
            moved={}
            for (x,y),coeff in f.items():
                X,Y=mul(phi(g),x),mul(phi(g),y)
                edge=tuple(sorted((X,Y)))
                sign=1 if X<Y else 2
                moved[edge]=(moved.get(edge,0)+sign*coeff)%3
            assert actual=={k:v for k,v in moved.items() if v%3}
    census=collections.Counter(len(routes[d])-1 for d in rset)
    print('H27-PARABOLIC',len(address),len(internal),len(crossing),len(outside),'paths',dict(census),flush=True)
    return {
     'W33_projective_space':'PG(3,3) with alternating symplectic form omega(x,y)=x0*y2-x2*y0+x1*y3-x3*y1',
     'chosen_polar_point_F3':[1,0,0,0],
     'affine_points_not_perpendicular_to_polar_point':27,
     'polar_hyperplane_points_perpendicular_to_polar_point':13,
     'symplectic_Heisenberg_parabolic_subgroup_order':27,
     'symplectic_group_parameter_law':'(a,b,c)(A,B,C)=(a+A,b+B,c+C+aB-bA) mod 3',
     'native_cubic_H27_isomorphism':'(a,b,c) -> (a,b,2(c-ab)) mod 3, checked for all 729 multiplication pairs',
     'affine_ray_to_native_address':[{ 'witting_ray_index':raymap[i], 'symplectic_point_index':i,'H27_address':list(g)} for i,g in sorted(address.items())],
     'W33_edge_partition':{'affine_affine':len(internal),'affine_polar':len(crossing),'polar_polar':len(outside)},
     'directed_detector_substitution_admitted_affine_edges':2*len(internal),
     'directed_detector_substitution_erasure_outside_affine_edges':2*(len(crossing)+len(outside)),
     'Schlaefli_edges':len(sch_edges),
     'eight_relative_affine_graph_generators':[list(x) for x in sorted(rset)],
     'native_path_length_census_per_relative_generator':{str(k):v for k,v in sorted(census.items())},
     'chain_map':'For affine directed W33 event i->j, map H27 addresses x,y and the relative generator delta=x^-1*y to a preselected H27-transported one- or two-edge Schlaefli path. Over F3, d1_S F1 = F0 d1_W on all 108 affine edges, with signed reversal and 27 group equivariances checked.',
     'out_of_sector_handling':'132/240 unoriented events are typed erasures, not assigned an H27 edge. A total deterministic H27-equivariant map of all 480 remains obstructed.',
     'quantum_limit':'This is an exact partial linear GRAPH CHAIN MAP of vertex/edge modules, not an equivariant 2-cell/CSS stabilizer map, physical ququart-to-qutrit CPTP channel or protected logical operation.'}
def construct_dst(points,i,g):
    z=norm(symplectic_matrix_apply(points[i],g))
    return {p:k for k,p in enumerate(points)}[z]
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261015_toe93_affine_H27_chain.json').write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
