"""Native135-edge scalar-loop response with unit-cell temporal Gauss reduction.

Zero external deck momentum only. All109 transverse edge coordinates and26
nonconstant temporal constraints retained; higher gauge loops not included.
"""
from __future__ import annotations
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
from scipy.linalg import eigh,null_space,orth
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261108_coupled_holonomy_response as old


def zero_momentum_geometry(sizes):
    B,V,a,b,h,M=old.prior.geometry()
    path=ROOT/"data/PART_20261023_NATIVE_ZERO_HOLONOMY_FACE_COMPLETION.json"
    selected=json.loads(path.read_text())["independent_face_basis"]
    F=np.zeros((105,135),int)
    for i,row in enumerate(selected):
        for e,s in row["boundary"]:F[i,int(e)]+=int(s)
    assert not (F@B).any() and not (F@V).any()
    C=orth(F.T);Q=null_space(np.ones((1,27)));L=B@Q
    H=h/np.array(sizes)
    T=np.column_stack((H,C,L))
    assert C.shape==(135,105) and Q.shape==(27,26)
    assert np.max(abs(T[:,:109].T@L))<2e-13
    assert np.linalg.matrix_rank(T)==135
    return B,V,a,b,H,C,L,Q,F,T


def schur(A,keep):
    return A[:keep,:keep]-A[:keep,keep:]@np.linalg.solve(A[keep:,keep:],A[keep:,:keep])


@lru_cache(None)
def magnetic_prescriptions():
    from w33_20261027_native_bloch_face_module import geometry,enumerate_faces
    from w33_pass12188_native_period_symplectic_repair import mul
    from itertools import product
    B,V,edges,lookup,nbr=geometry()
    faces,census=enumerate_faces(V,lookup,nbr)
    F=np.zeros((len(faces),135),int)
    for i,face in enumerate(faces):
        for e,s in face:F[i,e]+=s
    assert F.shape==(1287,135) and not (F@B).any() and not (F@V).any()
    Fbasis=zero_momentum_geometry((2,2,2,2))[-2]
    keys={tuple(r) for r in F}|{tuple(-r) for r in F}
    assert all(tuple(r) in keys for r in Fbasis)
    full=F.T@F;selected=Fbasis.T@Fbasis
    group=list(product(range(3),repeat=3));idx={g:i for i,g in enumerate(group)}
    all_errors=[];basis_errors=[]
    for g in group:
        p=[idx[mul(g,x)] for x in group];P=np.zeros((135,135),int)
        for e,(a,b) in enumerate(edges):
            x,y=p[a],p[b];P[lookup[min(x,y),max(x,y)],e]=1 if x<y else -1
        assert np.array_equal(P.T@P,np.eye(135,dtype=int))
        all_errors.append(int(np.max(abs(P.T@full@P-full))))
        basis_errors.append(int(np.max(abs(P.T@selected@P-selected))))
    assert max(all_errors)==0
    return full,dict(all_face_count=1287,selected_basis_count=105,
        zero_voltage_cycle_census=census,all_faces_H27_exact_max_error=max(all_errors),
        selected_basis_H27_exact_max_error=max(basis_errors),
        selected_basis_broken_controller_count=sum(x>0 for x in basis_errors),
        interpretation="Same rank105magnetic rowspace at zero momentum, different positive Hessians. Equal weighting of a selected independent basis need not preserve the graph controller; all1287short zero-voltage faces do. Unit weights and relative face-length couplings remain supplied.")


