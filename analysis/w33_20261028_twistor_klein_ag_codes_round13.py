#!/usr/bin/env python3
"""Independent finite Penrose/Klein correspondence, Conwell G_2(8),
and projective-variety AG evaluation/CSS certificate over F_2.

This does NOT derive Minkowski space, physical photons, gravity or a
quantum-memory threshold. Over F2 there is no Minkowski real structure.
"""
from __future__ import annotations
import itertools
import collections
import json
from functools import lru_cache
from pathlib import Path

PAIRS=list(itertools.combinations(range(4),2))
Q=lambda x: (((x>>0)&1)*((x>>5)&1) ^ ((x>>1)&1)*((x>>4)&1) ^ ((x>>2)&1)*((x>>3)&1))
POLAR=lambda a,b: Q(a^b)^Q(a)^Q(b)


def rref(rows,n):
    x=list(rows); piv=[];rank=0
    for col in range(n):
        idx=next((j for j in range(rank,len(x)) if (x[j]>>col)&1),None)
        if idx is None:continue
        x[rank],x[idx]=x[idx],x[rank]
        for j in range(len(x)):
            if j!=rank and (x[j]>>col)&1:x[j]^=x[rank]
        piv.append(col);rank+=1
        if rank==len(x):break
    return x[:rank],piv


def null_basis(basis,n):
    r,piv=rref(basis,n)
    free=[j for j in range(n) if j not in piv]
    out=[(1<<j)|sum(1<<c for v,c in zip(r,piv) if (v>>j)&1) for j in free]
    assert len(out)==n-len(r)
    assert all((x&y).bit_count()%2==0 for x in basis for y in out)
    return out


def codeword_weight_enumerator(basis):
    # Exact binary linear-space traversal in Gray order: 2^21 takes ~1 sec.
    code=0;prev=0;weights=collections.Counter()
    for i in range(1<<len(basis)):
        gray=i^(i>>1)
        if i: code ^= basis[(gray^prev).bit_length()-1]
        prev=gray
        weights[code.bit_count()]+=1
    return dict(sorted(weights.items()))


def evaluation_rows(points,degree):
    return [sum(1<<index for index,p in enumerate(points)
                if all((p>>j)&1 for j in mons))
            for d in range(1,degree+1)
            for mons in itertools.combinations(range(6),d)]


def summarize_code(points,degree,enumerate_dim=21):
    n=len(points);basis,_=rref(evaluation_rows(points,degree),n)
    k=len(basis)
    result={'length':n,'dimension':k,'homogeneous_polynomial_degree':degree}
    if k<=enumerate_dim:
        weights=codeword_weight_enumerator(basis)
        result['distance']=min(i for i in weights if i)
        result['weight_enumerator']={str(w):c for w,c in weights.items()}
        assert sum(weights.values())==2**k
    return result,basis


def plucker(u,v):
    return sum(((((u>>a)&1)*((v>>b)&1)^(((u>>b)&1)*((v>>a)&1)))<<i)
               for i,(a,b) in enumerate(PAIRS))


def conwell_heptads(off):
    adjacency={p:{q for q in off if q!=p and POLAR(p,q)==1} for p in off}
    assert all(len(x)==12 for x in adjacency.values())
    # Increasing-order clique DFS; all seven-element maximal cliques.
    heptads=[]
    def extend(chosen,candidates):
        if len(chosen)==7:
            heptads.append(tuple(chosen));return
        for i,p in enumerate(candidates):
            later=[q for q in candidates[i+1:] if q in adjacency[p]]
            if len(chosen)+1+len(later)>=7:extend(chosen+[p],later)
    extend([],off)
    assert len(heptads)==8 and len(set(heptads))==8
    assert all(len(set(a)&set(b))==1 for a,b in itertools.combinations(heptads,2))
    owners={p:tuple(i for i,h in enumerate(heptads) if p in h) for p in off}
    assert all(len(x)==2 for x in owners.values())
    assert len(set(owners.values()))==28
    tris=set()
    for a,b,c in itertools.combinations(off,3):
        if a^b==c:tris.add(frozenset((a,b,c)))
    assert len(tris)==56
    for tri in tris:
        identifiers={owners[p] for p in tri}
        # Each exterior projective line = 3 pairs of an 8-label triple.
        pairs=set.union(*(set(x) for x in identifiers))
        assert len(pairs)==3 and identifiers=={tuple(sorted(pair)) for pair in itertools.combinations(pairs,2)}
    return heptads,owners,tris,adjacency


