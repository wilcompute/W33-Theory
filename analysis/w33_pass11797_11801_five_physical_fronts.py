"""Five exact follow-ups to11796, with actual model inputs and named maps.

11797: all-order vacuum invariant/R reduction and finite outsider screen.
11798: E8 cocharacter, twisted modules and universal axion direction.
11799: all-order necessary mass lattices and finite coupling matrices.
11800: full Gaussian spectral residual, not a fictitious lower gap.
11801: uniform native two-hop operator, homogenized matter stress/fibers.
Prior two-hop rank-six repair belongs to11518; no rediscovery claim.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
from collections import Counter, defaultdict
from functools import lru_cache
from math import lcm, prod
import gzip, hashlib, json, sys
import numpy as np
import sympy as S
from sympy.matrices.normalforms import hermite_normal_form

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass11786_certified_spectral_transitions import I, parameters
from w33_pass11796_parity_complete_abelian_higgs import inputs, vevs
OUT=ROOT/'data/w33_pass11797_11801_five_physical_fronts.json'
RAW=ROOT/'data/w33_pass11797_full_benchmark_metadata.json.gz'


def load():
    raw=json.loads(gzip.decompress(RAW.read_bytes()))
    prior=json.loads((ROOT/'data/w33_pass11796_parity_complete_abelian_higgs.json').read_text())
    fields=raw['fields']; support=list(prior['symbolic_squared_VEV_norms'])
    charges={n:tuple(F(x) for x in f['q']) for n,f in fields.items()}
    return raw,prior,fields,support,charges


def corrected_r(field):
    r=list(map(F,field['RQ'])); r[0]+=6*F(field['G'][0]); return r


def selection(names,fields):
    nonr=[sum(F(fields[n]['nonR'][i]) for n in names) for i in range(4)]
    r=[sum(corrected_r(fields[n])[i] for n in names) for i in range(3)]
    return (all(x.denominator==1 and x%order==0 for x,order in zip(nonr,[6,3,2,2]))
            and all(x.denominator==1 and (x+1)%order==0 for x,order in zip(r,[6,3,2])))


def support_monomials(support,q,max_degree=4):
    out=defaultdict(list)
    for degree in range(max_degree+1):
        for names in combinations_with_replacement(support,degree):
            charge=tuple(sum(q[n][i] for n in names) for i in range(9))
            out[charge].append(names)
    return out


def vacuum_ring(fields,support,q):
    mat=S.Matrix.hstack(*(S.Matrix(q[n]) for n in support))
    null=mat.nullspace();fi=['n_17','n_47','n_50','n_80','n_82']
    assert mat.rank()==8 and len(null)==5
    assert all(v[support.index(n)]==0 for v in null for n in fi)
    # Independent seven charge directions: five FI fields and the two
    # singlet pairs; the eighth direction is the doublet charge.
    independent=fi+['n_9','n_37','n_35']
    assert S.Matrix.hstack(*(S.Matrix(q[n]) for n in independent)).rank()==8
    pairs={'x':['n_9','n_54'],'y':['n_37','n_38'],
           'M11':['n_35','n_36'],'M12':['n_35','n_40'],
           'M21':['n_39','n_36'],'M22':['n_39','n_40']}
    assert all(tuple(sum(q[n][i] for n in ns) for i in range(9))==(F(0),)*9 for ns in pairs.values())
    pair_r={k:list(map(str,[sum(corrected_r(fields[n])[i] for n in ns) for i in range(3)])) for k,ns in pairs.items()}
    assert pair_r['x']==['2','-1','0']
    assert all(pair_r[k]==['7','0','-1'] for k in pairs if k!='x')
    allowed=[]
    for a in range(1,8):
        for b in range(10):
            if (2*a+7*b+1)%6==0 and (-a+1)%3==0 and (-b+1)%2==0:
                allowed.append([a,b,2*(a+b)])
    assert min(x[2] for x in allowed)==8
    assert all(a%3==1 and b%6==3 for a,b,degree in allowed)
    leading=[]
    for cubes in combinations_with_replacement([k for k in pairs if k!='x'],3):
        names=pairs['x']+sum((pairs[k] for k in cubes),[])
        if selection(names,fields):leading.append(dict(invariants=['x',*cubes],fields=names))
    # Cross mesons carry the same odd fixed-point Z2; their total is even.
    assert len(leading)==19  # ten diagonal/y cubics and nine even cross-meson cubics
    A=S.Matrix([[1,0],[0,1]]);B=S.Matrix([[0,1],[1,0]])
    eps=S.Matrix([[0,1],[-1,0]]); meson=A.T*eps*B
    assert meson==S.diag(1,-1) and meson.det()==-1
    outside,free=mat.gauss_jordan_solve(-S.Matrix(q['n_81']))
    assert [outside[support.index(n)] for n in fi]==[1,0,0,0,1]
    assert selection(['n_81','n_17','n_82'],fields)
    return dict(status='PASS',support_charge_rank=8,nullspace_dimension=5,
        all_order_absent_pure_vacuum_fields=fi,
        abelian_neutral_pair_generators=pairs,corrected_pair_R=pair_r,
        gauge_invariant_ring='C[x,y,M11,M12,M21,M22]; M=A^T epsilon B for two negative/positive hidden doublet flavors. The baryon product is det(M), not another independent generator.',
        all_order_necessary_rule='x exponent a=1 mod3; total y/meson degree b=3 mod6; cross-meson count even. Additional fixed-point/instanton/coset rules and amplitudes still apply.',
        minimum_pure_support_degree=8,degree8_necessary_candidates=leading,
        degree8_distinct_field_multisets=len({tuple(sorted(r['fields'])) for r in leading}),
        VEV_mesons_at_unit_t=[[str(x) for x in row] for row in meson.tolist()],
        F_reduction='Both flavor matrices are invertible on11796. F_A=epsilon*B*(dW/dM)^T and F_B=-epsilon*A*(dW/dM); hence all doublet F terms vanish iff the complete2x2 meson gradient vanishes. Nonzero n9,n54,n37,n38 also require Wx=Wy=0.',
        generic_leading_boundary='W8=x*P3(y,M). Nonzero x forces all derivatives of P3 to vanish. A generic nonsingular cubic has no nonzero critical point; physical coefficients, special cancellations and higher orders decide the actual vacuum. No actual F-flatness is inferred.',
        outside81_fixed_core={'n_17':1,'n_82':1},
        outside81_all_order_F='F81=n17*n82*[lambda+G(x^3,y,M)]; every nonconstant invariant multiplier has x degree0 mod3 and total y/meson degree0 mod6 (plus even cross-meson count). First possible correction is x^3, six more elementary VEV powers. The cubic coefficient must be computed: if nonzero, no cancellation exists in a sufficiently small neutral-invariant neighborhood.',
        cubic81_oscillator_Rule5_control={'fields':['n_81','n_17','n_82'],
            'G2_twist_sum':'2','G2_holomorphic_left_oscillators':1,'G2_antiholomorphic_left_oscillators':4,
            'right_oscillators':0,'G2_only_antiholomorphic_instantons':True,'necessary_Rule5_passes':True,
            'other_planes_oscillator_numbers':0,
            'scope':'Counts recovered uniquely from total oscillator counts and signed RQ-q_shift on these three fields;1<=4 passes Rule5 for anti-only instantons. Additional fixed-point lattice sums/amplitude are not inferred from this one rule.'},
        prior='11796 owns support;10974 owns corrected G2 R+6theta-gamma and prime-plane rules;1107.2137/1301.2322 own additional CFT rules.')


def global_parity(raw,prior,fields):
    _,lattice,_,_,_,_=inputs()
    h=S.Matrix(lattice['integral_charge_lattice_basis']).applyfunc(S.Rational)
    alpha=S.Matrix([prior['primitive_order_two_character']])*h.inv()*lattice['lattice_denominator']
    basis=S.Matrix(raw['u1_embedding']).applyfunc(S.Rational); t=alpha*basis
    def e8(v):
        integral=all(x.q==1 for x in v)
        half=all(x.q==2 for x in v)
        return (integral or half) and sum(v).q==1 and sum(v)%2==0
    assert all(e8(list(t)[i:i+8]) for i in (0,8))
    assert not all(e8([x/2 for x in list(t)[i:i+8]]) for i in (0,8))
    states=0
    for name,f in fields.items():
        for p in f['weights']:
            value=t.dot(S.Matrix(p).applyfunc(S.Rational));states+=1
            assert value.q==1 and int(value)%2==prior['all176_field_parities'][name]
    rows=raw['model_text'].split('Shifts and Wilsonlines:\n')[1].split('end model')[0].strip().splitlines()
    shift_pairs=[t.dot(S.Matrix([S.Rational(x.strip()) for x in row.split(',')])) for row in rows]
    assert all(x.q==1 for x in shift_pairs) and alpha[0]==0
    # All string momenta P=l+kV+sum n_i W_i have integral t.P:
    # E8 self-duality covers l; the eight displayed pairings cover shifts.
    assert states==328
    anomalies=[]
    for power in [1,3]:
        value=sum(prod(abs(int(x)) for x in f['dim'].split(','))*
                  (alpha.dot(S.Matrix(f['q']).applyfunc(S.Rational)))**power for f in fields.values())
        anomalies.append(str(S.simplify(value)))
    assert anomalies==['0','0']
    return dict(status='PASS',charge_covector=[str(x) for x in alpha],E8xE8_vector=[str(x) for x in t],
        E8_lattice_membership=[True,True],half_vector_in_product_lattice=False,
        full_weight_states_verified=states,shift_and_Wilson_pairings=list(map(str,shift_pairs)),
        full_string_order_two='g(P)=exp(i*pi*t.P). E8 self-duality and integral t.V,t.W imply g^2=1 on every momentum coset, not only the328 massless weight states. Non-membership of t/2 gives nontrivial order2 on the E8 gauge torus.',
        universal_axion_anomalous_coordinate=str(alpha[0]),continuous_gravitational_and_cubic_traces=anomalies,
        universal_axion_scope='The coefficient along the declared unique anomalous U1 is exactly zero, so this element does not translate the universal anomalous axion in that input basis. Model-dependent/blow-up axion charge matrices and nonperturbative effects are not supplied.',
        prior='11793 charge HNF;11796 order2 field character and instanton parity controls; regenerated original orbifolder gauge embedding adds the global cocharacter witness.')


def augmented_charge(field):
    return list(map(F,field['q']))+list(map(F,field['nonR']))+corrected_r(field)+[F(abs(int(field['dim'].split(',')[3]))==2)]


def mass_lattice(fields,support):
    vectors={n:augmented_charge(f) for n,f in fields.items()};den=lcm(*(x.denominator for v in vectors.values() for x in v))
    columns=[S.Matrix([int(den*x) for x in vectors[n]]) for n in support]
    moduli=[6,3,2,2,6,3,2,2]
    for i,order in enumerate(moduli):
        v=S.zeros(17,1);v[9+i]=den*order;columns.append(v)
    original=S.Matrix.hstack(*columns);h=hermite_normal_form(original)
    dual=(h.T*h).inv()*h.T
    target=S.Matrix([0]*13+[-den]*3+[0])
    def membership(names):
        rhs=target-sum((S.Matrix([int(den*x) for x in vectors[n]]) for n in names),S.zeros(17,1))
        coords=dual*rhs
        if h*coords!=rhs:return False,{'span_obstruction':[str(x) for x in rhs-h*coords]}
        bad=next((i for i,x in enumerate(coords) if x.q!=1),None)
        if bad is not None:
            lam=dual[bad,:];assert all(x.q==1 for x in lam*original)
            return False,{'integer_lattice_annihilator':[str(x) for x in lam],'target_pairing':str((lam*rhs)[0])}
        return True,{}
    return membership,dict(denominator=den,Hermite_basis=[[str(x) for x in row] for row in h.tolist()],rank=h.rank(),
        scope='Lattice exclusion is all-order necessary with signed exponents; membership alone does not supply nonnegative powers, amplitudes or F-flatness. Gamma-corrected R and hidden SU2 center included.')


def couplings(fields,support,q,prior):
    monomials=support_monomials(support,q,4)
    membership,lat=mass_lattice(fields,support)
    # SM-conjugate pairs, including actual hypercharge checks.
    def names(dim,y):return [n for n,f in fields.items() if f['dim']==dim and F(f['q'][1])==F(y)]
    families={'d':(names('-3,1,1,1','-1/3'),names('3,1,1,1','1/3')),
              'u':(names('-3,1,1,1','2/3'),names('3,1,1,1','-2/3')),
              'e':(names('1,1,1,1','-1'),names('1,1,1,1','1')),
              'x':(names('-3,1,1,1','1/6'),names('3,1,1,1','-1/6')),
              'v':(names('1,1,1,1','-1/2'),names('1,1,1,1','1/2')),
              'H':(names('1,2,1,1','-1/2'),names('1,2,1,1','1/2'))}
    results={};requests=set()
    charge_matrix=S.Matrix.hstack(*(S.Matrix(q[n]) for n in support))
    fi=['n_17','n_47','n_50','n_80','n_82']
    def positive_core(names):
        rhs=-sum((S.Matrix(q[n]) for n in names),S.zeros(9,1))
        try:exponents,free=charge_matrix.gauss_jordan_solve(rhs)
        except ValueError:return False,{'outside_support_charge_span':True}
        fixed=[exponents[support.index(n)] for n in fi]
        assert not any(x.free_symbols for x in fixed)
        return all(x.q==1 and x>=0 for x in fixed),{'uniquely_fixed_FI_exponents':dict(zip(fi,map(str,fixed)))}
    def finite(names):
        target=tuple(-sum(q[n][i] for n in names) for i in range(9))
        hits=[]
        for ms in monomials.get(target,[]):
            full=tuple(names)+ms
            ds=sum(abs(int(fields[n]['dim'].split(',')[3]))==2 for n in full)
            if ds%2==0 and selection(full,fields):hits.append(full);requests.add(tuple(sorted(full)))
        return hits
    for sector,(rows,cols) in families.items():
        allowed=S.zeros(len(rows),len(cols));positive=S.zeros(len(rows),len(cols));degree=S.zeros(len(rows),len(cols));witnesses={};bad=[];cone_bad=[]
        for i,a in enumerate(rows):
            for j,b in enumerate(cols):
                ok,proof=membership([a,b]);allowed[i,j]=int(ok)
                if not ok:bad.append(dict(fields=[a,b],**proof))
                nonnegative,proof=positive_core([a,b]);positive[i,j]=int(ok and nonnegative)
                if not nonnegative:cone_bad.append(dict(fields=[a,b],**proof))
                hits=finite([a,b])
                if hits:degree[i,j]=min(map(len,hits));witnesses[f'{i},{j}']=[list(x) for x in hits]
        results[sector]=dict(rows=rows,columns=cols,all_order_lattice_allowed=[list(map(int,row)) for row in allowed.tolist()],
            finite_necessary_minimum_degrees=[list(map(int,row)) for row in degree.tolist()],finite_witnesses=witnesses,exact_all_order_exclusions=bad,
            all_order_nonnegative_core_mask=[list(map(int,row)) for row in positive.tolist()],exact_nonnegative_core_exclusions=cone_bad,
            all_order_mass_rank_upper_bound=matching_rank(positive.tolist()),
            lattice_matching_rank=matching_rank(allowed.tolist()),finite_matching_rank=matching_rank(degree.tolist()))
    basis=json.loads((ROOT/'data/w33_pass11793_order_four_matter_action.json').read_text())['candidate_three_family_Higgs_basis']
    yukawas={}
    for sector,rs,cs,hr in [('u','Q','u_c','H_u'),('d','Q','d_c','H_d'),('e','L','e_c','H_d')]:
        matrix=[];mask=[];witnesses={};excluded=[]
        for i,a in enumerate(basis[rs]):
            row=[];prow=[]
            for j,b in enumerate(basis[cs]):
                full=[a,b,basis[hr][0]];hits=finite(full)
                nonnegative,proof=positive_core(full);prow.append(int(nonnegative and membership(full)[0]))
                if not nonnegative:excluded.append(dict(fields=full,**proof))
                row.append(min(map(len,hits),default=0));witnesses[f'{i},{j}']=[list(x) for x in hits]
            matrix.append(row);mask.append(prow)
        yukawas[sector]=dict(minimum_degrees=matrix,witnesses=witnesses,necessary_matching_rank=matching_rank(matrix),
            all_order_nonnegative_core_mask=mask,all_order_rank_upper_bound=matching_rank(mask),exact_nonnegative_core_exclusions=excluded)
    # No right-handed neutrino assignment is supplied. Audit the actual
    # Weinberg operator and every odd SM/hidden singlet as a candidate.
    def necessary_matrix(rows,cols,prefix):
        mask=[];excluded=[]
        for a in rows:
            row=[]
            for b in cols:
                full=prefix(a,b)
                nonnegative,proof=positive_core(full)
                ok=nonnegative and membership(full)[0]
                row.append(int(ok))
                if not nonnegative:excluded.append(dict(fields=full,**proof))
            mask.append(row)
        return dict(rows=rows,columns=cols,necessary_mask=mask,
                    structural_rank_upper_bound=matching_rank(mask),
                    exact_core_exclusions=excluded)
    lepton=basis['L'];hu=basis['H_u'][0]
    neutral=[n for n,f in fields.items() if f['dim']=='1,1,1,1'
             and q[n][1]==0 and prior['all176_field_parities'][n]==1]
    neutrino=dict(Weinberg=necessary_matrix(lepton,lepton,lambda a,b:[a,hu,b,hu]),
        candidate_odd_singlets=neutral,
        Dirac=necessary_matrix(lepton,neutral,lambda a,b:[a,hu,b]),
        Majorana=necessary_matrix(neutral,neutral,lambda a,b:[a,b]),
        scope='Necessary perturbative holomorphic masks on the same13-field support. Odd gauge singlets are candidates, not an assigned neutrino basis. No seesaw inverse, amplitudes or neutrino eigenvalues are inferred.')
    # Exact one-variable real-cone relaxation: no truncation in VEV order.
    basis_columns=fi+['n_9','n_37','n_35'];selected=[0,2,3,4,5,6,7,8]
    charge_inverse=S.Matrix.hstack(*(S.Matrix(q[n]) for n in basis_columns)).extract(selected,list(range(8))).inv()
    def coordinates(ns):
        return charge_inverse*(-sum((S.Matrix(q[n]) for n in ns),S.zeros(9,1))).extract(selected,[0])
    def one_variable_cone(beta,nu):
        lo=S.Rational(0);hi=None
        for b,n in zip(beta,nu):
            if n>0:hi=min(hi,b/n) if hi is not None else b/n
            elif n<0:lo=max(lo,b/n)
            elif b<0:return False
        return hi is None or bool(hi>=lo)
    additions=[]
    for n,f in fields.items():
        if n in support or f['dim'].split(',')[:2]!=['1','1'] or q[n][1]!=0 or prior['all176_field_parities'][n]!=0:continue
        nu=[-x for x in coordinates([n])[:5]]
        mask=[[int(one_variable_cone(coordinates([a,b,hu])[:5],nu)) for b in basis['u_c']] for a in basis['Q']]
        rank=matching_rank(mask)
        # Original support has no SU4 charge. A single commuting fundamental
        # has no positive-degree SL4 invariant (epsilon of four copies is0).
        hidden4=abs(int(f['dim'].split(',')[2]))==4
        additions.append(dict(field=n,dimension=f['dim'],FI_coordinate_direction=list(map(str,nu)),
            relaxed_real_cone_mask=mask,relaxed_structural_rank_upper_bound=rank,
            holomorphic_hidden_invariant_rank_upper_bound=1 if hidden4 else rank))
    assert len(additions)==43
    assert [r['field'] for r in additions if r['relaxed_structural_rank_upper_bound']>1]==['n_69','n_74']
    assert all(r['holomorphic_hidden_invariant_rank_upper_bound']==1 for r in additions)
    outsiders=[]
    for n,f in fields.items():
        if n in support or f['dim'] not in ('1,1,1,1','1,1,1,2') or q[n][1]!=0:continue
        hits=finite([n])
        if hits:outsiders.extend(dict(outside=n,fields=list(x)) for x in hits)
    down=results['d'];hall_names=['d_1','d_3','d_6','d_7'];hall=[down['rows'].index(n) for n in hall_names]
    neighbors=[n for j,n in enumerate(down['columns']) if any(down['all_order_nonnegative_core_mask'][i][j] for i in hall)]
    assert neighbors==['bd_1','bd_7'] and down['all_order_mass_rank_upper_bound']==5
    assert yukawas['u']['all_order_rank_upper_bound']==1
    assert results['x']['all_order_mass_rank_upper_bound']==0
    assert results['v']['all_order_mass_rank_upper_bound']==8
    return dict(status='PASS',mass_lattice=lat,mass_sectors=results,Yukawa_sectors=yukawas,neutrino_sector=neutrino,
        single_even_condensate_extension_audit=additions,
        single_addition_boundary='All43 even SM-neutral fields outside the13-field support were tested with an exact unbounded real-cone relaxation. Only n69,n74 (hidden SU4 fundamentals) relax the up-mask beyond rank1; neither has a positive-degree holomorphic SU4 invariant as the sole new charged flavor. Thus no single elementary addition repairs the declared Hu up-Yukawa rank. Coordinated hidden flavors, changed Higgs basis and nonperturbative mechanisms remain open.',
        additional_fractional_exotics={'fractional_colored_2x2_rank_upper_bound':0,'half_charged_14x14_rank_upper_bound':8,'unlifted_fractional_colored_pairs':2,'minimum_unlifted_half_charged_pairs':6},
        exact_color_triplet_Hall_obstruction={'rows':hall_names,'all_order_possible_neighbors':neighbors,'row_count':4,'neighbor_count':2,'maximum_7x10_mass_rank':5,'unavoidable_unpaired_triplets':2},
        physical_branch_boundary='On precisely11796 support, perturbative holomorphic color masses have rank<=5 of7 at every order: at least two colored pairs remain. The declared even Hu=bl1 up-Yukawa has rank<=1 at every order. More VEV fields, nonperturbative/Kahler mechanisms or different Higgs identification are not covered.',
        outsider_necessary_candidates_through_degree5=outsiders,
        max_VEV_insertions=4,requests=[list(x) for x in sorted(requests)],
        amplitude_boundary='Structural matching uses distinct candidate entries and generic independent coefficients. These necessary-rule matrices are not physical mass ranks. Actual space-group check, invariant contraction, shared coefficient relations and moduli-dependent CFT amplitudes are separate.')


def matching_rank(matrix):
    match={}
    def visit(row,seen):
        for col,x in enumerate(matrix[row]):
            if x and col not in seen:
                seen.add(col)
                if col not in match or visit(match[col],seen):match[col]=row;return True
        return False
    return sum(visit(i,set()) for i in range(len(matrix)))


def spectral_residual():
    import w33_pass11769_quantized_current_vacuum as old
    geo=old.geometry();u=np.rint(40*geo['u']).astype(np.int64);v=np.rint(40*geo['v']).astype(np.int64)
    g=np.rint(10*geo['g']).astype(np.int64)
    matrices=[v@v.T,v@g@v.T,v@g@g@v.T,u@u.T,u@g@u.T,u@g@g@u.T,v@u.T,u@v.T]
    signatures=Counter(tuple(int(a[i,j]) for a in matrices) for i in range(160) for j in range(160))
    m,t,f,e=parameters();root=I(10).sqrt();a=I(F(1,20)).sqrt()
    def poly(offset):
        real={};imag={}
        def add(p,i,j,c):
            ex=[0]*4;ex[offset]=i;ex[offset+1]=j;ex=tuple(ex);p[ex]=p.get(ex,I(0))+c
        for k,c in [(2,I(1)),(1,2*a),(0,a*a)]:
            for i,j,d in [(2,0,f*f),(1,0,2*f*a),(0,0,a*a+2*m/t),(0,2,-I(1))]:add(real,k+i,j,c*d)
            for i,j,d in [(1,1,2*f),(0,1,2*a)]:add(imag,k+i,j,c*d)
        return real,imag
    p0,p1=poly(0),poly(2);h2=I(0)
    for sig,count in signatures.items():
        vv,vgv,vg2v,uu,ugu,ug2u,vu,uv=sig
        xx=t*(I(F(vv,1600))+I(F(vgv,16000))/root+(4/root-1)*I(F(vg2v,960000)))/2
        zz=(I(F(uu,1600))-I(F(ugu,16000))/root+(4/root-1)*I(F(ug2u,960000)))/(2*t)
        cov=[[t*m,I(0),xx,I(F(vu,3200))],[I(0),m/t,I(F(uv,3200)),zz],
             [xx,I(F(uv,3200)),t*m,I(0)],[I(F(vu,3200)),zz,I(0),m/t]]
        @lru_cache(None)
        def wick(ex):
            if sum(ex)%2:return I(0)
            if not any(ex):return I(1)
            i=next(i for i,x in enumerate(ex) if x);r=list(ex);r[i]-=1;ans=I(0)
            for j,num in enumerate(r):
                if num:
                    z=r.copy();z[j]-=1;ans+=num*cov[i][j]*wick(tuple(z))
            return ans
        pair=lambda p,q:sum((c*d*wick(tuple(a+b for a,b in zip(x,y))) for x,c in p.items() for y,d in q.items()),I(0))
        h2+=count*(pair(p0[0],p1[0])+pair(p0[1],p1[1]))
    variance=h2-e*e;assert variance.lo>0
    sigma=variance.sqrt()
    return dict(status='PASS',edge_pair_covariance_classes=len(signatures),ordered_edge_pairs=160**2,
        trial_energy_interval=e.data(),full_H_squared_norm_interval=h2.data(),full_residual_variance_interval=variance.data(),
        spectral_distance_upper_bound=str(sigma.hi),spectrum_intersects_interval=[str((e-sigma).lo),str((e+sigma).hi)],
        exact_action='J_e^2 psi/psi=(X+a)^2[(fX+a+iZ)^2+2m/t]. All ordered160^2 edge pairs are integrated by rational outward-rounded Gaussian Wick moments through degree8.',
        scope='A full infinite-Hilbert-space residual for the named Gaussian, not a truncated matrix residual. The spectral theorem gives distance(E,spec H)<=sigma. Without an excited-state lower bound this does not certify E0, uniqueness, a numeric lower gap or physical particle masses.',
        prior='11769 owns actual H and optimized Gaussian;11786 interval arithmetic;11778 compact spectrum; parallel round3 excludes scalar linear-current SOS.')


def native_matter_stress():
    original=json.loads((ROOT/'data/w33_pass11389_parabolic_spatial_cover.json').read_text())['line']
    edges=original['edges'];E=S.Matrix(original['fcc_harmonic_displacements']).applyfunc(S.Rational)
    voltage=S.Matrix(original['integer_voltage']).applyfunc(S.Rational)
    star=[[] for _ in range(80)]
    for i,(a,b) in enumerate(edges):star[a].append((b,i,1));star[b].append((a,i,-1))
    two=[];A=S.zeros(80)
    for a,b in edges:A[a,b]=A[b,a]=1
    for center,st in enumerate(star):
        for (b,i,si),(c,j,sj) in combinations(st,2):
            two.append((b,c,-si*E[i,:]+sj*E[j,:],-si*voltage[i,:]+sj*voltage[j,:]))
    assert len(two)==480 and len({tuple(sorted([a,b])) for a,b,d,z in two})==480
    L=4*S.eye(80)-A;L2=S.zeros(80)
    for a,b,d,z in two:
        L2[a,a]+=1;L2[b,b]+=1;L2[a,b]-=1;L2[b,a]-=1
    assert L2==8*L-L*L
    def row(v):return [v[0]**2,v[1]**2,v[2]**2,v[0]*v[1],v[0]*v[2],v[1]*v[2]]
    response=S.Matrix([row(E[i,:]) for i in range(160)]+[row(d) for a,b,d,z in two])/80
    assert response[:160,:].rank()==4 and response.rank()==6
    witnesses=list(response.T.rref()[1]);minor=response[witnesses,:];assert minor.det()!=0
    # Six-channel right inverse names the actual conductance map for every
    # specified tensor deltaK; unused channels are left unchanged.
    right=S.zeros(640,6)
    for i,index in enumerate(witnesses):right[index,:]=minor.T.inv()[i,:]
    assert response.T*right==S.eye(6)
    tensor=sum((d.T*d for a,b,d,z in two),S.zeros(3))/80
    assert tensor==8*S.eye(3)*S.Rational(27,3200)
    kappa=S.Rational(1,8);K=S.eye(3)*S.Rational(27,3200)*(1+8*kappa)
    # A microscopic fiber is visible to generic matter even though it is
    # invisible to affine acoustic fields. Find a short exact relation.
    null=response.T.nullspace()[0];assert response.T*null==S.zeros(6,1)
    channels=[(a,b,E[i,:]) for i,(a,b) in enumerate(edges)]+[(a,b,d) for a,b,d,z in two]
    probe=None
    for vertex in range(80):
        value=sum(null[i]*int((a==vertex)!=(b==vertex)) for i,(a,b,d) in enumerate(channels))
        if value:probe=dict(vertex=vertex,fiber_energy_pairing=str(value));break
    assert probe is not None
    rho,k1,k2,k3=S.symbols('rho k1 k2 k3',positive=True)
    kin=S.diag(k1,k2,k3);det=kin.det();N=(det/rho)**S.Rational(1,4)
    metric=(rho*det)**S.Rational(1,2)*kin.inv();volume=S.sqrt(metric.det())
    assert S.simplify(volume/N-rho)==0 and (N*volume*metric.inv()-kin).applyfunc(S.simplify)==S.zeros(3)
    return dict(status='PASS',native_one_hop_metric_rank=4,prior_two_hop_rank_six_owner='Pass11518 in11516-11520',
        all_native_two_hop_channels=480,nonzero_displacement_two_hop_channels=sum(d!=S.zeros(1,3) for a,b,d,z in two),
        uniform_two_hop_operator='L2(k)=8L(k)-L(k)^2 for every Bloch k; native graph has no4cycles, so every distinct same-side neighbor has one two-edge path.',
        harmonic_two_hop_tensor=[[str(x) for x in row] for row in tensor.tolist()],
        uniform_augmented_band='lambda_completed=lambda+kappa*(8lambda-lambda^2). Uniform harmonic realization is unchanged; acoustic K=(1+8kappa)*(27/3200)I.',
        kappa=str(kappa),acoustic_speed_squared=str(K[0,0]),complete_linear_metric_rank=6,
        metric_tensor_coordinate_order=['Kxx','Kyy','Kzz','Kxy','Kxz','Kyz'],
        right_inverse_channels=witnesses,right_inverse_values=[[str(x) for x in right[index,:]] for index in witnesses],
        positive_conductance_scope='At positive uniform kappa, sufficiently small tensor perturbations preserve all positive channel weights; the explicit right inverse realizes every symmetric deltaK.',
        exact_microscopic_metric_fiber_probe=probe,
        acoustic_stress='For affine phi=p.x, deltaE=40*p^T*deltaK*p; a metric fiber gives zero. For general cell fields it need not, as the stored vertex probe shows. Extra microscopic couplings cannot silently be declared metric gauge redundancy.',
        conserved_graph_energy='H=1/2 sum_v rho_v*dotphi_v^2+1/2 sum_channels w_ab*(phi_a-phi_b)^2. Cell energy uses half each spring; flux I_ab=(w_ab/2)*(phi_a-phi_b)*(dotphi_a+dotphi_b), and dotE_a=-sum_b I_ab exactly by rho_a*ddotphi_a=-sum_b w_ab*(phi_a-phi_b).',
        continuum_metric_map='For S=1/2 integral[rho*dotphi²-Kij*d_i phi*d_j phi], N=(detK/rho)^(1/4), h=(rho*detK)^(1/2)*K^-1. Then rho=sqrt(h)/N, K=N*sqrt(h)*h^-1: an explicit minimally coupled scalar action, with shift set zero.',
        gravity_boundary='This builds an actual matter/stress map on the native cover and exposes its metric fibers. Einstein-Hilbert dynamics, gravitational constraints, physical scales, selected parabolic and cosmological constant are not derived. Two-hop rank repair itself is prior11518, not new.')


def certificate():
    raw,prior,fields,support,q=load()
    result=dict(schema='w33.pass11797_11801.v1',status='PASS',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        inputs_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n') if p.suffix=='.json' else p.read_bytes()).hexdigest() for p in [RAW,ROOT/'data/w33_pass11796_parity_complete_abelian_higgs.json',ROOT/'data/w33_pass11389_parabolic_spatial_cover.json',ROOT/'data/w33_pass11797_corrected_named_coupling_checks.json',ROOT/'data/w33_pass11793_order_four_matter_action.json']})
    checks=json.loads((ROOT/'data/w33_pass11797_corrected_named_coupling_checks.json').read_text())
    for name,call in [('pass11797',lambda:vacuum_ring(fields,support,q)),('pass11798',lambda:global_parity(raw,prior,fields)),('pass11799',lambda:couplings(fields,support,q,prior)),('pass11800',spectral_residual),('pass11801',native_matter_stress)]:
        result[name]=call();print(name,'PASS',flush=True)
    canonical=lambda rows:sorted(tuple(sorted(r['fields'])) for r in rows)
    assert canonical(checks['degree8']['rows'])==canonical(result['pass11797']['degree8_necessary_candidates'])
    assert canonical(checks['finite_mass_and_outsider']['rows'])==sorted(tuple(x) for x in result['pass11799']['requests'])
    assert all(r['allowed_count']==1 for group in ('degree8','finite_mass_and_outsider') for r in checks[group]['rows'])
    result['pass11797']['actual_named_gauge_space_group_corrected_R_passes']=19
    result['pass11799']['actual_named_finite_gauge_space_group_corrected_R_passes']=6
    return result


if __name__=='__main__':
    result=certificate();OUT.write_text(json.dumps(result,indent=2)+'\n')
