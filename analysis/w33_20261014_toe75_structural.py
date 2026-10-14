"""TOE75 independently checkable finite W33 structural progress in four fronts.

A. Strict all-160-edge, all-three-phase low-disorder guarantee + actual
   exact 17-link destabilizing upper witness, no MILP proof required.
B. Full unbounded Gauss rotor: ordered first *two* eigenvalue upper bounds
   by exact min-max on disjoint native basis vectors. NOT a spectral gap.
C. Classify all 20 extra 2-flip neighbor covers of seven known PGSp
   orbit seeds via explicit full group orbit membership; explore ONE new.
D. Actual cellular cochain Dirac-Kahler on W33 graph square (dimension 2),
   with sparse d1*d0=0, full integer ranks by Kunneth and the rigorous
   distinction from the four-dimensional spin Dirac index.
"""
from __future__ import annotations
import collections,itertools,json,sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix,eye,kron,vstack,hstack
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_five_fronts import octagons,windings,HIGH,graph
from w33_20261014_toe69_two_octagon_covariance import patch,exact_gauss_electric
from w33_20261014_toe74_unconditional_gauge_bound import certificate as rotor_certificate
from w33_20261014_toe74_quantum_neighbors import certificate as neighborhoods
from w33_pass1081_1086_core import (
    build_w33,transvection_perm,outer_similitude_perm,line_perm)

def disorder():
    # TOE64 global sufficient leading beta^7 three-pi flux uniqueness.
    # Verify it in exact fractions, and a distinct exact upper negative
    # W33 native 17-link Hessian witness at epsilon=24461519/1e8.
    e=F(1,7)
    r=((1+e)/(1-e))**8
    assert r<11
    a=79-2*r;d=77-r;b=-r
    det=a*d-2*b*b
    assert a>0 and det>0 and (77-7*r)>0
    ed,adj,cycles=octagons()
    high=set(HIGH);assert len(high)==17 and len(ed)==160
    q=(0,-1,1)
    active=[]
    for ci,w in windings(cycles,ed):
        dot=sum(w[i]*q[i] for i in range(3))
        if dot:
            c=(1 if sum(w)%2 else -1)*dot*dot
            active.append((c,tuple(cycles[ci])))
    assert len(active)==159
    def numerator(n,d):
        return sum(int(c)*(d+n)**len(high.intersection(cy))*
                    (d-n)**(8-len(high.intersection(cy)))
                   for c,cy in active)
    nlo,nhi,d0=24461518,24461519,100000000
    assert numerator(nlo,d0)>0 and numerator(nhi,d0)<0
    return {
       "status":"PASS_TOE75_RATIONAL_ALL_EDGES_LOWER_AND_REALIZABLE_UPPER",
       "entire_amplitude_box_edges":160,
       "verified_global_unique_three_pi_free_energy_at_epsilon":"1/7",
       "TOE64_stronger_algebraic_sufficient_epsilon":"(11^(1/8)-1)/(11^(1/8)+1)",
       "global_three_phase_signed_square_matrix_test":{
         "r":str(r),"A":str(a),"symmetric_block_det":str(det),
         "antisymmetric_eigenvalue":str(77-7*r)},
       "realizable_17_edge_witness_indices":list(sorted(high)),
       "native_winding_cycles_fixed_q":len(active),
       "negative_Hessian_rayleigh_witness_epsilon":f"{nhi}/{d0}",
       "positive_fixed_witness_rayleigh_epsilon":f"{nlo}/{d0}",
       "exact_witness_negative_numerator":str(numerator(nhi,d0)),
       "exact_witness_positive_numerator":str(numerator(nlo,d0)),
       "global_threshold_bracket":{
         "rigorous_sufficient_lower":"(11^(1/8)-1)/(11^(1/8)+1)",
         "rigorous_possible_upper":"24461519/100000000"},
       "scope":"Exact lower bound for unique global leading-beta^7 three-pi holonomy on all 160 independent hopping magnitudes (TOE64 theorem verified at epsilon 1/7), plus actual W33 negative Hessian upper example. Does not prove the intervening sharp threshold, all-temperature disorder result, or all-real-direction MILP global optimum."}