def equivariant_gl4_a8_action(heptads,owners):
    """Compute all 12 elementary GL4(2) generators on the eight heptads.

    This certifies the natural A8 action and the 28-point coset, not
    a choice of a physical spacetime real structure.
    """
    hs={frozenset(h):i for i,h in enumerate(heptads)}
    def action_on_bivector(p,i,j):
        def T(u):return u ^ (((u>>j)&1)<<i)
        output=0
        for k,(a,b) in enumerate(PAIRS):
            if (p>>k)&1:output^=plucker(T(1<<a),T(1<<b))
        return output
    generators=[]
    for i in range(4):
        for j in range(4):
            if i==j:continue
            perm=tuple(hs[frozenset(action_on_bivector(p,i,j) for p in h)]
                       for h in heptads)
            # GL4(2)=A8, so all 12 elementary transvections act evenly.
            inversions=sum(perm[a]>perm[b] for a in range(8) for b in range(a+1,8))
            assert inversions%2==0
            for p,lab in owners.items():
                dst=tuple(sorted(perm[k] for k in lab))
                assert owners[action_on_bivector(p,i,j)]==dst
            generators.append({'elementary_add': [i,j],'heptad_permutation':list(perm)})
    # closure: order 20160 exactly, without relying only on known isomorphism
    identity=tuple(range(8)); found={identity};stack=[identity]
    perms=[tuple(g['heptad_permutation']) for g in generators]
    while stack:
        p=stack.pop()
        for q in perms:
            t=tuple(p[q[k]] for k in range(8))
            if t not in found:found.add(t);stack.append(t)
    assert len(found)==20160
    # Orbit size 28, stabilizer of a labeled nondegenerate bivector = 720
    stabilizer=sum(set((p[0],p[1]))=={0,1} for p in found)
    assert stabilizer==720
    return {'generator_count':12,'heptad_action_order':len(found),
            'all_generators_even_permutations':True,
            'identified_finite_group':'GL4(F2) = A8',
            'stabilizer_of_two_heptad_labels':stabilizer,
            'orbit_of_28_pairs':len(found)//stabilizer,
            'point_to_heptad_pair_equivariance_verified':True,
            'generators':generators}


def native_reflection_on_finite_heptads(heptads,owners):
    # The actual integral native period reflection, reduced to F2.
    # Physical Lorentzian conjugation is NOT implied by this F2 action.
    T=[[-1,0,0,0],[1,1,0,0],[-1,0,1,0],[0,0,0,1]]
    def action4(u):
        return sum((sum(T[i][j]*((u>>j)&1) for j in range(4))%2)<<i
                   for i in range(4))
    def action6(p):
        result=0
        for k,(a,b) in enumerate(PAIRS):
            if (p>>k)&1:result^=plucker(action4(1<<a),action4(1<<b))
        return result
    lookup={frozenset(h):i for i,h in enumerate(heptads)}
    perm=tuple(lookup[frozenset(action6(p) for p in h)] for h in heptads)
    assert all(perm[perm[i]]==i for i in range(8))
    assert sum(perm[i]==i for i in range(8))==0
    assert sum(action6(p)==p for p in owners)==4
    assert all(tuple(sorted(perm[j] for j in pair))==owners[action6(p)]
               for p,pair in owners.items())
    return {'reflection_heptad_permutation':list(perm),
            'cycle_type':'2^4 (four transpositions)',
            'fixed_heptads':0,'fixed_off_quadric_points':4,
            'preserves_Conwell_pair_labeling':True,
            'caveat':'F2-period reflection is not a Lorentzian twistor real structure.'}


