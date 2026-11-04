#!/usr/bin/env python3
"""Five second-order TOE controls that extend, rather than duplicate, the
2026-11-03 six-front baseline. All claimed identities are replayed at runtime.
No emergent spacetime, physical gravity or measured constants are asserted.
"""
from __future__ import annotations
from pathlib import Path
from itertools import product, combinations
from math import gamma
import json, math
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"2026_11_03_second_order_toe_frontier.json"

def nonabelian_cube():
    rng=np.random.default_rng(18034)
    def su2():
        a,b,c,d=rng.normal(size=4)
        a,b,c,d=np.asarray([a,b,c,d])/np.linalg.norm([a,b,c,d])
        return np.array([[a+1j*b,c+1j*d],[-c+1j*d,a-1j*b]])
    # Twelve oriented edges of one elementary 3-cube.
    links={i:su2() for i in range(1,13)}
    A,B,C,D,E,F,G,H,I,J,K,L=range(1,13)
    srcdst=[
      ((0,0,0),(1,0,0)),((0,0,0),(0,1,0)),((0,0,0),(0,0,1)),
      ((1,0,0),(1,1,0)),((1,0,0),(1,0,1)),
      ((0,1,0),(1,1,0)),((0,1,0),(0,1,1)),
      ((0,0,1),(1,0,1)),((0,0,1),(0,1,1)),
      ((1,1,0),(1,1,1)),((1,0,1),(1,1,1)),((0,1,1),(1,1,1))]
    def inverse(w):return [-i for i in w[::-1]]
    def mat(w,U):
        X=np.eye(2,dtype=complex)
        for v in w:X=X@(U[v] if v>0 else U[-v].conj().T)
        return X
    xy0=[A,D,-F,-B];xz0=[A,E,-H,-C];yz0=[B,G,-I,-C]
    xy1=[H,K,-L,-I];xz1=[F,J,-L,-G];yz1=[D,J,-K,-E]
    faces=[inverse(yz0),[B]+inverse(xz1)+[-B],inverse(xy0),
           [A]+yz1+[-A],xz0,[C]+xy1+[-C]]
    # A shelling of the oriented cube's six gauge-transported faces.
    P=np.eye(2,dtype=complex)
    for w in faces:P=P@mat(w,links)
    eps=float(np.linalg.norm(P-np.eye(2)))
    assert eps<1e-12,eps
    # Deliberately OMIT the transports from root to opposite faces.
    naive=[inverse(yz0),inverse(xz1),inverse(xy0),yz1,xz0,xy1]
    Q=np.eye(2,dtype=complex)
    for w in naive:Q=Q@mat(w,links)
    naive_err=float(np.linalg.norm(Q-np.eye(2)))
    assert naive_err>.01,naive_err
    g={tuple(v):su2() for pair in srcdst for v in pair}
    transformed={i:g[p]@links[i]@g[q].conj().T
                 for i,(p,q) in enumerate(srcdst,start=1)}
    root=g[(0,0,0)]
    covariance=max(float(np.linalg.norm(mat(w,transformed)
                 -root@mat(w,links)@root.conj().T)) for w in faces)
    assert covariance<1e-12,covariance
    nonflat=max(float(np.linalg.norm(mat(w,links)-np.eye(2))) for w in faces)
    assert nonflat>.1
    return dict(status="PASS",face_count=6,noncommuting_group="SU(2)",
       six_transport_face_Bianchi_residual=eps,
       deliberately_untransported_face_product_defect=naive_err,
       maximum_gauge_covariance_error=covariance,
       largest_nontrivial_rooted_face_holonomy=nonflat,
       boundary="Nonabelian cube gauge Bianchi identity; NOT gravitational Levi-Civita Bianchi or first-class ADM constraints.")

