#!/usr/bin/env python3
"""Exact finite-field W(3,q) Levi flag flat-band locality audit.

For q in 2,3,4,5, including the genuine GF(4) extension field, derive the radial Hodge/cycle projector
P=(q^4 A_0-q^3 A_1+q^2 A_2-q A_3+A_4)/E.
The protected sector is flat under any polynomial in the unweighted flag
line-graph adjacency. A local flag potential lifts one protected eigenvalue
but leaks into the complementary cut sector. This is not emergent gravity.
"""
from __future__ import annotations
from collections import Counter, deque, defaultdict
from itertools import product
from pathlib import Path
import json
import math
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"2026_11_03_levi_flatband_locality_tradeoff.json"

def field_add(a,b,q):
    return (int(a)^int(b)) if q==4 else (int(a)+int(b))%q

def field_sub(a,b,q):
    return (int(a)^int(b)) if q==4 else (int(a)-int(b))%q

def field_mul(a,b,q):
    if q!=4:
        return (int(a)*int(b))%q
    a0,a1=int(a)&1,(int(a)>>1)&1
    b0,b1=int(b)&1,(int(b)>>1)&1
    return ((a0&b0)^(a1&b1)) | (((a0&b1)^(a1&b0)^(a1&b1))<<1)

def normalize(v,q):
    for t in v:
        if t%q:
            inv=({1:1,2:3,3:2}[int(t)] if q==4 else pow(int(t)%q,-1,q))
            return tuple(field_mul(int(a),inv,q) for a in v)
    raise ValueError("cannot projectivize zero")

def symplectic(x,y,q):
    return field_add(field_sub(field_mul(x[0],y[2],q),field_mul(x[2],y[0],q),q),
        field_sub(field_mul(x[1],y[3],q),field_mul(x[3],y[1],q),q),q)

def geometry(q):
    """GF(q) for q=2,3,4=2^2,5; GF4 modulus z^2+z+1."""
    assert q in (2,3,4,5)
    points=sorted({normalize(t,q) for t in product(range(q),repeat=4) if any(t)})
    indices={p:i for i,p in enumerate(points)}
    lines=set()
    for i,x in enumerate(points):
        for j in range(i+1,len(points)):
            y=points[j]
            if symplectic(x,y,q)==0:
                line=frozenset(indices[normalize(
                    tuple(field_add(field_mul(a,x[k],q),field_mul(b,y[k],q),q)
                          for k in range(4)),q)]
                    for a,b in product(range(q),repeat=2) if a or b)
                assert len(line)==q+1
                lines.add(line)
    lines=sorted(lines,key=lambda s:tuple(sorted(s)))
    flags=sorted((p,j) for j,line in enumerate(lines) for p in line)
    n=(q+1)*(q*q+1); E=(q+1)*n
    assert len(points)==len(lines)==n and len(flags)==E
    point_stars=defaultdict(list)
    line_stars=defaultdict(list)
    for i,(p,j) in enumerate(flags):
        point_stars[p].append(i);line_stars[j].append(i)
    neighbors=[]
    for i,(p,j) in enumerate(flags):
        neighbors.append(sorted((set(point_stars[p])|set(line_stars[j]))-{i}))
    assert all(len(neigh)==2*q for neigh in neighbors)
    return points,lines,flags,neighbors,point_stars,line_stars

def all_distances(neighbors):
    E=len(neighbors)
    distance=np.empty((E,E),dtype=np.int8)
    for source in range(E):
        row=np.full(E,-1,dtype=np.int8)
        row[source]=0
        queue=deque([source])
        while queue:
            u=queue.popleft()
            for v in neighbors[u]:
                if row[v]<0:
                    row[v]=row[u]+1
                    queue.append(v)
        assert row.min()==0 and row.max()==4
        distance[source]=row
    return distance

