"""Explicit subgroup/cochain interfaces between the two native A4-invariant twists.

The subgroup/cochain classification is standard, not inferred from spin counts.
Uses the native branch addresses and the prior complete cocycle census.
"""
import itertools,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261103_deck_cocycle_symmetry_selection import exponent,sectors,BRANCH

def beta(a,b):
    x,y=(a>>1)&1,(a>>2)&1;u,v=(b>>1)&1,(b>>2)&1
    return (x*v+2*(x*y*u+y*u*v))%4

def torsion(a,b):return 2*((a>>1)&1)*((b>>2)&1)%4

def build():
    H=[0,3,5,6];assert all((g.bit_count()%2==0)==(g in H)for g in range(8))
    checks=0
    for a,b,c in itertools.product(H,repeat=3):
        target=2*(exponent(120,a,b,c)^exponent(127,a,b,c))
        delta=(beta(b,c)+beta(a,b^c)-beta(a^b,c)-beta(a,b))%4
        assert delta==target
        assert (torsion(b,c)+torsion(a,b^c)-torsion(a^b,c)-torsion(a,b))%4==0
        checks+=1
    assert (torsion(3,5)-torsion(5,3))%4==2
    # Distinct cochain-gauge classes can nevertheless be equivalent module
    # categories under ambient twisted conjugation in the folded group.
    def slant(g,a,b):return 2*(exponent(120,g,a,b)^exponent(120,a,b,g)^exponent(120,a,g,b))
    assert (slant(1,3,5)-slant(1,5,3))%4==2
    conjugation_gauge=None
    for values in itertools.product(range(4),repeat=3):
        lam=dict(zip(H,[0,*values]))
        if all((lam[a]+lam[b]-lam[a^b])%4==(slant(1,a,b)-torsion(a,b))%4 for a,b in itertools.product(H,repeat=2)):
            conjugation_gauge=lam;break
    assert conjugation_gauge is not None
    # Enumerate all actual subgroups, then use complete diagonal restrictions.
    subgroups=[]
    for mask in range(1<<7):
        K=[0]+[i+1 for i in range(7)if mask>>i&1]
        if all(a^b in K for a,b in itertools.product(K,repeat=2)):subgroups.append(K)
    admissible=[K for K in subgroups if all(exponent(7,g,g,g)==0 for g in K)]
    assert len(admissible)==5 and all(set(K)<=set(H)for K in admissible)
    # Native geometric action on Z4^2: translations and four ramified inversions.
    perms={}
    for e,a,b in itertools.product(range(2),repeat=3):
        perms[e,a,b]=[(((-1)**e*x+2*a)%4)*4+(((-1)**e*y+2*b)%4)for x,y in itertools.product(range(4),repeat=2)]
    free=[key for key,p in perms.items()if all(i!=j for i,j in enumerate(p))]
    assert free==[(0,0,1),(0,1,0),(0,1,1)]
    assert [sum(i==j for i,j in enumerate(p))for key,p in perms.items()if key[0]]==[4]*4
    # Map abstract generator bits to deck coordinates so1,2,4 are branch inversions.
    def native_key(g):return (g.bit_count()%2,(g>>1)&1,(g>>2)&1)
    assert all(native_key(g)[0]==0 for g in H) and all(native_key(g)[0]==1 for g in BRANCH)
    old=json.loads((ROOT/'data/w33_20261102_deck_monodromy_network.json').read_text())
    native_perms=old['deck_permutations']
    # The certificate may serialize rows with labels; compare actual vertex permutations.
    if isinstance(native_perms,dict):native_perms=list(native_perms.values())
    if native_perms and isinstance(native_perms[0],dict):
        key=next(k for k,v in native_perms[0].items()if isinstance(v,list)and len(v)==16)
        native_perms=[row[key]for row in native_perms]
    assert {tuple(p)for p in native_perms}=={tuple(p)for p in perms.values()}
    assert sectors(120)['spins']!=sectors(127)['spins']
    return dict(status='PASS_EXPLICIT_NONINVERTIBLE_DECK_TWIST_INTERFACES',
        bulk_twists=[120,127],ratio_code=7,maximal_diagonal_subgroup=H,
        character='chi(g)=g0+g1+g2 mod2; H=ker chi',
        beta_formula='For a=(x xor y,x,y), b=(u xor v,u,v): beta(a,b)=i^(x*v)*(-1)^(x*y*u+y*u*v)',
        beta_i_exponents=[[beta(a,b)for b in H]for a in H],exact_coboundary_checks=checks,
        folded_group='C2^3 x C2^3 with associator omega120 times inverse(omega127)',
        algebra='A=sum_(h in H) e_(h,h); e_h e_k=beta(h,k)e_(h xor k). Exact delta beta equals folded associator on diagonal H.',
        algebra_dimension_in_input_pointed_category=4,Lagrangian_full_center_dimension_in_folded_bulk=64,
        full_diagonal_obstruction='Every g outside H has ratio omega(g,g,g)=-1; a normalized U1 coboundary on its C2 subgroup equals+1 on(g,g,g). Thus no subgroup containing g admits this diagonal interface.',
        admissible_diagonal_subgroups=admissible,diagonal_subgroup_cochain_gauge_data=6,ambient_equivalence_classes_among_diagonal_subgroups=5,
        torsion='On H, multiply beta by zeta(a,b)=(-1)^(x_a*y_b). Its commutator on3,5 is-1, so these are two distinct cochain-gauge choices. They are NOT distinct after ambient folded-group twisted conjugation: conjugation by(1,0) multiplies by a slant2-cocycle in the nontrivial H2 class. The explicit1-cochain below identifies its ratio with zeta.',
        ambient_conjugation_element=[1,0],ambient_conjugation_ratio_gauge_i_exponents=conjugation_gauge,
        no_invertible_interface='Bulk topological spin multisets differ, so these ribbon categories cannot be equivalent; an invertible topological interface is excluded.',
        native_geometry='H is exactly the free translation V4 in the native16-vertex deck action. The four branch-inertia elements1,2,4,7 lie outside H and each fix4 vertices. Actual exported permutations checked as a set.',
        source_recent='https://arxiv.org/html/2610.36029v1',source_classification='https://arxiv.org/abs/1706.03611',
        ownership='Prior deck-monodromy and cocycle-symmetry producers own the covering, meridians and classes120/127. The subgroup/cochain construction is standard; this explicit cochain and native ramification connection are the present audit.',
        boundary='Mathematical DW interface data for extra supplied topological phases. A4-invariant bulk classes and stable H do not by themselves establish an A4-equivariant interface: defect coherence is not constructed. No native Hamiltonian or laboratory phase inferred.')

if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261103_deck_twist_interfaces.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],d['diagonal_subgroup_cochain_gauge_data'],d['ambient_equivalence_classes_among_diagonal_subgroups'],flush=True)