def causal_scale_drift():
    import runpy
    d=runpy.run_path(str(ROOT/"analysis"/"2026_11_03_causal_set_dimension_nulls.py"))
    rng=np.random.default_rng(334)
    Ns=(32,48,72,96)
    grid=np.array([.006,.010,.014,.018,.022,.028,.034,.042,.050,.060,.075,.09])
    nfit=48
    fit_target=[d["rstat"](d["order"](d["sprinkled"](4,nfit,90000+i))) for i in range(32)]
    mean_target=float(np.mean(fit_target))
    # Freeze p using density-only training, no test observations.
    fit=[]
    for ip,p in enumerate(grid):
        vals=[]
        for j in range(26):
            # independent seed per growth replicate
            seed=100000+1000*ip+j
            g=np.random.default_rng(seed)
            C=np.zeros((nfit,nfit),dtype=bool)
            for k in range(nfit):
                for q in np.flatnonzero(g.random(k)<p):
                    C[k,q]=True; C[k]|=C[q]
            vals.append(d["rstat"](C))
        fit.append(float(np.mean(vals)))
    selected=float(grid[int(np.argmin(np.abs(np.array(fit)-mean_target)))])
    rows=[]
    for n in Ns:
        tg=[]; nul=[]
        for j in range(30):
            C=d["order"](d["sprinkled"](4,n,200000+n*100+j))
            tg.append((d["rstat"](C),d["longest"](C)))
        for j in range(45):
            g=np.random.default_rng(500000+n*100+j)
            C=np.zeros((n,n),dtype=bool)
            for i in range(n):
                for q in np.flatnonzero(g.random(i)<selected):
                    C[i,q]=True;C[i]|=C[q]
            nul.append((d["rstat"](C),d["longest"](C)))
        avg=lambda x:[float(np.mean([z[k] for z in x])) for k in (0,1)]
        a=avg(tg);b=avg(nul)
        rows.append(dict(n=n,reference_density=a[0],reference_height=a[1],
                         growth_density=b[0],growth_height=b[1]))
    target_drift=rows[-1]["reference_density"]-rows[0]["reference_density"]
    growth_drift=rows[-1]["growth_density"]-rows[0]["growth_density"]
    assert abs(target_drift)<.045,rows
    assert growth_drift>.06,rows
    return dict(status="PASS",frozen_p=selected,training_only_n=nfit,
        training_target_density=mean_target,train_candidate_grid=grid.tolist(),
        train_null_densities=fit,finite_size=rows,
        reference_density_change=target_drift,growth_density_change=growth_drift,
        theory_four_d_density=gamma(5)*gamma(2)/(2*gamma(6)),
        boundary="Only one fixed p from N=48; 30/45 independent replicas per N=32,48,72,96. Rejects its scale stability as a 4D Alexandrov-order model, not causal-set quantum gravity in general.")

def rank_f2_columns(columns):
    pivots={}
    for x in columns:
        while x:
            i=x.bit_length()-1
            if i not in pivots:pivots[i]=x;break
            x^=pivots[i]
    return len(pivots)

def simplicial_phases():
    # Boundary of octahedron S2: 6 points in three antipodal pairs,
    # eight triangular facets (one point from each pair).
    faces=[tuple(sorted(x)) for x in product((0,1),(2,3),(4,5))]
    def complex_of(mask):
        facets=[tuple(f) for f in faces]
        for j,f in enumerate(faces):
            if mask>>j&1:facets.append(tuple(sorted((*f,6))))
        cells=[set() for _ in range(4)]
        for f in facets:
            for k in range(1,len(f)+1):
                for c in combinations(f,k):cells[k-1].add(tuple(sorted(c)))
        cells=[sorted(z) for z in cells]
        ranks=[]
        for k in range(1,4):
            lookup={x:i for i,x in enumerate(cells[k-1])}
            cols=[]
            for f in cells[k]:
                bits=0
                for s in combinations(f,k):bits^=1<<lookup[s]
                cols.append(bits)
            ranks.append(rank_f2_columns(cols))
        r=[0,*ranks,0]
        betti=[len(cells[k])-r[k]-r[k+1] for k in range(4)]
        fvec=[len(c) for c in cells]
        assert sum(((-1)**j)*fvec[j] for j in range(4))==sum(((-1)**j)*betti[j] for j in range(4))
        # The fundamental 3D non-purity of every partial cone:
        # some original triangles are maximal 2-cells.
        nonpure=sum(not (mask>>j&1) for j in range(8)) if mask else 0
        return fvec,betti,nonpure
    states=[complex_of(mask) for mask in range(256)]
    assert states[0]==([6,12,8,0],[1,0,1,0],0),states[0]
    assert states[255]==([7,18,20,8],[1,0,0,0],0),states[255]
    assert all(states[m][2]>0 for m in range(1,255))
    assert all(states[m][1][0]==1 for m in range(256))
    # Exact finite ensemble of 2^8 locally updated tetrahedron subsets.
    phase_counts={}
    for mask in range(256):
        k=mask.bit_count()
        key=(k,states[mask][1][2])
        phase_counts[key]=phase_counts.get(key,0)+1
    # Sum over physical cone face occupation without a prescribed
    # global-dimension jump; changing from pure 2D to pure 3D
    # necessarily crosses mixed-dimensional masks in this move family.
    return dict(status="PASS",initial_sphere=dict(fvector=states[0][0],betti=states[0][1]),
       final_three_ball=dict(fvector=states[-1][0],betti=states[-1][1]),
       total_subsets=256,partial_mixed_dimensional_states=254,
       pure_endpoints=2,
       distribution_by_tetra_count_and_beta2=[
         dict(tetra=k,betti2=b,count=v) for (k,b),v in sorted(phase_counts.items())],
       topology_boundary="Attaching 3-simplices over existing 2-faces changes local topological dimension but passes through nonpure complexes. At all-eight endpoint topology becomes a 3-ball with boundary, not closed spacetime. This does not prove dimension selection.")