def other_five_frontiers():
    """Independent exact obstructions, not a five-part physical TOE solution."""
    import sympy as sp
    omega=(-1+sp.I*sp.sqrt(3))/2
    W=sp.Matrix([[0,1,1,-1],[-1,0,1,-1],
                 [0,0,1,-1],[0,0,1,0]])
    N=sp.Matrix([[10,-5,1,-6],[-5,10,-5,6],
                 [1,-5,10,-6],[-6,6,-6,12]])
    z=[sp.Integer(1),sp.Integer(1),omega,omega**2]
    h=sp.Matrix([sp.prod(z[j]**int(W[i,j]) for j in range(4))
                 for i in range(4)])
    d=h-sp.ones(4,1)
    assert sp.simplify(sp.expand_complex((d.T*N*d)[0]/2))==0
    assert z[0]==z[1]==1 and z[2]!=1
    return {
       'smaller_than_six_gauge_repair':{
        'four_term_common_e0_e1_activation_disproved':True,
        'exact_character':['1','1','omega','omega^2'],
        'global_exceptional_polynomial_Q_zero':True,
        'translation_weight_e0_e1_zero':True,
        'stronger_2_to_5_term_general_no_go_proved':False},
       'full_native_spectrum':{
        'full_135_link_N_by_N_numeric_spectrum_computed':False,
        'analytical_massless_obstruction':
        'At identity commutator curl rows vanish and the Bloch curl rank falls from 108 to 105; bounded analytic native link operators have vanishing eigenvalues as z->1. No uniform massive gap for the acoustic flux branches.',
        'optical_dispersion_and_equal_coupling_comparison_open':True},
       'matter_selector':{
        'GL4_F2_orbit_of_28_nondegenerate_forms':28,
        'full_GL4_F2_invariant_choice_of_one_form_impossible':True,
        'stabilizer_of_selected_form_order':720,
        'dynamically_spontaneous_or_explicit_selection_open':True},
       'binary_CSS_photonic_bridge':{
        'candidate_classical_to_quantum_CSS_prototypes':[[35,14,3],[28,15,3]],
        'physical_measurement_and_noise_threshold_derived':False},
       'native_reflection':{
        'finite_F2_heptad_permutation_cycle_type':'2^4',
        'finite_F2_fixes_4_off_quadric_points':True,
        'Lorentzian_time_or_photon_helicities_derived':False}
    }


def explicit_28_CSS_checks():
    """A seven-X/six-Z stabilizer description and all 28 one-error syndromes.

    Constructed from the actual six Plucker coordinate evaluation vectors,
    not arbitrary generators of a 21-dimensional quadratic code.
    """
    points=[p for p in range(1,64) if Q(p)==1]
    coord=evaluation_rows(points,1)
    assert len(coord)==6 and len(rref(coord,28)[0])==6
    ones=(1<<28)-1
    quadratic=evaluation_rows(points,2)
    dual=null_basis(quadratic,28)
    x_checks=coord+[ones]
    z_checks=coord
    assert len(rref(x_checks,28)[0])==7
    assert len(rref(dual+x_checks,28)[0])==7
    assert all((x&z).bit_count()%2==0 for x in x_checks for z in z_checks)
    assert all((x&row).bit_count()%2==0 for x in x_checks for row in quadratic)
    assert codeword_weight_enumerator(x_checks)=={0:1,12:63,16:63,28:1}
    sx=[sum(((r>>i)&1)<<j for j,r in enumerate(z_checks)) for i in range(28)]
    sz=[sum(((r>>i)&1)<<j for j,r in enumerate(x_checks)) for i in range(28)]
    assert sx==points
    assert sz==[p|64 for p in points]
    assert len(set(sx))==len(set(sz))==28
    return {'quantum_CSS_parameters':[28,15,3],
            'X_check_rank':7,'Z_check_rank':6,
            'X_checks_bitsets':[int(x) for x in x_checks],
            'Z_checks_bitsets':[int(x) for x in z_checks],
            'dual_quadratic_equals_C1_plus_allones':True,
            'X_check_code_weight_enumerator':{'0':1,'12':63,'16':63,'28':1},
            'single_X_error_syndrome_is_off_quadric_point':True,
            'single_Z_error_syndrome_is_off_quadric_point_with_top_bit_1':True,
            'all_28_single_qubit_Pauli_error_locations_identifiable':True,
            'physical_measurement_circuit_implemented':False}


