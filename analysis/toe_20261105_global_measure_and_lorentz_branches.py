"""Finite determinant-line and analytically continued Regge controls.

Neither a local all-configuration chiral measure nor nonlinear ADM closure.
"""
import pathlib,json,itertools,math,sys
import numpy as np
R=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'analysis'))
import toe_20261103_mechanism_four_dimensional_overlap as ov

def toron_chern(L=2,N=10,charge=1):
    frames={};gap=100.;rank=None
    xs=list(itertools.product(range(L),repeat=4))
    for a,b in itertools.product(range(N),repeat=2):
        U=ov.links(L,0,1)**charge
        for j,x in enumerate(xs):
            if x[0]==L-1:U[j,0]*=np.exp(2j*np.pi*charge*a/N)
            if x[1]==L-1:U[j,1]*=np.exp(2j*np.pi*charge*b/N)
        D,G,hat,lam=ov.operator(U,L)
        w,V=np.linalg.eigh((np.eye(len(hat))-hat)/2)
        F=V[:,w>.5];frames[a,b]=F;gap=min(gap,float(min(abs(lam))))
        if rank is None:rank=F.shape[1]
        assert F.shape[1]==rank
    links={};min_singular=1.
    for a,b in itertools.product(range(N),repeat=2):
        for direction in [0,1]:
            c,d=((a+1)%N,b)if direction==0 else(a,(b+1)%N)
            z=frames[a,b].conj().T@frames[c,d]
            sign,logabs=np.linalg.slogdet(z)
            assert abs(sign)>0
            links[a,b,direction]=sign
            min_singular=min(min_singular,float(np.linalg.svd(z,compute_uv=False).min()))
    phases=[]
    for a,b in itertools.product(range(N),repeat=2):
        phases.append(float(np.angle(links[a,b,0]*links[(a+1)%N,b,1]/links[a,(b+1)%N,0]/links[a,b,1])))
    return dict(L=L,grid=N,charge=charge,background_flux34=1,projector_rank=rank,
        kernel_gap_min=gap,frame_neighbor_min_singular=min_singular,
        whole_parameter_torus_gap_lower_bound=gap-2*np.pi*abs(charge)/N,
        gap_bound_scope='Each toron derivative of H has operator norm at most|q|: the differentiated boundary hopping uses complementary gamma projectors on opposite endpoint blocks. Nearest mesh point differs by at most pi/N per coordinate; Weyl bound gives gap_sample_min-2pi|q|/N. Numerical eigenvalue rounding must be allowed; no interval eigensolver used. The method already belongs to12030; here applied to the4D flux family.',
        first_Chern_sum=sum(phases)/(2*np.pi),max_parameter_plaquette_angle=max(map(abs,phases)))

P=np.vstack((np.zeros(4),np.diag([2.,1.,1.,1.])))
P=np.vstack((P,P.mean(axis=0)))
cells=[tuple([5]+[i for i in range(5)if i!=omit])for omit in range(5)]
edges=list(itertools.combinations(range(6),2));tri=sorted({tuple(sorted(t))for c in cells for t in itertools.combinations(c,3)})
internal=[t for t in tri if 5 in t];outer=[t for t in tri if 5 not in t]
normals=np.vstack((-np.ones(4),np.eye(4)))

def continue_action(perturb=None,steps=160,epsilon=1e-7,positions=None,with_gradient=False):
    pts=P if positions is None else positions
    if perturb is None:perturb=np.zeros(5)
    previous_roots={};previous_angles={};changes=0
    for tick in range(steps+1):
        z=np.exp(-1j*(np.pi-epsilon)*tick/steps)
        squared={e:(z*(pts[e[0],0]-pts[e[1],0])**2+sum((pts[e[0],j]-pts[e[1],j])**2 for j in [1,2,3]))for e in edges}
        for i in range(5):squared[i,5]+=perturb[i]
        def d(i,j):return 0 if i==j else squared[tuple(sorted((i,j)))]
        def root(key,x):
            r=np.sqrt(complex(x))
            if key in previous_roots and abs(-r-previous_roots[key])<abs(r-previous_roots[key]):r=-r
            previous_roots[key]=r;return r
        areas={}
        for t in tri:
            a,b,c=t;u=d(a,b);v=d(a,c);w=d(b,c)
            areas[t]=root(('area',t),u*v-((u+v-w)/2)**2)/2
        sums={t:0j for t in tri}
        for ci,c in enumerate(cells):
            G=np.array([[(d(c[0],i)+d(c[0],j)-d(i,j))/2 for j in c[1:]]for i in c[1:]],complex)
            normal=normals@np.linalg.inv(G)@normals.T
            roots=[root(('normal',ci,i),normal[i,i])for i in range(5)]
            for t0 in itertools.combinations(c,3):
                t=tuple(sorted(t0));i,j=[k for k in range(5)if c[k]not in t]
                cosine=-normal[i,j]/(roots[i]*roots[j]);angle=np.arccos(complex(cosine));key=(ci,t)
                if key in previous_angles:
                    candidates=[sg*angle+2*np.pi*k for sg in [1,-1]for k in [-2,-1,0,1,2]]
                    selected=min(candidates,key=lambda a:abs(a-previous_angles[key]))
                    if abs(selected-angle)>1e-9:changes+=1
                    angle=selected
                previous_angles[key]=angle;sums[t]+=angle
    deficit={t:2*np.pi-sums[t]for t in internal}
    action=sum(areas[t]*deficit[t]for t in internal)+sum(areas[t]*(np.pi-sums[t])for t in outer)
    if with_gradient:
        grad=np.zeros(5,complex)
        for i in range(5):
            for t in internal:
                if i not in t:continue
                k=next(j for j in t if j not in [i,5]);u=d(5,i);v=d(5,k);w=d(i,k)
                grad[i]+=deficit[t]*(v-(u+v-w)/2)/(8*areas[t])
        return action,deficit,changes,grad
    return action,deficit,changes