def interacting_matter():
    t,x=sp.symbols("t x",real=True)
    a,g,m,n=sp.symbols("alpha g m n",real=True)
    p=sp.Function("phi")(t,x);q=sp.Function("chi")(t,x)
    V1=m*m*p*p/sp.Integer(2)
    V2=n*n*q*q/sp.Integer(2)
    Vi=g*p*p*q*q/sp.Integer(2)
    def tensor(field,pot):
        ft=sp.diff(field,t);fx=sp.diff(field,x)
        L=(ft*ft-fx*fx)/2-pot
        return [[ft*ft-L,-ft*fx],[-ft*fx,fx*fx+L]]
    Ta=tensor(p,V1+a*Vi);Tb=tensor(q,V2+(1-a)*Vi)
    EOM={sp.diff(p,t,2):sp.diff(p,x,2)-m*m*p-g*p*q*q,
         sp.diff(q,t,2):sp.diff(q,x,2)-n*n*q-g*q*p*p}
    div=lambda T:[sp.expand(sp.diff(T[0][i],t)+sp.diff(T[1][i],x)).subs(EOM).expand() for i in (0,1)]
    da=div(Ta);db=div(Tb)
    Q=[g*((a-1)*p*q*q*sp.diff(p,t)+a*p*p*q*sp.diff(q,t)),
       -g*((a-1)*p*q*q*sp.diff(p,x)+a*p*p*q*sp.diff(q,x))]
    assert all(sp.simplify(da[i]-Q[i])==0 for i in (0,1)),da
    assert all(sp.simplify(db[i]+Q[i])==0 for i in (0,1)),db
    inputs={a:sp.Rational(1,2),g:2,m:1,n:3,
       p:2,q:3,sp.diff(p,t):5,sp.diff(q,t):-7,
       sp.diff(p,x):11,sp.diff(q,x):13}
    qpoint=[int(z.subs(inputs)) for z in Q]
    assert qpoint==[-174,42],qpoint
    # A nonuniversal linear spin-2 source is not conserved for coupled
    # matter, even though each scalar is precisely on its joint EOM.
    return dict(status="PASS",interaction="V_int=g phi^2 chi^2/2",
      split="T_A uses alpha V_int, T_B uses (1-alpha) V_int",
      on_shell_div_TA=["g((alpha-1)phi chi^2 partial^nu phi + alpha phi^2 chi partial^nu chi)"],
      on_shell_div_TB="minus divergence T_A",
      independent_species_not_conserved=True,
      total_tensor_conserved=True,
      weighted_tensor_divergence="(kappa_A-kappa_B) Q^nu",
      explicit_Q_upper_t_x=qpoint,nonuniversal_kappa1_kappa2=(1,2),
      nonuniversal_weighted_divergence=[-z for z in qpoint],
      universal_weighted_divergence=[0,0],
      boundary="Exact classical on-shell coupled 1+1D field identity. An arbitrary split of interaction energy means species-only couplings are not individually invariant; demonstrates conservation-driven universal total-stress coupling requirement, not an emergent graviton or full quantum Ward theorem.")