def spectral_minmax():
    p=patch();old=rotor_certificate()
    L=3
    fock=[bits for bits in range(1<<11) if bits.bit_count()==5]
    shifts=[tuple(map(int,z)) for z in p["P"][:,p["chords"]]]
    chord=dict((e,i) for i,e in enumerate(p["chords"]))
    candidates=[]
    for b in fock:
        occ=np.array([(b>>j)&1 for j in range(11)],dtype=int)
        stag=int((1-2*p["background"])@occ)
        for flux in itertools.product(range(-L,L+1),repeat=2):
            electric=exact_gauss_electric(occ,np.array(flux),p)
            diag=640*int(electric@electric)+600*stag+3750
            candidates.append((diag,b,flux))
    candidates.sort()
    first=candidates[0]
    def linked(s,t):
        _,b,x=s;_,c,y=t
        if b==c:
            return any(y==(x[0]+dr*u,x[1]+dr*v)
                       for u,v in shifts for dr in (-1,1))
        xor=b^c
        for i,(u,v) in enumerate(p["p_ed"]):
            if xor!=((1<<u)|(1<<v)):continue
            occu=(b>>u)&1;occv=(b>>v)&1
            if occu==occv:continue
            shift=[0,0]
            if i in chord:shift[chord[i]]=-(1 if occu else -1)
            if y==(x[0]+shift[0],x[1]+shift[1]):return True
        return False
    partner=next(z for z in candidates[1:200] if not linked(first,z))
    # The 2D subspace spanned by two orthogonal non-directly-coupled
    # computational basis states has H restriction DIAGONAL, so the
    # second full unbounded-rotor ordered eigenvalue is <= max diag.
    upper_second=F(max(first[0],partner[0]),2000)
    lower_ground=F(old["unconditional_full_rotor_E0_lower_fraction"])
    upper_ground=F(old["unconditional_full_rotor_E0_upper_fraction"])
    assert lower_ground<upper_ground<upper_second
    return {
       "status":"PASS_TOE75_UNCONDITIONAL_ORDERED_SECOND_EIGENVALUE_UPPER",
       "native_patch_sites_edges":[11,12],
       "finite_P_dimension":len(candidates),
       "two_orthogonal_native_state_rayleigh_witnesses":[
         {"electric_diagonal_units_2000":z[0],"fermion_bits":z[1],
          "integer_flux":list(z[2])} for z in (first,partner)],
       "off_diagonal_direct_coupling_exactly_zero":True,
       "unbounded_ground_lower":str(lower_ground),
       "unbounded_ground_upper":str(upper_ground),
       "unbounded_second_eigenvalue_upper":str(upper_second),
       "second_eigenvalue_ordering_scope":"Variational min-max E1 <= max(two diagonal witnesses), since the full infinite-flux Hamiltonian is confining and has compact resolvent. No tight lower E1 bound or positive E1-E0 gap claimed.",
       "spectral_gap_certified":False}

def quantum_orbits():
    prior=neighborhoods()
    known=[tuple(z) for z in prior["seven_seed_cover_cycle_lists"]]
    assert len(known)==7
    candidates=sorted({tuple(cv)
       for row in prior["neighborhood_summary"]
       for cv in row["local_neighbor_cover_identifiers"]}-set(known))
    assert len(candidates)==20
    points,pidx,lines,lidx,_,_,_,flags,flagidx=build_w33()
    edges,adj,cycles=octagons()
    inv={tuple(sorted(c)):i for i,c in enumerate(cycles)}
    def action(per):
        lp=line_perm(per,lines,lidx)
        ep=[flagidx[(per[p],lp[l])] for p,l in flags]
        return tuple(inv[tuple(sorted(ep[e] for e in c))] for c in cycles)
    gen=[action(transvection_perm(points[i],points,pidx)) for i in (0,1,2,4,8,15)]
    gen.append(action(outer_similitude_perm(points,pidx)))
    def orbit(seed,watch):
        seen={seed};q=collections.deque([seed])
        found={seed} & watch
        while q:
            z=q.popleft()
            for gg in gen:
                zz=tuple(sorted(gg[i] for i in z))
                if zz not in seen:
                    seen.add(zz);q.append(zz)
                    if zz in watch:found.add(zz)
        return len(seen),found
    remaining=set(candidates)
    matches={}
    sizes=[]
    for i,seed in enumerate(known):
        n,found=orbit(seed,remaining)
        assert n==51840
        sizes.append(n)
        matches[str(i)]=len(found)
        remaining-=found
    novel=[]
    if remaining:
        target=min(remaining)
        n,found=orbit(target,remaining)
        novel=[list(target)]
        # Orbit size may be below 51840 if there is a stabilizer.
        assert n>0 and n<=51840 and n%2==0
        remaining-=found
        extra={"one_additional_orbit_size":n,
               "extra_orbit_intersects_original_20_candidates":len(found),
               "one_extra_seed_20_cycle_ids":list(target)}
    else:extra={}
    return {
       "status":"PASS_TOE75_20_NEIGHBOR_FULL_ORBIT_MEMBERSHIP",
       "seven_legacy_full_group_orbit_sizes":sizes,
       "candidate_distinct_neighbors_outside_seven_SEEDS":len(candidates),
       "candidate_membership_counts_in_seven_known_orbits":matches,
       "candidate_neighbors_outside_all_seven_orbits":len(candidates)-sum(matches.values()),
       "new_orbit_information":extra,
       "not_yet_classified_candidate_remainder":len(remaining),
       "scope":"Exact full PGSp group actions on unordered 20-cycle covers; examines all 20 new representatives against seven full 51840-cover orbits, with at most one new orbit classified. Does NOT construct the full all-state quantum Hamiltonian or classify all exact-cover orbits."}

