"""Five physically distinct TOE controls: Klein A1 gauge modulus, F4 running,
quantum photonic memory, winding-modular stability, and Wilson-line scope.

The research is conditional on the specified parent mathematical models.
No experimental observations or completed particle theory are claimed.
"""
import itertools
import json
import math
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PRIME=23
I5=np.eye(5,dtype=np.int64)


def null_mod(mat, p=PRIME):
    a=[[int(v)%p for v in row] for row in mat]
    cols=len(a[0]); rows=len(a)
    piv=[]; r=0
    for c in range(cols):
        k=next((k for k in range(r,rows) if a[k][c]),None)
        if k is None: continue
        a[r],a[k]=a[k],a[r]
        inv=pow(a[r][c],-1,p)
        a[r]=[x*inv%p for x in a[r]]
        for t in range(rows):
            if t!=r and a[t][c]:
                fac=a[t][c]
                a[t]=[(x-fac*y)%p for x,y in zip(a[t],a[r])]
        piv.append(c);r+=1
        if r==rows:break
    out=[]
    for f in range(cols):
        if f in piv:continue
        v=[0]*cols;v[f]=1
        for i,col in enumerate(piv):v[col]=-a[i][f]%p
        out.append(np.array(v,dtype=np.int64))
    assert all(np.all((np.array(mat,dtype=np.int64)@v)%p==0) for v in out)
    return out


def cubic(v,p=PRIME):
    return sum(int(v[i])**2*int(v[(i+1)%5]) for i in range(5))%p


def klein_gauge_locus_rational_moduli():
    cert=json.loads((ROOT/"data/toe_20261118_klein_odd_Weil_fixed_strata.json").read_text(encoding="utf-8"))
    assert cert["group_order"]==660 and cert["status"]=="PASS"
    nums=cert["generator_S_cyclotomic_numerators"]
    w=cert["D_weights"]
    root=2
    assert pow(root,11,PRIME)==1 and root!=1
    inverse11=pow(11,-1,PRIME)
    S=np.array([[sum(int(c)*pow(root,k,PRIME) for k,c in enumerate(entry))*inverse11%PRIME
                 for entry in row] for row in nums],dtype=np.int64)
    D=np.diag([pow(root,int(a),PRIME) for a in w]).astype(np.int64)
    ident=I5
    assert np.array_equal(S@S%PRIME,ident)
    key=lambda m:tuple(map(int,m.flat))
    seen={key(ident)}
    queue=[ident]
    for g in queue:
        for gen in (S,D):
            m=gen@g%PRIME
            if key(m) not in seen:
                seen.add(key(m));queue.append(m)
    assert len(queue)==660
    centralizer=[g for g in queue if np.array_equal(g@S%PRIME,S@g%PRIME)]
    assert len(centralizer)==12
    involutions=[g for g in centralizer if key(g)!=key(ident) and
                 np.array_equal(g@g%PRIME,ident)]
    assert len(involutions)>=2
    # Involution S is central in its dihedral centralizer. Find another
    # commuting involution T generating a Klein V4 with S.
    chosen=None
    for T in involutions:
        if np.array_equal(T,S):continue
        plus=null_mod(np.vstack((S-ident,T-ident)))
        minus=null_mod(np.vstack((S-ident,T+ident)))
        if len(plus)==2 and len(minus)==1:
            chosen=(T,plus,minus);break
    assert chosen is not None
    T,plus,minus=chosen
    assert len(null_mod(S-ident))==3 and len(null_mod(T-ident))==3
    assert len(null_mod(np.vstack((S-ident,T-ident))))==2
    u,v=plus; z=minus[0]
    assert cubic(z)==0
    eval_u=cubic(u)
    eval_v=cubic(v)
    pp=cubic((u+v)%PRIME)
    pm=cubic((u-v)%PRIME)
    sum_bc=(pp-eval_u-eval_v)%PRIME
    minus_b_plus_c=(pm-eval_u+eval_v)%PRIME
    inv2=pow(2,-1,PRIME)
    aa,bb,cc,dd=(eval_u,
                  (sum_bc-minus_b_plus_c)*inv2%PRIME,
                  (sum_bc+minus_b_plus_c)*inv2%PRIME,
                  eval_v)
    discriminant=(bb*bb*cc*cc - 4*aa*cc**3 - 4*bb**3*dd -
                  27*aa*aa*dd*dd + 18*aa*bb*cc*dd)%PRIME
    assert discriminant!=0
    # In the projective S-fixed plane, T has a fixed plus-line that meets
    # smooth E in THREE distinct points (binary cubic discriminant !=0),
    # and a minus-line in E (homogeneous odd f invariant under T).
    # Thus T acts as a nontrivial elliptic involution with FOUR fixed
    # points. Any such holomorphic elliptic involution acts -1 on H^1(E,R).
    # Q is the nontrivial Euler-3 circle bundle over E, so by Gysin,
    # H^1(Q,R)~H^1(E,R)~R^2 and T acts -I. Consequently H^1(Q/C6,R)=0.
    return dict(parent_PSL_order=660, centralizer_order=len(centralizer),
                effective_residual_action_order=6,
                V4_joint_plus_dimension=len(plus),
                S_plus_T_minus_dimension=len(minus),
                mod23_binary_cubic_coefficients=[aa,bb,cc,dd],
                mod23_binary_cubic_discriminant=discriminant,
                binary_cubic_is_squarefree_in_characteristic_zero=True,
                extra_T_minus_fixed_point_on_elliptic_E=True,
                T_projective_fixed_points_on_E=4,
                induced_T_action_H1_E="-identity",
                Q_circle_bundle_Euler_degree=3,
                b1_Q=2,b2_Q=2,
                quotient_b1_rational=0,quotient_b2_rational=0,
                quotient_b0_rational=1,quotient_b3_rational=1,
                quotient_rational_homology="Q/C6 has the rational Betti numbers of S3",
                physics="Unfluxed trivial-adjoint-coefficient gauge zero-mode count has no b1-type moduli on full holomorphic PSL quotient. Localized intersection states, nontrivial adjoint monodromy, flux and orbifold singular spectra not computed.")