def run_case(q,full_matrix=False):
    points,lines,flags,neighbors,pstars,lstars=geometry(q)
    E=len(flags)
    dist=all_distances(neighbors)
    shells=[1,2*q,2*q*q,2*q**3,q**4]
    assert all(np.array_equal(np.bincount(row,minlength=5),shells) for row in dist)
    # Every pair at distance d has the same intersection numbers.
    ints=[(0,2*q)]
    for d in range(1,5):
        u=int(np.flatnonzero(dist[0]==d)[0])
        ints.append(tuple(int(np.count_nonzero(dist[0,np.asarray(neighbors[v],int)]==j))
            for v in (u,) for j in range(max(0,d-1),min(4,d+1)+1)))
    for d in range(1,5):
        ref=ints[d]
        for u in np.flatnonzero(dist[0]==d):
            calc=tuple(int(np.count_nonzero(dist[0,np.asarray(neighbors[u],int)]==j))
                for j in range(max(0,d-1),min(4,d+1)+1))
            assert calc==ref,(q,d,ref,calc)
    expected_intersections={
       1:(1,q-1,q),2:(1,q-1,q),3:(1,q-1,q),4:(2,2*q-2)}
    assert all(ints[k]==v for k,v in expected_intersections.items())
    kvec=np.array([q**4,-q**3,q*q,-q,1],dtype=np.int64)
    K=kvec[dist]
    assert np.array_equal(K,K.T)
    # Incidence D has +1 on points, -1 on lines; U=abs(D). Both
    # have identical kernels on a bipartite incidence graph.
    for stars in (pstars,lstars):
        for group in stars.values():
            assert np.all(K[group,:].sum(axis=0)==0)
    # Adjacent flag graph A sends K to -2K: exact integer equation.
    AK=np.vstack([K[neigh,:].sum(axis=0) for neigh in neighbors])
    assert np.array_equal(AK,-2*K)
    # Full integer idempotence at smaller sizes. At q=5 test columns
    # and deterministic independent probes; symbolic proof uses the
    # tridiagonal distance recurrence and trace/rank.
    if full_matrix:
        assert np.array_equal(K@K,E*K)
    else:
        probes=np.eye(E,dtype=np.int64)[:,[0,1,E//3,E//2,E-1]]
        probes=np.column_stack((probes,np.arange(E,dtype=np.int64)%7-3))
        assert np.array_equal(K@(K@probes),E*(K@probes))
    trace=int(np.trace(K))
    assert trace==E*q**4
    assert int(np.dot(K[:,0],K[:,0]))==E*q**4
    p=q**4/E
    cut=1-p
    weights=[int(v*k*k)/(E*q**4) for v,k in zip(shells,kvec)]
    assert abs(sum(weights)-1)<1e-12
    # For local V=e_e e_e^T, PVP has only eigen p and
    # ||QVP||_op = sqrt(p(1-p)); PVP is dense because
    # every K radial coefficient is nonzero.
    return {"q":q,"points":len(points),"lines":len(lines),
       "levi_vertices":len(points)+len(lines),"flags":E,
       "cycle_rank":q**4,"flat_band_adjacency_eigenvalue":-2,
       "flag_graph_degree":2*q,"diameter":4,
       "distance_shells":shells,"intersection_profiles":ints,
       "integer_projector_coefficients":kvec.tolist(),
       "projector_denominator":E,"exact_incidence_and_flatband_residual":0,
       "projector_test":"full exact K^2=E K" if full_matrix else "deterministic basis-column and vector K^2=E K probes",
       "projection_onto_defect":p,
       "defect_cut_leakage_amplitude":math.sqrt(p*cut),
       "leakage_to_band_split_ratio":math.sqrt(cut/p),
       "projected_defect_radial_probability":weights,
       "all_projected_defect_matrix_entries_nonzero":True}

def finite_time_control():
    # Small-time unitary control in the q=3 geometry, kept separate
    # from the exact integer certificate above.
    from scipy.sparse import csr_matrix,diags
    from scipy.sparse.linalg import expm_multiply
    pp,ll,flags,neighbors,_,_=geometry(3)
    distance=all_distances(neighbors)
    K=np.array([81,-27,9,-3,1],np.int64)[distance]
    P=K.astype(float)/160.
    E=160
    ii=[i for i,neigh in enumerate(neighbors) for _ in neigh]
    jj=[j for neigh in neighbors for j in neigh]
    A=csr_matrix((np.ones(len(ii)),(ii,jj)),shape=(E,E))
    g=0.25
    V=diags([1.]+[0.]*(E-1),0,shape=(E,E))
    H=A+g*V
    p=81/160.
    psi=P[:,0]/math.sqrt(p)
    assert abs(float(np.dot(psi,psi))-1)<1e-12
    expected_coefficient=g*g*p*(1-p)
    tests=[]
    for t in (0.005,0.01,0.02):
        evo=expm_multiply((-1j*t)*H,psi)
        leakage=evo-P@evo
        prob=float(np.vdot(leakage,leakage).real)
        expected=expected_coefficient*t*t
        assert abs(prob/expected-1)<.04,(t,prob,expected)
        tests.append({"t":t,"cut_leakage_probability":prob,
                      "leading_order_prediction":expected,
                      "relative_error":prob/expected-1})
    # Equal-coupling nearest-neighbor two-flag bond control.
    c=-27/160
    assert distance[0,neighbors[0][0]]==1
    mix_plus=math.sqrt((p+c)*(1-p-c))
    mix_minus=math.sqrt((p-c)*(1-p+c))
    return {"q":3,"onsite_coupling":g,
       "small_time_leakage_coefficient":expected_coefficient,
       "finite_time_tests":tests,
       "adjacent_bond_projected_eigenvalues":[p+c,c-p],
       "adjacent_bond_cut_leakage_amplitudes":[mix_plus,mix_minus],
       "two_flag_bond_is_local_but_not_cycle_preserving":True}

def main():
    cases=[run_case(q,full_matrix=(q in (2,3))) for q in (2,3,4,5)]
    finite=finite_time_control()
    output={"status":"PASS_EXACT_PRIME_FIELD_LEVI_HODGE_FLATBAND_LOCALITY_TRADEOFF",
       "date":"2026-11-03",
       "scope":"Finite generalized-quadrangle incidence geometry, not emergent spacetime or a TOE; prime fields q=2,3,5 explicitly enumerated. All prime-power q proof is a graph-theoretic extension, not fully enumerated for extension fields.",
       "formula":"v=(q+1)(q^2+1); E=(q+1)^2(q^2+1); beta1=E-2v+1=q^4",
       "radial_projector":"P_cycle=(q^4 A0-q^3 A1+q^2 A2-q A3+A4)/E",
       "distance_regular_intersection_array":"b=(2q,q,q,q), c=(1,1,1,2) on Levi line graph",
       "rigidity":"For any onsite diagonal V, [V,P]_(ef)=(V_ee-V_ff)P_ef. Since every entry of P is nonzero, [V,P]=0 iff V is a scalar constant. Any polynomial h(A_flag) restricts to h(-2)I on the cycle space, so it cannot generate intra-band dispersion.",
       "local_defect":"V=lambda |e><e|: PVP has rank1 eigenvalue lambda p with p=q^4/E, and ||(I-P)VP||=|lambda|sqrt[p(1-p)]. PVP is dense with all E^2 entries nonzero.",
       "cases":cases,"q3_dynamical_controls":finite,
       "proof_note":"GQ(q,q) incidence is (q+1)-regular and connected; Euler rank gives q^4. The line graph is distance-regular with stated intersection array. Its -2 eigenspace is ker of unsigned incidence U, dimension q^4. The radial K satisfies A K=-2K by the three-term recurrence. Each A_d is a polynomial in A, so K is central on eigenspaces; its image is the -2 eigenspace and trace(K)=E*q^4, hence K=E P_cycle.",
       "independent_prior":["analysis/w33_levi_kirchhoff_cycle_projector.py","analysis/w33_levi_flag_association_scheme.py","analysis/2026_11_03_local_spin2_hamiltonian_closure.py"],
       "literature":["https://doi.org/10.1515/nanoph-2024-0135","https://www.nature.com/articles/s42005-025-02138-6"],
       "not_claimed":["emergent Lorentzian metric","full Hilbert-space local dynamics","graviton","bona fide qutrit hardware","experimental physics"]}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(output,indent=2)+"\n",encoding="utf8")
    print("PASS",[(c["q"],c["flags"],c["cycle_rank"],c["projection_onto_defect"],
                   round(c["leakage_to_band_split_ratio"],6)) for c in cases])
    print("FINITETIME",finite["finite_time_tests"])
if __name__=="__main__":main()
