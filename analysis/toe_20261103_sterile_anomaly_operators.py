"""Global integer classification for three B-L singlets, plus Dirac operators.

The familiar standard/exotic B-L sectors are prior (1008.4572,1105.6064).
The fixed observed SM generation count is input, never a derived prediction.
"""
import fractions,itertools,json,math,pathlib
import sympy as s
ROOT=pathlib.Path(__file__).resolve().parents[1]

def build():
    # All entries are left-handed Weyl fields; charges in ordinary B-L units.
    sm=[('Q',6,s.Rational(1,6),s.Rational(1,3)),('uc',3,-s.Rational(2,3),-s.Rational(1,3)),
        ('dc',3,s.Rational(1,3),-s.Rational(1,3)),('L',2,-s.Rational(1,2),-1),('ec',1,1,1)]
    mixed=[s.expand(sum(n*y*y*b for _,n,y,b in sm)),s.expand(sum(n*y*b*b for _,n,y,b in sm))]
    assert mixed==[0,0]
    assert sum(n*b for _,n,y,b in sm)==sum(n*b**3 for _,n,y,b in sm)==-1
    assert 2*s.Rational(1,3)-s.Rational(1,3)-s.Rational(1,3)==0 and 3*s.Rational(1,3)-1==0
    # Let q=(1+a,1+b,1-a-b), a=g*u,b=g*v with gcd(u,v)=1.
    # Anomaly equations imply2(u^2+uv+v^2)=g*u*v*(u+v).
    # Coprimality forces u|2,v|2,u+v|2; this is a finite global proof.
    sectors={(1,1,1)};proof_rows=[]
    for u,v in itertools.product([-2,-1,1,2],repeat=2):
        if math.gcd(u,v)!=1 or u+v==0 or 2%(u+v):continue
        g=fractions.Fraction(2*(u*u+u*v+v*v),u*v*(u+v))
        if g.denominator!=1 or g<=0:continue
        a,b=int(g)*u,int(g)*v;charges=tuple(sorted((1+a,1+b,1-a-b)))
        assert sum(charges)==sum(x**3 for x in charges)==3
        sectors.add(charges);proof_rows.append(dict(u=u,v=v,g=int(g),charges=charges))
    assert sectors=={(1,1,1),(-5,4,4)}
    # Ordinary integer B-L is a restriction. In the actual quark-normalized
    # lattice Q=3(B-L), sterile charges may also be noninteger in B-L units.
    # Repeat the cutoff-free divisor proof around mean Q=3, so u,v,u+v|6.
    quantized={(3,3,3)};quantized_cases=[]
    divisors=[-6,-3,-2,-1,1,2,3,6]
    for u,v in itertools.product(divisors,repeat=2):
        if math.gcd(u,v)!=1 or u+v==0 or 6%(u+v):continue
        g=fractions.Fraction(6*(u*u+u*v+v*v),u*v*(u+v))
        if g.denominator!=1 or g<=0:continue
        a,b=int(g)*u,int(g)*v;charges=tuple(sorted((3+a,3+b,3-a-b)))
        assert sum(charges)==9 and sum(x**3 for x in charges)==81
        quantized.add(charges);quantized_cases.append(dict(u=u,v=v,g=int(g),charges=charges))
    assert quantized=={(3,3,3),(-15,12,12),(-18,10,17)}
    allowed=[q for q in quantized if all((x-3)%9==0 for x in q)]
    assert set(allowed)=={(3,3,3),(-15,12,12)}
    x=s.symbols('x');two=s.expand(x**3+(3-x)**3-3)
    assert s.discriminant(two,x)<0
    examples=[]
    for charges in sorted(sectors):
        # Integer normalization Q=3(B-L): quarks have minimum charge1;
        # a scalar Phi of B-L=3 has integer charge9.
        op=[]
        for q in charges:
            net=3*(q-1);assert net%9==0
            power=-net//9
            op.append(dict(sterile_left_charge=q,Phi_minus_Phidagger_power=power,operator_dimension=4+abs(power)))
        assert all((3*(a+b))%9!=0 for a,b in itertools.combinations_with_replacement(charges,2))
        examples.append(dict(charges=charges,renormalizable_Dirac_rank_bound=charges.count(1),Dirac_operators=op,
            active_Weinberg_residue_mod9=(-6)%9,sterile_Majorana_residues=sorted({3*(a+b)%9 for a,b in itertools.combinations_with_replacement(charges,2)})))
    # Explicit nonzero full-rank Dirac coefficient benchmark with higher-dimensional columns.
    eps=s.symbols('epsilon');Y=s.Matrix([[1,2,1],[2,1,3],[1,1,1]])*s.diag(eps,eps,eps**2)
    assert s.expand(Y.det())==eps**4
    vev=174e9;heavy=.05;ratio=heavy/vev
    return dict(status='PASS_GLOBAL_THREE_SINGLET_ANOMALY_CLASSIFICATION_AND_DIRAC_OPERATORS',
        standard_model_generations_input=3,sterile_left_charge_solutions=[list(q)for q in sorted(sectors)],
        all_quark_normalized_integer_sectors=[list(q)for q in sorted(quantized)],quark_normalized_cubic_target=81,quark_normalized_linear_target=9,
        quantized_divisor_proof_cases=quantized_cases,
        normalization_extension='Requiring integer charges only in Q=3(B-L), as the quark charge lattice permits, adds(-18,10,17), or B-L=(-6,10/3,17/3). Thus the two ordinary-integer-B-L sectors are NOT the entire charge-quantized classification. The same proof uses u,v,u+v dividing6 rather than2 and exhausts64 divisor pairs.',
        single_Phi_Dirac_mass_selection='With Phi of Q=9 and L of Q=-3, an LHn operator exists with arbitrary Phi/Phi-dagger powers iff Q_n=3 mod9. Requiring all three sterile columns therefore excludes(-18,10,17) and leaves exactly the standard and exotic sectors. This is an extra operator/symmetry-breaking hypothesis, not anomaly cancellation alone.',
        global_gauge_quotient_control='For the alternative global gauge group (SU3_color x U1_BL)/Z3, a representation obeys Q mod3=color triality. Standard quarks satisfy it, while color singlets must have Q divisible3. The sector(-18,10,17) is then disallowed; standard/exotic sectors remain. The direct product and quotient are distinct supplied global-group choices, not interchangeable notation.',
        mixed_Y2_BL_and_Y_BL2_anomalies=mixed,SM_gravity_BL_anomaly_per_generation=-1,SM_cubic_BL_anomaly_per_generation=-1,
        sterile_constraints='sum_i q_i=3 and sum_i q_i^3=3 for left-handed SM-singlet Weyl fields',
        global_classification_proof='Subtract1 from each charge. Apart from the all1 solution, set a=g*u,b=g*v with coprime nonzero u,v and u+v nonzero. The cubic equation reduces to2(u^2+uv+v^2)=g*u*v*(u+v). Since the quadratic factor is coprime to u,v,u+v separately, each divides2. Exhausting the finite divisors yields only permutations of(-5,4,4), with no charge cutoff.',
        divisor_proof_cases=proof_rows,at_least_three_singlets='One singlet has charge3 and fails the cubic equation; two have cubic residual9x^2-27x+24, with negative discriminant. Thus no real two-singlet solution, and no integer one-singlet solution.',
        symmetry_breaking='Declare the direct-product gauge group with integer charge Q=3(B-L). A scalar of Q=9 leaves Z9 before any optional quotient with the color center. No quotient is silently assumed.',
        sectors=examples,Dirac_mass_coefficient_benchmark=[[str(z)for z in row]for row in Y.tolist()],determinant='epsilon^4',
        exotic_hierarchy='Two generic Dirac columns arise at dimension5 and one at dimension6: mnu=vH*[epsilon*y1,epsilon*y2,epsilon^2*y3]. With nonsingular O(1) coefficients this gives two masses of order epsilon*vH and one of order epsilon^2*vH.',
        scale_illustration=dict(vH_eV=vev,heavy_neutrino_mass_input_eV=heavy,epsilon_estimate=ratio,light_neutrino_parametric_scale_eV=heavy**2/vev),
        protection='Both the active Weinberg operator and every sterile Majorana bilinear have nonzero charge mod9. Arbitrary powers of the single Phi/Phi-dagger cannot generate them. The displayed higher-dimensional operators can give full-rank Dirac masses without breaking the residual gauge symmetry.',
        source_exotic='https://arxiv.org/abs/1105.6064',source_earlier='https://arxiv.org/abs/1008.4572',
        ownership='The standard and(-4,-4,+5) right-handed B-L assignments and gauged Dirac protection are known. This uses left-handed conjugate charges and supplies a cutoff-free elementary classification and explicit minimal operator/rank controls. Pass12545 owns the earlier different SM-shaped anomaly enumeration.',
        boundary='A conditional B-L extension, not a derivation of three generations, gauge group, ordering, measured Yukawas, absolute neutrino masses or a complete UV completion. The example hierarchy assumes O(1) Wilson coefficients and a supplied small scalar-to-cutoff ratio.')

if __name__=='__main__':
    d=build();(ROOT/'data/toe_20261103_sterile_anomaly_operators.json').write_text(json.dumps(d,indent=2,default=lambda x:int(x)if isinstance(x,s.Integer)else str(x))+'\n',encoding='utf-8');print(d['status'],d['sterile_left_charge_solutions'],flush=True)