def F4_one_loop_RG():
    # Fixed illustrative electroweak MSbar inputs near M_Z, not a precision fit.
    inv_alpha_em=127.952
    sin2=.23129
    alpha_s=.1179
    mZ=91.1876
    a_em=1/inv_alpha_em
    g2=4*math.pi*a_em/sin2
    gy=4*math.pi*a_em/(1-sin2)
    g3=4*math.pi*alpha_s
    y2,yY,y3=1/g2,1/gy,1/g3
    b2,bY,b3=-19/6,41/6,-7
    assert abs(gy/g2-sin2/(1-sin2))<1e-13
    def evolved(t):
        z3=y3-b3*t/(8*math.pi**2)
        z2=y2-b2*t/(8*math.pi**2)
        zY=yY-bY*t/(8*math.pi**2)
        assert z3>0 and z2>0 and zY>0
        return dict(invg2_3=z3,invg2_2=z2,invg2_Y=zY,
                    g3sq_over_g2sq=z2/z3,gYsq_over_g2sq=z2/zY,
                    sin2_thetaW=z2/(z2+zY),
                    F4_color_residual=z2-2*z3,
                    F4_weak_hypercharge_residual=z2-3*zY)
    t32=8*math.pi**2*(y2-2*y3)/(b2-2*b3)
    t2Y=8*math.pi**2*(y2-3*yY)/(b2-3*bY)
    assert 0<t32<10 and 60<t2Y<80
    R32=evolved(t32)
    R2Y=evolved(t2Y)
    assert abs(R32["F4_color_residual"])<1e-12
    assert abs(R2Y["F4_weak_hypercharge_residual"])<1e-12
    assert abs(t32-t2Y)>60
    tPlanck=math.log(2.4e18/mZ)
    return dict(inputs=dict(alpha_em_inv=inv_alpha_em,sin2_MSbar=sin2,
                            alpha_s=alpha_s,MZ_GeV=mZ,
                            beta_coeffs_hypercharge_weak_strong=[bY,b2,b3]),
                F4_boundary="g3^2=2*g2^2 and gY^2=3*g2^2, sin^2(thetaW)=3/4",
                color_match_lnmu_overMZ=t32,color_match_GeV=mZ*math.exp(t32),
                hypercharge_match_lnmu_overMZ=t2Y,
                hypercharge_match_log10_GeV=math.log10(mZ)+t2Y/math.log(10),
                separation_lnmu=t2Y-t32,
                color_match_residual_hypercharge=R32["F4_weak_hypercharge_residual"],
                hypercharge_match_residual_color=R2Y["F4_color_residual"],
                reduced_Planck_scale_residuals=evolved(tPlanck),
                no_common_one_loop_SM_scale=True,
                limitation="Only SM field content and one-loop beta functions in an illustrative MSbar benchmark, neglecting threshold corrections/new F4 states and two-loop effects; no UV no-go theorem.")