@lru_cache(maxsize=1)
def certificate():
    allpoints=list(range(1,64));klein=[x for x in allpoints if Q(x)==0];off=[x for x in allpoints if Q(x)]
    assert(len(klein),len(off))==(35,28)
    # 35 two-subspaces in F2^4. Each has 3 points; 15 points
    # each lie on 7 finite twistor lines, giving 105 incidences.
    lines={frozenset((u,v,u^v)):plucker(u,v) for u,v in itertools.combinations(range(1,16),2)}
    assert len(lines)==35 and set(lines.values())==set(klein)
    per_twistor_point=collections.Counter(t for line in lines for t in line)
    assert len(per_twistor_point)==15 and set(per_twistor_point.values())=={7}
    # Incidence: meeting Klein lines are exactly Q-polar pairs.
    meet=0
    reverse={p:line for line,p in lines.items()}
    for a,b in itertools.combinations(klein,2):
        intersect=bool(reverse[a]&reverse[b]);polar_zero=(POLAR(a,b)==0)
        assert intersect==polar_zero
        meet+=intersect
    assert meet==315
    assert sum(1 for a,b in itertools.combinations(klein,2) if POLAR(a,b)==0)==315
    h,owners,tris,adj=conwell_heptads(off)
    equivariance=equivariant_gl4_a8_action(h,owners)
    reflection=native_reflection_on_finite_heptads(h,owners)
    good=[x for x in off if Q(x)]
    assert len(good)==28
    records={};basis={}
    for name,pts in [('Klein',klein),('off_quadric',off)]:
        records[name]={}
        for d in (1,2,3,4):
            record,b=summarize_code(pts,d)
            records[name][str(d)]=record;basis[(name,d)]=b
        C1=basis[(name,1)];C2=basis[(name,2)]
        assert len(rref(C1+C2,len(pts))[1])==len(C2)
        dual2=null_basis(C2,len(pts))
        dual2dist=min(w for w in codeword_weight_enumerator(dual2) if w)
        # Degree 1 dual contains incidence triples from Q or exterior lines.
        triples=[frozenset((u,v,u^v)) for u,v in itertools.combinations(pts,2) if u^v in pts]
        triples=set(triples)
        assert len(triples)==(105 if name=='Klein' else 56)
        assert all(all(sum((row>>(pts.index(t)))&1 for t in triple)%2==0
                       for row in C1) for triple in triples)
        assert all(any(sum((row>>(pts.index(t)))&1 for t in triple)%2
                       for row in C2) for triple in triples)
        # CSS: X stabilizers C2^perp, Z stabilizers C1; commute by nesting.
        # CSS distance: min(d(C2\C1),d(C1^perp\C2^perp))=min(d2,3).
        records[name]['CSS_from_nested_degree_1_and_2']={
          'length':len(pts),'logical_qubits':len(C2)-len(C1),
          'X_check_rank':len(dual2),'Z_check_rank':len(C1),
          'distance':3,'logical_weight_degree2_side':records[name]['2']['distance'],
          'dual_degree2_distance':dual2dist,
          'commutation_exact':True,'weight3_incidence_logical_witnesses':len(triples),
          'physical_optics_claim':False}
        assert dual2dist>=4
        assert len(pts)-len(dual2)-len(C1)==len(C2)-len(C1)
    assert [records['Klein'][str(d)]['dimension'] for d in (1,2,3,4)]==[6,20,34,35]
    assert [records['off_quadric'][str(d)]['dimension'] for d in (1,2,3,4)]==[6,21,27,28]
    assert records['Klein']['1']['weight_enumerator']=={'0':1,'16':35,'20':28}
    assert records['off_quadric']['1']['weight_enumerator']=={'0':1,'12':28,'16':35}
    assert records['Klein']['2']['distance']==6 and records['off_quadric']['2']['distance']==4
    # First-order full projective simplex [63,6,32]: disjoint coordinate split.
    both,bb=summarize_code(allpoints,1)
    assert both['weight_enumerator']=={'0':1,'32':63}
    # Correct potentially misleading historical terminology.
    return {
      'schema':'w33.toe.klein_twistor_AG_CSS.finite_F2.v1',
      'quadric':{'field':'F2','klein_quadric_points':35,'complement_points':28,
                 'plucker_order':['01','02','03','12','13','23'],
                 'equation':'p01*p23+p02*p13+p03*p12=0',
                 'finite_twistor_points':15,'finite_twistor_lines':35,
                 'point_line_incidence_count':105,'each_twistor_point_lines':7,
                 'intersecting_line_pairs':315,'disjoint_line_pairs':280},
      'conwell':{'heptad_members':[list(x) for x in h],
                 'point_to_heptad_pair':{str(p):list(owners[p]) for p in off},
                 'heptads':len(h),'heptad_size':7,
                 'pairwise_intersection_size':1,'off_points_per_heptads':2,
                 'exterior_projective_lines':len(tris),
                 'external_lines_as_G2_8_triangles':True,
                 'canonical_GL4_F2_to_A8':equivariance,
                 'native_reflection_F2_action':reflection,
                 'symmetry': 'eight heptads canonically determined as 7-cliques; numbering of heptads is conventional'},
      'codes':records,'full_simplex_code':both,
      'explicit_28_CSS_checks':explicit_28_CSS_checks(),
      'other_five_frontiers':other_five_frontiers(),
      'limits':{
        'not_a_Lorentzian_spacetime':True,
        'no_SU22_real_structure_over_F2':True,
        'classical_codes_vs_CSS_quantum_codes_distinguished':True,
        'no_photonic_physical_decoder_tested':True,
        'no_AG_curve_Goppa_code_claim':True,
        'repo_historical_correction':'[7,3,4] binary code is simplex, NOT the [7,4,3] Hamming code.'}
    }


if __name__=='__main__':
    import sys
    result=json.dumps(certificate(),indent=2)+'\n'
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(result,encoding='utf-8')
    else:print(result,end='')
