#!/usr/bin/env python3
"""Exact W33 point-vs-line symmetry intertwiner and protected flat-band no-go.

Full PSp(4,3) preserving point and line labels has three orbits on
points^2 and lines^2, and exactly TWO orbits on point x line:
incident (160) and nonincident (1440). Consequently every equivariant
point-line bilinear coupling is a*B+b*(J-B), rank <=25, so a chiral
80x80 Hamiltonian [[0,T],[T†,0]] has AT LEAST 30 zero eigenvalues.
The 15 point and 15 line zero sectors are distinct irreducible
modules and cannot mix under PSp(4,3). No unpaired chiral index emerges.
"""
import json,math,sys,collections
from pathlib import Path
import numpy as np
from w33_20261109_sp4_commutant_generation_obstruction import action

def orbit(start,gp,gl):
    seen={start};todo=collections.deque([start])
    while todo:
        i,j=todo.popleft()
        for p,l in zip(gp,gl):
            v=(p[i],l[j])
            if v not in seen:seen.add(v);todo.append(v)
    return seen

def main(path=None):
    pts,lines,inc,gp=action()
    lids={line:j for j,line in enumerate(lines)}
    gl=[]
    for p in gp:
        g=[lids[frozenset(p[i] for i in line)] for line in lines]
        assert len(set(g))==40
        gl.append(g)
    B=np.zeros((40,40),int)
    for i,lis in enumerate(inc):
        for j in lis:B[i,j]=1
    assert B.sum()==160
    for p,l in zip(gp,gl):
        assert np.array_equal(B[np.ix_(p,l)],B)
    incpair=next((i,j) for i in range(40) for j in range(40) if B[i,j])
    nonpair=next((i,j) for i in range(40) for j in range(40) if not B[i,j])
    O1=orbit(incpair,gp,gl)
    O0=orbit(nonpair,gp,gl)
    assert len(O1)==160 and len(O0)==1440 and len(O1|O0)==1600
    assert not O1&O0
    assert np.linalg.matrix_rank(B)==25
    sing=np.linalg.svd(B,compute_uv=False)
    assert np.sum(abs(sing-4)<1e-11)==1
    assert np.sum(abs(sing-math.sqrt(6))<1e-11)==24
    assert np.sum(sing<1e-11)==15
    J=np.ones_like(B)
    rank_cases=[]
    for a,b in ((1,0),(0,1),(1,1),(1,2),(1,-1),(0,0)):
        T=a*B+b*(J-B)
        s=np.linalg.svd(T,compute_uv=False)
        rank=int(np.sum(s>1e-10))
        predicted=int(a+9*b!=0)+24*int(a!=b)
        # on trivial vector B acts 4, J-B acts36,
        # so singlet coefficient 4a+36b=4(a+9b)
        assert rank==predicted,(a,b,rank,predicted)
        H=np.block([[np.zeros((40,40)),T],[T.T,np.zeros((40,40))]])
        null=80-2*rank
        assert int(np.sum(abs(np.linalg.eigvalsh(H))<1e-9))==null
        rank_cases.append({"a":a,"b":b,"rank":rank,
              "zero_eigenvalue_multiplicity":null,
              "point_chiral_kernel_dimension":40-rank,
              "line_chiral_kernel_dimension":40-rank})
    # Explicit symmetry-selected 15D dark-state projector.
    # On the W33 point graph A=BB^T-4I, eigenvalues are 12,2,-4,
    # so P_-4=(A-12I)(A-2I)/96=(8I-4A+J)/24.
    Ap=B@B.T-4*np.eye(40,dtype=int)
    Al=B.T@B-4*np.eye(40,dtype=int)
    dark_frames=[]
    for side,A,Z in (("points",Ap,B.T),("lines",Al,B)):
        P=(8*np.eye(40)-4*A+np.ones((40,40)))/24
        assert np.max(abs(P@P-P))<1e-13
        assert abs(np.trace(P)-15)<1e-13
        assert np.max(abs(Z@P))<1e-13
        G=(8/3)*P
        assert np.max(abs(np.diag(G)-1))<1e-13
        assert np.max(abs(G[A==1]+1/3))<1e-13
        assert np.max(abs(G[(A==0)&(~np.eye(40,dtype=bool))]-1/9))<1e-13
        assert np.max(abs(G@G-(8/3)*G))<1e-13
        dark_frames.append({"side":side,"projector_rank":15,
             "projector_formula":"(8I-4A+J)/24",
             "unit_norm_40vector_tight_frame_rank":15,
             "frame_constant":"8/3",
             "pair_inner_product_if_collinear":"-1/3",
             "pair_inner_product_if_noncollinear":"1/9",
             "projector_full_group_invariant":True})
    v=((8*np.eye(40)-4*Ap+np.ones((40,40)))/24)[:,0]/math.sqrt(3/8)
    assert abs(np.linalg.norm(v)-1)<1e-13
    assert np.linalg.norm(B.T@v)<1e-13
    # A single edge phase detuning makes the exact dark state leak at
    # short times. Predict line-sector t^2 coefficient analytically.
    theta=math.pi/5
    j=next(j for j in range(40) if B[0,j])
    T=B.astype(complex);T[0,j]*=np.exp(1j*theta)
    short_time_var=float(np.vdot(T.conj().T@v,T.conj().T@v).real)
    expected=float(1.5*math.sin(theta/2)**2)
    assert abs(short_time_var-expected)<1e-12
    # The cross commutant =2, the two rank-3 diagonal commutants
    # =3 each. Dimension End_G(point ⊕ line)=3+3+2+2=10.
    # A group-equivariant linear map from the line module to the point
    # module has B,J as a basis; no such map connects the 15D kernels.
    result={
      "status":"PASS_EXACT_W33_INCIDENT_160_NONINCIDENT_1440_30_FLAT_ZERO_MODES",
      "projective_symplectic_transvection_generators":len(gp),
      "incidence_point_line_pair_orbits":[{"type":"incident","size":len(O1)},
                                          {"type":"nonincident","size":len(O0)}],
      "permutation_point_module_dimension":40,
      "permutation_line_module_dimension":40,
      "point_and_line_commutant_dimensions":[3,3],
      "point_line_intertwiner_dimension":2,
      "direct_sum_80_dim_commutant_dimension":10,
      "point_line_intertwiner_basis":["incidence B","all_ones_minus_incidence J-B"],
      "B_singular_spectrum":{"4":1,"sqrt6":24,"0":15},
      "native_B_rank":25,
      "explicit_15D_dark_tight_frames":dark_frames,
      "one_detuned_edge_dark_state_test":{"incident_point":0,"incident_line":j,
           "edge_phase_radians":theta,"exact_short_time_line_leakage_t2_coefficient":expected,
           "independent_matrix_leakage_t2_coefficient":short_time_var,
           "leakage_formula":"3/2 sin²(theta/2) for projector-column dark state centered at perturbed point"},
      "chiral_H0_spectrum":{"plus4":1,"minus4":1,"plus_sqrt6":24,"minus_sqrt6":24,"zero":30},
      "six_invariant_coupling_controls":rank_cases,
      "exact_theorem":"Every linear point-to-line map intertwining the FULL PSp(4,3) action equals a B+b(J-B), hence has rank <=25 and at least 15 point and 15 line zero vectors. An 80-dimensional bipartite chiral H=[[0,T],[T†,0]] has >=30 exact flat zero modes, with chiral index (#point zero-#line zero)=0. This does not uniquely isolate a 3-family sector or an unpaired Weyl cone.",
      "scope":"Only full group-equivariant linear point/line couplings; interactions or selected backgrounds, nontrivial gauge bundles, symmetry breaking, other representations and extended spatial hopping can evade it. Zero at energy zero also requires chiral grading. This finite obstruction does NOT constitute the continuum Nielsen-Ninomiya theorem, a 3+1D Dirac theory or a physical SM derivation.",
      "novelty_scope":"Incidence spectrum and representation theory are classical. Original added value is an independently executable repo-specific exact constraint on candidate W33-symmetric TOE bilinears."}
    if path:Path(path).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PSp4 80-mode",json.dumps({"cross_orbits":[len(O1),len(O0)],"commutant":10,
      "B_rank":25,"zero_modes":30,"controls":rank_cases}))
    return result

if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