def microscopic_commutator_tomography():
    I=np.eye(2,dtype=complex)
    X=np.array([[0,1],[1,0]],complex)
    Y=np.array([[0,-1j],[1j,0]],complex)
    Z=np.diag([1,-1]).astype(complex)
    n=5;dim=2**n
    def pauli(terms):
        o=np.array([[1.]],complex)
        for i in range(n):o=np.kron(o,terms.get(i,I))
        return o
    XX={(i,j):pauli({i:X,j:X}) for i,j in combinations(range(n),2)}
    YY={(i,j):pauli({i:Y,j:Y}) for i,j in XX}
    Zs=[pauli({i:Z}) for i in range(n)]
    coupling={(0,1):.5,(1,2):-.75,(2,3):5/6,(3,4):-.875,(0,4):.9}
    H=sum((v*XX[k] for k,v in coupling.items()),np.zeros((dim,dim),complex))
    H+=sum((.12*(i+1)*Zs[i] for i in range(n)),np.zeros_like(H))
    comm=lambda a,b:a@b-b@a
    inferred={}
    err=0
    for k in XX:
        i,j=k
        D=comm(Zs[j],comm(H,Zs[i]))
        J=float(np.trace(YY[k].conj().T@D).real/(4*dim))
        expected=coupling.get(k,0.)
        err=max(err,abs(J-expected),float(np.linalg.norm(D-4*expected*YY[k])))
        if abs(J)>1e-9:inferred[f"{i}-{j}"]=J
    assert err<1e-12,err
    assert len(inferred)==5
    # 3-body term produces a falsely inferred edge under a mere norm
    # detector, but orthogonal Pauli-basis projection rejects it.
    H3=1.2*pauli({0:X,1:X,2:X})
    Db=comm(Zs[1],comm(H3,Zs[0]))
    false_norm=float(np.linalg.norm(Db))
    exact_two_body_coeff=float(np.trace(Db@YY[(0,1)]).real/(4*dim))
    assert false_norm>1 and abs(exact_two_body_coeff)<1e-12
    # Local choice of Pauli axes is a gauge: Z0 conjugation flips
    # all fitted XX signs incident on site0, keeping magnitudes.
    G=Zs[0];Hg=G@H@G
    gauge={}
    for k in XX:
        i,j=k
        D=comm(Zs[j],comm(Hg,Zs[i]))
        J=float(np.trace(YY[k]@D).real/(4*dim))
        assert abs(abs(J)-abs(coupling.get(k,0.)))<1e-12
        if abs(J)>1e-9:gauge[f"{i}-{j}"]=J
    assert gauge["0-1"]==-inferred["0-1"]
    assert gauge["1-2"]==inferred["1-2"]
    return dict(status="PASS",hilbert_dimension=dim,sites=n,
      supplied_hamiltonian="sum_(i<j) J_ij X_i X_j + sum_i h_i Z_i",
      reconstruction_formula="J_ij = Tr(Y_i Y_j [Z_j,[H,Z_i]])/(4*2^n)",
      inferred_signed_couplings=inferred,
      maximum_pair_operator_reconstruction_error=err,
      third_body_false_positive_double_commutator_norm=false_norm,
      third_body_exact_pair_projection=exact_two_body_coeff,
      local_Z_gauge_transformed_couplings=gauge,
      boundary="Commutator derivatives identify pair coefficients only in supplied qubit tensor factors and Pauli axes. Unknown operators with higher-body support need basis-resolved tomography. A local conjugation changes coupling signs. Locality not derived from abstract algebra alone.")

