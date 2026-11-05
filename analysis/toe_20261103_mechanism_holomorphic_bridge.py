"""One extra consistency bridge: make the Dirac messenger chain holomorphic.

The previous nonsupersymmetric Phi-dagger vertices cannot be called a SUSY W.
Introduce a separately dynamical oppositely charged multiplet, audit its cost.
"""
import json,pathlib
import sympy as s
ROOT=pathlib.Path(__file__).resolve().parents[1]

def build():
    p,m,z,v,lam=s.symbols('PhiPlus PhiMinus Z v lam',real=True)
    W=lam*z*(p*m-v*v);xs=[p,m,z];point={p:v,m:v,z:0}
    F=[s.diff(W,x).subs(point)for x in xs];assert F==[0,0,0]
    H=s.hessian(W,xs).subs(point)
    assert H.rank()==2
    # Exact gauge tangent is (PhiPlus,-PhiMinus,0).
    assert H*s.Matrix([v,-v,0])==s.zeros(3,1)
    assert s.factor(H.charpoly().as_expr())!=0
    charges={'L':-1,'H':0,'nA':4,'nC':-5,'N':-1,'Nc':1,'B':-2,'Bc':2,'PhiPlus':3,'PhiMinus':-3,'Z':0}
    terms=[['L','H','Nc'],['N','Nc'],['N','PhiMinus','nA'],['N','PhiPlus','B'],
        ['Bc','PhiMinus','Nc'],['B','Bc'],['Bc','PhiPlus','nC'],['Z','PhiPlus','PhiMinus']]
    assert all(sum(charges[x]for x in term)==0 for term in terms)
    # U1 beta in N=1 SUSY counts sum over CHIRAL supermultiplet charges²,
    # NOT2/3 Weyl+1/3 only the old single scalar content.
    TrSM=s.Rational(13);Trsterile=16+16+25;Trmessenger=3*2+2*4;Trbreaking=9+9
    b=TrSM+Trsterile+Trmessenger+Trbreaking;assert b==102
    # Field-space conventions: phi vevs=v, no hidden1/sqrt2 in v definition.
    g=s.symbols('g',positive=True);D=3*(p*p-m*m)
    assert D.subs(point)==0
    return dict(status='PASS_HOLOMORPHIC_DIRAC_BRIDGE_WITH_D_FLAT_BREAKING',
        superpotential_breaking=str(W),F_at_supplied_real_branch=list(map(str,F)),D_at_branch=0,
        breaking_Hessian=[[str(x)for x in row]for row in H.tolist()],
        uneaten_chiral_supersymmetric_masses='sqrt(2)*abs(lambda*v) for the radial and Z chiral multiplets',
        null_gauge_tangent=['v','-v','0'],vector_multiplet_mass='2*g*3*abs(v)',
        charge_neutral_holomorphic_vertices=terms,left_handed_BL_charges=charges,
        SUSY_BL_beta_breakdown=dict(SM_three_generations=13,steriles=57,messengers=14,breaking_pair=18,total=102),
        mechanism='Replace each Phi^dag vertex of the previous non-SUSY messenger model with an INDEPENDENT chiral PhiMinus of charge-3. Keep PhiPlus of charge+3. Wbreaking=lambda Z(PhiPlus PhiMinus-v²). On PhiPlus=PhiMinus=v real,Z=0 the F and D equations vanish. The gauge tangent is the sole Hessian null; the complexified gauge orbit is eaten by the massive vector. Z9 survives in quark-normalized charge Q=3(B-L).',
        new_anomalies='Opposite-charge breaking multiplets and each messenger pair cancel linear/cubic Abelian anomalies. Added fields are SM singlets. This does not supersymmetrize the earlier native SU4 model automatically.',
        beta='Assuming a supersymmetric SM with both Higgs doublets, three exotic sterile supermultiplets, three N pairs, one B pair and both breaking multiplets above their thresholds, bBL=sum_chiral dim(R)*qBL²=13+57+14+18=102. Higgs BL=0. Non-GUT-normalized bY=11 and mixed bYBL=8. Supersymmetrizing changes the entire beta matrix and thresholds;59 from the non-SUSY model cannot be reused.',
        vacuum_cost='The breaking scale v and coupling lambda are supplied inputs, Wbreaking=0 at its supersymmetric vacuum, and the breaking subsystem alone does not uplift, select the observed CC, protect a rolling scalar after SUSY breaking or determine PMNS data. Coupling it to other sectors can move the branch and transmit soft masses.',
        boundary='A holomorphic and D-flat compatibility module with explicitly enlarged field content, not a demonstrated common UV action or full scalar/fermion spectrum of all combined theories. No comparison of102 to nonsupersymmetric bounds without threshold matching.',
        sources=['https://arxiv.org/abs/hep-ph/9709356','https://arxiv.org/abs/1411.5042'])

if __name__=='__main__':
    d=build();(ROOT/'data/toe_20261103_mechanism_holomorphic_bridge.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],d['SUSY_BL_beta_breakdown']['total'],flush=True)