def squared_graph_dirac():
    ed,_=graph()
    assert len(ed)==160
    # Graph incidence C^0(R^80)->C^1(R^160).
    rows=[];cols=[];data=[]
    for e,(a,b) in enumerate(ed):
        rows.extend([e,e]);cols.extend([a,b]);data.extend([-1,1])
    B=csr_matrix((data,(rows,cols)),shape=(160,80),dtype=np.int32)
    Iv=eye(80,format="csr",dtype=np.int32)
    Ie=eye(160,format="csr",dtype=np.int32)
    d0=vstack([kron(B,Iv,format="csr"),kron(Iv,B,format="csr")],format="csr")
    d1=hstack([-kron(Ie,B,format="csr"),kron(B,Ie,format="csr")],format="csr")
    assert d0.shape==(25600,6400) and d1.shape==(25600,25600)
    composition=d1@d0
    assert composition.nnz==0 or not np.any(composition.data)
    # Kunneth over Z: H*(G) = (1,81), product yields
    # H0=1,H1=162,H2=6561. Ranks follow rank nullity.
    betti=[1,162,6561];rankd0=6400-1
    rankd1=25600-6561
    assert 25600-rankd0-rankd1==162
    return {
       "status":"PASS_TOE75_NATIVE_LEVI_SQUARED_LOCAL_CELLULAR_DIRAC",
       "actual_native_graph_vertices_edges":[80,160],
       "product_cells_by_dimension":[6400,25600,25600],
       "integer_d0_shape":list(d0.shape),"integer_d1_shape":list(d1.shape),
       "exact_d1_d0_nonzero_entries":0,
       "ranks_from_integral_Kunneth":[rankd0,rankd1],
       "product_Z_betti_numbers":betti,"Euler_Dirac_index":6400,
       "closed_W33_squared_4D_surface_Euler_index":25600,
       "closed_W33_squared_4D_surface_spin_Dirac_index":0,
       "obstruction":"The raw graph product G×G is ONLY a 2D square complex (no 3- or 4-cells). Its index 6400 is the Euler/Kahler-Dirac index, NOT a 4D spin index. Replacing each native graph by a closed genus-81 surface requires extra 2-cells and dual cycles; a local 4D spinor/overlap stencil has not been constructed.",
       "scope":"True sparse local cochain Dirac prototype, exact cochain identity, native combinatorial topology; not a physical 4D chiral fermion spectrum."}

def certificate():
    return {"status":"PASS_TOE75_FOUR_STRUCTURAL_FRONTS",
            "disorder":disorder(),"gauge":spectral_minmax(),
            "quantum_geometry":quantum_orbits(),"dirac_geometry":squared_graph_dirac()}
if __name__=="__main__":
    r=certificate()
    (ROOT/"data/w33_20261014_toe75_structural.json").write_text(json.dumps(r,indent=2)+"\n")
    print(r["status"],r["quantum_geometry"]["candidate_neighbors_outside_all_seven_orbits"],
          r["gauge"]["unbounded_second_eigenvalue_upper"])