def regge_controls():
    S,de,changes=continue_action();h=2e-5
    gradient=np.array([(continue_action(h*x)[0]-continue_action(-h*x)[0])/(2*h)for x in np.eye(5)])
    rng=np.random.default_rng(291);motion=[]
    for _ in range(3):
        pos=P.copy();pos[5]+=rng.normal(size=4)*.002
        sm,dm,_=continue_action(positions=pos)
        motion.append(dict(action_change=abs(sm-S),max_deficit=max(map(abs,dm.values()))))
    refined=continue_action(steps=320)[0]
    # Off-shell edge variation creates curvature. No reference subtraction.
    curved,cd,_=continue_action(np.array([.001,0,0,0,0]))
    analytic=continue_action(with_gradient=True)[3]
    matrices=[]
    for amplitude in [0.,.001]:
        base=np.array([amplitude,0,0,0,0])
        H=np.column_stack([(continue_action(base+h*x,with_gradient=True)[3]-continue_action(base-h*x,with_gradient=True)[3])/(2*h)for x in np.eye(5)])
        J=np.array([2*np.diag([-1.,1.,1.,1.])@(P[5]-P[i])for i in range(5)])
        matrices.append(dict(perturbation=amplitude,Hessian_singular_values=np.linalg.svd(H,compute_uv=False).tolist(),Hessian_times_flat_vertex_J_norm=float(np.linalg.norm(H@J)),complex_symmetry_defect=float(np.linalg.norm(H-H.T))))
    assert np.linalg.norm(analytic-gradient)<1e-6
    return dict(action_flat=[S.real,S.imag],flat_hinge_max_deficit=max(map(abs,de.values())),
        raw_action_flat_FD_gradient_norm=float(np.linalg.norm(gradient)),gradient=[[x.real,x.imag]for x in gradient],
        branch_changes=changes,continuation_160_vs_320_action_error=abs(S-refined),flat_vertex_motion_controls=motion,
        Schlafli_vs_FD_gradient_error=float(np.linalg.norm(analytic-gradient)),flat_and_offshell_Hessian_controls=matrices,
        off_flat_max_deficit=max(map(abs,cd.values())),off_flat_action_change=abs(curved-S),
        prescription='Continue the complete Euclidean Regge+boundary action along metric diag(exp(-i alpha),1,1,1), alpha0..pi-epsilon. Track each square root and arccos sheet continuously; include actual boundary exterior angles. No flat-value subtraction. Geometry is one Lorentzian1to5 simplex refinement, not the prior nine-simplex action.',
        limits='A finite complex continuation on a declared sheet and time orientation. Correct flat stationarity and geometric-motion Ward controls are necessary, not a proof of reflection positivity, causal quantum dynamics, all-triangulation uniqueness or nonlinear Hamiltonian constraint closure. No lapse/shift Poisson algebra is constructed.',
        sources=['https://arxiv.org/abs/2303.07367','https://arxiv.org/abs/0905.1670'])

def build():
    rows=[toron_chern(2,N,q)for N,q in [(8,1),(12,1),(8,-1),(12,-1),(40,1)]]
    regge=regge_controls()
    return dict(status='EXECUTED_GLOBAL_MEASURE_AND_LORENTZ_BRANCH_TESTS',toron_rows=rows,Regge=regge,
        measure_boundary='Actual4D Wilson/overlap projector family over two periodic boundary-link torons, with flux34. Discrete determinant-link Chern calculation; mesh/gap/overlap diagnostics exported. A nonzero Chern number obstructs one global smooth basis for that representation. Opposite-charge sums test vectorlike cancellation only. No local reconstruction current, anomaly-free chiral full-sector measure or continuum limit follows from this finite test.',
        chiral_inventory_limit='The earlier chiral charges(-9,-5,-1,7,8) need much finer spatial/parameter lattices to avoid charge-amplified flux aliasing. They are not falsely certified by a coarse-torus zero. A full SM/non-Abelian construction remains open.',
        prior=['analysis/toe_20261103_mechanism_four_dimensional_overlap.py','analysis/toe_20261103_mechanism_sector_reference.py','analysis/w33_pass12026_12033_theta_soft_threshold_connections.py:12030','analysis/w33_pass12034_12038_joint_mechanisms.py:12038','analysis/toe_20261105_nine_simplex_regge_action_hessian_lorentz_diagnostic.py'],
        literature=['https://arxiv.org/abs/hep-lat/9811032','https://arxiv.org/abs/2303.07367'],
        boundary='Both fronts executed as explicit finite necessary controls; neither global chiral measure nor full nonlinear GR is solved.')
if __name__=='__main__':
    out=build();(R/'data/toe_20261105_global_measure_and_lorentz_branches.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(out['status'],[(x['grid'],x['charge'],x['first_Chern_sum'])for x in out['toron_rows']],out['Regge'],flush=True)