class FullResponse:
    def __init__(self,sizes=(2,2,2,2),mass=.8):
        self.sizes=tuple(sizes);self.mass=mass
        B,V,a,b,H,C,L,Q,F,T=zero_momentum_geometry(sizes)
        self.B=B;self.Q=Q;self.T=T;self.C=C;self.Fcurl=F
        self.volume=np.prod(sizes[:3]);self.Lcells=sizes[3]
        self.tree_electric=self.Lcells*T.T@T
        all_metric,self.magnetic_symmetry=magnetic_prescriptions()
        self.tree_magnetic_options=dict(basis105=self.Lcells*(F@T).T@(F@T),
            all1287=self.Lcells*T.T@all_metric@T)
        self.use_magnetic("basis105")
        points=old.momenta(sizes)
        contact=np.zeros(135);bubble0=np.zeros((135,135))
        moments=[np.zeros((135,135)) for _ in range(3)]
        ps=[];norms=[];ys=[]
        controls={nu:dict(mixed=np.zeros((135,26)),density=np.zeros((26,26)),
                          density_contact=np.zeros((26,26)),density_bubble=np.zeros((26,26)),
                          Z=np.zeros((135,135)),global_density=0.) for nu in (.2,.7)}
        commutator_residual=0.
        for start in range(0,len(points),8):
            k=points[start:start+8];z=np.exp(1j*k@V.T)
            H0=old.prior.matrices(k)[0];vals,U=np.linalg.eigh(H0)
            w=np.sqrt(np.maximum(vals,0)+mass**2);Uh=U.conj().transpose(0,2,1)
            R=(U/(2*w[:,None,:]))@Uh
            contact+=2*(z*R[:,b,a]).real.sum(0)/self.volume
            # Sparse literal edge derivative, independently of density vertices.
            Y=(-1j*z[:, :,None,None]*U[:,a,:].conj()[:,:,:,None]*U[:,b,:][:,:,None,:]
                +1j*z.conj()[:,:,None,None]*U[:,b,:].conj()[:,:,:,None]*U[:,a,:][:,:,None,:])
            Y=Y.transpose(1,0,2,3).reshape(135,-1)
            N=np.einsum('bvi,vc,bvj->bcij',U.conj(),Q,U,optimize=True)
            N=N.transpose(1,0,2,3).reshape(26,-1)
            wa=w[:,:,None];wb=w[:,None,:]
            p=(wa+wb).ravel();delta=(wa-wb).ravel()
            norm=(2*wa*wb).ravel()
            eigen_delta=(vals[:,:,None]-vals[:,None,:]).ravel()
            commutator_residual=max(commutator_residual,float(np.max(abs(L.T@Y-1j*eigen_delta*N))))
            def gram(weight,X=Y):
                A=X*np.sqrt(weight)[None,:]
                return (A@A.conj().T).real/self.volume
            bubble0+=gram(1/(norm*p))
            for r in range(3):moments[r]+=gram(1/(norm*p**(3+2*r)))
            for nu,c in controls.items():
                c["Z"]+=gram(1/(norm*p*(p*p+nu*nu)))
                c["mixed"]+=((Y*(delta/(norm*(p*p+nu*nu))))@N.conj().T).imag/self.volume
                c["density"]+=gram(delta*delta*p/(norm*(p*p+nu*nu)),N)
                c["density_contact"]+=gram(p/norm,N)
                c["density_bubble"]+=gram(p*(2*norm+nu*nu)/(norm*(p*p+nu*nu)),N)
                NI=(Uh@U).reshape(len(k),27,27).ravel()
                c["global_density"]+=float(np.sum(abs(NI)**2*delta**2*p/(norm*(p*p+nu*nu)))/self.volume)
            ys.append(Y);ps.append(p);norms.append(norm)
        self.Y=np.concatenate(ys,axis=1)
        self.p=np.concatenate(ps);self.norm=np.concatenate(norms)
        self.Kedge=np.diag(contact)-bubble0
        self.Kedge=(self.Kedge+self.Kedge.T)/2
        self.K=T.T@self.Kedge@T
        self.moments=[T.T@z@T for z in moments]
        self.static_gauge_residual=float(np.max(abs(self.Kedge@L)))
        assert self.static_gauge_residual<1e-10 and commutator_residual<1e-10
        self.K[109:,:]=0;self.K[:,109:]=0  # audited exact gauge null directions
        self.commutator_residual=commutator_residual
        self.ward_controls=[]
        for nu,c in controls.items():
            Z=T.T@c["Z"]@T
            mixed=T.T@c["mixed"]
            W=np.zeros((161,161),complex)
            W[:135,:135]=self.K+nu*nu*Z
            W[:135,135:]=1j*nu*mixed
            W[135:,:135]=-1j*nu*mixed.T
            W[135:,135:]=c["density"]
            gauge=np.vstack((np.zeros((109,26)),np.eye(26),1j*nu*np.eye(26)))
            err=float(np.max(abs(W@gauge)))
            assert err<1e-10
            bad=W.copy();bad[135:,135:]-=c["density_contact"]
            missing_contact=float(np.max(abs(bad@gauge)))
            contact_balance=float(np.max(abs(c["density_contact"]-c["density_bubble"]-c["density"])))
            assert missing_contact>1e-4 and contact_balance<1e-12
            self.ward_controls.append(dict(nu=nu,full161by161_Ward_residual=err,
                omitted_temporal_contact_Ward_residual=missing_contact,
                direct_contact_minus_bubble_agreement=contact_balance,
                direct_mixed_vs_spatial_max=float(np.max(abs(mixed-Z[:,109:]))),
                direct_density_vs_spatial_max=float(np.max(abs(c["density"]-Z[109:,109:]))),
                uniform_charge_density_response=c["global_density"]))

    def Zmoment(self,s):
        return sum(s**r*z for r,z in enumerate(self.moments))

    def Zprime_moment(self,s):
        return self.moments[1]+2*s*self.moments[2]

    @lru_cache(maxsize=24)
    def Zexact(self,s,derivative=False):
        weight=1/(self.norm*self.p*(self.p*self.p-s))
        if derivative:weight/=self.p*self.p-s
        A=self.Y*np.sqrt(weight)[None,:]
        Z=(A@A.conj().T).real/self.volume
        return self.T.T@Z@self.T

    def physical(self,s,g=1.,beta=1.,gauss=True,exact=False):
        Z=self.Zexact(float(s)) if exact else self.Zmoment(s)
        E=self.tree_electric/g**2+Z
        reduced=schur(E,109) if gauss else E[:109,:109]
        return (self.K[:109,:109]+beta/g**2*self.tree_magnetic[:109,:109]-s*reduced)

    def low(self,s,g=1.,beta=1.,gauss=True,optical=True,exact=False):
        A=self.physical(s,g,beta,gauss,exact)
        return schur(A,4) if optical else A[:4,:4]

    def slope_low(self,s,g=1.,beta=1.):
        Z=self.Zexact(float(s));Zp=self.Zexact(float(s),True)
        E=self.tree_electric/g**2+Z
        U=np.vstack((np.eye(109),-np.linalg.solve(E[109:,109:],E[109:,:109])))
        Ered=U.T@E@U;Epred=U.T@Zp@U
        P=self.physical(s,g,beta,True,True)
        O=np.vstack((np.eye(4),-np.linalg.solve(P[4:,4:],P[4:,:4])))
        return O.T@(Ered+s*Epred)@O

    def tree_G_harmonic(self,g=1.):
        return self.tree_electric[:4,:4]/g**2

    def profile_invariance(self,s=0.,g=1.):
        _,V,_,_,h,_=old.prior.geometry()
        target=(V-h)/np.array(self.sizes)
        L=self.B@self.Q;mix=np.linalg.lstsq(L,target,rcond=None)[0]
        assert np.max(abs(L@mix-target))<1e-13
        S=np.eye(135);S[109:,:4]=mix
        E=self.tree_electric/g**2+self.Zmoment(s)
        changed=S.T@E@S
        return dict(Gauss_reduced_profile_error=float(np.max(abs(schur(E,109)-schur(changed,109)))),
            clamped_profile_change=float(np.linalg.norm(E[:4,:4]-changed[:4,:4])),
            zero_static_gauge_block_error=float(np.max(abs(S.T@self.K@S-self.K))))

    def use_magnetic(self,name):
        self.magnetic_name=name;self.tree_magnetic=self.tree_magnetic_options[name]

    def modes(self,g=1.,beta=1.):
        Kopt=self.tree_magnetic[4:109,4:109]*beta
        Eopt=self.tree_electric[4:109,4:109]
        gap=float(eigh(Kopt,Eopt,eigvals_only=True).min())
        upper=min(.4*gap,.5*(2*self.mass)**2)
        assert np.linalg.eigvalsh(self.physical(upper,g,beta)[4:,4:]).min()>0
        def roots(gauss,optical):
            assert np.linalg.eigvalsh(self.low(0,g,beta,gauss,optical)).min()>0
            assert np.linalg.eigvalsh(self.low(upper,g,beta,gauss,optical)).max()<0
            return sorted(brentq(lambda s,i=i:np.linalg.eigvalsh(self.low(s,g,beta,gauss,optical))[i],
                                  0,upper,xtol=1e-17,rtol=1e-11) for i in range(4))
        full=roots(True,True);fixed=roots(False,False);gauss4=roots(True,False)
        groups=[]
        for s in full:
            if groups and abs(s-groups[-1]["s"])<max(1e-12,1e-7*s):
                groups[-1]["multiplicity"]+=1;continue
            groups.append(dict(s=float(s),multiplicity=1))
        for row in groups:
            s=row["s"];F=self.low(s,g,beta,True,True,True)
            ev,V=eigh(F);U=V[:,np.argsort(abs(ev))[:row["multiplicity"]]]
            slope=self.slope_low(s,g,beta)
            residue=U@np.linalg.solve(U.T@slope@U,U.T)
            row.update(theta4_residue=float(residue[3,3]),
                unexpanded_low_kernel_residual=float(np.linalg.norm(F@U)),
                reduced_slope_min_eigenvalue=float(np.linalg.eigvalsh(slope).min()),
                moment_expansion_ratio=float(s/(2*self.mass)**2))
            row['mass_squared_residual_bound']=float(row['unexpanded_low_kernel_residual']/np.linalg.eigvalsh(self.tree_electric[:109,:109]/g**2).min())
            q=s/(2*self.mass)**2
            row['unreduced_moment_kernel_remainder_bound']=float(s*q**3/(1-q)*np.linalg.norm(self.moments[0],2))
            assert row["unexpanded_low_kernel_residual"]<2e-9
        G=self.tree_G_harmonic(g);C0=self.moments[0]
        corrected=schur(self.tree_electric/g**2+C0,109)[:4,:4]-G
        return dict(g=g,beta=beta,magnetic_prescription=self.magnetic_name,tree_optical_gap_squared=gap,root_search_upper=upper,
            full_gauss_and_optical_squared_frequencies=full,
            clamped_temporal_and_optical_squared_frequencies=fixed,
            gauss_but_optical_clamped_squared_frequencies=gauss4,
            full_low_groups=groups,
            fixed_A0_loop_metric=C0[:4,:4].tolist(),
            Gauss_reduced_loop_metric=corrected.tolist(),
            Gauss_metric_correction_norm=float(np.linalg.norm(C0[:4,:4]-corrected)),
            scope="All135unitcell edge coordinates and26nonconstant temporal modes; zero external deck momentum. Four low poles of tree gauge plus scalar-loop quadratic action. Not a full interacting quantum-gauge or nonzero-momentum continuum result.")