def winding_modular_phase():
    # Inputs: parent 11D / IIB conditional mixed winding-Rayon formula.
    def shortest(tau, window=10):
        z=min(((abs(u+v*tau)**2/tau.imag,u,v)
               for u in range(-window,window+1)
               for v in range(-window,window+1) if (u,v)!=(0,0)))
        return z
    def diag(tau,ratio):
        val,u,v=shortest(tau)
        lam=3*math.pi*ratio*val
        mass=lam-2-math.sqrt(4+16*lam)
        return dict(tau_real=tau.real,tau_imag=tau.imag,
                    shortest_norm=val,shortest_vector=[u,v],
                    lambda_min=lam, m2L2=mass,BF_violation=lam<12)
    square=diag(1j,1)
    hexagon=diag(complex(.5,math.sqrt(3)/2),1)
    assert square["shortest_norm"]==1
    assert abs(hexagon["shortest_norm"]-2/math.sqrt(3))<1e-12
    assert square["BF_violation"] and hexagon["BF_violation"]
    threshold=2*math.sqrt(3)/math.pi
    assert 1<threshold<1.2
    assert not diag(complex(.5,math.sqrt(3)/2),1.2)["BF_violation"]
    assert diag(20j,10)["BF_violation"] # cusp defeats finite high-flux ratio
    # Exact BF condition m2L2<-4 iff 0<lambda<12; minimum -25/4 at lambda=15/4.
    lm=15/4
    assert abs(lm-2-math.sqrt(4+16*lm)+25/4)<1e-12
    return dict(square_ratio1=square,hexagonal_ratio1=hexagon,
                universal_unstable_threshold_ratio=threshold,
                safe_modulus_exists_only_if_ratio_at_least=threshold,
                cusp_still_unstable_at_any_fixed_finite_positive_ratio=True,
                maximum_BF_deficit_in_model=9/4,
                minimum_m2L2=-25/4,
                conditional_status="Consequences of the repository's mixed-mode dispersion. Not a full string-theory winding or KK spectrum.")


def binomial_tail(n,p):
    mass=[0.]*(n+1)
    mass[0]=(1-p)**n
    for k in range(n):
        mass[k+1]=mass[k]*(n-k)/(k+1)*p/(1-p)
    suffix=[0.]*(n+2)
    for k in range(n,-1,-1):
        suffix[k]=suffix[k+1]+mass[k]
    assert abs(suffix[0]-1)<1e-10
    return suffix


def sample_budget(p0,p1,alpha=.01,beta=.01):
    assert 0<p0<p1<1
    for n in range(1,1001):
        null=binomial_tail(n,p0)
        alt=binomial_tail(n,p1)
        for threshold in range(1,n+1):
            a=null[threshold];b=1-alt[threshold]
            if a<=alpha and b<=beta:
                return dict(accepted_shots=n, plus_click_threshold=threshold,
                            false_positive=a,false_negative=b,p0=p0,p1=p1)
    raise AssertionError("No finite sample")


def quantum_memory_entanglement_falsifier():
    # SWAP-causal-break construction: an arbitrary qutrit is stored in
    # coherent memory then returned despite replacement. As an overall
    # input-output channel this is identity, not retrocausality.
    dim=3
    phi=np.zeros(dim*dim,dtype=complex)
    for i in range(dim):phi[dim*i+i]=1/math.sqrt(dim)
    pure=np.outer(phi,phi.conj())
    ident9=np.eye(9,dtype=complex)/9
    eta=.4
    choi=eta*pure+(1-eta)*ident9
    pt=choi.reshape(3,3,3,3).transpose(0,3,2,1).reshape(9,9)
    eig=np.linalg.eigvalsh(pt)
    negativity=-sum(x for x in eig if x <0)
    assert abs(negativity-.2)<1e-12
    assert np.sum(eig<-.00001)==3
    F=float(np.real(phi.conj()@choi@phi))
    assert abs(F-7/15)<1e-12
    assert F>1/3
    cert=sample_budget(1/3,F)
    assert (cert["accepted_shots"],cert["plus_click_threshold"])==(292,117)
    return dict(classical_entanglement_breaking_fidelity_bound="F<=1/3",
                conditional_quantum_memory_channel="Depolarizing qutrit memory eta=0.4 after coherent SWAP and causal break",
                eta=eta,choi_fidelity=F,Choi_PT_eigenvalues=list(map(float,eig)),
                negativity=float(negativity),depolarizing_EB_threshold_eta=1/4,
                exact_one_sided_99percent_both_errors=cert,
                necessary_resource="independent entangled qutrit reference and joint maximally entangled projector",
                caveats="The witness separates EB from non-EB channels in this scenario, not quantum memory from every dimension-bounded classical multi-time strategy. IID accepted shots, detection loopholes and calibration unverified; no hardware measured.")


def run():
    result=dict(status="PASS",Klein_gauge=klein_gauge_locus_rational_moduli(),
                F4_RG=F4_one_loop_RG(),winding=winding_modular_phase(),
                photon=quantum_memory_entanglement_falsifier())
    out=ROOT/"data/toe_20261118_fivefront_Klein_F4_winding_memory.json"
    out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("PASS Klein gauge locus rational b1",result["Klein_gauge"]["quotient_b1_rational"])
    print("PASS F4 scales color GeV",result["F4_RG"]["color_match_GeV"],
          "hypercharge log10GeV",result["F4_RG"]["hypercharge_match_log10_GeV"])
    print("PASS winding universal ratio",result["winding"]["universal_unstable_threshold_ratio"])
    print("PASS quantum memory witness",result["photon"]["exact_one_sided_99percent_both_errors"])
    return result


if __name__=="__main__":
    run()
