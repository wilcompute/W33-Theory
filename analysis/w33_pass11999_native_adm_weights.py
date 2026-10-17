"""Actual edge-weight ADM kinetic map and constraints, with GR input explicit.

11995 owns the metric chart. Here its rational differential supplies the
canonical momenta, primary null directions and transverse two-mode reduction.
The continuum ADM curvature law is supplied, not derived from graph combinatorics.
"""
import json,itertools
from pathlib import Path
import sympy as s
import numpy as np
from w33_pass12000_native_unitary_clock import native_paths
ROOT=Path(__file__).resolve().parents[1]
PAIRS=list(itertools.combinations_with_replacement(range(3),2))


def payload():
    prior=json.loads((ROOT/'data/w33_pass11995_native_metric_gr_lift.json').read_text());old=json.loads((ROOT/'data/w33_pass11991_native_four_period_cover.json').read_text())
    G=s.Matrix(old['exact_acoustic_metric']);C=s.Matrix(old['harmonic_voltages_Q']);u=s.Matrix([3,0,2,1]);T=native_paths()[4]
    r=(u.T*G*u)[0];K=G-2*G*u*u.T*G/r;K=T.inv()*K*T.T.inv();g=K.inv();h=g[1:,1:]
    assert all(h[:i,:i].det()>0 for i in range(1,4)) and K[0,0]<0
    n=-1/K[0,0];shift=[-K[0,i]/K[0,0] for i in range(1,4)]
    derivative=[]
    for e in range(135):
        dG=C[e,:].T*C[e,:]/27
        dK=dG-2*(dG*u*u.T*G+G*u*u.T*dG)/r+2*G*u*u.T*G*(u.T*dG*u)[0]/r**2
        dK=T.inv()*dK*T.T.inv();dg=-g*dK*g
        dn=dK[0,0]/K[0,0]**2
        db=[-dK[0,i]/K[0,0]+K[0,i]*dK[0,0]/K[0,0]**2 for i in range(1,4)]
        derivative.append(s.Matrix([dn,*db,*[dg[i+1,j+1] for i,j in PAIRS]]))
    Jall=s.Matrix.hstack(*derivative);selected=prior['selected_edge_indices'];J=Jall[:,selected];assert J.det()!=0 and Jall.rank()==10
    E=[]
    for i,j in PAIRS:
        m=s.zeros(3);m[i,j]=m[j,i]=1;E.append(m)
    hi=h.inv();W=s.Matrix([[s.trace(hi*a*hi*b)-s.trace(hi*a)*s.trace(hi*b) for b in E] for a in E])
    Q=s.zeros(10);Q[4:,4:]=W;pullback=J.T*Q*J;assert pullback.rank()==6
    ev=np.linalg.eigvalsh(np.array(pullback,float));assert sum(ev>1e-9)==5 and sum(ev< -1e-9)==1
    null=J.inv()[:,:4];assert pullback*null==s.zeros(10,4)
    # Exact canonical one-form in a generic rational variation.
    dq=s.Matrix(range(1,11));p=s.Matrix(range(2,12));dw=J.inv()*dq;pw=J.T*p
    assert (pw.T*dw)[0]==(p.T*dq)[0]
    # Linearized continuum constraints at a nonzero mode: four firstclass
    # constraints in the12D spatial metric phase space, not a graph bracket.
    k=s.Matrix([2,-1,3]);qq=s.symbols('q0:6');pp=s.symbols('p0:6');qmat=sum((v*a for v,a in zip(qq,E)),s.zeros(3));pmat=s.zeros(3)
    for p0,(i,j) in zip(pp,PAIRS):pmat[i,j]=pmat[j,i]=p0 if i==j else p0/2
    H=(k.T*qmat*k)[0]-(k.T*k)[0]*s.trace(qmat);M=-2*pmat*k
    constraints=s.Matrix([H,*M]);D=constraints.jacobian([*qq,*pp]);omega=s.zeros(12);omega[:6,6:]=s.eye(6);omega[6:,:6]=-s.eye(6)
    assert D.rank()==4 and D*omega*D.T==s.zeros(4)
    tt=s.Matrix([s.trace(qmat),*(qmat*k)]).jacobian(qq).nullspace();assert len(tt)==2
    TT=s.Matrix.hstack(*tt);Wflat=s.Matrix([[s.trace(a*b)-s.trace(a)*s.trace(b) for b in E] for a in E]);energy=TT.T*Wflat*TT
    assert energy[0,0]>0 and energy.det()>0
    return dict(status='PASS',exact_ADM_lapse_squared=str(n),exact_ADM_shift=list(map(str,shift)),exact_spatial_metric_Q=[[str(x) for x in row] for row in h.tolist()],
        exact_selected_edge_ADM_jacobian=[[str(x) for x in row] for row in J.tolist()],exact_selected_ADM_jacobian_determinant=str(J.det()),
        spatial_DeWitt_form_Q=[[str(x) for x in row] for row in W.tolist()],
        edge_velocity_Hessian_rank=6,edge_velocity_Hessian_inertia={'positive':5,'negative_conformal':1,'lapse_shift_zero':4},
        exact_primary_null_directions_Q=[[str(x) for x in row] for row in null.tolist()],
        canonical_map='dq=Jdw; p_w=J^T p_q and p_q=J^-T p_w. Four primary constraints are columns(J^-1)_(lapse²,shift)^T p_w=0.',
        explicit_action='S[w]=integral N sqrt(h) [Kij K^ij-K²+R3(h)-2Lambda] dt d3x, Kij=(dot h_ij-Lie_beta h_ij)/(2N), N=sqrt(n(w)), beta(w),h(w) givenbytheactualnativeinversemetricreflection. SuppliedcontinuumR3/spatialderivatives andEinsteincoupling, no nativeactionselection.',
        linearized_constraint_rank=4,linearized_constraint_Poisson_matrix_zero=True,transverse_traceless_dimension=2,exact_TT_kinetic_form=energy.tolist(),
        full135_weight_count='If actiondepends onthetenmetriccoordinatesonly,125redundantcoordinateshaveprimarymomenta0. ADMhas4primary+4secondaryfirstclassconstraints. Conditionalcontinuumphasecount270-2*(125+8)=4, i.e.twoDOF. Generic135weightkineticterms invalidate this.',
        boundary='A concrete canonical implementation of supplied nonlinearGR on nativeweightfields. Its fullcontinuumconstraintalgebra is inherited by invertiblefieldredefinition, not newlyderived. The finitepointwise11976bracketfailure is unchanged; noG/Lambda or microscopiccurvatureterm is selected.',
        prior=['11995 actualnative10metricchart andclockalignment','11961 continuumADM necessaryconditions','11976 finitepointwise matterbracket obstruction','11992 full nonlinearGowdy benchmark'],
        primary=['https://arxiv.org/abs/gr-qc/0405109'])

if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11999_native_adm_weights.json').write_text(json.dumps(d,indent=2,default=int)+'\n');print(d['status'],d['edge_velocity_Hessian_inertia'])