def produce():
    rows=[]
    for n in (2,3):
        x=FullResponse((n,n,n,2),.8)
        options=[]
        for name in ("basis105","all1287"):
            x.use_magnetic(name)
            options.append(dict(name=name,results=[x.modes(g) for g in (.5,1.)]))
        rows.append(dict(sizes=list(x.sizes),mass=x.mass,
            transverse_dimension=109,optical_dimension=105,temporal_nonconstant_dimension=26,
            static_gauge_residual=x.static_gauge_residual,
            direct_current_density_commutator_residual=x.commutator_residual,
            direct_temporal_Ward_controls=x.ward_controls,
            static_harmonic_Hessian=x.K[:4,:4].tolist(),
            restored_profile_invariance=x.profile_invariance(),
            magnetic_symmetry=x.magnetic_symmetry,magnetic_options=options))
    paths=[str(Path(__file__).relative_to(ROOT)),"analysis/toe_20261108_coupled_holonomy_response.py",
           "data/PART_20261023_NATIVE_ZERO_HOLONOMY_FACE_COMPLETION.json",
           "data/w33_pass11991_native_four_period_cover.json"]
    return dict(status="NATIVE_ZERO_EXTERNAL_MOMENTUM_FULL_EDGE_TEMPORAL_GAUSS_SCALAR_KERNEL_NOT_TOE",
        rows=rows,
        direct_density_integrals="I0=p/[2ab(p²+nu²)], I1=(b-a)nu/[2ab(p²+nu²)], I2=p(4ab+nu²)/[2ab(p²+nu²)]. Temporal contact p/(2ab) minus I2 yields (a-b)²p/[2ab(p²+nu²)]. Mixed current/density bubble gives i nu Z_PL.",
        Gauss_reduction="Spatial basis=(4harmonic,105coexact,26gradients). On zero external deck momentum remove26temporal A0 modes by Schur: Eeff=E_PP-E_PL E_LL^-1 E_LP, E=bare electric+Z(s). Then eliminate105optical coordinates below their gap. Uniform temporal charge is the redundant neutral-vacuum gauge mode.",
        ordering="For harmonic representatives,0<=Zeff<=Z_HH in4holonomy truncation, so fixedA0 roots<=Gauss4 roots<=tree roots. Optical relaxation further lowers the4low roots relative to Gauss4. Net shift versus the earlier clamped model need not have one sign.",
        limits="Supplied scalar/gauge action, torus sizes,mass,g,beta and continuous time. Zero external deck momentum only. Higher gauge loops, full charged fermion/scalar inventory, nonzeroexternal-momentum propagation, physical3+1 continuum, radius dynamics, relic/cosmological fit, measured units and TOE not supplied.",
        input_raw_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths})


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--out",default="data/toe_20261108_native_gauss_response.json")
    a=p.parse_args();d=produce()
    (ROOT/a.out).write_text(json.dumps(d,indent=2)+"\n",encoding="utf-8")
    print(json.dumps([dict(sizes=r["sizes"],Ward=r["direct_temporal_Ward_controls"],magnetic_symmetry=r["magnetic_symmetry"],modes=[dict(name=z["name"],frequencies=[x["full_gauss_and_optical_squared_frequencies"] for x in z["results"]]) for z in r["magnetic_options"]]) for r in d["rows"]]))
