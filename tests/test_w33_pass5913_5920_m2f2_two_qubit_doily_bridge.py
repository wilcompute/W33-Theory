from analysis.w33_pass5913_5920_m2f2_two_qubit_doily_bridge import (
    MATS, ZERO, det, phi, q0, symp, polar_det, graph, srg_params, S2, SANIGA, pauli_vec
)


def test_determinant_is_standard_two_qubit_quadratic():
    assert len(set(phi(m) for m in MATS)) == 16
    assert all(det(m) == q0(phi(m)) for m in MATS)
    assert all(polar_det(m,n) == symp(phi(m),phi(n)) for m in MATS for n in MATS)


def test_nonzero_matrices_form_doily_graph():
    S=[m for m in MATS if m != ZERO]
    assert srg_params(graph(S,polar_det)) == [15,6,1,3]


def test_rank_split_is_9_plus_6():
    S=[m for m in MATS if m != ZERO]
    r1=[m for m in S if det(m)==0]
    r2=[m for m in S if det(m)==1]
    assert (len(r1),len(r2)) == (9,6)
    assert srg_params(graph(r1,polar_det)) == [9,4,1,2]
    A6=graph(r2,polar_det)
    assert set(map(int,A6.sum(axis=1))) == {3}
    assert int(A6.sum()//2) == 9


def test_saniga_grid_is_local_clifford_conjugate_to_det_grid():
    C={i:pauli_vec(*pq) for i,pq in SANIGA.items()}
    source={C[i] for i in range(7,16)}
    target={phi(m) for m in MATS if m != ZERO and det(m)==0}
    assert {S2(x) for x in source} == target
    assert all(symp(S2(x),S2(y)) == symp(x,y) for x in map(phi,MATS) for y in map(phi,MATS))


def test_quadratic_hyperplane_counts():
    V=list(map(phi,MATS)); Vnon=[x for x in V if x != (0,0,0,0)]
    sizes=[]
    for v in V:
        zeros=[x for x in Vnon if (q0(x)^symp(v,x))==0]
        sizes.append(len(zeros))
    assert sizes.count(9)==10
    assert sizes.count(5)==6