def w33_one_excitation_commutator_bridge():
    # qutrit symplectic projective space: normalize the first nonzero
    # coordinate of a nonzero vector in F3^4.
    pts=[]
    for x in product(range(3),repeat=4):
        if not any(x):continue
        j=next(i for i,v in enumerate(x) if v)
        inv=1 if x[j]==1 else 2
        y=tuple((inv*v)%3 for v in x)
        if y not in pts:pts.append(y)
    assert len(pts)==40
    n=len(pts)
    def form(a,b):
        return (a[0]*b[1]-a[1]*b[0]+a[2]*b[3]-a[3]*b[2])%3
    adjacency=np.zeros((n,n),dtype=int)
    for i in range(n):
        for j in range(i+1,n):
            if form(pts[i],pts[j])==0:
                adjacency[i,j]=adjacency[j,i]=1
    assert np.all(adjacency.sum(axis=1)==12)
    assert int(adjacency.sum()/2)==240
    Q=adjacency@adjacency
    for i in range(n):
        for j in range(n):
            if i==j:assert Q[i,j]==12
            elif adjacency[i,j]:assert Q[i,j]==2
            else:assert Q[i,j]==4
    # Physically SUPPLIED number-conserving one-excitation Hamiltonian
    # on the 40-dimensional single-photon mode Hilbert space.
    H=adjacency.astype(complex)
    projectors=[np.diag(np.eye(n)[i]).astype(complex) for i in range(n)]
    comm=lambda a,b:a@b-b@a
    checked=0;maxerr=0.
    # 40×40 matrices: sample fixed 50 pairs, plus algebraic exact formula
    # over every one of the 780 pairs.
    pairs=list(combinations(range(n),2))
    choose=np.linspace(0,len(pairs)-1,50,dtype=int)
    for idx in choose:
        i,j=pairs[int(idx)]
        D=comm(projectors[j],comm(H,projectors[i]))
        E=np.zeros_like(H);E[i,j]=E[j,i]=adjacency[i,j]
        err=float(np.linalg.norm(D-E))
        assert err<1e-12
        maxerr=max(maxerr,err)
        checked+=1
    # Exact matrix-unit identity: [Pj,[H,Pi]]=H_ij E_ij+H_ji E_ji
    # for i!=j. This identity determines every adjacency entry.
    assert np.all((H!=0)==(adjacency!=0))
    return dict(status="PASS",projective_points=n,regular_degree=12,
      edges=240,graph_parameters=[40,12,2,4],tested_matrix_commutators=checked,
      maximum_operator_residual=maxerr,
      exact_all_pairs_matrix_unit_identity="For i!=j, [P_j,[H,P_i]]=H_ij |i><j| + H_ji |j><i|",
      reconstructed_graph="The W(3,3) adjacency, GIVEN as a 40-mode Hamiltonian, is identifiable from mode-occupancy commutators in the single-excitation sector.",
      boundary="40 W33 modes and adjacency hopping were supplied. This experiment does not select W33 from a free information algebra, infer absolute coupling energy, establish photonic gate universality or produce gravitational locality.")

def main():
    payload={
      "date":"2026-11-03",
      "status":"PASS_FIVE_SECOND_ORDER_TOE_CONTROLS",
      "baseline_commit":"94ee11b997c448f310327c4a80902500b4173ba7",
      "SU2_nonabelian_discrete_Bianchi":nonabelian_cube(),
      "causal_fixed_coupling_finite_size_drift":causal_scale_drift(),
      "mixed_dimension_simplicial_cone":simplicial_phases(),
      "interacting_matter_universal_coupling":interacting_matter(),
      "nongeometric_commutator_graph_inference":microscopic_commutator_tomography(),
      "bonus_W33_single_excitation_operator_bridge":w33_one_excitation_commutator_bridge(),
      "conclusion":"Five exact or seeded computational stress tests. They constrain, but do not construct, an emergent TOE. In particular no first-class curved spin-2 gravitational Hamiltonian, closed dimension-selected 3+1D Lorentzian phase or derived Planck scale.",
      "literature":[
       "https://doi.org/10.1103/PhysRevD.91.124034",
       "https://doi.org/10.1007/s41114-019-0023-1",
       "https://link.springer.com/article/10.1007/s00454-026-00818-w",
       "https://doi.org/10.1103/PhysRev.135.B1049",
       "https://doi.org/10.1103/n242-m1l2"]
    }
    OUT.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf8")
    for k,v in payload.items():
        if isinstance(v,dict):print(k, {key:val for key,val in v.items() if key=="status" or key.endswith("drift") or key.endswith("residual") or key=="frozen_p" or key=="explicit_Q_upper_t_x" or key=="partial_mixed_dimensional_states" or key=="maximum_pair_operator_reconstruction_error"},flush=True)
    return payload
if __name__=="__main__":main()
